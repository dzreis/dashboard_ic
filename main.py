import os
import logging
import pandas as pd
import streamlit as st

from views import visualizacao_estatistica
from views import ml_teste  # importa o pipeline completo com PCA + DBSCAN

st.set_page_config(page_title="Dashboard Análise de Interações", layout="wide")

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ----------- INTERFACE PRINCIPAL ------------------

st.title("🧠 Análise de Interações - Reabilitação Motora")

# -------- Navegação por abas --------
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

    ### 🤖 Modelo Preditivo
    - Página dedicada à apresentação de resultados gerados pelo modelo de aprendizado de máquina não supervisionado.
    """)

# -------- Página 2: Visualização Estatística --------
with abas[1]:
    visualizacao_estatistica.carregar()

# -------- Página 3: Resultados do Modelo Preditivo --------
with abas[2]:
    st.title("🤖 Resultados do Modelo de Aprendizado de Máquina")

    st.markdown("""
    ### 🧠 Análise de Padrões de Movimento Corporal

    Esta seção apresenta uma análise automática dos dados de movimento do paciente, com base em um modelo de aprendizado de máquina. 
    O objetivo é **identificar grupos (clusters) com padrões semelhantes de movimento** em diferentes partes do corpo, permitindo a 
    detecção de possíveis **compensações, assimetrias ou desvios**.

    #### 📌 O que você está vendo:

    - **Gráfico de Dispersão**:  
    Mostra as execuções do paciente agrupadas em cores diferentes, com base na semelhança geral dos movimentos.  
    Cada ponto representa um conjunto de dados, e os grupos (clusters) podem indicar padrões de movimento distintos.

    - **Gráfico de Barras**:  
    Apresenta a **média de movimento** por parte do corpo dentro de cada grupo identificado.  
    Isso permite comparar, por exemplo, se um grupo utiliza mais o cotovelo direito do que o esquerdo, sugerindo compensação do movimento.

    - **Tabela de Médias por Grupo**:  
    Resume os valores médios de movimento (ângulos) de cada articulação para cada grupo.  
    Essa tabela ajuda a entender o comportamento típico de cada cluster e facilita a identificação de desequilíbrios.

    - **Interpretação Automática**:  
    Um texto resumido com os principais padrões identificados nos grupos, facilitando a análise clínica sem necessidade de conhecimento 
    técnico em modelos de inteligência artificial.
    """)

    uploaded_file = st.sidebar.file_uploader("📁 Envie o arquivo CSV do paciente", type="csv")
    pasta_treinamento = "treino"  # ajuste se necessário

    if st.sidebar.button("🔍 Analisar"):
        if uploaded_file is None:
            st.info("Envie um arquivo CSV para análise.")
        else:
            # Chamada da função principal do ml_teste.py
            (fig_pca, fig_barras), clusters, interpretacao, tabela = ml_teste.processar_e_plotar(uploaded_file, pasta_treinamento)

            if fig_pca and fig_barras:
                st.subheader("Gráfico de Dispersão com PCA")
                st.plotly_chart(fig_pca, use_container_width=True)

                st.subheader("Gráfico de Médias por Cluster")
                st.plotly_chart(fig_barras, use_container_width=True)

                st.markdown(f"### 🧾 Interpretação")
                st.success(interpretacao)

                st.markdown("### 📄 Informações Médias por Cluster")
                colunas_numericas = tabela.select_dtypes(include=['float', 'int']).columns
                st.dataframe(tabela.style.format({col: "{:.2f}" for col in colunas_numericas}))
            
            else:
                st.warning(interpretacao)


# -------- Página 4: Em construção --------
with abas[3]:
    st.title("🚧 Página em Construção")
    st.info("Esta funcionalidade está em desenvolvimento. Volte em breve!")
