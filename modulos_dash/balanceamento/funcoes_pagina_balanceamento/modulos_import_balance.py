import pandas as pd
import numpy as np

def contas_caixas_e_horas(b,caixotes, avg_frutos_caixotes,primeira_percent,segunda_percent,terceira_percent, produtividade_embaladeira):

        b['Caixas_total'] = ((caixotes * avg_frutos_caixotes * b['Percentual']) / b['Calibre']) / 100
        b['Caixas_1'] = ((caixotes * avg_frutos_caixotes * (b['Percentual']/100) * primeira_percent) / b['Calibre']) 
        b['Caixas_2'] = ((caixotes * avg_frutos_caixotes * (b['Percentual']/100) * segunda_percent)  / b['Calibre']) 
        b['Caixas_3'] = ((caixotes * avg_frutos_caixotes * (b['Percentual']/100) * terceira_percent) / b['Calibre'])
        b['Horas_4kg'] = (b['Caixas_total'] / b['Ritmo']) / produtividade_embaladeira   

        return b 

def contas_balanceamento(b, embaladeira, caixotes, avg_frutos_caixotes, produtividade_talo):

    ritmo_embaladeira = ((b['Horas_4kg'].sum()  / embaladeira) * (1/24))
    corte_talo = round((caixotes * avg_frutos_caixotes) / (101303.19 * produtividade_talo * ritmo_embaladeira))
    ritmo_talo = ((((caixotes * avg_frutos_caixotes) / corte_talo) / (4200 * produtividade_talo)) * (1/24))
    diferenca_aceitavel = abs(round((ritmo_embaladeira - ritmo_talo),3))
    corte_talo2 = corte_talo
    ritmo_talo_2 = ((((caixotes * avg_frutos_caixotes) / corte_talo2) / (4200 * produtividade_talo)) * (1/24))

    return ritmo_embaladeira, corte_talo, ritmo_talo, diferenca_aceitavel, corte_talo2, ritmo_talo_2



def contas_dentro_da_def_equilibrio(caixotes,ritmo_talo_2,avg_frutos_caixotes, produtividade_limpeza,b,embaladeira,segunda_percent,terceira_percent,refugo_percent,produtividade_limpeza2,primeira_percent,corte_talo2):

    caixotes_hora = round((caixotes*0.0416667)/(ritmo_talo_2))
    Limpeza_selecao = round((caixotes_hora * avg_frutos_caixotes * 0.6) / (3230 * produtividade_limpeza))
    ton_horas = round(((b['Caixas_total'].sum()*4.05)/1000)/(b['Horas_4kg'].sum()/embaladeira),2)
    soma = segunda_percent + terceira_percent + refugo_percent                
    selecao_ = round((caixotes_hora * avg_frutos_caixotes * soma / (3501 * produtividade_limpeza2)) + (caixotes_hora * avg_frutos_caixotes * primeira_percent / (6480 * produtividade_limpeza2)))

    corte_talo3 = str(corte_talo2)
    selecao__3 = str(selecao_)
    Limpeza_selecao_2 = str(Limpeza_selecao)
    caixotes_hora_2 = str(caixotes_hora)
    ton_horas_2 = str(ton_horas)

    return corte_talo3, selecao__3, Limpeza_selecao_2, caixotes_hora_2, ton_horas_2, caixotes_hora, ton_horas


def criando_c_and_dt33(dataset_33):
    dataset_33 = dataset_33.sort_values(['Calibre'])
    dataset_33['Calibre Name'] = dataset_33['Calibre'].astype(str)
    c = round(dataset_33['Percentual'],2)

    return dataset_33, c
