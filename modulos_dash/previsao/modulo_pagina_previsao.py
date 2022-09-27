from base64 import b16decode
from math import ceil
from ipython_genutils.py3compat import buffer_to_bytes
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
from torch import true_divide
from PIL import Image

def previsao_dash():
    img = Image.open('agrodn.png')
    newsize = (380,110)
    img2 = img.resize(newsize)

        ########## JANELA LATERAL ##########

    st.sidebar.image(img2, use_column_width=True)
    st.sidebar.title('Menu')
    st.sidebar.markdown('Escolha a informação para visualizar:')
        


    @st.experimental_memo
    def get_data() -> pd.DataFrame:
        return  pd.read_excel('C:/Users/bernard.collin/Desktop/planilha_denilton/pred_semanas/df_cleanref_TALHAO.xlsx')

    df_comportamento_qualidade = get_data()

    @st.experimental_memo
    def get_data2() -> pd.DataFrame:
        return pd.read_excel('C:/Users/bernard.collin/Desktop/planilha_denilton/pred_semanas/Comportamento_calibres_TALHAO.xlsx')

    df_comportamento_calibres_TALHAO = get_data2()



    pagina_selecionada = st.sidebar.radio('', ['Históricos','Previsão'])


############################ COLOCAR UM IF DE SE TALHAO DO CONTROLE X IS NOT IN EU RETORNO A PARTE DE VARIEDADE ############################
    
    if  pagina_selecionada == 'Históricos':
        
################### HISTORICO TALHAO ###################


        st.success('#### Histórico por talhão')

        dd = df_comportamento_calibres_TALHAO.groupby('TALHAO').FAZENDA.value_counts()
        ee = pd.DataFrame(dd)
        ee = ee.drop(columns = ['FAZENDA'])
        ee = ee.reset_index()
        ee = ee.drop(columns = ['FAZENDA'])
        lista_talhoes = ee


        coluna_t1, coluna_t2, coluna_t3 = st.columns([1,1,1])


        Talhao = coluna_t1.selectbox('Escolha o talhao', lista_talhoes, key = 'Escolher talhao')

        
        input_Talhao = str(Talhao)
        filtro_graph = df_comportamento_calibres_TALHAO['TALHAO'] == input_Talhao
        dataset_talhao = df_comportamento_calibres_TALHAO[filtro_graph]

        lista_controle_var_talha = pd.unique(dataset_talhao['Ordem_controle'])
        lista_controle_var_talha = pd.DataFrame(lista_controle_var_talha)
        lista_controle_var_talha.rename(columns = {0:'Ordem_controle'}, inplace = True)

        def ordem_num(lista_controle_var_talha):
            if lista_controle_var_talha['Ordem_controle'] == 'Primeiro Controle':
                return 1
            elif lista_controle_var_talha['Ordem_controle'] == 'Segundo Controle':
                return 2
            elif lista_controle_var_talha['Ordem_controle'] == 'Terceiro Controle':
                return 3
            elif lista_controle_var_talha['Ordem_controle'] == 'Quarto Controle':
                return 4

        lista_controle_var_talha['Ordem'] = lista_controle_var_talha.apply(ordem_num, axis = 1)
        lista_controle_var_talha = lista_controle_var_talha.sort_values('Ordem')
        
        Ordem_control_talha = coluna_t2.selectbox('Escolha a ordem do controle', lista_controle_var_talha, key = 'Escolher controle talhao')
        input_ordem_control_talha = str(Ordem_control_talha)



        # fazer uma lista de talhao da base de qualidade


        lista_talhoes_quality = pd.unique(df_comportamento_qualidade['TALHAO'])
        lista_talhoes_quality = pd.DataFrame(lista_talhoes_quality)
        lista_talhoes_quality.rename(columns = {0:'TALHAO'}, inplace = True)


        ## ou seja, se meu talhao, nao estiver dentro desta lista, faço o filtro por variedade, se nao, por talhao


        



        result_talha = lista_talhoes_quality.TALHAO.isin([input_Talhao]).any().any()
        
        if result_talha:
            filtro_graph_quality = df_comportamento_qualidade['TALHAO'] == input_Talhao
            dataset_quality_3 = df_comportamento_qualidade[filtro_graph_quality]

        else:

            filtro_talha = df_comportamento_calibres_TALHAO['TALHAO'] == Talhao
            df_filtrado = df_comportamento_calibres_TALHAO[filtro_talha]

            df_filtrado_2 = df_filtrado.groupby('TALHAO')['VARIEDADE'].value_counts()
            df_filtrado_2 = pd.DataFrame(df_filtrado_2)
            df_filtrado_2.rename(columns = {'VARIEDADE':'cont'}, inplace = True)
            df_filtrado_2 = df_filtrado_2.reset_index()
        
            variety = df_filtrado_2['VARIEDADE'][0]


            filtro_graph_quality = df_comportamento_qualidade['VARIEDADE'] == variety
            dataset_quality_3 = df_comportamento_qualidade[filtro_graph_quality]


        filtro_graph = dataset_talhao['Ordem_controle'] == input_ordem_control_talha
        dataset_talhao = dataset_talhao[filtro_graph]



        ### FAZER UM FILTRO AQUI SE O TALHAO NAO ESTIVER NA LISTA DE TALHAO DA BASE DE QUALIDADE, FILTRAR POR QUALIDADE

    

        filtro_graph_control_quali = dataset_quality_3['Ordem_controle'] == input_ordem_control_talha
        dataset_quality_4 = dataset_quality_3[filtro_graph_control_quali]
        dataset_quality_piv = pd.pivot_table(dataset_quality_4, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['Ordem_controle'], aggfunc = np.mean)
        dataset_quality_piv = dataset_quality_piv.reset_index()
    

        dataset_quality_piv = dataset_quality_piv.drop(columns = ['Ordem_controle'])
        dataset_quality_piv['TOT_PRIMEIRA'] = dataset_quality_piv['TOT_PRIMEIRA'].astype(str)
        dataset_quality_piv['TOT_SEGUNDA'] = dataset_quality_piv['TOT_SEGUNDA'].astype(str)
        dataset_quality_piv['TOT_TERCEIRA'] = dataset_quality_piv['TOT_TERCEIRA'].astype(str)
        dataset_quality_piv['TOT_REFUGO'] = dataset_quality_piv['TOT_REFUGO'].astype(str)
        dataset_quality_piv = dataset_quality_piv[['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO']]
        dataset_quality_piv = dataset_quality_piv.T
        dataset_quality_piv = dataset_quality_piv.reset_index()
        dataset_quality_piv.rename(columns = {'index':'Qualidade',0:'Percentual', 1:'Percentual', 2:'Percentual', 3:'Percentual'}, inplace = True)
        dataset_quality_piv['Percentual'] = dataset_quality_piv['Percentual'].astype(float)
        def mudanca_nomes_qualidades(dataset_quality_piv):
            if dataset_quality_piv['Qualidade'] == 'TOT_PRIMEIRA':
                return '1º'
            elif dataset_quality_piv['Qualidade'] == 'TOT_SEGUNDA':
                return '2º'
            elif dataset_quality_piv['Qualidade'] == 'TOT_TERCEIRA':
                return '3º'
            elif dataset_quality_piv['Qualidade'] == 'TOT_REFUGO':
                return 'REF'
        dataset_quality_piv['Qualidade'] = dataset_quality_piv.apply(mudanca_nomes_qualidades, axis = 1)


        coluna_1, coluna_2 = st.columns(2)

        fig = px.histogram(dataset_talhao, x = 'VALOR_CALIBRE', y = 'Calibre', color = 'VALOR_CALIBRE', 
        category_orders={'VALOR_CALIBRE':['CALIBRE_5','CALIBRE_6','CALIBRE_7','CALIBRE_8','CALIBRE_9','CALIBRE_10','CALIBRE_12','CALIBRE_14']},
        histfunc = 'avg')
        fig.update_traces(marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
        coluna_1.info('##### Histórico de distribuição de calibre')
        coluna_1.plotly_chart(fig)
        
            
        fig = go.Figure(data=[go.Pie(labels = dataset_quality_piv['Qualidade'], values = dataset_quality_piv['Percentual'], marker_colors = px.colors.sequential.Emrld ,hole = .4, pull=0.03)])
        fig.update_traces(textposition='inside', textinfo='percent+label',textfont_size=17,marker=dict(line=dict(color='#000000', width=1)))
        coluna_2.info('##### Histórico dos percentuais de qualidade')
        coluna_2.plotly_chart(fig)

################################## HISTORICO VARIEDADE ##################################

        #filtro_graph_control = dataset_variedade['Ordem_controle'] == input_ordem_control
        #dataset_variedade_2 = dataset_variedade[filtro_graph_control]
        dd_var = df_comportamento_calibres_TALHAO.groupby('VARIEDADE').VARIEDADE.value_counts()
        dd_var = df_comportamento_calibres_TALHAO['VARIEDADE'].value_counts()
        ee_var = pd.DataFrame(dd_var)
        ee_var.rename(columns={'VARIEDADE':'REMOVER'}, inplace = True)
        ee_var = ee_var.reset_index()
        ee_var.rename(columns={'index':'VARIEDADE'}, inplace = True)
        lista_variedades = ee_var
        
        
        st.success('#### Histórico por variedade')
    

        filtro_talha = df_comportamento_calibres_TALHAO['TALHAO'] == Talhao
        df_filtrado = df_comportamento_calibres_TALHAO[filtro_talha]

        df_filtrado_2 = df_filtrado.groupby('TALHAO')['VARIEDADE'].value_counts()
        df_filtrado_2 = pd.DataFrame(df_filtrado_2)
        df_filtrado_2.rename(columns = {'VARIEDADE':'cont'}, inplace = True)
        df_filtrado_2 = df_filtrado_2.reset_index()
        

        variety = df_filtrado_2['VARIEDADE'][0]

        Variedade_ = coluna_t3.selectbox('Escolha a variedade', options = [variety, 'KEITT','KENT','PALMER','TOMMY'], key = 'Escolher variedade')
        input_variedade = str(Variedade_)
        input_variedade


        filtro_graph_var = df_comportamento_calibres_TALHAO['VARIEDADE'] == input_variedade
        dataset_variedade = df_comportamento_calibres_TALHAO[filtro_graph_var]


        lista_controle_var = pd.unique(dataset_variedade['Ordem_controle'])
        lista_controle_var = pd.DataFrame(lista_controle_var)
        lista_controle_var.rename(columns = {0:'Ordem_controle'}, inplace = True)
        def ordem_num(lista_controle_var):
            if lista_controle_var['Ordem_controle'] == 'Primeiro Controle':
                return 1
            elif lista_controle_var['Ordem_controle'] == 'Segundo Controle':
                return 2
            elif lista_controle_var['Ordem_controle'] == 'Terceiro Controle':
                return 3
            elif lista_controle_var['Ordem_controle'] == 'Quarto Controle':
                return 4
        lista_controle_var['Ordem'] = lista_controle_var.apply(ordem_num, axis = 1)
        lista_controle_var = lista_controle_var.sort_values('Ordem')






        filtro_graph_control = dataset_variedade['Ordem_controle'] == input_ordem_control_talha
        dataset_variedade_2 = dataset_variedade[filtro_graph_control]
        filtro_graph_quality = df_comportamento_qualidade['VARIEDADE'] == input_variedade
        dataset_quality = df_comportamento_qualidade[filtro_graph_quality]  
        filtro_graph_control_quali = dataset_quality['Ordem_controle'] == input_ordem_control_talha
        dataset_quality_2 = dataset_quality[filtro_graph_control_quali]
        dataset_quality2_piv = pd.pivot_table(dataset_quality_2, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['Ordem_controle'], aggfunc = np.mean)
        dataset_quality2_piv = dataset_quality2_piv.reset_index()
        dataset_quality2_piv = dataset_quality2_piv.drop(columns = ['Ordem_controle'])
        dataset_quality2_piv['TOT_PRIMEIRA'] = dataset_quality2_piv['TOT_PRIMEIRA'].astype(str)
        dataset_quality2_piv['TOT_SEGUNDA'] = dataset_quality2_piv['TOT_SEGUNDA'].astype(str)
        dataset_quality2_piv['TOT_TERCEIRA'] = dataset_quality2_piv['TOT_TERCEIRA'].astype(str)
        dataset_quality2_piv['TOT_REFUGO'] = dataset_quality2_piv['TOT_REFUGO'].astype(str)
        dataset_quality2_piv = dataset_quality2_piv.T
        dataset_quality2_piv = dataset_quality2_piv.reset_index()
        dataset_quality2_piv.rename(columns = {'index':'Qualidade',0:'Percentual', 1:'Percentual', 2:'Percentual', 3:'Percentual'}, inplace = True)
        dataset_quality2_piv['Percentual'] = dataset_quality2_piv['Percentual'].astype(float)

        def mudanca_nomes_qualidades(dataset_quality2_piv):
            if dataset_quality2_piv['Qualidade'] == 'TOT_PRIMEIRA':
                return '1º'
            elif dataset_quality2_piv['Qualidade'] == 'TOT_SEGUNDA':
                return '2º'
            elif dataset_quality2_piv['Qualidade'] == 'TOT_TERCEIRA':
                return '3º'
            elif dataset_quality2_piv['Qualidade'] == 'TOT_REFUGO':
                return 'REF'
        dataset_quality2_piv['Qualidade'] = dataset_quality2_piv.apply(mudanca_nomes_qualidades, axis = 1)


################################## GRÁFICOS   ##################################



        colunaa1, colunaa2 = st.columns(2)

        fig = px.histogram(dataset_variedade_2, x = 'VALOR_CALIBRE', y = 'Calibre', color = 'VALOR_CALIBRE', 
        category_orders={'VALOR_CALIBRE':['CALIBRE_5','CALIBRE_6','CALIBRE_7','CALIBRE_8','CALIBRE_9','CALIBRE_10','CALIBRE_12','CALIBRE_14']},
        histfunc = 'avg')
        #fig.update_layout(height = 400, width = 1600)
        fig.update_traces(marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
        colunaa1.info('##### Histórico de distribuição de calibre')
        colunaa1.plotly_chart(fig)

        fig = go.Figure(data=[go.Pie(labels = dataset_quality2_piv['Qualidade'], values = dataset_quality2_piv['Percentual'], marker_colors = px.colors.sequential.Emrld ,hole = .4, pull=0.03)])
        fig.update_traces(textposition='inside', textinfo='percent+label',textfont_size=17,marker=dict(line=dict(color='#000000', width=1)))
        colunaa2.info('##### Histórico dos percentuais de qualidade')
        colunaa2.plotly_chart(fig)        

################### VARIEDADE ACIMA ###################





        ############################     VARIEDADE      ############################




    if pagina_selecionada == 'Previsão':
        
        from sklearn.model_selection import train_test_split as tts
        from xgboost import XGBRegressor
        from sklearn.metrics import r2_score
        from category_encoders.ordinal import OrdinalEncoder



        ################################ TREINAMENTO DO MODELO ################################
        
        df5 = pd.read_excel('Data_set_final_modelo_pred.xlsx')


        
        x = df5.drop(columns = ['Calibre','conca','Unnamed: 0','SAFRA','TALHAO'])
        y = df5['Calibre']

        xtrain, xtest, ytrain, ytest = tts(x,y, test_size = 0.2, random_state = 0)
        enc1 = OrdinalEncoder(cols=['VALOR_CALIBRE','VARIEDADE'])

        enc1.fit(xtrain)

        xtrain_enc = enc1.transform(xtrain)

        xtest_enc = enc1.transform(xtest)
        
        xgb = XGBRegressor(max_depth = 4, n_estimators = 12)
        xgb.fit(xtrain_enc, ytrain)


        pred = xgb.predict(xtest_enc)


        error = pred - ytest
        output2 = enc1.inverse_transform(xtest_enc)
        output2['Real'] = ytest
        output2['Pred'] = pred
        output2['Error'] =  output2['Pred'] - output2['Real']



      ######################## CRIANDO LABELS PARA O MODELO ################################


        dd = df_comportamento_calibres_TALHAO.groupby('TALHAO').FAZENDA.value_counts()

        ee = pd.DataFrame(dd)
        ee = ee.drop(columns = ['FAZENDA'])
        ee = ee.reset_index()
        ee = ee.drop(columns = ['FAZENDA'])
        lista_talhoes = ee


    #    st.write('Escolha a variedade')
    #    st.write('Insira os percentuais históricos da última SAFRA')


    #    lista_var = ['TOMMY','KEITT','KENT','PALMER']
        #variedade_input2 = st.selectbox('Selecione a variedade', lista_var, key = 'Escolher var')
        ## AO SELECIONAR  TALHAO, VOU BUSCAR O SEU HISTORICO E SUA VARIEDADE

        ## CRIAR UMA BASE COM GROUPBY DE TALHAO E VARIEDADE SO
        # 

        talhao_input2 = st.selectbox('Selecione o talhão', lista_talhoes, key = 'Escolhertalhao__') 

        talhao_var = df_comportamento_calibres_TALHAO.groupby('TALHAO').VARIEDADE.value_counts()
        talhao_var = pd.DataFrame(talhao_var)
        
        talhao_var.rename(columns = {'VARIEDADE':'QUANTIDADE'}, inplace = True)
        talhao_var = talhao_var.reset_index()
        talhao_var = talhao_var.drop(columns = 'QUANTIDADE')
        

        variedade_talhao = talhao_var[talhao_var.TALHAO==talhao_input2].VARIEDADE.item()
        variedade_input2 = variedade_talhao
        

        ## pegar item (variedade) que é equivalente ao talhao selecionado
        #for i in df_comportamento_calibres_TALHAO['VARIEDADE']
        #talhao_input2


        ## QUERO RESGATAR APENAS O HSTORICO DO TALHAO PARA COLOCAR DE INPUT 
        ## E A VARIEDADE DESSE TALHAO PARA O INPUT TAMBEM


        if variedade_input2 == 'TOMMY':
            variedade_input = 3
        elif variedade_input2 == 'KEITT':
            variedade_input = 2
        elif variedade_input2 == 'KENT':
            variedade_input = 1
        elif variedade_input2 == 'PALMER':
            variedade_input = 4

        st.write(variedade_input2, variedade_input)
        
        if variedade_input == 1:
            value_5 = 4.71
            value_6 = 23.14
            value_7 = 26.28
            value_8 = 20.25
            value_9 = 9.09
            value_10 = 9.36
            value_12 = 6.96
            value_14 = 0.23

        elif variedade_input == 2:
            value_5 = 6.91
            value_6 = 22.34
            value_7 = 23.55
            value_8 = 20.83
            value_9 = 8.89
            value_10 = 9.29
            value_12 = 7.40
            value_14 = 0.57

        elif variedade_input == 3:
            value_5 = 0.11
            value_6 = 4.18
            value_7 = 9.62
            value_8 = 24.48
            value_9 = 18.52
            value_10 = 27.07
            value_12 = 15.50
            value_14 = 0.53

        elif variedade_input == 4:
            value_5 = 4.49
            value_6 = 17.28
            value_7 = 17.45
            value_8 = 23.37
            value_9 = 13.22
            value_10 = 15.84
            value_12 = 8.10
            value_14 = 0.25


        #### CONCENTRAÇÂO DO TALHAO
        #st.write(df_comportamento_calibres_TALHAO.columns)


        filtro = df_comportamento_calibres_TALHAO['Ordem_controle'] == 'Primeiro Controle'
        df_hist = df_comportamento_calibres_TALHAO[filtro]


        df_hist_1 = df_hist.groupby(['TALHAO','VALOR_CALIBRE']).Calibre.mean()
        df_hist_1 = pd.DataFrame(df_hist_1)
        df_hist_1 = df_hist_1.reset_index()
        
    
        
        filtro_talhao = df_hist_1['TALHAO'] == talhao_input2
        df_hist_2 = df_hist_1[filtro_talhao]
        
        

        value_5 =  df_hist_2[df_hist_2.VALOR_CALIBRE=='CALIBRE_5'].Calibre.item()
        value_6 =  df_hist_2[df_hist_2.VALOR_CALIBRE=='CALIBRE_6'].Calibre.item()
        value_7 =  df_hist_2[df_hist_2.VALOR_CALIBRE=='CALIBRE_7'].Calibre.item()
        value_8 =  df_hist_2[df_hist_2.VALOR_CALIBRE=='CALIBRE_8'].Calibre.item()
        value_9 =  df_hist_2[df_hist_2.VALOR_CALIBRE=='CALIBRE_9'].Calibre.item()
        value_10 =  df_hist_2[df_hist_2.VALOR_CALIBRE=='CALIBRE_10'].Calibre.item()
        value_12 =  df_hist_2[df_hist_2.VALOR_CALIBRE=='CALIBRE_12'].Calibre.item()
        value_14 =  df_hist_2[df_hist_2.VALOR_CALIBRE=='CALIBRE_14'].Calibre.item()
        

################################### QUALIDADE ################################################

        filtro_graph_quality = df_comportamento_qualidade['TALHAO'] == talhao_input2
        dataset_quality = df_comportamento_qualidade[filtro_graph_quality]

        dataset_quality_piv = pd.pivot_table(dataset_quality, values = ['TOT_PRIMEIRA','TOT_SEGUNDA','TOT_TERCEIRA','TOT_REFUGO'], index = ['Ordem_controle'], aggfunc = np.mean)
        dataset_quality_piv = dataset_quality_piv.reset_index()
        
        


        
        coluna1, coluna2, coluna3, coluna4, coluna5, coluna6, coluna7, coluna8 = st.columns(8)

        calibre_5 = coluna1.text_input('Calibre 5', value = round(value_5,2))
        calibre_6 = coluna2.text_input('Calibre 6', value = round(value_6,2))
        calibre_7 = coluna3.text_input('Calibre 7', value = round(value_7,2))
        calibre_8 = coluna4.text_input('Calibre 8', value = round(value_8,2))
        calibre_9 = coluna5.text_input('Calibre 9', value = round(value_9,2))
        calibre_10 = coluna6.text_input('Calibre 10', value = round(value_10,2))
        calibre_12 = coluna7.text_input('Calibre 12', value = round(value_12,2))
        calibre_14 = coluna8.text_input('Calibre 14', value = round(value_14,2))

        calibre_5 = float(calibre_5)
        calibre_6 = float(calibre_6)
        calibre_7 = float(calibre_7)
        calibre_9 = float(calibre_9)
        calibre_10 = float(calibre_10)
        calibre_12 = float(calibre_12)
        calibre_14 = float(calibre_14)
        calibre_8 = float(calibre_8)





        data_input = pd.DataFrame({
                                "VALOR_CALIBRE":[1,2,3,4,5,6,7,8]
                                }) 

        def historico(data_input):
            if data_input['VALOR_CALIBRE'] == 6:
                return calibre_5
            if data_input['VALOR_CALIBRE'] == 3:
                return calibre_6
            if data_input['VALOR_CALIBRE'] == 8:
                return calibre_7
            if data_input['VALOR_CALIBRE'] == 2:
                return calibre_8
            if data_input['VALOR_CALIBRE'] == 1:
                return calibre_9
            if data_input['VALOR_CALIBRE'] == 4:
                return calibre_10
            if data_input['VALOR_CALIBRE'] == 7:
                return calibre_12
            if data_input['VALOR_CALIBRE'] == 5:
                return calibre_14

        data_input['Historico_calibre'] = data_input.apply(historico, axis = 1)
        data_input['VARIEDADE'] = variedade_input

        data_input = data_input[['VARIEDADE','VALOR_CALIBRE','Historico_calibre']]


        pred = xgb.predict(data_input)
        data_input['Pred'] = pred
        
        def variedade_corr (data_input):
            if data_input['VARIEDADE'] == 3:
                return 'TOMMY'
            elif data_input['VARIEDADE'] == 2:
                return 'KEITT'
            elif data_input['VARIEDADE'] == 1:
                return 'KENT'
            elif data_input['VARIEDADE'] == 4:
                return 'PALMER'
        data_input['VARIEDADE'] = data_input.apply(variedade_corr, axis =1)  
            

        def calibre_correcao(data_input):
            if data_input['VALOR_CALIBRE'] == 6:
                return "Calibre_5"
            if data_input['VALOR_CALIBRE'] == 3:
                return "Calibre_6"
            if data_input['VALOR_CALIBRE'] == 8:
                return "Calibre_7"
            if data_input['VALOR_CALIBRE'] == 2:
                return "Calibre_8"
            if data_input['VALOR_CALIBRE'] == 1:
                return "Calibre_9"
            if data_input['VALOR_CALIBRE'] == 4:
                return "Calibre_10"
            if data_input['VALOR_CALIBRE'] == 7:
                return "Calibre_12"
            if data_input['VALOR_CALIBRE'] == 5:
                return "Calibre_14"

        data_input['VALOR_CALIBRE'] = data_input.apply(calibre_correcao, axis = 1)



        lista_control = ['Primeiro Controle','Segundo Controle','Terceiro Controle','Quarto Controle']
        ordem_controle = st.selectbox('Selecione a ordem do controle', lista_control, key = 'Escolher control')

        

        filtro = df_comportamento_calibres_TALHAO['VARIEDADE'] == variedade_input2
        df_comportamento_calibres_TALHAO = df_comportamento_calibres_TALHAO[filtro]

        


        agf = df_comportamento_calibres_TALHAO.groupby(['VALOR_CALIBRE','Ordem_controle'])['Calibre'].mean()
        agf = agf.reset_index()


        
########################## QUEDA DE PERCENTUAIS NO SEGUNDO CONTROLE  ##########################

        filtro_calibre_5 = agf['VALOR_CALIBRE'] == 'CALIBRE_5'
        agf_5 = agf[filtro_calibre_5]
        agf_5_queda_segunda = (agf_5[agf_5.Ordem_controle=='Segundo Controle'].Calibre.item()) / agf_5[agf_5.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda segunda cal 5:', agf_5_queda_segunda)

        filtro_calibre_6 = agf['VALOR_CALIBRE'] == 'CALIBRE_6'
        agf_6 = agf[filtro_calibre_6]
        agf_6_queda_segunda = (agf_6[agf_6.Ordem_controle=='Segundo Controle'].Calibre.item()) / agf_6[agf_6.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda segunda cal 6:', agf_6_queda_segunda)

        filtro_calibre_7 = agf['VALOR_CALIBRE'] == 'CALIBRE_7'
        agf_7 = agf[filtro_calibre_7]
        agf_7_queda_segunda = (agf_7[agf_7.Ordem_controle=='Segundo Controle'].Calibre.item()) / agf_7[agf_7.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda segunda cal 7:', agf_7_queda_segunda)

        filtro_calibre_8 = agf['VALOR_CALIBRE'] == 'CALIBRE_8'
        agf_8 = agf[filtro_calibre_8]
        agf_8_queda_segunda = (agf_8[agf_8.Ordem_controle=='Segundo Controle'].Calibre.item()) / agf_8[agf_8.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda segunda cal 8:', agf_8_queda_segunda)

        filtro_calibre_9 = agf['VALOR_CALIBRE'] == 'CALIBRE_9'
        agf_9 = agf[filtro_calibre_9]
        agf_9_queda_segunda = (agf_9[agf_9.Ordem_controle=='Segundo Controle'].Calibre.item()) / agf_9[agf_9.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda segunda cal 9:', agf_9_queda_segunda)

        filtro_calibre_10 = agf['VALOR_CALIBRE'] == 'CALIBRE_10'
        agf_10 = agf[filtro_calibre_10]
        agf_10_queda_segunda = (agf_10[agf_10.Ordem_controle=='Segundo Controle'].Calibre.item()) / agf_10[agf_10.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda segunda cal 10:', agf_10_queda_segunda)

        filtro_calibre_12 = agf['VALOR_CALIBRE'] == 'CALIBRE_12'
        agf_12 = agf[filtro_calibre_12]
        agf_12_queda_segunda = (agf_12[agf_12.Ordem_controle=='Segundo Controle'].Calibre.item()) / agf_12[agf_12.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda segunda cal 12:', agf_12_queda_segunda)

        filtro_calibre_14 = agf['VALOR_CALIBRE'] == 'CALIBRE_14'
        agf_14 = agf[filtro_calibre_14]
        agf_14_queda_segunda = (agf_14[agf_14.Ordem_controle=='Segundo Controle'].Calibre.item()) / agf_14[agf_14.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda segunda cal 14:', agf_14_queda_segunda)

########################## QUEDA DE PERCENTUAIS NO TERCEIRO CONTROLE  ##########################


        filtro_calibre_5 = agf['VALOR_CALIBRE'] == 'CALIBRE_5'
        agf_5 = agf[filtro_calibre_5]
        agf_5_queda_terceira = (agf_5[agf_5.Ordem_controle=='Terceiro Controle'].Calibre.item()) / agf_5[agf_5.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda terceira cal 5:', agf_5_queda_terceira)

        filtro_calibre_6 = agf['VALOR_CALIBRE'] == 'CALIBRE_6'
        agf_6 = agf[filtro_calibre_6]
        agf_6_queda_terceira = (agf_6[agf_6.Ordem_controle=='Terceiro Controle'].Calibre.item()) / agf_6[agf_6.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda terceira cal 6:', agf_6_queda_terceira)

        filtro_calibre_7 = agf['VALOR_CALIBRE'] == 'CALIBRE_7'
        agf_7 = agf[filtro_calibre_7]
        agf_7_queda_terceira = (agf_7[agf_7.Ordem_controle=='Terceiro Controle'].Calibre.item()) / agf_7[agf_7.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda terceira cal 7:', agf_7_queda_terceira)

        filtro_calibre_8 = agf['VALOR_CALIBRE'] == 'CALIBRE_8'
        agf_8 = agf[filtro_calibre_8]
        agf_8_queda_terceira = (agf_8[agf_8.Ordem_controle=='Terceiro Controle'].Calibre.item()) / agf_8[agf_8.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda terceira cal 8:', agf_8_queda_terceira)
        

        filtro_calibre_9 = agf['VALOR_CALIBRE'] == 'CALIBRE_9'
        agf_9 = agf[filtro_calibre_9]
        agf_9_queda_terceira = (agf_9[agf_9.Ordem_controle=='Terceiro Controle'].Calibre.item()) / agf_9[agf_9.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda terceira cal 9:', agf_9_queda_terceira)

        filtro_calibre_10 = agf['VALOR_CALIBRE'] == 'CALIBRE_10'
        agf_10 = agf[filtro_calibre_10]
        agf_10_queda_terceira = (agf_10[agf_10.Ordem_controle=='Terceiro Controle'].Calibre.item()) / agf_10[agf_10.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda terceira cal 10:', agf_10_queda_terceira)

        filtro_calibre_12 = agf['VALOR_CALIBRE'] == 'CALIBRE_12'
        agf_12 = agf[filtro_calibre_12]
        agf_12_queda_terceira = (agf_12[agf_12.Ordem_controle=='Terceiro Controle'].Calibre.item()) / agf_12[agf_12.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda terceira cal 12:', agf_12_queda_terceira)

        filtro_calibre_14 = agf['VALOR_CALIBRE'] == 'CALIBRE_14'
        agf_14 = agf[filtro_calibre_14]
        agf_14_queda_terceira = (agf_14[agf_14.Ordem_controle=='Terceiro Controle'].Calibre.item()) / agf_14[agf_14.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda terceira cal 14:', agf_14_queda_terceira)
########################## QUEDA DE PERCENTUAIS NO QUARTO CONTROLE  ##########################

        filtro_calibre_5 = agf['VALOR_CALIBRE'] == 'CALIBRE_5'
        agf_5 = agf[filtro_calibre_5]
        agf_5_queda_quarta = (agf_5[agf_5.Ordem_controle=='Quarto Controle'].Calibre.item()) / agf_5[agf_5.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda quarta cal 5:', agf_5_queda_quarta)

        filtro_calibre_6 = agf['VALOR_CALIBRE'] == 'CALIBRE_6'
        agf_6 = agf[filtro_calibre_6]
        agf_6_queda_quarta = (agf_6[agf_6.Ordem_controle=='Quarto Controle'].Calibre.item()) / agf_6[agf_6.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda quarta cal 6:', agf_6_queda_quarta)

        filtro_calibre_7 = agf['VALOR_CALIBRE'] == 'CALIBRE_7'
        agf_7 = agf[filtro_calibre_7]
        agf_7_queda_quarta = (agf_7[agf_7.Ordem_controle=='Quarto Controle'].Calibre.item()) / agf_7[agf_7.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda quarta cal 7:', agf_7_queda_quarta)

        filtro_calibre_8 = agf['VALOR_CALIBRE'] == 'CALIBRE_8'
        agf_8 = agf[filtro_calibre_8]
        agf_8_queda_quarta = (agf_8[agf_8.Ordem_controle=='Quarto Controle'].Calibre.item()) / agf_8[agf_8.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write(agf_8)
        st.write('Multiplicador queda quarta cal 8:', agf_8_queda_quarta)

        filtro_calibre_9 = agf['VALOR_CALIBRE'] == 'CALIBRE_9'
        agf_9 = agf[filtro_calibre_9]
        agf_9_queda_quarta = (agf_9[agf_9.Ordem_controle=='Quarto Controle'].Calibre.item()) / agf_9[agf_9.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda quarta cal 9:', agf_9_queda_quarta)

        filtro_calibre_10 = agf['VALOR_CALIBRE'] == 'CALIBRE_10'
        agf_10 = agf[filtro_calibre_10]
        agf_10_queda_quarta = (agf_10[agf_10.Ordem_controle=='Quarto Controle'].Calibre.item()) / agf_10[agf_10.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda quarta cal 10:', agf_10_queda_quarta)

        filtro_calibre_12 = agf['VALOR_CALIBRE'] == 'CALIBRE_12'
        agf_12 = agf[filtro_calibre_12]
        agf_12_queda_quarta = (agf_12[agf_12.Ordem_controle=='Quarto Controle'].Calibre.item()) / agf_12[agf_12.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        st.write('Multiplicador queda quarta cal 12:', agf_12_queda_quarta)

        filtro_calibre_14 = agf['VALOR_CALIBRE'] == 'CALIBRE_14'
        agf_14 = agf[filtro_calibre_14]
        agf_14_queda_quarta = (agf_14[agf_14.Ordem_controle=='Quarto Controle'].Calibre.item()) / agf_14[agf_14.Ordem_controle=='Primeiro Controle'].Calibre.item() 
        
        st.write('Multiplicador queda quarta cal 14:', agf_14_queda_quarta)

        
        ###################### QUEDA SEGUNDO CONTROLE ######################
        
        
        filtro_2 = dataset_quality_piv['Ordem_controle'] == ordem_controle
        dataset_quality_piv_filtro = dataset_quality_piv[filtro_2]


        dataset_quality_piv_filtro = dataset_quality_piv_filtro.drop(columns = ['Ordem_controle'])
        dataset_quality_piv_filtro['TOT_PRIMEIRA'] = dataset_quality_piv_filtro['TOT_PRIMEIRA'].astype(str)
        dataset_quality_piv_filtro['TOT_SEGUNDA'] = dataset_quality_piv_filtro['TOT_SEGUNDA'].astype(str)
        dataset_quality_piv_filtro['TOT_TERCEIRA'] = dataset_quality_piv_filtro['TOT_TERCEIRA'].astype(str)
        dataset_quality_piv_filtro['TOT_REFUGO'] = dataset_quality_piv_filtro['TOT_REFUGO'].astype(str)
        dataset_quality_piv_filtro = dataset_quality_piv_filtro.T
        dataset_quality_piv_filtro = dataset_quality_piv_filtro.reset_index()
        dataset_quality_piv_filtro.rename(columns = {'index':'Qualidade',0:'Percentual', 1:'Percentual', 2:'Percentual', 3:'Percentual'}, inplace = True)
        dataset_quality_piv_filtro['Percentual'] = dataset_quality_piv_filtro['Percentual'].astype(float)


        
        
        def correcao_controle(data_input):

            if (data_input['VALOR_CALIBRE'] == 'Calibre_6' and ordem_controle == 'Segundo Controle'):
                return data_input['Pred'] * agf_6_queda_segunda
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_6' and ordem_controle == 'Terceiro Controle'):
                return data_input['Pred'] * agf_6_queda_terceira
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_6' and ordem_controle == 'Quarto Controle'):
                return data_input['Pred'] * agf_6_queda_quarta
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_6' and ordem_controle == 'Primeiro Controle'):
                return data_input['Pred'] 



            elif (data_input['VALOR_CALIBRE'] == 'Calibre_5' and ordem_controle == 'Segundo Controle'):
                return data_input['Pred'] * agf_5_queda_segunda
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_5' and ordem_controle == 'Terceiro Controle'):
                return data_input['Pred'] * agf_5_queda_terceira
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_5' and ordem_controle == 'Quarto Controle'):
                return data_input['Pred'] * agf_5_queda_quarta
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_5' and ordem_controle == 'Primeiro Controle'):
                return data_input['Pred']    

            elif (data_input['VALOR_CALIBRE'] == 'Calibre_7' and ordem_controle == 'Segundo Controle'):
                return data_input['Pred'] * agf_7_queda_segunda
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_7' and ordem_controle == 'Terceiro Controle'):
                return data_input['Pred'] * agf_7_queda_terceira
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_7' and ordem_controle == 'Quarto Controle'):
                return data_input['Pred'] * agf_7_queda_quarta
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_7' and ordem_controle == 'Primeiro Controle'):
                return data_input['Pred']          

            elif (data_input['VALOR_CALIBRE'] == 'Calibre_8' and ordem_controle == 'Segundo Controle'):
                return data_input['Pred'] * agf_8_queda_segunda
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_8' and ordem_controle == 'Terceiro Controle'):
                return data_input['Pred'] * agf_8_queda_terceira
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_8' and ordem_controle == 'Quarto Controle'):
                return data_input['Pred'] * agf_8_queda_quarta
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_8' and ordem_controle == 'Primeiro Controle'):
                return data_input['Pred']        

            elif (data_input['VALOR_CALIBRE'] == 'Calibre_9' and ordem_controle == 'Segundo Controle'):
                return data_input['Pred'] * agf_9_queda_segunda
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_9' and ordem_controle == 'Terceiro Controle'):
                return data_input['Pred'] * agf_9_queda_terceira
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_9' and ordem_controle == 'Quarto Controle'):
                return data_input['Pred'] * agf_9_queda_quarta
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_9' and ordem_controle == 'Primeiro Controle'):
                return data_input['Pred']      
            
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_10' and ordem_controle == 'Segundo Controle'):
                return data_input['Pred'] * agf_10_queda_segunda
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_10' and ordem_controle == 'Terceiro Controle'):
                return data_input['Pred'] * agf_10_queda_terceira
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_10' and ordem_controle == 'Quarto Controle'):
                return data_input['Pred'] * agf_10_queda_quarta
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_10' and ordem_controle == 'Primeiro Controle'):
                return data_input['Pred']   
            
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_12' and ordem_controle == 'Segundo Controle'):
                return data_input['Pred'] * agf_12_queda_segunda
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_12' and ordem_controle == 'Terceiro Controle'):
                return data_input['Pred'] * agf_12_queda_terceira
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_12' and ordem_controle == 'Quarto Controle'):
                return data_input['Pred'] * agf_12_queda_quarta
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_12' and ordem_controle == 'Primeiro Controle'):
                return data_input['Pred'] 
            
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_14' and ordem_controle == 'Segundo Controle'):
                return data_input['Pred'] * agf_14_queda_segunda
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_14' and ordem_controle == 'Terceiro Controle'):
                return data_input['Pred'] * agf_14_queda_terceira
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_14' and ordem_controle == 'Quarto Controle'):
                return data_input['Pred'] * agf_14_queda_quarta
            elif (data_input['VALOR_CALIBRE'] == 'Calibre_14' and ordem_controle == 'Primeiro Controle'):
                return data_input['Pred'] 


            else:
                return data_input['Pred'] 

        data_input['Pred'] = data_input.apply(correcao_controle, axis = 1)
            















        def mudanca_nomes_qualidades(dataset_quality_piv_filtro):
            if dataset_quality_piv_filtro['Qualidade'] == 'TOT_PRIMEIRA':
                return '1º'
            elif dataset_quality_piv_filtro['Qualidade'] == 'TOT_SEGUNDA':
                return '2º'
            elif dataset_quality_piv_filtro['Qualidade'] == 'TOT_TERCEIRA':
                return '3º'
            elif dataset_quality_piv_filtro['Qualidade'] == 'TOT_REFUGO':
                return 'REF'
        dataset_quality_piv_filtro['Qualidade'] = dataset_quality_piv_filtro.apply(mudanca_nomes_qualidades, axis = 1)


        data_input['Pred'] = round(data_input['Pred'],2)
        coluna_10, coluna_12 = st.columns(2)
        coluna_10.success('##### Previsão de calibres')
        
        fig = px.bar(data_input, x = 'VALOR_CALIBRE', y = 'Pred',text = 'Pred',
        category_orders= {'VALOR_CALIBRE':['Calibre_5','Calibre_6','Calibre_7','Calibre_8','Calibre_9','Calibre_10','Calibre_12','Calibre_14']})
        fig.update_layout(height = 500, width = 700, uniformtext_minsize=10, uniformtext_mode='show', font = dict(size = 15))
        fig.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False, marker_color='rgb(166,230,81)', marker_line_color='rgb(0,0,0)',
                  marker_line_width=1.5, opacity=0.75)
        coluna_10.plotly_chart(fig)

        coluna_12.success('##### Estimativa de qualidade')
        fig = go.Figure(data=[go.Pie(labels = dataset_quality_piv_filtro['Qualidade'], values = dataset_quality_piv_filtro['Percentual'], marker_colors = px.colors.sequential.Emrld ,hole = .4, pull=0.03)])
        #fig.add_trace(go.Pie(dataset_quality_piv_filtro, names = 'Qualidade', values = 'Percentual', hole = 0.4))
        fig.update_traces(textposition='inside', textinfo='percent+label',textfont_size=17,marker=dict(line=dict(color='#000000', width=1)))
        coluna_12.plotly_chart(fig)


        

        st.success('##### Comportamento histórico do talhão ')
        ## TENHO QUE RETIRAR O FILTRO DA VARIEDADE E DEIXAR O DO TALHAO
        ### OU NAO
    #    df_comportamento_calibres_TALHAO

        filtro_3 = df_comportamento_calibres_TALHAO['TALHAO'] == talhao_input2
        df_comportamento_calibres_TALHAO_2 = df_comportamento_calibres_TALHAO[filtro_3]

        

        fig = px.histogram(df_comportamento_calibres_TALHAO_2, x = 'VALOR_CALIBRE', y = 'Calibre', color = 'VALOR_CALIBRE',histfunc = 'avg', 
        category_orders={'VALOR_CALIBRE':['CALIBRE_5','CALIBRE_6','CALIBRE_7','CALIBRE_8','CALIBRE_9','CALIBRE_10','CALIBRE_12','CALIBRE_14'],
        'Ordem_controle':['Primeiro Controle','Segundo Controle','Terceiro Controle','Quarto Controle']}, facet_col = 'Ordem_controle', color_discrete_sequence= px.colors.sequential.Aggrnyl)
        #fig.update_layout(uniformtext_minsize=10, uniformtext_mode='show', font = dict(size = 15))
        fig.update_traces(marker_line_color = 'rgb(0,0,0)',marker_line_width = 1.5)
        fig.update_layout(height = 400, width = 1700)
        
        #fig.update_traces(showlegend = True)
        st.plotly_chart(fig)















