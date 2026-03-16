import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
from dotenv import load_dotenv
load_dotenv()
os.environ["JAVA_HOME"] = os.getenv("JAVA_HOME")

MINIO_ENDPOINT = os.getenv("MLFLOW_S3_ENDPOINT_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")

print(f"DEBUG - Endpoint: {MINIO_ENDPOINT}")
print(f"DEBUG - Access Key: {MINIO_ACCESS_KEY}")
print(f"DEBUG - Secret Key: {MINIO_SECRET_KEY}")
if not MINIO_SECRET_KEY:
    raise ValueError("A senha do MinIO está vazia! O Python não leu o .env direito.")

def create_spark_session():
    return SparkSession.builder \
        .appName("OpenLake-Ingestion") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.1,org.apache.hadoop:hadoop-aws:3.3.4") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT) \
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY) \
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

def main():
    spark = create_spark_session()

    # simular a leitura de dados
    data = [("user1", 25, "SP"), ("user2", 25, "SP"), ("user3", 25, "SP")]
    df = spark.createDataFrame(data, ["name", "age", "state"])

    df = df.withColumn("timestamp", current_timestamp())

    # salvar no minIO "s3a://nome-do-bucket/caminho
    target_path = "s3a://lakehouse/silver/users_table"

    print(f"Salvando dados em formato Delta no MinIO: {target_path}")

    df.write.format("delta").mode("overwrite").save(target_path)

    df_check = spark.read.format("delta").load(target_path)
    df_check.show()


if __name__ == "__main__":
    main()