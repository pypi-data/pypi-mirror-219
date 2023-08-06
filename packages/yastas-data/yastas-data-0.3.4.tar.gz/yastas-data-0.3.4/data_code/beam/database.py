import apache_beam as beam
from data_code.gcp.sql import Database
import time
class GetQuery(beam.DoFn):
    def __init__(self, host, port, database, query, string_conn, project_id, secret_user, secret_password):
        self.host=host
        self.port=port
        self.database=database
        self.query = query
        self.string_conn = string_conn
        self.project_id = project_id
        self.secret_user = secret_user
        self.secret_password = secret_password
        self.postgres = Database(self.host,self.port,self.database,self.secret_user,self.secret_password, self.project_id)

    def setup(self):
        self.conn = self.postgres.get_connection()
        self.postgres.raise_proxy(self.string_conn)
        

    def process(self, element):
        query_result=self.postgres.execute_query(self.conn, query=self.query)
        self.postgres.close_connection(self.conn)
        self.postgres.shut_down_proxy()
        return query_result
        

    def teardown(self):
        # Investigate functionality
        pass

