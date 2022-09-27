import pandas as pd
import numpy as np
import streamlit as st


def criando_embaladeiras_ativas(allow_output_mutation=True):
    url_embaladeiras_ativas = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenericaMYSQLAvilla?sql=SELECT%20*%20FROM%209090agrodan.vw_dx_emb_presentes'
    df_embaladeiras_ativas = pd.read_json(url_embaladeiras_ativas)
    return df_embaladeiras_ativas

def importando_data_MAF(allow_output_mutation=True):

    url = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH'
    variaveis_df = pd.read_json(url)

    return variaveis_df

def correcao_(variaveis_df):
    if variaveis_df['VARIEDADE'] == 'TOMMY ATKINS':
        return 'Tommy Atkins'
    elif variaveis_df['VARIEDADE'] == 'PALMER':
        return 'Palmer'
    elif variaveis_df['VARIEDADE'] == 'KEITT':
        return 'Keitt'
    elif variaveis_df['VARIEDADE'] == 'KENT':
        return 'Kent'
    elif variaveis_df['VARIEDADE'] == 'OMER':
        return 'Omer'
    elif variaveis_df['VARIEDADE'] == 'OSTEEN':
        return 'Osteen'
    else:
        return 'NADA'

def calibre(variaveis_df):
    if variaveis_df['VARIEDADE'] == 'Palmer':

        if (variaveis_df['PESO'] <= 1130 and variaveis_df['PESO'] > 980):
            return '4'
        elif (variaveis_df['PESO'] <= 980 and variaveis_df['PESO'] > 777):
            return '5'
        elif (variaveis_df['PESO'] <= 777 and variaveis_df['PESO'] > 630):
            return '6'
        elif (variaveis_df['PESO'] <= 630 and variaveis_df['PESO'] > 557):
            return '7'
        elif (variaveis_df['PESO'] <= 557 and variaveis_df['PESO'] > 478):
            return '8'
        elif (variaveis_df['PESO'] <= 478 and variaveis_df['PESO'] > 438):
            return '9'
        elif (variaveis_df['PESO'] <= 438 and variaveis_df['PESO'] > 376):
            return '10'
        elif (variaveis_df['PESO'] <= 376 and variaveis_df['PESO'] > 295):
            return '12'
        elif (variaveis_df['PESO'] <= 295 and variaveis_df['PESO'] > 280):
            return '14'
        elif (variaveis_df['PESO'] <= 280):
            return '0'
        elif (variaveis_df['PESO'] > 1130):
            return '100'


    if variaveis_df['VARIEDADE'] == 'Tommy Atkins':

        if (variaveis_df['PESO'] <= 1200 and variaveis_df['PESO'] > 1000):
            return '4'
        elif (variaveis_df['PESO'] <= 1000 and variaveis_df['PESO'] > 880):
            return '5'
        elif (variaveis_df['PESO'] <= 880 and variaveis_df['PESO'] > 640):
            return '6'
        elif (variaveis_df['PESO'] <= 640 and variaveis_df['PESO'] > 557):
            return '7'
        elif (variaveis_df['PESO'] <= 557 and variaveis_df['PESO'] > 480):
            return '8'
        elif (variaveis_df['PESO'] <= 480 and variaveis_df['PESO'] > 442):
            return '9'
        elif (variaveis_df['PESO'] <= 442 and variaveis_df['PESO'] > 371):
            return '10'
        elif (variaveis_df['PESO'] <= 371 and variaveis_df['PESO'] > 296):
            return '12'
        elif (variaveis_df['PESO'] <= 296 and variaveis_df['PESO'] > 279):
            return '14'
        elif (variaveis_df['PESO'] <= 279):
            return '0'
        elif (variaveis_df['PESO'] > 1200):
            return '100'
        

    if (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer'):

        if (variaveis_df['PESO'] <= 1500 and variaveis_df['PESO'] > 880):
            return '4'
        elif (variaveis_df['PESO'] <= 880 and variaveis_df['PESO'] > 770):
            return '5'
        elif (variaveis_df['PESO'] <= 770 and variaveis_df['PESO'] > 622):
            return '6'
        elif (variaveis_df['PESO'] <= 622 and variaveis_df['PESO'] > 553):
            return '7'
        elif (variaveis_df['PESO'] <= 553 and variaveis_df['PESO'] > 476):
            return '8'
        elif (variaveis_df['PESO'] <= 476 and variaveis_df['PESO'] > 439):
            return '9'
        elif (variaveis_df['PESO'] <= 439 and variaveis_df['PESO'] > 385):
            return '10'
        elif (variaveis_df['PESO'] <= 385 and variaveis_df['PESO'] > 305):
            return '12'
        elif (variaveis_df['PESO'] <= 305 and variaveis_df['PESO'] > 279):
            return '14'
        elif (variaveis_df['PESO'] <= 279):
            return '0'
        elif (variaveis_df['PESO'] > 1500):
            return '100'


    if variaveis_df['VARIEDADE'] == 'Kent':

        if (variaveis_df['PESO'] <= 1300 and variaveis_df['PESO'] > 930):
            return '4'
        elif (variaveis_df['PESO'] <= 930 and variaveis_df['PESO'] > 760):
            return '5'
        elif (variaveis_df['PESO'] <= 760 and variaveis_df['PESO'] > 626):
            return '6'
        elif (variaveis_df['PESO'] <= 626 and variaveis_df['PESO'] > 545):
            return '7'
        elif (variaveis_df['PESO'] <= 545 and variaveis_df['PESO'] > 476):
            return '8'
        elif (variaveis_df['PESO'] <= 476 and variaveis_df['PESO'] > 444):
            return '9'
        elif (variaveis_df['PESO'] <= 444 and variaveis_df['PESO'] > 375):
            return '10'
        elif (variaveis_df['PESO'] <= 375 and variaveis_df['PESO'] > 303):
            return '12'
        elif (variaveis_df['PESO'] <= 303 and variaveis_df['PESO'] > 269):
            return '14'
        elif (variaveis_df['PESO'] <= 269):
            return '0'
        elif (variaveis_df['PESO'] > 1300):
            return '100'


    if variaveis_df['VARIEDADE'] == 'Osteen':

        if (variaveis_df['PESO'] <= 1500 and variaveis_df['PESO'] > 985):
            return '4'
        elif (variaveis_df['PESO'] <= 985 and variaveis_df['PESO'] > 779):
            return '5'
        elif (variaveis_df['PESO'] <= 779 and variaveis_df['PESO'] > 631):
            return '6'
        elif (variaveis_df['PESO'] <= 631 and variaveis_df['PESO'] > 557):
            return '7'
        elif (variaveis_df['PESO'] <= 557 and variaveis_df['PESO'] > 475):
            return '8'
        elif (variaveis_df['PESO'] <= 475 and variaveis_df['PESO'] > 438):
            return '9'
        elif (variaveis_df['PESO'] <= 438 and variaveis_df['PESO'] > 371):
            return '10'
        elif (variaveis_df['PESO'] <= 371 and variaveis_df['PESO'] > 303):
            return '12'
        elif (variaveis_df['PESO'] <= 303 and variaveis_df['PESO'] > 268):
            return '14'
        elif (variaveis_df['PESO'] <= 268):
            return '0'
        elif (variaveis_df['PESO'] > 1500):
            return '100' 

def definindo_dataset(variaveis_df):
    variaveis_df = variaveis_df.drop(columns = ['CONTENTORES'])
    variaveis_df.rename(columns={'TOTAL_CONTENTORES':'CONTENTORES'}, inplace = True)

    dataset = variaveis_df

    dataset.rename(columns = {"PESO":"Peso","CALIBRE":"Calibre","NUMERO_FRUTO":"Fruto","QUALIDADE":"Qualidade","VARIEDADE":"Variedade"}, inplace = True)

    return dataset

def ajustes_DATA_MAF(dataset_MAF):
    dataset_MAF = dataset_MAF.dropna()
    dataset_MAF = dataset_MAF.drop(columns = ['CONTROLE_MAF'])
    dataset_MAF['Calibre'] = dataset_MAF['CALIBRE_QUALIDADE'].str[:3]
    dataset_MAF['Qualidade'] = dataset_MAF['CALIBRE_QUALIDADE'].str[3:]

    return dataset_MAF

def correcao_calibre_MAF(dataset_MAF):
    if dataset_MAF['Calibre'] == 'C05':
        return 5
    elif dataset_MAF['Calibre'] == 'C04':
        return 4
    elif dataset_MAF['Calibre'] == 'C06':
        return 6
    elif dataset_MAF['Calibre'] == 'C07':
        return 7
    elif dataset_MAF['Calibre'] == 'C08':
        return 8
    elif dataset_MAF['Calibre'] == 'C09':
        return 9
    elif dataset_MAF['Calibre'] == 'C10':
        return 10
    elif dataset_MAF['Calibre'] == 'C12':
        return 12
    elif dataset_MAF['Calibre'] == 'C14':
        return 14
    elif dataset_MAF['Calibre'] == 'C16':
        return 16
    elif dataset_MAF['Calibre'] == 'Ref':
        return 0

def ajuste_final(dataset_MAF):
    if dataset_MAF['Calibre'] == '0':
        return 'Refugo'
    else:
        return dataset_MAF['Calibre']

def correcao_qualidade_MAF(dataset_MAF):
    if dataset_MAF['Qualidade'] == ' Q1':
        return 1
    elif dataset_MAF['Qualidade'] == ' Q2':
        return 2
    elif dataset_MAF['Qualidade'] == ' Q3':
        return 3
    elif dataset_MAF['Qualidade'] == 'ugo':
        return 4

def correcao_variedade_maf(dataset_MAF):
    if dataset_MAF['VARIEDADE'] == 'TOMMY':
        return "Tommy Atkins"
    elif dataset_MAF['VARIEDADE'] == 'TAMMY':
        return "Tommy Atkins"
    elif dataset_MAF['VARIEDADE'] == 'KEITT':
        return "Keitt"
    elif dataset_MAF['VARIEDADE'] == 'KENT':
        return "Kent"
    elif dataset_MAF['VARIEDADE'] == 'PALMER' or dataset_MAF['VARIEDADE'] == 'PALMER.':
        return "Palmer"
    elif dataset_MAF['VARIEDADE'] == 'OMER':
        return 'Omer'
    elif dataset_MAF['VARIEDADE'] == 'OSTEEN':
        return 'Osteen'

def som_frutos(dataset_MAF):

    somatorio_frutos_peso = pd.pivot_table(dataset_MAF, index = 'Calibre', values = ['QTD_FRUTOS','PESO_KG','QTD_FRUTOS_RECENTE','PESO_KG_RECENTE'],aggfunc= 'sum')
    somatorio_frutos_peso = somatorio_frutos_peso.reset_index()
    somatorio_frutos_peso['Percentual'] = (somatorio_frutos_peso['QTD_FRUTOS'] / somatorio_frutos_peso['QTD_FRUTOS'].sum()) * 100
    somatorio_frutos_peso['Percentual_RECENTE'] = (somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / somatorio_frutos_peso['QTD_FRUTOS_RECENTE'].sum()) * 100

    return somatorio_frutos_peso

def som_frutos_qualid(dataset_MAF):

    somatorio_qualidade = pd.pivot_table(dataset_MAF, index = 'Qualidade', values = ['QTD_FRUTOS'],aggfunc= 'sum')
    somatorio_qualidade = somatorio_qualidade.reset_index()
    somatorio_qualidade['Percent'] = (somatorio_qualidade['QTD_FRUTOS'] / somatorio_qualidade['QTD_FRUTOS'].sum())

    return somatorio_qualidade

def somatorio_qualdidade_replace(somatorio_qualidade):

    result = somatorio_qualidade.Qualidade.isin([3]).any().any()
    if result:
        print(' ')
    else:
        somatorio_qualidade = somatorio_qualidade.append({'Qualidade':3, 'Percent':0}, ignore_index=True)

    result2 = somatorio_qualidade.Qualidade.isin([4]).any().any()
    if result2:
        print(' ')
    else:
        somatorio_qualidade = somatorio_qualidade.append({'Qualidade':4, 'Percent':0}, ignore_index=True)

    result3 = somatorio_qualidade.Qualidade.isin([2]).any().any()
    if result3:
        print(' ')
    else:
        somatorio_qualidade = somatorio_qualidade.append({'Qualidade':2, 'Percent':0}, ignore_index=True)
    
    result4 = somatorio_qualidade.Qualidade.isin([1]).any().any()
    if result4:
        print(' ')
    else:
        somatorio_qualidade = somatorio_qualidade.append({'Qualidade':1, 'Percent':0}, ignore_index=True)

    return somatorio_qualidade

def corr_(somatorio_qualidade):
    if somatorio_qualidade['Qualidade'] == 1.0:
        return 1
    elif somatorio_qualidade['Qualidade'] == 2.0:
        return 2
    elif somatorio_qualidade['Qualidade'] == 3.0:
        return 3
    elif somatorio_qualidade['Qualidade'] == 4.0:
        return 4

def somatorio_ajuste_calibres_correcao(somatorio_frutos_peso):

    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['5']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'5', 'Percentual':0}, ignore_index=True)
    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['6']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'6', 'Percentual':0}, ignore_index=True)
    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['7']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'7', 'Percentual':0}, ignore_index=True)


    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['8']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'8', 'Percentual':0}, ignore_index=True)


    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['9']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'9', 'Percentual':0}, ignore_index=True)


    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['10']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'10', 'Percentual':0}, ignore_index=True)


    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['12']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'12', 'Percentual':0}, ignore_index=True)


    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['14']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'14', 'Percentual':0}, ignore_index=True)


    result_somatorio_frutos_peso = somatorio_frutos_peso.Calibre.isin(['16']).any().any()
    if result_somatorio_frutos_peso:
        print(' ')
    else:
        somatorio_frutos_peso = somatorio_frutos_peso.append({'Calibre':'16', 'Percentual':0}, ignore_index=True)
    return somatorio_frutos_peso

def frutos_controle_keitt(df_media_frutos_caixa):
        if df_media_frutos_caixa['Calibre'] == '4':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.2

        elif df_media_frutos_caixa['Calibre'] == '5':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.825
            
        elif df_media_frutos_caixa['Calibre'] == '6':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.676
            
        elif df_media_frutos_caixa['Calibre'] == '7':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.604
            
        elif df_media_frutos_caixa['Calibre'] == '8':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5145
            
        elif df_media_frutos_caixa['Calibre'] == '9':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4575
            
        elif df_media_frutos_caixa['Calibre'] == '10':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.412
            
        elif df_media_frutos_caixa['Calibre'] == '12':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.345
            
        elif df_media_frutos_caixa['Calibre'] == '14':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.292
            
        elif df_media_frutos_caixa['Calibre'] == '16':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.256

def frutos_controle_palmer(df_media_frutos_caixa):

        if df_media_frutos_caixa['Calibre'] == '4':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.055

        elif df_media_frutos_caixa['Calibre'] == '5':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.8785

        elif df_media_frutos_caixa['Calibre'] == '6':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.666

        elif df_media_frutos_caixa['Calibre'] == '7':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.593

        elif df_media_frutos_caixa['Calibre'] == '8':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5175

        elif df_media_frutos_caixa['Calibre'] == '9':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.458

        elif df_media_frutos_caixa['Calibre'] == '10':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.407

        elif df_media_frutos_caixa['Calibre'] == '12':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.3355

        elif df_media_frutos_caixa['Calibre'] == '14':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2875

        elif df_media_frutos_caixa['Calibre'] == '16':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.230

def frutos_controle_tommy(df_media_frutos_caixa):

        if df_media_frutos_caixa['Calibre'] == '4':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.1

        elif df_media_frutos_caixa['Calibre'] == '5':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.940

        elif df_media_frutos_caixa['Calibre'] == '6':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.760

        elif df_media_frutos_caixa['Calibre'] == '7':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5985

        elif df_media_frutos_caixa['Calibre'] == '8':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5185

        elif df_media_frutos_caixa['Calibre'] == '9':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.461

        elif df_media_frutos_caixa['Calibre'] == '10':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4065

        elif df_media_frutos_caixa['Calibre'] == '12':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.3335

        elif df_media_frutos_caixa['Calibre'] == '14':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2875

        elif df_media_frutos_caixa['Calibre'] == '16':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2655

def frutos_controle_kent(df_media_frutos_caixa):

        if df_media_frutos_caixa['Calibre'] == '4':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.115

        elif df_media_frutos_caixa['Calibre'] == '5':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.845
            
        elif df_media_frutos_caixa['Calibre'] == '6':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.693
            
        elif df_media_frutos_caixa['Calibre'] == '7':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5855
            
        elif df_media_frutos_caixa['Calibre'] == '8':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5105
            
        elif df_media_frutos_caixa['Calibre'] == '9':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.460
            
        elif df_media_frutos_caixa['Calibre'] == '10':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4095
            
        elif df_media_frutos_caixa['Calibre'] == '12':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.339
            
        elif df_media_frutos_caixa['Calibre'] == '14':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.286
            
        elif df_media_frutos_caixa['Calibre'] == '16':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2545
        
def frutos_controle_osteen(df_media_frutos_caixa):

        if df_media_frutos_caixa['Calibre'] == '4':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.243

        elif df_media_frutos_caixa['Calibre'] == '5':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.882
            
        elif df_media_frutos_caixa['Calibre'] == '6':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.705
            
        elif df_media_frutos_caixa['Calibre'] == '7':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.594
            
        elif df_media_frutos_caixa['Calibre'] == '8':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.516
            
        elif df_media_frutos_caixa['Calibre'] == '9':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4565
            
        elif df_media_frutos_caixa['Calibre'] == '10':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4045
            
        elif df_media_frutos_caixa['Calibre'] == '12':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.337
            
        elif df_media_frutos_caixa['Calibre'] == '14':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2855
            
        elif df_media_frutos_caixa['Calibre'] == '16':
            return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.249

def caixas_maf(somatorio_frutos_peso):
    if somatorio_frutos_peso['Calibre'] == 4:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 4
    elif somatorio_frutos_peso['Calibre'] == 5:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 5
    elif somatorio_frutos_peso['Calibre'] == 6:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 6
    elif somatorio_frutos_peso['Calibre'] == 7:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 7
    elif somatorio_frutos_peso['Calibre'] == 8:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 8
    elif somatorio_frutos_peso['Calibre'] == 9:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 9
    elif somatorio_frutos_peso['Calibre'] == 10:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 10
    elif somatorio_frutos_peso['Calibre'] == 12:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 12
    elif somatorio_frutos_peso['Calibre'] == 14:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 14
    elif somatorio_frutos_peso['Calibre'] == 16:
        return somatorio_frutos_peso['QTD_FRUTOS'] / 16

def caixas_maf_recente(somatorio_frutos_peso):
    if somatorio_frutos_peso['Calibre'] == 4:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 4
    elif somatorio_frutos_peso['Calibre'] == 5:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 5
    elif somatorio_frutos_peso['Calibre'] == 6:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 6
    elif somatorio_frutos_peso['Calibre'] == 7:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 7
    elif somatorio_frutos_peso['Calibre'] == 8:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 8
    elif somatorio_frutos_peso['Calibre'] == 9:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 9
    elif somatorio_frutos_peso['Calibre'] == 10:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 10
    elif somatorio_frutos_peso['Calibre'] == 12:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 12
    elif somatorio_frutos_peso['Calibre'] == 14:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 14
    elif somatorio_frutos_peso['Calibre'] == 16:
        return somatorio_frutos_peso['QTD_FRUTOS_RECENTE'] / 16










