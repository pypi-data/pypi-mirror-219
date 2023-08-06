from .MigratorRedshiftConnector import MigratorRedshiftConnector
from .MigratorRedshiftReader import MigratorRedshiftReader
from .MigratorRedshiftWriter import MigratorRedshiftWriter


class MigratorRedshift:
    def __init__(
        self,
        env=None,
        s3_credentials=None,
        struct=None,
        source_credentials=None,
    ):
        self.migrator_redshift_connector = MigratorRedshiftConnector(
            env=env,
            s3_credentials=s3_credentials,
            source_credentials=source_credentials,
        )

        self.migrator_redshift_reader = MigratorRedshiftReader(
            s3_credentials=s3_credentials,
            struct=struct,
            migrator_redshift_connector=self.migrator_redshift_connector,
        )

        self.migrator_redshift_writer = MigratorRedshiftWriter(
            struct=struct,
            migrator_redshift_connector=self.migrator_redshift_connector,
        )

        self.source_credentials = source_credentials
        self.struct = struct
        self.s3_credentials = s3_credentials
        self.env = env

    def save_data_to_s3(self):
        return self.migrator_redshift_reader.save_data_to_s3()

    def save_to_redshift(self, path_files_to_insert):
        return self.migrator_redshift_writer.save_to_redshift(path_files_to_insert)

    def get_structs_source_to_target(self, database, tables="all"):
        self.migrator_redshift_connector.connect_target()

        statement = f" and database = '{database}'"

        if tables != "all":
            statement = f"""
            {statement} and target_relation in ({tables})
            """
        else:
            statement = f" {statement} and is_active is true"

        cur = self.migrator_redshift_connector.target_conn.cursor()
        cur.execute(
            f"""
                select 
                    id, 
                    source_relation,
                    source_engine,
                    target_relation,
                    source_incremental_column,
                    target_incremental_column,
                    read_batch_size,
                    incremental_interval_delta,
                    database
                from 
                    dataeng.relations_extraction
                where
                    1=1 
                    {statement};
            """
        )

        structs = []

        relations_extraction = cur.fetchall()
        for r in relations_extraction:
            s = {
                "source_relation": r[1],
                "source_engine": r[2],
                "target_relation": r[3],
                "source_incremental_column": r[4],
                "target_incremental_column": r[5],
                "read_batch_size": r[6],
                "incremental_interval_delta": r[7],
                "database": r[8],
                "columns": [],
                "columns_upsert": [],
            }
            cur.execute(
                f"""
                    select 
                        source_name, 
                        target_name, 
                        source_type, 
                        target_type,
                        is_upsert
                    from
                        dataeng.relations_colums_extraction
                    where
                        relation_id = {r[0]}
                        and is_active is true
                    order by source_order asc;
                """
            )
            columns = cur.fetchall()
            for c in columns:
                s["columns"].append(
                    {
                        "source_name": c[0],
                        "target_name": c[1],
                        "source_type": c[2],
                        "target_type": c[3],
                    }
                )
                if c[4] is True:
                    s["columns_upsert"].append(c[1])

            structs.append(s)

        self.migrator_redshift_connector.close_target()

        return structs
