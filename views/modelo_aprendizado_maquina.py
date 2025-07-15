import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from io import StringIO

# Função principal que será chamada no dashboard
def carregar():
    st.header("📈 Agrupamento dos Dados com K-Means")

    # Upload do arquivo CSV
    arquivo = st.sidebar.file_uploader("Envie seu arquivo CSV", type=["csv"])
    if arquivo is None:
        st.warning("Por favor, envie um arquivo CSV para continuar.")
        return

    # Leitura do CSV
    df = pd.read_csv(arquivo)

    # Verifica se o arquivo tem pelo menos 14 colunas
    if df.shape[1] < 14:
        st.error("O CSV enviado não possui colunas suficientes para a análise (mínimo de 14 colunas).")
        return

    # Seleção das colunas para o modelo: da 4 à 13 (índices 3:13), exceto 6 e 7 (índices 5 e 6)
    colunas_modelo = [i for i in range(3, 13) if i not in [5, 6]]
    dados_modelo = df.iloc[:, colunas_modelo]

    # Normalização dos dados
    scaler = StandardScaler()
    dados_normalizados = scaler.fit_transform(dados_modelo)

    # ===== Método do cotovelo para sugerir número de clusters =====
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(dados_normalizados)
        wcss.append(kmeans.inertia_)

    st.subheader("📊 Método do Cotovelo")
    fig_elbow = px.line(
        x=range(1, 11),
        y=wcss,
        markers=True,
        labels={"x": "Número de Clusters", "y": "Inércia (WCSS)"},
        title="Número ideal de clusters (Método do Cotovelo)"
    )
    st.plotly_chart(fig_elbow)

    # Escolha de número de clusters
    n_clusters = st.slider("Selecione o número de clusters", 2, 10, value=3)

    # ===== Aplicação do K-Means =====
    kmeans_final = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans_final.fit_predict(dados_normalizados)

    # Adiciona a informação dos clusters ao dataframe original
    df_resultado = df.copy()
    df_resultado["Cluster"] = clusters

    # ===== Avaliação com Silhouette Score =====
    silhouette = silhouette_score(dados_normalizados, clusters)
    st.success(f"Silhouette Score: **{silhouette:.3f}**")

    # ===== Visualização dos clusters =====
    st.subheader("🔍 Visualização dos Clusters")

    # Seleciona duas variáveis para o gráfico
    colunas_disponiveis = dados_modelo.columns.tolist()
    var_x = st.selectbox("Selecione a variável para o eixo X", colunas_disponiveis, index=0)
    var_y = st.selectbox("Selecione a variável para o eixo Y", colunas_disponiveis, index=1)

    fig_cluster = px.scatter(
        df_resultado,
        x=df.columns[var_x],
        y=df.columns[var_y],
        color=df_resultado["Cluster"].astype(str),
        title=f"Clusters com K-Means ({n_clusters} grupos)",
        labels={"color": "Cluster"},
        hover_data=[df.columns[0]]  # tempo
    )
    st.plotly_chart(fig_cluster)

    # ===== Exibição do resultado tabular =====
    with st.expander("📋 Ver dados com cluster atribuído"):
        st.dataframe(df_resultado.head(20))
