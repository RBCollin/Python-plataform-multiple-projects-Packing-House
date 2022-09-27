import socket
import streamlit as st

######### VAI SER CADA LINHA VAI TER UMA IMPRESSORA
### ONDE EM CADA LINHA VAI CAIR UM CALIBRE E UMA QUALIDADE

st.success('### Controle de etiqueta')

dataframe = 'http://sia:3000/backend/busca_generica/buscaGenerica?view=MGCLI.AGDTI_VW_DX_BALANCEAMENTO_PH'




empresa = 'AGRODAN'
controle = '5252'

# L- é o numero da semana e o dia da semana

quantidade_ = st.number_input('Selecione a quantidade para impressão:', key = 'qtd', value = 1)

empresa = 'AGRODAN'
controle = '5252'
talhao = 'AGD-106'
variedade = 'Palmer'
endereco = 'Km 28 Estrada Vicinal Belém/Ibó-Zona Rural'
razao_agrodan = 'Agropecuária Roriz Dantas Ltda'
cidade = 'Belém do S. Francisco PE'

SEMANA = '02'
DIA = '38'


calibre = st.number_input('Escolha o calibre:', value = 5)
calibre2 = str(calibre)


### QUALIDADE É SÓ 1
qualidade = 'I'

########## VAO SER DIFERENTES POIS VAO SER VARIAS IMPRESSORAS 

###### COLCOAR UM SELECTBOX PARA O IP EX:
### ESTEIRA 1,2,3,4 E CADA UMA VAI TER UM IP QUE VAI CORRESPONDER A UMA QUALIDADE CALIBRE ETC

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
^FT82,183^A0N,34,33^FH\^CI28^FD{controle} L-{controle}^FS^CI27
^FT17,221^A0N,39,38^FH\^CI28^FD{variedade}^FS^CI27
^FT498,183^A0N,34,33^FH\^CI28^FD{controle} L-{controle}^FS^CI27
^FT433,221^A0N,39,38^FH\^CI28^FD{variedade}^FS^CI27
^PQ1,0,1,Y
^XZ

""".encode()

if st.button('Imprimir', key = '   '):
    
    st.write('...')
    mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         

    try:           
        mysocket.connect((host, port))                                
        for i in range(1):
            mysocket.send(etiqueta_baquer2)    
        mysocket.close()
        st.write('Etiqueta impressa com sucesso !')                                            
    except:
        st.write("Falha na conexão com a impressora !")













































































































































































































