import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from glob import glob
import logging

# Configuração do logger para acompanhar o processo via terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def carregar_dados_treino(pasta_treino, colunas):
    """
    Lê todos os arquivos CSV da pasta de treino e concatena os dados relevantes.

    Parâmetros:
        pasta_treino (str): Caminho para a pasta com arquivos CSV de treino.
        colunas (list): Lista de colunas que devem estar presentes em cada arquivo.

    Retorna:
        DataFrame com os dados combinados ou vazio se nada for válido.
    """
    arquivos_csv = glob(os.path.join(pasta_treino, "*.csv"))
    dfs = []

    for arquivo in arquivos_csv:
        try:
            df = pd.read_csv(arquivo)
            if set(colunas).issubset(df.columns):
                dfs.append(df[colunas].dropna())  # Garante que não existam valores ausentes
                logger.info(f"Arquivo carregado para treino: {arquivo}")
            else:
                logger.warning(f"Colunas esperadas não encontradas em {arquivo}")
        except Exception as e:
            logger.error(f"Erro ao carregar {arquivo}: {e}")

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()

def processar_csv_teste(arquivo_teste, colunas):
    """
    Processa o arquivo CSV enviado pelo usuário para teste.

    Parâmetros:
        arquivo_teste (str): Caminho do arquivo de teste.
        colunas (list): Lista de colunas a serem utilizadas.

    Retorna:
        DataFrame com os dados do teste, apenas colunas esperadas e sem valores nulos.
    """
    try:
        df_teste = pd.read_csv(arquivo_teste)
        return df_teste[colunas].dropna()
    except Exception as e:
        logger.error(f"Erro ao processar arquivo de teste: {e}")
        return pd.DataFrame()

def treinar_modelo(dados_treino):
    """
    Aplica normalização, redução de dimensionalidade (PCA) e treina o modelo DBSCAN.

    Retorna:
        scaler (StandardScaler): Normalizador treinado.
        pca (PCA): Redutor de dimensionalidade treinado.
        dbscan (DBSCAN): Modelo de clustering treinado.
    """
    scaler = StandardScaler()
    dados_norm = scaler.fit_transform(dados_treino)

    pca = PCA(n_components=2)  # Reduz para duas dimensões para visualização
    dados_pca = pca.fit_transform(dados_norm)

    dbscan = DBSCAN(eps=0.6, min_samples=30)  # Parâmetros podem ser ajustados depois
    dbscan.fit(dados_pca)

    logger.info("Modelo DBSCAN treinado com sucesso.")
    return scaler, pca, dbscan

def aplicar_modelo(dados_teste, scaler, pca, modelo):
    """
    Aplica o pipeline de transformação e faz predição no conjunto de teste.

    Retorna:
        dados_pca (np.array): Dados reduzidos em 2D (PCA).
        clusters (np.array): Rótulos de cluster atribuídos aos dados de teste.
    """
    dados_norm = scaler.transform(dados_teste)
    dados_pca = pca.transform(dados_norm)
    clusters = modelo.fit_predict(dados_pca)

    logger.info("Modelo DBSCAN aplicado ao conjunto de teste.")
    return dados_pca, clusters


def gerar_graficos_interpretaveis(dados_teste, dados_pca, clusters):
    """
    Gera visualizações interpretáveis para profissionais da saúde:
    1. Gráfico de dispersão PCA com clusters rotulados.
    2. Gráfico de barras com médias dos ângulos por cluster.

    Parâmetros:
        dados_teste (DataFrame): Dados originais do teste.
        dados_pca (np.array): Dados reduzidos via PCA.
        clusters (np.array): Rótulos dos clusters.

    Retorna:
        fig_pca (Figure): Gráfico PCA com clusters.
        fig_barras (Figure): Gráfico de barras com médias por cluster.
        tabela_resumo (DataFrame): Tabela de médias por cluster.
    """
    df = dados_teste.copy()
    df['Cluster'] = clusters.astype(str)
    df['PCA1'] = dados_pca[:, 0]
    df['PCA2'] = dados_pca[:, 1]

    # 1. Gráfico de PCA com clusters
    fig_pca = px.scatter(
        df, x='PCA1', y='PCA2',
        color='Cluster',
        title='Visualização dos Grupos de Movimento (PCA)',
        labels={'PCA1': 'Componente Principal 1', 'PCA2': 'Componente Principal 2'},
        opacity=0.7,
        color_discrete_sequence=px.colors.qualitative.Set1
    )

    # 2. Gráfico de barras com médias por cluster
    medias = df.groupby('Cluster').mean(numeric_only=True).reset_index()
    medias_melt = medias.melt(id_vars='Cluster', value_name='Ângulo Médio', var_name='Articulação')
    medias_melt = medias_melt[medias_melt['Articulação'].isin(dados_teste.columns)]

    fig_barras = px.bar(
        medias_melt,
        x='Articulação',
        y='Ângulo Médio',
        color='Cluster',
        barmode='group',
        title='Média dos Ângulos por Cluster',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_barras.update_layout(xaxis_tickangle=-45)

    return fig_pca, fig_barras, medias


def identificar_outliers(dados_teste, clusters):
    """
    Identifica os pontos classificados como -1 pelo DBSCAN e 
    destaca quais articulações mais se desviam da média (procura por compensações).

    Retorna:
        outliers (DataFrame): Apenas os pontos fora do padrão.
        explicacoes (list): Lista de mensagens com articulações mais impactadas.
    """
    outliers = dados_teste[clusters == -1]
    if outliers.empty:
        return outliers, []

    medias = dados_teste.mean()
    explicacoes = []

    for i, linha in outliers.iterrows():
        # Calcula diferença absoluta em relação à média
        diferencas = (linha - medias).abs()
        # Seleciona as 2 maiores variações
        top_variaveis = diferencas.sort_values(ascending=False).head(2).index.tolist()
        explicacoes.append(f"Registro {i}: variações fora do esperado em {', '.join(top_variaveis)}")

    return outliers, explicacoes


def processar_e_plotar(arquivo_teste, pasta_treino):
    """
    Função principal que executa todo o pipeline:
    - Carrega os dados
    - Treina o modelo
    - Aplica no teste
    - Gera gráfico
    - Cria uma interpretação simplificada para o usuário

    Retorna:
        figs (tuple): Gráficos para o Streamlit (PCA e Barras).
        clusters_teste (array): Rótulos dos clusters detectados.
        interpretacao (str): Mensagem simples para o profissional.
        tabela_resumo (DataFrame): Médias por cluster.
        explicacoes_outliers (list): Explicações sobre os outliers detectados.
    """
    colunas_modelo = [
        'shoulderLangle', 'shoulderRangle',
        'elbowLangle', 'elbowRangle',
        'hipLangle', 'hipRangle',
        'kneeLangle', 'kneeRangle'
    ]

    dados_treino = carregar_dados_treino(pasta_treino, colunas_modelo)
    if dados_treino.empty:
        logger.warning("Nenhum dado de treino válido encontrado.")
        return None, None, "⚠️ Nenhum dado de treino válido encontrado.", None, []

    dados_teste = processar_csv_teste(arquivo_teste, colunas_modelo)
    if dados_teste.empty:
        logger.warning("Dados de teste inválidos ou vazios.")
        return None, None, "⚠️ Arquivo de teste inválido ou com dados ausentes.", None, []

    scaler, pca, modelo = treinar_modelo(dados_treino)
    dados_pca_teste, clusters_teste = aplicar_modelo(dados_teste, scaler, pca, modelo)

    # Gerar visualização interpretável
    fig_pca, fig_barras, tabela_resumo = gerar_graficos_interpretaveis(dados_teste, dados_pca_teste, clusters_teste)

    # Identificar outliers (-1) e explicar
    outliers, explicacoes_outliers = identificar_outliers(dados_teste, clusters_teste)

    interpretacao = (
        "🔴 Foram detectados padrões de movimento incomuns (possíveis compensações)."
        if -1 in clusters_teste else
        "🟢 Todos os padrões de movimento estão dentro da normalidade esperada."
    )

    return (fig_pca, fig_barras), clusters_teste, interpretacao, tabela_resumo, explicacoes_outliers


'''
def processar_e_plotar(arquivo_teste, pasta_treino):
    """
    Função principal que executa todo o pipeline:
    - Carrega os dados
    - Treina o modelo
    - Aplica no teste
    - Gera gráfico
    - Cria uma interpretação simplificada para o usuário

    Retorna:
        fig (Plotly Figure): Gráfico para o Streamlit.
        clusters_teste (array): Rótulos dos clusters detectados.
        interpretacao (str): Mensagem simples e útil para o profissional da saúde.
    """
    colunas_modelo = [
        'shoulderLangle', 'shoulderRangle',
        'elbowLangle', 'elbowRangle',
        'hipLangle', 'hipRangle',
        'kneeLangle', 'kneeRangle'
    ]

    dados_treino = carregar_dados_treino(pasta_treino, colunas_modelo)
    if dados_treino.empty:
        logger.warning("Nenhum dado de treino válido encontrado.")
        return None, None, "⚠️ Nenhum dado de treino válido encontrado."

    dados_teste = processar_csv_teste(arquivo_teste, colunas_modelo)
    if dados_teste.empty:
        logger.warning("Dados de teste inválidos ou vazios.")
        return None, None, "⚠️ Arquivo de teste inválido ou com dados ausentes."

    scaler, pca, modelo = treinar_modelo(dados_treino)
    dados_pca_teste, clusters_teste = aplicar_modelo(dados_teste, scaler, pca, modelo)

    # Gerar visualização interpretável
    fig_pca, fig_barras, tabela_resumo = gerar_graficos_interpretaveis(dados_teste, dados_pca_teste, clusters_teste)

    interpretacao = (
        "🔴 Foram detectados padrões de movimento incomuns (possíveis compensações)."
        if -1 in clusters_teste else
        "🟢 Todos os padrões de movimento estão dentro da normalidade esperada."
    )

    return (fig_pca, fig_barras), clusters_teste, interpretacao, tabela_resumo
'''
