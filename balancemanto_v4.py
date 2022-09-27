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


# sia
# 177.52.21.58


st.set_page_config(layout="wide")


selected = option_menu(
    menu_title = 'Packing House - Projetos',
    options = ['Balanceamento','Previsão de Calibres','Contagem de frutos','Produtividade','Etiquetas'],
    icons = ['plus-slash-minus','bar-chart-line-fill','camera-video-fill','people-fill','card-heading'],
    menu_icon = 'box-seam',
    default_index = 0,
    orientation = 'horizontal',
    styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#f56e00", "font-size": "20px"}, 
            "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#009b36","font-size": "20px"},
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
            #b

            ## ou seja, eu tenho b prontinho ja

            st.session_state.b_ = b
            st.session_state.anterior = variaveis_df


            if len(df_embaladeiras_ativas) == 0:
                url_embaladeiras_ativas = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_EMB_ATIVAS'
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



### PRIMEIRO - CHECKAR SE O TALHAO TA NA BASE DE AMOSTRAGEM
### SE NÃO - CHECKAR SE TEM BASE DO HISTORICO DESSE TALHAO
### SE NÃO - UTLIZAR A VARIEDADE DESSE TALHAO

## JOGAR ISSO PARA DENTRO DO BOTAO DE ATUALIZAR ONTROLE E EXPORTAR OS PERCENTUAIS



            #b
            ### colocar um condicional de se o len == 1 pegar o historico
            #st.write(len(b))

            st.session_state.grafico_passado = b

            # colocar um session state para o b

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
            
    ########################## DEFINIÇÃO DA BASE DOS PERCENTUAIS ########################## LEMBRAR DE CORRIGIR OS PERCENTUAIS DE CALIBRES QUE NÃO EXISTIREM DESTES TALHÕES

    ########################## AQUI É SE ELE ESTIVER NA LISTA EU TRAGO A BASE DE AMOSTRAGEM    


                
    ########################## AQUI É SE O TALHAO NAO ESTIVER NA LISTA DE AMOSTRAGEM EU TRAGO O HISTORICO DO TALHAO OU DA VARIEDADE       

    ########################### VERIFICANDO SE O TALHAO ESTA NA BASE HISTORICA DE  TALHAO

                if result_talhao_2:
                        from modulos_dash.balanceamento.funcoes_atualizar_controle.funcoes_else_base_amostragem import * 
                        
                        st.write('Base do histórico do talhão')

                        filtro_talhao = df_comportamento_calibres_TALHAO['TALHAO'] == talhao_controle
                        df_comportamento_calibres_TALHAO = df_comportamento_calibres_TALHAO[filtro_talhao] 

                        
                        df_comportamento_calibres_TALHAO_PIV = pd.pivot_table(df_comportamento_calibres_TALHAO, index = ['TALHAO','VALOR_CALIBRE'], values = 'Calibre', aggfunc= np.mean)
                        df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.reset_index()
                        df_comportamento_calibres_TALHAO_PIV.rename(columns = {'Calibre':'Percentual','VALOR_CALIBRE':'Calibre'}, inplace = True)
                        df_comportamento_calibres_TALHAO_PIV['Calibre'] = df_comportamento_calibres_TALHAO_PIV.apply(correcao_calibre_new, axis = 1)
                        df_comportamento_calibres_TALHAO_PIV['Percentual_RECENTE'] = 0
                        df_comportamento_calibres_TALHAO_PIV = df_comportamento_calibres_TALHAO_PIV.drop(columns = ['TALHAO'])
                


    ###################################### CORREÇÃO PARA CALIBRE FALTANTE COLOCANDO A MÉDIA DA VARIEDADE ######################################


    ###################################### FAZENDO PARA  A TOMMY ######################################

                        
                        df_comportamento_calibres_TALHAO_PIV = correcao_calibre_media_variedade(VARIEDADE,df_comportamento_calibres_TALHAO_PIV)

                        df_graficos_passado  = df_comportamento_calibres_TALHAO_PIV
                        st.session_state.grafico_passado = df_graficos_passado
                        

                        st.session_state.b_ = df_comportamento_calibres_TALHAO_PIV

                        #### COLOCAR AQUI A CORREÇÃO DO CALIBRE QUE N EXISTIR PARA A MEDIA DA VARIEDADE


    ##################### COLOCAR AQUI A BASE QUALITY DE QUALIDADE #####################

                        ## PRIMEIRA COISA É APLICAR O FILTRO DE TALHAO
                        
                        lista_talhoes_quality = pd.unique(df_comportamento_qualidade["TALHAO"])   ### ESSA LOGICA SERVE TAMVBEM PARA  FILTRO DE ITENS EM UMA COLUNA DE UMA BASE
                        lista_talhoes_quality = pd.DataFrame(lista_talhoes_quality)
                        lista_talhoes_quality.rename(columns = {0:'TALHAO'}, inplace = True)
                        
    #################### VERIFICANDO SE O TALHAO ESTA NA BASE HISTORICA DE QUALIDADE, SE NAO, UTILIZO A MEDIA DA VARIEDADE

                        result_talhao_3_ = lista_talhoes_quality.TALHAO.isin([talhao_controle]).any().any()

                        if result_talhao_3_:

                            filtro_talhao_quality = df_comportamento_qualidade['TALHAO'] == talhao_controle
                            df_comportamento_qualidade = df_comportamento_qualidade[filtro_talhao_quality] 
                            dataset_quality_piv = pd.pivot_table(df_comportamento_qualidade, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['TALHAO'], aggfunc = np.mean)
                            dataset_quality_piv = dataset_quality_piv.reset_index()
                            
                            dataset_quality_piv = dataset_quality_piv.drop(columns = ['TALHAO'])
                            

                            #st.write('PRA QUALIDADE VOU USAR O FILTRO TALHAO')

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

    #############################  CORREÇÃO PARA QUALIDADE FALTANTE E COLOCANDO A DA VARIEDADE ####################################

                        dataset_quality_piv = correcao_qualidade_para_variedade(VARIEDADE,dataset_quality_piv)

                        st.session_state.quality_percent = dataset_quality_piv


    #### CALCULANDO A MEDIA DE FRUTOS POR CAIXOTES NOVO

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

    ########################### SE ELE NAO ESTOVER TRAGO A BASE HISTORICA DA VARIEDADE CORRESPONDENTE AO TALHAO 
    ##### PRA TESTAR ESA LOGICA É SO COLOCAR O TALHAO  AGD-BAHIA 096

                else:
    ########################### SE NAO TIVER NA BASE TALHAO, TRAGO AQUI O HISTORICO DA VARIEDADE DAQUELE CONTROLE
                        
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

    #############################  CORREÇÃO PARA QUALIDADE FALTANTE E COLOCANDO A DA VARIEDADE ####################################

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

    ############################# PERCENTUAIS DE CALIBRE  #############################

                        filtro_talhao = df_comportamento_calibres_TALHAO['VARIEDADE'] == VARIEDADE_2
                        df_comportamento_calibres_TALHAO = df_comportamento_calibres_TALHAO[filtro_talhao] 

                        ####### FILTRO TALHAO APLICADO
                        ####### AGORA O OBJTEIVO É FAZER UMA DINAMICA DE TALHAO, CALIBRE COM AS MÉDIAS DELES
                        
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
                
    ###################################### CORREÇÃO PARA CALIBRE FALTANTE COLOCANDO A MÉDIA DA VARIEDADE ######################################


    ###################################### FAZENDO PARA  A TOMMY ######################################

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

        ###################################### FAZENDO PARA  A KEITT ######################################
                
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


        ###################################### FAZENDO PARA  A KENT ######################################
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

        ###################################### FAZENDO PARA  A PALMER ######################################
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

        ###################################### FAZENDO PARA  A OMER ######################################
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

        ###################################### FAZENDO PARA  A PALMER ######################################
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


    #### CALCULANDO A MEDIA DE FRUTOS POR CAIXOTES NOVO

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
                #st.write('#### Tente novamente em alguns minutos')
            
            a = dataset['Calibre'].value_counts() / dataset['Calibre'].count()

            
            toneladas_totais_controle = dataset['PESO_CONTROLE'][0].item() * 1000

            
        ################ ALTERAR AQUI DENTRO OS PERCENTUAIS DE CALIBRE EM b ################

            from urllib.error import HTTPError
            try:
                url_percentual_MAF = 'http://177.52.21.58:3000/backend/maf/percentuaisCalibre'
                dataset_MAF = pd.read_json(url_percentual_MAF)
                
            except HTTPError :
                st.error('### Erro com a base de dados da MAF !!')
                #st.error('#### Aguarde um tempo e atualize novamente.')

            

            dataset_MAF = ajustes_DATA_MAF(dataset_MAF)

     ########################################## REMOVER ACIMA DEPOIS ##########################################


            dataset_MAF['Calibre'] = dataset_MAF.apply(correcao_calibre_MAF, axis = 1)

            dataset_MAF['Calibre'] = dataset_MAF['Calibre'].astype(str)

            dataset_MAF['Calibre'] = dataset_MAF.apply(ajuste_final, axis = 1) 


            dataset_MAF['Qualidade'] = dataset_MAF.apply(correcao_qualidade_MAF, axis = 1)
            dataset_MAF = dataset_MAF.drop(columns = ['CALIBRE_QUALIDADE'])

            dataset_MAF['VARIEDADE'] = dataset_MAF.apply(correcao_variedade_maf, axis = 1)


            controle = dataset_MAF['CONTROLE_MEGA'][0]
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


    ################################## DEFININDO NOVOS PERCENTUAIS ##################################
        
            somatorio_frutos_peso = somatorio_ajuste_calibres_correcao(somatorio_frutos_peso)

##################### CONTA DE MEDIA DE FRUTOS DO CONTROLE #####################


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
            
##################### FINAL DA CONTA DE MEDIA DE FRUTOS DO CONTROLE #####################

            filtro_ref = somatorio_frutos_peso['Calibre'] != 'Refugo'
            somatorio_frutos_peso = somatorio_frutos_peso[filtro_ref]

            somatorio_frutos_peso['Calibre'] = somatorio_frutos_peso['Calibre'].astype(int)
            somatorio_frutos_peso_para_b = somatorio_frutos_peso.drop(columns = ['PESO_KG','QTD_FRUTOS'])

            b = somatorio_frutos_peso_para_b
            b = b.sort_values('Calibre')
            
            st.session_state.b_ = b
            st.session_state.anterior = dataset

            df_embaladeiras_ativas = criando_embaladeiras_ativas()
            
            if len(df_embaladeiras_ativas) == 0:
                url_embaladeiras_ativas = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_EMB_ATIVAS'
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
        st.info('http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH')
        st.info('http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH')

    Caixotes = dataset['CONTENTORES'][0].item()
    
    dataset = dataset 
    ########################################   CORRIGINDO PERCENTUAIS FALTANTES    ################
    from modulos_dash.balanceamento.funcoes_menu.modulos_import_func_menu import *

    b = correcao_calibres_de_b(b)
    percentual_de_4,percentual_de_5,percentual_de_6,percentual_de_7,percentual_de_8,percentual_de_9,percentual_de_10,percentual_de_12,percentual_de_14,percentual_de_16 = definindo_percentuais(b)

    ##### CORRIGINDO PERCENTUAIS FALTANTES ###############################
    
    quality = correcao_quality(quality)

    ######################  CHECK QUALIDADE GERAL - ATRIBUINDO VALOR ####################
    
    primeira_percent,segunda_percent,terceira_percent,refugo_percent = definindo_percentuais_quality(quality)

    st.session_state_base_crua = b
    dataset_2 = dataset 

    ###########  ATRIBUINDO CONSTANTES INICIAIS PARA AS VARIAVEIS #####################

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

    ############## ESTRUTURAÇÃO DAS ABAS ##############
    

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
        
        ############## DEFININDO CONTROLE ######################
        #tempo_2 = st.session_state_tempo

        colunA, colunB, colunC, colunD = st.columns([0.3,0.3,0.5,1])

        #controle = dataset['CONTROLE'][0]


        st.session_state.controle = controle

        ############## EXIBINDO MÉTRICA DO CONTROLE ######################
        controle2 = st.session_state.controle
        colunA.metric(label="Controle", value= controle2, delta= VARIEDADE)
        colunC.metric(label="MAF (t/h)", value= produtividade_atual) 

        tempo_2 = st.session_state_tempo
        colunB.metric(label="Intervalo de tempo (min)", value= round(tempo_2,2))
        #st.metric(label="MAF", value= produtividade_atual, delta= 't/h')  

        col2, col3 = st.columns([0.30,1])
        
        emba_aviso = st.session_state.emba_aviso

        ######################################### ALTERANDO PERCENTUAIS    ###############################################

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
        
            
        ########################## FAZER AQUI AQUELA SEPRAÇÃO POR VARIEDADE


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

        ################################ CALCULO DE CAIXAS POR QUALIDADE ################################

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
        

        ############ CONTAS BALANCEAMENTO

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
                    
                    e = round(df_comportamento_calibres_TALHAO_PIV['Percentual'],2)

                    fig.add_trace(go.Bar(x = df_comportamento_calibres_TALHAO_PIV['Calibre'],y = df_comportamento_calibres_TALHAO_PIV['Percentual'], name = 'Previsão', text = e))





                    fig.update_traces(textposition="inside",textfont_size=25, cliponaxis=False,textangle=90, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    fig.update_layout(height = 600, width = 1000,uniformtext_minsize=15)
        
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


if selected == 'Previsão de Calibres':
    from modulos_dash.previsao.modulo_pagina_previsao import *
    bb = previsao_dash()
    bb

    
#### DEIXAR MODULO DA CONTAGEM EM STANDY BY
if selected == 'Contagem de frutos':
    


    coluna1, coluna3 = st.columns([0.5,1])
    
    
    coluna1.write('## Monitoramento e troca de controle:')
    coluna3.markdown('#')
    


    if coluna3.button('Iniciar monitoramento'):
        
        import plotly.express as px
        import plotly.graph_objects as go
        from PIL import Image


        #st.write('### Contagem de frutos')

        
        #st.write('Opa, clicastes?')
        import time
        import os
        os.environ["OMP_NUM_THREADS"] = "1"
        os.environ["OPENBLAS_NUM_THREADS"] = "1"
        os.environ["MKL_NUM_THREADS"] = "1"
        os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
        os.environ["NUMEXPR_NUM_THREADS"] = "1"
        os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

        import sys
        sys.path.insert(0, './yolov5')

        import argparse
        import os
        import platform
        import shutil
        import time
        from pathlib import Path
        import cv2
        import torch
        import torch.backends.cudnn as cudnn

        from yolov5.models.experimental import attempt_load
        from yolov5.utils.downloads import attempt_download
        from yolov5.models.common import DetectMultiBackend
        from yolov5.utils.datasets import LoadImages, LoadStreams
        from yolov5.utils.general import (LOGGER, check_img_size, non_max_suppression, scale_coords, 
                                        check_imshow, xyxy2xywh, increment_path)
        from yolov5.utils.torch_utils import select_device, time_sync
        from yolov5.utils.plots import Annotator, colors
        from deep_sort.utils.parser import get_config
        from deep_sort.deep_sort import DeepSort


        #from modulos_dash.contagem.modulo_pagina_contagem import *

        FILE = Path(__file__).resolve()
        ROOT = FILE.parents[0]  # yolov5 deepsort root directory
        if str(ROOT) not in sys.path:
            sys.path.append(str(ROOT))  # add ROOT to PATH
        ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
        count = 0
        data = []
        count_fly = 0
        count_fly2 = 0
        data_fly = []
        data_fly2 = []
        
        def detect(opt):
            out, source, yolo_model, deep_sort_model, show_vid, save_vid, save_txt, imgsz, evaluate, half, project, name, exist_ok= \
                opt.output, opt.source, opt.yolo_model, opt.deep_sort_model, opt.show_vid, opt.save_vid, \
                opt.save_txt, opt.imgsz, opt.evaluate, opt.half, opt.project, opt.name, opt.exist_ok
            webcam = source == '0' or source.startswith(
                'rtsp') or source.startswith('http') or source.endswith('.txt')

            device = select_device(opt.device)
            # initialize deepsort
            cfg = get_config()
            cfg.merge_from_file(opt.config_deepsort)
            deepsort = DeepSort(deep_sort_model,
                                device,
                                max_dist=cfg.DEEPSORT.MAX_DIST,
                                max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                                max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                                )

            # Initialize
            
            half &= device.type != 'cpu'  # half precision only supported on CUDA

            # The MOT16 evaluation runs multiple inference streams in parallel, each one writing to
            # its own .txt file. Hence, in that case, the output folder is not restored
            if not evaluate:
                if os.path.exists(out):
                    pass
                    shutil.rmtree(out)  # delete output folder
                os.makedirs(out)  # make new output folder

            # Directories
            save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
            save_dir.mkdir(parents=True, exist_ok=True)  # make dir

            # Load model
            device = select_device(device)
            model = DetectMultiBackend(yolo_model, device=device, dnn=opt.dnn)
            stride, names, pt, jit, _ = model.stride, model.names, model.pt, model.jit, model.onnx
            imgsz = check_img_size(imgsz, s=stride)  # check image size

            # Half
            half &= pt and device.type != 'cpu'  # half precision only supported by PyTorch on CUDA
            if pt:
                model.model.half() if half else model.model.float()

            # Set Dataloader
            vid_path, vid_writer = None, None
            # Check if environment supports image displays
            if show_vid:
                show_vid = check_imshow()

            # Dataloader
            if webcam:
                show_vid = check_imshow()
                cudnn.benchmark = True  # set True to speed up constant image size inference
                dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt and not jit)
                bs = len(dataset)  # batch_size
            else:
                dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt and not jit)
                bs = 1  # batch_size
            vid_path, vid_writer = [None] * bs, [None] * bs

            # Get names and colors
            names = model.module.names if hasattr(model, 'module') else model.names

            # extract what is in between the last '/' and last '.'
            txt_file_name = source.split('/')[-1].split('.')[0]
            txt_path = str(Path(save_dir)) + '/' + txt_file_name + '.txt'

            if pt and device.type != 'cpu':
                model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.model.parameters())))  # warmup
            dt, seen = [0.0, 0.0, 0.0, 0.0], 0
            
            




            with st.empty():

                start_time = time.time() 
                st.session_state.percent_processado = 0
                st.session_state.controle = 'Controle...'
                st.session_state.toneladas_passadas = 0 

                url_control = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH'
                dataset_mega = pd.read_json(url_control)
                tons_tot = dataset_mega['PESO_CONTROLE'][0]
                


                for frame_idx, (path, img, im0s, vid_cap, s) in enumerate(dataset):

                    current_time = time.time()
                    time_passed = current_time - start_time

                        
                    t1 = time_sync()
                    
                    
                    if time_passed > 60:

                        start_time = current_time

                        url_percentual_MAF = 'http://177.52.21.58:3000/backend/maf/percentuaisCalibre'
                        dataset_MAF = pd.read_json(url_percentual_MAF)
                        tons_passesed = dataset_MAF['PESO_KG'].sum() / 1000
                        st.session_state.toneladas_passadas = tons_passesed 
                        
                        


                        dataset_MAF['Calibre'] = dataset_MAF['CALIBRE_QUALIDADE'].str[:3]
                        dataset_MAF['Qualidade'] = dataset_MAF['CALIBRE_QUALIDADE'].str[3:]


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

                        dataset_MAF['Calibre'] = dataset_MAF.apply(correcao_calibre_MAF, axis = 1)
                        dataset_MAF['Calibre'] = dataset_MAF['Calibre'].astype(str)


                        dataset_MAF['Calibre_22'] = dataset_MAF['Calibre'].astype(float)
                        
                        
                        #coluna_4.write(QTD_REFUGO_MAF)


                        def ajuste_final(dataset_MAF):
                            if dataset_MAF['Calibre'] == '0':
                                return 'Refugo'
                            else:
                                return dataset_MAF['Calibre']
                        dataset_MAF['Calibre'] = dataset_MAF.apply(ajuste_final, axis = 1)


                        dataset_MAF = dataset_MAF.drop(columns = ['CALIBRE_QUALIDADE'])

                        def correcao_variedade_maf(dataset_MAF):
                            if dataset_MAF['VARIEDADE'] == 'TOMMY':
                                return "Tommy Atkins"
                            elif dataset_MAF['VARIEDADE'] == 'TAMMY':
                                return "Tommy Atkins"
                            elif dataset_MAF['VARIEDADE'] == 'KEITT':
                                return "Keitt"
                            elif dataset_MAF['VARIEDADE'] == 'KENT':
                                return "Kent"
                            elif dataset_MAF['VARIEDADE'] == 'PALMER':
                                return "Palmer"
                            elif dataset_MAF['VARIEDADE'] == 'OMER':
                                return 'Omer'
                            elif dataset_MAF['VARIEDADE'] == 'OSTEEN':
                                return 'Osteen'
                        dataset_MAF['VARIEDADE'] = dataset_MAF.apply(correcao_variedade_maf, axis = 1)

                        
                        somatorio_frutos_peso = pd.pivot_table(dataset_MAF, index = 'Calibre', values = ['QTD_FRUTOS','PESO_KG'],aggfunc= 'sum')
                        somatorio_frutos_peso = somatorio_frutos_peso.reset_index()

                        somatorio_frutos_peso['Percentual'] = (somatorio_frutos_peso['QTD_FRUTOS'] / somatorio_frutos_peso['QTD_FRUTOS'].sum()) * 100

                        filtro_refugo = somatorio_frutos_peso['Calibre'] != 'Refugo'
                        somatorio_frutos_peso = somatorio_frutos_peso[filtro_refugo]


                        somatorio_frutos_peso = somatorio_frutos_peso[['Calibre','Percentual']]

                        refugo_total = count_fly2 + 0

                        somatorio_frutos_peso['Frutos_refugo'] = (somatorio_frutos_peso['Percentual'] * refugo_total) / 100
                        

                        VARIEDADE = dataset_MAF['VARIEDADE'][1]

                        ### DEFININDO PESO MEDIO DOS CALIBRES E MULTIPLICANDO PELA QUANTIDADE DE FRUTOS
                        def frutos_controle(somatorio_frutos_peso):
                            if VARIEDADE == 'Palmer':
                                if somatorio_frutos_peso['Calibre'] == '4':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 1.055

                                elif somatorio_frutos_peso['Calibre'] == '5':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.8785

                                elif somatorio_frutos_peso['Calibre'] == '6':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.666

                                elif somatorio_frutos_peso['Calibre'] == '7':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.593

                                elif somatorio_frutos_peso['Calibre'] == '8':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.5175

                                elif somatorio_frutos_peso['Calibre'] == '9':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.458

                                elif somatorio_frutos_peso['Calibre'] == '10':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.407

                                elif somatorio_frutos_peso['Calibre'] == '12':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.3355

                                elif somatorio_frutos_peso['Calibre'] == '14':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.2875

                                elif somatorio_frutos_peso['Calibre'] == '16':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.230


                            #################################################### TOMMY ATKINS #####################################################
                            elif VARIEDADE == 'Tommy Atkins':
                                if somatorio_frutos_peso['Calibre'] == '4':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 1.1

                                elif somatorio_frutos_peso['Calibre'] == '5':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.940

                                elif somatorio_frutos_peso['Calibre'] == '6':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.760

                                elif somatorio_frutos_peso['Calibre'] == '7':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.5985

                                elif somatorio_frutos_peso['Calibre'] == '8':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.5185

                                elif somatorio_frutos_peso['Calibre'] == '9':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.461

                                elif somatorio_frutos_peso['Calibre'] == '10':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.4065

                                elif somatorio_frutos_peso['Calibre'] == '12':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.3335

                                elif somatorio_frutos_peso['Calibre'] == '14':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.2875

                                elif somatorio_frutos_peso['Calibre'] == '16':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.2655
                                
                            #################################################### KEITT #####################################################
                            elif VARIEDADE == 'Keitt' or VARIEDADE == 'Omer':
                                if somatorio_frutos_peso['Calibre'] == '4':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 1.2

                                elif somatorio_frutos_peso['Calibre'] == '5':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.825
                                    
                                elif somatorio_frutos_peso['Calibre'] == '6':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.676
                                    
                                elif somatorio_frutos_peso['Calibre'] == '7':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.604
                                    
                                elif somatorio_frutos_peso['Calibre'] == '8':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.5145
                                    
                                elif somatorio_frutos_peso['Calibre'] == '9':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.4575
                                    
                                elif somatorio_frutos_peso['Calibre'] == '10':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.412
                                    
                                elif somatorio_frutos_peso['Calibre'] == '12':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.345
                                    
                                elif somatorio_frutos_peso['Calibre'] == '14':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.292
                                    
                                elif somatorio_frutos_peso['Calibre'] == '16':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.256
                                
                                

                            #################################################### KENT #####################################################
                            elif VARIEDADE == 'Kent':

                                if somatorio_frutos_peso['Calibre'] == '4':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 1.115

                                elif  somatorio_frutos_peso['Calibre'] == '5':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.845
                                    
                                elif  somatorio_frutos_peso['Calibre'] == '6':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.693
                                    
                                elif  somatorio_frutos_peso['Calibre'] == '7':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.5855
                                    
                                elif  somatorio_frutos_peso['Calibre'] == '8':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.5105
                                    
                                elif  somatorio_frutos_peso['Calibre'] == '9':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.460
                                    
                                elif  somatorio_frutos_peso['Calibre'] == '10':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.4095
                                    
                                elif  somatorio_frutos_peso['Calibre'] == '12':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.339
                                    
                                elif  somatorio_frutos_peso['Calibre'] == '14':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.286
                                    
                                elif  somatorio_frutos_peso['Calibre'] == '16':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.2545
                                
                            
                            #################################################### OSTEEN #####################################################
                            elif VARIEDADE == 'Osteen':

                                if somatorio_frutos_peso['Calibre'] == '4':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 1.243

                                elif somatorio_frutos_peso['Calibre'] == '5':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.882
                                    
                                elif somatorio_frutos_peso['Calibre'] == '6':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.705
                                    
                                elif somatorio_frutos_peso['Calibre'] == '7':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.594
                                    
                                elif somatorio_frutos_peso['Calibre'] == '8':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.516
                                    
                                elif somatorio_frutos_peso['Calibre'] == '9':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.4565
                                    
                                elif somatorio_frutos_peso['Calibre'] == '10':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.4045
                                    
                                elif somatorio_frutos_peso['Calibre'] == '12':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.337
                                    
                                elif somatorio_frutos_peso['Calibre'] == '14':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.2855
                                    
                                elif somatorio_frutos_peso['Calibre'] == '16':
                                    return somatorio_frutos_peso['Frutos_refugo'] * 0.249

                        somatorio_frutos_peso['KGS_REFUGO_CONTROLE'] = somatorio_frutos_peso.apply(frutos_controle, axis = 1)

                        somatorio_frutos_peso['KGS_REFUGO_CONTROLE_tons'] = somatorio_frutos_peso['KGS_REFUGO_CONTROLE'] / 1000

                        

                        tons_count_ref = somatorio_frutos_peso['KGS_REFUGO_CONTROLE_tons'].sum()


                        ## CRIAR UMA COLUNA [REFUGO CALIBRE] EM SOMATORIO FRUTOS QUE É O COUNT_FLY VS A COLUNA PERCENTE
                        ## E DEPOIS ACHO O PESO MÉDIO PASSADO DESSA COLUNA 


                        ton_total_passado = (tons_passesed + tons_count_ref)


                        
                        #coluna_4.write(tons_tot)

                        controle_p = dataset_mega['CONTROLE'][0].item()

                        percent_passed = round((100 * ton_total_passado) / tons_tot,2)

                        #coluna_4.write(percent_passed)

                        st.session_state.percent_processado = percent_passed
                        st.session_state.controle = controle_p


                    img = torch.from_numpy(img).to(device)
                    img = img.half() if half else img.float()  # uint8 to fp16/32
                    img /= 255.0  # 0 - 255 to 0.0 - 1.0
                    if img.ndimension() == 3:
                        img = img.unsqueeze(0)
                    t2 = time_sync()
                    dt[0] += t2 - t1

                    # Inference
                    visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if opt.visualize else False
                    pred = model(img, augment=opt.augment, visualize=visualize)
                    t3 = time_sync()
                    dt[1] += t3 - t2

                    # Apply NMS
                    pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, opt.classes, opt.agnostic_nms, max_det=opt.max_det)
                    dt[2] += time_sync() - t3
                    
                   # tempo_passado = current_time - start_time
                    
                    # Process detections
                    
                    for i, det in enumerate(pred):  # detections per image
                        seen += 1
                        if webcam:  # batch_size >= 1
                            p, im0, _ = path[i], im0s[i].copy(), dataset.count
                            s += f'{i}: '
                        else:
                            p, im0, _ = path, im0s.copy(), getattr(dataset, 'frame', 0)

                        p = Path(p)  # to Path
                        save_path = str(save_dir / p.name)  # im.jpg, vid.mp4, ...
                        s += '%gx%g ' % img.shape[2:]  # print string

                        annotator = Annotator(im0, line_width=2, pil=not ascii)
                        w, h = im0.shape[1], im0.shape[0]
                        if det is not None and len(det):
                            # Rescale boxes from img_size to im0 size
                            det[:, :4] = scale_coords(
                                img.shape[2:], det[:, :4], im0.shape).round()

                            # Print results
                            for c in det[:, -1].unique():
                                n = (det[:, -1] == c).sum()  # detections per class
                                
                                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                            xywhs = xyxy2xywh(det[:, 0:4])
                            confs = det[:, 4]
                            clss = det[:, 5]

                            # pass detections to deepsort
                            t4 = time_sync()
                            outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss.cpu(), im0)
                            
                            t5 = time_sync()
                            dt[3] += t5 - t4
                            
                            # draw boxes for visualization
                            if len(outputs) > 0:
                                for j, (output, conf) in enumerate(zip(outputs, confs)):

                                    bboxes = output[0:4]
                                    id = output[4]
                                    classe = output[5]
                                    #count
                                    count_obj(bboxes,w,h,id,classe)
                                    c = int(classe)  # integer class
                                    label = f'{id} {names[c]} {conf:.2f}'
                                    annotator.box_label(bboxes, label, color=colors(c, True))

                                    if save_txt:
                                        # to MOT format
                                        bbox_left = output[0]
                                        bbox_top = output[1]
                                        bbox_w = output[2] - output[0]
                                        bbox_h = output[3] - output[1]
                                        # Write MOT compliant results to file
                                        with open(txt_path, 'a') as f:
                                            f.write(('%g ' * 10 + '\n') % (frame_idx + 1, id, bbox_left,  # MOT format
                                                                        bbox_top, bbox_w, bbox_h, -1, -1, -1, -1))

                            LOGGER.info(f'{s}Done. YOLO:({t3 - t2:.3f}s), DeepSort:({t5 - t4:.3f}s)')

                        else:
                            deepsort.increment_ages()
                            LOGGER.info('No detections')

                        
                        im0 = annotator.result()


                        if show_vid:
                            global count_fly
                            color = (0,255,0)
                            start_point = (0, h-150)
                            end_point = (w, h-150)
                            cv2.line(im0, start_point, end_point, color, thickness=2)
                            thickness = 3
                            org = (150,150)
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            fontScale = 1

                            color2 = (0,255,255)
                            fontScale2 = 1
                            org2 = (150,100)

                            cv2.putText(im0, str(count_fly) + ' ' + 'Mangas' , org, font,
                                fontScale,color,thickness, cv2.LINE_AA)


                            #cv2.putText(im0, 'mangos_C2:' + str(count_fly2), org2, font,
                            #   fontScale2,color2,thickness, cv2.LINE_AA)
                        #  cv2.putText(im0, 'Flyss:' + str(count_fly), org, font,
                            #  fontScale,color,thickness, cv2.LINE_AA)
                        #   cv2.putText(im0, 'Flys2:' + str(count_fly2), org, font,
                            #  fontScale,color,thickness, cv2.LINE_AA)


                            cv2.imshow(str(p), im0)
                            


                            

                            percent_passed = st.session_state.percent_processado 
                            controle_p = st.session_state.controle

                            count_fly2 = count_fly + 0
                            

                            col1, col2, col3 = st.columns([1,1,1])
                            
                            


                            #col1.write('### Percentual processado')
                           # col1.metric(label = 'Processado (%):', value = percent_passed, delta = controle_p)
                            

                            col2.error('### Limite para troca')
                            
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

                            col2.plotly_chart(fig)
                            
                            title_ = '#### Processamento do controle:' + ' ' +str(controle_p)
                            col1.error(title_)
                           # col1.error(controle_p)
                            time_passed_2 = round(time_passed,2)

                            fig2 = px.bar(x = [time_passed_2], title = 'Próxima atualização')

                            fig2.add_vline(60)
                            fig2.update_xaxes(range = [0,60],visible=False)
                            fig2.update_yaxes(visible=False)
                            fig2.update_layout(height = 150, width = 1700)
                            fig2.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1)
                            

                            ### UM GRAFICO DE LINHA POR TEMPO SERIA MUITO BOM MOSTRANDOD MAIS OU MENOS
                            ### A PRODITIVIDADE MÉDIA

                            tons_passesed = st.session_state.toneladas_passadas 
                            # titulo = 'Controle atual:' + ' ' + str(controle_p)

                            fig22 = go.Figure()
                            fig22.add_trace(go.Bar(y = [tons_tot], name = 'Toneladas totais', text = round(tons_tot,2), marker_color='orangered'))
                            fig22.add_trace(go.Bar(y = [tons_passesed], name = 'Toneladas processadas', text = round(tons_passesed,2), marker_color='darkgreen'))
                            fig22.update_layout(height = 400, width = 500, title = 'Total X Processado')
                            fig22.update_traces(marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                        
                            col1.plotly_chart(fig22)
                            col1.write(' ')
                            col1.plotly_chart(fig2)



                            

                            col3.error('### Contagem nas esteiras de refugo')
                            
                            col3.write(' ')
                            col3.write(' ')
                            col3.write(' ')
                            # col3.write(' ')
                            # col3.write(' ')
                            # col3.write(' ')
                            col3.image(im0 , channels = 'BGR')


                            
                            if percent_passed > 97.5:
                                
                                
                                col1.error('#### 97.5 % do controle processado')
                                col2.error('#### Clique em iniciar para monitorar outro controle')
                            
                                

                                st.stop()


                            #st.image(im0)

                            #cv2.waitKey(1)
                            #st.video(im0)
                            if cv2.waitKey(1) == ord('q'):  # q to quit
                                raise StopIteration

                            # Save results (image with detections)
                        if save_vid:
                            if vid_path != save_path:  # new video
                                vid_path = save_path
                                if isinstance(vid_writer, cv2.VideoWriter):
                                    vid_writer.release()  # release previous video writer
                                if vid_cap:  # video
                                    fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                    w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                    h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                else:  # stream
                                    fps, w, h = 30, im0.shape[1], im0.shape[0]

                                vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                                
                            vid_writer.write(im0)
                        

                    #data2 = requests.get("http://177.52.21.58:3000/backend/maf/#percentuaisCalibre")
                    #json_data2 = data2.json()
                   # dataset_MAF = pd.DataFrame.from_dict(json_data2)
                            
                    #st.write(dataset_MAF)



            
            # Print results
            t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
            LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS, %.1fms deep sort update \
                per image at shape {(1, 3, *imgsz)}' % t)
                
            
            if save_txt or save_vid:
                print('Results saved to %s' % save_path)
                if platform == 'darwin':  # MacOS
                    os.system('open ' + save_path)

        #def count_obj(box,w,h,id):
            #global count,data 
            #center_coordinates = (int(box[0]+(box[2]-box[0])/2), int(box[1]+(box[3]-box[1])/2))
            #if int(box[1]+(box[3]-box[1])/2) > (h - 350):
                #if id not in data:
                # count += 1
                # data.append(id)
            
        
        def count_obj(box,w,h,id,classe):
            global count_fly,data_fly, count_fly2 , data_fly2
            center_coordinates = (int(box[0]+(box[2]-box[0])/2) , int(box[1]+(box[3]-box[1])/2))
            
            if  classe == 0:
                if int(box[1]+(box[3]-box[1])/2) < (h-150):
                    if id not in data_fly:
                            count_fly += 1
                            data_fly.append(id)
                           
                            
try:
    with st.empty():
        if __name__ == '__main__':
            parser = argparse.ArgumentParser()
            parser.add_argument('--yolo_model', nargs='+', type=str, default='best_final.pt', help='model.pt path(s)')
            parser.add_argument('--deep_sort_model', type=str, default='osnet_x0_25')
            parser.add_argument('--source', type=str, default='rtsp://localhost:554/live', help='source') 

            ### file/folder, 0 for webcam 'videos/video_controle_450_keitt.mp4' 
            ### link camera1: 'rtsp://admin:admin102030@192.168.3.92:554/cam/realmonitor?channel=1&subtype=0'
            ### link youtube fuciona tambem

            parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
            parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
            parser.add_argument('--conf-thres', type=float, default=0.75, help='object confidence threshold')
            parser.add_argument('--iou-thres', type=float, default=0.75, help='IOU threshold for NMS')
            parser.add_argument('--fourcc', type=str, default='mp4v', help='output video codec (verify ffmpeg support)')
            parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
            parser.add_argument('--show-vid', action='store_true', help='display tracking video results',default = True)
            parser.add_argument('--save-vid', action='store_true', help='save video tracking results', default = True)
            parser.add_argument('--save-txt', action='store_true', help='save MOT compliant results to *.txt')
            # class 0 is person, 1 is bycicle, 2 is car... 79 is oven
            #parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 16 17')
            parser.add_argument('--classes', default=[0,1], type=int, help='filter by class')
            parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
            parser.add_argument('--augment', action='store_true', help='augmented inference')
            parser.add_argument('--evaluate', action='store_true', help='augmented inference')
            parser.add_argument("--config_deepsort", type=str, default="deep_sort/configs/deep_sort.yaml")
            parser.add_argument("--half", action="store_true", help="use FP16 half-precision inference")
            parser.add_argument('--visualize', action='store_true', help='visualize features')
            parser.add_argument('--max-det', type=int, default=1000, help='maximum detection per image')
            parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
            parser.add_argument('--project', default=ROOT / 'runs/track', help='save results to project/name')
            parser.add_argument('--name', default='exp', help='save results to project/name')
            parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
            opt = parser.parse_args()
            opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand

            with torch.no_grad():
                detect(opt)
except NameError:
    st.write(' ')


if selected == 'Produtividade':
    
    from PIL import Image
    img = Image.open('agrodn.png')
    newsize = (380,110)
    img2 = img.resize(newsize)

        ########## JANELA LATERAL ##########

    st.sidebar.image(img2, use_column_width=True)
    st.sidebar.title('Menu')
    st.sidebar.markdown('Escolha a informação para visualizar:')

    pagina_selecionada = st.sidebar.radio('', ['Produtividade Controle','Produtividade Embaladeiras'])
    
    if pagina_selecionada == 'Produtividade Controle':
        
        from modulos_dash.embaladeira.dash_produtividade import *
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
                
                df = get_data_ritmo()
                
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


###################### TRAZER AINDA UM GRAFICO COMPARATIVO COM O ANO ANTERIOR PRA SE TER UMA EXPECTATIVA MENSAL APENAS

                with coluna1:
                #    st.write('__')

                ### FAZER FIILTRO DA VARIEDADE EM DF_ANO_MES PARA PLOTAR A MEDIA DE REFERENCIA


                    df_ano_mes_piv['ANO'] = df_ano_mes_piv['ANO'].astype(str)

                    fig = px.bar(df_ano_mes_piv, x = 'MES',y = 'TON_HORA', color = 'VARIEDADE', facet_row = 'VARIEDADE', category_orders = {'VARIEDADE':['Tommy','Palmer','Keitt']})
                    #fig.update_layout(height = 500, width = 500)

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
                #  st.write('__')
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


                    fig.add_hline(df_dia_palmer['TON_HORA'].mean(), line_color = 'darkred', line_dash="dot",  annotation_text="Avg-P", annotation_font_color="darkred",col=2, row = 'all')
                    fig.add_hline(df_dia_keitt['TON_HORA'].mean(), line_color = 'darkgreen', line_dash="dot",  annotation_text="Avg-K", annotation_font_color="darkgreen",col=3, row = 'all')
                    fig.add_hline(df_dia_tommy['TON_HORA'].mean(), line_color = 'darkblue', line_dash="dot",  annotation_text="Avg-T", annotation_font_color="darkblue",col=1, row = 'all')
                    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("VARIEDADE=", "")))
                # fig.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))

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
                    fig.add_hline(df_ano_palmer['TON_HORA'].mean(), line_color = 'blue', line_dash="dot",  annotation_text="AVG PALMER", annotation_font_color="blue",row=2)
                    fig.add_hline(df_ano_palmer['TON_HORA'].mean() + (df_ano_palmer['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-P", annotation_font_color="black",row=2)
                    fig.add_hline(df_ano_palmer['TON_HORA'].mean() - (df_ano_palmer['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-P", annotation_font_color="black",row=2)


                    fig.add_hline(df_ano_keitt['TON_HORA'].mean(), line_color = 'green', line_dash="dot",  annotation_text="AVG KEITT", annotation_font_color="green",row=1)
                    fig.add_hline(df_ano_keitt['TON_HORA'].mean() + (df_ano_keitt['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-K", annotation_font_color="black",row=1)
                    fig.add_hline(df_ano_keitt['TON_HORA'].mean() - (df_ano_keitt['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-K", annotation_font_color="black",row=1)
                

                    fig.add_hline(df_ano_tommy['TON_HORA'].mean(), line_color = 'red', line_dash="dot",  annotation_text="AVG TOMMY", annotation_font_color="red",row=3)
                    fig.add_hline(df_ano_tommy['TON_HORA'].mean() + (df_ano_tommy['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-T", annotation_font_color="black",row=3)
                    fig.add_hline(df_ano_tommy['TON_HORA'].mean() - (df_ano_tommy['TON_HORA'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-T", annotation_font_color="black",row=3)

                    fig.update_layout(height = 850, width = 1850, hovermode="x unified")
                    fig.update_traces(mode="markers+lines", hovertemplate=None, textfont_size=12, cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
                    
                    fig.update_xaxes(categoryorder='category ascending',matches='x')
                    fig.update_yaxes(matches=None)
                    #fig.update_yaxes(showticklabels=True, row=2)
                    fig.for_each_annotation(lambda a: a.update(text=a.text.replace("VARIEDADE=", "")))
                    placeholder6.write(fig)


                time.sleep(20)


    if pagina_selecionada == 'Produtividade Embaladeiras':
        
        ###################### INTERESSANTE FAZER UM TREEMAP DAS EMBALADEIRAS 

        import requests
        st.write('Dash Emabaladeiras')
        data2 = requests.get("http://177.52.21.58:3000/backend/busca_generica/buscaGenericaMYSQLAvilla?sql=CALL%209090agrodan.SP_DX_EMB_PRODUTIVIDADE_RECENTE()")
        
        json_data2 = data2.json()

        df_piv_3=pd.json_normalize(json_data2)
        df_piv_3 = pd.DataFrame.from_dict(df_piv_3)

        dic = df_piv_3[:1]
        dic = dic.reset_index()

        df_22 = dic.set_index('index').T.to_dict('list')
        aa = df_22.get(0)
        df_ = pd.DataFrame.from_dict(aa)


######################## FAZENDO O CX/HR ACUMULADA ########################


        df_ = df_.sort_values(['LEH_DATA']).reset_index(drop = True)

        df_['CX_acu'] = df_.groupby(['PESSOA','VARIEDADE','LINHAPRODUCAO'])['LEH_QUANTIDADE'].cumsum(axis = 0)
        df_['HR_acu'] = df_.groupby(['PESSOA','VARIEDADE','LINHAPRODUCAO'])['HORAS'].cumsum(axis = 0)
        df_['CX_acu_HR_acu'] = df_['CX_acu'] / df_['HR_acu']

        df_['LEH_DATA'] = df_['LEH_DATA'].str.split('.').str[0]
        df_['DATA'] = df_['LEH_DATA'].str.split('T').str[0]
        df_['ANO'] = df_['DATA'].str.split('-').str[0]
        df_['MES'] = df_['DATA'].str.split('-').str[1]
        df_['DIA'] = df_['DATA'].str.split('-').str[2]
        
        # af =  df_['LINHAPRODUCAO'].value_counts()
        # af = pd.DataFrame(af)
        # af = (af['LINHAPRODUCAO']* 100) / af['LINHAPRODUCAO'].sum()
        # af

        def correcao_nomes_variedades(df_):
            if df_['VARIEDADE'] == 'Tommy - 31' or df_['VARIEDADE'] == 'Tommy - 30' or df_['VARIEDADE'] == 'Tommy - 32' or df_['VARIEDADE'] == 'Tommy - 29':
                return 'Tommy Atkins'
            elif df_['VARIEDADE'] == 'Palmer -02':
                return 'Palmer'
            elif df_['VARIEDADE'] == 'Keitt 02 C' or df_['VARIEDADE'] == 'Keitt 02':
                return 'Keitt'
            else:
                return 'NADA'
        df_['VARIEDADE'] = df_.apply(correcao_nomes_variedades, axis = 1)
        

        df_['HORARIO'] = df_['LEH_DATA'].str.split('T').str[1]
        df_['HORA'] = df_['HORARIO'] .str.split(':').str[0]
        df_['MIN'] = df_['HORARIO'] .str.split(':').str[1]
        df_['HORA_MIN'] = df_['HORA'] + ':' + df_['MIN']

        
        
        def definindo_calibre(df_):
            if df_['VARIEDADE'] == 'Palmer':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return '4'
               if df_['LINHAPRODUCAO'] == 3:
                   return '5'
               if df_['LINHAPRODUCAO'] == 4:
                   return '5'
               if df_['LINHAPRODUCAO'] == 5:
                   return '5'
               if df_['LINHAPRODUCAO'] == 6:
                   return '8'
               if df_['LINHAPRODUCAO'] == 7:
                   return '8'
               if df_['LINHAPRODUCAO'] == 8:
                   return '8'
               if df_['LINHAPRODUCAO'] == 9:
                   return '8'
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return '10'
               if df_['LINHAPRODUCAO'] == 12:
                   return '10'
               if df_['LINHAPRODUCAO'] == 13:
                   return '10'
               if df_['LINHAPRODUCAO'] == 14:
                   return '9'
               if df_['LINHAPRODUCAO'] == 15:
                   return '9'
               if df_['LINHAPRODUCAO'] == 16:
                   return '9'
               if df_['LINHAPRODUCAO'] == 17:
                   return '6'
               if df_['LINHAPRODUCAO'] == 18:
                   return '6'
               if df_['LINHAPRODUCAO'] == 19:
                   return '12'
               if df_['LINHAPRODUCAO'] == 20:
                   return '7'
               if df_['LINHAPRODUCAO'] == 21:
                   return '7'
               if df_['LINHAPRODUCAO'] == 22:
                   return '7'
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Keitt':
                
                if df_['LINHAPRODUCAO'] == 1:
                       return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '4'
                if df_['LINHAPRODUCAO'] == 3:
                   return '10'
                if df_['LINHAPRODUCAO'] == 4:
                   return '10'
                if df_['LINHAPRODUCAO'] == 5:
                   return '10'
                if df_['LINHAPRODUCAO'] == 6:
                   return '10'
                if df_['LINHAPRODUCAO'] == 7:
                   return '9'
                if df_['LINHAPRODUCAO'] == 8:
                   return '9'
                if df_['LINHAPRODUCAO'] == 9:
                   return '9'
                if df_['LINHAPRODUCAO'] == 10:
                   return '9'
                if df_['LINHAPRODUCAO'] == 11:
                   return '6'
                if df_['LINHAPRODUCAO'] == 12:
                   return '6'
                if df_['LINHAPRODUCAO'] == 13:
                   return '6'
                if df_['LINHAPRODUCAO'] == 14:
                   return '8'
                if df_['LINHAPRODUCAO'] == 15:
                   return '8'
                if df_['LINHAPRODUCAO'] == 16:
                   return '8'
                if df_['LINHAPRODUCAO'] == 17:
                   return '7'
                if df_['LINHAPRODUCAO'] == 18:
                   return '7'
                if df_['LINHAPRODUCAO'] == 19:
                   return '7'
                if df_['LINHAPRODUCAO'] == 20:
                   return '5'
                if df_['LINHAPRODUCAO'] == 21:
                   return '5'
                if df_['LINHAPRODUCAO'] == 22:
                   return '5'
                else:
                    return
                'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                       return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '4'
                if df_['LINHAPRODUCAO'] == 3:
                   return '6'
                if df_['LINHAPRODUCAO'] == 4:
                   return '6'
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return '7'
                if df_['LINHAPRODUCAO'] == 7:
                   return '7'
                if df_['LINHAPRODUCAO'] == 8:
                   return '7'
                if df_['LINHAPRODUCAO'] == 9:
                   return '7'
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return '10'
                if df_['LINHAPRODUCAO'] == 12:
                   return '10'
                if df_['LINHAPRODUCAO'] == 13:
                   return '10'
                if df_['LINHAPRODUCAO'] == 14:
                   return '9'
                if df_['LINHAPRODUCAO'] == 15:
                   return '9'
                if df_['LINHAPRODUCAO'] == 16:
                   return '9'
                if df_['LINHAPRODUCAO'] == 17:
                   return '12'
                if df_['LINHAPRODUCAO'] == 18:
                   return '12'
                if df_['LINHAPRODUCAO'] == 19:
                   return '12'
                if df_['LINHAPRODUCAO'] == 20:
                   return '8'
                if df_['LINHAPRODUCAO'] == 21:
                   return '8'
                if df_['LINHAPRODUCAO'] == 22:
                   return '8'
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_1'] = df_.apply(definindo_calibre, axis = 1)
        
        def definindo_calibre_2(df_):
            if df_['VARIEDADE'] == 'Palmer':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return '4'
               if df_['LINHAPRODUCAO'] == 3:
                   return ''
               if df_['LINHAPRODUCAO'] == 4:
                   return '14'
               if df_['LINHAPRODUCAO'] == 5:
                   return ''
               if df_['LINHAPRODUCAO'] == 6:
                   return ''
               if df_['LINHAPRODUCAO'] == 7:
                   return ''
               if df_['LINHAPRODUCAO'] == 8:
                   return ''
               if df_['LINHAPRODUCAO'] == 9:
                   return ''
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return ''
               if df_['LINHAPRODUCAO'] == 12:
                   return ''
               if df_['LINHAPRODUCAO'] == 13:
                   return ''
               if df_['LINHAPRODUCAO'] == 14:
                   return ''
               if df_['LINHAPRODUCAO'] == 15:
                   return ''
               if df_['LINHAPRODUCAO'] == 16:
                   return ''
               if df_['LINHAPRODUCAO'] == 17:
                   return ''
               if df_['LINHAPRODUCAO'] == 18:
                   return '12'
               if df_['LINHAPRODUCAO'] == 19:
                   return '6'
               if df_['LINHAPRODUCAO'] == 20:
                   return ''
               if df_['LINHAPRODUCAO'] == 21:
                   return ''
               if df_['LINHAPRODUCAO'] == 22:
                   return ''
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Keitt':
                
                if df_['LINHAPRODUCAO'] == 1:
                       return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '4'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return ''
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return '14'
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                    return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '4'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return '14'
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return ''
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_2'] = df_.apply(definindo_calibre_2, axis = 1)
       
        
        def definindo_calibre_3(df_):
            if df_['VARIEDADE'] == 'Palmer' or df_['VARIEDADE'] == 'Keitt':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return '16'
               if df_['LINHAPRODUCAO'] == 3:
                   return ''
               if df_['LINHAPRODUCAO'] == 4:
                   return ''
               if df_['LINHAPRODUCAO'] == 5:
                   return ''
               if df_['LINHAPRODUCAO'] == 6:
                   return ''
               if df_['LINHAPRODUCAO'] == 7:
                   return ''
               if df_['LINHAPRODUCAO'] == 8:
                   return ''
               if df_['LINHAPRODUCAO'] == 9:
                   return ''
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return ''
               if df_['LINHAPRODUCAO'] == 12:
                   return ''
               if df_['LINHAPRODUCAO'] == 13:
                   return ''
               if df_['LINHAPRODUCAO'] == 14:
                   return ''
               if df_['LINHAPRODUCAO'] == 15:
                   return ''
               if df_['LINHAPRODUCAO'] == 16:
                   return ''
               if df_['LINHAPRODUCAO'] == 17:
                   return ''
               if df_['LINHAPRODUCAO'] == 18:
                   return ''
               if df_['LINHAPRODUCAO'] == 19:
                   return ''
               if df_['LINHAPRODUCAO'] == 20:
                   return ''
               if df_['LINHAPRODUCAO'] == 21:
                   return ''
               if df_['LINHAPRODUCAO'] == 22:
                   return ''
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                    return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '5'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return ''
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return ''
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_3'] = df_.apply(definindo_calibre_3, axis = 1)
        
        
        def definindo_calibre_4(df_):
            if df_['VARIEDADE'] == 'Palmer' or df_['VARIEDADE'] == 'Keitt':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return '16'
               if df_['LINHAPRODUCAO'] == 3:
                   return ''
               if df_['LINHAPRODUCAO'] == 4:
                   return ''
               if df_['LINHAPRODUCAO'] == 5:
                   return ''
               if df_['LINHAPRODUCAO'] == 6:
                   return ''
               if df_['LINHAPRODUCAO'] == 7:
                   return ''
               if df_['LINHAPRODUCAO'] == 8:
                   return ''
               if df_['LINHAPRODUCAO'] == 9:
                   return ''
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return ''
               if df_['LINHAPRODUCAO'] == 12:
                   return ''
               if df_['LINHAPRODUCAO'] == 13:
                   return ''
               if df_['LINHAPRODUCAO'] == 14:
                   return ''
               if df_['LINHAPRODUCAO'] == 15:
                   return ''
               if df_['LINHAPRODUCAO'] == 16:
                   return ''
               if df_['LINHAPRODUCAO'] == 17:
                   return ''
               if df_['LINHAPRODUCAO'] == 18:
                   return ''
               if df_['LINHAPRODUCAO'] == 19:
                   return ''
               if df_['LINHAPRODUCAO'] == 20:
                   return ''
               if df_['LINHAPRODUCAO'] == 21:
                   return ''
               if df_['LINHAPRODUCAO'] == 22:
                   return ''
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                    return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '5'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return ''
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return ''
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_4'] = df_.apply(definindo_calibre_4, axis = 1)
        
        
        def definindo_calibre_5(df_):
            if df_['VARIEDADE'] == 'Palmer' or df_['VARIEDADE'] == 'Keitt':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return '14'
               if df_['LINHAPRODUCAO'] == 3:
                   return ''
               if df_['LINHAPRODUCAO'] == 4:
                   return ''
               if df_['LINHAPRODUCAO'] == 5:
                   return ''
               if df_['LINHAPRODUCAO'] == 6:
                   return ''
               if df_['LINHAPRODUCAO'] == 7:
                   return ''
               if df_['LINHAPRODUCAO'] == 8:
                   return ''
               if df_['LINHAPRODUCAO'] == 9:
                   return ''
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return ''
               if df_['LINHAPRODUCAO'] == 12:
                   return ''
               if df_['LINHAPRODUCAO'] == 13:
                   return ''
               if df_['LINHAPRODUCAO'] == 14:
                   return ''
               if df_['LINHAPRODUCAO'] == 15:
                   return ''
               if df_['LINHAPRODUCAO'] == 16:
                   return ''
               if df_['LINHAPRODUCAO'] == 17:
                   return ''
               if df_['LINHAPRODUCAO'] == 18:
                   return ''
               if df_['LINHAPRODUCAO'] == 19:
                   return ''
               if df_['LINHAPRODUCAO'] == 20:
                   return ''
               if df_['LINHAPRODUCAO'] == 21:
                   return ''
               if df_['LINHAPRODUCAO'] == 22:
                   return ''
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                    return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '14'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return ''
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return ''
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_5'] = df_.apply(definindo_calibre_5, axis = 1)
        
        
        def definindo_calibre_6(df_):
            if df_['VARIEDADE'] == 'Palmer' or df_['VARIEDADE'] == 'Keitt':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return 'Refugo'
               if df_['LINHAPRODUCAO'] == 3:
                   return ''
               if df_['LINHAPRODUCAO'] == 4:
                   return ''
               if df_['LINHAPRODUCAO'] == 5:
                   return ''
               if df_['LINHAPRODUCAO'] == 6:
                   return ''
               if df_['LINHAPRODUCAO'] == 7:
                   return ''
               if df_['LINHAPRODUCAO'] == 8:
                   return ''
               if df_['LINHAPRODUCAO'] == 9:
                   return ''
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return ''
               if df_['LINHAPRODUCAO'] == 12:
                   return ''
               if df_['LINHAPRODUCAO'] == 13:
                   return ''
               if df_['LINHAPRODUCAO'] == 14:
                   return ''
               if df_['LINHAPRODUCAO'] == 15:
                   return ''
               if df_['LINHAPRODUCAO'] == 16:
                   return ''
               if df_['LINHAPRODUCAO'] == 17:
                   return ''
               if df_['LINHAPRODUCAO'] == 18:
                   return ''
               if df_['LINHAPRODUCAO'] == 19:
                   return ''
               if df_['LINHAPRODUCAO'] == 20:
                   return ''
               if df_['LINHAPRODUCAO'] == 21:
                   return ''
               if df_['LINHAPRODUCAO'] == 22:
                   return ''
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                    return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '14'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return ''
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return ''
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_6'] = df_.apply(definindo_calibre_6, axis = 1)
        
        
        def definindo_calibre_7(df_):
            if df_['VARIEDADE'] == 'Palmer' or df_['VARIEDADE'] == 'Keitt':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return ''
               if df_['LINHAPRODUCAO'] == 3:
                   return ''
               if df_['LINHAPRODUCAO'] == 4:
                   return ''
               if df_['LINHAPRODUCAO'] == 5:
                   return ''
               if df_['LINHAPRODUCAO'] == 6:
                   return ''
               if df_['LINHAPRODUCAO'] == 7:
                   return ''
               if df_['LINHAPRODUCAO'] == 8:
                   return ''
               if df_['LINHAPRODUCAO'] == 9:
                   return ''
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return ''
               if df_['LINHAPRODUCAO'] == 12:
                   return ''
               if df_['LINHAPRODUCAO'] == 13:
                   return ''
               if df_['LINHAPRODUCAO'] == 14:
                   return ''
               if df_['LINHAPRODUCAO'] == 15:
                   return ''
               if df_['LINHAPRODUCAO'] == 16:
                   return ''
               if df_['LINHAPRODUCAO'] == 17:
                   return ''
               if df_['LINHAPRODUCAO'] == 18:
                   return ''
               if df_['LINHAPRODUCAO'] == 19:
                   return ''
               if df_['LINHAPRODUCAO'] == 20:
                   return ''
               if df_['LINHAPRODUCAO'] == 21:
                   return ''
               if df_['LINHAPRODUCAO'] == 22:
                   return ''
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                    return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '16'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return ''
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return ''
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_7'] = df_.apply(definindo_calibre_7, axis = 1)
        
        
        def definindo_calibre_8(df_):
            if df_['VARIEDADE'] == 'Palmer' or df_['VARIEDADE'] == 'Keitt':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return ''
               if df_['LINHAPRODUCAO'] == 3:
                   return ''
               if df_['LINHAPRODUCAO'] == 4:
                   return ''
               if df_['LINHAPRODUCAO'] == 5:
                   return ''
               if df_['LINHAPRODUCAO'] == 6:
                   return ''
               if df_['LINHAPRODUCAO'] == 7:
                   return ''
               if df_['LINHAPRODUCAO'] == 8:
                   return ''
               if df_['LINHAPRODUCAO'] == 9:
                   return ''
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return ''
               if df_['LINHAPRODUCAO'] == 12:
                   return ''
               if df_['LINHAPRODUCAO'] == 13:
                   return ''
               if df_['LINHAPRODUCAO'] == 14:
                   return ''
               if df_['LINHAPRODUCAO'] == 15:
                   return ''
               if df_['LINHAPRODUCAO'] == 16:
                   return ''
               if df_['LINHAPRODUCAO'] == 17:
                   return ''
               if df_['LINHAPRODUCAO'] == 18:
                   return ''
               if df_['LINHAPRODUCAO'] == 19:
                   return ''
               if df_['LINHAPRODUCAO'] == 20:
                   return ''
               if df_['LINHAPRODUCAO'] == 21:
                   return ''
               if df_['LINHAPRODUCAO'] == 22:
                   return ''
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                    return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return '16'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return ''
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return ''
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_8'] = df_.apply(definindo_calibre_8, axis = 1)
        
        
        def definindo_calibre_9(df_):
            if df_['VARIEDADE'] == 'Palmer' or df_['VARIEDADE'] == 'Keitt':
               if df_['LINHAPRODUCAO'] == 1:
                   return ''
               if df_['LINHAPRODUCAO'] == 2:
                   return ''
               if df_['LINHAPRODUCAO'] == 3:
                   return ''
               if df_['LINHAPRODUCAO'] == 4:
                   return ''
               if df_['LINHAPRODUCAO'] == 5:
                   return ''
               if df_['LINHAPRODUCAO'] == 6:
                   return ''
               if df_['LINHAPRODUCAO'] == 7:
                   return ''
               if df_['LINHAPRODUCAO'] == 8:
                   return ''
               if df_['LINHAPRODUCAO'] == 9:
                   return ''
               if df_['LINHAPRODUCAO'] == 10:
                   return ''
               if df_['LINHAPRODUCAO'] == 11:
                   return ''
               if df_['LINHAPRODUCAO'] == 12:
                   return ''
               if df_['LINHAPRODUCAO'] == 13:
                   return ''
               if df_['LINHAPRODUCAO'] == 14:
                   return ''
               if df_['LINHAPRODUCAO'] == 15:
                   return ''
               if df_['LINHAPRODUCAO'] == 16:
                   return ''
               if df_['LINHAPRODUCAO'] == 17:
                   return ''
               if df_['LINHAPRODUCAO'] == 18:
                   return ''
               if df_['LINHAPRODUCAO'] == 19:
                   return ''
               if df_['LINHAPRODUCAO'] == 20:
                   return ''
               if df_['LINHAPRODUCAO'] == 21:
                   return ''
               if df_['LINHAPRODUCAO'] == 22:
                   return ''
               else:
                   return 'Sem configuração'
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
                if df_['LINHAPRODUCAO'] == 1:
                    return ''
                if df_['LINHAPRODUCAO'] == 2:
                   return 'Refugo'
                if df_['LINHAPRODUCAO'] == 3:
                   return ''
                if df_['LINHAPRODUCAO'] == 4:
                   return ''
                if df_['LINHAPRODUCAO'] == 5:
                   return ''
                if df_['LINHAPRODUCAO'] == 6:
                   return ''
                if df_['LINHAPRODUCAO'] == 7:
                   return ''
                if df_['LINHAPRODUCAO'] == 8:
                   return ''
                if df_['LINHAPRODUCAO'] == 9:
                   return ''
                if df_['LINHAPRODUCAO'] == 10:
                   return ''
                if df_['LINHAPRODUCAO'] == 11:
                   return ''
                if df_['LINHAPRODUCAO'] == 12:
                   return ''
                if df_['LINHAPRODUCAO'] == 13:
                   return ''
                if df_['LINHAPRODUCAO'] == 14:
                   return ''
                if df_['LINHAPRODUCAO'] == 15:
                   return ''
                if df_['LINHAPRODUCAO'] == 16:
                   return ''
                if df_['LINHAPRODUCAO'] == 17:
                   return ''
                if df_['LINHAPRODUCAO'] == 18:
                   return ''
                if df_['LINHAPRODUCAO'] == 19:
                   return ''
                if df_['LINHAPRODUCAO'] == 20:
                   return ''
                if df_['LINHAPRODUCAO'] == 21:
                   return ''
                if df_['LINHAPRODUCAO'] == 22:
                   return ''
                else:
                    return
                'Sem configuração'
       
        df_['CALIBRE_9'] = df_.apply(definindo_calibre_9, axis = 1)
        
      ################ OU ESTABALER UM PADRAO DE MEDIA DE ACORDO COM O QUE CAI NA LINHA JA DA CNOFIGURACAO 
      
        def peso_medio_linha(df_):
            if df_['VARIEDADE'] == 'Palmer':
               if df_['LINHAPRODUCAO'] == 1:
                   return 0
               if df_['LINHAPRODUCAO'] == 2:
                   return 0.5715
               if df_['LINHAPRODUCAO'] == 3:
                   return 0.8785
               if df_['LINHAPRODUCAO'] == 4:
                   return 0.5815
               if df_['LINHAPRODUCAO'] == 5:
                   return 0.8785
               if df_['LINHAPRODUCAO'] == 6:
                   return 0.5175
               if df_['LINHAPRODUCAO'] == 7:
                   return 0.5175
               if df_['LINHAPRODUCAO'] == 8:
                   return 0.5175
               if df_['LINHAPRODUCAO'] == 9:
                   return 0.5175
               if df_['LINHAPRODUCAO'] == 10:
                   return 0
               if df_['LINHAPRODUCAO'] == 11:
                   return 0.407
               if df_['LINHAPRODUCAO'] == 12:
                   return 0.407
               if df_['LINHAPRODUCAO'] == 13:
                   return 0.407
               if df_['LINHAPRODUCAO'] == 14:
                   return 0.458
               if df_['LINHAPRODUCAO'] == 15:
                   return 0.458
               if df_['LINHAPRODUCAO'] == 16:
                   return 0.458
               if df_['LINHAPRODUCAO'] == 17:
                   return 0.666
               if df_['LINHAPRODUCAO'] == 18:
                   return 0.500
               if df_['LINHAPRODUCAO'] == 19:
                   return 0.500
               if df_['LINHAPRODUCAO'] == 20:
                   return 0.593
               if df_['LINHAPRODUCAO'] == 21:
                   return 0.593
               if df_['LINHAPRODUCAO'] == 22:
                   return 0.593
               else:
                   return 0
            elif df_['VARIEDADE'] == 'Keitt':
                
               if df_['LINHAPRODUCAO'] == 1:
                   return 0
               if df_['LINHAPRODUCAO'] == 2:
                   return 0.641
               if df_['LINHAPRODUCAO'] == 3:
                   return 0.412
               if df_['LINHAPRODUCAO'] == 4:
                   return 0.412
               if df_['LINHAPRODUCAO'] == 5:
                   return 0.412
               if df_['LINHAPRODUCAO'] == 6:
                   return 0.412
               if df_['LINHAPRODUCAO'] == 7:
                   return 0.4575
               if df_['LINHAPRODUCAO'] == 8:
                   return 0.4575
               if df_['LINHAPRODUCAO'] == 9:
                   return 0.4575
               if df_['LINHAPRODUCAO'] == 10:
                   return 0.4575
               if df_['LINHAPRODUCAO'] == 11:
                   return 0.676
               if df_['LINHAPRODUCAO'] == 12:
                   return 0.484
               if df_['LINHAPRODUCAO'] == 13:
                   return 0.676
               if df_['LINHAPRODUCAO'] == 14:
                   return 0.5145
               if df_['LINHAPRODUCAO'] == 15:
                   return 0.5145
               if df_['LINHAPRODUCAO'] == 16:
                   return 0.5145
               if df_['LINHAPRODUCAO'] == 17:
                   return 0.604
               if df_['LINHAPRODUCAO'] == 18:
                   return 0.604
               if df_['LINHAPRODUCAO'] == 19:
                   return 0.604
               if df_['LINHAPRODUCAO'] == 20:
                   return 0.825
               if df_['LINHAPRODUCAO'] == 21:
                   return 0.825
               if df_['LINHAPRODUCAO'] == 22:
                   return 0.825
               else:
                   return 0
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
               if df_['LINHAPRODUCAO'] == 1:
                   return 0
               if df_['LINHAPRODUCAO'] == 2:
                   return 0.6483
               if df_['LINHAPRODUCAO'] == 3:
                   return 0.760
               if df_['LINHAPRODUCAO'] == 4:
                   return 0.5238
               if df_['LINHAPRODUCAO'] == 5:
                   return 0
               if df_['LINHAPRODUCAO'] == 6:
                   return 0.5985
               if df_['LINHAPRODUCAO'] == 7:
                   return 0.5985
               if df_['LINHAPRODUCAO'] == 8:
                   return 0.5985
               if df_['LINHAPRODUCAO'] == 9:
                   return 0.5985
               if df_['LINHAPRODUCAO'] == 10:
                   return 0
               if df_['LINHAPRODUCAO'] == 11:
                   return 0.4065
               if df_['LINHAPRODUCAO'] == 12:
                   return 0.4065
               if df_['LINHAPRODUCAO'] == 13:
                   return 0.4065
               if df_['LINHAPRODUCAO'] == 14:
                   return 0.461
               if df_['LINHAPRODUCAO'] == 15:
                   return 0.461
               if df_['LINHAPRODUCAO'] == 16:
                   return 0.461
               if df_['LINHAPRODUCAO'] == 17:
                   return 0.3335
               if df_['LINHAPRODUCAO'] == 18:
                   return 0.3335
               if df_['LINHAPRODUCAO'] == 19:
                   return 0.3335
               if df_['LINHAPRODUCAO'] == 20:
                   return 0.5185
               if df_['LINHAPRODUCAO'] == 21:
                   return 0.5185
               if df_['LINHAPRODUCAO'] == 22:
                   return 0.5185
               else:
                   return 0
        
        df_['PESO_MEDIO_LINHA'] = df_.apply(peso_medio_linha, axis = 1)
            
        def calibre_medio_linha(df_):
            if df_['VARIEDADE'] == 'Palmer':
               if df_['LINHAPRODUCAO'] == 1:
                   return 0
               if df_['LINHAPRODUCAO'] == 2:
                   return 10.8
               if df_['LINHAPRODUCAO'] == 3:
                   return 5
               if df_['LINHAPRODUCAO'] == 4:
                   return 9.5
               if df_['LINHAPRODUCAO'] == 5:
                   return 5
               if df_['LINHAPRODUCAO'] == 6:
                   return 8
               if df_['LINHAPRODUCAO'] == 7:
                   return 8
               if df_['LINHAPRODUCAO'] == 8:
                   return 8
               if df_['LINHAPRODUCAO'] == 9:
                   return 8
               if df_['LINHAPRODUCAO'] == 10:
                   return 0
               if df_['LINHAPRODUCAO'] == 11:
                   return 10
               if df_['LINHAPRODUCAO'] == 12:
                   return 10
               if df_['LINHAPRODUCAO'] == 13:
                   return 10
               if df_['LINHAPRODUCAO'] == 14:
                   return 9
               if df_['LINHAPRODUCAO'] == 15:
                   return 9
               if df_['LINHAPRODUCAO'] == 16:
                   return 9
               if df_['LINHAPRODUCAO'] == 17:
                   return 6
               if df_['LINHAPRODUCAO'] == 18:
                   return 9
               if df_['LINHAPRODUCAO'] == 19:
                   return 9
               if df_['LINHAPRODUCAO'] == 20:
                   return 7
               if df_['LINHAPRODUCAO'] == 21:
                   return 7
               if df_['LINHAPRODUCAO'] == 22:
                   return 7
               else:
                   return 0
            elif df_['VARIEDADE'] == 'Keitt':
                
               if df_['LINHAPRODUCAO'] == 1:
                   return 0
               if df_['LINHAPRODUCAO'] == 2:
                   return 10.8
               if df_['LINHAPRODUCAO'] == 3:
                   return 10
               if df_['LINHAPRODUCAO'] == 4:
                   return 10
               if df_['LINHAPRODUCAO'] == 5:
                   return 10
               if df_['LINHAPRODUCAO'] == 6:
                   return 10
               if df_['LINHAPRODUCAO'] == 7:
                   return 9
               if df_['LINHAPRODUCAO'] == 8:
                   return 9
               if df_['LINHAPRODUCAO'] == 9:
                   return 9
               if df_['LINHAPRODUCAO'] == 10:
                   return 9
               if df_['LINHAPRODUCAO'] == 11:
                   return 6
               if df_['LINHAPRODUCAO'] == 12:
                   return 10
               if df_['LINHAPRODUCAO'] == 13:
                   return 6
               if df_['LINHAPRODUCAO'] == 14:
                   return 8
               if df_['LINHAPRODUCAO'] == 15:
                   return 8
               if df_['LINHAPRODUCAO'] == 16:
                   return 8
               if df_['LINHAPRODUCAO'] == 17:
                   return 7
               if df_['LINHAPRODUCAO'] == 18:
                   return 7
               if df_['LINHAPRODUCAO'] == 19:
                   return 7
               if df_['LINHAPRODUCAO'] == 20:
                   return 5
               if df_['LINHAPRODUCAO'] == 21:
                   return 5
               if df_['LINHAPRODUCAO'] == 22:
                   return 5
               else:
                   return 0
            elif df_['VARIEDADE'] == 'Tommy Atkins':
                
               if df_['LINHAPRODUCAO'] == 1:
                   return 0
               if df_['LINHAPRODUCAO'] == 2:
                   return 9.75
               if df_['LINHAPRODUCAO'] == 3:
                   return 6
               if df_['LINHAPRODUCAO'] == 4:
                   return 10
               if df_['LINHAPRODUCAO'] == 5:
                   return 0
               if df_['LINHAPRODUCAO'] == 6:
                   return 7
               if df_['LINHAPRODUCAO'] == 7:
                   return 7
               if df_['LINHAPRODUCAO'] == 8:
                   return 7
               if df_['LINHAPRODUCAO'] == 9:
                   return 7
               if df_['LINHAPRODUCAO'] == 10:
                   return 0
               if df_['LINHAPRODUCAO'] == 11:
                   return 10
               if df_['LINHAPRODUCAO'] == 12:
                   return 10
               if df_['LINHAPRODUCAO'] == 13:
                   return 10
               if df_['LINHAPRODUCAO'] == 14:
                   return 9
               if df_['LINHAPRODUCAO'] == 15:
                   return 9
               if df_['LINHAPRODUCAO'] == 16:
                   return 9
               if df_['LINHAPRODUCAO'] == 17:
                   return 12
               if df_['LINHAPRODUCAO'] == 18:
                   return 12
               if df_['LINHAPRODUCAO'] == 19:
                   return 12
               if df_['LINHAPRODUCAO'] == 20:
                   return 8
               if df_['LINHAPRODUCAO'] == 21:
                   return 8
               if df_['LINHAPRODUCAO'] == 22:
                   return 8
               else:
                   return 0
        
        df_['CALIBRE_MEDIO_LINHA'] = df_.apply(calibre_medio_linha, axis = 1)
        
        
        ##################### REMOVENDO OUTLIERS     #####################
        
        
    #    def is_outlier(s):
     #       lower_limit = s.mean() - (s.std() * 1.5)
    #        upper_limit = s.mean() + (s.std() * 1.5)
    #        return ~s.between(lower_limit, upper_limit)

     #   df_ = df_[~df_.groupby(['VARIEDADE'])['CX_HORA'].apply(is_outlier)]
         
         

         ######## CRIAR 3 COLUNAS - 
         # CX POR EMBALADEIRA
         # HR ACUMULADA 
         # A DIVISA0 DA CX ACU POR HR ACU EM CADA LINHA DAS EMBALADEIRAS



        ### FAZER POR LINHA, POIS CADA LINHA VOU TER UM CALIBRE OU MEDIA DE CALIBRE QUE DANILO VAI ENTREGAR

        



        #### ABALISE GERAL MEDIA TA COM ALGUM PROBLEMA VOU FOCAR PRIMEIRO NO DESEMPENHO INDIVIDUAL
        #### FAZER UMA COLUNA DAS MULHERS COM MAIORES DP E PEGAR UM HEAD
        #### 

        ## FAZER UMA COMPARACAO INDIVIDUAL - QUEM INDIVIDUALMENTE ESTA MAIS INCONSTANTE E FORA DA SUA MEDIA ?
        ## FAZER UMA COMPARACAO POR CALIBRE DA VARIEDADE - QUEM DENTRE OS CLAIBRES ESTA MAIS DESTOANTE DA NORMALIZADADE
        ## E TAMBEM PEGAR AS PRINCIPAIS
        ## CREIO QUE UMA CARTA DE CONTROLE RESOLVE TUDO ISSO
        ## MAS PODEMOS ABORDAR OUTROS GRAFICOS
        #
        
        ## OBJETVIO FAZER UMA LINHA DO TEMPO ACUULADO POR EMBALADEIRA

        ### COLOCAR UM METRICS COM A MEDIA DE TON/HR DE CADA VARIEDADE É BOM
        ### PODE SER SEÇOES DIFENTES MOSTRANDO O DESEMEPNHOS DAS EMBALADEIRAS NESSE MTERIC POR ALIBRE

############## DEIFNINDO RITMO PADRAO NORMALIZADO DOS CALIBRES DE CADA VARIEDADE ##############
        
        filtro_nada = df_['VARIEDADE'] != 'NADA'
        df_ = df_[filtro_nada]

        df_ = df_.dropna()


        def is_outlier(s):
            lower_limit = s.mean() - (s.std() * 2)
            upper_limit = s.mean() + (s.std() * 2)
            return ~s.between(lower_limit, upper_limit)

        df_normalizado = df_[~df_.groupby(['VARIEDADE','CALIBRE_1'])['CX_acu_HR_acu'].apply(is_outlier)]

        

        ## TENHO O MEU IDEAL MEDIO COM BASE NA VARIEDADE E LINHA == CALIBRE 
        ## DIVIDIR OS DADOS POR VARIEDADE

        




        # filtro_keitt = df_normalizado['VARIEDADE'] == 'Keitt'
        # df_norm_keitt = df_normalizado[filtro_keitt]

        # filtro_palmer = df_normalizado['VARIEDADE'] == 'Palmer'
        # df_norm_palmer = df_normalizado[filtro_palmer]

        # filtro_Tommy = df_normalizado['VARIEDADE'] == 'Tommy Atkins'
        # df_norm_tommy = df_normalizado[filtro_Tommy]

        
        
        #### NAO DA PRA COLOCAR O RITMO PADRAO POIS A GENTE N SABE SE É COM PAPEL OU SEM PAPEL
        #### VOU TER QUE FAZER PELA MEDIA DO CALIBRE DA VARIEDADE MESMO FAZENDO OS FILTROS
        #### O INTERESSANTE ERA SE A GENTE JA COLOCASE COMO META A ER POIS N IREMOS SABER SE ESTAO MUITO FORA OU DENTRO DO PADRAO



        fig = px.line(df_normalizado, x = 'LEH_DATA', y = 'CX_acu_HR_acu', facet_col = 'VARIEDADE',facet_row= 'CALIBRE_1', color = 'PESSOA',category_orders = {'VARIEDADE':['Keitt','Palmer','Tommy Atkins']})
        fig.update_layout(height = 900, width = 1900)


        # fig.add_hline(df_norm_keitt['CX_acu_HR_acu'].mean(), line_color = 'blue', line_dash="dot",  annotation_text="AVG KEITT", annotation_font_color="blue",row=3)
        # fig.add_hline(df_norm_keitt['CX_acu_HR_acu'].mean() + (df_norm_keitt['CX_acu_HR_acu'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-K", annotation_font_color="black",row=3)
        # fig.add_hline(df_norm_keitt['CX_acu_HR_acu'].mean() - (df_norm_keitt['CX_acu_HR_acu'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-K", annotation_font_color="black",row=3)
        
        # fig.add_hline(df_norm_palmer['CX_acu_HR_acu'].mean(), line_color = 'blue', line_dash="dot",  annotation_text="AVG PALMER", annotation_font_color="blue",row=2)
        # fig.add_hline(df_norm_palmer['CX_acu_HR_acu'].mean() + (df_norm_palmer['CX_acu_HR_acu'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-P", annotation_font_color="black",row=2)
        # fig.add_hline(df_norm_palmer['CX_acu_HR_acu'].mean() - (df_norm_palmer['CX_acu_HR_acu'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-P", annotation_font_color="black",row=2)

        # fig.add_hline(df_norm_tommy['CX_acu_HR_acu'].mean(), line_color = 'green', line_dash="dot",  annotation_text="AVG TOMMY", annotation_font_color="green",row=1)
        # fig.add_hline(df_norm_tommy['CX_acu_HR_acu'].mean() + (df_norm_tommy['CX_acu_HR_acu'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LS-T", annotation_font_color="black",row=1)
        # fig.add_hline(df_norm_tommy['CX_acu_HR_acu'].mean() - (df_norm_tommy['CX_acu_HR_acu'].std() * 2), line_color = 'black', line_dash="dot",  annotation_text="LI-T", annotation_font_color="black",row=1)

        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("CALIBRE_1=", "")))
        fig.update_yaxes(matches=None)
        fig.update_traces(mode="markers+lines", hovertemplate=None, textfont_size=12, cliponaxis=False, marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
        fig

        ### VAMOS FAZER AGORA O GRAFICO DE BARRAS COM AS 3 PIORES POR CALIBRE DA VARIEDADE EM MEDIA NO DIA
        ### OU SEJA FAZER UM SORT INVERSO E PEGAR O HEAD DAS 3
        ## VAMOS FAZER O EXEMPLO PRA PALMER QUE É QUEM A GENTETEM MAIS DADOS


        filtro_palmer = df_normalizado['VARIEDADE'] == 'Palmer'
        df_norm_palmer = df_normalizado[filtro_palmer]






        ### E OUTRA ABA COM COM AS QUE TIERAM MAIORES QUEDAS PERCENTUAIS EM RELAÇÇÂO AO SEU PROPO RITMO







        df_['TON_HR_ACU'] =  (df_['CX_acu_HR_acu'] * df_['CALIBRE_MEDIO_LINHA'] * df_['PESO_MEDIO_LINHA']) / 1000
            
            
        ######## PARA ACHAR A TONELADA POR HORA EU MULTIPLO A QUANTIDADE DE CAIXAS PELO CALIBRE E VOU TER A QTD DE FRUTOS DAQUELA MULHER
        ######## EM UMA HORA. PEGO ESSA QUANTIDADE DE FRUTOS E MULTIPLICO PELO PESO MÉDIO DAQUELE CALIBRE
        ######## E AI EU TENHO A TONELADA POR HORA DAQUELA MULHER PARA AQUELE CALIBRE
        ######## COM ISSO, EU ACHO A MÈDIA DE TONELADA POR HRS DE CADA MULHER
        ######## E SOMO TODAS ESSAS MÉDIAS E EU ACHO A TON/HR DAS EMBALADEIRAS TOTAIS
        
        ######## POR CALIBRE VARIEDADE TENHO QUE ESPERAR DANILO AINDA

        df_





        #### GRAFICO DE LINHA E BOXPLOT

        # df_

        # st.download_button( label = 'Baixar Configuração (csv)',data = df_.to_csv(), mime = 'text/csv')

        # st.write(len(df_['PESSOA'].value_counts()))
        # saa = df_['CX_HORA'].sum()
        # saa
        
       
        # caixas_hr = df_['CX_acu_HR_acu'].sum() / len(df_['PESSOA'].value_counts())



        # df_piv = pd.pivot_table(df_, index = ['VARIEDADE','HORA_MIN','PESSOA'], values = ['CX_acu_HR_acu','TON_HR_ACU'], aggfunc = np.mean)
        # df_piv = df_piv.reset_index()
        
        
        
        
        # fig = px.line(df_piv, x = 'HORA_MIN', y = 'CX_acu_HR_acu',  color = 'VARIEDADE')
        # fig.update_xaxes(categoryorder='category ascending')
        # fig.update_layout(height = 500, width = 1800)
        # st.plotly_chart(fig)
        
        
        # fig = px.box(df_piv, y = 'CX_acu_HR_acu', facet_col = 'VARIEDADE', color = 'VARIEDADE',points="all", hover_name = 'PESSOA')
        # fig.update_layout(height = 500, width = 1800)
        # st.plotly_chart(fig)
        

        
        
        ###### EMBALADEIRA AQUI NAO SERVE PARA FIM DE COMPARACAO ENTRE EMBALADEIRAs APENAS PARA CALCULAR A CAPACIDADE DE TON/HR DAS MULHERES ############
        
        
        # df_piv_embala = pd.pivot_table(df_, index = ['VARIEDADE','PESSOA'], values = ['CX_acu_HR_acu','TON_HR_ACU'], aggfunc = np.mean)
        # df_piv_embala = df_piv_embala.reset_index()
        # df_piv_embala =  df_piv_embala.sort_values(['CX_acu_HR_acu'], ascending=False)
        # df_piv_embala
        
        
        # df_piv_embala_2 = pd.pivot_table(df_piv_embala, index = ['VARIEDADE','PESSOA'], values = ['CX_acu_HR_acu','TON_HR_ACU'], aggfunc = np.sum)
        # df_piv_embala_2
        
        
        # af = df_piv_embala_2.groupby(['VARIEDADE'])['TON_HR_ACU'].sum()
        # af
        
        # #st.write('Ritmo atual embaladeiras T/H', toneladas_horas_atuais)
        
        
        # fig = px.bar(df_piv_embala, x = 'PESSOA', y = 'CX_acu_HR_acu', facet_row = 'VARIEDADE', color  = 'VARIEDADE')
        # fig.update_yaxes(categoryorder='category ascending')
        # fig.update_layout(height = 750, width = 1800)
        # st.plotly_chart(fig)
        

if selected == 'Etiquetas':

    import sqlite3
    import socket
    


    from pathlib import Path    
    import pandas as pd  # pip install pandas openpyxl
    import plotly.express as px  # pip install plotly-express
    import streamlit as st  # pip install streamlit

    from modulos_dash.balanceamento.funcoes_atualizar_MAF.modulos_import_func_MAF import *



    st.success('### Controle de etiqueta')


    url = 'http://177.52.21.58:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH'
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


    url_maf = 'http://177.52.21.58:3000/backend/maf/percentuaisCalibre'
    dataframe_MAF = pd.read_json(url_maf)

    controle_maf = dataframe_MAF['CONTROLE_MEGA'][0]
    variedade = dataframe_MAF['VARIEDADE'][0]


    ### FAZER UM INSERTE NO BANCO AQUI QUE SE O CONTROLE MEGA diferente DO CONTROLE BANCO
    ### ZERAR TODOS OS VALORES

    conn = sqlite3.connect(r"C:\Users\danillo.xavier\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
    cursor = conn.cursor()

    df_sql = pd.read_sql_query("""SELECT * FROM import22 """, conn)
    controle_banco = df_sql['controle_db'][0]

    conn.close()

    caixas_totais = round(dataframe_MAF['QTD_CAIXAS'][0])
    st.error(f'###### Controle atual: {controle_maf} / Quantidade de caixas totais: {caixas_totais}')

    calibre = dataframe_MAF['CALIBRE'][0]
    calibre = calibre.split('C')[1]
    calibre = calibre.split(' ')[0]
    calibre = int(calibre)

   ######### RESETANDO VALORES SE O CONTROLE 

    if controle_banco != controle_maf:
        url_maf = 'http://177.52.21.58:3000/backend/maf/percentuaisCalibre'
        dataframe_MAF = pd.read_json(url_maf)
        caixas_totais = round(dataframe_MAF['QTD_CAIXAS'][0])

        #C:\Users\danillo.xavier\Desktop\planilha_denilton\banco_impressora


        conn = sqlite3.connect(r"C:\Users\danillo.xavier\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
        ## CONSULTAR AQUI O TOTAL DE ETIQUETAS ANTES DE EXCLUIR TUDO DA BASE PRA SALVAER EM UMA VARIAVEL


        df_sql_22 = pd.read_sql_query("""SELECT * FROM import22 """, conn)
        total_etiquetas = df_sql_22['total_etiquetas'][0]



        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM import22; 
        """)
        
        caixas_totais = caixas_totais
        caixas_restantes = caixas_totais
        controle_maf = controle_maf
        etiquetas_impressas = 0
        controle_db = controle_maf

        cursor.execute(f"""
        INSERT INTO import22 (caixas_totais, caixas_restantes, controle_maf, etiquetas_impressas, controle_db, total_etiquetas)
        VALUES ({caixas_totais}, {caixas_restantes} ,{controle_maf} ,{etiquetas_impressas}, {controle_db}, {total_etiquetas})
        """)

        conn.commit()
        conn.close()

    
    else:
        url_maf = 'http://177.52.21.58:3000/backend/maf/percentuaisCalibre'
        dataframe_MAF = pd.read_json(url_maf)
        caixas_totais = round(dataframe_MAF['QTD_CAIXAS'][0])


        conn = sqlite3.connect(r"C:\Users\danillo.xavier\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
        cursor = conn.cursor()
        
        df_sql_inicio = pd.read_sql_query("""SELECT * FROM import22 """, conn)

        caixas_totais = caixas_totais
        caixas_restantes = caixas_totais
        controle_maf = df_sql_inicio['controle_maf'][0]
        etiquetas_impressas = df_sql_inicio['etiquetas_impressas'][0]
        controle_db = df_sql_inicio['controle_db'][0]


        total_etiquetas = df_sql_inicio['total_etiquetas'][0]



        cursor.execute("""
        DELETE FROM import22; 
        """)

        cursor.execute(f"""
        INSERT INTO import22 (caixas_totais, caixas_restantes, controle_maf, etiquetas_impressas, controle_db, total_etiquetas)
        VALUES ({caixas_totais}, {caixas_restantes} ,{controle_maf} ,{etiquetas_impressas}, {controle_db}, {total_etiquetas})
        """)

        conn.commit()
        conn.close()
    




    with st.form('Envio de etiqueta'):
        import math

        coluna1, coluna2, coluna3, coluna4 = st.columns([0.5,1,1,0.5])
        
        # coluna2.info('### Selecione o calibre')

        # calibre = coluna2.selectbox('Calibre:',
        #                             options = ['4','5','6','7','8','9','10','12','14','16'])


        conn = sqlite3.connect(r"C:\Users\danillo.xavier\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
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


        quantidade_ = coluna2.text_input('Quantidade de linhas para impressão:', key = 'qtd', value = 0)

        quantidade_ = int(quantidade_)
        quantidade_ = (quantidade_) / (2)
        quantidade_ = math.ceil(quantidade_)
        quantidade_ = int(quantidade_)
        

        #### ANALISANDO SE QUANTIDADE TA MAIOR DO QUE O RESTANTE NO BANCO
        
        
        if (quantidade_ > quantidade_) or (quantidade_ > 30):

             st.write('##### QUANTIDADE DE IMPRESSÃO MAIOR DO QUE A PERMITIDA OU O RESTANTE PARA O CONTROLE !!')
             st.write('###### AJUSTANDO NOVO VALOR PARA O MÍNIMO DE 30 !!')
             quantidade_ = 30


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
        ^PR2,2
        ~SD25
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
        ^FO5,144^GFA,241,3936,48,:Z64:eJzt17EJwzAQheEXDLkuWsDYK7hMYcgqGcGlq6DRPIpG0ACGi0bQTwi4uKs/hAsX75fMu6+oXT93bxw8716l+VT3pWZfud/rI4Hn28fkWyXejqEQPxTLxKsa4toS8/vE/DoyP67MT0/mH9TvzKeNebuaR79z8yV8+PDhw4cP/7N/Q3+1/UD9wvz933uP7k+6b+l+pvuc7n/aF7RfaB/R/sJ9N5PePHmfwv79AgsfSKo=:B069
        ^FT0,47^A0N,17,18^FB388,1,4,C^FH\^CI28^FDProduct: Certified Mangoes         Origin:Brazil^FS^CI27
        ^FT0,68^A0N,17,18^FB388,1,4,C^FH\^CI28^FDPacked by {empresa} ^FS^CI27
        ^FT0,89^A0N,17,18^FB388,1,4,C^FH\^CI28^FD{razao_agrodan} ^FS^CI27
        ^FT0,110^A0N,17,18^FB388,1,4,C^FH\^CI28^FD{endereco}^FS^CI27
        ^FT0,131^A0N,17,18^FB388,1,4,C^FH\^CI28^FD{cidade}^FS^CI27
        ^FT191,33^A0N,17,18^FH\^CI28^FDCGC 12.786.836/0001-42^FS^CI27
        ^FT18,31^A0N,17,18^FH\^CI28^FDGGN 4049929700871^FS^CI27'
        ^FT18,165^A0N,17,18^FH\^CI28^FDBatch ^FS^CI27
        ^FT18,186^A0N,17,18^FH\^CI28^FDNumber:^FS^CI27
        ^FT287,185^A0N,17,18^FH\^CI28^FDSize:{calibre2}^FS^CI27
        ^FT20,84^A0N,17,18^FH\^CI28^FDClass {qualidade}^FS^CI27
        ^FT0,215^A0N,14,15^FB546,1,4,C^FH\^CI28^FDWaxed with:E914 and E904^FS^CI27
        ^FO1,8^GFA,297,6812,52,:Z64:eJzt2bENwjAQBdBDKdyRBRBZgTIFUlZhBMqUHo1RMkJKCoTBdgSi4v4vUJD+FefGT6dYSvPPLCR3zbaUn6QUKwHGpHStpruZu8K9nkP0GxvqAYwxay+5b+Yv1z6qmd7dW3VCiIixsRiIWJ9bi5ljbnvMlOs7zGxfw/xVPqXHTGDNCJr4bGfMNGs30K+wmElGRkZGRkZGRkZGRkZGRkZG5q/NiTBrzrgYcwBNbr/KLZlMlclumYyYyaIDZsqTMdk6k+EzuwJmJ0HtPjpkL7PsWJhdDrEzegCZraO2:5CC2
        ^FO421,144^GFA,241,3936,48,:Z64:eJzt17EJwzAQheEXDLkuWsDYK7hMYcgqGcGlq6DRPIpG0ACGi0bQTwi4uKs/hAsX75fMu6+oXT93bxw8716l+VT3pWZfud/rI4Hn28fkWyXejqEQPxTLxKsa4toS8/vE/DoyP67MT0/mH9TvzKeNebuaR79z8yV8+PDhw4cP/7N/Q3+1/UD9wvz933uP7k+6b+l+pvuc7n/aF7RfaB/R/sJ9N5PePHmfwv79AgsfSKo=:B069
        ^FT405,47^A0N,17,18^FB410,1,4,C^FH\^CI28^FDProduct: Certified Mangoes         Origin:Brazil^FS^CI27
        ^FT405,68^A0N,17,18^FB410,1,4,C^FH\^CI28^FDPacked by {empresa} ^FS^CI27
        ^FT405,89^A0N,17,18^FB410,1,4,C^FH\^CI28^FD{razao_agrodan}^FS^CI27
        ^FT405,110^A0N,17,18^FB410,1,4,C^FH\^CI28^FD{endereco}^FS^CI27
        ^FT405,131^A0N,17,18^FB410,1,4,C^FH\^CI28^FD{cidade}^FS^CI27
        ^FT607,33^A0N,17,18^FH\^CI28^FDCGC 12.786.836/0001-42^FS^CI27
        ^FT434,31^A0N,17,18^FH\^CI28^FDGGN 4049929700871^FS^CI27
        ^FT434,165^A0N,17,18^FH\^CI28^FDBatch ^FS^CI27
        ^FT434,186^A0N,17,18^FH\^CI28^FDNumber:^FS^CI27
        ^FT703,185^A0N,17,18^FH\^CI28^FDSize:{calibre2}^FS^CI27
        ^FT436,84^A0N,17,18^FH\^CI28^FDClass {qualidade}^FS^CI27
        ^FT563,215^A0N,14,15^FB252,1,4,C^FH\^CI28^FDWaxed with:E914 and E904^FS^CI27
        ^FO417,8^GFA,297,6812,52,:Z64:eJzt2bENwjAQBdBDKdyRBRBZgTIFUlZhBMqUHo1RMkJKCoTBdgSi4v4vUJD+FefGT6dYSvPPLCR3zbaUn6QUKwHGpHStpruZu8K9nkP0GxvqAYwxay+5b+Yv1z6qmd7dW3VCiIixsRiIWJ9bi5ljbnvMlOs7zGxfw/xVPqXHTGDNCJr4bGfMNGs30K+wmElGRkZGRkZGRkZGRkZGRkZG5q/NiTBrzrgYcwBNbr/KLZlMlclumYyYyaIDZsqTMdk6k+EzuwJmJ0HtPjpkL7PsWJhdDrEzegCZraO2:5CC2
        ^FT82,183^A0N,34,33^FH\^CI28^FD{controle_maf} L-{num_semana}{dia_semana}^FS^CI27
        ^FT17,221^A0N,39,38^FH\^CI28^FD{variedade}^FS^CI27
        ^FT498,183^A0N,34,33^FH\^CI28^FD{controle_maf} L-{num_semana}{dia_semana}^FS^CI27
        ^FT433,221^A0N,39,38^FH\^CI28^FD{variedade}^FS^CI27
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


                

                conn = sqlite3.connect(r"C:\Users\danillo.xavier\Desktop\planilha_denilton\banco_impressora\Chinook.db", timeout=15)
                cursor = conn.cursor()

                

                df_sql = pd.read_sql_query("""SELECT * FROM import22 """, conn)


                etiquetas_impressas2 = df_sql['etiquetas_impressas'][0] + (quantidade_ * 2 )
                caixas_restantes = df_sql['caixas_restantes'][0] - etiquetas_impressas2 




                total_etiquetas_2 = df_sql['total_etiquetas'][0] + etiquetas_impressas2




                cursor.execute("""
                DELETE FROM import22; 
                """)

                cursor.execute(f"""
                INSERT INTO import22 (caixas_totais, caixas_restantes, controle_maf, etiquetas_impressas, controle_db, total_etiquetas)
                VALUES ({caixas_totais}, {caixas_restantes},{controle_maf}, {etiquetas_impressas2}, {controle_db}, {total_etiquetas_2})
                """)
                
                caixas_restantes_graph = caixas_restantes

                conn.commit()
                st.write('Dados inseridos com sucesso no banco')
                conn.close()


                st.write('Etiquetas impressas com sucesso!')   
                st.write(caixas_restantes) 

                

                #time.sleep(3)
                #st.stop()   

            except:
                st.write(caixas_restantes)
                st.write("Falha na conexão com a impressora !")
                #time.sleep(10)
            time.sleep(0.3)
            st.experimental_rerun()















