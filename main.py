import streamlit as st

st.set_page_config(page_title="Dashboard Análise de Interações", layout="wide")

from views import visualizacao_estatistica
from views import modelo_aprendizado_maquina
from views import ml_teste

# Painel lateral fixo
#st.sidebar.title("🏥 Painel de Controle")

#uploaded_file = st.sidebar.file_uploader("Envie o arquivo CSV", type=["csv"])
# Fonte dos dados
#data_source = st.sidebar.selectbox("Fonte dos dados", ["Infravermelho", "RGB"])

# -------- Navegação por abas no cabeçalho --------
abas = st.tabs(["🏠 Início", "📊 Visualização Estatística", "🤖 Modelo Preditivo", "🚧 Outra Página"])

# -------- Página 1: Instruções --------
with abas[0]:
    st.title("✨Reabilitação assistida por AR: visualização e análise dos dados")
    st.markdown("""
    Este dashboard tem como objetivo auxiliar na análise de dados obtidos a partir de interações com softwares de reabilitação.

    ### 📁 Upload de Arquivo
    - O arquivo deve estar no formato **.CSV**.
    - Faça o envio utilizando a barra lateral à esquerda.

    ### ⚙️ Parâmetros
    - **Fonte dos dados**: Tipo de câmera utilizada (Infravermelho ou RGB).

    ### 📊 Visualização Estatística
    - Página destinada a apresentar análises exploratórias iniciais dos dados enviados.
    - É necessário selecionar os parâmetros corretamente e realizar o upload de um arquivo CSV válido.
    
    ### 🤖 Modelo Preditivo
    - Página dedicada à apresentação de resultados gerados pelo modelo de aprendizado de máquina não supervisionado.
    - Aqui serão exibidas métricas, clusters identificados ou padrões detectados automaticamente.

    ### 🚧 Outra Página
    - Funcionalidade em desenvolvimento.
    """)

# -------- Página 2: Visualização Estatística --------
with abas[1]:
    visualizacao_estatistica.carregar()

# -------- Página 3: Resultados do Modelo Preditivo --------
with abas[2]:
    st.title("🤖 Resultados do Modelo de Aprendizado de Máquina")
    st.markdown("""
    Nesta seção, você verá os resultados gerados pelos modelos de aprendizado não supervisionado.
    
    - Gráficos de agrupamento (ex: K-means, DBSCAN)
    - Visualização de outliers ou padrões
    - Métricas como silhouette score ou número de clusters
    """)
    #modelo_aprendizado_maquina.carregar()
    ml_teste.carregar()

# -------- Página 4: Em construção --------
with abas[3]:
    st.title("🚧 Página em Construção")
    st.info("Esta funcionalidade está em desenvolvimento. Volte em breve!")
