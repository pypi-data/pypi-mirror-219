import io
import io
import pandas as pd
from datetime import datetime


class MigratorRedshiftReader:
    def __init__(self, s3_credentials, struct, migrator_redshift_connector):
        self.struct = struct
        self.s3_credentials = s3_credentials
        self.migrator_redshift_connector = migrator_redshift_connector

    def convert_types(self, df):
        for c in self.struct["columns"]:
            case_target_type = {
                "varchar": "str",
                "text": "str",
                "timestamp": "datetime64[ns]",
                "super": "str",
            }

            if c["target_type"] in case_target_type.keys():
                df[c["source_name"]] = df[c["source_name"]].astype(
                    case_target_type[c["target_type"]]
                )
                if case_target_type[c["target_type"]] == "str":
                    df[c["source_name"]].replace("None", "", inplace=True)

        return df

    def get_incremental_statement(self):
        if (
            "source_incremental_column" in self.struct.keys()
            and self.struct["source_incremental_column"] is not None
            and "target_incremental_column" in self.struct.keys()
            and self.struct["target_incremental_column"] is not None
        ):
            self.migrator_redshift_connector.connect_target()
            sql = f"""
                select max("{self.struct["target_incremental_column"]}") as max_value
                from {self.struct["target_relation"]}
            """

            cursor = self.migrator_redshift_connector.target_conn.cursor()

            cursor.execute(sql)
            result = cursor.fetchall()

            if len(result) == 0 or result[0][0] is None:
                sql_return = ""
            else:
                for c in self.struct["columns"]:
                    if c["target_name"] == self.struct["target_incremental_column"]:
                        target_type = c["target_type"]

                if (
                    target_type == "int"
                    or target_type == "bigint"
                    or target_type == "numeric"
                    or target_type == "float"
                    or target_type == "double"
                ):
                    sql_return = f'and "{self.struct["source_incremental_column"]}" > {result[0][0]}'
                else:
                    sql_return = f'and "{self.struct["source_incremental_column"]}" > \'{result[0][0]}\''

            cursor.close()
            self.migrator_redshift_connector.target_conn.close()

            return sql_return

        else:
            return ""

    def get_columns_source(self):
        columns = []
        for c in self.struct["columns"]:
            if (
                c["target_type"] == "super"
                or c["target_type"] == "varchar"
                or c["target_type"] == "text"
            ):
                columns.append(
                    f'substring("{c["source_name"]}"::varchar,0,60000) as "{c["source_name"]}"'
                )
            else:
                columns.append(f'"{c["source_name"]}"')
        return ",".join(columns)

    def get_order_by_sql_statement(self):
        if (
            "source_incremental_column" in self.struct.keys()
            and self.struct["source_incremental_column"] is not None
        ):
            return f' order by "{self.struct["source_incremental_column"]}" asc'
        else:
            return ""

    def get_sql_statement(self):
        sql = f"""
            select {self.get_columns_source()} 
            from {self.struct["source_relation"]} 
            where 1=1
            {self.get_incremental_statement()} 
            {self.get_order_by_sql_statement()}
        """
        print(f"SQL Statement: {sql}")
        return sql

    def save_data_to_s3(self):
        self.migrator_redshift_connector.connect_s3()
        self.migrator_redshift_connector.connect_source()

        sql = self.get_sql_statement()

        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        idx = 1
        path_file = None

        for chunk_df in pd.read_sql(
            sql,
            self.migrator_redshift_connector.source_conn,
            chunksize=self.struct["read_batch_size"],
        ):
            if len(chunk_df) != 0:
                path_file = f'{self.s3_credentials["path"]}{self.struct["database"]}/{self.struct["source_relation"]}/{time}/{idx}.parquet'
                print(f"Saving file {path_file}")

                buffer = io.BytesIO()
                chunk_df = self.convert_types(chunk_df)

                chunk_df.to_parquet(buffer, index=False, engine="pyarrow")
                self.migrator_redshift_connector.s3_session.Object(
                    self.s3_credentials["bucket"],
                    path_file,
                ).put(Body=buffer.getvalue())

                buffer.close()
                idx = idx + 1

        self.migrator_redshift_connector.close_source()

        if path_file is None:
            return None
        else:
            return f's3://{self.s3_credentials["bucket"]}/{self.s3_credentials["path"]}{self.struct["database"]}/{self.struct["source_relation"]}/{time}/'
