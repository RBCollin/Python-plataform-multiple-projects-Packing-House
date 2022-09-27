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


def contas_auxiliares(Layout_linha,b,quality):

    Layout_linha['Auxiliar'] = Layout_linha['Calibre'] + Layout_linha['Qualidade']
    Layout_linha['Auxiliar2'] = Layout_linha['Calibre2'] + Layout_linha['Qualidade2']
    b['Calibre'] = b['Calibre'].astype(str)
    quality['Qualidade']= quality['Qualidade'].astype(str)

    return Layout_linha, b, quality


def rename_b (b):
    if b['Calibre'] == '4.0' or b['Calibre'] == '4':
        return '4'
    elif b['Calibre'] == '5.0' or b['Calibre'] == '5':
        return '5'
    elif b['Calibre'] == '6.0' or b['Calibre'] == '6':
        return '6'
    elif b['Calibre'] == '7.0' or b['Calibre'] == '7':
        return '7'
    elif b['Calibre'] == '8.0' or b['Calibre'] == '8':
        return '8'
    elif b['Calibre'] == '9.0' or b['Calibre'] == '9':
        return '9'
    elif b['Calibre'] == '10.0' or b['Calibre'] == '10':
        return '10'
    elif b['Calibre'] == '12.0' or b['Calibre'] == '12':
        return '12'
    elif b['Calibre'] == '14.0' or b['Calibre'] == '14':
        return '14'
    elif b['Calibre'] == '16.0' or b['Calibre'] == '16':
        return '16'



def criacao_layout_linhas(Layout_linha, quality, caixotes, avg_frutos_caixotes, b, embaladeira):

    Layout_linha_2 = pd.merge(Layout_linha, quality, on = 'Qualidade', how = 'left')
    Layout_linha_2.rename(columns={'Percent':'P_Quali_1'}, inplace = True)

    Layout_linha_3 = pd.merge(Layout_linha_2, quality, left_on = 'Qualidade2',right_on = 'Qualidade', how = 'left')
    Layout_linha_3.rename(columns={'Percent':'P_Quali_2'}, inplace = True)
    Layout_linha_3 = Layout_linha_3.drop(columns = ['Qualidade_y'])
    

    Layout_linha_4 = pd.merge(Layout_linha_3, b[['Calibre','Percentual']], left_on = 'Calibre', right_on = 'Calibre', how = 'left')
    Layout_linha_4.rename(columns={'Percentual':'P_cal_1'}, inplace = True)

    Layout_linha_5 = pd.merge(Layout_linha_4, b[['Calibre','Percentual']], left_on = 'Calibre2', right_on = 'Calibre', how = 'left')
    Layout_linha_5.rename(columns={'Percentual':'P_cal_2'}, inplace = True)
    
    
    Layout_linha_5 = Layout_linha_5.drop(columns = ['Calibre_y'])
    Layout_linha_5.rename(columns = {'Calibre_x':'Calibre','Qualidade_x':'Qualidade'}, inplace = True)
    
    Layout_linha_5['Frutos'] = (caixotes * avg_frutos_caixotes) * Layout_linha_5['P_cal_1'] * (Layout_linha_5['P_Quali_1']/100)
    Layout_linha_5['Frutos2'] = (caixotes * avg_frutos_caixotes) * Layout_linha_5['P_cal_2'] * (Layout_linha_5['P_Quali_2']/100)
    

##################################### CALCULO DE CAIXAS POR LINHAS ################################################################

    Layout_linha_5['Calibre'] = Layout_linha_5['Calibre'].replace("Refugo","1")
    Layout_linha_5['Calibre'] = Layout_linha_5['Calibre'].replace("Aéreo","2")

    Layout_linha_5['Calibre'] = Layout_linha_5['Calibre'].replace("","1")
    Layout_linha_5['Calibre2'] = Layout_linha_5['Calibre2'].replace("","1")
    

    Layout_linha_5['Calibre'] = Layout_linha_5['Calibre'].astype(float)
    Layout_linha_5['Calibre2'] = Layout_linha_5['Calibre2'].astype(float)

    Layout_linha_5['Caixas'] = Layout_linha_5['Frutos'] / Layout_linha_5['Calibre']
    Layout_linha_5['Caixas2'] = Layout_linha_5['Frutos2'] / Layout_linha_5['Calibre2']

    ##################################### CALCULO DE HORAS POR LINHA ################################################################

    b['Calibre'] = b['Calibre'].astype(float)

    Layout_linha_6 = pd.merge(Layout_linha_5, b[['Calibre','Ritmo']], left_on = 'Calibre', right_on = 'Calibre', how = 'left')
    Layout_linha_6.rename(columns={'Ritmo':'Ritmo_1'}, inplace = True)
    
    Layout_linha_7 = pd.merge(Layout_linha_6, b[['Calibre','Ritmo']], left_on = 'Calibre2', right_on = 'Calibre', how = 'left')
    Layout_linha_7 = Layout_linha_7.drop(columns = ['Calibre_y'])
    Layout_linha_7.rename(columns = {'Ritmo':'Ritmo_2','Calibre_x':'Calibre'}, inplace = True) 

    Layout_linha_7['Horas_1'] = (Layout_linha_7['Caixas'] / Layout_linha_7['Ritmo_1'])
    Layout_linha_7['Horas_1'].fillna(0, inplace = True)

    Layout_linha_7['Horas_2'] = (Layout_linha_7['Caixas2'] / Layout_linha_7['Ritmo_2'])
    Layout_linha_7['Horas_2'].fillna(0, inplace = True)

    Layout_linha_7['Horas'] = Layout_linha_7['Horas_1'] + Layout_linha_7['Horas_2']

    ##################################### CALCULO DE EMBALADEIRAS POR LINHA ################################################################

    
    Layout_linha_7['Embaladeiras'] = round((embaladeira * Layout_linha_7['Horas']) / Layout_linha_7['Horas'].sum(),1)
    
    Layout_linha_7['Embaladeiras_1'] = round((embaladeira * Layout_linha_7['Horas_1']) / Layout_linha_7['Horas'].sum(),1)
    Layout_linha_7['Embaladeiras_2'] = round((embaladeira * Layout_linha_7['Horas_2']) / Layout_linha_7['Horas'].sum(),1)

    return Layout_linha_7



def setores(Layout_linha_7):
    if Layout_linha_7['Linha'] == '1' or Layout_linha_7['Linha'] == '2':
        return 1
    elif Layout_linha_7['Linha'] == '3' or Layout_linha_7['Linha'] == '4' or Layout_linha_7['Linha'] == '5' or Layout_linha_7['Linha'] == '6':
        return 2
    elif Layout_linha_7['Linha'] == '7' or Layout_linha_7['Linha'] == '8' or Layout_linha_7['Linha'] == '9' or Layout_linha_7['Linha'] == '10':
        return 3
    elif Layout_linha_7['Linha'] == '11' or Layout_linha_7['Linha'] == '12' or Layout_linha_7['Linha'] == '13' or Layout_linha_7['Linha'] == '14':
        return 4
    elif Layout_linha_7['Linha'] == '15' or Layout_linha_7['Linha'] == '16' or Layout_linha_7['Linha'] == '17' or Layout_linha_7['Linha'] == '18':
        return 5
    elif Layout_linha_7['Linha'] == '19' or Layout_linha_7['Linha'] == '20' or Layout_linha_7['Linha'] == '21' or Layout_linha_7['Linha'] == '22':
        return 6
    else:
        return 'NADA'


def criando_df_setores(Layout_linha_7):
    df_setores = round(Layout_linha_7.groupby('Setores')['Embaladeiras'].sum(),2)
    df_setores = df_setores.reset_index()
    df_setores['Embaladeiras'] = round(df_setores['Embaladeiras'],0)

    return df_setores



def criando_lay_8(Layout_linha_7):

    Layout_linha_8 = Layout_linha_7[['Linha','Calibre','Qualidade','Calibre2','Qualidade2','Frutos','Frutos2','Caixas','Caixas2','Embaladeiras','Setores','Embaladeiras_1','Embaladeiras_2']]

    Layout_linha_8['Calibre'] = Layout_linha_8['Calibre'].astype(str)
    Layout_linha_8['Calibre'] = Layout_linha_8['Calibre'].replace('1.0',' ')

    Layout_linha_8['Calibre2'] = Layout_linha_8['Calibre2'].astype(str)
    Layout_linha_8['Calibre2'] = Layout_linha_8['Calibre2'].replace('1.0',' ')

    Layout_linha_8  = Layout_linha_8.fillna(0)
    Layout_linha_8 = round(Layout_linha_8,1)
    

    Layout_linha_8 = Layout_linha_8.astype(str)
    Layout_linha_8 = Layout_linha_8.replace('0.0',' ')

    return Layout_linha_8












