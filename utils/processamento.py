import numpy as np

def calcular_frames_por_segundo(df, time):
    df['seconds'] = df[time].astype(str).str[-2:]
    df['count'] = (df['seconds'] != df['seconds'].shift(1)).cumsum()
    result = df.groupby('count').size().reset_index(name='counts')
    frames_por_seg = result.loc[1, 'counts'] if len(result) > 1 else None
    return frames_por_seg

def calcular_tempos_picos(dados, frames_por_seg, amplitude_limite, tempo_inicial, duracao_minima=1):
    tempo = np.arange(len(dados)) / frames_por_seg
    mascara = dados > amplitude_limite
    intervalos = np.diff(mascara.astype(int))
    inicios_picos = np.where(intervalos == 1)[0]
    finais_picos = np.where(intervalos == -1)[0]

    if inicios_picos.size == 0 or finais_picos.size == 0:
        return [], 0.0

    if finais_picos[0] < inicios_picos[0]:
        finais_picos = finais_picos[1:]
    if len(finais_picos) < len(inicios_picos):
        inicios_picos = inicios_picos[:len(finais_picos)]

    inicios_picos = np.array([pico for pico in inicios_picos if tempo[pico] > tempo_inicial])
    finais_picos = np.array([pico for pico in finais_picos if tempo[pico] > tempo_inicial])

    picos_filtrados = [(inicio, final) for inicio, final in zip(inicios_picos, finais_picos)
                       if ((tempo[final] - tempo[inicio]) * frames_por_seg) >= duracao_minima * frames_por_seg]

    duracoes_picos = [(tempo[final] - tempo[inicio]) for inicio, final in picos_filtrados]
    media_duracao = sum(duracoes_picos) / len(duracoes_picos) if duracoes_picos else 0.0

    return duracoes_picos, media_duracao

def classificar(picos):
    classificacao = []
    for valor in picos:
        if valor <= 5:
            classificacao.append('Nível 1')
        elif 5 < valor <= 9:
            classificacao.append('Nível 2')
        else:
            classificacao.append('Nível 3')
    return classificacao
