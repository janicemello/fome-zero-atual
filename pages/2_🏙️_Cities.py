#visão Cities

import pandas as pd
import streamlit as st 
import plotly.express as px
import numpy as np 
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

print(df.isna().sum())
#substituir pelos cod do pais 
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
st.set_page_config(page_title='Cities 🏙️', layout="wide")
st.title('🏙️ Visão Cidades')
st.sidebar.markdown('# Filtros')


#criando filtro 
countries = st.sidebar.multiselect("Escolha os paises que deseja visualizar os restaurantes",['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'], default=['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'])
linhas_selecionadas2 = df['country_code'].isin(countries)
df = df.loc[linhas_selecionadas2, :]

#============================================
#       VISÃO CIDADES
#============================================
print(df.columns)
with st.container():  
            #st.markdown("Top 10 cidades com restaurantes na base de dados")
            st.write('Top 10 cidades com restaurantes na base de dados' ,unsafe_allow_html=True)
            df_aux = df.loc[:, ['restaurant_id','city']].groupby('city').nunique().sort_values('restaurant_id', ascending=False).head(10).reset_index()
            df_paises = df.loc[:,['city','country_code']].groupby('city').first().reset_index()
            df_aux = (df_aux.join(df_paises.set_index('city'),on='city').sort_values('restaurant_id', ascending=False))
            fig= px.bar(df_aux,x='city', y='restaurant_id', color='country_code', category_orders={'city': df_aux['city'][::-1]})
            fig.update_traces(texttemplate= '%{y}',textposition='inside')
            st.plotly_chart(fig, use_container_width=True)

            
with st.container():
            col1, col2 = st.columns(2)
            with col1: 
                st.write('Top 7 cidades com restaurantes com média de avaliação acima de 4')
                df_aux = df.loc[(df['aggregate_rating']>= 4), ['restaurant_id', 'city']]
                df_aux = (df_aux.groupby('city').nunique()).sort_values('restaurant_id', ascending=False).head(7).reset_index()
                df_paises = df.loc[:,['city','country_code']].groupby('city').first().reset_index()
                df_aux = (df_aux.join(df_paises.set_index('city'),on='city').sort_values('restaurant_id', ascending=True))
                fig= px.bar(df_aux,
                        x='city', 
                        y='restaurant_id',
                        color='country_code',
                        category_orders={'city': df_aux['city'][::-1]})
                fig.update_traces(texttemplate= '%{y}',textposition='inside')
                st.plotly_chart(fig, use_container_width=True)

            with col2: 
                st.markdown('Top 7 cidades com restaurantes com média de avaliação abaixo de 2.5')
                df_aux = df.loc[(df['aggregate_rating']<= 2.5), ['restaurant_id', 'city']]
                df_aux = (df_aux.groupby('city').nunique().sort_values('restaurant_id', ascending=False).head(7).reset_index())
                df_paises = df.loc[:,['city','country_code']].groupby('city').first().reset_index()
                df_aux = (df_aux.join(df_paises.set_index('city'),on='city').sort_values('restaurant_id', ascending=True))
                fig= px.bar(df_aux,
                        x='city', 
                        y='restaurant_id',
                        color='country_code',
                        category_orders={'city': df_aux['city'][::-1]})
                fig.update_traces(texttemplate= '%{y}',textposition='inside')
                st.plotly_chart(fig, use_container_width=True)
with st.container():
            #st.markdown("Top 10 cidades com restaurantes na base de dados")
            df_aux = df.loc[:, ['cuisines','city']].groupby('city').nunique().sort_values('cuisines', ascending=False).head(10).reset_index()
            df_paises = df.loc[:,['city','country_code']].groupby('city').first().reset_index()
            df_aux = (df_aux.join(df_paises.set_index('city'),on='city').sort_values('cuisines', ascending=False))
            fig= px.bar(df_aux,x='city', y='cuisines', color='country_code', category_orders={'city': df_aux['city']})
            fig.update_traces(texttemplate= '%{y}',textposition='inside')
            st.plotly_chart(fig, use_container_width=True)