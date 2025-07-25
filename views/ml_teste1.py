import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import plotly.express as px

def carregar():
    st.title("🤖 Resultados do Modelo de Aprendizado de Máquina")

    uploaded_file = st.file_uploader("Envie seu arquivo CSV para análise", type=["csv"])

    if uploaded_file:
        st.sidebar.header("Configurações do DBSCAN")
        eps = st.sidebar.slider("eps", min_value=0.1, max_value=2.0, value=0.5, step=0.05)
        min_samples = st.sidebar.slider("min_samples", min_value=1, max_value=30, value=10, step=1)

        fig = processar_e_plotar(uploaded_file, eps=eps, min_samples=min_samples)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Por favor, envie um arquivo CSV para iniciar a análise.")

def processar_e_plotar(file, eps=0.5, min_samples=10):
    # 1. Carregar os dados
    df = pd.read_csv(file)

    # 2. Selecionar as colunas de interesse
    colunas_modelo = [
        'shoulderLangle',
        'shoulderRangle',
        'elbowLangle',
        'elbowRangle',
        'hipLangle',
        'hipRangle',
        'kneeLangle',
        'kneeRangle'
    ]
    dados = df[colunas_modelo].dropna()

    # 3. Normalização dos dados
    scaler = StandardScaler()
    dados_norm = scaler.fit_transform(dados)

    # 4. PCA para redução para 2D
    pca = PCA(n_components=2)
    dados_pca = pca.fit_transform(dados_norm)

    # 5. DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(dados_pca)

    # 6. Preparar DataFrame para plot
    df_plot = pd.DataFrame({
        'PC1': dados_pca[:, 0],
        'PC2': dados_pca[:, 1],
        'Cluster': clusters.astype(str)  # para plotly tratar como categórico
    })

    # 7. Plot interativo com Plotly Express
    fig = px.scatter(
        df_plot,
        x='PC1',
        y='PC2',
        color='Cluster',
        title='Padrões de Movimento Detectados com DBSCAN + PCA',
        labels={'PC1': 'Componente Principal 1', 'PC2': 'Componente Principal 2'},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color='DarkSlateGrey')))
    fig.update_layout(legend_title_text='Cluster')

    return fig
