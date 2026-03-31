import boto3
import os


def create_lakehouse_bucket():
    """Conecta no MinIO e cria o bucket principal se ele não existir."""
    endpoint = os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000")
    access_key = os.getenv("AWS_ACCESS_KEY_ID", "euzinha")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY", "senhazona123")
    bucket_name = "lakehouse"

    print(f"Conectando ao Storage em {endpoint}...")

    s3_client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ O bucket '{bucket_name}' já existe e está pronto para uso.")
    except Exception:
        print(f"🏗 Criando o bucket '{bucket_name}'...")
        s3_client.create_bucket(Bucket=bucket_name)
        print("Bucket criado com sucesso!")


if __name__ == "__main__":
    create_lakehouse_bucket()