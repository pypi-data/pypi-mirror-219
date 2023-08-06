from data_code.gcp.secrets import get_secret
import psycopg2
import logging
import os
import time
class Proxy():
    """Funcionalidades relacionadas al proxy para lograr comunicación con bases de datos.
    """
    def logprint_i(self,msg):
        logging.info(msg)
        print(msg)

    def raise_proxy(self, string_connection:str):
        self.logprint_i("Inicia levantacion del proxy.....")
        PROXYUP_COMMANDS = [
            f"rm -fr DTF && mkdir DTF && cd DTF && \
            wget --progress=bar:force:noscroll https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy && ls -la cloud_sql_proxy && \
            chmod 755 cloud_sql_proxy && ls -la cloud_sql_proxy && pwd && ls -latrh && \
            nohup ./{string_connection} -ip_address_types=PRIVATE  & \&& \
            sleep 5 ",
        ]

        self.logprint_i("Inicia descarga proxy")
        for command in PROXYUP_COMMANDS:
            os.system(command)
            time.sleep(3)
        self.logprint_i("termina levantacion del proxy.....")

        self.logprint_i("proxy_up_executed")
    
    def shut_down_proxy(self):
        #TODO: Crear la baja del proxy para evitar vulnerabilidades.
        os.system("rm -fr DTF")
        print("\t\t\t\tShut down proxy")

class Database(Proxy):
    """_summary_

    Args:
        Proxy (Proxy): _description_
    """
    def __init__(self, host, port, database, secret_user, secret_pswd, project_id):
        self.host = host
        self.port = port
        self.database_name = database
        user = get_secret(secret_user,project_id)
        password = get_secret(secret_pswd,project_id)
        self.user = user
        self.password = password
        
    def get_connection(self):
        # Establecer la conexión con la base de datos
        connection = psycopg2.connect(
            host=self.host,
            port=self.port, 
            database=self.database_name,
            user=self.user,
            password=self.password
        )
        return connection
    
    def get_tables(self, connection):

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()
        

        # Obtener los nombres de las tablas
        cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                    """)

        # Obtener los resultados
        filas = cursor.fetchall()

        # Procesar los resultados
        tablen="Tablenames"
        print(f"\n/ {tablen.upper():^20} \\")
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        
        for fila in filas:
            print(f"| {fila[0]:^20} |")
            print("________________________")
        print("\n")
        # Cerrar el cursor y la conexión
        #cursor.close()
        
    def execute_query(self, connection, query:str):

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Ejecutar una consulta de ejemplo
        cursor.execute(query)

        # Obtener los resultados de la consulta
        query_result = cursor.fetchall()

        # Procesar los resultados
        # for fila in filas:
        #     print(fila)

        # Cerrar el cursor y la conexión
        cursor.close()
        return query_result

    def close_connection(self, connection):
        # Cerrar el cursor y la conexión
        connection.close()

