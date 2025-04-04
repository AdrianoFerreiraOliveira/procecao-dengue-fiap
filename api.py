from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Carrega o modelo e as features salvas no .pkl
modelo, features = joblib.load('modelo/modelo_dengue.pkl')

# Cria o schema de input dinamicamente baseado nas features
class InputDados(BaseModel):
    ign_branco: float
    analfabeto: float
    serie_1a4_incompleta: float
    serie_4_completa: float
    serie_5a8_completa: float
    fundamental_completo: float
    medio_completo: float
    medio_incompleto: float
    superior_incompleto: float
    superior_completo: float
    nao_se_aplica: float
    idade_menor1: float
    idade_1a4: float
    idade_5a9: float
    idade_10a14: float
    idade_15a19: float
    idade_20a39: float
    idade_40a59: float
    idade_60a64: float
    idade_65a69: float
    idade_70a79: float
    idade_80mais: float

@app.get("/")
def read_root():
    return {"message": "🚀 API do Modelo de Previsão de Dengue rodando!"}

@app.post("/prever")
def prever(input_dados: InputDados):
    # Converte para DataFrame e garante ordem correta das colunas
    df_entrada = pd.DataFrame([input_dados.dict()])
    df_entrada = df_entrada[features]

    # Faz a previsão
    previsao = modelo.predict(df_entrada)

    return {"casos_previstos": int(previsao[0])}
