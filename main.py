import os
import logging
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import streamlit as st

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Colunas usadas no modelo
colunas_modelo = [
    'shoulderLangle', 'shoulderRangle',
    'elbowLangle', 'elbowRangle',
    'hipLangle', 'hipRangle',
    'kneeLangle', 'kneeRangle'
]

def carregar_dados_treinamento(pasta_treinamento):
    logger.debug(f"Lendo arquivos da pasta de treino: {pasta_treinamento}")
    dados_treinamento = []
    for arquivo in os.listdir(pasta_treinamento):
        if arquivo.endswith(".csv"):
            caminho = os.path.join(pasta_treinamento, arquivo)
            df = pd.read_csv(caminho)
            df = df[colunas_modelo]
            dados_treinamento.append(df)
    return pd.concat(dados_treinamento, ignore_index=True)

def carregar_dados_teste(arquivo):
    logger.debug(f"Carregando dados de teste do arquivo: {arquivo.name}")
    df = pd.read_csv(arquivo)
    return df[colunas_modelo]

def treinar_modelo(dados, n_clusters=3):
    logger.debug("Iniciando padronização e treinamento do modelo")
    scaler = StandardScaler()
    dados_normalizados = scaler.fit_transform(dados)
    modelo = KMeans(n_clusters=n_clusters, random_state=42)
    modelo.fit(dados_normalizados)
    return modelo, scaler

def testar_modelo(modelo, scaler, dados_teste):
    logger.debug("Aplicando modelo aos dados de teste")
    dados_teste_normalizados = scaler.transform(dados_teste)
    predicoes = modelo.predict(dados_teste_normalizados)
    return predicoes

def exibir_resultados(dados_teste, predicoes):
    logger.debug("Gerando visualização dos resultados")
    df_resultado = dados_teste.copy()
    df_resultado['cluster'] = predicoes
    fig = px.scatter_matrix(df_resultado, dimensions=colunas_modelo, color='cluster',
                            title="Visualização dos Clusters nos Dados do Paciente")
    st.plotly_chart(fig, use_container_width=True)

    padrao = "❌ Possível padrão de compensação identificado."
    if len(set(predicoes)) > 1:
        st.warning(padrao)
    else:
        st.success("✅ Movimento consistente — sem padrão de compensação detectado.")

def processar_e_plotar(uploaded_file, pasta_treinamento):
    if uploaded_file is None:
        st.info("Envie um arquivo CSV para análise.")
        return

    try:
        dados_treinamento = carregar_dados_treinamento(pasta_treinamento)
        dados_teste = carregar_dados_teste(uploaded_file)
        modelo, scaler = treinar_modelo(dados_treinamento)
        predicoes = testar_modelo(modelo, scaler, dados_teste)
        exibir_resultados(dados_teste, predicoes)
    except Exception as e:
        logger.exception("Erro durante o processamento do modelo")
        st.error(f"Erro ao processar os dados: {e}")
