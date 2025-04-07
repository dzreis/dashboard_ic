import streamlit as st

# DEVE vir aqui, antes de qualquer outro comando do Streamlit
st.set_page_config(page_title="Dashboard Análise de Interações", layout="wide")

from views import visualizacao_estatistica

# Painel lateral fixo
st.sidebar.title("🏥 Painel de Controle")
st.sidebar.header("Defina os parâmetros")

uploaded_file = st.sidebar.file_uploader("Envie o arquivo CSV", type=["csv"])
# Fonte dos dados
data_source = st.sidebar.selectbox("Fonte dos dados", ["Infravermelho", "RGB"])
# Grupo de membros
body_group = st.sidebar.selectbox("Grupo de membros", ["Upper limbs", "Lower limbs"])
if body_group == "Upper limbs":
    software_options = ["Pong", "Invaders", "Puzzle", "Counter"]
else:
    software_options = ["Barrier", "Maps", "Walk"]

interaction_software = st.sidebar.selectbox("Software de interação", software_options)

# -------- Navegação por abas no cabeçalho --------
abas = st.tabs(["🏠 Início", "📊 Visualização Estatística", "🚧 Outra Página"])

# -------- Página 1: Instruções --------
with abas[0]:
    st.title("🏠 Bem-vindo ao Dashboard de Análise de Interações")
    st.markdown("""
    Este dashboard tem como objetivo auxiliar na análise de dados obtidos a partir de interações com softwares de reabilitação.

    ### 📁 Upload de Arquivo
    - O arquivo deve estar no formato **.CSV**.
    - Faça o envio utilizando a barra lateral à esquerda.

    ### ⚙️ Parâmetros
    - **Fonte dos dados**: Tipo de câmera utilizada (Infravermelho ou RGB).
    - **Grupo de membros**: Região corporal analisada (superior ou inferior).
    - **Software de interação**: Jogo ou aplicação utilizada durante a captação dos dados.

    ### 📊 Visualização Estatística
    - Página destinada a apresentar análises exploratórias iniciais dos dados enviados.
    - É necessário selecionar os parâmetros corretamente e realizar o upload de um arquivo CSV válido.

    ### 🚧 Outra Página
    - Funcionalidade em desenvolvimento.
    """)

# -------- Página 2: Visualização Estatística --------
with abas[1]:
    visualizacao_estatistica.carregar()

# -------- Página 3: Em construção --------
with abas[2]:
    st.title("🚧 Página em Construção")
    st.info("Esta funcionalidade está em desenvolvimento. Volte em breve!")
