import pandas as pd
import numpy as np



def percentual_calibre_amostragem(dataset_talhao_controle):
    dataset_talhao_controle['Percentual'] = (dataset_talhao_controle['FRUTO'] / dataset_talhao_controle['FRUTO'].sum() ) * 100
    dataset_talhao_controle_para_b = dataset_talhao_controle[['CALIBRE','Percentual']]
    dataset_talhao_controle_para_b['Percentual_RECENTE'] = 0
    dataset_talhao_controle_para_b.rename(columns = {'CALIBRE':'Calibre'}, inplace = True)
    return dataset_talhao_controle_para_b


def correcao_calibre(dataset_talhao_controle_para_b):
    if dataset_talhao_controle_para_b['Calibre'] == 'Pequeno':
        return 16
    elif dataset_talhao_controle_para_b['Calibre'] == 'Grande':
        return 100
    else:
        return dataset_talhao_controle_para_b['Calibre']

def logica_inserir_calibre(VARIEDADE, dataset_talhao_controle_para_b):

    if VARIEDADE == 'Tommy Atkins':
#### CALIBRE 4
        result_cal4 = dataset_talhao_controle_para_b.Calibre.isin([4]).any().any()
        if result_cal4:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':4, 'Percentual':0.04}, ignore_index=True)
#### CALIBRE 5
        result_cal5 = dataset_talhao_controle_para_b.Calibre.isin([5]).any().any()
        if result_cal5:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':5, 'Percentual':0.11}, ignore_index=True)
#### CALIBRE 6
        result_cal6 = dataset_talhao_controle_para_b.Calibre.isin([6]).any().any()
        if result_cal6:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':6, 'Percentual':4.18}, ignore_index=True)

#### CALIBRE 7
        result_cal7 = dataset_talhao_controle_para_b.Calibre.isin([7]).any().any()
        if result_cal7:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':7, 'Percentual':9.62}, ignore_index=True)
#### CALIBRE 8
        result_cal8 = dataset_talhao_controle_para_b.Calibre.isin([8]).any().any()
        if result_cal8:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':8, 'Percentual':24.48}, ignore_index=True)
#### CALIBRE 9
        result_cal9 = dataset_talhao_controle_para_b.Calibre.isin([9]).any().any()
        if result_cal9:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':9, 'Percentual':18.52}, ignore_index=True)
#### CALIBRE 10
        result_cal10 = dataset_talhao_controle_para_b.Calibre.isin([10]).any().any()
        if result_cal10:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':10, 'Percentual':27.07}, ignore_index=True)                    
#### CALIBRE 12
        result_cal12 = dataset_talhao_controle_para_b.Calibre.isin([12]).any().any()
        if result_cal12:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':12, 'Percentual':15.50}, ignore_index=True) 
#### CALIBRE 14
        result_cal14 = dataset_talhao_controle_para_b.Calibre.isin([14]).any().any()
        if result_cal14:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':14, 'Percentual':0.53}, ignore_index=True)    
#### CALIBRE 16
        result_cal16 = dataset_talhao_controle_para_b.Calibre.isin([16]).any().any()
        if result_cal16:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':16, 'Percentual':0.09}, ignore_index=True)  

###################################### FAZENDO PARA  A KEITT ######################################


    if VARIEDADE == 'Keitt':
#### CALIBRE 4
        result_cal4 = dataset_talhao_controle_para_b.Calibre.isin([4]).any().any()
        if result_cal4:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
#### CALIBRE 5
        result_cal5 = dataset_talhao_controle_para_b.Calibre.isin([5]).any().any()
        if result_cal5:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':5, 'Percentual':6.91}, ignore_index=True)
#### CALIBRE 6
        result_cal6 = dataset_talhao_controle_para_b.Calibre.isin([6]).any().any()
        if result_cal6:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':6, 'Percentual':22.34}, ignore_index=True)
#### CALIBRE 7
        result_cal7 = dataset_talhao_controle_para_b.Calibre.isin([7]).any().any()
        if result_cal7:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':7, 'Percentual':23.55}, ignore_index=True)
#### CALIBRE 8
        result_cal8 = dataset_talhao_controle_para_b.Calibre.isin([8]).any().any()
        if result_cal8:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':8, 'Percentual':20.83}, ignore_index=True)
#### CALIBRE 9
        result_cal9 = dataset_talhao_controle_para_b.Calibre.isin([9]).any().any()
        if result_cal9:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':9, 'Percentual':8.29}, ignore_index=True)
#### CALIBRE 10
        result_cal10 = dataset_talhao_controle_para_b.Calibre.isin([10]).any().any()
        if result_cal10:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':10, 'Percentual':9.29}, ignore_index=True)                    
#### CALIBRE 12
        result_cal12 = dataset_talhao_controle_para_b.Calibre.isin([12]).any().any()
        if result_cal12:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':12, 'Percentual':7.40}, ignore_index=True) 
#### CALIBRE 14
        result_cal14 = dataset_talhao_controle_para_b.Calibre.isin([14]).any().any()
        if result_cal14:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':14, 'Percentual':0.57}, ignore_index=True)    
#### CALIBRE 16
        result_cal16 = dataset_talhao_controle_para_b.Calibre.isin([16]).any().any()
        if result_cal16:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':16, 'Percentual':0.09}, ignore_index=True)  


###################################### FAZENDO PARA  A KENT ######################################
    if VARIEDADE == 'Kent':
#### CALIBRE 4
        result_cal4 = dataset_talhao_controle_para_b.Calibre.isin([4]).any().any()
        if result_cal4:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
#### CALIBRE 5
        result_cal5 = dataset_talhao_controle_para_b.Calibre.isin([5]).any().any()
        if result_cal5:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':5, 'Percentual':4.71}, ignore_index=True)
#### CALIBRE 6
        result_cal6 = dataset_talhao_controle_para_b.Calibre.isin([6]).any().any()
        if result_cal6:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':6, 'Percentual':23.14}, ignore_index=True)
#### CALIBRE 7
        result_cal7 = dataset_talhao_controle_para_b.Calibre.isin([7]).any().any()
        if result_cal7:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':7, 'Percentual':26.28}, ignore_index=True)
#### CALIBRE 8
        result_cal8 = dataset_talhao_controle_para_b.Calibre.isin([8]).any().any()
        if result_cal8:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':8, 'Percentual':20.25}, ignore_index=True)
#### CALIBRE 9
        result_cal9 = dataset_talhao_controle_para_b.Calibre.isin([9]).any().any()
        if result_cal9:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':9, 'Percentual':9.09}, ignore_index=True)
#### CALIBRE 10
        result_cal10 = dataset_talhao_controle_para_b.Calibre.isin([10]).any().any()
        if result_cal10:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':10, 'Percentual':9.36}, ignore_index=True)                    
#### CALIBRE 12
        result_cal12 = dataset_talhao_controle_para_b.Calibre.isin([12]).any().any()
        if result_cal12:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':12, 'Percentual':6.96}, ignore_index=True) 
#### CALIBRE 14
        result_cal14 = dataset_talhao_controle_para_b.Calibre.isin([14]).any().any()
        if result_cal14:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':14, 'Percentual':0.23}, ignore_index=True)    
#### CALIBRE 16
        result_cal16 = dataset_talhao_controle_para_b.Calibre.isin([16]).any().any()
        if result_cal16:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':16, 'Percentual':0.09}, ignore_index=True)  

###################################### FAZENDO PARA  A PALMER ######################################
    if VARIEDADE =='Palmer':
#### CALIBRE 4
        result_cal4 = dataset_talhao_controle_para_b.Calibre.isin([4]).any().any()
        if result_cal4:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
#### CALIBRE 5
        result_cal5 = dataset_talhao_controle_para_b.Calibre.isin([5]).any().any()
        if result_cal5:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':5, 'Percentual':4.49}, ignore_index=True)
#### CALIBRE 6
        result_cal6 = dataset_talhao_controle_para_b.Calibre.isin([6]).any().any()
        if result_cal6:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':6, 'Percentual':17.28}, ignore_index=True)
#### CALIBRE 7
        result_cal7 = dataset_talhao_controle_para_b.Calibre.isin([7]).any().any()
        if result_cal7:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':7, 'Percentual':17.45}, ignore_index=True)
#### CALIBRE 8
        result_cal8 = dataset_talhao_controle_para_b.Calibre.isin([8]).any().any()
        if result_cal8:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':8, 'Percentual':23.37}, ignore_index=True)
#### CALIBRE 9
        result_cal9 = dataset_talhao_controle_para_b.Calibre.isin([9]).any().any()
        if result_cal9:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':9, 'Percentual':13.22}, ignore_index=True)
#### CALIBRE 10
        result_cal10 = dataset_talhao_controle_para_b.Calibre.isin([10]).any().any()
        if result_cal10:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':10, 'Percentual':15.84}, ignore_index=True)                    
#### CALIBRE 12
        result_cal12 = dataset_talhao_controle_para_b.Calibre.isin([12]).any().any()
        if result_cal12:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':12, 'Percentual':8.10}, ignore_index=True) 
#### CALIBRE 14
        result_cal14 = dataset_talhao_controle_para_b.Calibre.isin([14]).any().any()
        if result_cal14:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':14, 'Percentual':0.25}, ignore_index=True)    
#### CALIBRE 16
        result_cal16 = dataset_talhao_controle_para_b.Calibre.isin([16]).any().any()
        if result_cal16:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':16, 'Percentual':0.00}, ignore_index=True)  

###################################### FAZENDO PARA  A OMER ######################################
    if VARIEDADE =='Omer':
#### CALIBRE 4
        result_cal4 = dataset_talhao_controle_para_b.Calibre.isin([4]).any().any()
        if result_cal4:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
#### CALIBRE 5
        result_cal5 = dataset_talhao_controle_para_b.Calibre.isin([5]).any().any()
        if result_cal5:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':5, 'Percentual':0.00}, ignore_index=True)
#### CALIBRE 6
        result_cal6 = dataset_talhao_controle_para_b.Calibre.isin([6]).any().any()
        if result_cal6:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':6, 'Percentual':3.32}, ignore_index=True)
#### CALIBRE 7
        result_cal7 = dataset_talhao_controle_para_b.Calibre.isin([7]).any().any()
        if result_cal7:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':7, 'Percentual':11.03}, ignore_index=True)
#### CALIBRE 8
        result_cal8 = dataset_talhao_controle_para_b.Calibre.isin([8]).any().any()
        if result_cal8:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':8, 'Percentual':29.07}, ignore_index=True)
#### CALIBRE 9
        result_cal9 = dataset_talhao_controle_para_b.Calibre.isin([9]).any().any()
        if result_cal9:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':9, 'Percentual':19.18}, ignore_index=True)
#### CALIBRE 10
        result_cal10 = dataset_talhao_controle_para_b.Calibre.isin([10]).any().any()
        if result_cal10:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':10, 'Percentual':25.83}, ignore_index=True)                    
#### CALIBRE 12
        result_cal12 = dataset_talhao_controle_para_b.Calibre.isin([12]).any().any()
        if result_cal12:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':12, 'Percentual':11.55}, ignore_index=True) 
#### CALIBRE 14
        result_cal14 = dataset_talhao_controle_para_b.Calibre.isin([14]).any().any()
        if result_cal14:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':14, 'Percentual':0.01}, ignore_index=True)    
#### CALIBRE 16
        result_cal16 = dataset_talhao_controle_para_b.Calibre.isin([16]).any().any()
        if result_cal16:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':16, 'Percentual':0.00}, ignore_index=True)  

###################################### FAZENDO PARA  A PALMER ######################################
    if VARIEDADE =='Osteen':
#### CALIBRE 4
        result_cal4 = dataset_talhao_controle_para_b.Calibre.isin([4]).any().any()
        if result_cal4:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
#### CALIBRE 5
        result_cal5 = dataset_talhao_controle_para_b.Calibre.isin([5]).any().any()
        if result_cal5:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':5, 'Percentual':3.47}, ignore_index=True)
#### CALIBRE 6
        result_cal6 = dataset_talhao_controle_para_b.Calibre.isin([6]).any().any()
        if result_cal6:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':6, 'Percentual':17.51}, ignore_index=True)
#### CALIBRE 7
        result_cal7 = dataset_talhao_controle_para_b.Calibre.isin([7]).any().any()
        if result_cal7:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':7, 'Percentual':26.57}, ignore_index=True)
#### CALIBRE 8
        result_cal8 = dataset_talhao_controle_para_b.Calibre.isin([8]).any().any()
        if result_cal8:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':8, 'Percentual':27.12}, ignore_index=True)
#### CALIBRE 9
        result_cal9 = dataset_talhao_controle_para_b.Calibre.isin([9]).any().any()
        if result_cal9:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':9, 'Percentual':11.42}, ignore_index=True)
#### CALIBRE 10
        result_cal10 = dataset_talhao_controle_para_b.Calibre.isin([10]).any().any()
        if result_cal10:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':10, 'Percentual':9.74}, ignore_index=True)                    
#### CALIBRE 12
        result_cal12 = dataset_talhao_controle_para_b.Calibre.isin([12]).any().any()
        if result_cal12:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':12, 'Percentual':4.00}, ignore_index=True) 
#### CALIBRE 14
        result_cal14 = dataset_talhao_controle_para_b.Calibre.isin([14]).any().any()
        if result_cal14:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':14, 'Percentual':0.19}, ignore_index=True)    
#### CALIBRE 16
        result_cal16 = dataset_talhao_controle_para_b.Calibre.isin([16]).any().any()
        if result_cal16:
            print(' ')
        else:
            dataset_talhao_controle_para_b = dataset_talhao_controle_para_b.append({'Calibre':16, 'Percentual':0.00}, ignore_index=True)  

    return dataset_talhao_controle_para_b




def alteracao_colunas_quality(dataset_quality_piv):
    dataset_quality_piv['TOT_PRIMEIRA'] = dataset_quality_piv['TOT_PRIMEIRA'].astype(str)
    dataset_quality_piv['TOT_SEGUNDA'] = dataset_quality_piv['TOT_SEGUNDA'].astype(str)
    dataset_quality_piv['TOT_TERCEIRA'] = dataset_quality_piv['TOT_TERCEIRA'].astype(str)
    dataset_quality_piv['TOT_REFUGO'] = dataset_quality_piv['TOT_REFUGO'].astype(str)
    dataset_quality_piv = dataset_quality_piv.T
    dataset_quality_piv = dataset_quality_piv.reset_index()
    dataset_quality_piv.rename(columns = {'index':'Qualidade',0:'Percent', 1:'Percent', 2:'Percent', 3:'Percent'}, inplace = True)
    dataset_quality_piv['Percent'] = dataset_quality_piv['Percent'].astype(float)
    return dataset_quality_piv



def mudanca_nomes_qualidades(dataset_quality_piv):
    if dataset_quality_piv['Qualidade'] == 'TOT_PRIMEIRA':
        return 1
    elif dataset_quality_piv['Qualidade'] == 'TOT_SEGUNDA':
        return 2
    elif dataset_quality_piv['Qualidade'] == 'TOT_TERCEIRA':
        return 3
    elif dataset_quality_piv['Qualidade'] == 'TOT_REFUGO':
        return 4


def correcao_qualidade_faltante(VARIEDADE, dataset_quality_piv):
    if VARIEDADE == 'Tommy Atkins':
        #### QUALIDADE 1
        result_QUALI_1 = dataset_quality_piv.Qualidade.isin([1]).any().any()
        if result_QUALI_1:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':1, 'Percent':0.73}, ignore_index=True)

        #### QUALIDADE 2
        result_QUALI_2 = dataset_quality_piv.Qualidade.isin([2]).any().any()
        if result_QUALI_2:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':2, 'Percent':0.16}, ignore_index=True)

        #### QUALIDADE 3
        result_QUALI_3 = dataset_quality_piv.Qualidade.isin([3]).any().any()
        if result_QUALI_3:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':3, 'Percent':0.01}, ignore_index=True)

        #### QUALIDADE 4
        result_QUALI_4 = dataset_quality_piv.Qualidade.isin([4]).any().any()
        if result_QUALI_4:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':4, 'Percent':0.10}, ignore_index=True)
    
    if VARIEDADE == 'Keitt':
        #### QUALIDADE 1
        result_QUALI_1 = dataset_quality_piv.Qualidade.isin([1]).any().any()
        if result_QUALI_1:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':1, 'Percent':0.81}, ignore_index=True)

        #### QUALIDADE 2
        result_QUALI_2 = dataset_quality_piv.Qualidade.isin([2]).any().any()
        if result_QUALI_2:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':2, 'Percent':0.14}, ignore_index=True)

        #### QUALIDADE 3
        result_QUALI_3 = dataset_quality_piv.Qualidade.isin([3]).any().any()
        if result_QUALI_3:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':3, 'Percent':0.0}, ignore_index=True)

        #### QUALIDADE 4
        result_QUALI_4 = dataset_quality_piv.Qualidade.isin([4]).any().any()
        if result_QUALI_4:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':4, 'Percent':0.05}, ignore_index=True)

    if VARIEDADE == 'Kent':
        #### QUALIDADE 1
        result_QUALI_1 = dataset_quality_piv.Qualidade.isin([1]).any().any()
        if result_QUALI_1:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':1, 'Percent':0.82}, ignore_index=True)

        #### QUALIDADE 2
        result_QUALI_2 = dataset_quality_piv.Qualidade.isin([2]).any().any()
        if result_QUALI_2:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':2, 'Percent':0.13}, ignore_index=True)

        #### QUALIDADE 3
        result_QUALI_3 = dataset_quality_piv.Qualidade.isin([3]).any().any()
        if result_QUALI_3:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':3, 'Percent':0.00}, ignore_index=True)

        #### QUALIDADE 4
        result_QUALI_4 = dataset_quality_piv.Qualidade.isin([4]).any().any()
        if result_QUALI_4:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':4, 'Percent':0.05}, ignore_index=True)
    
    if VARIEDADE == 'Palmer':
        #### QUALIDADE 1
        result_QUALI_1 = dataset_quality_piv.Qualidade.isin([1]).any().any()
        if result_QUALI_1:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':1, 'Percent':0.73}, ignore_index=True)

        #### QUALIDADE 2
        result_QUALI_2 = dataset_quality_piv.Qualidade.isin([2]).any().any()
        if result_QUALI_2:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':2, 'Percent':0.15}, ignore_index=True)

        #### QUALIDADE 3
        result_QUALI_3 = dataset_quality_piv.Qualidade.isin([3]).any().any()
        if result_QUALI_3:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':3, 'Percent':0.01}, ignore_index=True)

        #### QUALIDADE 4
        result_QUALI_4 = dataset_quality_piv.Qualidade.isin([4]).any().any()
        if result_QUALI_4:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':4, 'Percent':0.11}, ignore_index=True)

    if VARIEDADE == 'Osteen':
        #### QUALIDADE 1
        result_QUALI_1 = dataset_quality_piv.Qualidade.isin([1]).any().any()
        if result_QUALI_1:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':1, 'Percent':0.72}, ignore_index=True)

        #### QUALIDADE 2
        result_QUALI_2 = dataset_quality_piv.Qualidade.isin([2]).any().any()
        if result_QUALI_2:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':2, 'Percent':0.22}, ignore_index=True)

        #### QUALIDADE 3
        result_QUALI_3 = dataset_quality_piv.Qualidade.isin([3]).any().any()
        if result_QUALI_3:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':3, 'Percent':0.00}, ignore_index=True)

        #### QUALIDADE 4
        result_QUALI_4 = dataset_quality_piv.Qualidade.isin([4]).any().any()
        if result_QUALI_4:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':4, 'Percent':0.06}, ignore_index=True)
    
    if VARIEDADE == 'Omer':
        #### QUALIDADE 1
        result_QUALI_1 = dataset_quality_piv.Qualidade.isin([1]).any().any()
        if result_QUALI_1:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':1, 'Percent':0.78}, ignore_index=True)

        #### QUALIDADE 2
        result_QUALI_2 = dataset_quality_piv.Qualidade.isin([2]).any().any()
        if result_QUALI_2:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':2, 'Percent':0.14}, ignore_index=True)

        #### QUALIDADE 3
        result_QUALI_3 = dataset_quality_piv.Qualidade.isin([3]).any().any()
        if result_QUALI_3:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':3, 'Percent':0.00}, ignore_index=True)

        #### QUALIDADE 4
        result_QUALI_4 = dataset_quality_piv.Qualidade.isin([4]).any().any()
        if result_QUALI_4:
            print(' ')
        else:
            dataset_quality_piv = dataset_quality_piv.append({'Qualidade':4, 'Percent':0.08}, ignore_index=True)
    return dataset_quality_piv



def frutos_controle_palmer(df_media_frutos_caixa):
    if df_media_frutos_caixa['Calibre'] == 4:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.055

    elif df_media_frutos_caixa['Calibre'] == 5:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.8785

    elif df_media_frutos_caixa['Calibre'] == 6:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.666

    elif df_media_frutos_caixa['Calibre'] == 7:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.593

    elif df_media_frutos_caixa['Calibre'] == 8:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5175

    elif df_media_frutos_caixa['Calibre'] == 9:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.458

    elif df_media_frutos_caixa['Calibre'] == 10:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.407

    elif df_media_frutos_caixa['Calibre'] == 12:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.3355

    elif df_media_frutos_caixa['Calibre'] ==14:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2875

    elif df_media_frutos_caixa['Calibre'] == 16:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.230


    #################################################### TOMMY ATKINS #####################################################
def frutos_controle_tommy(df_media_frutos_caixa):
    if  df_media_frutos_caixa['Calibre'] == 4:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.1

    elif df_media_frutos_caixa['Calibre'] == 5:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.940

    elif df_media_frutos_caixa['Calibre'] == 6:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.760

    elif df_media_frutos_caixa['Calibre'] == 7:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5985

    elif  df_media_frutos_caixa['Calibre'] == 8:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5185

    elif  df_media_frutos_caixa['Calibre'] == 9:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.461

    elif df_media_frutos_caixa['Calibre'] == 10:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4065

    elif df_media_frutos_caixa['Calibre'] == 12:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.3335

    elif df_media_frutos_caixa['Calibre'] == 14:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2875

    elif  df_media_frutos_caixa['Calibre'] == 16:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2655
    
#################################################### KEITT #####################################################
def frutos_controle_keitt(df_media_frutos_caixa):
    if df_media_frutos_caixa['Calibre'] == 4:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.2

    elif  df_media_frutos_caixa['Calibre'] == 5:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.825
        
    elif df_media_frutos_caixa['Calibre'] == 6:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.676
        
    elif  df_media_frutos_caixa['Calibre'] == 7:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.604
        
    elif df_media_frutos_caixa['Calibre'] == 8:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5145
        
    elif  df_media_frutos_caixa['Calibre'] == 9:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4575
        
    elif  df_media_frutos_caixa['Calibre'] == 10:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.412
        
    elif  df_media_frutos_caixa['Calibre'] == 12:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.345
        
    elif  df_media_frutos_caixa['Calibre'] == 14:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.292
        
    elif  df_media_frutos_caixa['Calibre'] == 16:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.256
    
    

#################################################### KENT #####################################################
def frutos_controle_kent(df_media_frutos_caixa):

    if df_media_frutos_caixa['Calibre'] == 4:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.115

    elif df_media_frutos_caixa['Calibre'] == 5:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.845
        
    elif df_media_frutos_caixa['Calibre'] == 6:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.693
        
    elif df_media_frutos_caixa['Calibre'] == 7:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5855
        
    elif  df_media_frutos_caixa['Calibre'] == 8:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5105
        
    elif df_media_frutos_caixa['Calibre'] == 9:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.460
        
    elif df_media_frutos_caixa['Calibre'] == 10:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4095
        
    elif df_media_frutos_caixa['Calibre'] == 12:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.339
        
    elif  df_media_frutos_caixa['Calibre'] == 14:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.286
        
    elif df_media_frutos_caixa['Calibre'] == 16:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2545
    

#################################################### OSTEEN #####################################################
def frutos_controle_osteen(df_media_frutos_caixa):

    if df_media_frutos_caixa['Calibre'] == 4:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.243

    elif  df_media_frutos_caixa['Calibre'] == 5:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.882
        
    elif df_media_frutos_caixa['Calibre'] == 6:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.705
        
    elif  df_media_frutos_caixa['Calibre'] == 7:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.594
        
    elif  df_media_frutos_caixa['Calibre'] == 8:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.516
        
    elif  df_media_frutos_caixa['Calibre'] == 9:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4565
        
    elif  df_media_frutos_caixa['Calibre'] == 10:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4045
        
    elif  df_media_frutos_caixa['Calibre'] == 12:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.337
        
    elif  df_media_frutos_caixa['Calibre'] == 14:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2855
        
    elif  df_media_frutos_caixa['Calibre'] == 16:
        return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.249
















