import os
import mlflow
import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import urllib3

# Suprime avisos chatos de conexão
urllib3.disable_warnings()

load_dotenv()

# Configuração do MLflow
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("MINIO_ROOT_USER")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("MINIO_ROOT_PASSWORD")

# O MLflow precisa dessa variável de ambiente para usar o S3
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

mlflow.set_experiment("OpenLake_Classificacao_Usuarios")


def main():
    #mlflow.sklearn.autolog()

    with mlflow.start_run() as run:
        print(f"🚀 Iniciando experimento. Run ID: {run.info.run_id}")

        # Como não instalamos o pacote Pandas-Delta para simplificar,
        # vamos usar um dataset local simulando a saída da ETL por enquanto
        print("📊 Carregando dados da Silver Layer...")
        df = pd.DataFrame({
            "age": [25, 30, 22, 35, 40, 28, 50, 18],
            "score": [80, 90, 75, 85, 95, 78, 88, 60],
            "comprou": [1, 1, 0, 1, 1, 0, 1, 0]
        })

        X = df[["age", "score"]]
        y = df["comprou"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("🤖 Treinando Random Forest...")
        model = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
        model.fit(X_train, y_train)

        previsoes = model.predict(X_test)
        acuracia = accuracy_score(y_test, previsoes)

        mlflow.log_metric("acuracia_customizada", acuracia)
        print(f"✅ Treino concluído! Acurácia: {acuracia}")

        print("📦 Fazendo upload do modelo para o MinIO...")
        mlflow.sklearn.log_model(model, "model")

        print(f"✅ Treino concluído! Acurácia: {acuracia}")


if __name__ == "__main__":
    main()