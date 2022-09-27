import pandas as pd
import numpy as np

def correcao_calibres_de_b(b):
    result_b = b.Calibre.isin([4]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':4, 'Percentual':0}, ignore_index=True)
    
    result_b = b.Calibre.isin([5]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':5, 'Percentual':0}, ignore_index=True)


    result_b = b.Calibre.isin([6]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':6, 'Percentual':0}, ignore_index=True)


    result_b = b.Calibre.isin([7]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':7, 'Percentual':0}, ignore_index=True)


    result_b = b.Calibre.isin([8]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':8, 'Percentual':0}, ignore_index=True)


    result_b = b.Calibre.isin([9]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':9, 'Percentual':0}, ignore_index=True)


    result_b = b.Calibre.isin([10]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':10, 'Percentual':0}, ignore_index=True)


    result_b = b.Calibre.isin([12]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':12, 'Percentual':0}, ignore_index=True)


    result_b = b.Calibre.isin([14]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':14, 'Percentual':0}, ignore_index=True)


    result_b = b.Calibre.isin([16]).any().any()
    if result_b:
        print(' ')
    else:
        b = b.append({'Calibre':16, 'Percentual':0}, ignore_index=True)
    return b


def definindo_percentuais(b):
    percentual_de_4 = b[b.Calibre==4].Percentual.item()
    percentual_de_5 = b[b.Calibre==5].Percentual.item()
    percentual_de_6 = b[b.Calibre==6].Percentual.item()
    percentual_de_7 = b[b.Calibre==7].Percentual.item()
    percentual_de_8 = b[b.Calibre==8].Percentual.item()
    percentual_de_9 = b[b.Calibre==9].Percentual.item()
    percentual_de_10 = b[b.Calibre==10].Percentual.item()
    percentual_de_12 = b[b.Calibre==12].Percentual.item()
    percentual_de_14 = b[b.Calibre==14].Percentual.item()
    percentual_de_16 = b[b.Calibre==16].Percentual.item()

    return percentual_de_4,percentual_de_5,percentual_de_6,percentual_de_7,percentual_de_8,percentual_de_9,percentual_de_10,percentual_de_12,percentual_de_14,percentual_de_16


def correcao_quality(quality):
    result = quality.Qualidade.isin([3]).any().any()
    if result:
        print(' ')
    else:
        quality = quality.append({'Qualidade':3, 'Percent':0}, ignore_index=True)

    result2 = quality.Qualidade.isin([4]).any().any()
    if result2:
        print(' ')
    else:
        quality = quality.append({'Qualidade':4, 'Percent':0}, ignore_index=True)

    result3 = quality.Qualidade.isin([2]).any().any()
    if result3:
        print(' ')
    else:
        quality = quality.append({'Qualidade':2, 'Percent':0}, ignore_index=True)


    result4 = quality.Qualidade.isin([1]).any().any()
    if result4:
        print(' ')
    else:
        quality = quality.append({'Qualidade':1, 'Percent':0}, ignore_index=True)

    quality['Qualidade'] = quality['Qualidade'].astype(int)
    quality = pd.pivot_table(quality, values = 'Percent', aggfunc=np.sum, index = 'Qualidade')
    quality = quality.reset_index()
    
    return quality


def definindo_percentuais_quality(quality):
    primeira_percent = quality[quality.Qualidade==1].Percent.item()
    segunda_percent = quality[quality.Qualidade==2].Percent.item()
    terceira_percent = quality[quality.Qualidade==3].Percent.item()
    refugo_percent = quality[quality.Qualidade==4].Percent.item()
    return primeira_percent,segunda_percent,terceira_percent,refugo_percent


def atribuindo_constantes_iniciais():
    produtividade_embaladeira = 0.75
    produtividade_talo = 0.80
    produtividade_limpeza = 0.75
    produtividade_limpeza2 = 0.75
    return produtividade_embaladeira,produtividade_talo,produtividade_limpeza,produtividade_limpeza2



