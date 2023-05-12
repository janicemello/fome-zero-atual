#Country
import pandas as pd
import streamlit as st 
import numpy as np 
import plotly.express as px
import matplotlib.pyplot as plt
import inflection
from PIL import Image
import folium
from haversine import haversine
import streamlit as st 
from PIL import Image
import altair as alt


#importando um arquivo 
df = pd.read_csv(r'./zomato.csv')


#Cleaning the dates 

#apagando linhas vazias
linhas_vazias2 = df["Cuisines"].notna()
df = df.loc[linhas_vazias2,:]

#RENOMEAR COLUNAS 
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
df = rename_columns(df)


#substituindo o codigo do país pelo nome do país 
countries = {
    1: 'India',
    14: 'Australia', 
    30: 'Brazil', 
    37: 'Canada', 
    94: 'Indonesia', 
    148: 'New Zeland', 
    162: 'Philippines', 
    166: 'Qatar', 
    184: 'Singapure', 
    189: 'South Africa', 
    191: 'Sri Lanka', 
    208: 'Turkey', 
    214: 'United Arab Emirates',
    215: 'England', 
    216: 'United States of America' 
}

def country_name(country_code):
    return countries[country_code]
df['country_code'] = df['country_code'].apply(country_name)



#Criando o tipo de comida 
def create_price_type(price_range):
    if price_range == 1:
        return "Cheap"
    elif price_range == 2: 
        return "normal"
    elif price_range == 3:
        return "expensive"
    else: 
        return "gourmet"
    
df["price_range"] = df["price_range"].apply(create_price_type)

#CAtegorizando os restaurantes 
df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])


#===========================================
#       BARRA LATERAL STREAMLIT
#============================================
st.set_page_config(page_title='Countries 🌎', layout="wide")
st.sidebar.markdown('# Filtros')

#criando filtro 

st.markdown('Filtros')
countries = st.sidebar.multiselect("Escolha os paises que deseja visualizar os restaurantes",['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'], default=['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'])
linhas_selecionadas2 = df['country_code'].isin(countries)
df = df.loc[linhas_selecionadas2, :]

#============================================
#       VISÃO COUNTRY
#============================================

st.title('Visão Países🌎 ')
#Restaurantes registrados por país 
with st.container():
    st.markdown('Quantidade de restaurantes registrados por País')
    df_aux = df.loc[:,['restaurant_id', 'country_code']].groupby("country_code").nunique().reset_index()
    #grafico
    df_aux = st.bar_chart(data= df_aux, x="country_code", y='restaurant_id')

#Cidades registrados por país
with st.container():
    st.markdown('Quantidade de cidades registrados por País')
    df_aux = df.loc[:,['city', 'country_code']].groupby("country_code").nunique().reset_index()
    #grafico
    df_aux = st.bar_chart(data= df_aux, x="country_code", y='city')


with st.container():
    col1, col2 = st.columns(2)
    with col1:
    #média de avaliações feitas por pais 
        st.markdown('Média de avaliações feitas por País')
        df_aux = df.loc[:,['votes', 'country_code']].groupby("country_code").mean().reset_index()
        #grafico
        df_aux = st.bar_chart(data= df_aux, x="country_code", y='votes')
    with col2:
    #média preço prato duas pessoas por país 
        st.markdown('Média de preço de um prato para duas pessoas por País')
        df_aux = df.loc[:,['average_cost_for_two', 'country_code']].groupby("country_code").mean().reset_index()
    #grafico
        df_aux = st.bar_chart(data= df_aux, x="country_code", y='average_cost_for_two')



