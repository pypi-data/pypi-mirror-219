import boto3
import psycopg2
from sqlalchemy import create_engine

from maisaedu_utilities_prefect.dw import get_red_credentials


class MigratorRedshiftConnector:
    def __init__(
        self,
        env,
        s3_credentials,
        source_credentials,
    ):
        self.source_credentials = source_credentials
        self.s3_credentials = s3_credentials
        self.env = env
        self.iam_role = "arn:aws:iam::977647303146:role/service-role/AmazonRedshift-CommandsAccessRole-20220714T104138"

    def connect_target(self):
        red_credentials = get_red_credentials(self.env)
        self.target_conn = psycopg2.connect(
            host=red_credentials["host"],
            database=red_credentials["database"],
            user=red_credentials["user"],
            password=red_credentials["password"],
            port=red_credentials["port"],
        )

    def close_target(self):
        self.target_conn.close()

    def connect_s3(self):
        session = boto3.Session(
            aws_access_key_id=self.s3_credentials["access-key"],
            aws_secret_access_key=self.s3_credentials["secret-access-key"],
            region_name=self.s3_credentials["region"],
        )

        self.s3_session = session.resource("s3")

    def connect_source(self):
        engine = create_engine(
            f"postgresql+psycopg2://{self.source_credentials['user']}:{self.source_credentials['password']}@{self.source_credentials['host']}:{self.source_credentials['port']}/{self.source_credentials['database']}"
        )
        self.source_conn = engine.connect().execution_options(stream_results=True)

    def close_source(self):
        self.source_conn.close()
