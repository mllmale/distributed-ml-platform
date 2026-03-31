from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ml.src.utils import setup_logging, set_aws_credentials
from .schemas import UserDataInput, PredictionOutput
from .model_loader import load_mlflow_model

logger = setup_logging()
set_aws_credentials()

ml_model = None
current_run_id = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global ml_model, current_run_id
    logger.info("Iniciando a API OpenLake...")
    ml_model, current_run_id = load_mlflow_model()
    yield
    logger.info("Desligando a API...")
    ml_model = None


app = FastAPI(title="OpenLake Model API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.post("/predict", response_model=PredictionOutput)
def predict(data: UserDataInput):
    if not ml_model:
        raise HTTPException(status_code=503, detail="Modelo offline.")

    try:
        prediction = ml_model.predict([[data.age, data.score]])
        return PredictionOutput(
            status="sucesso",
            previsao=int(prediction[0]),
            modelo_versao=current_run_id
        )
    except Exception as e:
        logger.error(f"Erro na inferência: {e}")
        raise HTTPException(status_code=500, detail="Erro interno.")