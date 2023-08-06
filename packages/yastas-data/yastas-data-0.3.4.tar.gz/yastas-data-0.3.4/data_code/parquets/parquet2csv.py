import pandas as pd

def parquet_csv(parquet_file, csv_file):

    # Leer el archivo Parquet en un DataFrame de pandas
    df = pd.read_parquet(parquet_file)

    # Guardar el DataFrame en formato CSV
    df.to_csv(csv_file, index=False)
env="dev"
domain="AB"
table="streaming_movimientos"
step="raw"
root_parquet = f"gs://yas-sii-inp-ext-{step}-{env}"
parquet_query = f"{root_parquet}/{domain}/parquet_schema/parquet-schema-{domain}-{step}-{table}-00000-of-00001.txt"
parquet_raw = f"{root_parquet}/{domain}/{step}_{table}-00000-of-00001.parquet"
print(f"query: {parquet_query}\n raw: {parquet_raw}" )

# parquet ="C:\\Users\\e-ajuareza\\Documents\\Yastas\\yas-cierre-sii\\params\\streaming\\parquet\\raw_streaming_movimientos-00000-of-00001.parquet"
# file_name =  parquet.split('\\')[-1].split('\\')[0]
# csv =f"C:\\Users\\e-ajuareza\\Documents\\Yastas\\yas-cierre-sii\\params\\streaming\\parquet\\csv\\{file_name}.csv"
# print(parquet,csv)
# parquet_csv(parquet,csv)


