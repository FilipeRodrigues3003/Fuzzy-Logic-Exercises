''' 

'''

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import sys
import requests
from bs4 import BeautifulSoup

res = requests.get('http://dolarhoje.com')

res.raise_for_status()
textSoup = BeautifulSoup(res.text, 'html.parser')
elems = textSoup.find_all(class_='cotMoeda nacional')
num = str(elems[0].select('input')).strip("[<input id= type= value=/>]")
text = num.split()
valor = text[2][7:11]
dol = float(valor.replace(',','.'))
dollar_atual = dol

print(dollar_atual)

x_dolar = np.arange(0, 7.01, 0.01) # Avaliar valores do Dólar com duas casas decimais de R$ 0 até R$ 7
x_tempo = np.arange(1, 1097, 1)  # Avaliar tempo na compra de acordo com a quantidade de meses
x_risco = np.arange(0, 101, 1) # tempo do riscoimento entre 0% e 100%

# mb = Muito Baixo | b = Baixo | m = Médio | a = Alto | ma = Muito Alto
dolar_mb = fuzz.trapmf(x_dolar, [0, 0, 1.9417, 2.905951762])
dolar_b = fuzz.trimf(x_dolar, [1.117939230, 2.309947585, 3.50195594])
dolar_m = fuzz.trimf(x_dolar, [1.7139434071, 2.905951762, 4.2487])
dolar_a = fuzz.trimf(x_dolar, [2.309947585, 3.50195594, 4.693964295])
dolar_ma = fuzz.trapmf(x_dolar,[2.905951762, 4.2487, 7, 7]) 

tempo_b = fuzz.trimf(x_tempo, [0, 0, 548])
tempo_m = fuzz.trimf(x_tempo, [0, 548, 1096])
tempo_a = fuzz.trimf(x_tempo, [548, 1096, 1096])

risco_b = fuzz.trimf(x_risco, [0, 0, 50])
risco_m = fuzz.trimf(x_risco, [0, 50, 100])
risco_a = fuzz.trimf(x_risco,  [50, 100, 100])

'''
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_dolar, dolar_mb, 'y', linewidth=1.5, label="Muito Baixo")
ax0.plot(x_dolar, dolar_b, 'g', linewidth=1.5, label="Baixo")
ax0.plot(x_dolar, dolar_m, 'r', linewidth=1.5, label="Médio")
ax0.plot(x_dolar, dolar_a, 'b', linewidth=1.5, label="Alto")
ax0.plot(x_dolar, dolar_ma, 'm', linewidth=1.5, label="Muito Alto")
ax0.set_title('Valor do Dólar em relação ao Real')
ax0.legend()


ax1.plot(x_tempo, tempo_b, 'g', linewidth=1.5, label="Baixo")
ax1.plot(x_tempo, tempo_m, 'r', linewidth=1.5, label="Médio")
ax1.plot(x_tempo, tempo_a, 'b', linewidth=1.5, label="Alto")
ax1.set_title('tempo de riscoimento em função do tempo de analise disponível (em meses)')
ax1.legend()

ax2.plot(x_risco, risco_b, 'g', linewidth=1.5, label="Baixo")
ax2.plot(x_risco, risco_m, 'r', linewidth=1.5, label="Médio")
ax2.plot(x_risco, risco_a, 'b', linewidth=1.5, label="Alto")
ax2.set_title('tempo em realizar o riscoimento hoje')
ax2.legend()

for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()



plt.tight_layout()
#plt.show()
'''
'''Regras Fuzzy

SE (DOLAR É MB) E (tempo É MB)
    ENTÃO risco É BAIXO
SE (DOLAR É B) E (tempo É MB)
    ENTÃO risco É BAIXO
SE (DOLAR É M) E (tempo É MB)
    ENTÃO risco É BAIXO
SE (DOLAR É A) E (tempo É MB)
    ENTÃO risco É BAIXO
SE (DOLAR É MA) E (tempo É MB)
    ENTÃO risco É BAIXO

SE (DOLAR É MB) E (tempo É B)
    ENTÃO risco É BAIXO
SE (DOLAR É B) E (tempo É B)
    ENTÃO risco É BAIXO
SE (DOLAR É M) E (tempo É B)
    ENTÃO risco É BAIXO
SE (DOLAR É A) E (tempo É B)
    ENTÃO risco É MEDIO
SE (DOLAR É MA) E (tempo É B)
    ENTÃO risco É MEDIO

SE (DOLAR É MB) E (tempo É M)
    ENTÃO risco É MEDIO
SE (DOLAR É B) E (tempo É M)
    ENTÃO risco É MEDIO
SE (DOLAR É M) E (tempo É M)
    ENTÃO risco É MEDIO
SE (DOLAR É A) E (tempo É M)
    ENTÃO risco É MEDIO
SE (DOLAR É MA) E (tempo É M)
    ENTÃO risco É MEDIO

SE (DOLAR É MB) E (tempo É A)
    ENTÃO risco É MEDIO
SE (DOLAR É B) E (tempo É A)
    ENTÃO risco É MEDIO
SE (DOLAR É M) E (tempo É A)
    ENTÃO risco É ALTO
SE (DOLAR É A) E (tempo É A)
    ENTÃO risco É ALTO
SE (DOLAR É MA) E (tempo É A)
    ENTÃO risco É ALTO

SE (DOLAR É MB) E (tempo É MA)
    ENTÃO risco É ALTO
SE (DOLAR É B) E (tempo É MA)
    ENTÃO risco É ALTO
SE (DOLAR É M) E (tempo É MA)
    ENTÃO risco É ALTO
SE (DOLAR É A) E (tempo É MA)
    ENTÃO risco É ALTO
SE (DOLAR É MA) E (tempo É MA)
    ENTÃO risco É ALTO

'''

d_input = dollar_atual
r_input = int(str(sys.argv[1]).strip(" "))

dolar_level_mb = fuzz.interp_membership(x_dolar, dolar_mb, d_input)
dolar_level_b = fuzz.interp_membership(x_dolar, dolar_b, d_input)
dolar_level_m = fuzz.interp_membership(x_dolar, dolar_m, d_input)
dolar_level_a = fuzz.interp_membership(x_dolar, dolar_a, d_input)
dolar_level_ma = fuzz.interp_membership(x_dolar, dolar_ma, d_input)

tempo_level_b = fuzz.interp_membership(x_tempo, tempo_b, r_input)
tempo_level_m = fuzz.interp_membership(x_tempo, tempo_m, r_input)
tempo_level_a = fuzz.interp_membership(x_tempo, tempo_a, r_input)


# tempo Baixo

rule1 = np.fmax(dolar_level_mb, tempo_level_b)
risco_active_a = np.fmin(rule1, risco_a)

rule2 = np.fmax(dolar_level_b, tempo_level_b)
risco_active_a = np.fmin(rule2, risco_a)

rule3 = np.fmax(dolar_level_m, tempo_level_b)
risco_active_a = np.fmin(rule3, risco_a)

rule4 = np.fmax(dolar_level_a, tempo_level_b)
risco_active_a = np.fmin(rule4, risco_a)

rule5 = np.fmax(dolar_level_ma, tempo_level_b)
risco_active_a = np.fmin(rule5, risco_a)

# tempo Médio

rule6 = np.fmax(dolar_level_mb, tempo_level_m)
risco_active_b = np.fmin(rule6, risco_b)

rule7 = np.fmax(dolar_level_b, tempo_level_m)
risco_active_m = np.fmin(rule7, risco_m)

rule8 = np.fmax(dolar_level_m, tempo_level_m)
risco_active_m = np.fmin(rule8, risco_m)

rule9 = np.fmax(dolar_level_a, tempo_level_m)
risco_active_m = np.fmin(rule9, risco_m)

rule10 = np.fmax(dolar_level_ma, tempo_level_m)
risco_active_a = np.fmin(rule10, risco_a)

# tempo Alto

rule11 = np.fmax(dolar_level_mb, tempo_level_a)
risco_active_b = np.fmin(rule11, risco_b)

rule12 = np.fmax(dolar_level_b, tempo_level_a)
risco_active_b = np.fmin(rule12, risco_b)

rule13 = np.fmax(dolar_level_m, tempo_level_a)
risco_active_b = np.fmin(rule13, risco_b)

rule14 = np.fmax(dolar_level_a, tempo_level_a)
risco_active_b = np.fmin(rule14, risco_b)

rule15 = np.fmax(dolar_level_ma, tempo_level_a)
risco_active_b = np.fmin(rule15, risco_b)

'''
rule1 = np.fmax(tempo_level_b, np.fmax(dolar_level_mb, np.fmax(dolar_level_b, np.fmax(dolar_level_m, np.fmax(dolar_level_a, dolar_level_ma)))))
risco_active_a = np.fmin(rule1, risco_a)

rule2 = np.fmax(tempo_level_m, np.fmax(dolar_level_mb, np.fmax(dolar_level_b, np.fmax(dolar_level_m, np.fmax(dolar_level_a, dolar_level_ma)))))
risco_active_m = np.fmin(rule1, risco_m)

rule3 = np.fmax(tempo_level_a, np.fmax(dolar_level_mb, np.fmax(dolar_level_b, np.fmax(dolar_level_m, np.fmax(dolar_level_a, dolar_level_ma)))))
risco_active_b = np.fmin(rule1, risco_b)
'''

## Desfuzzificação

risco0 = np.zeros_like(x_risco)

aggregated = np.fmax(risco_active_b, np.fmax(risco_active_m, risco_active_a))

risco = fuzz.defuzz(x_risco, aggregated, 'centroid')
risco_activation = fuzz.interp_membership(x_risco, aggregated, risco)

print(risco)

print(risco_activation)

fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.fill_between(x_risco, risco0, risco_active_b, facecolor='b', alpha=0.7)
ax0.plot(x_risco, risco_b, 'b', linewidth=0.5, linestyle='--')
ax0.fill_between(x_risco, risco0, risco_active_m, facecolor='g', alpha=0.7)
ax0.plot(x_risco, risco_m, 'g', linewidth=0.5, linestyle='--')
ax0.fill_between(x_risco, risco0, risco_active_a, facecolor='r', alpha=0.7)
ax0.plot(x_risco, risco_a, 'r', linewidth=0.5, linestyle='--')
ax0.plot([risco, risco], [0, risco_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Conjunto de Saída pertencente')

for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
#plt.show()



# Visualização do Resultado
'''
fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.plot(x_risco, risco_b, 'b', linewidth=0.5, linestyle='--')
ax0.plot(x_risco, risco_m, 'g', linewidth=0.5, linestyle='--')
ax0.plot(x_risco, risco_a, 'r', linewidth=0.5, linestyle='--')
ax0.fill_between(x_risco, risco0, aggregated, facecolor='Orange', alpha=0.7)
ax0.plot([risco, risco], [0, risco_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Conjunto de Saída e Resultado (Linha)')

for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
'''

plt.show()

