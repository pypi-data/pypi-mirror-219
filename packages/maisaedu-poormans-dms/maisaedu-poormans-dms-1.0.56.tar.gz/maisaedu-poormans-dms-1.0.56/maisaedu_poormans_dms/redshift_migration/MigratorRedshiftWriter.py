class MigratorRedshiftWriter:
    def __init__(self, struct, migrator_redshift_connector):
        self.struct = struct
        self.migrator_redshift_connector = migrator_redshift_connector

    def get_serialization_if_has_super(self):
        for c in self.struct["columns"]:
            if c["target_type"] == "super":
                return "SERIALIZETOJSON"
        return ""

    def create_statement_upsert(self, temp_target_relation):
        statement_upsert = ""
        for c in self.struct["columns_upsert"]:
            statement_upsert = (
                statement_upsert
                + f'and {self.struct["target_relation"]}.{c} = {temp_target_relation}.{c} '
            )

        return statement_upsert

    def save_data(self, is_upsert, target_cursor, path_files_to_insert):
        temp_target_relation = f'"temp_{self.struct["target_relation"]}"'

        target_cursor.execute(
            f"""
                    CREATE TEMP TABLE {temp_target_relation} (LIKE {self.struct["target_relation"]});
                """
        )

        target_cursor.execute(
            f"""
                COPY {temp_target_relation}
                FROM '{path_files_to_insert}' 
                IAM_ROLE '{self.migrator_redshift_connector.iam_role}'
                FORMAT AS PARQUET
                {self.get_serialization_if_has_super()};
            """
        )
        self.migrator_redshift_connector.target_conn.commit()

        if is_upsert is True:
            target_cursor.execute(
                f"""
                    DELETE FROM {self.struct["target_relation"]} 
                    USING {temp_target_relation} 
                    WHERE 1=1 
                        {self.create_statement_upsert(temp_target_relation)}    
                    ;
                """
            )
        else:
            target_cursor.execute(
                f"""
                    DELETE FROM {self.struct["target_relation"]};
                """
            )

        target_cursor.execute(
            f"""
                INSERT INTO {self.struct["target_relation"]}
                SELECT * FROM {temp_target_relation};
            """
        )

        self.migrator_redshift_connector.target_conn.commit()

        target_cursor.execute(f"""DROP TABLE {temp_target_relation};""")

        self.migrator_redshift_connector.target_conn.commit()

    def save_to_redshift(self, path_files_to_insert):
        self.migrator_redshift_connector.connect_target()
        cursor = self.migrator_redshift_connector.target_conn.cursor()

        if (
            len(self.struct["columns_upsert"]) == 0
            or self.struct["columns_upsert"] is None
            or "columns_upsert" not in self.struct.keys()
        ):
            is_upsert = False
        else:
            is_upsert = True

        self.save_data(
            target_cursor=cursor,
            path_files_to_insert=path_files_to_insert,
            is_upsert=is_upsert,
        )

        cursor.close()
        self.migrator_redshift_connector.target_conn.close()
