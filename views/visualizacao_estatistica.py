import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.processamento import calcular_frames_por_segundo, calcular_tempos_picos, classificar

def carregar():
    st.title("📊 Análise Estatística Inicial")
    st.subheader("Envio de arquivos CSV")

    col1, col2 = st.columns(2)
    with col1:
        inicio_file = st.file_uploader("CSV do Início", type="csv", key="inicio")
    with col2:
        final_file = st.file_uploader("CSV do Final", type="csv", key="final")

    if inicio_file and final_file:
        inicio_df = pd.read_csv(inicio_file)
        final_df = pd.read_csv(final_file)

        colunas_movimento = ['shoulderLangle', 'shoulderRangle']
        inicio_amplitude = inicio_df[colunas_movimento]
        final_amplitude = final_df[colunas_movimento]

        fps_inicio = calcular_frames_por_segundo(inicio_df, 'time')
        fps_final = calcular_frames_por_segundo(final_df, 'time')

        conv_tempo_inicial = int(len(inicio_df) / fps_inicio)
        conv_tempo_final = int(len(final_df) / fps_final)

        # Impressão do tempo de execução em segundos
        st.write(f"⏱️ Tempo total no INÍCIO: **{conv_tempo_inicial}** segundos")
        st.write(f"⏱️ Tempo total no FINAL: **{conv_tempo_final}** segundos")

        #
        tempo_inicio = np.arange(len(inicio_df) / fps_inicio)
        tempo_final = np.arange(len(final_df) / fps_final)

        st.subheader("📉 Gráfico de Amplitude Inicial x Final")
        fig, ax = plt.subplots()
        ax.plot(tempo_inicio, inicio_amplitude.shoulderLangle, label='Início')
        ax.plot(tempo_final, final_amplitude.shoulderLangle, label='Final')
        ax.set_title("Comparação de Amplitude da Articulação Alvo")
        ax.set_xlabel("Tempo (segundos)")
        ax.set_ylabel("Amplitude")
        ax.legend()
        ax.grid()
        st.pyplot(fig)

        # Análise de picos
        dados_inicio = inicio_amplitude['shoulderLangle']
        dados_final = final_amplitude['shoulderLangle']
        amplitude_limite = 55

        picos_i, media_i = calcular_tempos_picos(dados_inicio, fps_inicio, amplitude_limite, 5)
        picos_f, media_f = calcular_tempos_picos(dados_final, fps_final, amplitude_limite, 2)

        st.write(f"📈 Média dos picos iniciais: {media_i:.2f}s")
        st.write(f"📈 Média dos picos finais: {media_f:.2f}s")

        st.subheader("📌 Classificação de Nível dos Picos")
        st.write("**Início:**", classificar(picos_i))
        st.write("**Final:**", classificar(picos_f))
    else:
        st.info("Por favor, envie os dois arquivos CSV para iniciar a análise.")
