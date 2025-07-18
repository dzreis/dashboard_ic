import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from io import StringIO
from utils.processamento import calcular_frames_por_segundo

# Função principal que será chamada no dashboard
def carregar():
    st.header("📈 Agrupamento dos dados com K-Means")

    # Upload do arquivo CSV
    arquivo = st.file_uploader("📁 Envie seu arquivo CSV", type="csv")
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
    st.markdown("""
    Silhouette Score é uma métrica que avalia a qualidade dos clusters:
    - Valores próximos de 1: indicam que os dados estão bem agrupados e separados dos outros
    - Valores próximos de 0: sugerem sobreposição entre clusters
    - Valores próximos de -1: indicam agrupamentos incorretos
    """)

    # ===== Visualização dos clusters com PCA =====
    st.subheader("🔍 Visualização dos Clusters")

    # Aplica PCA para redução para 2 dimensões
    pca = PCA(n_components=2)
    dados_pca = pca.fit_transform(dados_normalizados)

    # Converte tempo (em frames) para segundos reais
    coluna_tempo = df.columns[0]  # primeira coluna
    fps = calcular_frames_por_segundo(df.copy(), coluna_tempo)

    if fps is None or fps == 0:
        st.error("Não foi possível calcular os frames por segundo (FPS). Verifique o formato da coluna de tempo.")
        return

    # Cria nova coluna com tempo em segundos
    df["Tempo (s)"] = df[coluna_tempo] / fps

    # Cria DataFrame para plotagem
    df_pca = pd.DataFrame(data=dados_pca, columns=["Componente 1", "Componente 2"])
    df_pca["Cluster"] = clusters
    df_pca["Tempo (s)"] = df["Tempo (s)"]

    # Gráfico interativo
    fig_pca = px.scatter(
        df_pca,
        x="Componente 1",
        y="Componente 2",
        color=df_pca["Cluster"].astype(str),
        title=f"Visualização dos Dados com PCA ({n_clusters} Clusters)",
        labels={"color": "Cluster"},
        hover_data=["Tempo (s)"]
    )
    st.plotly_chart(fig_pca)


    # ===== Visualização dos clusters com t-SNE =====
    st.subheader("🔍 Visualização dos Clusters (t-SNE)")

    from sklearn.manifold import TSNE

    with st.spinner("Calculando t-SNE... isso pode levar alguns segundos."):
        tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=1000)
        dados_tsne = tsne.fit_transform(dados_normalizados)

    # Criação do DataFrame para visualização
    df_tsne = pd.DataFrame(dados_tsne, columns=["Dimensão 1", "Dimensão 2"])
    df_tsne["Cluster"] = clusters
    df_tsne["Tempo (s)"] = df["Tempo (s)"]

    # Plot com Plotly
    fig_tsne = px.scatter(
        df_tsne,
        x="Dimensão 1",
        y="Dimensão 2",
        color=df_tsne["Cluster"].astype(str),
        title=f"Visualização dos Dados com t-SNE ({n_clusters} Clusters)",
        labels={"color": "Cluster"},
        hover_data=["Tempo (s)"]
    )
    st.plotly_chart(fig_tsne)

       # ===== Visualização dos clusters =====
    st.subheader("🔍 Visualização dos Clusters")

    # Seleciona duas variáveis para o gráfico
    colunas_disponiveis = dados_modelo.columns.tolist()
    var_x = st.selectbox("Selecione a variável para o eixo X", colunas_disponiveis, index=0)
    var_y = st.selectbox("Selecione a variável para o eixo Y", colunas_disponiveis, index=1)
    df["Tempo (s)"] = df[coluna_tempo] / fps
    df_resultado["Tempo (s)"] = df["Tempo (s)"]


    fig_cluster = px.scatter(
    df_resultado,
    x=var_x,
    y=var_y,
    color=df_resultado["Cluster"].astype(str),
    title=f"Clusters com K-Means ({n_clusters} grupos)",
    labels={"color": "Cluster"},
    hover_data=["Tempo (s)"]
    )
    st.plotly_chart(fig_cluster)
    