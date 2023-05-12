#Cuisines
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


#print(df['cuisines'].unique())



#===========================================
#       BARRA LATERAL STREAMLIT
#============================================
st.set_page_config(page_title="Cuisines", page_icon="🍽️", layout="wide")
st.sidebar.markdown('# Filtros')

#criando filtro 
countries = st.sidebar.multiselect("Escolha os paises que deseja visualizar os restaurantes",['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'], default=['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'])
linhas_selecionadas2 = df['country_code'].isin(countries)
df = df.loc[linhas_selecionadas2, :]

#filtro quantidade de restaurantes
top_n = st.sidebar.slider("Selecione a quantidade de Restaurantes que deseja visualizar", 1, 20, 10)



#filtro  Tipos de Culinária
cuisiness = st.sidebar.multiselect("Escolha os paises que deseja visualizar os restaurantes",['Italian','European','Filipino','American','Korean','Pizza','Taiwanese','Japanese','Coffee','Chinese','Seafood','Singaporean',
                                                                                                'Vietnamese','Latin American','Healthy Food','Cafe','Fast,Food','Brazilian','Argentine','Arabian','Bakery','Tex-Mex','Bar Food','International','French','Steak',
                                                                                                'German','Sushi','Grill','Peruvian','North Eastern','Ice Cream','Burger','Mexican','Vegetarian','Contemporary','Desserts','Juices','Beverages','Spanish','Thai','Indian',
                                                                                                'Mineira','BBQ','Mongolian','Portuguese','Greek','Asian','Author','Gourmet Fast Food','Lebanese','Modern Australian','African','Coffee and Tea','Australian','Middle Eastern',
                                                                                                'Malaysian','Tapas','New American','Pub Food','Southern','Diner','Donuts','Southwestern','Sandwich','Irish','Mediterranean', 'Cafe Food','Korean BBQ','Fusion','Canadian',
                                                                                                'Breakfast','Cajun','New Mexican','Belgian','Cuban','Taco','Caribbean','Polish','Deli','British','California','Others','Eastern European','Creole','Ramen','Ukrainian',
                                                                                                'Hawaiian','Patisserie','Yum Cha','Pacific Northwest','Tea','Moroccan','Burmese','Dim Sum','Crepes','Fish and Chips','Russian','Continental','South Indian','North Indian',
                                                                                                'Salad','Finger Food','Mandi','Turkish','Kerala','Pakistani','Biryani','Street Food','Nepalese','Goan','Iranian','Mughlai','Rajasthani','Mithai','Maharashtrian','Gujarati',
                                                                                                'Rolls','Momos','Parsi','Modern Indian','Andhra','Tibetan','Kebab','Chettinad','Bengali','Assamese','Naga','Hyderabadi','Awadhi','Afghan','Lucknowi','Charcoal Chicken',
                                                                                                'Mangalorean','Egyptian','Malwani','Armenian','Roast Chicken','Indonesian','Western','Dimsum','Sunda','Kiwi','Asian Fusion','Pan Asian','Balti','Scottish','Cantonese',
                                                                                                'Sri Lankan','Khaleeji','South African','Drinks Only','Durban','World Cuisine','Izgara','Home-made','Giblets','Fresh Fish','Restaurant Cafe','Kumpir','Döner','Turkish Pizza',
                                                                                                'Ottoman','Old Turkish Bars','Kokoreç'],default=['Italian','European','Filipino','American','Korean','Pizza','Taiwanese','Japanese','Coffee','Chinese','Seafood','Singaporean',
                                                                                                                                        'Vietnamese','Latin American','Healthy Food','Cafe','Fast,Food','Brazilian','Argentine','Arabian','Bakery','Tex-Mex','Bar Food','International',
                                                                                                                                        'French','Steak','German','Sushi','Grill','Peruvian','North Eastern','Ice Cream','Burger','Mexican','Vegetarian','Contemporary','Desserts','Juices',
                                                                                                                                        'Beverages','Spanish','Thai','Indian','Mineira','BBQ','Mongolian','Portuguese','Greek','Asian','Author','Gourmet Fast Food','Lebanese','Modern Australian','African',
                                                                                                                                        'Coffee and Tea','Australian','Middle Eastern','Malaysian','Tapas','New American','Pub Food','Southern','Diner','Donuts','Southwestern','Sandwich','Irish','Mediterranean',
                                                                                                                                        'Cafe Food','Korean BBQ','Fusion','Canadian','Breakfast','Cajun','New Mexican','Belgian','Cuban','Taco','Caribbean','Polish','Deli','British','California','Others',
                                                                                                                                        'Eastern European','Creole','Ramen','Ukrainian','Hawaiian','Patisserie','Yum Cha','Pacific Northwest','Tea','Moroccan','Burmese','Dim Sum','Crepes','Fish and Chips',
                                                                                                                                        'Russian','Continental','South Indian','North Indian','Salad','Finger Food','Mandi','Turkish','Kerala','Pakistani','Biryani','Street Food','Nepalese','Goan','Iranian',
                                                                                                                                        'Mughlai','Rajasthani','Mithai','Maharashtrian','Gujarati','Rolls','Momos','Parsi','Modern Indian','Andhra','Tibetan','Kebab','Chettinad','Bengali','Assamese','Naga',
                                                                                                                                        'Hyderabadi','Awadhi','Afghan','Lucknowi','Charcoal Chicken','Mangalorean','Egyptian','Malwani','Armenian','Roast Chicken','Indonesian','Western','Dimsum','Sunda','Kiwi',
                                                                                                                                        'Asian Fusion','Pan Asian','Balti','Scottish','Cantonese','Sri Lankan','Khaleeji','South African','Drinks Only','Durban','World Cuisine','Izgara','Home-made','Giblets',
                                                                                                                                        'Fresh Fish','Restaurant Cafe','Kumpir','Döner','Turkish Pizza','Ottoman','Old Turkish Bars','Kokoreç'])
linhas_selecionadas2 = df['cuisines'].isin(cuisiness)
df = df.loc[linhas_selecionadas2, :]

#==========================================
#       FUNÇÕES 
#==========================================

def top_cuisines():
    cuisines = {
        "Italian": "",
        "American": "",
        "Arabian": "",
        "Japanese": "",
        "Brazilian": "",
    }

    cols = [
        "restaurant_id",
        "restaurant_name",
        "country_code",
        "city",
        "cuisines",
        "average_cost_for_two",
        "currency",
        "aggregate_rating",
        "votes",
    ]

    for key in cuisines.keys():

        lines = df["cuisines"] == key

        cuisines[key] = (
            df.loc[lines, cols]
            .sort_values(["aggregate_rating", "restaurant_id"], ascending=[False, True])
            .iloc[0, :]
            .to_dict()
        )

    return cuisines


def write_metrics():

    cuisines = top_cuisines()

    italian, american, arabian, japonese, brazilian = st.columns(len(cuisines))

    with italian:
        st.metric(
            label=f'Italiana: {cuisines["Italian"]["restaurant_name"]}',
            value=f'{cuisines["Italian"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Italian"]['country_code']}\n
            Cidade: {cuisines["Italian"]['city']}\n
            Média Prato para dois: {cuisines["Italian"]['average_cost_for_two']} ({cuisines["Italian"]['currency']})
            """,
        )

    with american:
        st.metric(
            label=f'Italiana: {cuisines["American"]["restaurant_name"]}',
            value=f'{cuisines["American"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["American"]['country_code']}\n
            Cidade: {cuisines["American"]['city']}\n
            Média Prato para dois: {cuisines["American"]['average_cost_for_two']} ({cuisines["American"]['currency']})
            """,
        )

    with arabian:
        st.metric(
            label=f'Italiana: {cuisines["Arabian"]["restaurant_name"]}',
            value=f'{cuisines["Arabian"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Arabian"]['country_code']}\n
            Cidade: {cuisines["Arabian"]['city']}\n
            Média Prato para dois: {cuisines["Arabian"]['average_cost_for_two']} ({cuisines["Arabian"]['currency']})
            """,
        )

    with japonese:
        st.metric(
            label=f'Italiana: {cuisines["Japanese"]["restaurant_name"]}',
            value=f'{cuisines["Japanese"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Japanese"]['country_code']}\n
            Cidade: {cuisines["Japanese"]['city']}\n
            Média Prato para dois: {cuisines["Japanese"]['average_cost_for_two']} ({cuisines["Japanese"]['currency']})
            """,
        )

    with brazilian:
        st.metric(
            label=f'Italiana: {cuisines["Brazilian"]["restaurant_name"]}',
            value=f'{cuisines["Brazilian"]["aggregate_rating"]}/5.0',
            help=f"""
            País: {cuisines["Brazilian"]['country_code']}\n
            Cidade: {cuisines["Brazilian"]['city']}\n
            Média Prato para dois: {cuisines["Brazilian"]['average_cost_for_two']} ({cuisines["Brazilian"]['currency']})
            """,
        )

    return None


def top_restaurants(countries, cuisines, top_n):
    cols = [
        "restaurant_id",
        "restaurant_name",
        "country_code",
        "city",
        "cuisines",
        "average_cost_for_two",
        "aggregate_rating",
        "votes",
    ]

    lines = (df["cuisines"].isin(cuisines)) & (df["country_code"].isin(countries))

    dataframe = df.loc[lines, cols].sort_values(
        ["aggregate_rating", "restaurant_id"], ascending=[False, True]
    )

    return dataframe.head(top_n)


def top_best_cuisines(countries, top_n):
    lines = df["country_code"].isin(countries)

    grouped_df = (
        df.loc[lines, ["aggregate_rating", "cuisines"]]
        .groupby("cuisines")
        .mean()
        .sort_values("aggregate_rating", ascending=False)
        .reset_index()
        .head(top_n)
    )

    fig = px.bar(
        grouped_df.head(top_n),
        x="cuisines",
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto=".2f",
        title=f"Top {top_n} Melhores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "aggregate_rating": "Média da Avaliação Média",
        },
    )

    return fig


def top_worst_cuisines(countries, top_n):
    lines = df["country_code"].isin(countries)

    grouped_df = (
        df.loc[lines, ["aggregate_rating", "cuisines"]]
        .groupby("cuisines")
        .mean()
        .sort_values("aggregate_rating")
        .reset_index()
        .head(top_n)
    )

    fig = px.bar(
        grouped_df.head(top_n),
        x="cuisines",
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto=".2f",
        title=f"Top {top_n} Piores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "aggregate_rating": "Média da Avaliação Média",
        },
    )

    return fig
#============================================
#       VISÃO CUISINES
#============================================

with st.container():
            df_restaurants = countries, top_n, cuisiness
            st.markdown(f"## Melhores Restaurantes dos Principais tipos Culinários")
            write_metrics()
#TABELA TOP 10            
            st.markdown(f"## Top {top_n} Restaurantes")
            df_aux = df.loc[:, ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines','average_cost_for_two', 'aggregate_rating', 'votes']].sort_values('aggregate_rating', ascending=False).head(top_n)
            st.dataframe(df_aux.head(top_n))
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        fig = top_best_cuisines(countries, top_n)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = top_worst_cuisines(countries, top_n)
        st.plotly_chart(fig, use_container_width=True)

#with st.container():
#            st.write('Top 20 restaurantes' ,unsafe_allow_html=True)
#            df_aux = df.loc[:, ['restaurant_id','restaurant_name', 'country_code','city','cuisines','average_cost_for_two','aggregate_rating','votes']]
#            st.dataframe(df_aux)