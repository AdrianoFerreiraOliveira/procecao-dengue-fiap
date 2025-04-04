import streamlit as st
import requests

st.set_page_config(page_title="Dashboard de Previsão de Dengue", layout="wide")
st.title("Dashboard de Previsão de Casos de Dengue")
st.markdown("Preencha os campos abaixo para realizar uma previsão.")

# Lista de features
features = [
    'ign_branco',
    'analfabeto',
    'serie_1a4_incompleta',
    'serie_4_completa',
    'serie_5a8_completa',
    'fundamental_completo',
    'medio_completo',
    'medio_incompleto',
    'superior_incompleto',
    'superior_completo',
    'nao_se_aplica',
    'idade_menor1',
    'idade_1a4',
    'idade_5a9',
    'idade_10a14',
    'idade_15a19',
    'idade_20a39',
    'idade_40a59',
    'idade_60a64',
    'idade_65a69',
    'idade_70a79',
    'idade_80mais'
]

# Cria colunas para inputs
cols = st.columns(3)

# Cria o dicionário de inputs manualmente organizados nas colunas
input_data = {}

for index, feature in enumerate(features):
    col = cols[index % 3]  # Distribui as features entre as colunas
    input_data[feature] = col.number_input(label=feature, value=0.0, format="%.2f")

st.markdown("---")

if st.button("Realizar Previsão"):
    try:
        response = requests.post("http://127.0.0.1:8000/prever", json=input_data)

        if response.status_code == 200:
            resultado = response.json()
            st.success(f"Previsão de casos: {resultado['casos_previstos']} casos")
            with st.expander("Valores utilizados na previsão"):
                st.json(input_data)
        else:
            st.error("Erro ao consultar a API. Verifique se a API está rodando.")
    except Exception as e:
        st.error(f"Erro ao realizar a requisição: {e}")
