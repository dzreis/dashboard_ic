# [cite_start]ESTUDO E APLICAÇÃO DE TÉCNICAS DE APRENDIZAGEM DE MÁQUINA EM DADOS CINEMÁTICOS GERADOS POR VISÃO COMPUTACIONAL [cite: 629]

## 🎯 Sobre o Projeto (Resumo Executivo)

[cite_start]Este projeto de Iniciação Científica explorou a integração de **Inteligência Artificial (IA)**, **Aprendizado de Máquina (AM)** e **Visão Computacional (VC)** para a análise de dados cinemáticos de pacientes em reabilitação motora e neurofuncional[cite: 646, 655].

[cite_start]O principal entregável prático é este **Dashboard Interativo** que permite a profissionais de saúde (fisioterapeutas e terapeutas ocupacionais) visualizar, de forma simples e objetiva, métricas estatísticas do movimento do paciente[cite: 586, 569, 450].

## 💡 Entregável Principal: Dashboard Interativo

[cite_start]A ferramenta foi desenvolvida para transformar dados brutos de movimento, gerados por software de VC (ex: KinesiOS) [cite: 520, 644][cite_start], em informações visuais e quantitativas[cite: 554, 587].

**Funcionalidades:**
* [cite_start]Visualização de métricas estatísticas (média, mediana) da amplitude do movimento da articulação alvo (ombro)[cite: 547, 708].
* [cite_start]Comparação do desempenho do paciente entre sessões inicial e final de tratamento[cite: 518, 547].
* [cite_start]Identificação automática dos momentos de movimento esperado (encaixe das peças de um quebra-cabeças) e cálculo do tempo médio de reação e/ou conclusão da tarefa[cite: 523, 550].

## ⚙️ Tecnologias Utilizadas (Tech Stack)

| Categoria | Tecnologia | Uso Principal |
| :--- | :--- | :--- |
| **Linguagem** | Python | [cite_start]Linguagem principal do projeto [cite: 701] |
| **Web App/Interface** | Streamlit | [cite_start]Desenvolvimento da interface do dashboard [cite: 701, 543] |
| **Processamento de Dados** | Pandas, NumPy | [cite_start]Manipulação, limpeza e normalização dos dados cinemáticos [cite: 701, 714] |
| **Visualização** | Plotly | [cite_start]Criação de gráficos interativos para o dashboard [cite: 701, 543] |
| **Aprendizado de Máquina** | Scikit-learn | [cite_start]Testes exploratórios com algoritmos de agrupamento (DBSCAN, K-Means) [cite: 706, 474] |

## 🚧 Resultados da Pesquisa e Limitações do AM

A fase de testes com algoritmos de Aprendizado de Máquina Não Supervisionado (DBSCAN), embora não tenha resultado em um modelo final e robusto, gerou contribuições importantes:

* [cite_start]**Limitação do Dataset:** Os modelos não geraram agrupamentos (clusters) claros e clinicamente interpretáveis devido à natureza restrita, ruidosa e não padronizada da base de dados disponível[cite: 535, 536, 558].
* [cite_start]**Lição Aprendida:** A qualidade, quantidade e padronização da base de dados são fatores decisivos para o sucesso da aplicação de AM em cenários clínicos de reabilitação[cite: 562, 575].

## 🚀 Próximos Passos

* [cite_start]**Validação Clínica:** Realizar a validação do dashboard em ambientes clínicos reais (hospitais e clínicas) para comprovar sua usabilidade e eficácia[cite: 578].
* [cite_start]**Expansão do AM:** Continuar os testes com modelos de AM mais avançados (ex: redes neurais) em conjunto com a construção de uma base de dados mais ampla e padronizada[cite: 580].