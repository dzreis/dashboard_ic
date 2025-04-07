import streamlit as st

# Título principal
st.title("Dashboard de Análise de Interações")

# Sidebar
st.sidebar.header("Upload e Parâmetros")

# Upload do arquivo CSV
uploaded_file = st.sidebar.file_uploader("Envie o arquivo CSV", type=["csv"])

# Fonte dos dados
data_source = st.sidebar.selectbox("Fonte dos dados", ["Infravermelho", "RGB"])

# Grupo de membros
body_group = st.sidebar.selectbox("Grupo de membros", ["Upper limbs", "Lower limbs"])

# Opções de software de interação, dependendo do grupo selecionado
if body_group == "Upper limbs":
    software_options = ["Pong", "Invaders", "Puzzle", "Counter"]
else:
    software_options = ["Barrier", "Maps", "Walk"]

interaction_software = st.sidebar.selectbox("Software de interação", software_options)

# Exibição das escolhas no painel principal (só para visualização por enquanto)
st.subheader("Resumo das Seleções")
st.write(f"**Fonte dos dados:** {data_source}")
st.write(f"**Grupo de membros:** {body_group}")
st.write(f"**Software de interação:** {interaction_software}")

# Mostrar nome do arquivo enviado (caso tenha upload)
if uploaded_file is not None:
    st.success(f"Arquivo enviado: {uploaded_file.name}")
else:
    st.warning("Nenhum arquivo enviado ainda.")
