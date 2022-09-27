import pandas as pd 
import numpy as np

def lay_9(Layout_linha_9):

    Layout_linha_9 = Layout_linha_9.drop(columns = ['Unnamed: 0'])
    Layout_linha_9['Setores'] = Layout_linha_9['Setores'].astype(str)

    Layout_linha_9['Embaladeiras'] = Layout_linha_9['Embaladeiras'].replace(' ','0')
    Layout_linha_9['Embaladeiras'] = Layout_linha_9['Embaladeiras'].astype(float)

    Layout_linha_9['Embaladeiras_1'] = Layout_linha_9['Embaladeiras_1'].replace(' ','0')
    Layout_linha_9['Embaladeiras_1'] = Layout_linha_9['Embaladeiras_1'].astype(float)

    Layout_linha_9['Embaladeiras_2'] = Layout_linha_9['Embaladeiras_2'].replace(' ','0')
    Layout_linha_9['Embaladeiras_2'] = Layout_linha_9['Embaladeiras_2'].astype(float)

    return Layout_linha_9


def correcao_variedade(padrao_embaldeiras):
    if padrao_embaldeiras['VARIEDADE'] == 'Tommy ':
        return 'Tommy Atkins'
    elif padrao_embaldeiras['VARIEDADE'] == 'Keitt ':
        return 'Keitt'
    else:
        return padrao_embaldeiras['VARIEDADE']



def ritmos_de_b(b, produtividade_embaladeira, embaladeira): 

    filtro = b['Ritmo_embaladeira'] != 'NADA'
    b = b[filtro]

    b['Horas_4kg_embaladeiras'] = (b['Caixas_total'] / b['Ritmo_embaladeira']) / produtividade_embaladeira 

    ton_horas_embaladeiras = round(((b['Caixas_total'].sum()*4.05)/1000)/(b['Horas_4kg_embaladeiras'].sum()/embaladeira),2)

    return b, ton_horas_embaladeiras
























