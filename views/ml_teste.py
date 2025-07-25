import os
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from glob import glob
import logging

# Configurar logs para depuração no terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def carregar_dados_treino(pasta_treino, colunas):
    arquivos_csv = glob(os.path.join(pasta_treino, "*.csv"))
    dfs = []
    for arquivo in arquivos_csv:
        try:
            df = pd.read_csv(arquivo)
            if set(colunas).issubset(df.columns):
                dfs.append(df[colunas].dropna())
                logger.info(f"Arquivo carregado para treino: {arquivo}")
            else:
                logger.warning(f"Colunas esperadas nao encontradas em {arquivo}")
        except Exception as e:
            logger.error(f"Erro ao carregar {arquivo}: {e}")
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()

def processar_csv_teste(arquivo_teste, colunas):
    try:
        df_teste = pd.read_csv(arquivo_teste)
        return df_teste[colunas].dropna()
    except Exception as e:
        logger.error(f"Erro ao processar arquivo de teste: {e}")
        return pd.DataFrame()

def treinar_modelo(dados_treino):
    scaler = StandardScaler()
    dados_norm = scaler.fit_transform(dados_treino)
    pca = PCA(n_components=2)
    dados_pca = pca.fit_transform(dados_norm)
    dbscan = DBSCAN(eps=0.5, min_samples=20)
    dbscan.fit(dados_pca)
    logger.info("Modelo DBSCAN treinado com sucesso.")
    return scaler, pca, dbscan

def aplicar_modelo(dados_teste, scaler, pca, modelo):
    dados_norm = scaler.transform(dados_teste)
    dados_pca = pca.transform(dados_norm)
    clusters = modelo.fit_predict(dados_pca)
    logger.info("Modelo DBSCAN aplicado ao conjunto de teste.")
    return dados_pca, clusters

def gerar_grafico_plotly(dados_pca, clusters):
    df_plot = pd.DataFrame(dados_pca, columns=['PC1', 'PC2'])
    df_plot['Cluster'] = clusters.astype(str)
    fig = px.scatter(df_plot, x='PC1', y='PC2', color='Cluster',
                     title='Padrões de Movimento Detectados (DBSCAN + PCA)',
                     labels={'PC1': 'Componente Principal 1', 'PC2': 'Componente Principal 2'},
                     color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(legend_title_text='Cluster')
    return fig

def processar_e_plotar(arquivo_teste, pasta_treino):
    colunas_modelo = [
        'shoulderLangle', 'shoulderRangle', 'elbowLangle', 'elbowRangle',
        'hipLangle', 'hipRangle', 'kneeLangle', 'kneeRangle'
    ]

    dados_treino = carregar_dados_treino(pasta_treino, colunas_modelo)
    if dados_treino.empty:
        logger.warning("Nenhum dado de treino válido encontrado.")
        return None, None, "Nenhum dado de treino válido encontrado."

    dados_teste = processar_csv_teste(arquivo_teste, colunas_modelo)
    if dados_teste.empty:
        logger.warning("Dados de teste inválidos ou vazios.")
        return None, None, "Dados de teste inválidos ou vazios."

    scaler, pca, modelo = treinar_modelo(dados_treino)
    dados_pca_teste, clusters_teste = aplicar_modelo(dados_teste, scaler, pca, modelo)
    fig = gerar_grafico_plotly(dados_pca_teste, clusters_teste)

    interpretacao = (
        "🔴 Foram detectados padrões de movimento incomuns (possíveis compensações)."
        if -1 in clusters_teste else
        "🟢 Todos os padrões detectados estão dentro da normalidade esperada."
    )

    return fig, clusters_teste, interpretacao
