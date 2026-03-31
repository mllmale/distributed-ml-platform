from pydantic import BaseModel, Field

class UserDataInput(BaseModel):
    age: int = Field(..., description="Idade do usuário", gt=0, le=120)
    score: int = Field(..., description="Pontuação do usuário", ge=0, le=100)

class PredictionOutput(BaseModel):
    status: str
    previsao: int
    modelo_versao: str