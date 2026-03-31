import os
import logging
import mlflow

logger = logging.getLogger(__name__)


def load_mlflow_model():
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    run_id = os.getenv("RUN_ID", "a835a604da97495fa2d37b1372f3c97e")

    try:
        logger.info(f"Conectando ao MLflow em {mlflow_uri}...")
        mlflow.set_tracking_uri(mlflow_uri)

        logger.info(f"Baixando artefatos do modelo (Run ID: {run_id})...")
        model_uri = f"runs:/{run_id}/model"

        model = mlflow.sklearn.load_model(model_uri)
        logger.info("Modelo carregado com sucesso!")
        return model, run_id

    except Exception as e:
        logger.error(f"Falha ao carregar o modelo do MLflow: {e}")
        raise e