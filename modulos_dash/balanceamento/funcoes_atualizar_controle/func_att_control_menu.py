import pandas as pd
import numpy as np


def criando_variaveis_df():
    url = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH'
    variaveis_df = pd.read_json(url)
    return variaveis_df

def criando_embaladeiras_ativas():
    url_embaladeiras_ativas = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenericaMYSQLAvilla?sql=SELECT%20*%20FROM%209090agrodan.vw_dx_emb_presentes'
    df_embaladeiras_ativas = pd.read_json(url_embaladeiras_ativas)
    return df_embaladeiras_ativas

def criando_amostragem():
    url_amostragem = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGAGR.AGR_VW_DX_CALIBRES_CAMPO%20WHERE%201=1%20AND%20SYSDATE%20-%20to_date(DATA,%27yyyy-mm-dd%27)%20%3C=%2060%20AND%20DATA%20IS%20NOT%20NULL'
    df_amostragem_1 = pd.read_json(url_amostragem)
    return df_amostragem_1


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
    if variaveis_df['VARIEDADE'] == 'Palmer' and (variaveis_df['PESO'] <= 1130 and variaveis_df['PESO'] > 980):
        return '4'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 980 and variaveis_df['PESO'] > 777):
        return '5'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 777 and variaveis_df['PESO'] > 630):
        return '6'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 630 and variaveis_df['PESO'] > 557):
        return '7'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 557 and variaveis_df['PESO'] > 478):
        return '8'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 478 and variaveis_df['PESO'] > 438):
        return '9'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 438 and variaveis_df['PESO'] > 376):
        return '10'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 376 and variaveis_df['PESO'] > 295):
        return '12'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 295 and variaveis_df['PESO'] > 280):
        return '14'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] <= 280):
        return '0'
    elif (variaveis_df['VARIEDADE'] == 'Palmer') and (variaveis_df['PESO'] > 1130):
        return '100'
    #################################################### TOMMY ATKINS #####################################################
    elif variaveis_df['VARIEDADE'] == 'Tommy Atkins' and (variaveis_df['PESO'] <= 1200 and variaveis_df['PESO'] > 1000):
        return '4'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 1000 and variaveis_df['PESO'] > 880):
        return '5'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 880 and variaveis_df['PESO'] > 640):
        return '6'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 640 and variaveis_df['PESO'] > 557):
        return '7'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 557 and variaveis_df['PESO'] > 480):
        return '8'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 480 and variaveis_df['PESO'] > 442):
        return '9'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 442 and variaveis_df['PESO'] > 371):
        return '10'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 371 and variaveis_df['PESO'] > 296):
        return '12'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 296 and variaveis_df['PESO'] > 279):
        return '14'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] <= 279):
        return '0'
    elif (variaveis_df['VARIEDADE'] == 'Tommy Atkins') and (variaveis_df['PESO'] > 1200):
        return '100'
        
    #################################################### KEITT #####################################################

    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 1500 and variaveis_df['PESO'] > 880):
        return '4'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 880 and variaveis_df['PESO'] > 770):
        return '5'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 770 and variaveis_df['PESO'] > 622):
        return '6'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 622 and variaveis_df['PESO'] > 553):
        return '7'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 553 and variaveis_df['PESO'] > 476):
        return '8'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 476 and variaveis_df['PESO'] > 439):
        return '9'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 439 and variaveis_df['PESO'] > 385):
        return '10'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 385 and variaveis_df['PESO'] > 305):
        return '12'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 305 and variaveis_df['PESO'] > 279):
        return '14'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] <= 279):
        return '0'
    elif (variaveis_df['VARIEDADE'] == 'Keitt' or variaveis_df['VARIEDADE'] == 'Omer') and (variaveis_df['PESO'] > 1500):
        return '100'

    #################################################### KENT #####################################################
    elif variaveis_df['VARIEDADE'] == 'Kent' and (variaveis_df['PESO'] <= 1300 and variaveis_df['PESO'] > 930):
        return '4'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 930 and variaveis_df['PESO'] > 760):
        return '5'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 760 and variaveis_df['PESO'] > 626):
        return '6'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 626 and variaveis_df['PESO'] > 545):
        return '7'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 545 and variaveis_df['PESO'] > 476):
        return '8'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 476 and variaveis_df['PESO'] > 444):
        return '9'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 444 and variaveis_df['PESO'] > 375):
        return '10'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 375 and variaveis_df['PESO'] > 303):
        return '12'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 303 and variaveis_df['PESO'] > 269):
        return '14'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] <= 269):
        return '0'
    elif (variaveis_df['VARIEDADE'] == 'Kent') and (variaveis_df['PESO'] > 1300):
        return '100'
    #################################################### OSTEEN #####################################################


    elif variaveis_df['VARIEDADE'] == 'Osteen' and (variaveis_df['PESO'] <= 1500 and variaveis_df['PESO'] > 985):
        return '4'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 985 and variaveis_df['PESO'] > 779):
        return '5'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 779 and variaveis_df['PESO'] > 631):
        return '6'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 631 and variaveis_df['PESO'] > 557):
        return '7'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 557 and variaveis_df['PESO'] > 475):
        return '8'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 475 and variaveis_df['PESO'] > 438):
        return '9'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 438 and variaveis_df['PESO'] > 371):
        return '10'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 371 and variaveis_df['PESO'] > 303):
        return '12'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 303 and variaveis_df['PESO'] > 268):
        return '14'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] <= 268):
        return '0'
    elif (variaveis_df['VARIEDADE'] == 'Osteen') and (variaveis_df['PESO'] > 1500):
        return '100' 


def remover_rename(variaveis_df):
    variaveis_df_2 = variaveis_df.drop(columns = ['CONTENTORES'])
    variaveis_df_2.rename(columns={'TOTAL_CONTENTORES':'CONTENTORES'}, inplace = True)

    return variaveis_df_2


def percentual_recente_b(dataset):
    a = dataset['Calibre'].value_counts() / dataset['Calibre'].count()
    b = pd.DataFrame(a)
    b = b.reset_index()
    b.columns = ['Calibre', 'Percentual']
    b['Percentual'] = b['Percentual']*100
    b = b.sort_values('Calibre')
    b['Percentual_RECENTE'] = 0

    return b


def definindo_lista_talhoes(df_amostragem_1):
    df_amostragem_1 = df_amostragem_1[['TALHAO','FRUTO','PESO','CALIBRE']]
    df_amostragem_1_piv = pd.pivot_table(df_amostragem_1, values = ['FRUTO','PESO'], index=['CALIBRE','TALHAO'], aggfunc={'FRUTO': np.sum,'PESO': np.mean})
    df_amostragem_1_piv = df_amostragem_1_piv.reset_index()
    
    lista_talhoes = pd.unique(df_amostragem_1_piv["TALHAO"])   ### ESSA LOGICA SERVE TAMVBEM PARA  FILTRO DE ITENS EM UMA COLUNA DE UMA BASE
    lista_talhoes = pd.DataFrame(lista_talhoes)
    lista_talhoes.rename(columns = {0:'TALHAO'}, inplace = True)
    
    return df_amostragem_1_piv,lista_talhoes

























































































