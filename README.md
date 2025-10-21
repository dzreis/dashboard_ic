# ESTUDO E APLICAÇÃO DE TÉCNICAS DE APRENDIZAGEM DE MÁQUINA EM DADOS CINEMÁTICOS GERADOS POR VISÃO COMPUTACIONAL

## 🎯 Sobre o Projeto (Resumo Executivo)

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
| **Web App/Interface** | Streamlit | Desenvolvimento da interface do dashboard  |
| **Processamento de Dados** | Pandas, NumPy | Manipulação, limpeza e normalização dos dados cinemáticos |
| **Visualização** | Plotly | Criação de gráficos interativos para o dashboard |
| **Aprendizado de Máquina** | Scikit-learn | Testes exploratórios com algoritmos de agrupamento (DBSCAN, K-Means) |

## 🚧 Resultados da Pesquisa e Limitações do AM

A fase de testes com algoritmos de Aprendizado de Máquina Não Supervisionado (DBSCAN), embora não tenha resultado em um modelo final e robusto, gerou contribuições importantes:

* **Limitação do Dataset:** Os modelos não geraram agrupamentos (clusters) claros e clinicamente interpretáveis devido à natureza restrita, ruidosa e não padronizada da base de dados disponível.
* **Lição Aprendida:** A qualidade, quantidade e padronização da base de dados são fatores decisivos para o sucesso da aplicação de AM em cenários clínicos de reabilitação.

## 🚀 Próximos Passos

* **Validação Clínica:** Realizar a validação do dashboard em ambientes clínicos reais (hospitais e clínicas) para comprovar sua usabilidade e eficácia.
* **Expansão do AM:** Continuar os testes com modelos de AM mais avançados (ex: redes neurais) em conjunto com a construção de uma base de dados mais ampla e padronizada.