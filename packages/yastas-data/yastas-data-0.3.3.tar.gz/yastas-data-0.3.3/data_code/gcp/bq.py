from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import ast
import subprocess

def create_or_evaluate_bq_table(table_id:str,raw_parquet:str)->dict:
    """Verifica si existe la tabla y extrae los metadatos; en caso de que no exista la crea con base en el parquet de raw.

    Args:
        table (str): Nombre de la tabla.
        raw_parquet (str): Ruta del parquet.

    Returns:
        dict: Diccionario con la metadata de la tabla.
    """
    try:
        client = bigquery.Client()
        client.get_table(table_id.replace(':','.'))  # Make an API request.
        print(f"Table: {table_id} already exists.")
        metadata_table_bq = get_metadata(table_id)
        return metadata_table_bq
    except NotFound:
        print(f"Table: {table_id} not found. \nCreating it with parquet: {raw_parquet}")
        #TODO: bq load --autodetect --source_format=PARQUET <project_id>:<dataset>.<table_name> gs://<bucket_name>/<path_to_parquet_file>
        subprocess.run(["bq","load","--autodetect", "--source_format=PARQUET", table_id, raw_parquet], capture_output=True, shell=True).stdout
        print(f'{table_id} was created succesfully')
        metadata_table_bq = get_metadata(table_id)
        return metadata_table_bq

def get_metadata(table_id:str)->dict:
    """_summary_

    Args:
        table_id (str): _description_

    Returns:
        dict: _description_
    """
    metadata_table_bq = subprocess.run(["bq","show","--format=prettyjson", table_id], capture_output=True, shell=True).stdout
    metadata_table_bq = ast.literal_eval(metadata_table_bq.decode('UTF-8'))
    return metadata_table_bq