# ESTUDO E APLICAÇÃO DE TÉCNICAS DE APRENDIZAGEM DE MÁQUINA EM DADOS CINEMÁTICOS GERADOS POR VISÃO COMPUTACIONAL

## 🎯 Sobre o Projeto

Este projeto de Iniciação Científica explorou a integração de **Inteligência Artificial (IA)**, **Aprendizado de Máquina (AM)** e **Visão Computacional (VC)** para a análise de dados cinemáticos de pacientes em reabilitação motora e neurofuncional.

O principal entregável prático é este **Dashboard Interativo** que permite a profissionais de saúde (fisioterapeutas e terapeutas ocupacionais) visualizar, de forma simples e objetiva, métricas estatísticas do movimento do paciente.

## 💡 Entregável Principal: Dashboard Interativo

A ferramenta foi desenvolvida para transformar dados brutos de movimento, gerados por software de VC (ex: KinesiOS), em informações visuais e quantitativas.

**Funcionalidades:**
* Visualização de métricas estatísticas (média, mediana) da amplitude do movimento da articulação alvo (ombro).
* Comparação do desempenho do paciente entre sessões inicial e final de tratamento.
* Identificação automática dos momentos de movimento esperado (encaixe das peças de um quebra-cabeças) e cálculo do tempo médio de reação e/ou conclusão da tarefa.

## ⚙️ Tecnologias Utilizadas

| Categoria | Tecnologia | Uso Principal |
| :--- | :--- | :--- |
| **Linguagem** | Python | Linguagem principal do projeto |
| **Web App/Interface** | Streamlit | Desenvolvimento da interface do dashboard  |
| **Processamento de Dados** | Pandas, NumPy | Manipulação, limpeza e normalização dos dados cinemáticos |
| **Visualização** | Plotly | Criação de gráficos interativos para o dashboard |
| **Aprendizado de Máquina** | Scikit-learn | Testes exploratórios com algoritmos de agrupamento (DBSCAN, K-Means) |

## 🚀 Como Usar/Reproduzir o Projeto

Siga os passos abaixo para clonar o repositório, instalar as dependências e rodar o dashboard interativo na sua máquina local.

### Pré-requisitos
Certifique-se de ter o **Python (versão 3.x)** instalado em seu sistema.

### Passo a Passo

1.  **Clone o repositório** para a sua máquina local:
    ```bash
    git clone https://github.com/dzreis/dashboard_ic.git
    cd dashboard_ic
    ```

2.  **Instale os pacotes e dependências** necessárias, listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação** usando o Streamlit. O dashboard será aberto automaticamente no seu navegador padrão:
    ```bash
    streamlit run main.py
    ```