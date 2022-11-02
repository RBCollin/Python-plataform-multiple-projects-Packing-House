from math import ceil
from requests import HTTPError
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
from dateutil.parser import parse
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import requests
import torch
import torchvision
import sqlite3



st.set_page_config(layout="wide")

selected = option_menu(
    menu_title = 'Packing House - Projetos',
    options = ['Balanceamento','Previsão e Histórico','Produtividade PH','Etiquetas','Count Test'],
    icons = ['plus-slash-minus','bar-chart-line-fill','graph-up-arrow','card-heading','camera-video-off-fill'],
    menu_icon = 'box-seam',
    default_index = 0,
    orientation = 'horizontal',
    styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#f56e00", "font-size": "16px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#009b36","font-size": "16px"},
        }
)

if selected == 'Balanceamento':


    with open ('style.css') as f:
        st.markdown(f'<style>{f.read()}<style>', unsafe_allow_html=True)

    coluna_inicial_1, coluna_inicial_2 = st.columns([0.8,1])
    with coluna_inicial_1:
        st.title('Packing House - Linhas de Embalagem')

    with coluna_inicial_2:
        
        st.write('')
        st.write('')


########  CRIAR UMA ST.SELECTBOX COM OS TALHOES E CONTROLES DA BASE
########  PARA ISSO A BASE DO MEGA TEM QUE SER EXATAMENTE IGUAL POREM COM TODOS OS CONTROLES QUE ELE QUER CONSULTAR
########  CRTL + C DE TODO O CODIGO PARA RECRIAR UM PARA A BJ
######## POREM PADRAO DE LINHAS, RITMO, PRODUTIVIDADE VÃO SER TUDO DIFERENTE, É OUTRO PH


        if st.button('Atualizar Controle'):

            from modulos_dash.balanceamento.funcoes_atualizar_controle.func_att_control_menu import *

            variaveis_df,df_embaladeiras_ativas , df_amostragem_1 = criando_variaveis_df(), criando_embaladeiras_ativas(),criando_amostragem()

            st.session_state.dataframe_amostragem = df_amostragem_1 


            talhao_controle_1 = variaveis_df['TALHAO'][0]
            st.session_state.talhao_control = talhao_controle_1


            variaveis_df['VARIEDADE'] = variaveis_df.apply(correcao_, axis = 1)
            variaveis_df['CALIBRE'] = variaveis_df.apply(calibre, axis =1)
            variaveis_df = remover_rename(variaveis_df)


            dataset = variaveis_df


            controle = dataset['CONTROLE'][0]
            st.session_state.control = controle

            VARIEDADE = dataset['VARIEDADE'][0]
            st.session_state.variety = VARIEDADE


            dataset.rename(columns = {"PESO":"Peso","CALIBRE":"Calibre","NUMERO_FRUTO":"Fruto","QUALIDADE":"Qualidade","VARIEDADE":"Variedade"}, inplace = True)
            try:
                dataset['Calibre'] = dataset['Calibre'].astype(int)
            except TypeError:
                st.write('### Erro com a base do mega !! ')
            
            peso_total_controle = dataset['PESO_CONTROLE'][0]
            peso_total_controle = round(peso_total_controle,2)
            peso_total_controle = str(peso_total_controle)
            st.write('Peso total do controle:',peso_total_controle, 'ton')
            

            b = percentual_recente_b(dataset)

            st.session_state.b_ = b
            st.session_state.anterior = variaveis_df


            if len(df_embaladeiras_ativas) == 0:
                url_embaladeiras_ativas = 'http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_EMB_ATIVAS'
                df_embaladeiras_ativas = pd.read_json(url_embaladeiras_ativas)


            df_embaladeiras_ativas.rename(columns = {'CPF':'MATRICULA','PESSOA':'NOME'}, inplace = True)
            df_embaladeiras_ativas['NOME'] = df_embaladeiras_ativas['NOME'].str[6:]


            st.session_state.url_embala = df_embaladeiras_ativas

            quality = dataset['Qualidade'].value_counts() / dataset['Qualidade'].count()
            quality = pd.DataFrame(quality)
            quality = quality.reset_index()
            quality.columns = ['Qualidade','Percent']

            st.session_state.quality_percent = quality
            produtividade_atual = 38
            st.session_state.prod_MAF = produtividade_atual
            
            st.session_state.cxs_recentes = 100000
            
            st.session_state.cxs_process = 0
            tempo = 0
            st.session_state_tempo = tempo
            
            st.session_state.media_frutos_caixotes = 30


            st.session_state.grafico_passado = b


            if len(b) == 1:

                @st.experimental_memo
                def get_data() -> pd.DataFrame:
                    return pd.read_excel('C:/Users/bernard.collin/Desktop/planilha_denilton/pred_semanas/Comportamento_calibres_TALHAO.xlsx')

                df_comportamento_calibres_TALHAO = get_data()

                @st.experimental_memo
                def get_data2() -> pd.DataFrame:
                    return pd.read_excel('C:/Users/bernard.collin/Desktop/planilha_denilton/pred_semanas/df_cleanref_TALHAO.xlsx')


                df_comportamento_qualidade = get_data2()
                
                lista_talhoes = pd.unique(df_comportamento_calibres_TALHAO["TALHAO"]) 
                lista_talhoes = pd.DataFrame(lista_talhoes)
                lista_talhoes.rename(columns = {0:'TALHAO'}, inplace = True)

                talhao_controle = st.session_state.talhao_control
                result_talhao_2 = lista_talhoes.TALHAO.isin([talhao_controle]).any().any()
               
                @st.experimental_memo
                def criando_gg(allow_output_mutation=True):
                    data = requests.get("http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.DXDW_HISTORICO_CALIBRES")
                    json_data = data.json()
                    df_piv_2=pd.json_normalize(json_data)
                    df_piv_2 = pd.DataFrame.from_dict(df_piv_2)
                    dataset = pd.DataFrame(df_piv_2)
                    return dataset
                dataset_teste = criando_gg()
                
                # data = requests.get("http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.DXDW_HISTORICO_CALIBRES")
                # json_data = data.json()
                # df_piv_2=pd.json_normalize(json_data)
                # df_piv_2 = pd.DataFrame.from_dict(df_piv_2)
                # dataset = pd.DataFrame(df_piv_2)

                filtro_calibre = dataset_teste['VALOR_CALIBRE'] != 'CALIBRE_11'
                dataset_teste = dataset_teste[filtro_calibre]

                filtro_calibre2 = dataset_teste['VALOR_CALIBRE'] != 'CALIBRE_13'
                datasdataset_testeet = dataset_teste[filtro_calibre2]

                dataset_teste['CALIBRE'] = dataset_teste['CALIBRE'] * 100
  
                dataset_teste.rename(columns = {'VALOR_CALIBRE':'Calibre'}, inplace = True)

                dd = dataset_teste.groupby('TALH_ST_DESCRICAO').SAFRA_ST_CODIGO.value_counts()
                ee = pd.DataFrame(dd)
                ee = ee.drop(columns = ['SAFRA_ST_CODIGO'])
                ee = ee.reset_index()
                ee = ee.drop(columns = ['SAFRA_ST_CODIGO'])
                lista_talhoes_teste = ee

                result_talhao_teste = lista_talhoes_teste.TALH_ST_DESCRICAO.isin([talhao_controle]).any().any() 

                dataset_teste_filtro = dataset_teste['TALH_ST_DESCRICAO'] == talhao_controle
                dataset_teste_filtrado = dataset_teste[dataset_teste_filtro]
                

                filtro_max = dataset_teste_filtrado['ORDEM'] == dataset_teste_filtrado['ORDEM'].max()
                dataset_teste_filtrado_recente = dataset_teste_filtrado[filtro_max]

            
                if result_talhao_teste:

                    st.write('Base do histórico do controle mais recente')

                    from modulos_dash.balanceamento.funcoes_atualizar_controle.funcoes_else_base_amostragem import *

                    dataset_teste_filtrado_recente['Calibre'] = dataset_teste_filtrado_recente.apply(correcao_calibre_new, axis = 1)
                    dataset_teste_filtrado_recente['Percentual_RECENTE'] = 0
                    dataset_teste_filtrado_recente = dataset_teste_filtrado_recente.drop(columns = ['TALH_ST_DESCRICAO'])
                    dataset_teste_filtrado_recente.rename(columns = {'CALIBRE':'Percentual'}, inplace = True)
                    dataset_teste_filtrado_recente = dataset_teste_filtrado_recente.drop(columns = ['SAFRA_ST_CODIGO','VARIEDADE','CPROC_IN_CODIGO','DATA_EMBALAGEM','ORDEM'])
                    dataset_teste_filtrado_recente = dataset_teste_filtrado_recente[['Calibre','Percentual','Percentual_RECENTE']]
                    dataset_teste_filtrado_recente['Calibre'] = dataset_teste_filtrado_recente['Calibre'].astype(float)
                    dataset_teste_filtrado_recente['Percentual_RECENTE'] = dataset_teste_filtrado_recente['Percentual_RECENTE'].astype(float)


                    df_comportamento_calibres_TALHAO_PIV = dataset_teste_filtrado_recente
                    df_comportamento_calibres_TALHAO_PIV = correcao_calibre_media_variedade(VARIEDADE,df_comportamento_calibres_TALHAO_PIV)
                    #df_comportamento_calibres_TALHAO_PIV



                    df_graficos_passado  = df_comportamento_calibres_TALHAO_PIV
                    st.session_state.grafico_passado = df_graficos_passado

                    st.session_state.b_ = df_comportamento_calibres_TALHAO_PIV
                        
                    lista_talhoes_quality = pd.unique(df_comportamento_qualidade["TALHAO"])   
                    lista_talhoes_quality = pd.DataFrame(lista_talhoes_quality)
                    lista_talhoes_quality.rename(columns = {0:'TALHAO'}, inplace = True)            

                    result_talhao_3_ = lista_talhoes_quality.TALHAO.isin([talhao_controle]).any().any()

                    if result_talhao_3_:

                        filtro_talhao_quality = df_comportamento_qualidade['TALHAO'] == talhao_controle
                        df_comportamento_qualidade = df_comportamento_qualidade[filtro_talhao_quality] 
                        dataset_quality_piv = pd.pivot_table(df_comportamento_qualidade, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['TALHAO'], aggfunc = np.mean)
                        dataset_quality_piv = dataset_quality_piv.reset_index()
                        
                        dataset_quality_piv = dataset_quality_piv.drop(columns = ['TALHAO'])
                        

                    else:
                        #st.write('PRA QUALIDADE VOU USAR O FILTRO VARIEDADE')

                        if VARIEDADE == 'Tommy Atkins':
                            VARIEDADE_2 = 'TOMMY'
                        if VARIEDADE == 'Keitt':
                            VARIEDADE_2 = 'KEITT'
                        if VARIEDADE == 'Kent':
                            VARIEDADE_2 = 'KENT'
                        if VARIEDADE == 'Palmer':
                            VARIEDADE_2 = 'PALMER'
                        if VARIEDADE == 'Osteen':
                            VARIEDADE_2 = 'OSTEEN'
                        if VARIEDADE == 'Omer':
                            VARIEDADE_2 = 'OMER'
                        try:
                            filtro_talhao_quality = df_comportamento_qualidade['VARIEDADE'] == VARIEDADE_2
                            df_comportamento_qualidade = df_comportamento_qualidade[filtro_talhao_quality] 
                        except NameError:
                            st.write('#### Variedade faltando no mega, atualize novamente em alguns minutos')
                        

                        dataset_quality_piv = pd.pivot_table(df_comportamento_qualidade, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['VARIEDADE'], aggfunc = np.mean)
                        dataset_quality_piv = dataset_quality_piv.reset_index()
                        dataset_quality_piv = dataset_quality_piv.drop(columns = ['VARIEDADE'])

                        
                    dataset_quality_piv = tratamento_dataset_quality_piv(dataset_quality_piv)

                    dataset_quality_piv['Qualidade'] = dataset_quality_piv.apply(mudanca_nomes_qualidades, axis = 1)
                    dataset_quality_piv['Percent'] = dataset_quality_piv['Percent'] / 100

                    dataset_quality_piv = correcao_qualidade_para_variedade(VARIEDADE,dataset_quality_piv)

                    st.session_state.quality_percent = dataset_quality_piv

                    toneladas_totais_controle = dataset['PESO_CONTROLE'][0].item() * 1000
                    df_media_frutos_caixa = df_comportamento_calibres_TALHAO_PIV
                    df_media_frutos_caixa['Quilos/calibre/controle'] = toneladas_totais_controle * (df_media_frutos_caixa['Percentual']/100)
                    

                    if VARIEDADE == 'Palmer':
                        df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_palmer, axis = 1)
                    if VARIEDADE == 'Tommy Atkins':
                        df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_tommy, axis = 1)
                    if VARIEDADE == 'Keitt' or VARIEDADE == 'Omer':
                        df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_keitt, axis = 1)
                    if VARIEDADE == 'Kent':
                        df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_kent, axis = 1)
                    if VARIEDADE == 'Osteen':
                        df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_osteen, axis = 1)


                    quantidade_total_frutos_controle = df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'].sum()
                    contentores_totais = dataset['CONTENTORES'][0].item()
                    media_frutos = quantidade_total_frutos_controle / contentores_totais
                
                    st.session_state.media_frutos_caixotes =  media_frutos


                elif result_talhao_2:
                        from modulos_dash.balanceamento.funcoes_atualizar_controle.funcoes_else_base_amostragem import * 
                                               
                        st.write('Base do histórico M21 do talhão.')

                        filtro_talhao = df_comportamento_calibres_TALHAO['TALHAO'] == talhao_controle
                        df_comportamento_calibres_TALHAO = df_comportamento_calibres_TALHAO[filtro_talhao] 

                        
                        df_comportamento_calibres_TALHAO_PIV = pd.pivot_table(df_comportamento_calibres_TALHAO, index = ['TALHAO','VALOR_CALIBRE'], values = 'Calibre', aggfunc= np.mean)
                        df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.reset_index()
                        df_comportamento_calibres_TALHAO_PIV.rename(columns = {'Calibre':'Percentual','VALOR_CALIBRE':'Calibre'}, inplace = True)
                        df_comportamento_calibres_TALHAO_PIV['Calibre'] = df_comportamento_calibres_TALHAO_PIV.apply(correcao_calibre_new, axis = 1)
                        df_comportamento_calibres_TALHAO_PIV['Percentual_RECENTE'] = 0
                        df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.drop(columns = ['TALHAO'])


                        df_comportamento_calibres_TALHAO_PIV = correcao_calibre_media_variedade(VARIEDADE,df_comportamento_calibres_TALHAO_PIV)
                        
                        df_graficos_passado  = df_comportamento_calibres_TALHAO_PIV
                        st.session_state.grafico_passado = df_graficos_passado
                        

                        st.session_state.b_ = df_comportamento_calibres_TALHAO_PIV

                        
                        lista_talhoes_quality = pd.unique(df_comportamento_qualidade["TALHAO"]) 
                        lista_talhoes_quality = pd.DataFrame(lista_talhoes_quality)
                        lista_talhoes_quality.rename(columns = {0:'TALHAO'}, inplace = True)
                        
                        result_talhao_3_ = lista_talhoes_quality.TALHAO.isin([talhao_controle]).any().any()

                        if result_talhao_3_:

                            filtro_talhao_quality = df_comportamento_qualidade['TALHAO'] == talhao_controle
                            df_comportamento_qualidade = df_comportamento_qualidade[filtro_talhao_quality] 
                            dataset_quality_piv = pd.pivot_table(df_comportamento_qualidade, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['TALHAO'], aggfunc = np.mean)
                            dataset_quality_piv = dataset_quality_piv.reset_index()
                            
                            dataset_quality_piv = dataset_quality_piv.drop(columns = ['TALHAO'])
                            


                        else:


                            if VARIEDADE == 'Tommy Atkins':
                                VARIEDADE_2 = 'TOMMY'
                            if VARIEDADE == 'Keitt':
                                VARIEDADE_2 = 'KEITT'
                            if VARIEDADE == 'Kent':
                                VARIEDADE_2 = 'KENT'
                            if VARIEDADE == 'Palmer':
                                VARIEDADE_2 = 'PALMER'
                            if VARIEDADE == 'Osteen':
                                VARIEDADE_2 = 'OSTEEN'
                            if VARIEDADE == 'Omer':
                                VARIEDADE_2 = 'OMER'
                            try:
                                filtro_talhao_quality = df_comportamento_qualidade['VARIEDADE'] == VARIEDADE_2
                                df_comportamento_qualidade = df_comportamento_qualidade[filtro_talhao_quality] 
                            except NameError:
                                st.write('#### Variedade faltando no mega, atualize novamente em alguns minutos')
                            

                            dataset_quality_piv = pd.pivot_table(df_comportamento_qualidade, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['VARIEDADE'], aggfunc = np.mean)
                            dataset_quality_piv = dataset_quality_piv.reset_index()
                            dataset_quality_piv = dataset_quality_piv.drop(columns = ['VARIEDADE'])

                            
                        dataset_quality_piv = tratamento_dataset_quality_piv(dataset_quality_piv)

                        dataset_quality_piv['Qualidade'] = dataset_quality_piv.apply(mudanca_nomes_qualidades, axis = 1)
                        dataset_quality_piv['Percent'] = dataset_quality_piv['Percent'] / 100


                        dataset_quality_piv = correcao_qualidade_para_variedade(VARIEDADE,dataset_quality_piv)

                        st.session_state.quality_percent = dataset_quality_piv

                        toneladas_totais_controle = dataset['PESO_CONTROLE'][0].item() * 1000
                        df_media_frutos_caixa = df_comportamento_calibres_TALHAO_PIV
                        df_media_frutos_caixa['Quilos/calibre/controle'] = toneladas_totais_controle * (df_media_frutos_caixa['Percentual']/100)
                        

                        if VARIEDADE == 'Palmer':
                            df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_palmer, axis = 1)
                        if VARIEDADE == 'Tommy Atkins':
                            df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_tommy, axis = 1)
                        if VARIEDADE == 'Keitt' or VARIEDADE == 'Omer':
                            df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_keitt, axis = 1)
                        if VARIEDADE == 'Kent':
                            df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_kent, axis = 1)
                        if VARIEDADE == 'Osteen':
                            df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_osteen, axis = 1)


                        quantidade_total_frutos_controle = df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'].sum()
                        contentores_totais = dataset['CONTENTORES'][0].item()
                        media_frutos = quantidade_total_frutos_controle / contentores_totais
                    
                        st.session_state.media_frutos_caixotes =  media_frutos 


                else:
                        
                        st.write('Base do histórico da variedade')
                        
                        if VARIEDADE == 'Tommy Atkins':
                            VARIEDADE_2 = 'TOMMY'
                        if VARIEDADE == 'Keitt':
                            VARIEDADE_2 = 'KEITT'
                        if VARIEDADE == 'Kent':
                            VARIEDADE_2 = 'KENT'
                        if VARIEDADE == 'Palmer':
                            VARIEDADE_2 = 'PALMER'
                        if VARIEDADE == 'Osteen':
                            VARIEDADE_2 = 'OSTEEN'
                        if VARIEDADE == 'Omer':
                            VARIEDADE_2 = 'OMER'

                        filtro_talhao_quality = df_comportamento_qualidade['VARIEDADE'] == VARIEDADE_2
                        df_comportamento_qualidade = df_comportamento_qualidade[filtro_talhao_quality] 


                        dataset_quality_piv = pd.pivot_table(df_comportamento_qualidade, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['VARIEDADE'], aggfunc = np.mean)
                        

                        def conta_quality_piv(dataset_quality_piv):
                            dataset_quality_piv = dataset_quality_piv.reset_index()
                            dataset_quality_piv = dataset_quality_piv.drop(columns = ['VARIEDADE'])
                            dataset_quality_piv['TOT_PRIMEIRA'] = dataset_quality_piv['TOT_PRIMEIRA'].astype(str)
                            dataset_quality_piv['TOT_SEGUNDA'] = dataset_quality_piv['TOT_SEGUNDA'].astype(str)
                            dataset_quality_piv['TOT_TERCEIRA'] = dataset_quality_piv['TOT_TERCEIRA'].astype(str)
                            dataset_quality_piv['TOT_REFUGO'] = dataset_quality_piv['TOT_REFUGO'].astype(str)
                            dataset_quality_piv = dataset_quality_piv.T
                            dataset_quality_piv = dataset_quality_piv.reset_index()
                            dataset_quality_piv.rename(columns = {'index':'Qualidade',0:'Percent', 1:'Percent', 2:'Percent', 3:'Percent'}, inplace = True)
                            dataset_quality_piv['Percent'] = dataset_quality_piv['Percent'].astype(float)
                            return dataset_quality_piv
                        dataset_quality_piv = conta_quality_piv(dataset_quality_piv)


                        def mudanca_nomes_qualidades(dataset_quality_piv):
                            if dataset_quality_piv['Qualidade'] == 'TOT_PRIMEIRA':
                                return 1
                            elif dataset_quality_piv['Qualidade'] == 'TOT_SEGUNDA':
                                return 2
                            elif dataset_quality_piv['Qualidade'] == 'TOT_TERCEIRA':
                                return 3
                            elif dataset_quality_piv['Qualidade'] == 'TOT_REFUGO':
                                return 4

                        dataset_quality_piv['Qualidade'] = dataset_quality_piv.apply(mudanca_nomes_qualidades, axis = 1)
                        dataset_quality_piv['Percent'] = dataset_quality_piv['Percent'] / 100

                        def correcao_qualidade_faltante_colocando_variedade(VARIEDADE, dataset_quality_piv):
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
                        dataset_quality_piv = correcao_qualidade_faltante_colocando_variedade(VARIEDADE, dataset_quality_piv)

                        st.session_state.quality_percent = dataset_quality_piv

                        filtro_talhao = df_comportamento_calibres_TALHAO['VARIEDADE'] == VARIEDADE_2
                        df_comportamento_calibres_TALHAO = df_comportamento_calibres_TALHAO[filtro_talhao] 
                    
                        df_comportamento_calibres_TALHAO_PIV = pd.pivot_table(df_comportamento_calibres_TALHAO, index = ['VARIEDADE','VALOR_CALIBRE'], values = 'Calibre', aggfunc= np.mean)
                        df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.reset_index()
                        df_comportamento_calibres_TALHAO_PIV.rename(columns = {'Calibre':'Percentual','VALOR_CALIBRE':'Calibre'}, inplace = True)
                        
                        def correcao_calibre_new (df_comportamento_calibres_TALHAO_PIV):
                            if df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_4':
                                return 4
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_5':
                                return 5
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_6':
                                return 6
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_7':
                                return 7
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_8':
                                return 8
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_9':
                                return 9
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_10':
                                return 10
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_12':
                                return 12
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_14':
                                return 14
                            elif df_comportamento_calibres_TALHAO_PIV['Calibre'] == 'CALIBRE_16':
                                return 16

                        df_comportamento_calibres_TALHAO_PIV['Calibre'] = df_comportamento_calibres_TALHAO_PIV.apply(correcao_calibre_new, axis = 1)
                        df_comportamento_calibres_TALHAO_PIV['Percentual_RECENTE'] = 0
                  
                        df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.drop(columns = ['VARIEDADE'])

                        def ajuste_percentuais_variedades(VARIEDADE,df_comportamento_calibres_TALHAO_PIV):
                            if VARIEDADE == 'Tommy Atkins':
                        #### CALIBRE 4
                                result_cal4 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([4]).any().any()
                                if result_cal4:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':4, 'Percentual':0.04}, ignore_index=True)
                        #### CALIBRE 5
                                result_cal5 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([5]).any().any()
                                if result_cal5:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':5, 'Percentual':0.11}, ignore_index=True)
                        #### CALIBRE 6
                                result_cal6 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([6]).any().any()
                                if result_cal6:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':6, 'Percentual':4.18}, ignore_index=True)

                        #### CALIBRE 7
                                result_cal7 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([7]).any().any()
                                if result_cal7:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':7, 'Percentual':9.62}, ignore_index=True)
                        #### CALIBRE 8
                                result_cal8 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([8]).any().any()
                                if result_cal8:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':8, 'Percentual':24.48}, ignore_index=True)
                        #### CALIBRE 9
                                result_cal9 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([9]).any().any()
                                if result_cal9:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':9, 'Percentual':18.52}, ignore_index=True)
                        #### CALIBRE 10
                                result_cal10 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([10]).any().any()
                                if result_cal10:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':10, 'Percentual':27.07}, ignore_index=True)                    
                        #### CALIBRE 12
                                result_cal12 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([12]).any().any()
                                if result_cal12:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':12, 'Percentual':15.50}, ignore_index=True) 
                        #### CALIBRE 14
                                result_cal14 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([14]).any().any()
                                if result_cal14:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':14, 'Percentual':0.53}, ignore_index=True)    
                        #### CALIBRE 16
                                result_cal16 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([16]).any().any()
                                if result_cal16:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':16, 'Percentual':0.09}, ignore_index=True)  
                
                            if VARIEDADE == 'Keitt':
                        #### CALIBRE 4
                                result_cal4 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([4]).any().any()
                                if result_cal4:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
                        #### CALIBRE 5
                                result_cal5 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([5]).any().any()
                                if result_cal5:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':5, 'Percentual':6.91}, ignore_index=True)
                        #### CALIBRE 6
                                result_cal6 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([6]).any().any()
                                if result_cal6:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':6, 'Percentual':22.34}, ignore_index=True)
                        #### CALIBRE 7
                                result_cal7 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([7]).any().any()
                                if result_cal7:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':7, 'Percentual':23.55}, ignore_index=True)
                        #### CALIBRE 8
                                result_cal8 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([8]).any().any()
                                if result_cal8:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':8, 'Percentual':20.83}, ignore_index=True)
                        #### CALIBRE 9
                                result_cal9 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([9]).any().any()
                                if result_cal9:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':9, 'Percentual':8.29}, ignore_index=True)
                        #### CALIBRE 10
                                result_cal10 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([10]).any().any()
                                if result_cal10:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':10, 'Percentual':9.29}, ignore_index=True)                    
                        #### CALIBRE 12
                                result_cal12 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([12]).any().any()
                                if result_cal12:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':12, 'Percentual':7.40}, ignore_index=True) 
                        #### CALIBRE 14
                                result_cal14 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([14]).any().any()
                                if result_cal14:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':14, 'Percentual':0.57}, ignore_index=True)    
                        #### CALIBRE 16
                                result_cal16 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([16]).any().any()
                                if result_cal16:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':16, 'Percentual':0.09}, ignore_index=True)  


                            if VARIEDADE == 'Kent':
                        #### CALIBRE 4
                                result_cal4 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([4]).any().any()
                                if result_cal4:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
                        #### CALIBRE 5
                                result_cal5 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([5]).any().any()
                                if result_cal5:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':5, 'Percentual':4.71}, ignore_index=True)
                        #### CALIBRE 6
                                result_cal6 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([6]).any().any()
                                if result_cal6:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':6, 'Percentual':23.14}, ignore_index=True)
                        #### CALIBRE 7
                                result_cal7 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([7]).any().any()
                                if result_cal7:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':7, 'Percentual':26.28}, ignore_index=True)
                        #### CALIBRE 8
                                result_cal8 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([8]).any().any()
                                if result_cal8:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':8, 'Percentual':20.25}, ignore_index=True)
                        #### CALIBRE 9
                                result_cal9 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([9]).any().any()
                                if result_cal9:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':9, 'Percentual':9.09}, ignore_index=True)
                        #### CALIBRE 10
                                result_cal10 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([10]).any().any()
                                if result_cal10:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':10, 'Percentual':9.36}, ignore_index=True)                    
                        #### CALIBRE 12
                                result_cal12 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([12]).any().any()
                                if result_cal12:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':12, 'Percentual':6.96}, ignore_index=True) 
                        #### CALIBRE 14
                                result_cal14 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([14]).any().any()
                                if result_cal14:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':14, 'Percentual':0.23}, ignore_index=True)    
                        #### CALIBRE 16
                                result_cal16 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([16]).any().any()
                                if result_cal16:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':16, 'Percentual':0.09}, ignore_index=True)  

                            if VARIEDADE =='Palmer':
                        #### CALIBRE 4
                                result_cal4 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([4]).any().any()
                                if result_cal4:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
                        #### CALIBRE 5
                                result_cal5 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([5]).any().any()
                                if result_cal5:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':5, 'Percentual':4.49}, ignore_index=True)
                        #### CALIBRE 6
                                result_cal6 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([6]).any().any()
                                if result_cal6:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':6, 'Percentual':17.28}, ignore_index=True)
                        #### CALIBRE 7
                                result_cal7 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([7]).any().any()
                                if result_cal7:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':7, 'Percentual':17.45}, ignore_index=True)
                        #### CALIBRE 8
                                result_cal8 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([8]).any().any()
                                if result_cal8:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':8, 'Percentual':23.37}, ignore_index=True)
                        #### CALIBRE 9
                                result_cal9 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([9]).any().any()
                                if result_cal9:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':9, 'Percentual':13.22}, ignore_index=True)
                        #### CALIBRE 10
                                result_cal10 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([10]).any().any()
                                if result_cal10:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':10, 'Percentual':15.84}, ignore_index=True)                    
                        #### CALIBRE 12
                                result_cal12 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([12]).any().any()
                                if result_cal12:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':12, 'Percentual':8.10}, ignore_index=True) 
                        #### CALIBRE 14
                                result_cal14 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([14]).any().any()
                                if result_cal14:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':14, 'Percentual':0.25}, ignore_index=True)    
                        #### CALIBRE 16
                                result_cal16 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([16]).any().any()
                                if result_cal16:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':16, 'Percentual':0.00}, ignore_index=True)  

                            if VARIEDADE =='Omer':
                        #### CALIBRE 4
                                result_cal4 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([4]).any().any()
                                if result_cal4:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
                        #### CALIBRE 5
                                result_cal5 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([5]).any().any()
                                if result_cal5:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':5, 'Percentual':0.00}, ignore_index=True)
                        #### CALIBRE 6
                                result_cal6 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([6]).any().any()
                                if result_cal6:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':6, 'Percentual':3.32}, ignore_index=True)
                        #### CALIBRE 7
                                result_cal7 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([7]).any().any()
                                if result_cal7:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':7, 'Percentual':11.03}, ignore_index=True)
                        #### CALIBRE 8
                                result_cal8 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([8]).any().any()
                                if result_cal8:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':8, 'Percentual':29.07}, ignore_index=True)
                        #### CALIBRE 9
                                result_cal9 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([9]).any().any()
                                if result_cal9:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':9, 'Percentual':19.18}, ignore_index=True)
                        #### CALIBRE 10
                                result_cal10 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([10]).any().any()
                                if result_cal10:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':10, 'Percentual':25.83}, ignore_index=True)                    
                        #### CALIBRE 12
                                result_cal12 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([12]).any().any()
                                if result_cal12:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':12, 'Percentual':11.55}, ignore_index=True) 
                        #### CALIBRE 14
                                result_cal14 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([14]).any().any()
                                if result_cal14:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':14, 'Percentual':0.01}, ignore_index=True)    
                        #### CALIBRE 16
                                result_cal16 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([16]).any().any()
                                if result_cal16:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':16, 'Percentual':0.00}, ignore_index=True)  

                            if VARIEDADE =='Osteen':
                        #### CALIBRE 4
                                result_cal4 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([4]).any().any()
                                if result_cal4:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':4, 'Percentual':0.00}, ignore_index=True)
                        #### CALIBRE 5
                                result_cal5 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([5]).any().any()
                                if result_cal5:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':5, 'Percentual':3.47}, ignore_index=True)
                        #### CALIBRE 6
                                result_cal6 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([6]).any().any()
                                if result_cal6:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':6, 'Percentual':17.51}, ignore_index=True)
                        #### CALIBRE 7
                                result_cal7 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([7]).any().any()
                                if result_cal7:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':7, 'Percentual':26.57}, ignore_index=True)
                        #### CALIBRE 8
                                result_cal8 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([8]).any().any()
                                if result_cal8:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':8, 'Percentual':27.12}, ignore_index=True)
                        #### CALIBRE 9
                                result_cal9 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([9]).any().any()
                                if result_cal9:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':9, 'Percentual':11.42}, ignore_index=True)
                        #### CALIBRE 10
                                result_cal10 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([10]).any().any()
                                if result_cal10:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':10, 'Percentual':9.74}, ignore_index=True)                    
                        #### CALIBRE 12
                                result_cal12 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([12]).any().any()
                                if result_cal12:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':12, 'Percentual':4.00}, ignore_index=True) 
                        #### CALIBRE 14
                                result_cal14 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([14]).any().any()
                                if result_cal14:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':14, 'Percentual':0.19}, ignore_index=True)    
                        #### CALIBRE 16
                                result_cal16 = df_comportamento_calibres_TALHAO_PIV.Calibre.isin([16]).any().any()
                                if result_cal16:
                                    print(' ')
                                else:
                                    df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.append({'Calibre':16, 'Percentual':0.00}, ignore_index=True)  
                            return df_comportamento_calibres_TALHAO_PIV
                        df_comportamento_calibres_TALHAO_PIV = ajuste_percentuais_variedades(VARIEDADE,df_comportamento_calibres_TALHAO_PIV)


                        toneladas_totais_controle = dataset['PESO_CONTROLE'][0] * 1000
                        df_media_frutos_caixa = df_comportamento_calibres_TALHAO_PIV
                        df_media_frutos_caixa['Quilos/calibre/controle'] = toneladas_totais_controle * (df_media_frutos_caixa['Percentual']/100)
                        
                        def frutos_controle(df_media_frutos_caixa):
                            if VARIEDADE == 'Palmer':

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

                            if VARIEDADE == 'Tommy Atkins':

                                if df_media_frutos_caixa['Calibre'] == 4:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.1

                                elif df_media_frutos_caixa['Calibre'] == 5:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.940

                                elif df_media_frutos_caixa['Calibre'] == 6:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.760

                                elif df_media_frutos_caixa['Calibre'] == 7:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5985

                                elif df_media_frutos_caixa['Calibre'] == 8:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5185

                                elif df_media_frutos_caixa['Calibre'] == 9:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.461

                                elif df_media_frutos_caixa['Calibre'] == 10:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4065

                                elif df_media_frutos_caixa['Calibre'] == 12:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.3335

                                elif df_media_frutos_caixa['Calibre'] == 14:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2875

                                elif df_media_frutos_caixa['Calibre'] == 16:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2655
                                
                            #################################################### KEITT #####################################################

                            if (VARIEDADE == 'Keitt' or VARIEDADE == 'Omer'):
                                if df_media_frutos_caixa['Calibre'] == 4:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.2

                                elif df_media_frutos_caixa['Calibre'] == 5:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.825
                                    
                                elif df_media_frutos_caixa['Calibre'] == 6:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.676
                                    
                                elif df_media_frutos_caixa['Calibre'] == 7:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.604
                                    
                                elif df_media_frutos_caixa['Calibre'] == 8:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5145
                                    
                                elif df_media_frutos_caixa['Calibre'] == 9:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4575
                                    
                                elif df_media_frutos_caixa['Calibre'] == 10:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.412
                                    
                                elif df_media_frutos_caixa['Calibre'] == 12:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.345
                                    
                                elif df_media_frutos_caixa['Calibre'] == 14:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.292
                                    
                                elif df_media_frutos_caixa['Calibre'] == 16:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.256
                                
                            #################################################### KENT #####################################################
                            if VARIEDADE == 'Kent':

                                if df_media_frutos_caixa['Calibre'] == 4:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.115

                                elif df_media_frutos_caixa['Calibre'] == 5:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.845
                                    
                                elif df_media_frutos_caixa['Calibre'] == 6:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.693
                                    
                                elif df_media_frutos_caixa['Calibre'] == 7:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5855
                                    
                                elif df_media_frutos_caixa['Calibre'] == 8:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.5105
                                    
                                elif df_media_frutos_caixa['Calibre'] == 9:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.460
                                    
                                elif df_media_frutos_caixa['Calibre'] == 10:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4095
                                    
                                elif df_media_frutos_caixa['Calibre'] == 12:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.339
                                    
                                elif df_media_frutos_caixa['Calibre'] == 14:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.286
                                    
                                elif df_media_frutos_caixa['Calibre'] == 16:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2545
                                                       
                            #################################################### OSTEEN #####################################################

                            if VARIEDADE == 'Osteen':

                                if df_media_frutos_caixa['Calibre'] == 4:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 1.243

                                elif df_media_frutos_caixa['Calibre'] == 5:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.882
                                    
                                elif df_media_frutos_caixa['Calibre'] == 6:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.705
                                    
                                elif df_media_frutos_caixa['Calibre'] == 7:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.594
                                    
                                elif df_media_frutos_caixa['Calibre'] == 8:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.516
                                    
                                elif df_media_frutos_caixa['Calibre'] == 9:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4565
                                    
                                elif df_media_frutos_caixa['Calibre'] == 10:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.4045
                                    
                                elif df_media_frutos_caixa['Calibre'] == 12:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.337
                                    
                                elif df_media_frutos_caixa['Calibre'] == 14:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.2855
                                    
                                elif df_media_frutos_caixa['Calibre'] == 16:
                                    return df_media_frutos_caixa['Quilos/calibre/controle'] / 0.249


                        df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle, axis = 1)
                        quantidade_total_frutos_controle = df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'].sum()

                        contentores_totais = dataset['CONTENTORES'][0].item()

                        media_frutos = quantidade_total_frutos_controle / contentores_totais
                    
                        st.session_state.media_frutos_caixotes =  media_frutos 


                        df_graficos_passado  = df_comportamento_calibres_TALHAO_PIV
                        st.session_state.grafico_passado = df_graficos_passado

                        st.session_state.b_ = df_comportamento_calibres_TALHAO_PIV


    with coluna_inicial_2:
        st.write('')
        st.write('')

        if st.button('Atualizar MAF'):
            from modulos_dash.balanceamento.funcoes_atualizar_MAF.modulos_import_func_MAF import *
            

            df_graficos_passado  = st.session_state.grafico_passado
            st.session_state.grafico_passado = df_graficos_passado 


            variaveis_df = importando_data_MAF()
            variaveis_df['VARIEDADE'] = variaveis_df.apply(correcao_, axis = 1)
            variaveis_df['CALIBRE'] = variaveis_df.apply(calibre, axis =1)
            dataset = definindo_dataset(variaveis_df)
            
            try:
                dataset['Calibre'] = dataset['Calibre'].astype(int)
            except TypeError:
                st.write('###### OBS: Base de dados do mega sem variedade ou peso total.')

            
            a = dataset['Calibre'].value_counts() / dataset['Calibre'].count()

            toneladas_totais_controle = dataset['PESO_CONTROLE'][0].item() * 1000

            from urllib.error import HTTPError
            try:
                url_percentual_MAF = 'http://sia:3000/backend/maf/percentuaisCalibre'
                dataset_MAF = pd.read_json(url_percentual_MAF)
                
            except HTTPError :
                st.error('### Erro com a base de dados da MAF !!')

            

            dataset_MAF = ajustes_DATA_MAF(dataset_MAF)
            
     ########################################## REMOVER ACIMA DEPOIS ##########################################


            dataset_MAF['Calibre'] = dataset_MAF.apply(correcao_calibre_MAF, axis = 1)
            
            dataset_MAF['Calibre'] = dataset_MAF['Calibre'].astype(str)

            dataset_MAF['Calibre'] = dataset_MAF.apply(ajuste_final, axis = 1) 
            

            dataset_MAF['Qualidade'] = dataset_MAF.apply(correcao_qualidade_MAF, axis = 1)
            dataset_MAF = dataset_MAF.drop(columns = ['CALIBRE_QUALIDADE'])

            dataset_MAF['VARIEDADE'] = dataset_MAF.apply(correcao_variedade_maf, axis = 1)

            controle = dataset_MAF['CONTROLE_MEGA'][0]
            controle_MEGA = st.session_state.control
            st.session_state.control = controle

            VARIEDADE = dataset_MAF['VARIEDADE'][0]
            st.session_state.variety = VARIEDADE

            somatorio_frutos_peso = som_frutos(dataset_MAF)
        
            somatorio_qualidade = som_frutos_qualid(dataset_MAF)
            somatorio_qualidade = somatorio_qualdidade_replace(somatorio_qualidade)

            somatorio_qualidade['Qualidade'] = somatorio_qualidade.apply(corr_, axis =1)
            somatorio_qualidade['Qualidade'] = somatorio_qualidade['Qualidade'].astype(int)
            somatorio_qualidade = somatorio_qualidade.dropna()

            st.session_state.quality_percent = somatorio_qualidade

        
            somatorio_frutos_peso = somatorio_ajuste_calibres_correcao(somatorio_frutos_peso)
            

            df_media_frutos_caixa = somatorio_frutos_peso
            df_media_frutos_caixa['Quilos/calibre/controle'] = toneladas_totais_controle * (df_media_frutos_caixa['Percentual']/100)

            if VARIEDADE == 'Keitt' or VARIEDADE == 'Omer':
                df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_keitt, axis = 1)

            if VARIEDADE == 'Palmer':
                df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_palmer, axis = 1)

            if VARIEDADE == 'Tommy Atkins':
                df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_tommy, axis = 1)

            if VARIEDADE == 'Osteen':
                df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_osteen, axis = 1)
            
            if VARIEDADE == 'Kent':
                df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'] = df_media_frutos_caixa.apply(frutos_controle_kent, axis = 1)

            quantidade_total_frutos_controle = df_media_frutos_caixa['FRUTOS_CALIBRE_CONTROLE'].sum()
            contentores_totais = dataset['CONTENTORES'][0].item()
            media_frutos = quantidade_total_frutos_controle / contentores_totais
            
            st.session_state.media_frutos_caixotes =  media_frutos 
            
            filtro_ref = somatorio_frutos_peso['Calibre'] != 'Refugo'
            somatorio_frutos_peso = somatorio_frutos_peso[filtro_ref]



########## NEW LINES 

            filtro_ref = somatorio_frutos_peso['Calibre'] != 'nan'
            somatorio_frutos_peso = somatorio_frutos_peso[filtro_ref]

            somatorio_frutos_peso['Calibre'] = somatorio_frutos_peso['Calibre'].astype(float)
            somatorio_frutos_peso=somatorio_frutos_peso.dropna(subset=['PESO_KG'])
            somatorio_frutos_peso['Calibre'] = somatorio_frutos_peso['Calibre'].astype(int)

            somatorio_frutos_peso_para_b = somatorio_frutos_peso.drop(columns = ['PESO_KG','QTD_FRUTOS'])

            b = somatorio_frutos_peso_para_b
            b = b.sort_values('Calibre')
            
            st.session_state.b_ = b
            st.session_state.anterior = dataset

            df_embaladeiras_ativas = criando_embaladeiras_ativas()
            
            if len(df_embaladeiras_ativas) == 0:
                url_embaladeiras_ativas = 'http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_EMB_ATIVAS'
                df_embaladeiras_ativas = pd.read_json(url_embaladeiras_ativas)

            df_embaladeiras_ativas.rename(columns = {'CPF':'MATRICULA','PESSOA':'NOME'}, inplace = True)
            df_embaladeiras_ativas['NOME'] = df_embaladeiras_ativas['NOME'].str[6:]

            st.session_state.url_embala = df_embaladeiras_ativas

            results = [
                int((parse(c) - parse(o)).total_seconds())
                for c, o in zip(dataset_MAF['HORA_ULTIMA_ATUALIZACAO'], dataset_MAF['HORA_ATUALIZACAO'])
                if parse(c) - parse(o) < datetime.timedelta(seconds=1)]

            st.session_state_tempo = results[1]

            tempo_passado_minutos = results[1] * -1 / 60
            tempo_passado_horas = tempo_passado_minutos / 60
            toneladas_passadas = dataset_MAF['PESO_KG_RECENTE'].sum() / 1000

            st.session_state_tempo = tempo_passado_minutos

            produtividade_atual = round(toneladas_passadas / tempo_passado_horas,2)

            st.session_state.prod_MAF = produtividade_atual

            
            somatorio_frutos_peso['CAIXAS'] = somatorio_frutos_peso.apply(caixas_maf, axis = 1)
            caixas_total_processadas = somatorio_frutos_peso['CAIXAS'].sum()

            somatorio_frutos_peso['CAIXAS_RECENTE'] = somatorio_frutos_peso.apply(caixas_maf_recente, axis = 1)
            caixas_recentes_processadas = somatorio_frutos_peso['CAIXAS_RECENTE'].sum()

            st.session_state.cxs_recentes = caixas_recentes_processadas
            st.session_state.cxs_process = caixas_total_processadas

            hora_ultima_atualização = dataset_MAF['HORA_ULTIMA_ATUALIZACAO'][0]
            st.write('Horário da última atualização:', hora_ultima_atualização)
            st.write(f'Controle na base de histórico: {controle_MEGA}')


    try:
        b = st.session_state.b_ 
        dataset = st.session_state.anterior
        quality = st.session_state.quality_percent
        produtividade_atual = st.session_state.prod_MAF
        controle = st.session_state.control 
        VARIEDADE = st.session_state.variety

    except AttributeError:
        st.info('##### Clique em "Atualizar Controle" para verificar se existe amostragem para o controle atual !')
        dataset.rename(columns = {"PESO":"Peso","CALIBRE":"Calibre","NUMERO_FRUTO":"Fruto","QUALIDADE":"Qualidade"}, inplace = True)

    try:
        avg_frutos_caixotes = st.session_state.media_frutos_caixotes
        
    except ValueError:
        st.error('Erro com link do mega, possíveis motivos:')
        st.write('1 - Amostragem de calibres não lançada/feita para o controle')
        st.write('2 - Base do mega indisponível')
        st.write('3 - Erro de digitação nos campos da base de dados')
        
        st.error('###### Para verificar as opções acima clique nos links a seguir e verifique se um dos links carrega a base de dados sem erros ou valores faltantes')
        st.info('http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH')
        st.info('http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH')

    Caixotes = dataset['CONTENTORES'][0].item()
    
    dataset = dataset 
    from modulos_dash.balanceamento.funcoes_menu.modulos_import_func_menu import *

    b = correcao_calibres_de_b(b)
    percentual_de_4,percentual_de_5,percentual_de_6,percentual_de_7,percentual_de_8,percentual_de_9,percentual_de_10,percentual_de_12,percentual_de_14,percentual_de_16 = definindo_percentuais(b)

    quality = correcao_quality(quality)

    
    primeira_percent,segunda_percent,terceira_percent,refugo_percent = definindo_percentuais_quality(quality)

    st.session_state_base_crua = b
    dataset_2 = dataset 


    produtividade_embaladeira, produtividade_talo, produtividade_limpeza, produtividade_limpeza2 = atribuindo_constantes_iniciais()

    caixotes = Caixotes
    variedade = VARIEDADE 

    ############ BASE DE ESTUDO DAS EMBALADEIRAS E DAS ATIVAS NO DIA ##############################

    padrao_embaldeiras_total = pd.read_excel('padrao_embaladeiras_TUDO_cenarios.xlsx')
    df_embaladeiras_ativas = st.session_state.url_embala

    df_222 = df_embaladeiras_ativas.merge(padrao_embaldeiras_total)
    padrao_embaldeiras = df_222
    embaladeira = len(padrao_embaldeiras.groupby('PESSOA'))

    Programa_input = 'Safra'
    st.session_state.emba_aviso = embaladeira

    coluna1, coluna2 = st.columns(2)

    
    with coluna1:
        from PIL import Image
        img = Image.open('agrodn.png')
        newsize = (380,110)
        img2 = img.resize(newsize)

        ########## JANELA LATERAL ##########

        st.sidebar.image(img2, use_column_width=True)
        st.sidebar.title('Menu')
        st.sidebar.markdown('Escolha a informação para visualizar:')


    pagina_selecionada = st.sidebar.radio('', ['Balanceamento e produtividade','Linhas de embalagem','Distribuição embaladeiras'])

    if pagina_selecionada == 'Balanceamento e produtividade':
        

        colunA, colunB, colunC, colunD = st.columns([0.3,0.3,0.5,1])


        st.session_state.controle = controle

        controle2 = st.session_state.controle
        colunA.metric(label="Controle", value= controle2, delta= VARIEDADE)
        colunC.metric(label="MAF (t/h)", value= produtividade_atual) 

        tempo_2 = st.session_state_tempo
        colunB.metric(label="Intervalo de tempo (min)", value= round(tempo_2,2))

        col2, col3 = st.columns([0.30,1])
        
        emba_aviso = st.session_state.emba_aviso


        st.success('### Ajuste dos percentuais de distribuição')
        coluna_0, coluna_11, coluna_22, coluna_33, coluna_44, coluna_55, coluna_66, coluna_77, coluna_88, coluna_99, coluna_00 = st.columns([0.01,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5])

        
        coluna_11.info('###### Calibre 4')
        percent_caliber_4 = coluna_11.text_input(label = '', value = round(percentual_de_4,2))
        coluna_22.info('###### Calibre 5')
        percent_caliber_5 = coluna_22.text_input(label = ' ', value = round(percentual_de_5,2))
        coluna_33.info('###### Calibre 6')
        percent_caliber_6 = coluna_33.text_input(label = '  ', value = round(percentual_de_6,2))
        coluna_44.info('###### Calibre 7')
        percent_caliber_7 = coluna_44.text_input(label = '   ', value = round(percentual_de_7,2))
        coluna_55.info('###### Calibre 8')
        percent_caliber_8 = coluna_55.text_input(label = '    ', value = round(percentual_de_8,2))
        coluna_66.info('###### Calibre 9')
        percent_caliber_9 = coluna_66.text_input(label = '     ', value = round(percentual_de_9,2))
        coluna_77.info('###### Calibre 10')
        percent_caliber_10 = coluna_77.text_input(label = '      ', value = round(percentual_de_10,2))
        coluna_88.info('###### Calibre 12')
        percent_caliber_12 = coluna_88.text_input(label = '       ', value = round(percentual_de_12,2))
        coluna_99.info('###### Calibre 14')
        percent_caliber_14 = coluna_99.text_input(label = '         ', value = round(percentual_de_14,2))
        coluna_00.info('###### Calibre 16')
        percent_caliber_16 = coluna_00.text_input(label = '           ', value = round(percentual_de_16,2))


        percent_caliber_4 = float(percent_caliber_4)
        percent_caliber_5 = float(percent_caliber_5)
        percent_caliber_6 = float(percent_caliber_6)
        percent_caliber_7 = float(percent_caliber_7)
        percent_caliber_8 = float(percent_caliber_8)
        percent_caliber_9 = float(percent_caliber_9)
        percent_caliber_10 = float(percent_caliber_10)
        percent_caliber_12 = float(percent_caliber_12)
        percent_caliber_14 = float(percent_caliber_14)
        percent_caliber_16 = float(percent_caliber_16)



        st.session_state_percent_4 = percent_caliber_4 
        st.session_state_percent_5 = percent_caliber_5
        st.session_state_percent_6 = percent_caliber_6 
        st.session_state_percent_7 = percent_caliber_7 
        st.session_state_percent_8 = percent_caliber_8 
        st.session_state_percent_9 = percent_caliber_9 
        st.session_state_percent_10 = percent_caliber_10 
        st.session_state_percent_12 = percent_caliber_12
        st.session_state_percent_14 = percent_caliber_14 
        st.session_state_percent_16 = percent_caliber_16
        st.write('')

        from modulos_dash.balanceamento.funcoes_pagina_balanceamento.modulos_import_balance import *
        

        def ajuste(b):
            if b['Calibre'] == 4:
                return percent_caliber_4
            elif b['Calibre'] == 5:
                return percent_caliber_5
            elif b['Calibre'] == 6:
                return percent_caliber_6
            elif b['Calibre'] == 7:
                return percent_caliber_7
            elif b['Calibre'] == 8:
                return percent_caliber_8
            elif b['Calibre'] == 9:
                return percent_caliber_9
            elif b['Calibre'] == 10:
                return percent_caliber_10
            elif b['Calibre'] == 12:
                return percent_caliber_12
            elif b['Calibre'] == 14:
                return percent_caliber_14
            elif b['Calibre'] == 16:
                return percent_caliber_16

        b['Percentual'] = b.apply(ajuste, axis = 1)

        st.success('### Balanceamento')

        with st.form(key='planilha'):
            
            coluna1_1, coluna2_2,coluna3_3, coluna4_4 = st.columns([0.4,0.09,0.66,1])
            
            embaladeira_input = coluna1_1.number_input(label = 'Ajuste a quantidade de embaladeiras:', value = emba_aviso  , format = "%d", step = 1)
            Programa_input_2 = coluna1_1.selectbox('Selecione o período:', ['Safra','Entre Safra'])
            produtividade_embaladeira_input = coluna1_1.slider('Produtividade Embaladeiras', min_value = 0.1, max_value = 0.99, value = 0.75, step = 0.01)
            produtividade_talo_input = coluna1_1.slider('Produtividade Corte de Talo', min_value = 0.1, max_value = 0.99, value = 0.80, step = 0.01)
            produtividade_limpeza_input = coluna1_1.slider('Produtividade da Limpeza', min_value = 0.1, max_value = 0.99, value = 0.75, step = 0.01)
            produtividade_limpeza2_input = coluna1_1.slider('Produtividade da Seleção', min_value = 0.1, max_value = 0.99, value = 0.75, step = 0.01) 

            st.success('### Embalagem - (Com ou Sem Papel):')

            colun0, colun, colun2, colun3, colun4, colun5,colun6,colun7,colun8,colun9,colun00 = st.columns([0.02,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5])

            if variedade == 'Keitt' or variedade == 'Omer':

                colun.info('###### Calibre 4')
                calibre_4_papel = colun.selectbox(label = '', options = ('Sem','Com'))
                colun2.info('###### Calibre 5')
                calibre_5_papel = colun2.selectbox(label = ' ', options = ('Sem','Com'))
                colun3.info('###### Calibre 6')
                calibre_6_papel = colun3.selectbox(label = '  ', options = ('Sem','Com'))
                colun4.info('###### Calibre 7')
                calibre_7_papel = colun4.selectbox(label = '   ', options = ('Sem','Com'))
                colun5.info('###### Calibre 8')
                calibre_8_papel = colun5.selectbox(label = '    ', options = ('Sem','Com'))
                colun6.info('###### Calibre 9')
                calibre_9_papel = colun6.selectbox(label = '     ', options = ('Sem','Com'))
                colun7.info('###### Calibre 10')
                calibre_10_papel = colun7.selectbox(label = '      ', options = ('Sem','Com'))
                colun8.info('###### Calibre 12')
                calibre_12_papel = colun8.selectbox(label = '       ', options = ('Sem','Com'))
                colun9.info('###### Calibre 14')
                calibre_14_papel = colun9.selectbox(label = '        ', options = ('Sem','Com'))
                colun00.info('###### Calibre 16')
                calibre_16_papel = colun00.selectbox(label = '           ', options = ('Sem','Com'))

            if variedade == 'Kent' or variedade == 'Osteen':

                colun.info('###### Calibre 4')
                calibre_4_papel = colun.selectbox(label = '', options = ('Sem','Com'))
                colun2.info('###### Calibre 5')
                calibre_5_papel = colun2.selectbox(label = ' ', options = ('Sem','Com'))
                colun3.info('###### Calibre 6')
                calibre_6_papel = colun3.selectbox(label = '  ', options = ('Sem','Com'))
                colun4.info('###### Calibre 7')
                calibre_7_papel = colun4.selectbox(label = '   ', options = ('Sem','Com'))
                colun5.info('###### Calibre 8')
                calibre_8_papel = colun5.selectbox(label = '    ', options = ('Sem','Com'))
                colun6.info('###### Calibre 9')
                calibre_9_papel = colun6.selectbox(label = '     ', options = ('Sem','Com'))
                colun7.info('###### Calibre 10')
                calibre_10_papel = colun7.selectbox(label = '      ', options = ('Sem','Com'))
                colun8.info('###### Calibre 12')
                calibre_12_papel = colun8.selectbox(label = '       ', options = ('Sem','Com'))
                colun9.info('###### Calibre 14')
                calibre_14_papel = colun9.selectbox(label = '        ', options = ('Sem','Com'))
                colun00.info('###### Calibre 16')
                calibre_16_papel = colun00.selectbox(label = '           ', options = ('Sem','Com'))
            
            if variedade == 'Palmer':

                colun.info('###### Calibre 4')
                calibre_4_papel = colun.selectbox(label = '', options = ('Com','Sem'))
                colun2.info('###### Calibre 5')
                calibre_5_papel = colun2.selectbox(label = ' ', options = ('Com','Sem'))
                colun3.info('###### Calibre 6')
                calibre_6_papel = colun3.selectbox(label = '  ', options = ('Com','Sem'))
                colun4.info('###### Calibre 7')
                calibre_7_papel = colun4.selectbox(label = '   ', options = ('Com','Sem'))
                colun5.info('###### Calibre 8')
                calibre_8_papel = colun5.selectbox(label = '    ', options = ('Com','Sem'))
                colun6.info('###### Calibre 9')
                calibre_9_papel = colun6.selectbox(label = '     ', options = ('Com','Sem'))
                colun7.info('###### Calibre 10')
                calibre_10_papel = colun7.selectbox(label = '      ', options = ('Com','Sem'))
                colun8.info('###### Calibre 12')
                calibre_12_papel = colun8.selectbox(label = '       ', options = ('Com','Sem'))
                colun9.info('###### Calibre 14')
                calibre_14_papel = colun9.selectbox(label = '        ', options = ('Com','Sem'))
                colun00.info('###### Calibre 16')
                calibre_16_papel = colun00.selectbox(label = '           ', options = ('Com','Sem'))

            if variedade == 'Tommy Atkins':

                colun.info('###### Calibre 4')
                calibre_4_papel = colun.selectbox(label = '', options = ('Com','Sem'))
                colun2.info('###### Calibre 5')
                calibre_5_papel = colun2.selectbox(label = ' ', options = ('Com','Sem'))
                colun3.info('###### Calibre 6')
                calibre_6_papel = colun3.selectbox(label = '  ', options = ('Com','Sem'))
                colun4.info('###### Calibre 7')
                calibre_7_papel = colun4.selectbox(label = '   ', options = ('Com','Sem'))
                colun5.info('###### Calibre 8')
                calibre_8_papel = colun5.selectbox(label = '    ', options = ('Com','Sem'))
                colun6.info('###### Calibre 9')
                calibre_9_papel = colun6.selectbox(label = '     ', options = ('Com','Sem'))
                colun7.info('###### Calibre 10')
                calibre_10_papel = colun7.selectbox(label = '      ', options = ('Com','Sem'))
                colun8.info('###### Calibre 12')
                calibre_12_papel = colun8.selectbox(label = '       ', options = ('Com','Sem'))
                colun9.info('###### Calibre 14')
                calibre_14_papel = colun9.selectbox(label = '        ', options = ('Com','Sem'))
                colun00.info('###### Calibre 16')
                calibre_16_papel = colun00.selectbox(label = '           ', options = ('Com','Sem'))


            button_submit = coluna1_1.form_submit_button('Calcular')

        if button_submit:
            embaladeira =  embaladeira_input
            Programa_input = Programa_input_2
            produtividade_embaladeira = produtividade_embaladeira_input
            produtividade_talo= produtividade_talo_input 
            produtividade_limpeza = produtividade_limpeza_input
            produtividade_limpeza2 = produtividade_limpeza2_input


        def ritmo(b):

                if variedade == 'Palmer':

                    if (b['Calibre'] == 5 ) and (calibre_4_papel == 'Com' ):
                        return 229
                    elif (b['Calibre'] == 4) and (calibre_5_papel == 'Com'):
                        return 229
                    elif (b['Calibre'] == 6) and (calibre_6_papel == 'Com'):
                        return 169
                    elif (b['Calibre'] == 7) and (calibre_7_papel == 'Com'):
                        return 174
                    elif (b['Calibre'] == 8) and (calibre_8_papel == 'Com'):
                        return 191
                    elif (b['Calibre'] == 9) and (calibre_9_papel == 'Com'):
                        return 157
                    elif (b['Calibre'] == 10) and (calibre_10_papel == 'Com'):
                        return 139
                    elif (b['Calibre'] == 12) and (calibre_12_papel == 'Com'):
                        return 149
                    elif (b['Calibre'] == 14) and (calibre_14_papel == 'Com'):
                        return 85


    ############################################### PALMER SEM PAPEL #######################################################

                    elif (b['Calibre'] == 5) and ( calibre_4_papel == 'Sem'):
                        return 517
                    elif (b['Calibre'] == 4) and (calibre_5_papel == 'Sem'):
                        return 517
                    elif (b['Calibre'] == 6) and ( calibre_6_papel == 'Sem'):
                        return 412
                    elif (b['Calibre'] == 7) and (calibre_7_papel == 'Sem'):
                        return 321
                    elif (b['Calibre'] == 8) and (calibre_8_papel == 'Sem'):
                        return 301
                    elif (b['Calibre'] == 9) and (calibre_9_papel == 'Sem'):
                        return 257
                    elif (b['Calibre'] == 10) and (calibre_10_papel == 'Sem'):
                        return 261
                    elif (b['Calibre'] == 12) and ( calibre_12_papel == 'Sem'):
                        return 253
                    elif (b['Calibre'] == 14) and (calibre_14_papel == 'Sem'):
                        return 220
                
                if (variedade == 'Keitt' or variedade == 'Omer'):
                    if (b['Calibre'] == 5 and calibre_5_papel == 'Sem'):
                        return 517
                    elif (b['Calibre'] == 4  and calibre_4_papel == 'Sem'):
                        return 517
                    elif (b['Calibre'] == 6 and calibre_6_papel == 'Sem'):
                        return 412
                    elif (b['Calibre'] == 7 and calibre_7_papel == 'Sem'):
                        return 321
                    elif (b['Calibre'] == 8  and calibre_8_papel == 'Sem'):
                        return 301
                    elif (b['Calibre'] == 9 and calibre_9_papel == 'Sem'):
                        return 257
                    elif (b['Calibre'] == 10  and calibre_10_papel == 'Sem'):
                        return 261
                    elif (b['Calibre'] == 12 and calibre_12_papel == 'Sem') :
                        return 253
                    elif (b['Calibre'] == 14  and calibre_14_papel == 'Sem') :
                        return 220
                    elif (b['Calibre'] == 16  and calibre_16_papel == 'Sem') :
                        return 200
                    
                    elif (b['Calibre'] == 5 and calibre_5_papel == 'Com'):
                        return 235
                    elif (b['Calibre'] == 4 and calibre_4_papel == 'Com'):
                        return 235
                    elif (b['Calibre'] == 6  and calibre_6_papel == 'Com'):
                        return 178
                    elif (b['Calibre'] == 7 and calibre_7_papel == 'Com'):
                        return 185
                    elif (b['Calibre'] == 8 and calibre_8_papel == 'Com'):
                        return 195
                    elif (b['Calibre'] == 9  and calibre_9_papel == 'Com'):
                        return 154
                    elif (b['Calibre'] == 10 and calibre_10_papel == 'Com'):
                        return 144
                    elif (b['Calibre'] == 12 and calibre_12_papel == 'Com'):
                        return 158
                    elif (b['Calibre'] == 14 and calibre_14_papel == 'Com'):
                        return 90
                    elif (b['Calibre'] == 16 and calibre_16_papel == 'Com'):
                        return 80

                if variedade == 'Kent':

                    if (b['Calibre'] == 5) and (calibre_5_papel == 'Sem'):
                        return 510
                    elif (b['Calibre'] == 6) and (calibre_6_papel == 'Sem'):
                        return 410
                    elif (b['Calibre'] == 7) and (calibre_7_papel == 'Sem'):
                        return 314
                    elif (b['Calibre'] == 8) and (calibre_8_papel == 'Sem'):
                        return 300
                    elif (b['Calibre'] == 9) and (calibre_9_papel == 'Sem'):
                        return 253
                    elif (b['Calibre'] == 10) and (calibre_10_papel == 'Sem'):
                        return 248
                    elif (b['Calibre'] == 12) and (calibre_12_papel == 'Sem'):
                        return 246
                    elif (b['Calibre'] == 14) and (calibre_14_papel == 'Sem'):
                        return 200
                    elif (b['Calibre'] == 16) and (calibre_16_papel == 'Sem'):
                        return 180

                    elif (b['Calibre'] == 5) and (calibre_5_papel == 'Com'):
                        return 235
                    elif (b['Calibre'] == 6) and (calibre_6_papel == 'Com'):
                        return 178
                    elif (b['Calibre'] == 7) and (calibre_7_papel == 'Com'):
                        return 185
                    elif (b['Calibre'] == 8) and (calibre_8_papel == 'Com'):
                        return 195
                    elif (b['Calibre'] == 9) and (calibre_9_papel == 'Com'):
                        return 154
                    elif (b['Calibre'] == 10) and (calibre_10_papel == 'Com'):
                        return 144
                    elif (b['Calibre'] == 12) and (calibre_12_papel == 'Com'):
                        return 158
                    elif (b['Calibre'] == 14) and (calibre_14_papel == 'Com'):
                        return 90
                    elif (b['Calibre'] == 16) and (calibre_16_papel == 'Com'):
                        return 80

                if (variedade == 'Tommy Atkins' or variedade == 'Osteen'):

                    if (b['Calibre'] == 5) and (calibre_5_papel == 'Com'):
                        return 235
                    elif (b['Calibre'] == 6) and (calibre_6_papel == 'Com'):
                        return 178
                    elif (b['Calibre'] == 7) and (calibre_7_papel == 'Com'):
                        return 185
                    elif (b['Calibre'] == 8) and (calibre_8_papel == 'Com'):
                        return 195
                    elif (b['Calibre'] == 9) and (calibre_9_papel == 'Com'):
                        return 154
                    elif (b['Calibre'] == 10) and (calibre_10_papel == 'Com'):
                        return 144
                    elif (b['Calibre'] == 12) and (calibre_12_papel == 'Com'):
                        return 158
                    elif (b['Calibre'] == 14) and (calibre_14_papel == 'Com'):
                        return 90

            ################################################## Tommy SEM PAPEL ############################################################# 

                    elif (b['Calibre'] == 5) and (calibre_5_papel == 'Sem'):
                        return 517
                    elif (b['Calibre'] == 6) and (calibre_6_papel == 'Sem'):
                        return 412
                    elif (b['Calibre'] == 7) and ( calibre_7_papel == 'Sem'):
                        return 321
                    elif (b['Calibre'] == 8) and ( calibre_8_papel == 'Sem'):
                        return 301
                    elif (b['Calibre'] == 9) and (calibre_9_papel == 'Sem'):
                        return 257
                    elif (b['Calibre'] == 10) and (calibre_10_papel == 'Sem'):
                        return 261
                    elif (b['Calibre'] == 12) and (calibre_12_papel == 'Sem'):
                        return 253
                    elif (b['Calibre'] == 14) and (calibre_14_papel == 'Sem'):
                        return 220

                else:
                    return 'NADA'
        
        b['Ritmo'] = b.apply(ritmo, axis = 1)


        filtro_ritmo = b['Ritmo'] != 'NADA'
        b = b[filtro_ritmo]

        col1, col2,col3,col4 = st.columns([0.1,0.01,1,1.2])

        b = contas_caixas_e_horas(b,caixotes, avg_frutos_caixotes,primeira_percent,segunda_percent,terceira_percent, produtividade_embaladeira)
        
        st.session_state.caixotes = caixotes
        st.session_state.embaladeira = embaladeira
        st.session_state.variedade = variedade
        st.session_state.periodo_safra = Programa_input 
        st.session_state.produtividade_embaladeira = produtividade_embaladeira
        st.session_state.produtividade_talo = produtividade_talo
        st.session_state.produtividade_limpeza = produtividade_limpeza
        st.session_state.produtividade_selecao = produtividade_limpeza2

        st.session_state.calibre4 = calibre_4_papel
        st.session_state.calibre5 = calibre_5_papel
        st.session_state.calibre6 = calibre_6_papel
        st.session_state.calibre7 = calibre_7_papel
        st.session_state.calibre8 = calibre_8_papel
        st.session_state.calibre9 = calibre_9_papel
        st.session_state.calibre10 = calibre_10_papel
        st.session_state.calibre12 = calibre_12_papel
        st.session_state.calibre14 = calibre_14_papel
        st.session_state.calibre16 = calibre_16_papel
        
        ritmo_embaladeira, corte_talo, ritmo_talo, diferenca_aceitavel, corte_talo2, ritmo_talo_2 = contas_balanceamento(b, embaladeira, caixotes, avg_frutos_caixotes, produtividade_talo)

        def equilibrio(corte_talo, embaladeira):
        
                corte_talo3, selecao__3, Limpeza_selecao_2, caixotes_hora_2, ton_horas_2, caixotes_hora, ton_horas = contas_dentro_da_def_equilibrio(caixotes,ritmo_talo_2,avg_frutos_caixotes, produtividade_limpeza,b,embaladeira,segunda_percent,terceira_percent,refugo_percent,produtividade_limpeza2,primeira_percent,corte_talo2)

                st.info('#### Quantidade de pessoas: ')
                st.write('#### Corte de talo: ', corte_talo3)
                st.write('#### Seleção: ',selecao__3)
                st.write('#### Limpeza: ', Limpeza_selecao_2 )
                st.markdown('       ')
                st.markdown('       ')
                st.info('#### Capacidade:' )
                st.write('#### Talo: ', ' ',caixotes_hora_2, 'Caixotes/Hora')
                st.write('#### Embalagem: ', ' ',ton_horas_2, 'Toneladas/Hora')
                        
                st.session_state.caixotes_hora = caixotes_hora
                st.session_state.ton_horas = ton_horas

        with coluna4_4:
                    
                    st.info('#### Distribuição de calibres:')
                    import plotly.graph_objects as go
                    import plotly.express as px
                    #b
                    dataset_33 = st.session_state_base_crua

                    def ajuste(dataset_33):
                            if dataset_33['Calibre'] == 4:
                                return percent_caliber_4
                            elif dataset_33['Calibre'] == 5:
                                return percent_caliber_5
                            elif dataset_33['Calibre'] == 6:
                                return percent_caliber_6
                            elif dataset_33['Calibre'] == 7:
                                return percent_caliber_7
                            elif dataset_33['Calibre'] == 8:
                                return percent_caliber_8
                            elif dataset_33['Calibre'] == 9:
                                return percent_caliber_9
                            elif dataset_33['Calibre'] == 10:
                                return percent_caliber_10
                            elif dataset_33['Calibre'] == 12:
                                return percent_caliber_12
                            elif dataset_33['Calibre'] == 14:
                                return percent_caliber_14
                            elif dataset_33['Calibre'] == 16:
                                return percent_caliber_16
                    dataset_33['Percentual'] = dataset_33.apply(ajuste, axis = 1)

                    dataset_33, c = criando_c_and_dt33(dataset_33)
                    

                    def rename(dataset_33):
                        if dataset_33['Calibre Name'] == '0':
                            return 'Pequeno'
                        elif dataset_33['Calibre Name'] == '100':
                            return 'Grande'
                        else:
                            return dataset_33['Calibre Name']
                    dataset_33['Calibre Name'] = dataset_33.apply(rename, axis = 1) 
                    d = round(dataset_33['Percentual_RECENTE'],2)

                    fig = go.Figure()

                    dataset_33['Calibre Name'] = dataset_33['Calibre Name'].astype(str)
                    dataset_33['Calibre Name'] = dataset_33['Calibre Name'].str.split('.').str[0]


                    fig.add_trace(go.Bar(x = dataset_33['Calibre Name'],y = dataset_33['Percentual'], text = c, name = 'Processado'))
                    fig.add_trace(go.Bar(x = dataset_33['Calibre Name'],y = dataset_33['Percentual_RECENTE'], text = d, name = 'Recente'))


                    df_comportamento_calibres_TALHAO_PIV = st.session_state.grafico_passado 
                    df_comportamento_calibres_TALHAO_PIV.sort_values(['Calibre'])
                    
                    e = round(df_comportamento_calibres_TALHAO_PIV['Percentual'],2)
                    
                    fig.add_trace(go.Bar(x = df_comportamento_calibres_TALHAO_PIV['Calibre'],y = df_comportamento_calibres_TALHAO_PIV['Percentual'], name = 'Histórico', text = e,
                    ))

                    fig.update_traces(textposition="outside",textfont_size=14, cliponaxis=False,textangle=0, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    fig.update_layout(height = 550, width = 900,uniformtext_minsize=10)
                                     
                    st.plotly_chart(fig) 

        with coluna3_3:      

                    equilibrio(corte_talo, embaladeira)

                    ton_horas = st.session_state.ton_horas

                    diference = str(round(((ton_horas - produtividade_atual)*100) / produtividade_atual ,2)) + ' ' + '%'
                    colunD.metric(label="Embaladeiras (t/h)", value = ton_horas, delta = diference) 

                    
                    caixas_total_controle = b['Caixas_total'].sum()
                    caixas_total_processadas = st.session_state.cxs_process
                    cxs_recente_process = st.session_state.cxs_recentes 

            
                    caixas_restantes = caixas_total_controle - caixas_total_processadas
                    caixotes_hora_time = st.session_state.caixotes_hora 

                    mins = round(caixas_restantes * tempo_2 / cxs_recente_process )

                    caixas_total_processadas = round(caixas_total_processadas,2)
                    caixas_restantes = round(caixas_restantes,2)
                    mins = round(mins,2)

                    st.session_state.caixas_processadas = caixas_total_processadas
                    st.session_state.caixas_restantes = caixas_restantes
                    st.session_state.mins = mins
                    
            
        with coluna2_2:
            st.write(" ")
            st.session_state.b = b
        

    elif pagina_selecionada == 'Linhas de embalagem':
        

        caixas_total_processadas = st.session_state.caixas_processadas
        caixas_restantes = st.session_state.caixas_restantes
        mins = st.session_state.mins

        caixotes_hora = st.session_state.caixotes_hora
        controle2 = st.session_state.controle
        ton_horas = st.session_state.ton_horas

    ######################## EXIBINDO MÉTRICAS CALCULADAS NA ABA ANTERIOR ########################

        col1, col2, col3, col4,col5,col6 = st.columns([0.5,1,1,1,1,1])
        col1.write("")
        col2.metric(label="Controle", value= controle2, delta= VARIEDADE)
        col6.metric(label="Caixotes/Hora", value= caixotes_hora, delta= None)
        
        col4.metric(label="MAF (t/h)", value= produtividade_atual) 

        diference = str(round(((ton_horas - produtividade_atual)*100) / produtividade_atual ,2)) + ' ' + '%'
        col5.metric(label="Embaladeiras (t/h)", value = ton_horas, delta = diference)


        tempo_2 = st.session_state_tempo
        col3.metric(label="Intervalo de tempo (min)", value= round(tempo_2,2))
    ###################### DIVISÃO DA TELA EM LINHAS E COLUNAS DE COLUNAS ######################

        col11,col22, col33 = st.columns([0.3,0.4,0.4])
        coluna1, coluna2 = st.columns(2)
    #    col1, col2 = st.columns([0.01,1])

    ###################### TRAZENDO VALORES DAS VARIAVEIS DA ABA ANTERIOR ######################

        Programa_input = st.session_state.periodo_safra
        caixotes = st.session_state.caixotes 
        embaladeira = st.session_state.embaladeira 
        variedade = st.session_state.variedade

        produtividade_embaladeira = st.session_state.produtividade_embaladeira
        produtividade_talo = st.session_state.produtividade_talo
        produtividade_limpeza = st.session_state.produtividade_limpeza 
        produtividade_limpeza2 = st.session_state.produtividade_selecao 

        calibre_4_papel = st.session_state.calibre4 
        calibre_5_papel = st.session_state.calibre5 
        calibre_6_papel = st.session_state.calibre6 
        calibre_7_papel = st.session_state.calibre7 
        calibre_8_papel = st.session_state.calibre8 
        calibre_9_papel = st.session_state.calibre9 
        calibre_10_papel = st.session_state.calibre10
        calibre_12_papel = st.session_state.calibre12
        calibre_14_papel = st.session_state.calibre14
        calibre_16_papel = st.session_state.calibre16

        percent_caliber_4 = st.session_state_percent_4
        percent_caliber_5 = st.session_state_percent_5
        percent_caliber_6 = st.session_state_percent_6
        percent_caliber_7 = st.session_state_percent_7
        percent_caliber_8 = st.session_state_percent_8
        percent_caliber_9 = st.session_state_percent_9
        percent_caliber_10 = st.session_state_percent_10
        percent_caliber_12 = st.session_state_percent_12
        percent_caliber_14 = st.session_state_percent_14
        percent_caliber_16 = st.session_state_percent_16

    ###################### ATRIBUINDO OS PERCENTUAIS PARA A 2º ABA ######################
        
        def ajuste(b):
            if b['Calibre'] == 4:
                return percent_caliber_4
            elif b['Calibre'] == 5:
                return percent_caliber_5
            elif b['Calibre'] == 6:
                return percent_caliber_6
            elif b['Calibre'] == 7:
                return percent_caliber_7
            elif b['Calibre'] == 8:
                return percent_caliber_8
            elif b['Calibre'] == 9:
                return percent_caliber_9
            elif b['Calibre'] == 10:
                return percent_caliber_10
            elif b['Calibre'] == 12:
                return percent_caliber_12
            elif b['Calibre'] == 14:
                return percent_caliber_14
            elif b['Calibre'] == 16:
                return percent_caliber_16
        b['Percentual'] = b.apply(ajuste, axis = 1)

    ###################### ATRIBUINDO OS RIMOS PARA A 2º ABA ######################

        def ritmo(b):

            if variedade == 'Palmer':

                if (b['Calibre'] == 5 ) and (calibre_4_papel == 'Com' ):
                    return 229
                elif (b['Calibre'] == 4) and (calibre_5_papel == 'Com'):
                    return 229
                elif (b['Calibre'] == 6) and (calibre_6_papel == 'Com'):
                    return 169
                elif (b['Calibre'] == 7) and (calibre_7_papel == 'Com'):
                    return 174
                elif (b['Calibre'] == 8) and (calibre_8_papel == 'Com'):
                    return 191
                elif (b['Calibre'] == 9) and (calibre_9_papel == 'Com'):
                    return 157
                elif (b['Calibre'] == 10) and (calibre_10_papel == 'Com'):
                    return 139
                elif (b['Calibre'] == 12) and (calibre_12_papel == 'Com'):
                    return 149
                elif (b['Calibre'] == 14) and (calibre_14_papel == 'Com'):
                    return 85


############################################### PALMER SEM PAPEL #######################################################

                elif (b['Calibre'] == 5) and ( calibre_4_papel == 'Sem'):
                    return 517
                elif (b['Calibre'] == 4) and (calibre_5_papel == 'Sem'):
                    return 517
                elif (b['Calibre'] == 6) and ( calibre_6_papel == 'Sem'):
                    return 412
                elif (b['Calibre'] == 7) and (calibre_7_papel == 'Sem'):
                    return 321
                elif (b['Calibre'] == 8) and (calibre_8_papel == 'Sem'):
                    return 301
                elif (b['Calibre'] == 9) and (calibre_9_papel == 'Sem'):
                    return 257
                elif (b['Calibre'] == 10) and (calibre_10_papel == 'Sem'):
                    return 261
                elif (b['Calibre'] == 12) and ( calibre_12_papel == 'Sem'):
                    return 253
                elif (b['Calibre'] == 14) and (calibre_14_papel == 'Sem'):
                    return 220
            
            if (variedade == 'Keitt' or variedade == 'Omer'):
                if (b['Calibre'] == 5 and calibre_5_papel == 'Sem'):
                    return 517
                elif (b['Calibre'] == 4  and calibre_4_papel == 'Sem'):
                    return 517
                elif (b['Calibre'] == 6 and calibre_6_papel == 'Sem'):
                    return 412
                elif (b['Calibre'] == 7 and calibre_7_papel == 'Sem'):
                    return 321
                elif (b['Calibre'] == 8  and calibre_8_papel == 'Sem'):
                    return 301
                elif (b['Calibre'] == 9 and calibre_9_papel == 'Sem'):
                    return 257
                elif (b['Calibre'] == 10  and calibre_10_papel == 'Sem'):
                    return 261
                elif (b['Calibre'] == 12 and calibre_12_papel == 'Sem') :
                    return 253
                elif (b['Calibre'] == 14  and calibre_14_papel == 'Sem') :
                    return 220
                elif (b['Calibre'] == 16  and calibre_16_papel == 'Sem') :
                    return 200
                
                elif (b['Calibre'] == 5 and calibre_5_papel == 'Com'):
                    return 235
                elif (b['Calibre'] == 4 and calibre_4_papel == 'Com'):
                    return 235
                elif (b['Calibre'] == 6  and calibre_6_papel == 'Com'):
                    return 178
                elif (b['Calibre'] == 7 and calibre_7_papel == 'Com'):
                    return 185
                elif (b['Calibre'] == 8 and calibre_8_papel == 'Com'):
                    return 195
                elif (b['Calibre'] == 9  and calibre_9_papel == 'Com'):
                    return 154
                elif (b['Calibre'] == 10 and calibre_10_papel == 'Com'):
                    return 144
                elif (b['Calibre'] == 12 and calibre_12_papel == 'Com'):
                    return 158
                elif (b['Calibre'] == 14 and calibre_14_papel == 'Com'):
                    return 90
                elif (b['Calibre'] == 16 and calibre_16_papel == 'Com'):
                    return 80

            if variedade == 'Kent':

                if (b['Calibre'] == 5) and (calibre_5_papel == 'Sem'):
                    return 510
                elif (b['Calibre'] == 6) and (calibre_6_papel == 'Sem'):
                    return 410
                elif (b['Calibre'] == 7) and (calibre_7_papel == 'Sem'):
                    return 314
                elif (b['Calibre'] == 8) and (calibre_8_papel == 'Sem'):
                    return 300
                elif (b['Calibre'] == 9) and (calibre_9_papel == 'Sem'):
                    return 253
                elif (b['Calibre'] == 10) and (calibre_10_papel == 'Sem'):
                    return 248
                elif (b['Calibre'] == 12) and (calibre_12_papel == 'Sem'):
                    return 246
                elif (b['Calibre'] == 14) and (calibre_14_papel == 'Sem'):
                    return 200
                elif (b['Calibre'] == 16) and (calibre_16_papel == 'Sem'):
                    return 180

                elif (b['Calibre'] == 5) and (calibre_5_papel == 'Com'):
                    return 235
                elif (b['Calibre'] == 6) and (calibre_6_papel == 'Com'):
                    return 178
                elif (b['Calibre'] == 7) and (calibre_7_papel == 'Com'):
                    return 185
                elif (b['Calibre'] == 8) and (calibre_8_papel == 'Com'):
                    return 195
                elif (b['Calibre'] == 9) and (calibre_9_papel == 'Com'):
                    return 154
                elif (b['Calibre'] == 10) and (calibre_10_papel == 'Com'):
                    return 144
                elif (b['Calibre'] == 12) and (calibre_12_papel == 'Com'):
                    return 158
                elif (b['Calibre'] == 14) and (calibre_14_papel == 'Com'):
                    return 90
                elif (b['Calibre'] == 16) and (calibre_16_papel == 'Com'):
                    return 80

            if (variedade == 'Tommy Atkins' or variedade == 'Osteen'):

                if (b['Calibre'] == 5) and (calibre_5_papel == 'Com'):
                    return 235
                elif (b['Calibre'] == 6) and (calibre_6_papel == 'Com'):
                    return 178
                elif (b['Calibre'] == 7) and (calibre_7_papel == 'Com'):
                    return 185
                elif (b['Calibre'] == 8) and (calibre_8_papel == 'Com'):
                    return 195
                elif (b['Calibre'] == 9) and (calibre_9_papel == 'Com'):
                    return 154
                elif (b['Calibre'] == 10) and (calibre_10_papel == 'Com'):
                    return 144
                elif (b['Calibre'] == 12) and (calibre_12_papel == 'Com'):
                    return 158
                elif (b['Calibre'] == 14) and (calibre_14_papel == 'Com'):
                    return 90

        ################################################## Tommy SEM PAPEL ############################################################# 

                elif (b['Calibre'] == 5) and (calibre_5_papel == 'Sem'):
                    return 517
                elif (b['Calibre'] == 6) and (calibre_6_papel == 'Sem'):
                    return 412
                elif (b['Calibre'] == 7) and ( calibre_7_papel == 'Sem'):
                    return 321
                elif (b['Calibre'] == 8) and ( calibre_8_papel == 'Sem'):
                    return 301
                elif (b['Calibre'] == 9) and (calibre_9_papel == 'Sem'):
                    return 257
                elif (b['Calibre'] == 10) and (calibre_10_papel == 'Sem'):
                    return 261
                elif (b['Calibre'] == 12) and (calibre_12_papel == 'Sem'):
                    return 253
                elif (b['Calibre'] == 14) and (calibre_14_papel == 'Sem'):
                    return 220

            else:
                return 'NADA'
        
        b['Ritmo'] = b.apply(ritmo, axis = 1)
        
        filtro_ritmo = b['Ritmo'] != 'NADA'
        b = b[filtro_ritmo]
            
        col1, col2,col3,col4 = st.columns([0.1,1,0.1,1])
        
    ################################ CÁCULO DE CAIXAS 2º ABA ##########################################
        from modulos_dash.balanceamento.funcoes_pagina_linhas.modulos_paginas_linhas import *

        b =  contas_caixas_e_horas(b,caixotes, avg_frutos_caixotes,primeira_percent,segunda_percent,terceira_percent, produtividade_embaladeira)
        
    ################################ BALANCEAMENTO  2º ABA ##########################################

        ritmo_embaladeira, corte_talo, ritmo_talo, diferenca_aceitavel, corte_talo2, ritmo_talo_2 = contas_balanceamento(b, embaladeira, caixotes, avg_frutos_caixotes, produtividade_talo)
        
    ################################ FUNÇÃO BALANCEAMENTO 2º ABA ##########################################

        def equilibrio(corte_talo, embaladeira):


            caixotes_hora = round((caixotes*0.0416667)/(ritmo_talo_2))
            soma = segunda_percent + terceira_percent + refugo_percent
            selecao_ = round((caixotes_hora * avg_frutos_caixotes * soma / (3501 * produtividade_limpeza2)) + (caixotes_hora * avg_frutos_caixotes * primeira_percent / (6480 * produtividade_limpeza2)))

            st.write("A quantidade ideal de pessoas no talo tem que ser:", corte_talo2)
            st.write('Capacidade de caixotes/hora no corte de talo é de:', caixotes_hora)
            st.write('Capacidade de Toneladas/Horas é de:', round(((b['Caixas_total'].sum()*4.05)/1000)/(b['Horas_4kg'].sum()/embaladeira),2))

            Limpeza_selecao = round((caixotes_hora * avg_frutos_caixotes * 0.6) / (3230 * produtividade_limpeza))

            st.write('Quantidade de pessoas na limpeza:', Limpeza_selecao)
            st.write('Quantidade de pessoas na selelao:', selecao_)
                
    ########################################### LAYOUT LINHAS DE EMBALAGEM ###########################################

        Layout_linha = pd.DataFrame({"Linha":['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22'],
                                    "Calibre":"",
                                    "Qualidade":"",
                                    "Calibre2":"",
                                    "Qualidade2":"",
                                    "Auxiliar":"",
                                    "Auxiliar2":"",
                                    "Frutos":"",
                                    "Frutos2":"",
                                    "Caixas":"",
                                    "Caixas2":"",
                                    "Horas":"",
                                    "Embaladeiras":"",
                                    "Paletizadores":""}) 
        
        def preenchendo_calibre(Layout_linha):

            if Programa_input == 'Entre Safra':

                if variedade == 'Palmer':

                    if (Layout_linha['Linha'] == '1'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '2'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '12'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '13'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '16'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '17'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '20'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '21'):
                        return '5'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '5'

                if variedade == 'Tommy Atkins':

                    if ( Layout_linha['Linha'] == '1'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '2'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '13'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return '9'
                    elif ( Layout_linha['Linha'] == '16'):
                        return '9'
                    elif ( Layout_linha['Linha'] == '17'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '20'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '21'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '7'

                if (variedade == 'Kent' or variedade == 'Keitt'  or variedade == 'Omer' or variedade == 'Osteen'):

                    if ( Layout_linha['Linha'] == '1'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '2'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return 'Aéreo'
                    elif ( Layout_linha['Linha'] == '10'):
                        return 'Aéreo'
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '13'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '16'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '19'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '9'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '9'

            if Programa_input == 'Safra':

                if variedade == 'Palmer' or variedade == 'Tommy Atkins':

                    if ( Layout_linha['Linha'] == '1'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '2'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '3'):
                        return '14'
                    elif ( Layout_linha['Linha'] == '4'):
                        return '14'
                    elif ( Layout_linha['Linha'] == '5'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '6'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return '9'
                    elif ( Layout_linha['Linha'] == '10'):
                        return '9'
                    elif ( Layout_linha['Linha'] == '11'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '12'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '15'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '18'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '8'

                if (variedade == 'Kent' or variedade == 'Keitt' or variedade == 'Omer' or variedade == 'Osteen'):

                    if ( Layout_linha['Linha'] == '1'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '2'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '3'):
                        return '14'
                    elif ( Layout_linha['Linha'] == '4'):
                        return '14'
                    elif ( Layout_linha['Linha'] == '5'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '6'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return '9'
                    elif ( Layout_linha['Linha'] == '10'):
                        return '9'
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '15'):
                        return '8'
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '18'):
                        return '7'
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '12'

            else:
                return 'NADA'
        Layout_linha['Calibre'] = Layout_linha.apply(preenchendo_calibre, axis = 1)

        def preenchendo_qualidade(Layout_linha):

            if Programa_input == 'Entre Safra':

                if variedade == 'Palmer':

                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '12'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '13'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '16'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '17'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '20'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'
                
                if variedade == 'Tommy Atkins':
                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '13'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '16'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '17'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '20'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'
        
                if (variedade == 'Kent' or variedade == 'Keitt' or variedade == 'Omer' or variedade == 'Osteen'):

                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '13'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '16'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '19'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'

            if Programa_input == 'Safra':

                if (variedade == 'Palmer' or variedade == 'Tommy Atkins'):
                    if ( Layout_linha['Linha'] == '1'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '2'):
                        return 'Refugo'
                    elif ( Layout_linha['Linha'] == '3'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '4'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '5'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '6'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '10'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '11'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '12'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '15'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '18'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'
                
                if (variedade == 'Kent' or variedade == 'Keitt' or variedade == 'Omer' or variedade == 'Osteen'):
        ############################################################### KENT E KEITT ###############################################################
                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '4'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '5'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '6'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '10'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '15'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '18'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'

            else:
                return 'NADA'
        Layout_linha['Qualidade'] = Layout_linha.apply(preenchendo_qualidade, axis = 1)

        def preenchendo_calibre2(Layout_linha):
        
            if Programa_input == 'Entre Safra':

                if variedade == 'Palmer':
                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return ''
                    elif ( Layout_linha['Linha'] == '13'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return ''
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '9'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '9'

                if variedade == 'Tommy Atkins':

                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return ''
                    elif ( Layout_linha['Linha'] == '13'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return ''
                    elif ( Layout_linha['Linha'] == '16'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '17'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '14'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '14'

                if (variedade == 'Kent' or variedade == 'Keitt' or variedade == 'Omer' or variedade == 'Osteen'):

                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '16'
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '16'):
                        return '12'
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '19'):
                        return '10'
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '5'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '5'

            if Programa_input == 'Safra':

                if (variedade == 'Palmer' or variedade == 'Tommy Atkins'):
            
                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return '5'
                    elif ( Layout_linha['Linha'] == '4'):
                        return '5'
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return ''
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return ''
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return ''
                    elif ( Layout_linha['Linha'] == '22'):
                        return ''
    
                if (variedade == 'Kent' or variedade == 'Keitt' or variedade == 'Omer' or variedade == 'Osteen'):

                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '16'
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return '6'
                    elif ( Layout_linha['Linha'] == '15'):
                        return ''
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '5'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '5'

            else:
                return 'NADA'
        Layout_linha['Calibre2'] = Layout_linha.apply(preenchendo_calibre2, axis = 1)


        def preenchendo_qualidade2(Layout_linha):
        
            if Programa_input == 'Entre Safra':

                if (variedade == 'Palmer'):

                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return ''
                    elif ( Layout_linha['Linha'] == '13'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return ''
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'
        
                if (variedade == 'Tommy Atkins'):

                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return ''
                    elif ( Layout_linha['Linha'] == '13'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return ''
                    elif ( Layout_linha['Linha'] == '16'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '17'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'

                if (variedade == 'Kent' or variedade == 'Keitt' or variedade == 'Omer' or variedade == 'Osteen'):
                
                    if ( Layout_linha['Linha'] == '1'):
                        return ''
                    elif ( Layout_linha['Linha'] == '2'):
                        return ''
                    elif ( Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif ( Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif ( Layout_linha['Linha'] == '7'):
                        return ''
                    elif ( Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '16'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '19'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'
    
            if Programa_input == 'Safra':
                
                if (variedade == 'Palmer' or variedade == 'Tommy Atkins'):

                    if (Layout_linha['Linha'] == '1'):
                        return ''
                    elif (Layout_linha['Linha'] == '2'):
                        return ''
                    elif (Layout_linha['Linha'] == '3'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '4'):
                        return '1'
                    elif (Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif (Layout_linha['Linha'] == '7'):
                        return ''
                    elif (Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return ''
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return ''
                    elif ( Layout_linha['Linha'] == '15'):
                        return ''
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return ''
                    elif ( Layout_linha['Linha'] == '18'):
                        return ''
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return ''
                    elif ( Layout_linha['Linha'] == '22'):
                        return ''
        
                if (variedade == 'Kent' or variedade == 'Keitt' or variedade == 'Omer' or variedade == 'Osteen'):

                    if (Layout_linha['Linha'] == '1'):
                        return ''
                    elif (Layout_linha['Linha'] == '2'):
                        return ''
                    elif (Layout_linha['Linha'] == '3'):
                        return ''
                    elif ( Layout_linha['Linha'] == '4'):
                        return ''
                    elif (Layout_linha['Linha'] == '5'):
                        return ''
                    elif ( Layout_linha['Linha'] == '6'):
                        return ''
                    elif (Layout_linha['Linha'] == '7'):
                        return ''
                    elif (Layout_linha['Linha'] == '8'):
                        return ''
                    elif ( Layout_linha['Linha'] == '9'):
                        return ''
                    elif ( Layout_linha['Linha'] == '10'):
                        return ''
                    elif ( Layout_linha['Linha'] == '11'):
                        return ''
                    elif ( Layout_linha['Linha'] == '12'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '13'):
                        return ''
                    elif ( Layout_linha['Linha'] == '14'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '15'):
                        return ''
                    elif ( Layout_linha['Linha'] == '16'):
                        return ''
                    elif ( Layout_linha['Linha'] == '17'):
                        return '2'
                    elif ( Layout_linha['Linha'] == '18'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '19'):
                        return ''
                    elif ( Layout_linha['Linha'] == '20'):
                        return ''
                    elif ( Layout_linha['Linha'] == '21'):
                        return '1'
                    elif ( Layout_linha['Linha'] == '22'):
                        return '2'
        
            else:
                return 'NADA'
        Layout_linha['Qualidade2'] = Layout_linha.apply(preenchendo_qualidade2, axis = 1)

        Layout_linha, b, quality = contas_auxiliares(Layout_linha,b,quality)
        b['Calibre'] = b.apply(rename_b, axis = 1)
        
            
    ##################################### CALCULO DA QUANTIDADE DE FRUTOS POR LINHA ################################################################

        Layout_linha_7 = criacao_layout_linhas(Layout_linha, quality, caixotes, avg_frutos_caixotes, b, embaladeira)



    ############################## CÁLCULO DE EMBALADEIRAS POR SETORES ###############################

        Layout_linha_7['Setores'] = Layout_linha_7.apply(setores, axis = 1)
        Layout_linha_7['Setores'] = Layout_linha_7['Setores'].astype(str)

    ############################## EXIBIÇÃO DAS INFORMAÇÕES ##############################
        import plotly.express as px
        import plotly.graph_objects as go
        
        with col11:
            ############################## PIZZA DOS PERCENTUAIS ##############################
            st.write("")
            st.info('##### Percentuais de qualidade:')

            fig = go.Figure(data=[go.Pie(labels = quality['Qualidade'], values = quality['Percent'], marker_colors = px.colors.sequential.Emrld ,hole = .35, pull=0.025)])
            fig.update_traces(textinfo='label+percent', textfont_size=15, textposition="inside", marker=dict(line = dict(color = '#000000', width = 1)))
            fig.update_layout(height = 450, width = 450, font = dict(size = 15))

            st.plotly_chart(fig) 


        ############################## BARRA - EMBALADEIRAS POR SETOR ##############################
        with col22:
            
            st.write(" ")
            st.info('##### Quantidade de embaladeiras por setor:')

            df_setores = criando_df_setores(Layout_linha_7)

            fig2 = px.bar(df_setores, x = 'Setores', y = 'Embaladeiras', color = 'Setores', text= 'Embaladeiras', color_discrete_sequence= px.colors.sequential.Aggrnyl ) 
            fig2.update_layout(height = 450, width = 650, uniformtext_minsize = 8, uniformtext_mode = 'show', font = dict(size = 14))
            fig2.update_traces(textfont_size = 14, textangle = 0, textposition = 'outside', cliponaxis = False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

            st.plotly_chart(fig2)

        ############################## BARRA - EMBALADEIRAS POR LINHA ##############################
        with col33:

            st.write(" ")
            st.info('##### Quantidade de embaladeiras por linha:')
            
            fig = px.bar(Layout_linha_7, x = 'Linha', y = 'Embaladeiras', color = 'Setores', text = 'Embaladeiras',color_discrete_sequence= px.colors.sequential.Aggrnyl)
            fig.update_layout(height = 450, width = 650, uniformtext_minsize=8, uniformtext_mode='show', font = dict(size = 14))
            fig.update_traces(textfont_size=20, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

            st.plotly_chart(fig)

        ############################## PLANILHA - DETALHES ##############################
        with col4:  

            st.info('##### Informações detalhadas das linhas de embalagem:')
            st.write('_______')

            Layout_linha_8 = criando_lay_8(Layout_linha_7)

            Layout_linha_8
            Layout_linha_8.to_excel('Layout_final.xlsx')
            st.download_button( label = 'Baixar Configuração (csv)',data = Layout_linha_8.to_csv(), mime = 'text/csv')

        with col2:

            st.info('##### Caixas processadas X restantes:')
            st.write('#### Tempo (min) de finalização estimado:',mins )
            fig = go.Figure()

            fig.add_trace(go.Bar(y = [caixas_total_processadas], text = str(caixas_total_processadas), name = 'Processado', marker_color='rgb(169, 220, 103)'))

            fig.add_trace(go.Bar(y = [caixas_restantes], text = str(caixas_restantes), name = 'Restante', marker_color='rgb(253, 174, 107)'))

            fig.update_layout(height = 500, width = 800, font = dict(size = 14))
            fig.update_traces(textfont_size=14, textposition="inside", marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

            #fig.add_trace(go.Bar(x = caixas_restantes))
            st.plotly_chart(fig)
            

    elif pagina_selecionada == 'Distribuição embaladeiras':

        ###################### IMPORT VALORES DAS ABAS PASSADAS ######################
        import plotly.express as px

        embaladeira = st.session_state.embaladeira 
        produtividade_embaladeira = st.session_state.produtividade_embaladeira
        produtividade_talo = st.session_state.produtividade_talo
        
        b = st.session_state.b

        caixotes_hora = st.session_state.caixotes_hora
        controle2 = st.session_state.controle
        ton_horas = st.session_state.ton_horas


        col1x, col2x, col3x, col4x,col5x,col6x = st.columns([1,1,1,1,1,1])    

    ######################## EXIBINDO MÉTRICAS CALCULADAS NA ABA ANTERIOR ########################

        col1x.metric(label="Controle", value= controle2, delta= VARIEDADE)
        col6x.metric(label="Caixotes/Hora", value= caixotes_hora, delta= None)        
        col3x.metric(label="MAF (t/h)", value= produtividade_atual) 


        diference = str(round(((ton_horas - produtividade_atual)*100) / produtividade_atual ,2)) + ' ' + '%'
        col4x.metric(label="Embaladeiras (t/h)", value = ton_horas, delta = diference)


        tempo_2 = st.session_state_tempo
        col2x.metric(label="Intervalo de tempo (min)", value= round(tempo_2,2))

        ###################### LAYOUT PÁGINA  ######################

        variedade = st.session_state.variedade
        col1, col2, col3 = st.columns(3)
        colunas1, colunas2 = st.columns([1,0.1])
        

        with colunas1:
            st.success('### Recomendação de embaladeiras por calibre:')
        colu1, colu2, colu3, colu4  = st.columns(4)

        ########################## LAYOUT DAS LIHAS ##########################


        Layout_linha_9 = pd.read_excel('Layout_final.xlsx')
        
        from modulos_dash.balanceamento.funcoes_paginas_distribuicao.modulos_distribuicao import *

        Layout_linha_9 = lay_9(Layout_linha_9)

    ################## DATASET EMBALADEIRAS #####################

        padrao_embaldeiras['PESSOA'] = padrao_embaldeiras['PESSOA'].str[6:]
    
    ############ CORREÇÃO VARIEDADE DATASET DAS EMBALADEIRAS ##########################

        padrao_embaldeiras['VARIEDADE'] = padrao_embaldeiras.apply(correcao_variedade, axis = 1)
        
        ##################### ESTRUTURAÇÃO PARA GRÁFICO DAS EMBALADEIRAS DE CADA CALIBRE ######################

        def check_valores(Layout_linha_9, list_values):
            resultDict = {}
            for elem in list_values:
                if elem in Layout_linha_9['Calibre'] and variedade == 'Palmer':

                    resultDict[elem] = True

                    aaa = Layout_linha_9.groupby(['Calibre'])['Embaladeiras_1'].sum()
                    aaa = aaa.reset_index()
                

                    bbb = Layout_linha_9.groupby(['Calibre2'])['Embaladeiras_2'].sum()
                    bbb = bbb.reset_index()
                    bbb = bbb.rename(columns={'Calibre2':'Calibre', 'Embaladeiras_2':'Embaladeiras_1'})
            
                    ccc = pd.concat((aaa,bbb))
                    ccc['Calibre'] = ccc['Calibre'].replace(' ','0')
                    ccc['Calibre'] = ccc['Calibre'].astype(float)
                    ccc = ccc.groupby(['Calibre'])['Embaladeiras_1'].sum()
                    ccc = ccc.reset_index()
                    
                    if elem == 5.0:

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Palmer'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 5
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        a = padrao_embaldeiras_palmer.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(20)
                        a = a.reset_index()
                        a['mean'] = round(a['mean'],0)
                        a = a.rename(columns = {'mean':'Caixas/Hora'})
                        a['Calibre'] = 5.0
                        a['Calibre'] = a['Calibre'].astype(str)
                        a['ID_PESSOA'] = a['ID_PESSOA'].astype(str)
                        media_a = a['Caixas/Hora'].mean()
                        st.session_state.media_a = media_a
                        aa = px.bar(a,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Palmer - Calibre 5',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        aa.update_yaxes(range = [a['Caixas/Hora'].min()-10,a['Caixas/Hora'].max()])
                        aa.add_hline(229)
                        aa.update_layout(height = 350, width = 350)
                        aa.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                        

                    elif elem == 6.0:
                        
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Palmer'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 6
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                    

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)
                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(a['ID_PESSOA'])]


                        b = padrao_embaldeiras_palmer_2.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        b = b.reset_index()
                        b['mean'] = round(b['mean'],0)
                        b = b.rename(columns = {'mean':'Caixas/Hora'})
                        b['Calibre'] = 6.0
                        b['Calibre'] = b['Calibre'].astype(str)
                        b['ID_PESSOA'] = b['ID_PESSOA'].astype(str)
                        media_b = b['Caixas/Hora'].mean()
                        st.session_state.media_b = media_b
                        bb = px.bar(b,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Palmer - Calibre 6',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        bb.update_yaxes(range = [b['Caixas/Hora'].min()-10,b['Caixas/Hora'].max()])
                        bb.add_hline(169)
                        bb.update_layout(height = 350, width = 350)
                        bb.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 7.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)
                        
                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Palmer'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 7
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)
                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        c = padrao_embaldeiras_palmer_3.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        c = c.reset_index()
                        c['mean'] = round(c['mean'],0)
                        c = c.rename(columns = {'mean':'Caixas/Hora'})
                        c['Calibre'] = 7.0
                        c['Calibre'] = c['Calibre'].astype(str)
                        c['ID_PESSOA'] = c['ID_PESSOA'].astype(str)
                        media_c = c['Caixas/Hora'].mean()
                        st.session_state.media_c = media_c
                        cc = px.bar(c,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Palmer - Calibre 7',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        cc.update_yaxes(range = [c['Caixas/Hora'].min()-10,c['Caixas/Hora'].max()])
                        cc.add_hline(174)
                        cc.update_layout(height = 350, width = 350)
                        cc.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 8.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Palmer'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 8
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        d = padrao_embaldeiras_palmer_4.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        d = d.reset_index()
                        d['mean'] = round(d['mean'],0)
                        d = d.rename(columns = {'mean':'Caixas/Hora'})
                        d['Calibre'] = 8.0
                        d['Calibre'] = d['Calibre'].astype(str)
                        d['ID_PESSOA'] = d['ID_PESSOA'].astype(str)
                        media_d = d['Caixas/Hora'].mean()
                        st.session_state.media_d = media_d
                        dd = px.bar(d,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Palmer - Calibre 8',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        dd.update_yaxes(range = [d['Caixas/Hora'].min()-10,d['Caixas/Hora'].max()])
                        dd.add_hline(189)
                        dd.update_layout(height = 350, width = 350)
                        dd.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                        

                    elif elem == 9.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0) 
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Palmer'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 9
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        
                        e = padrao_embaldeiras_palmer_5.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        e = e.reset_index()
                        e['mean'] = round(e['mean'],0)
                        e = e.rename(columns = {'mean':'Caixas/Hora'})
                        e['Calibre'] = 9.0
                        e['Calibre'] = e['Calibre'].astype(str)
                        
                        media_e = e['Caixas/Hora'].mean()
                        st.session_state.media_e = media_e
                        ee = px.bar(e,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Palmer - Calibre 9',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        ee.update_yaxes(range = [e['Caixas/Hora'].min()-10,e['Caixas/Hora'].max()])
                        ee.add_hline(157)
                        ee.update_layout(height = 350, width = 350)
                        ee.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 10.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)
                        
                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Palmer'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 10
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]

                        f = padrao_embaldeiras_palmer_6.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        f = f.reset_index()
                        f['mean'] = round(f['mean'],0)
                        f = f.rename(columns = {'mean':'Caixas/Hora'})
                        f['Calibre'] = 10.0
                        f['Calibre'] = f['Calibre'].astype(str)
                        f['ID_PESSOA'] = f['ID_PESSOA'].astype(str)
                        media_f = f['Caixas/Hora'].mean()
                        st.session_state.media_f = media_f
                        ff = px.bar(f,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Palmer - Calibre 10', hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        ff.update_yaxes(range = [f['Caixas/Hora'].min()-10,f['Caixas/Hora'].max()])
                        ff.add_hline(139)
                        ff.update_layout(height = 350, width = 350)
                        ff.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                        
                                    
                    elif elem == 12.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Palmer'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 12
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        
                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_7 = padrao_embaldeiras_palmer_6[~padrao_embaldeiras_palmer_6.ID_PESSOA.isin(f['ID_PESSOA'])]

                        g = padrao_embaldeiras_palmer_7.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        g = g.reset_index()
                        g['mean'] = round(g['mean'],0)
                        g = g.rename(columns = {'mean':'Caixas/Hora'})
                        g['Calibre'] = 12.0
                        g['Calibre'] = g['Calibre'].astype(str)
                        g['ID_PESSOA'] = g['ID_PESSOA'].astype(str)
                        media_g = g['Caixas/Hora'].mean()
                        st.session_state.media_g = media_g
                        gg = px.bar(g,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Palmer - Calibre 12',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        gg.update_yaxes(range = [g['Caixas/Hora'].min()-10,g['Caixas/Hora'].max()])
                        gg.add_hline(149)
                        gg.update_layout(height = 350, width = 350)
                        gg.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    
                    elif elem == 14.0:

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Palmer'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 14
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        
                        h = padrao_embaldeiras_palmer.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(20)
                        h = h.reset_index()
                        h['mean'] = round(h['mean'],0)
                        h = h.rename(columns = {'mean':'Caixas/Hora'})
                        h['Calibre'] = 14.0
                        h['Calibre'] = h['Calibre'].astype(str)
                        h['ID_PESSOA'] = h['ID_PESSOA'].astype(str)
                        media_h = h['Caixas/Hora'].mean()
                        st.session_state.media_h = media_h
                        hh = px.bar(h,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Palmer - Calibre 14',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        hh.update_yaxes(range = [h['Caixas/Hora'].min()-10,h['Caixas/Hora'].max()])
                        hh.update_layout(height = 350, width = 350)
                        hh.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                elif elem in Layout_linha_9['Calibre'] and variedade == 'Kent':
                    resultDict[elem] = True
                    
                    aaa = Layout_linha_9.groupby(['Calibre'])['Embaladeiras_1'].sum()
                    aaa = aaa.reset_index()

                    bbb = Layout_linha_9.groupby(['Calibre2'])['Embaladeiras_2'].sum()
                    bbb = bbb.reset_index()
                    bbb = bbb.rename(columns={'Calibre2':'Calibre', 'Embaladeiras_2':'Embaladeiras_1'})

                    ccc = pd.concat((aaa,bbb))
                    ccc['Calibre'] = ccc['Calibre'].replace(' ','0')
                    ccc['Calibre'] = ccc['Calibre'].astype(float)
                    ccc = ccc.groupby(['Calibre'])['Embaladeiras_1'].sum()
                    ccc = ccc.reset_index()

                    if elem == 5.0:

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Kent'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 5
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        
                        a = padrao_embaldeiras_palmer.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(20)
                        a = a.reset_index()
                        a['mean'] = round(a['mean'],0)
                        a = a.rename(columns = {'mean':'Caixas/Hora'})
                        a['Calibre'] = 5.0
                        a['Calibre'] = a['Calibre'].astype(str)
                        a['ID_PESSOA'] = a['ID_PESSOA'].astype(str)
                        media_a = a['Caixas/Hora'].mean()
                        st.session_state.media_a = media_a
                        aa = px.bar(a,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Kent - Calibre 5',hover_name = 'PESSOA', color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        aa.update_yaxes(range = [a['Caixas/Hora'].min()-10,a['Caixas/Hora'].max()])
                        aa.update_layout(height = 350, width = 350)
                        aa.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                        

                    elif elem == 6.0:
                        
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Kent'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]
                        
                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 6
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)
                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(a['ID_PESSOA'])]

                        b = padrao_embaldeiras_palmer_2.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        b = b.reset_index()
                        b['mean'] = round(b['mean'],0)
                        b = b.rename(columns = {'mean':'Caixas/Hora'})
                        b['Calibre'] = 6.0
                        b['Calibre'] = b['Calibre'].astype(str)
                        b['ID_PESSOA'] = b['ID_PESSOA'].astype(str)
                        media_b = b['Caixas/Hora'].mean()
                        st.session_state.media_b = media_b
                        bb = px.bar(b,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Kent - Calibre 6',hover_name = 'PESSOA', color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        bb.update_yaxes(range = [b['Caixas/Hora'].min()-10,b['Caixas/Hora'].max()])
                        bb.update_layout(height = 350, width = 350)
                        bb.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 7.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Kent'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 7
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)
                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        c = padrao_embaldeiras_palmer_3.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        c = c.reset_index()
                        c['mean'] = round(c['mean'],0)
                        c = c.rename(columns = {'mean':'Caixas/Hora'})
                        c['Calibre'] = 7.0
                        c['Calibre'] = c['Calibre'].astype(str)
                        c['ID_PESSOA'] = c['ID_PESSOA'].astype(str)
                        media_c = c['Caixas/Hora'].mean()
                        st.session_state.media_c = media_c
                        cc = px.bar(c,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Kent - Calibre 7', hover_name = 'PESSOA', color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        cc.update_yaxes(range = [c['Caixas/Hora'].min()-10,c['Caixas/Hora'].max()])
                        cc.update_layout(height = 350, width = 350)
                        cc.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    
                    elif elem == 8.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int) 

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Kent'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 8
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]


                        d = padrao_embaldeiras_palmer_4.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        d = d.reset_index()
                        d['mean'] = round(d['mean'],0)
                        d = d.rename(columns = {'mean':'Caixas/Hora'})
                        d['Calibre'] = 8.0
                        d['Calibre'] = d['Calibre'].astype(str)
                        d['ID_PESSOA'] = d['ID_PESSOA'].astype(str)
                        media_d = d['Caixas/Hora'].mean()
                        st.session_state.media_d = media_d
                        dd = px.bar(d,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Kent - Calibre 8', hover_name = 'PESSOA', color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        dd.update_yaxes(range = [d['Caixas/Hora'].min()-10,d['Caixas/Hora'].max()])
                        dd.update_layout(height = 350, width = 350)
                        dd.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    
                    elif elem == 9.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Kent'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 9
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        e = padrao_embaldeiras_palmer_5.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        e = e.reset_index()
                        e['mean'] = round(e['mean'],0)
                        e = e.rename(columns = {'mean':'Caixas/Hora'})
                        e['Calibre'] = 9.0
                        e['Calibre'] = e['Calibre'].astype(str)
                        e['ID_PESSOA'] = e['ID_PESSOA'].astype(str)
                        media_e = e['Caixas/Hora'].mean()
                        st.session_state.media_e = media_e
                        ee = px.bar(e,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Kent - Calibre 9' ,hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        ee.update_yaxes(range = [e['Caixas/Hora'].min()-10,e['Caixas/Hora'].max()])
                        ee.update_layout(height = 350, width = 350)
                        ee.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    
                    elif elem == 10.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Kent'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 10
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]

                        f = padrao_embaldeiras_palmer_6.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        f = f.reset_index()
                        f['mean'] = round(f['mean'],0)
                        f = f.rename(columns = {'mean':'Caixas/Hora'})
                        f['Calibre'] = 10.0
                        f['Calibre'] = f['Calibre'].astype(str)
                        f['ID_PESSOA'] = f['ID_PESSOA'].astype(str)
                        media_f = f['Caixas/Hora'].mean()
                        st.session_state.media_f = media_f
                        ff = px.bar(f,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Kent - Calibre 10' ,hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        ff.update_yaxes(range = [f['Caixas/Hora'].min()-10,f['Caixas/Hora'].max()])
                        ff.update_layout(height = 350, width = 350)
                        ff.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    
                    elif elem == 12.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Kent'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 12
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_7 = padrao_embaldeiras_palmer_6[~padrao_embaldeiras_palmer_6.ID_PESSOA.isin(f['ID_PESSOA'])]

                        g = padrao_embaldeiras_palmer_7.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        g = g.reset_index()
                        g['mean'] = round(g['mean'],0)
                        g = g.rename(columns = {'mean':'Caixas/Hora'})
                        g['Calibre'] = 12.0
                        g['Calibre'] = g['Calibre'].astype(str)
                        g['ID_PESSOA'] = g['ID_PESSOA'].astype(str)
                        media_g = g['Caixas/Hora'].mean()
                        st.session_state.media_g = media_g
                        gg = px.bar(g,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Kent - Calibre 12',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        gg.update_yaxes(range = [g['Caixas/Hora'].min()-10,g['Caixas/Hora'].max()])
                        gg.update_layout(height = 350, width = 350)
                        gg.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    
                    elif elem == 14.0:

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Kent'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 14
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        h = padrao_embaldeiras_palmer.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(20)
                        h = h.reset_index()
                        h['mean'] = round(h['mean'],0)
                        h = h.rename(columns = {'mean':'Caixas/Hora'})
                        h['Calibre'] = 14.0
                        h['Calibre'] = h['Calibre'].astype(str)
                        h['ID_PESSOA'] = h['ID_PESSOA'].astype(str)
                        media_h = h['Caixas/Hora'].mean()
                        st.session_state.media_h = media_h
                        hh = px.bar(h,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Kent - Calibre 14',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        hh.update_yaxes(range = [h['Caixas/Hora'].min()-10,h['Caixas/Hora'].max()])
                        hh.update_layout(height = 350, width = 350)
                        hh.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                elif elem in Layout_linha_9['Calibre'] and (variedade == 'Keitt'  or variedade == 'Omer'):

                    resultDict[elem] = True
                    aaa = Layout_linha_9.groupby(['Calibre'])['Embaladeiras_1'].sum()
                    aaa = aaa.reset_index()


                    bbb = Layout_linha_9.groupby(['Calibre2'])['Embaladeiras_2'].sum()
                    bbb = bbb.reset_index()
                    bbb = bbb.rename(columns={'Calibre2':'Calibre', 'Embaladeiras_2':'Embaladeiras_1'})

                    ccc = pd.concat((aaa,bbb))
                    ccc['Calibre'] = ccc['Calibre'].replace(' ','0')
                    ccc['Calibre'] = ccc['Calibre'].astype(float)
                    ccc = ccc.groupby(['Calibre'])['Embaladeiras_1'].sum()
                    ccc = ccc.reset_index()


                    if elem == 5.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Keitt'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 5
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        a = padrao_embaldeiras_palmer.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        a = a.reset_index()
                        a['mean'] = round(a['mean'],0)
                        a = a.rename(columns = {'mean':'Caixas/Hora'})
                        a['Calibre'] = 5.0
                        a['Calibre'] = a['Calibre'].astype(str)
                        a['ID_PESSOA'] = a['ID_PESSOA'].astype(str)

                        media_a = a['Caixas/Hora'].mean()
                        st.session_state.media_a = media_a

                        aa = px.bar(a,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Keitt - Calibre 5',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        aa.update_yaxes(range = [a['Caixas/Hora'].min()-10,a['Caixas/Hora'].max()])
                        aa.add_hline(517)
                        aa.update_layout(height = 350, width = 350)
                        aa.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 6.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Keitt'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 6
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)
                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(a['ID_PESSOA'])]

                        b = padrao_embaldeiras_palmer_2.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        b = b.reset_index()
                        b['mean'] = round(b['mean'],0)
                        b = b.rename(columns = {'mean':'Caixas/Hora'})
                        b['Calibre'] = 6.0
                        b['Calibre'] = b['Calibre'].astype(str)
                        b['ID_PESSOA'] = b['ID_PESSOA'].astype(str)
                        media_b = b['Caixas/Hora'].mean()
                        st.session_state.media_b = media_b
                        bb = px.bar(b,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Keitt - Calibre 6',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        bb.update_yaxes(range = [b['Caixas/Hora'].min()-10,b['Caixas/Hora'].max()])
                        bb.add_hline(412)
                        bb.update_layout(height = 350, width = 350)
                        bb.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 7.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Keitt'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 7
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)
                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        c = padrao_embaldeiras_palmer_3.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        c = c.reset_index()
                        c['mean'] = round(c['mean'],0)
                        c = c.rename(columns = {'mean':'Caixas/Hora'})
                        c['Calibre'] = 7.0
                        c['Calibre'] = c['Calibre'].astype(str)
                        c['ID_PESSOA'] = c['ID_PESSOA'].astype(str)
                        media_c = c['Caixas/Hora'].mean()
                        st.session_state.media_c = media_c
                        cc = px.bar(c,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Keitt - Calibre 7',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        cc.update_yaxes(range = [c['Caixas/Hora'].min()-10,c['Caixas/Hora'].max()])
                        cc.add_hline(321)
                        cc.update_layout(height = 350, width = 350)
                        cc.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 8.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Keitt'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 8
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        d = padrao_embaldeiras_palmer_4.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        d = d.reset_index()
                        d['mean'] = round(d['mean'],0)
                        d = d.rename(columns = {'mean':'Caixas/Hora'})
                        d['Calibre'] = 8.0
                        d['Calibre'] = d['Calibre'].astype(str)
                        d['ID_PESSOA'] = d['ID_PESSOA'].astype(str)
                        media_d = d['Caixas/Hora'].mean()
                        st.session_state.media_d = media_d
                        dd = px.bar(d,y = 'Caixas/Hora', color = 'ID_PESSOA',title = 'Keitt - Calibre 8',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        dd.update_yaxes(range = [d['Caixas/Hora'].min()-10,d['Caixas/Hora'].max()])
                        dd.add_hline(301)
                        dd.update_layout(height = 350, width = 350)
                        dd.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 9.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Keitt'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 9
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        e = padrao_embaldeiras_palmer_5.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        e = e.reset_index()
                        e['mean'] = round(e['mean'],0)
                        e = e.rename(columns = {'mean':'Caixas/Hora'})
                        e['Calibre'] = 9.0
                        e['Calibre'] = e['Calibre'].astype(str)
                        e['ID_PESSOA'] = e['ID_PESSOA'].astype(str)
                        media_e = e['Caixas/Hora'].mean()
                        st.session_state.media_e = media_e
                        ee = px.bar(e,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Keitt - Calibre 9' ,hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        ee.update_yaxes(range = [e['Caixas/Hora'].min()-10,e['Caixas/Hora'].max()])
                        ee.add_hline(257)
                        ee.update_layout(height = 350, width = 350)
                        ee.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 10.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Keitt'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 10
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]

                        f = padrao_embaldeiras_palmer_6.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        f = f.reset_index()
                        f['mean'] = round(f['mean'],0)
                        f = f.rename(columns = {'mean':'Caixas/Hora'})
                        f['Calibre'] = 10.0
                        f['Calibre'] = f['Calibre'].astype(str)
                        f['ID_PESSOA'] = f['ID_PESSOA'].astype(str)
                        media_f = f['Caixas/Hora'].mean()
                        st.session_state.media_f = media_f
                        ff = px.bar(f,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Keitt - Calibre 10',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        ff.update_yaxes(range = [f['Caixas/Hora'].min()-10,f['Caixas/Hora'].max()])
                        ff.add_hline(261)
                        ff.update_layout(height = 350, width = 350)
                        ff.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 12.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Keitt'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 12
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_7 = padrao_embaldeiras_palmer_6[~padrao_embaldeiras_palmer_6.ID_PESSOA.isin(f['ID_PESSOA'])]

                        
                        g = padrao_embaldeiras_palmer_7.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        g = g.reset_index()
                        g['mean'] = round(g['mean'],0)
                        g = g.rename(columns = {'mean':'Caixas/Hora'})
                        g['Calibre'] = 12.0
                        g['Calibre'] = g['Calibre'].astype(str)
                        g['ID_PESSOA'] = g['ID_PESSOA'].astype(str)
                        media_g = g['Caixas/Hora'].mean()
                        st.session_state.media_g = media_g
                        gg = px.bar(g,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Keitt - Calibre 12' ,hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        gg.update_yaxes(range = [g['Caixas/Hora'].min()-10,g['Caixas/Hora'].max()])
                        gg.add_hline(253)
                        gg.update_layout(height = 350, width = 350)
                        gg.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 14.0:

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Keitt'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 14
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        h = padrao_embaldeiras_palmer.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(20)
                        h = h.reset_index()
                        h['mean'] = round(h['mean'],0)
                        h = h.rename(columns = {'mean':'Caixas/Hora'})
                        h['Calibre'] = 14.0
                        h['Calibre'] = h['Calibre'].astype(str)
                        h['ID_PESSOA'] = h['ID_PESSOA'].astype(str)
                        media_h = h['Caixas/Hora'].mean()
                        st.session_state.media_h = media_h
                        hh = px.bar(h,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Keitt - Calibre 14',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl )
                        hh.update_yaxes(range = [h['Caixas/Hora'].min()-10,h['Caixas/Hora'].max()])
                        hh.update_layout(height = 350, width = 350)
                        hh.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                elif elem in Layout_linha_9['Calibre'] and (variedade == 'Tommy Atkins' or variedade == 'Osteen'):

                    resultDict[elem] = True

                    aaa = Layout_linha_9.groupby(['Calibre'])['Embaladeiras_1'].sum()
                    aaa = aaa.reset_index()

                    bbb = Layout_linha_9.groupby(['Calibre2'])['Embaladeiras_2'].sum()
                    bbb = bbb.reset_index()
                    bbb = bbb.rename(columns={'Calibre2':'Calibre', 'Embaladeiras_2':'Embaladeiras_1'})

                    ccc = pd.concat((aaa,bbb))
                    ccc['Calibre'] = ccc['Calibre'].replace(' ','0')
                    ccc['Calibre'] = ccc['Calibre'].astype(float)
                    ccc = ccc.groupby(['Calibre'])['Embaladeiras_1'].sum()
                    ccc = ccc.reset_index()

                    if elem == 5.0:

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Tommy Atkins'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 5
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        a = padrao_embaldeiras_palmer.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(20)
                        a = a.reset_index()
                        a['mean'] = round(a['mean'],0)
                        a = a.rename(columns = {'mean':'Caixas/Hora'})
                        a['Calibre'] = 5.0
                        a['Calibre'] = a['Calibre'].astype(str)
                        a['ID_PESSOA'] = a['ID_PESSOA'].astype(str)

                        media_a = a['Caixas/Hora'].mean()
                        st.session_state.media_a = media_a
                        aa = px.bar(a,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Tommy Atkins - Calibre 5',hover_name = 'PESSOA', color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        aa.update_yaxes(range = [a['Caixas/Hora'].min()-10,a['Caixas/Hora'].max()])
                        aa.add_hline(235)
                        aa.update_layout(height = 350, width = 350)
                        aa.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 6.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Tommy Atkins'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 6
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)
                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(a['ID_PESSOA'])]

                        b = padrao_embaldeiras_palmer_2.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        b = b.reset_index()
                        b['mean'] = round(b['mean'],0)
                        b = b.rename(columns = {'mean':'Caixas/Hora'})
                        b['Calibre'] = 6.0
                        b['Calibre'] = b['Calibre'].astype(str)
                        b['ID_PESSOA'] = b['ID_PESSOA'].astype(str)
                        media_b = b['Caixas/Hora'].mean()
                        st.session_state.media_b = media_b

                        bb = px.bar(b,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Tommy Atkins - Calibre 6',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        bb.update_yaxes(range = [b['Caixas/Hora'].min()-10,b['Caixas/Hora'].max()])
                        bb.add_hline(178)
                        bb.update_layout(height = 350, width = 350)
                        bb.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 7.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Tommy Atkins'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 7
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)
                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        c = padrao_embaldeiras_palmer_3.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        c = c.reset_index()
                        c['mean'] = round(c['mean'],0)
                        c = c.rename(columns = {'mean':'Caixas/Hora'})
                        c['Calibre'] = 7.0
                        c['Calibre'] = c['Calibre'].astype(str)
                        c['ID_PESSOA'] = c['ID_PESSOA'].astype(str)
                        media_c = c['Caixas/Hora'].mean()
                        st.session_state.media_c = media_c

                        cc = px.bar(c,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Tommy Atkins - Calibre 7', hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        cc.update_yaxes(range = [c['Caixas/Hora'].min()-10,c['Caixas/Hora'].max()])
                        cc.add_hline(185)
                        cc.update_layout(height = 350, width = 350)
                        cc.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 8.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Tommy Atkins'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 8
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        d = padrao_embaldeiras_palmer_4.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        d = d.reset_index()
                        d['mean'] = round(d['mean'],0)
                        d = d.rename(columns = {'mean':'Caixas/Hora'})
                        d['Calibre'] = 8.0
                        d['Calibre'] = d['Calibre'].astype(str)
                        d['ID_PESSOA'] = d['ID_PESSOA'].astype(str)

                        media_d = d['Caixas/Hora'].mean()
                        st.session_state.media_d = media_d
                        
                        dd = px.bar(d,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Tommy Atkins - Calibre 8',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        dd.update_yaxes(range = [d['Caixas/Hora'].min()-10,d['Caixas/Hora'].max()])
                        dd.add_hline(195)
                        dd.update_layout(height = 350, width = 350)
                        dd.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 9.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Tommy Atkins'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 9
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        e = padrao_embaldeiras_palmer_5.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        e = e.reset_index()
                        e['mean'] = round(e['mean'],0)
                        e = e.rename(columns = {'mean':'Caixas/Hora'})
                        e['Calibre'] = 9.0
                        e['Calibre'] = e['Calibre'].astype(str)
                        e['ID_PESSOA'] = e['ID_PESSOA'].astype(str)

                        media_e = e['Caixas/Hora'].mean()
                        st.session_state.media_e = media_e

                        ee = px.bar(e,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Tommy Atkins - Calibre 9',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        ee.update_yaxes(range = [e['Caixas/Hora'].min()-10,e['Caixas/Hora'].max()])
                        ee.add_hline(154)
                        ee.update_layout(height = 350, width = 350)
                        ee.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 10.0:
                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)

                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)

                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Tommy Atkins'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 10
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]

                        f = padrao_embaldeiras_palmer_6.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        f = f.reset_index()
                        f['mean'] = round(f['mean'],0)
                        f = f.rename(columns = {'mean':'Caixas/Hora'})
                        f['Calibre'] = 10.0
                        f['Calibre'] = f['Calibre'].astype(str)
                        f['ID_PESSOA'] = f['ID_PESSOA'].astype(str)

                        media_f = f['Caixas/Hora'].mean()
                        st.session_state.media_f = media_f

                        ff = px.bar(f,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Tommy Atkins - Calibre 10',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        ff.update_yaxes(range = [f['Caixas/Hora'].min()-10,f['Caixas/Hora'].max()])
                        ff.add_hline(144)
                        ff.update_layout(height = 350, width = 350)
                        ff.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 12.0:

                        kl1 = ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0]
                        kl1 = round(kl1,0)
                        
                        if kl1 == 0:
                            kl = ceil(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0])
                        elif kl1 > 0: 
                            kl = round(ccc.loc[ccc.Calibre== elem,'Embaladeiras_1'].values[0],0)
                            kl = kl.astype(int)
                        
                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Tommy Atkins'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 12
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]

                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]

                        padrao_embaldeiras_palmer_7 = padrao_embaldeiras_palmer_6[~padrao_embaldeiras_palmer_6.ID_PESSOA.isin(f['ID_PESSOA'])]

                        g = padrao_embaldeiras_palmer_7.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(kl)
                        g = g.reset_index()
                        g['mean'] = round(g['mean'],0)
                        g = g.rename(columns = {'mean':'Caixas/Hora'})
                        g['Calibre'] = 12.0
                        g['Calibre'] = g['Calibre'].astype(str)
                        g['ID_PESSOA'] = g['ID_PESSOA'].astype(str)

                        media_g = g['Caixas/Hora'].mean()
                        st.session_state.media_g = media_g

                        gg = px.bar(g,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Tommy Atkins  - Calibre 12',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        gg.update_yaxes(range = [g['Caixas/Hora'].min()-10,g['Caixas/Hora'].max()])
                        gg.add_hline(158)
                        gg.update_layout(height = 350, width = 350)
                        gg.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    elif elem == 14.0:

                        
                        filtro_variedade = padrao_embaldeiras['VARIEDADE'] == 'Tommy Atkins'
                        padrao_embaldeiras_palmer = padrao_embaldeiras[filtro_variedade]

                        filtro_calibre = padrao_embaldeiras['CALIBRE'] == 14
                        padrao_embaldeiras_palmer = padrao_embaldeiras_palmer[filtro_calibre]
                        padrao_embaldeiras_palmer['ID_PESSOA'] = padrao_embaldeiras_palmer['ID_PESSOA'].astype(str)

                        padrao_embaldeiras_palmer_2 = padrao_embaldeiras_palmer[~padrao_embaldeiras_palmer.ID_PESSOA.isin(b['ID_PESSOA'])]
                        padrao_embaldeiras_palmer_3 = padrao_embaldeiras_palmer_2[~padrao_embaldeiras_palmer_2.ID_PESSOA.isin(a['ID_PESSOA'])]
                        padrao_embaldeiras_palmer_4 = padrao_embaldeiras_palmer_3[~padrao_embaldeiras_palmer_3.ID_PESSOA.isin(c['ID_PESSOA'])]
                        padrao_embaldeiras_palmer_5 = padrao_embaldeiras_palmer_4[~padrao_embaldeiras_palmer_4.ID_PESSOA.isin(d['ID_PESSOA'])]
                        padrao_embaldeiras_palmer_6 = padrao_embaldeiras_palmer_5[~padrao_embaldeiras_palmer_5.ID_PESSOA.isin(e['ID_PESSOA'])]
                        padrao_embaldeiras_palmer_7 = padrao_embaldeiras_palmer_6[~padrao_embaldeiras_palmer_6.ID_PESSOA.isin(f['ID_PESSOA'])]
                        padrao_embaldeiras_palmer_8 = padrao_embaldeiras_palmer_7[~padrao_embaldeiras_palmer_7.ID_PESSOA.isin(g['ID_PESSOA'])]

                        h = padrao_embaldeiras_palmer.groupby(['ID_PESSOA','PESSOA'])['mean'].max().sort_values(ascending=False).head(20)
                        h = h.reset_index()
                        h['mean'] = round(h['mean'],0)
                        h = h.rename(columns = {'mean':'Caixas/Hora'})
                        h['Calibre'] = 14.0
                        h['Calibre'] = h['Calibre'].astype(str)
                        h['ID_PESSOA'] = h['ID_PESSOA'].astype(str)

                        media_h = h['Caixas/Hora'].mean()
                        st.session_state.media_h = media_h

                        hh = px.bar(h,y = 'Caixas/Hora', color = 'ID_PESSOA', title = 'Tommy Atkins - Calibre 14',hover_name = 'PESSOA',color_discrete_sequence= px.colors.sequential.Aggrnyl)
                        hh.update_yaxes(range = [h['Caixas/Hora'].min()-10,h['Caixas/Hora'].max()])
                        hh.add_hline(90)
                        hh.update_layout(height = 350, width = 350)
                        hh.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                else:
                    resultDict[elem] = False

            return colu1.write(aa), colu1.write(bb), colu2.write(cc), colu2.write(dd), colu3.write(ee), colu3.write(ff), colu4.write(gg), colu4.write(hh)

        result = check_valores(Layout_linha_9, [5.0,6.0,7.0,8.0,9.0,10.0,12.0,14.0])

        media_a = st.session_state.media_a
        media_b = st.session_state.media_b
        media_c = st.session_state.media_c
        media_d = st.session_state.media_d
        media_e = st.session_state.media_e
        media_f = st.session_state.media_f
        media_g = st.session_state.media_g
        media_h = st.session_state.media_h

    ###################### ATRIBUINDO NOVO RITMO  E PRODUTIVIDADE DAS EMBALADEIRAS INDICADAS ######################
        def ritmo(b):
            if b['Calibre'] == 5:
                return media_a
            elif b['Calibre'] == 6:
                return media_b
            elif b['Calibre'] == 7:
                return media_c
            elif b['Calibre'] == 8:
                return media_d
            elif b['Calibre'] == 9:
                return media_e
            elif b['Calibre'] == 10:
                return media_f
            elif b['Calibre'] == 12:
                return media_g
            elif b['Calibre'] == 14:
                return media_h
            else:
                return 'NADA'
        b['Ritmo_embaladeira'] = b.apply(ritmo, axis = 1) 

        b, ton_horas_embaladeiras = ritmos_de_b(b, produtividade_embaladeira, embaladeira)


    ############## EXIBIÇÃO ####################
        ################### BARRA EMBALADEIRAS POR LINHA ###############


        with col3:
            Layout_linha_9 = Layout_linha_9.fillna(' ')
            Layout_linha_9['Qualidade'] = Layout_linha_9['Qualidade'].astype(str)
            Layout_linha_9['Qualidade2'] = Layout_linha_9['Qualidade2'].astype(str)
            Layout_linha_9['Calibre - Qualidade'] = Layout_linha_9['Calibre'] + '-' +Layout_linha_9['Qualidade'] + ' '+ '/' + ' ' + Layout_linha_9['Calibre2'] + '-' + Layout_linha_9['Qualidade2']
            Layout_linha_9['Embaladeiras'] = round(Layout_linha_9['Embaladeiras'],1)

            st.error('##### Embaladeiras por linha de embalagem:')

            fig4 = px.bar(Layout_linha_9, x = 'Linha', y = 'Embaladeiras', color = 'Calibre - Qualidade', text = 'Embaladeiras',color_discrete_sequence= px.colors.sequential.Oranges, 
            category_orders={"Calibre":['5.0','6.0','7.0','8.0','9.0','10.0','12.0','14.0']}, hover_name = 'Linha')
            fig4.update_layout(height = 450, width = 550, uniformtext_minsize=10, uniformtext_mode='show', font = dict(size = 15))
            fig4.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

            st.plotly_chart(fig4)

        ################################ PIZZA DISTRIBUIÇÃO ########################################
        with col1:
            import plotly.graph_objects as go

            b['Calibre Name'] = b['Calibre'].astype(str)
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
            b['Calibre'] = b.apply(rename_b, axis = 1)
    ##################################### CALCULO DA QUA


            c = round(b['Percentual'],2)
            st.error('##### Concentração de calibres:')

            fig = go.Figure(data=[go.Pie(labels = b['Calibre Name'], values = b['Percentual'], marker_colors = px.colors.sequential.Oranges ,hole = .35, pull=0.01)])
            fig.update_traces(textinfo='label+percent', textfont_size=15, textposition="inside", marker=dict(line = dict(color = '#000000', width = 1)))
            fig.update_layout(height = 450, width = 450, font = dict(size = 15))
            
            st.plotly_chart(fig)
            
        ################################ BARRA EMBALADEIRAS POR CALIBRE ########################################
        with col2:
            aaa = Layout_linha_9.groupby(['Calibre'])['Embaladeiras_1'].sum()
            aaa = aaa.reset_index()

            bbb = Layout_linha_9.groupby(['Calibre2'])['Embaladeiras_2'].sum()
            bbb = bbb.reset_index()
            bbb = bbb.rename(columns={'Calibre2':'Calibre', 'Embaladeiras_2':'Embaladeiras_1'})

            ccc = pd.concat((aaa,bbb))
            ccc['Calibre'] = ccc['Calibre'].replace(' ',0)

            drop_2 = ccc[ccc['Calibre'] == 0 ].index
            ccc2 = ccc.drop(drop_2, inplace = True)
            ccc['Embaladeiras_1'] = round(ccc['Embaladeiras_1'],1)
        
            st.error('##### Quantidade de embaladeiras por calibre:')

            fig = px.bar(ccc, y = 'Calibre', x = 'Embaladeiras_1', color = 'Calibre',
            category_orders = {'Calibre':['2.0','5.0','6.0','7.0','8.0','9.0','10.0','12.0','14.0']}, text = 'Embaladeiras_1', color_discrete_sequence= px.colors.sequential.Oranges)
            fig.update_layout(height = 450, width = 500,uniformtext_minsize=8, uniformtext_mode='show', font = dict(size = 15))
            fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
            fig

        ################### CALCULO E EXIBIÇÃO DA NOVA CAPACIDADE DAS EMBALADEIRAS SELECIONADAS ####################################

        conta_delta = round(((100 * ton_horas_embaladeiras) / ton_horas) - 100,1)
        conta_delta2 = str(conta_delta) + ' ' + '%'

        col5x.metric(label="Recomendação (t/h)", value= ton_horas_embaladeiras, delta= conta_delta2)
        st.info('### ER atual vs ER embaladeiras selecionadas')

        dataframe = b[['Calibre Name','Percentual','Caixas_total','Ritmo','Horas_4kg','Ritmo_embaladeira','Horas_4kg_embaladeiras']]
        
        dataframe.rename(columns = {'Ritmo':'Ritmo Atual','Ritmo_embaladeira':'Ritmo Embaladeiras',
                                    'Horas_4kg_embaladeiras':'Horas Embaladeiras','Caixas_total':'Total de caixas',
                                    'Horas_4kg':'Horas Atual','Calibre Name':'Calibre'}, inplace = True)
        dataframe['Controle'] = controle2
        dataframe

        st.download_button( label = 'Baixar Planilha',data = dataframe.to_csv(), mime = 'text/csv')

if selected == 'Previsão e Histórico':

    from PIL import Image
    img = Image.open('agrodn.png')
    newsize = (380,110)
    img2 = img.resize(newsize)

        ########## JANELA LATERAL ##########

    st.sidebar.image(img2, use_column_width=True)
    st.sidebar.title('Menu')
    st.sidebar.markdown('Escolha a informação para visualizar:')



    pagina_selecionada = st.sidebar.radio('', ['Histórico dos talhões','Previsão de Calibres','Matéria Seca e Maturação'])




    if pagina_selecionada == 'Histórico dos talhões':

        @st.experimental_memo
        def criando_gg(allow_output_mutation=True):
            data = requests.get("http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.DXDW_HISTORICO_CALIBRES")
            json_data = data.json()
            df_piv_2=pd.json_normalize(json_data)
            df_piv_2 = pd.DataFrame.from_dict(df_piv_2)
            dataset = pd.DataFrame(df_piv_2)
            return dataset
        dataset = criando_gg()

        # data = requests.get("http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.DXDW_HISTORICO_CALIBRES")
        # json_data = data.json()
        # df_piv_2=pd.json_normalize(json_data)
        # df_piv_2 = pd.DataFrame.from_dict(df_piv_2)
        # dataset = pd.DataFrame(df_piv_2)

        filtro_calibre = dataset['VALOR_CALIBRE'] != 'CALIBRE_11'
        dataset = dataset[filtro_calibre]

        filtro_calibre2 = dataset['VALOR_CALIBRE'] != 'CALIBRE_13'
        dataset = dataset[filtro_calibre2]

        dataset['CALIBRE'] = dataset['CALIBRE'] * 100
        
    ###### FAZENDO O FILTRO DE TALHAO

        dd = dataset.groupby('TALH_ST_DESCRICAO').SAFRA_ST_CODIGO.value_counts()
        ee = pd.DataFrame(dd)
        ee = ee.drop(columns = ['SAFRA_ST_CODIGO'])
        ee = ee.reset_index()
        ee = ee.drop(columns = ['SAFRA_ST_CODIGO'])
        lista_talhoes = ee

        st.success("#### Histórico por controle")
        coll1, coll2,coll3, coll4, coll5, coll6 = st.columns([1,1,1,1,1,1])

        input_talhao = coll3.selectbox('Escolha um talhão:', lista_talhoes, key = 'Escolha de talhao')
        filtro_talhao = dataset['TALH_ST_DESCRICAO'] == input_talhao
        dataset_talhao = dataset[filtro_talhao]

        dataset['ORDEM'].value_counts()
    ###### FAZENDO O FILTRO DE ORDEM DO CONTROLE



        ff = dataset_talhao.groupby('ORDEM').CPROC_IN_CODIGO.value_counts()
        gg = pd.DataFrame(ff)
        gg = gg.drop(columns = ['CPROC_IN_CODIGO'])
        gg = gg.reset_index()
        gg = gg.drop(columns = ['CPROC_IN_CODIGO'])
        lista_de_ordem = gg

        
        input_ordem = coll4.selectbox('Escolha a ordem do controle:', lista_de_ordem, key = 'Escolha uma ordem')
        filtro_ordem = dataset_talhao['ORDEM'] == input_ordem
        dataset_talhao_ordem = dataset_talhao[filtro_ordem]

        filtro_max = dataset_talhao['ORDEM'] == dataset_talhao['ORDEM'].max()
        dataset_talhao_ordem2 = dataset_talhao[filtro_max]

        data_dataset_talhao_ordem2 = dataset_talhao_ordem2['DATA_EMBALAGEM'].iloc[0]
        controle_dataset_talhao_ordem2 = dataset_talhao_ordem2['CPROC_IN_CODIGO'].iloc[0]

        data_dataset_talhao_ordem = dataset_talhao_ordem['DATA_EMBALAGEM'].iloc[0]
        controle_dataset_talhao_ordem = dataset_talhao_ordem['CPROC_IN_CODIGO'].iloc[0]

        coluna1, coluna2, coluna3,coluna4 = st.columns([0.1,1,1,0.1])
        col1,col2 = st.columns([1,0.000001])


        coluna2.info(f'#### Controle mais recente: {controle_dataset_talhao_ordem2} \n Embalagem: {data_dataset_talhao_ordem2}')
        fig = px.bar(dataset_talhao_ordem2, x = 'VALOR_CALIBRE',hover_name = 'CPROC_IN_CODIGO', y = 'CALIBRE', color = 'VALOR_CALIBRE', text = round(dataset_talhao_ordem2['CALIBRE']))
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
        coluna2.plotly_chart(fig)
        coluna2.download_button( label = 'Baixar Controle mais recente (csv)',data = dataset_talhao_ordem2.to_csv(), mime = 'text/csv')

        coluna3.info(f'#### Controle: {controle_dataset_talhao_ordem} - Ordem: {input_ordem} \n Embalagem: {data_dataset_talhao_ordem}')
        fig = px.bar(dataset_talhao_ordem, x = 'VALOR_CALIBRE',hover_name = 'CPROC_IN_CODIGO',  y = 'CALIBRE', color = 'VALOR_CALIBRE', text = round(dataset_talhao_ordem['CALIBRE']))
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
        coluna3.plotly_chart(fig)
        coluna3.download_button( label = 'Baixar Ordem selecionada (csv)',data = dataset_talhao_ordem.to_csv(), mime = 'text/csv')

        col1.info(f'#### Histórico de todos os controles (M22) do talhão: {input_talhao}')
        fig = px.bar(dataset_talhao, x = 'VALOR_CALIBRE',hover_name = 'CPROC_IN_CODIGO', y = 'CALIBRE', facet_col = 'ORDEM', color = 'VALOR_CALIBRE', title = 'Todos', text = round(dataset_talhao['CALIBRE']))
        fig.update_traces(textfont_size=12, textangle=0, textposition="inside", marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
        fig.update_layout(height = 400, width = 1600)
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("ORDEM=", "")))
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("CALIBRE_", "")))
        col1.plotly_chart(fig)
        col1.download_button( label = 'Baixar Histórico completo (csv)',data = dataset_talhao.to_csv(), mime = 'text/csv')

    if pagina_selecionada == 'Previsão de Calibres':
        from tkinter import filedialog
        from turtle import filling
        import streamlit as st
        import pandas as pd
        import numpy as np
        import plotly.graph_objects as go
        import plotly.express as px
        import pickle
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots



        ### QUATRO INPUTS:

        ### PERCENTUAL MAIS RECENTE DAQUELE CALIBRE AMOSTRADO 
        ### MEDIA DO PESO DAQUELE CALIBRE NA AMOSTRAGEM MAIS RECENTE
        ### DIAS ATE A EMBALAGEM DA AMOSTRAGEM MAIS RECENTE
        ### ORDEM DO CONTROLE


        @st.experimental_memo
        def get_data():
            url = 'http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.DXDW_HISTORICO_CALIBRES'
            dataframe = pd.read_json(url)
            dataframe.isnull().sum()
            dataframe = dataframe.dropna()
            return dataframe
        dataframe = get_data()

        filtro_cal = dataframe['VALOR_CALIBRE'] != 'CALIBRE_11'
        dataframe = dataframe[filtro_cal]

        filtro_cal = dataframe['VALOR_CALIBRE'] != 'CALIBRE_13'
        dataframe = dataframe[filtro_cal]

        filtro_cal = dataframe['VALOR_CALIBRE'] != 'CALIBRE_4'
        dataframe = dataframe[filtro_cal]

        dataframe['talhao_calibre'] =   dataframe['VALOR_CALIBRE']  + dataframe['TALH_ST_DESCRICAO'] 



        ### TENHO QUE JUNTAR AS INFOS COM O 'dataframe' 

        ###procv de talhao calibre


        @st.experimental_memo
        def get_data2():
            url_amostragem = 'http://sia:3000/backend/busca_generica/buscaGenerica?view=MGAGR.AGR_VW_DX_CALIBRES_CAMPO%20WHERE%201=1%20AND%20SYSDATE%20-%20to_date(DATA,%27yyyy-mm-dd%27)%20%3C=%2060%20AND%20DATA%20IS%20NOT%20NULL'
            df_amostragem_1 = pd.read_json(url_amostragem)
            return df_amostragem_1

        df_amostragem_1 = get_data2()


        dados = df_amostragem_1.groupby(['TALHAO','CALIBRE'])['DATA'].max()
        dados2 = pd.DataFrame(dados)
        dados2 = dados2.reset_index()

        dados2['coluna_merg'] = dados2['TALHAO'] + dados2['CALIBRE'] + dados2['DATA']
        df_amostragem_1['coluna_merge'] = df_amostragem_1['TALHAO']+ df_amostragem_1['CALIBRE']+df_amostragem_1['DATA']
        dataset_merge = df_amostragem_1.merge(dados2, left_on = 'coluna_merge', right_on = 'coluna_merg')


        df_amostragem_2 = dataset_merge[['TALHAO_x','FRUTO','PESO','CALIBRE_x']]

        df_amostragem_1_piv = pd.pivot_table(dataset_merge, values = ['FRUTO','PESO'], index=['CALIBRE_x','TALHAO_x'],
                        aggfunc={'FRUTO': np.sum,
                                    'PESO': np.mean})
        df_amostragem_1_piv = df_amostragem_1_piv.reset_index()
        
        amostragem_percents = df_amostragem_1_piv.groupby(['TALHAO_x','CALIBRE_x'])['FRUTO'].sum() / df_amostragem_1_piv.groupby(['TALHAO_x'])['FRUTO'].sum() 
        amostragem_percents = pd.DataFrame(amostragem_percents)
        amostragem_percents = amostragem_percents.reset_index()




        amostragem_percents['VALOR_CALIBRE'] = 'CALIBRE_' + amostragem_percents['CALIBRE_x']
        amostragem_percents['talhao_calibre'] = amostragem_percents['VALOR_CALIBRE'] + amostragem_percents['TALHAO_x']





        df_amostragem_1_piv['VALOR_CALIBRE'] = 'CALIBRE_' + df_amostragem_1_piv['CALIBRE_x']
        df_amostragem_1_piv['talhao_calibre'] = df_amostragem_1_piv['VALOR_CALIBRE'] + df_amostragem_1_piv['TALHAO_x']
        



        dataset_merge1 = dataframe.merge(amostragem_percents, left_on = 'talhao_calibre', right_on = 'talhao_calibre')
        dataset_merge2 = dataset_merge1.merge(df_amostragem_1_piv, left_on = 'talhao_calibre', right_on = 'talhao_calibre')

        #dataframe
        #dataset_merge2

        dataset_merge3 = dataset_merge2[['TALH_ST_DESCRICAO','CPROC_IN_CODIGO', 
        'DATA_EMBALAGEM', 'ORDEM','VALOR_CALIBRE_x','CALIBRE','talhao_calibre','FRUTO_x','PESO','VARIEDADE']]

        dataset_merge3.rename(columns = {'FRUTO_x':'Perc_cal_amostr'}, inplace = True)
        
        ### AQUI JA TENHO O PESO E O PERCENTUAL DO CALIBRE E A ORDEM

        ### FALTA AGORA OS DIAS DA AMOSTRAGEM ATE EMBALAGEM
        dados2['VALOR_CALIBRE'] = 'CALIBRE_' + dados2['CALIBRE']

        dados2['talhao_calibre'] = dados2['VALOR_CALIBRE'] + dados2['TALHAO']


        dataset_merge4 = dataset_merge3.merge(dados2, left_on = 'talhao_calibre', right_on = 'talhao_calibre')

        dataset_merge4 = dataset_merge4[['TALH_ST_DESCRICAO','CPROC_IN_CODIGO', 
        'DATA_EMBALAGEM', 'ORDEM','VALOR_CALIBRE_x','CALIBRE_x','talhao_calibre','Perc_cal_amostr','PESO','DATA','VARIEDADE']]
        dataset_merge4.rename(columns = {'VALOR_CALIBRE_x':'REAL','DATA':'DATA_AMOSTRAGEM'}, inplace = True)


        from datetime import datetime, timedelta
        dataset_merge4['DATA_EMBALAGEM'] = pd.to_datetime(dataset_merge4['DATA_EMBALAGEM'], format="%Y/%m/%d")
        dataset_merge4['DATA_AMOSTRAGEM'] = pd.to_datetime(dataset_merge4['DATA_AMOSTRAGEM'], format="%Y/%m/%d")


        dataset_merge4['DIAS_ATE_EMBALA'] = (dataset_merge4['DATA_EMBALAGEM'] - dataset_merge4['DATA_AMOSTRAGEM'])
        dataset_merge4['DIAS_ATE_EMBALA'] = dataset_merge4['DIAS_ATE_EMBALA'] / np.timedelta64(1,'D')
        dataset_merge4['DIAS_ATE_EMBALA'] = dataset_merge4['DIAS_ATE_EMBALA'].astype(int)



       # dataset_merge4 = dataset_merge4[dataset_merge4['ORDEM'].between(1, 20)]
        #dataset_merge4 = dataset_merge4[dataset_merge4['Perc_cal_amostr'].between(0, 0.30)]
        dataset_merge4 = dataset_merge4[dataset_merge4['DIAS_ATE_EMBALA'].between(5, 30)]
        # dataset_merge4 = dataset_merge4[dataset_merge4['PESO'].between(0, 1000)]

        dataset_merge4 = dataset_merge4[dataset_merge4['CALIBRE_x'].between(0, 0.40)]

        # filtro_keitt = dataset_merge4['VARIEDADE'] == 'KEITT'
        # dataset_merge4_keitt = dataset_merge4[filtro_keitt]

        # dataset_merge4_keitt





        dataframe_final = dataset_merge4[['TALH_ST_DESCRICAO','CPROC_IN_CODIGO','DATA_EMBALAGEM','DATA_AMOSTRAGEM','REAL','CALIBRE_x','ORDEM','Perc_cal_amostr','DIAS_ATE_EMBALA','PESO','VARIEDADE']]



       # dataset_merge4 = dataset_merge4[dataset_merge4['ORDEM'].between(1, 20)]
       # dataset_merge4 = dataset_merge4[dataset_merge4['Perc_cal_amostr'].between(0, 0.60)]
        # dataset_merge4 = dataset_merge4[dataset_merge4['DIAS_ATE_EMBALA'].between(5, 30)]
      #  dataset_merge5 = dataset_merge4[dataset_merge4['PESO'].between(0, 1000)]

        #dataframe_final = dataframe_final[dataframe_final['CALIBRE_x'].between(0, 0.6)]


        dataframe_final['ERROR_AMOSTRA'] = abs(dataframe_final['Perc_cal_amostr'] - dataframe_final['CALIBRE_x'])


        dados_model = dataframe_final[['ORDEM','Perc_cal_amostr','DIAS_ATE_EMBALA','PESO']]
        

        with open('Modelo_final.pkl', 'rb') as f:
            modelo = pickle.load(f)

        pred_new = modelo.predict(dados_model)

     
        dataframe_final['Pred'] = pred_new

        def correcao_calibre_6_keitt(dataframe_final):
             if (dataframe_final['VARIEDADE'] == 'KEITT' and dataframe_final['REAL'] == 'CALIBRE_6') and (dataframe_final['Pred'] <= 0.20):
                        return 0.26
             else:
                return dataframe_final['Pred']

        dataframe_final['Pred'] = dataframe_final.apply(correcao_calibre_6_keitt, axis  = 1)

        def correcao_calibre_7_keitt(dataframe_final):
            if (dataframe_final['VARIEDADE'] == 'KEITT' and dataframe_final['REAL'] == 'CALIBRE_7') and (dataframe_final['Pred'] <= 0.10):
                    return 0.24
            else:
                return dataframe_final['Pred']

        dataframe_final['Pred'] = dataframe_final.apply(correcao_calibre_7_keitt, axis  = 1)


        def correcao_calibre_6_kent(dataframe_final):
             if (dataframe_final['VARIEDADE'] == 'KENT' and dataframe_final['REAL'] == 'CALIBRE_6') and (dataframe_final['Pred'] <= 0.20):
                        return 0.30
             else:
                return dataframe_final['Pred']

        dataframe_final['Pred'] = dataframe_final.apply(correcao_calibre_6_kent, axis  = 1)

        def correcao_calibre_8_kent(dataframe_final):
             if (dataframe_final['VARIEDADE'] == 'KENT' and dataframe_final['REAL'] == 'CALIBRE_8') and (dataframe_final['Pred'] >= 0.20):
                        return 0.12
             else:
                return dataframe_final['Pred']

        dataframe_final['Pred'] = dataframe_final.apply(correcao_calibre_8_kent, axis  = 1)

        def correcao_calibre_5_kent(dataframe_final):
             if (dataframe_final['VARIEDADE'] == 'KENT' and dataframe_final['REAL'] == 'CALIBRE_5') and (dataframe_final['Pred'] >= 0.12):
                        return 0.09
             else:
                return dataframe_final['Pred']

        dataframe_final['Pred'] = dataframe_final.apply(correcao_calibre_5_kent, axis  = 1)

        def correcao_calibre_10_kent(dataframe_final):
             if (dataframe_final['VARIEDADE'] == 'KENT' and dataframe_final['REAL'] == 'CALIBRE_10') and (dataframe_final['Pred'] >= 0.10):
                        return 0.05
             else:
                return dataframe_final['Pred']

        dataframe_final['Pred'] = dataframe_final.apply(correcao_calibre_10_kent, axis  = 1)

        def correcao_calibre_8_tommy(dataframe_final):
             if (dataframe_final['VARIEDADE'] == 'TOMMY' and dataframe_final['REAL'] == 'CALIBRE_8') and (dataframe_final['Pred'] <= 0.11):
                        return 0.20
             else:
                return dataframe_final['Pred']

        dataframe_final['Pred'] = dataframe_final.apply(correcao_calibre_8_tommy, axis  = 1)

        def correcao_calibre_9_tommy(dataframe_final):
             if (dataframe_final['VARIEDADE'] == 'TOMMY' and dataframe_final['REAL'] == 'CALIBRE_9') and (dataframe_final['Pred'] <= 0.11):
                        return 0.22
             else:
                return dataframe_final['Pred']

        dataframe_final['Pred'] = dataframe_final.apply(correcao_calibre_9_tommy, axis  = 1)



        filtro_palmer = dataframe_final['VARIEDADE'] != 'PALMER'
        dataframe_final = dataframe_final[filtro_palmer]

        filtro_palmer = dataframe_final['VARIEDADE'] != 'OSTEEN'
        dataframe_final = dataframe_final[filtro_palmer]

        filtro_palmer = dataframe_final['VARIEDADE'] != 'OMER'
        dataframe_final = dataframe_final[filtro_palmer]




        dataframe_final['Erro'] =  abs(dataframe_final['CALIBRE_x'] - dataframe_final['Pred'])
        dataframe_final['Erro_neg'] =  dataframe_final['Pred'] - dataframe_final['CALIBRE_x']
        dataframe_final = dataframe_final[dataframe_final['Erro'].between(0, 0.5)]

        def check(dataframe_final):
            if dataframe_final['Erro'] >  0.11:
                return 'ERROU'
            else:
                return 'ACERTOU'

        dataframe_final['Check'] = dataframe_final.apply(check, axis = 1)

        def check(dataframe_final):
            if dataframe_final['ERROR_AMOSTRA'] >  0.11:
                return 'ERROU'
            else:
                return 'ACERTOU'

        dataframe_final['Check Amostra'] = dataframe_final.apply(check, axis = 1)

        ### CRIAR AGR OS ST FILTROS

        cnt = len(dataframe_final['CPROC_IN_CODIGO'].value_counts())

        st.error(f'### Desempenho Geral - Novos dados ({cnt} controles)')

        coluna1, coluna2 = st.columns(2)

        with coluna1:
            st.error('Acurácia com threshold de 10%')
            fig = px.bar(dataframe_final, x = 'REAL', color = 'Check', category_orders = {'REAL':['CALIBRE_5','CALIBRE_6','CALIBRE_7','CALIBRE_8','CALIBRE_9','CALIBRE_10','CALIBRE_12','CALIBRE_14'], 'Check':['ACERTOU','ERROU']})
            st.plotly_chart(fig)


        with coluna2:
            st.error('Probabilidade de erros nas previsões por Calibre')
            # fig = px.bar(dataframe_final, x = 'REAL', color = 'Check Amostra', category_orders = {'REAL':['CALIBRE_5','CALIBRE_6','CALIBRE_7','CALIBRE_8','CALIBRE_9','CALIBRE_10','CALIBRE_12','CALIBRE_14'], 'Check Amostra':['ACERTOU','ERROU']})
            
            # st.plotly_chart(fig)

            fig = px.histogram(dataframe_final, x = 'Erro_neg', color = 'REAL', marginal = 'violin', category_orders = {'REAL':['CALIBRE_5','CALIBRE_6','CALIBRE_7','CALIBRE_8','CALIBRE_9','CALIBRE_10','CALIBRE_12','CALIBRE_14'], 'Check':['ACERTOU','ERROU']})
            fig.add_vline(0.11,line_color = 'red', line_dash="dot",  annotation_text=" + 10 % ", annotation_font_color="red")
            fig.add_vline(-0.11,line_color = 'red', line_dash="dot",  annotation_text=" - 10 % ", annotation_font_color="red")
            fig
            
            st.write("""
            - Os erros para todos os calibres se concentram em torno de zero e dentro da tolerância de 10%:
                - Exceto calibre 5 que ficou em torno de 16%.
            
            """)
            st.write('___')



        coluna1, coluna2 = st.columns(2)


        with coluna1:

            st.info("Percentuais dos totais de percentuais de cada calibre")
            fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

            fig.add_trace(go.Pie(labels=dataframe_final['REAL'] , pull=[0, 0, 0, 0,0, 0.2, 0, 0], marker_colors = px.colors.cyclical.Twilight, values=dataframe_final['Pred'], name="Previsto"),
                        1, 1)
            fig.add_trace(go.Pie(labels=dataframe_final['REAL'], pull=[0, 0, 0, 0,0,0.2, 0, 0, 0], values=dataframe_final['CALIBRE_x'], name="Real"),
                        1, 2)

            # Use `hole` to create a donut-like pie chart
            fig.update_traces(hole=.4, hoverinfo="label+percent+name", marker=dict(line = dict(color = '#000000', width = 1)))
            
            fig.update_layout( 
                # Add annotations in the center of the donut pies.
                annotations=[dict(text='Pred', x=0.17, y=0.5, font_size=20, showarrow=False),
                            dict(text='Real', x=0.80, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig)

        with coluna2:

            st.info("Médias previstas por calibre")

            fig = go.Figure()
            fig.add_trace(go.Histogram(x = dataframe_final['REAL'],  marker_color='darkblue', y = dataframe_final['CALIBRE_x'], histfunc = 'avg',name = 'Real'))

            fig.add_trace(go.Histogram(x = dataframe_final['REAL'],   marker_color='royalblue',y = dataframe_final['Pred'], histfunc = 'avg', name = 'Previsto'))

            # fig.add_trace(go.Histogram(x = dataframe_final['REAL'],   marker_color='green',y = dataframe_final['Perc_cal_amostr'], histfunc = 'avg', name = 'P_AMOS'))

            fig.update_traces(marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

            fig.update_yaxes(range = [0,0.5])

            fig.update_layout( height = 400, width = 650)
            fig.update_xaxes(categoryorder='array', categoryarray= ['CALIBRE_5','CALIBRE_6','CALIBRE_7','CALIBRE_8', 'CALIBRE_9','CALIBRE_10','CALIBRE_12','CALIBRE_14'])

            st.plotly_chart(fig)

            
        coluna1, coluna2 = st.columns([1,0.01])

        with coluna1:

            st.info('Erro do modelo por influência do erro da amostragem')
            fig = go.Figure()

            fig.add_trace(go.Bar(y = dataframe_final['Erro']*100, name = 'Error'))
            fig.add_trace(go.Scatter(y = dataframe_final['ERROR_AMOSTRA']*100, name = 'DIF AMOSTRA'))

            fig.add_hline(10, line_color = 'darkblue', line_dash="dot",  annotation_text=" + 10 % ",annotation_font_color="darkblue")

            fig.update_layout( title = 'Caliber (%) forecasting')
            fig.update_layout(height = 500, width = 1400)
            fig


        coluna1, coluna2 = st.columns([1,0.1])

        st.error('### Análise das previsões nível Talhão:Controle')

        dd = dataframe_final['TALH_ST_DESCRICAO'].value_counts()
        ee = pd.DataFrame(dd)
        ee = ee.drop(columns = ['TALH_ST_DESCRICAO'])
        ee = ee.reset_index()
        lista_talhoes = ee
        st.write('___')
        colu1, colu2, colu3 = st.columns([0.3,0.3,1])

        input_talhao = colu1.selectbox('Escolha um talhão:', lista_talhoes, key = 'Escolha de talhao')


        filtro_talhao = dataframe_final['TALH_ST_DESCRICAO'] == input_talhao
        dataframe_final = dataframe_final[filtro_talhao]




        dd = dataframe_final['CPROC_IN_CODIGO'].value_counts()
        ee = pd.DataFrame(dd)
        ee = ee.drop(columns = ['CPROC_IN_CODIGO'])
        ee = ee.reset_index()
        lista_controles= ee


        input_control = colu2.selectbox('Escolha um controle:', options = lista_controles, key = 'Escolha de controle')



        filtro_control = dataframe_final['CPROC_IN_CODIGO'] == input_control
        dataframe_final = dataframe_final[filtro_control]

        variety = dataframe_final.reset_index()
        variety = variety['VARIEDADE'][0]

        colu3.write(' ')
        colu3.write(' ')
        colu3.write(' ')

        colu3.write(f'Variedade do talhão: {variety}')

        #dataframe_final.query('CPROC_IN_CODIGO in @input_control')

        st.write('___')
        colunaxx, coluna1, colunax, coluna2, colunaxxx  = st.columns([0.01,1,0.1,1,0.1])

        with coluna1:
            
            st.info('Percentuais dos totais de percentuais de cada calibre')

            fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

            fig.add_trace(go.Pie(labels=dataframe_final['REAL'] , pull=[0, 0, 0, 0,0, 0.2, 0, 0], marker_colors = px.colors.cyclical.Twilight, values=dataframe_final['Pred'], name="Previsto"),
                        1, 1)
            fig.add_trace(go.Pie(labels=dataframe_final['REAL'], pull=[0, 0, 0, 0,0,0.2, 0, 0, 0], values=dataframe_final['CALIBRE_x'], name="Real"),
                        1, 2)

            fig.update_traces(hole=.4, hoverinfo="label+percent+name", marker=dict(line = dict(color = '#000000', width = 1)))
            fig.update_layout( height = 400, width = 650,

                annotations=[dict(text='Pred', x=0.17, y=0.5, font_size=20, showarrow=False),
                            dict(text='Real', x=0.82, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig)


        with coluna2:
            
            st.info('Comparativo de médias por calibre')
            fig = go.Figure()
            fig.add_trace(go.Histogram(x = dataframe_final['REAL'],  marker_color='darkblue', y = dataframe_final['CALIBRE_x'], histfunc = 'avg',name = 'Real'))

            fig.add_trace(go.Histogram(x = dataframe_final['REAL'],   marker_color='royalblue',y = dataframe_final['Pred'], histfunc = 'avg', name = 'Previsto'))

            #fig.add_trace(go.Scatter(y = dataframe_final['Check'],   marker_color='royalblue',y = dataframe_final['Pred'], name = 'Check'))

                

            # fig.add_trace(go.Histogram(x = dataframe_final['REAL'],   marker_color='green',y = dataframe_final['Perc_cal_amostr'], histfunc = 'avg', name = 'P_AMOS'))

            fig.update_traces(marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

            fig.update_layout(height = 400, width = 650)
            st.plotly_chart(fig)
            #### TALHAO CACHM 9.4 e controle 932,936,974 o modelo foi melhor que a amostragem
            
        with coluna1:
            st.info('Acurácia no controle com threshold de 10%')


            fig = px.bar(dataframe_final, x = 'REAL', color = 'Check', category_orders = {'REAL':['CALIBRE_5','CALIBRE_6','CALIBRE_7','CALIBRE_8','CALIBRE_9','CALIBRE_10','CALIBRE_12','CALIBRE_14'],'Check':['ACERTOU','ERROU']})
            fig.update_layout(height = 400, width = 500)
            st.plotly_chart(fig)

            

        with coluna2:
            st.info('Caliber (%) forecasting')
            fig = go.Figure()


            fig.add_trace(go.Bar(x =dataframe_final['REAL'] ,y = dataframe_final['Erro']*100, name = 'Error'))

            fig.add_trace(go.Scatter(x =dataframe_final['REAL'] , y = dataframe_final['ERROR_AMOSTRA']*100, name = 'DIF AMOSTRA'))

            fig.add_trace(go.Scatter(x =dataframe_final['REAL'] ,y = dataframe_final['DIAS_ATE_EMBALA'], name = 'DIAS'))

            

            fig.add_hline(11, line_color = 'red', line_dash="dot",  annotation_text=" + 10 % ", annotation_font_color="red")

        
            fig.update_layout(height = 400, width = 650)
            fig
            
        # st.error(""" 
        # - Considerações sobre erros: 
        #     - Modelo erra em situações em que um calibre tem um percentual muito alto para sua característica normal:
        #         - Exemplo: Calibre 6 próximo de 50% ou altos percentuais em calibres que normalmente são 0 ou próximos de zero.
        #     - E também tende a errar mais com o avanço de dias em alguns calibres e quando a amostragem é muito divergente do real;
        #     - Exemplo controle 897 CACH M9.4 onde o calibre 6 teve 53 % e a amostragem do calibre 7 foi bem distante do real;
        #     - Já para o controle 864, que também teve um alto percentual de calibre 6, a amostragem foi feita mais próxima, o que contribuiu para um bom ajuste.
        #     - OBS: Todos esses erros podem ser melhorados por um retreino com uma base maior e direcionamento das amostragens.
        
        # """)


            
    if pagina_selecionada == 'Matéria Seca e Maturação':
        import streamlit as st
        import pickle 
        import pandas as pd

        import plotly.graph_objects as go
        import plotly.express as px



        with open('MATERIA_SECA_MODEL.pkl', 'rb') as f:
            modelo_materia_seca = pickle.load(f)

        with open('MATURACAO_MODEL.pkl', 'rb') as f:
            modelo_maturacao = pickle.load(f)


        col1, col2 = st.columns(2)
        coluna1, coluna2,colunax, coluna3, coluna4  = st.columns([0.5,0.5,0.1,0.5,0.5])



        col1.error('### Previsão: Matéria Seca')

        maturacao = coluna1.slider('MATURAÇÃO', key = 'matu', min_value = 1.0, max_value = 2.0, value = 1.13, step = 0.01)

        materia_seca = coluna2.slider('MATÉRIA SECA', key = 'ms', min_value = 10.0, max_value = 16.0, value = 13.86, step = 0.1)


        dados_pred = [[maturacao, materia_seca]]

        a = modelo_materia_seca.predict(dados_pred)
        b = pd.DataFrame(a)
        b.rename(columns = {0:'MATERIA_SECA_R'}, inplace = True)

        b['VALOR_MAX_PROVAVEL'] = b['MATERIA_SECA_R'] + 0.5
        b['VALOR_MIN_PROVAVEL'] = b['MATERIA_SECA_R'] - 0.5

        colx,COL_, colxx = st.columns([1,0.2,1])
        colx.write('___')
        #colx.info('#### Estimativa MS')

        colx.write(b)

        # fig = go.Figure()

        # fig.add_trace(go.Bar(y = b['MATERIA_SECA_R'], 
        #                     error_y=dict(type='data',
        #                                 array=[0.5]) ))

        # colx.plotly_chart(fig)


        # col1, col2 = st.columns(2)
        # coluna1, coluna2,coluna3, coluna4  = st.columns([1,1,0.5,0.5])




        col2.error('### Previsão de Maturação')

        Distancia_dias = coluna3.slider('DIAS ATÉ COLHEITA', key = 'matu', min_value = 5.0, max_value = 56.0, value = 27.0, step = 1.0)

        maturcao_2 = maturacao

        materia_seca_2 = materia_seca

        materia_seca_min = coluna4.slider('MATÉRIA SECA MIN', key = 'ms', min_value = 10.0, max_value = 14.40, value = 12.48, step = 0.01)


        maturacao_R = b['MATERIA_SECA_R'][0]



        dados_pred_maturacao = [[Distancia_dias, maturcao_2, materia_seca_2,materia_seca_min, maturacao_R ]]

        a2 = modelo_maturacao.predict(dados_pred_maturacao)
        colxx.write('___')
        #colxx.info('#### Estimativa Maturação')

        b = pd.DataFrame(a2)
        b.rename(columns = {0:'MATURACAO'}, inplace = True)

        b['VALOR_MAX_PROVAVEL'] = b['MATURACAO'] + 0.05
        b['VALOR_MIN_PROVAVEL'] = b['MATURACAO'] - 0.1

        colxx.write(b)

        st.error('OBS 1: Os inputs do modelo de MS também são para o de Maturação, mas não o contrário. A MS prevista também é input do modelo de Maturação.')
        st.error('OBS2: Os erros mais prováveis dos dois modelos estão aplicados nos valores de máximo e mínimos de cada target.')
        st.error('OBS3: R² dos dois modelos estão em torno de 52 %. ')

if selected == 'Count Test':

    #if st.button('Iniciar monitoramento'):
    


    conn = sqlite3.connect(r"C:\Users\bernard.collin\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
    cursor = conn.cursor()
    
    df_sql_count = pd.read_sql_query("""SELECT * FROM frutos_count """, conn)
    
    percent_passed = df_sql_count['percent_passed'][0]

    tons_tot = df_sql_count['tons_tot'][0]
    tons_passesed = df_sql_count['tons_passed'][0]

    
    conn.commit()
    conn.close()

    from retrying import retry
    @retry (wait_fixed = 4000, stop_max_attempt_number = 4)
    def get_maf():
        url_percentual_MAF = 'http://sia:3000/backend/maf/percentuaisCalibre'
        dataset_MAF = pd.read_json(url_percentual_MAF)
        return dataset_MAF

    dataset_MAF = get_maf()

    @retry (wait_fixed = 4000, stop_max_attempt_number = 4)
    def get_mega():
        url_percentual_mega = 'http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH'
        dataset_MEGA = pd.read_json(url_percentual_mega)
        return dataset_MEGA

    dataset_MEGA = get_mega()

    controle_MAF = dataset_MAF['CONTROLE_MEGA'][0]
    controle_MEGA = dataset_MEGA['CONTROLE'][0]



    fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = percent_passed,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Processado (%)", 'font': {'size': 24}},
                delta = {'reference': 95, 'increasing': {'color': '#f56e00'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkgreen"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "black",
                    'steps': [{'range': [0, 20], 'color': '#ffab8c'},
                        {'range': [20, 50], 'color': '#ff7d4d'},
                        {'range': [50, 80], 'color': 'orangered'},
                        {'range': [80, 90], 'color': 'red'}],
                    'threshold': {
                        'line': {'color': 'red', 'width': 4},
                        'thickness': 0.75,
                        'value': 95}}))

    fig.update_layout(paper_bgcolor = "snow", font = {'color': 'black', 'family': "Arial"}, height = 400, width = 500)

    col1,col2 = st.columns([1,0.02])
    col1.success(f'## Troca de controle / Controle MEGA: {controle_MEGA} / Controle MAF: {controle_MAF}')
    col1.write('      ')

    coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns([0.2,1,1,1,0.2])
    coluna2.error('### Percentual')
    coluna2.plotly_chart(fig)


    tot_round = round(tons_tot,2)
    passed_round = round(tons_passesed,2)


    tot_str = str(tot_round)
    passed_str = str(passed_round)


    fig22 = go.Figure()
    fig22.add_trace(go.Bar(y = [tons_tot], text =  tot_str, name = 'Toneladas totais', marker_color='orangered'))
    fig22.add_trace(go.Bar(y = [tons_passesed],text = passed_str  ,name = 'Toneladas processadas', marker_color='darkgreen'))
    fig22.update_layout(height = 368, width = 500)
    fig22.update_traces(marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
    coluna3.error('### Toneladas')
    coluna3.plotly_chart(fig22)
    coluna4.error('### Contagem - Real Time')
    coluna4.video('https://youtu.be/SZ30SS4H2Co')
    # https://www.youtube.com/watch?v=RTfwjFwlxqo

    # if percent_passed == 0:
    #     st.info('### Aguarde o próximo controle iniciar...')
        #st.stop()

    time.sleep(50.55)
    st.experimental_rerun()   

if selected == 'Produtividade PH':

    from PIL import Image
    img = Image.open('agrodn.png')
    newsize = (380,110)
    img2 = img.resize(newsize)

        ########## JANELA LATERAL ##########

    st.sidebar.image(img2, use_column_width=True)
    st.sidebar.title('Menu')
    st.sidebar.markdown('Escolha a informação para visualizar:')

    pagina_selecionada = st.sidebar.radio('', ['Produtividade Controle'])

    if pagina_selecionada == 'Produtividade Controle':
        
        
        col1, col2 = st.columns([0.02, 1])
        coluna1, coluna2,coluna3, coluna4 = st.columns([0.2, 1,1,0.2])
        colunas_1, colunas_2, colunas_3, colunas_4 = st.columns([0.02,1,1,1])


        media_mensal_graph = coluna2.empty()
        media_diaria_graph = coluna3.empty()
        controle_graph = col2.empty()


        placeholder6 = col2.empty()
        placeholder1 = coluna2.empty()
        placeholder2 = coluna3.empty()
        placeholder3 = colunas_2.empty()
        placeholder4 = colunas_3.empty()
        placeholder5 = colunas_4.empty()


        start_button = st.empty()
        
        if start_button.button('Iniciar monitoramento',key='start'):

           start_button.empty()
          
           if st.button('Stop',key='stop'):
                pass

           while True:

                media_mensal_graph.success('#### Média mensal ano corrente')
                media_diaria_graph.success('#### Média diária mês corrente')
                controle_graph.success('#### Controle do processo')

                data = requests.get("http://sia:3000/backend/maf/buscarRitmoProducao")
                json_data = data.json()
                df_piv_2=pd.json_normalize(json_data)
                df_piv_2 = pd.DataFrame.from_dict(df_piv_2)
                
                df = pd.DataFrame(df_piv_2)

                df['DATA'] = df['INICIO_PROCESSAMENTO'].str.split('T').str[0]
                df['ANO'] = df['DATA'].str.split('-').str[0]
                df['MES'] = df['DATA'].str.split('-').str[1]
                df['DIA'] = df['DATA'].str.split('-').str[2]
                
        

                df['DATA'] = df['INICIO_PROCESSAMENTO'].str.split('T').str[0]
                df['ANO'] = df['DATA'].str.split('-').str[0]
                df['MES'] = df['DATA'].str.split('-').str[1]
                df['DIA'] = df['DATA'].str.split('-').str[2]
                df = df.dropna()



                def correcao_variedade(df):

                    if df['VARIEDADE'] == 'TOMMY' or df['VARIEDADE'] == 'TONNY' or df['VARIEDADE'] == 'TOOMY' or df['VARIEDADE'] == 'TOOMY ATKINS' or df['VARIEDADE'] == 'TOMMY,'  or df['VARIEDADE'] == 'TOMMY 2' or df['VARIEDADE'] == 'TOMMT' or df['VARIEDADE'] == 'TOMMY01' or df['VARIEDADE'] == 'tommy' or df['VARIEDADE'] == ' TOMMY' or df['VARIEDADE'] == 'TOMMY ' or df['VARIEDADE'] == 'TOMMY ATKINS' or df['VARIEDADE'] == 'TOMMY  ' or df['VARIEDADE'] == '  TOMMY  '  or df['VARIEDADE'] == '  TOMMY':
                        return 'Tommy'
                    
                    elif df['VARIEDADE'] == 'KEITT' or df['VARIEDADE'] == 'KEIT' or df['VARIEDADE'] == 'KEIIT' or df['VARIEDADE'] == 'KEITT.' or df['VARIEDADE'] == 'KEIITT'  or df['VARIEDADE'] == 'KEITT ' or df['VARIEDADE'] == ' KEITT' or df['VARIEDADE'] == 'KEITT  ' or df['VARIEDADE'] == '  KEITT  ' or df['VARIEDADE'] == '  KEITT' or df['VARIEDADE'] == ' KEITT ':
                        return 'Keitt'

                    elif df['VARIEDADE'] == 'OALMER' or df['VARIEDADE'] == 'PAMER' or df['VARIEDADE'] == 'PALMER' or df['VARIEDADE'] == 'PALMER' or df['VARIEDADE'] == 'PALMER '  or df['VARIEDADE'] == ' PALMER ' or df['VARIEDADE'] == ' PALER' or df['VARIEDADE'] == ' PALER ' or df['VARIEDADE'] == ' PALER' or df['VARIEDADE'] == 'PALER ': 
                        return 'Palmer'

                    #elif df['VARIEDADE'] == 'KENT':
                    #    return 'Kent'

                # elif df['VARIEDADE'] == 'OMER':
                #     return 'Omer'

                #    elif df['VARIEDADE'] == 'OSTEEN':
                #        return 'Osteen'                        
    
                    else:
                        return 'remover' 

                df['VARIEDADE'] = df.apply(correcao_variedade, axis = 1)

                filtro_osteen = df['VARIEDADE'] != 'remover'
                df = df[filtro_osteen]

                df['MES'] = df['MES'].astype(int)
                df['DIA'] = df['DIA'].astype(int)
                df['ANO'] = df['ANO'].astype(int)


    ############################## FILTRO FUNCIONA APENAS FORA DO RT ##############################
            
                ################ FILTRO MES MAIS RECENTE DO ANO MAIS RECENTE

    ############################## FILTRO FUNCIONA APENAS FORA DO RT ##############################
            
                ################ FILTRO MES MAIS RECENTE DO ANO MAIS RECENTE
                ano_recente = df['ANO'].max()

                df_filtro_ano = df['ANO'] == ano_recente
                df_ano = df[df_filtro_ano]

                mes_recente = df_ano['MES'].max()

                df_filtro_mes = df_ano['MES'] == mes_recente
                df_ano_mes = df_ano[df_filtro_mes]

            
                df_piv_dia_mes = pd.pivot_table(df_ano_mes, index = ['ANO','MES','DIA','VARIEDADE'], values = 'TON_HORA',aggfunc = np.mean)
                df_piv_dia_mes = df_piv_dia_mes.reset_index()


                df_piv = pd.pivot_table(df, index = ['ANO','MES','VARIEDADE'], values = 'TON_HORA',aggfunc = np.mean)
                df_piv = df_piv.reset_index()

                df_ano_mes_piv = pd.pivot_table(df_ano, index = ['ANO','MES','VARIEDADE'], values = 'TON_HORA',aggfunc = np.mean)
                df_ano_mes_piv = df_ano_mes_piv.reset_index()


                with coluna1:
               

                    df_ano_mes_piv['ANO'] = df_ano_mes_piv['ANO'].astype(str)

                    fig = px.bar(df_ano_mes_piv, x = 'MES',y = 'TON_HORA', color = 'VARIEDADE', facet_row = 'VARIEDADE', category_orders = {'VARIEDADE':['Tommy','Palmer','Keitt']})
                    

                    filtro_Palmer = df_ano_mes_piv['VARIEDADE'] == 'Palmer'
                    df_ano_mes_palmer = df_ano_mes_piv[filtro_Palmer]

                    filtro_Keitt = df_ano_mes_piv['VARIEDADE'] == 'Keitt'
                    df_ano_mes_keitt = df_ano_mes_piv[filtro_Keitt]

                    filtro_Tommy = df_ano_mes_piv['VARIEDADE'] == 'Tommy'
                    df_ano_mes_tommy = df_ano_mes_piv[filtro_Tommy]

                    fig.add_hline(df_ano_mes_palmer['TON_HORA'].mean(), line_color = 'darkred', line_dash="dot",  annotation_text="Avg-P", annotation_font_color="darkred",row=2, col = 'all')
                    fig.add_hline(df_ano_mes_keitt['TON_HORA'].mean(), line_color = 'darkgreen', line_dash="dot",  annotation_text="Avg-K", annotation_font_color="darkgreen",row=1, col = 'all')
                    fig.add_hline(df_ano_mes_tommy['TON_HORA'].mean(), line_color = 'darkblue', line_dash="dot",  annotation_text="Avg-T", annotation_font_color="darkblue",row=3, col = 'all')
                    fig.update_yaxes(matches=None)
                    

                    fig.update_layout(height = 500, width = 750,uniformtext_minsize=8, uniformtext_mode='show', font = dict(size = 15))
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("VARIEDADE=", "")))
                    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("MES=", "")))
                    
                    placeholder1.write(fig)


                with coluna2:
                
                    fig = px.bar(df_piv_dia_mes,x = 'DIA',y = 'TON_HORA', color = 'VARIEDADE', facet_col = 'VARIEDADE', category_orders = {'VARIEDADE':['Tommy','Palmer','Keitt']})
                    fig.update_layout(height = 420, width = 750,uniformtext_minsize=8, uniformtext_mode='show', font = dict(size = 15))
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)

                    filtro_Palmer = df_piv_dia_mes['VARIEDADE'] == 'Palmer'
                    df_dia_palmer = df_piv_dia_mes[filtro_Palmer]

                    filtro_Keitt = df_piv_dia_mes['VARIEDADE'] == 'Keitt'
                    df_dia_keitt = df_piv_dia_mes[filtro_Keitt]

                    filtro_Tommy = df_piv_dia_mes['VARIEDADE'] == 'Tommy'
                    df_dia_tommy = df_piv_dia_mes[filtro_Tommy]


                    def is_outlier(s):
                        lower_limit = s.mean() - (s.std() * 2)
                        upper_limit = s.mean() + (s.std() * 2)
                        return ~s.between(lower_limit, upper_limit)

                    df_dia_tommy = df_dia_tommy[~df_dia_tommy.groupby(['VARIEDADE'])['TON_HORA'].apply(is_outlier)]

                    def is_outlier(s):
                        lower_limit = s.mean() - (s.std() * 2)
                        upper_limit = s.mean() + (s.std() * 2)
                        return ~s.between(lower_limit, upper_limit)

                    df_dia_palmer = df_dia_palmer[~df_dia_palmer.groupby(['VARIEDADE'])['TON_HORA'].apply(is_outlier)]

                    def is_outlier(s):
                        lower_limit = s.mean() - (s.std() * 2)
                        upper_limit = s.mean() + (s.std() * 2)
                        return ~s.between(lower_limit, upper_limit)

                    df_dia_keitt = df_dia_keitt[~df_dia_keitt.groupby(['VARIEDADE'])['TON_HORA'].apply(is_outlier)]


                    #fig.add_hline(df_dia_palmer['TON_HORA'].mean(), line_color = 'darkred', line_dash="dot",  annotation_text="Avg-P", annotation_font_color="darkred",col=2, row = 'all')
                    fig.add_hline(df_dia_keitt['TON_HORA'].mean(), line_color = 'darkgreen', line_dash="dot",  annotation_text="Avg-K", annotation_font_color="darkgreen",col=3, row = 'all')
                    fig.add_hline(df_dia_tommy['TON_HORA'].mean(), line_color = 'darkblue', line_dash="dot",  annotation_text="Avg-T", annotation_font_color="darkblue",col=1, row = 'all')
                    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("VARIEDADE=", "")))
                

                    placeholder2.write(fig)
                    

                with colunas_2:

                    df_ano['INICIO_PROCESSAMENTO'] = pd.to_datetime(df_ano['INICIO_PROCESSAMENTO'])

                    filtro_Palmer = df_ano['VARIEDADE'] == 'Palmer'
                    df_ano_palmer = df_ano[filtro_Palmer]

                    filtro_Keitt = df_ano['VARIEDADE'] == 'Keitt'
                    df_ano_keitt = df_ano[filtro_Keitt]

                    filtro_Tommy = df_ano['VARIEDADE'] == 'Tommy'
                    df_ano_tommy = df_ano[filtro_Tommy]

                with col2:

############################# REMOVENDO OUTLIERS PARA DETERMINARMOS A MEDIA E DP SEM INFLUENCIAS E AI ENTAO CRIAR LIMITES SEM VIES #############################

                    def is_outlier(s):
                        lower_limit = s.mean() - (s.std() * 2)
                        upper_limit = s.mean() + (s.std() * 2)
                        return ~s.between(lower_limit, upper_limit)

                    df_ano_palmer = df_ano_palmer[~df_ano_palmer.groupby(['VARIEDADE'])['TON_HORA'].apply(is_outlier)]


                    def is_outlier(s):
                        lower_limit = s.mean() - (s.std() * 2)
                        upper_limit = s.mean() + (s.std() * 2)
                        return ~s.between(lower_limit, upper_limit)

                    df_ano_keitt = df_ano_keitt[~df_ano_keitt.groupby(['VARIEDADE'])['TON_HORA'].apply(is_outlier)]

                    def is_outlier(s):
                        lower_limit = s.mean() - (s.std() * 2)
                        upper_limit = s.mean() + (s.std() * 2)
                        return ~s.between(lower_limit, upper_limit)

                    df_ano_tommy = df_ano_tommy[~df_ano_tommy.groupby(['VARIEDADE'])['TON_HORA'].apply(is_outlier)]

                    
                    fig = px.line(df_ano, x = 'INICIO_PROCESSAMENTO', y = 'TON_HORA', facet_row = 'VARIEDADE', color = 'VARIEDADE', color_discrete_sequence= px.colors.qualitative.Set1, hover_name = 'CONTROLE_MEGA',facet_row_spacing=0.02,
                    category_orders = {'VARIEDADE':['Tommy','Palmer','Keitt']})
                    fig.add_hline(df_ano_palmer['TON_HORA'].mean(), line_color = 'red', line_dash="dot",  annotation_text="AVG PALMER", annotation_font_color="red",row=2)
                    fig.add_hline(df_ano_palmer['TON_HORA'].mean() + (df_ano_palmer['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-P", annotation_font_color="black",row=2)
                    fig.add_hline(df_ano_palmer['TON_HORA'].mean() - (df_ano_palmer['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-P", annotation_font_color="black",row=2)


                    fig.add_hline(df_ano_keitt['TON_HORA'].mean(), line_color = 'green', line_dash="dot",  annotation_text="AVG KEITT", annotation_font_color="green",row=1)
                    fig.add_hline(df_ano_keitt['TON_HORA'].mean() + (df_ano_keitt['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-K", annotation_font_color="black",row=1)
                    fig.add_hline(df_ano_keitt['TON_HORA'].mean() - (df_ano_keitt['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-K", annotation_font_color="black",row=1)
                

                    fig.add_hline(df_ano_tommy['TON_HORA'].mean(), line_color = 'blue', line_dash="dot",  annotation_text="AVG TOMMY", annotation_font_color="blue",row=3)
                    fig.add_hline(df_ano_tommy['TON_HORA'].mean() + (df_ano_tommy['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-T", annotation_font_color="black",row=3)
                    fig.add_hline(df_ano_tommy['TON_HORA'].mean() - (df_ano_tommy['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-T", annotation_font_color="black",row=3)

                    fig.update_layout(height = 850, width = 1850, hovermode="x unified")
                    fig.update_traces(mode="markers+lines", hovertemplate=None, textfont_size=12, cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    
                    fig.update_xaxes(categoryorder='category ascending',matches='x')
                    fig.update_yaxes(matches=None)
                    fig.update_traces(line_color='red', row=2)
                    fig.update_traces(line_color='blue', row=3)
                    
                    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("VARIEDADE=", "")))


                    placeholder6.write(fig)


                time.sleep(300)

if selected == 'Etiquetas':

    import sqlite3
    import socket
    


    from pathlib import Path    
    import pandas as pd  # pip install pandas openpyxl
    import plotly.express as px  # pip install plotly-express
    import streamlit as st  # pip install streamlit

    from modulos_dash.balanceamento.funcoes_atualizar_MAF.modulos_import_func_MAF import *



    st.success('### Controle de etiqueta')

    
    url = 'http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH'
    dataframe = pd.read_json(url)
    num_semana = dataframe['SEMANA_ANO'][0]
    dia_semana = dataframe['DIA_DA_SEMANA'][0]

    if dia_semana < 10:
        dia_semana = '0' + str(dia_semana)
    else:
        dia_semana = str(dia_semana)


    empresa = 'AGRODAN'
    endereco = 'Km 28 Estrada Vicinal Belém/Ibó-Zona Rural'
    razao_agrodan = 'Agropecuária Roriz Dantas Ltda'
    cidade = 'Belém do S. Francisco PE'
    qualidade = 'I'

    #### TIME SLEEP VAI FUNCIONAR APENAS PARA O AUTOMATICO, SEM OS INPUTS


    url_maf = 'http://sia:3000/backend/maf/percentuaisCalibre'
    dataframe_MAF = pd.read_json(url_maf)
    
    controle_maf = str(dataframe_MAF['CONTROLE_MEGA'][0])
    controle_maf2 = '0' + controle_maf
    

    variedade = dataframe_MAF['VARIEDADE'][0]


    ### FAZER UM INSERTE NO BANCO AQUI QUE SE O CONTROLE MEGA diferente DO CONTROLE BANCO
    ### ZERAR TODOS OS VALORES

    conn = sqlite3.connect(r"C:\Users\bernard.collin\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
    cursor = conn.cursor()

    df_sql = pd.read_sql_query("""SELECT * FROM import22 """, conn)
    controle_banco = df_sql['controle_db'][0]
    etiquetas_totais_disponiveis = df_sql['rolo_etiq'][0]

    conn.close()

    calibre = dataframe_MAF['CALIBRE'][0]
    calibre = calibre.split('C')[1]
    calibre = calibre.split(' ')[0]

    caixas_totais = round(dataframe_MAF['QTD_CAIXAS'][0])
    st.error(f'###### Controle atual: {controle_maf}  /  Calibre: {calibre}  /  Variedade: {variedade}  /  Nº Semana: {num_semana}  /  Nº Dia: {dia_semana}')
    st.error(f'###### Etiquetas disponíveis no rolo de impressão: {etiquetas_totais_disponiveis} / Quantidade de caixas totais: {caixas_totais}')

    
    #calibre = int(calibre)

   ######### RESETANDO VALORES SE O CONTROLE 
    dataframe_contolre = dataframe['CONTROLE'][0]
    
    controle_banco = str(controle_banco)
    
    

    if controle_banco != controle_maf:
        url_maf = 'http://sia:3000/backend/maf/percentuaisCalibre'
        dataframe_MAF = pd.read_json(url_maf)
        caixas_totais = round(dataframe_MAF['QTD_CAIXAS'][0])

        #C:\Users\danillo.xavier\Desktop\planilha_denilton\banco_impressora


        conn = sqlite3.connect(r"C:\Users\bernard.collin\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
        cursor = conn.cursor()
        
        df_sql_etq = pd.read_sql_query("""SELECT * FROM import22 """, conn)

        etiquetas_no_rolo = df_sql_etq['rolo_etiq'][0] 


        cursor.execute("""
        DELETE FROM import22; 
        """)
        
        caixas_totais = caixas_totais
        caixas_restantes = caixas_totais
        controle_maf = controle_maf
        etiquetas_impressas = 0
        controle_db = controle_maf

        ### ELA É UMA VARIAVEL INDEPENDENTE DO CONTROLE

        etiquetas_rolo = etiquetas_no_rolo


        cursor.execute(f"""
        INSERT INTO import22 (caixas_totais, caixas_restantes, controle_maf, etiquetas_impressas, controle_db, rolo_etiq)
        VALUES ({caixas_totais}, {caixas_restantes} ,{controle_maf} ,{etiquetas_impressas}, {controle_db}, {etiquetas_rolo})
        """)

        conn.commit()
        conn.close()

    
    else:
        url_maf = 'http://sia:3000/backend/maf/percentuaisCalibre'
        dataframe_MAF = pd.read_json(url_maf)
        caixas_totais = round(dataframe_MAF['QTD_CAIXAS'][0])


        conn = sqlite3.connect(r"C:\Users\bernard.collin\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
        cursor = conn.cursor()
        
        df_sql_inicio = pd.read_sql_query("""SELECT * FROM import22 """, conn)

        caixas_totais = caixas_totais
        caixas_restantes = caixas_totais
        controle_maf = df_sql_inicio['controle_maf'][0]
        etiquetas_impressas = df_sql_inicio['etiquetas_impressas'][0]
        controle_db = df_sql_inicio['controle_db'][0]

        etiquetas_no_rolo = df_sql_inicio['rolo_etiq'][0] 



        cursor.execute("""
        DELETE FROM import22; 
        """)

        cursor.execute(f"""
        INSERT INTO import22 (caixas_totais, caixas_restantes, controle_maf, etiquetas_impressas, controle_db, rolo_etiq)
        VALUES ({caixas_totais}, {caixas_restantes} ,{controle_maf} ,{etiquetas_impressas}, {controle_db}, {etiquetas_no_rolo})
        """)

        conn.commit()
        conn.close()
    
    if st.button('Reposição do rolo de etiqueta'):
        st.write('Etiquetas disponíveis reiniciadas para 2400 !')
        
        etiquetas = 2400     

        conn = sqlite3.connect(r"C:\Users\bernard.collin\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
        cursor = conn.cursor()
        
        cursor.execute("""
        DELETE FROM import22; 
        """)

        cursor.execute(f"""
        INSERT INTO import22 (caixas_totais, caixas_restantes, controle_maf, etiquetas_impressas, controle_db, rolo_etiq)
        VALUES ({caixas_totais}, {caixas_restantes} ,{controle_maf} ,{etiquetas_impressas}, {controle_db}, {etiquetas})
        """)

        conn.commit()
        conn.close()



    with st.form('Envio de etiqueta'):
        import math

        coluna1, coluna2, coluna3, coluna4 = st.columns([0.5,1,1,0.5])
        
        # coluna2.info('### Selecione o calibre')

        # calibre = coluna2.selectbox('Calibre:',
        #                             options = ['4','5','6','7','8','9','10','12','14','16'])


        conn = sqlite3.connect(r"C:\Users\bernard.collin\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
        cursor = conn.cursor()

        df_sql = pd.read_sql_query("""SELECT * FROM import22 """, conn)

        etiq = df_sql['etiquetas_impressas'][0] 

        caixas_restantes_graph = df_sql['caixas_restantes'][0] - etiq

        conn.close()


        fig = go.Figure()
        fig.add_trace(go.Bar(x = [caixas_restantes_graph], text = f'Caixas restantes: {caixas_restantes_graph}'))
        fig.add_trace(go.Bar(x = [caixas_totais], text = f'Total de caixas: {caixas_totais}'))
        fig.update_layout(title = 'Caixas etiquetadas:', height = 320, width = 600,showlegend=False,uniformtext_minsize=20, uniformtext_mode='show', font = dict(size = 20))        

        fig.update_traces(textfont_size=12, textposition="inside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
        coluna3.plotly_chart(fig)
   

        calibre2 = str(calibre)

        coluna2.write('### Ajuste a quantidade')


        quantidade_ = coluna2.text_input('Quantidade de etiquetas para impressão:', key = 'qtd', value = 0)

        quantidade_ = int(quantidade_)
        quantidade_ = (quantidade_) / (2)
        quantidade_ = math.ceil(quantidade_)
        quantidade_ = int(quantidade_)
        

        #### ANALISANDO SE QUANTIDADE TA MAIOR DO QUE O RESTANTE NO BANCO
        
        ### 15 linhas, o seja, 30 etiquetas
        
        if (quantidade_ >= 16) and (etiquetas_totais_disponiveis > 30):

             st.write('##### QUANTIDADE DE IMPRESSÃO MAIOR DO QUE A PERMITIDA !!')
             st.write('###### AJUSTANDO NOVO VALOR PARA O MÍNIMO DE 10 etiquetas (5 linhas) !!')
             quantidade_ = 5


####### N IMPRIMINDO MAIS DO QUE O RESTANTE NO ROLO

        elif ((quantidade_ * 2) <= etiquetas_totais_disponiveis) and (etiquetas_totais_disponiveis <= 30):

              quantidade_ = quantidade_ 

              
####### SE MANDAR MAIS DO QUE DISPONIVEL DO ROLO MANDO O RESTANTE DO ROLO SE N FOR MAIOR QUE 30 

        elif ((quantidade_ * 2) >= etiquetas_totais_disponiveis) and (etiquetas_totais_disponiveis <= 30):

               ### ajustando quantidade de linhas para gerar a quantidade restante no rolo

              quantidade_ = etiquetas_totais_disponiveis / 2
              quantidade_impressa = quantidade_ * 2

              st.write('##### QUANTIDADE DE IMPRESSÃO MAIOR DO QUE A PERMITIDA OU O RESTANTE PARA O ROLO !!')         
              st.write(f'###### AJUSTANDO NOVO VALOR PARA O MÍNIMO DE {quantidade_impressa} etiquetas !!')

        else:
            quantidade_ = quantidade_

       
        ###### COLCOAR UM SELECTBOX PARA O IP EX:
        ### ESTEIRA 1,2,3,4 E CADA UMA VAI TER UM IP QUE VAI CORRESPONDER A UMA QUALIDADE CALIBRE ETC
        #calibre2 = 9

        host = '192.168.3.95'
        port = 9100

        etiqueta_baquer2 = f"""<0x10>CT~~CD,~CC^~CT~
        ^XA
        ~TA000
        ~JSN
        ^LT0
        ^MNW
        ^MTT
        ^PON
        ^PMN
        ^LH0,0
        ^JMA
        ^PR3,3
        ~SD24
        ^JUS
        ^LRN
        ^CI27
        ^PA0,1,1,0
        ^XZ
        ^XA
        ^MMT
        ^PW815
        ^LL240
        ^LS0
        ^FO3,0^GFA,297,6812,52,:Z64:eJzt2bENwjAQBdBDKdyRBRBZgTIFUlZhBMqUHo1RMkJKCoTBdgSi4v4vUJD+FefGT6dYSvPPLCR3zbaUn6QUKwHGpHStpruZu8K9nkP0GxvqAYwxay+5b+Yv1z6qmd7dW3VCiIixsRiIWJ9bi5ljbnvMlOs7zGxfw/xVPqXHTGDNCJr4bGfMNGs30K+wmElGRkZGRkZGRkZGRkZGRkZG5q/NiTBrzrgYcwBNbr/KLZlMlclumYyYyaIDZsqTMdk6k+EzuwJmJ0HtPjpkL7PsWJhdDrEzegCZraO2:5CC2
        ^FO5,128^GFA,241,3936,48,:Z64:eJzt17EJwzAQheEXDLkuWsDYK7hMYcgqGcGlq6DRPIpG0ACGi0bQTwi4uKs/hAsX75fMu6+oXT93bxw8716l+VT3pWZfud/rI4Hn28fkWyXejqEQPxTLxKsa4toS8/vE/DoyP67MT0/mH9TvzKeNebuaR79z8yV8+PDhw4cP/7N/Q3+1/UD9wvz933uP7k+6b+l+pvuc7n/aF7RfaB/R/sJ9N5PePHmfwv79AgsfSKo=:B069
        ^FO23,28^GFA,1709,4180,44,:Z64:eJzd10FvG0UUB/CZ8ZN2HEXxbKiUVnKb8WZV5VQVTqZym5n1ql4JBFcOFaSQA8c0cIh66XRj0pWo0KpcekIg5UNwjNKg9ASFT+AUH9qbK3JIpcjizXqbOMYbwgUURrLj2fx2/fyfnZ1dQv77dg9fijBCe4SKzwml2Btqq8QAoQf4KURnBpZxQolBazaHbdu+UYZvgE4NLMA4myn7ZQP73jdOVNtJOal/8uuL+kWqmz91XizXG5ll9MraxscuvdLo2xred/lTzyOchLdFEs5RHV52zydhkNur7aXblF0NwNpEppE/jTbWIok19bBXhljlVia+pn0Zc7T3uLVsyKruXyyTU9aqQ9tH29fUb9nj9hvDlsoVccwatEbTc1kNhh23sTy005hZXsPAxizP7LjFHD71cCxCneXAo6WjHEhbtpdsvesqs1NO64cnKe3V9bME8+WtDXGYL1mVaxvaPZB3bb5jGx/uyAI0aEwM76dOtLQz1HHMifZstErHnvXEGEKEs7ZfcXrAeYHl4tDO8wBEm09MFlp+ZIXHZAgTE8V2ta6rU+ZHTULJmPKZe4Jth4Hnmu0jWy60LsShlibOLFjLkwJb6VRNZK1H4tof+2hlUmQ56ZqP7mW2L6cF2oUkKrIUzJJCexnnwTRHq6L5YhsHtoZzlAqPY2Yn2clBDucYSbKxMPPnC+vdG+TLGXkQMxxjM1+U2dBOp2/i78lhW/wH9gw0evRRkdlNXBxK+1l4bGRdwsbMUEdIuwVOZ23AjBVZUC/vbHWW67oyoztC7H7ZZ7Qy812jwUo7zc0Rqy/Ec3j51eJxIITrtoFR8TgKAkb5thyxQRns1VzLNBTCKwPHq38axQp3iUYs9zJrdClVy7NbmS2l0ZS1qnPcVp5be2B0NW2mIi6DYLSaRisNtK2R44ppa3EpymrAguSgBjamhoF9U29mWZGV5QvM5tCspeFVUXNBMail0brN4eniiOUvqc33+qW0+QzzhX5p/1L6wd1G6fVO6/uRwcAxYqObihouPae2uPSc2p6ZZs9pZ80sdHAe4B0dlTidwOnZ+zZIiKr00Dj2zeRzpa0kya3dH4ATjZsTBNL2eW7xLw55bkk8sGBnTrYCqKyfW3GrQ9CWfrm1eu0SieXuzNo2QL351c/86/ubRG/1VvH+5taqtfIzQUIlwV9s36zhSuGeD33gYXjzbfEwkCSe4220i21rFwNB8Ldtgwa7AnllEfnOfhz5NZH4gtpTFXiswdoULf42AFWNHbQ4abr4zyPLq04vVlW0JR4IyrHebdWN381sywfof9it4e3WzBbaLshYdbMcAsHQEj+rYR5thNZEYK2ArAaR1wCBgGFbzqytYazlYHPQkzebBOePiJZsDmFNYQ6ceeVJ4Ot60loWiNknZuH3HbV37Tpe93ZFa8Pp1ZvtmsJ8Z19t8T2Au2rP/Asn3P+44TOPXVNwXtwgzr7dYvA1+6Q/zjIiVGa1nSJ5E97Y49Jsfaf2Zm7ITo+3U2L3C3NxCr8b6J3nveUHa/c3CyxzXfehmnNxNgKN3+IJPgvIAtuXj8pc4b1RnTiv7JmYcF+IuYOxx31jHTwuWSmThIOY3Rpf78K3rzOLT4209KhMHiQgxNgLrb1/o5nFHGi2KEUn2LyG3OKU84uszYHbHHAsKLyT5zDeHmC+XGG+NzjW+xsf5FsaN8Znpf0JvYluBg==:9E0B
        ^FO191,8^GFA,289,456,24,:Z64:eJyt0E1qQkEMB/BMjH3RxbyMG10IHecGXqDmiYveygjdd67gTbR4EI/gDXTeBwWhXRQayOZHIMkf4H+qtlttWNneV7D0lSsN5kYnaVj0hQ0Dn1Lgr9IHG5HGRDFORTFmbVaybWLe2pijEijMQClmaJxg8Z2NoXcsHuaQcE7F1SbfbuwXtvSLj8FV6a33IJqc7DoPrWNxB9zuhfze+ucRrHd8ctucobsTCaT1OLhD6P5CBglsac25/GXmaMjh9SK+opKB9DnU17/mef+5br/NPwB6kkzG:BCF0
        ^FO17,8^GFA,293,380,20,:Z64:eJyd0DFuwlAMBmCHWCKRUHipOjK4KAfgBOh/IQMjR0A9QQcOkEdbESSGcAROQiQu0CN04AAZmQhOFaYyVPX4ybZ+m+j/NaQa4MjzXVW/XUdRf/gN44IlBrHP6YspeBwHOSpJeYFn+QySp5DZSgmrc9SZCTlobd3aHIls71bkeWtZZzEbKxuPMDtPM2Sy59eJ2akVjoCkl+JDDv7hS1Zqpf0xi0aOlRhwZ5rFgsXpPseillKbGRXHnmamQjTzmnC/rf9+utSit/UIf/1L87suj/puncJLNQ==:6C8C
        ^FO18,132^GFA,185,304,8,:Z64:eJxjYMAO6hlYGBSAtEMDlHaA0s7nZfRBdIuKkkEDUF2HiqNCA0jdEwcw7a4CoT3gNES+I0UJRNezL5cB0eQCBwcGsDsSoHQAjPZQPafHzj3Bw0PN0JCjh8HFQ0VRYYIHnHYC0fNPMDiC+RxQ2oPB4USKoiFHB9DdSxT12DkECNkPABfJJcA=:48F2
        ^FO287,152^GFA,93,152,8,:Z64:eJxjYMAO5DkgtEIDhHZwgNKcfywUQOIcHC4gvgyHQBOIZu6A0AweCv/A6jwcGqA0WFyhowGsXh6qnxAAAGpnDAw=:A1EC
        ^FO20,51^GFA,93,152,8,:Z64:eJxjYMAO+FuABCMDg4ALhFZQgdAOLDY2NmDayckJTDc5OIBpPihdBJVvYmIC64PQAi5tYPX8LVVgeUIAACo1Cvc=:AE54
        ^FO182,176^GFA,377,812,28,:Z64:eJzV0b1qwzAQB3AZD7fZL+DWfQwZ0uRV+gAdFDo0Q8AuHbolr9JuhS4KhvolMvyFh2zFnupCqKqzBHHzBjkQHPqhj7sT4jICMgmJW+oGIrYYSM95q5PXE7tjM8cUlrfUOpsY2NrfvLPVuQm2ijbZsh3tPstfiPQMSZI8DIenuiKSRc0mv2TZbFOUSNnsbjRJwZbtxj0AyjNnxlsuvMHsZ8qwKfSIbbOV/vO3nythjrLQ3uCstu4c33nVKMKw+NGIP95PFmtvC6ipVeJbyijYGoPLJ+Zq2LGlz4B7z1n09uqN/tk+KwyivgvGfQnW+/rYBpj61E+KdHnYpl0J18xgbg6l8DZ/HPvJtmJDF+Z3KfEH8RnKgA==:F5BA
        ^FO419,0^GFA,297,6812,52,:Z64:eJzt2bENwjAQBdBDKdyRBRBZgTIFUlZhBMqUHo1RMkJKCoTBdgSi4v4vUJD+FefGT6dYSvPPLCR3zbaUn6QUKwHGpHStpruZu8K9nkP0GxvqAYwxay+5b+Yv1z6qmd7dW3VCiIixsRiIWJ9bi5ljbnvMlOs7zGxfw/xVPqXHTGDNCJr4bGfMNGs30K+wmElGRkZGRkZGRkZGRkZGRkZG5q/NiTBrzrgYcwBNbr/KLZlMlclumYyYyaIDZsqTMdk6k+EzuwJmJ0HtPjpkL7PsWJhdDrEzegCZraO2:5CC2
        ^FO421,128^GFA,241,3936,48,:Z64:eJzt17EJwzAQheEXDLkuWsDYK7hMYcgqGcGlq6DRPIpG0ACGi0bQTwi4uKs/hAsX75fMu6+oXT93bxw8716l+VT3pWZfud/rI4Hn28fkWyXejqEQPxTLxKsa4toS8/vE/DoyP67MT0/mH9TvzKeNebuaR79z8yV8+PDhw4cP/7N/Q3+1/UD9wvz933uP7k+6b+l+pvuc7n/aF7RfaB/R/sJ9N5PePHmfwv79AgsfSKo=:B069
        ^FO439,28^GFA,1709,4180,44,:Z64:eJzd10FvG0UUB/CZ8ZN2HEXxbKiUVnKb8WZV5VQVTqZym5n1ql4JBFcOFaSQA8c0cIh66XRj0pWo0KpcekIg5UNwjNKg9ASFT+AUH9qbK3JIpcjizXqbOMYbwgUURrLj2fx2/fyfnZ1dQv77dg9fijBCe4SKzwml2Btqq8QAoQf4KURnBpZxQolBazaHbdu+UYZvgE4NLMA4myn7ZQP73jdOVNtJOal/8uuL+kWqmz91XizXG5ll9MraxscuvdLo2xred/lTzyOchLdFEs5RHV52zydhkNur7aXblF0NwNpEppE/jTbWIok19bBXhljlVia+pn0Zc7T3uLVsyKruXyyTU9aqQ9tH29fUb9nj9hvDlsoVccwatEbTc1kNhh23sTy005hZXsPAxizP7LjFHD71cCxCneXAo6WjHEhbtpdsvesqs1NO64cnKe3V9bME8+WtDXGYL1mVaxvaPZB3bb5jGx/uyAI0aEwM76dOtLQz1HHMifZstErHnvXEGEKEs7ZfcXrAeYHl4tDO8wBEm09MFlp+ZIXHZAgTE8V2ta6rU+ZHTULJmPKZe4Jth4Hnmu0jWy60LsShlibOLFjLkwJb6VRNZK1H4tof+2hlUmQ56ZqP7mW2L6cF2oUkKrIUzJJCexnnwTRHq6L5YhsHtoZzlAqPY2Yn2clBDucYSbKxMPPnC+vdG+TLGXkQMxxjM1+U2dBOp2/i78lhW/wH9gw0evRRkdlNXBxK+1l4bGRdwsbMUEdIuwVOZ23AjBVZUC/vbHWW67oyoztC7H7ZZ7Qy812jwUo7zc0Rqy/Ec3j51eJxIITrtoFR8TgKAkb5thyxQRns1VzLNBTCKwPHq38axQp3iUYs9zJrdClVy7NbmS2l0ZS1qnPcVp5be2B0NW2mIi6DYLSaRisNtK2R44ppa3EpymrAguSgBjamhoF9U29mWZGV5QvM5tCspeFVUXNBMail0brN4eniiOUvqc33+qW0+QzzhX5p/1L6wd1G6fVO6/uRwcAxYqObihouPae2uPSc2p6ZZs9pZ80sdHAe4B0dlTidwOnZ+zZIiKr00Dj2zeRzpa0kya3dH4ATjZsTBNL2eW7xLw55bkk8sGBnTrYCqKyfW3GrQ9CWfrm1eu0SieXuzNo2QL351c/86/ubRG/1VvH+5taqtfIzQUIlwV9s36zhSuGeD33gYXjzbfEwkCSe4220i21rFwNB8Ldtgwa7AnllEfnOfhz5NZH4gtpTFXiswdoULf42AFWNHbQ4abr4zyPLq04vVlW0JR4IyrHebdWN381sywfof9it4e3WzBbaLshYdbMcAsHQEj+rYR5thNZEYK2ArAaR1wCBgGFbzqytYazlYHPQkzebBOePiJZsDmFNYQ6ceeVJ4Ot60loWiNknZuH3HbV37Tpe93ZFa8Pp1ZvtmsJ8Z19t8T2Au2rP/Asn3P+44TOPXVNwXtwgzr7dYvA1+6Q/zjIiVGa1nSJ5E97Y49Jsfaf2Zm7ITo+3U2L3C3NxCr8b6J3nveUHa/c3CyxzXfehmnNxNgKN3+IJPgvIAtuXj8pc4b1RnTiv7JmYcF+IuYOxx31jHTwuWSmThIOY3Rpf78K3rzOLT4209KhMHiQgxNgLrb1/o5nFHGi2KEUn2LyG3OKU84uszYHbHHAsKLyT5zDeHmC+XGG+NzjW+xsf5FsaN8Znpf0JvYluBg==:9E0B
        ^FO607,8^GFA,289,456,24,:Z64:eJyt0E1qQkEMB/BMjH3RxbyMG10IHecGXqDmiYveygjdd67gTbR4EI/gDXTeBwWhXRQayOZHIMkf4H+qtlttWNneV7D0lSsN5kYnaVj0hQ0Dn1Lgr9IHG5HGRDFORTFmbVaybWLe2pijEijMQClmaJxg8Z2NoXcsHuaQcE7F1SbfbuwXtvSLj8FV6a33IJqc7DoPrWNxB9zuhfze+ucRrHd8ctucobsTCaT1OLhD6P5CBglsac25/GXmaMjh9SK+opKB9DnU17/mef+5br/NPwB6kkzG:BCF0
        ^FO433,8^GFA,293,380,20,:Z64:eJyd0DFuwlAMBmCHWCKRUHipOjK4KAfgBOh/IQMjR0A9QQcOkEdbESSGcAROQiQu0CN04AAZmQhOFaYyVPX4ybZ+m+j/NaQa4MjzXVW/XUdRf/gN44IlBrHP6YspeBwHOSpJeYFn+QySp5DZSgmrc9SZCTlobd3aHIls71bkeWtZZzEbKxuPMDtPM2Sy59eJ2akVjoCkl+JDDv7hS1Zqpf0xi0aOlRhwZ5rFgsXpPseillKbGRXHnmamQjTzmnC/rf9+utSit/UIf/1L87suj/puncJLNQ==:6C8C
        ^FO434,132^GFA,185,304,8,:Z64:eJxjYMAO6hlYGBSAtEMDlHaA0s7nZfRBdIuKkkEDUF2HiqNCA0jdEwcw7a4CoT3gNES+I0UJRNezL5cB0eQCBwcGsDsSoHQAjPZQPafHzj3Bw0PN0JCjh8HFQ0VRYYIHnHYC0fNPMDiC+RxQ2oPB4USKoiFHB9DdSxT12DkECNkPABfJJcA=:48F2
        ^FO703,152^GFA,93,152,8,:Z64:eJxjYMAO5DkgtEIDhHZwgNKcfywUQOIcHC4gvgyHQBOIZu6A0AweCv/A6jwcGqA0WFyhowGsXh6qnxAAAGpnDAw=:A1EC
        ^FO436,51^GFA,93,152,8,:Z64:eJxjYMAO+FuABCMDg4ALhFZQgdAOLDY2NmDayckJTDc5OIBpPihdBJVvYmIC64PQAi5tYPX8LVVgeUIAACo1Cvc=:AE54
        ^FO598,176^GFA,377,812,28,:Z64:eJzV0b1qwzAQB3AZD7fZL+DWfQwZ0uRV+gAdFDo0Q8AuHbolr9JuhS4KhvolMvyFh2zFnupCqKqzBHHzBjkQHPqhj7sT4jICMgmJW+oGIrYYSM95q5PXE7tjM8cUlrfUOpsY2NrfvLPVuQm2ijbZsh3tPstfiPQMSZI8DIenuiKSRc0mv2TZbFOUSNnsbjRJwZbtxj0AyjNnxlsuvMHsZ8qwKfSIbbOV/vO3nythjrLQ3uCstu4c33nVKMKw+NGIP95PFmtvC6ipVeJbyijYGoPLJ+Zq2LGlz4B7z1n09uqN/tk+KwyivgvGfQnW+/rYBpj61E+KdHnYpl0J18xgbg6l8DZ/HPvJtmJDF+Z3KfEH8RnKgA==:F5BA
        ^FT82,167^A0N,34,33^FH\^CI28^FD{controle_maf2} L-{num_semana}{dia_semana}^FS^CI27
        ^FT17,205^A0N,39,38^FH\^CI28^FD{variedade}^FS^CI27
        ^FPH,3^FT335,170^A0N,38,38^FH\^CI28^FD{calibre2}^FS^CI27
        ^FT498,167^A0N,34,33^FH\^CI28^FD{controle_maf2} L-{num_semana}{dia_semana}^FS^CI27
        ^FT433,205^A0N,39,38^FH\^CI28^FD{variedade}^FS^CI27
        ^FPH,3^FT751,170^A0N,38,38^FH\^CI28^FD{calibre2}^FS^CI27
        ^PQ1,0,1,Y
        ^XZ
        """.encode()

        submitted = coluna2.form_submit_button("Imprimir")

        if submitted:
            
            #### CONSULTAR BASE PARA ATUALIZAR INFORMAÇÕES AQUI 

            mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  

            try:           
                mysocket.connect((host, port))                                
                for i in range(quantidade_):
                    mysocket.send(etiqueta_baquer2)    
                mysocket.close()


                #### ATUALIZANDO QUANTIDADE DE ETIQUETAS

#### ATUALIZANDO QUANTIDADE DE CAIXAS NO BANCO


                conn = sqlite3.connect(r"C:\Users\bernard.collin\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
                cursor = conn.cursor()

                df_sql = pd.read_sql_query("""SELECT * FROM import22 """, conn)

                etiquetas_impressas2 = df_sql['etiquetas_impressas'][0] + (quantidade_ * 2 )
                
                caixas_restantes = df_sql['caixas_restantes'][0] - etiquetas_impressas2 

                total_etiquetas = df_sql['rolo_etiq'][0]


                rolo_etiquetas_atualizado = total_etiquetas - (quantidade_ * 2)



                cursor.execute("""
                DELETE FROM import22; 
                """)

                cursor.execute(f"""
                INSERT INTO import22 (caixas_totais, caixas_restantes, controle_maf, etiquetas_impressas, controle_db, rolo_etiq)
                VALUES ({caixas_totais}, {caixas_restantes},{controle_maf}, {etiquetas_impressas2}, {controle_db}, {rolo_etiquetas_atualizado})
                """)
                
                caixas_restantes_graph = caixas_restantes

                conn.commit()
                st.write('Dados inseridos com sucesso no banco')
                conn.close()


                st.write('Etiquetas impressas com sucesso!')   
                #st.write(caixas_restantes) 
                
                

                #time.sleep(3)
                #st.stop()   

            except:
                #st.write(caixas_restantes)
                st.write("Falha na conexão com a impressora !")
                #time.sleep(10)
            time.sleep(0.3)
            st.experimental_rerun()
             