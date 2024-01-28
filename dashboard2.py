import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Primeiro estudo de Dashboard em Streamlit')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# essa anotação de cache vai checar a entrada usada para a func e o código dentro da func
# se for a primeira vez rodando, o streamlit vai alocar o retorno da func no cache local
# a próxima vez, se nada das checagens tiver mudado, o streamlit pula a execução da função e faz a leitura do cache local
@st.cache_data 
def load_data(data_file,nrows):
    data = pd.read_csv(data_file, nrows=nrows)
    lowercase = lambda x: str(x).lower() # func lambda pra correr nos itens e deixar str minusculas
    data.rename(lowercase, axis='columns', inplace=True) # correr a variavel que contém a lambda pra minuscula
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) # altera o formato da coluna 'date/time'
    return data

# Cria um texto pra informar que os dados estão carregando
data_load_state = st.text('Carregando dados...')
# Carrega o seu dataframe
data = load_data(DATA_URL,1000)
# Informa quando os seus dados forem carregados
data_load_state.text("Concluído!")

if st.checkbox('Mostrar dados brutos'):
    st.subheader('Dados brutos')
    st.dataframe(data) # o streamlit carrega um dataframe com os dados que vc passar como parametro
# st.write(data) # write vai tentar ler o arquivo no formato que ele é realmente, nesse caso é um df

st.subheader('Número de viagens por hora')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

day_hour = data[DATE_COLUMN].dt.hour.unique()
# selected_hour = st.sidebar.selectbox('Hour',day_hour)
selected_hour = st.slider('Hora', 0, 23, 17)

data_map_per_hour = data[data[DATE_COLUMN].dt.hour==selected_hour]

st.subheader('Mapa de todas as viagens de %s:00' %selected_hour)
st.map(data_map_per_hour)