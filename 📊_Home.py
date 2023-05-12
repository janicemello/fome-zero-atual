import pandas as pd
import streamlit as st 
import numpy as np 
import inflection
from PIL import Image
import folium
from haversine import haversine
import streamlit as st 
from PIL import Image
from streamlit_folium import folium_static
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon, Icon



#importando um arquivo 
df = pd.read_csv(r'./zomato.csv')


#==================================
#       Limpeza dos dados
#==================================


#Cleaning the dates 
#apagando linhas vazias
linhas_vazias2 = df["Cuisines"].notna()
df = df.loc[linhas_vazias2,:]

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

#print(df)
print(df.columns)



#===========================================
#       BARRA LATERAL STREAMLIT
#============================================
st.set_page_config(page_title='Main Page 📊', layout="wide")
st.sidebar.markdown('Fome Zero')
image_path = "./logo.png"
image = Image.open(image_path)
st.sidebar.image(image, width=100)
st.sidebar.markdown('# Filtros')

#criando filtro 
countries = st.sidebar.multiselect("Escolha os paises que deseja visualizar os restaurantes",['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'], default=['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'])
linhas_selecionadas2 = df['country_code'].isin(countries)
df = df.loc[linhas_selecionadas2, :]

#============================================
#       VISÃO GERAL
#============================================
#create a container with a fixed width

st.markdown('### O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')



col1, col2, col3, col4, col5 = st.columns(5)

with col1: 
    restaurante_cadastrados = len(df["restaurant_id"].unique())
    col1.metric('Restaurantes Cadastrados', restaurante_cadastrados)
with col2: 
    paises_cadastrados = df.loc[:,"country_code"].nunique()
    col2.metric('Paises cadastrados', paises_cadastrados)
with col3: 
    cidades_cadastradas = df.loc[:,"city"].nunique()
    col3.metric('Qtd. de cidades cadastradas', cidades_cadastradas)
with col4: 
    avaliacao_feitas = sum(df.loc[:,"votes"])
    arredon = round(avaliacao_feitas,7)
    col4.metric('Avaliações feitas', arredon)
#with col5:
#    tipos_culinarias = len(df['cuisines'].unique())
#    col4.metric('Tipos de culinárias oferecidas', tipos_culinarias)



#mapa

#st.markdown('# Localização dos restaurantes')
#    #A localização central de cada cidade por tipo de tráfego.

data_plot = df.loc[:,['restaurant_name','country_code', "price_range","latitude", "longitude"]].groupby(['country_code', "restaurant_name", "price_range"]).median().reset_index()

#gráfico 
m = folium.Map([45, -102], zoom_start=4, width="%100", height="%100")  
df = df.sort_values('country_code')
last_country = None
marker_cluster = MarkerCluster()


for index, row in data_plot.iterrows():
    marker = folium.Marker(location=[row['latitude'],row['longitude']],
                icon=Icon(color='red',icon='no-sign'),
                popup= '<strong>' + row['restaurant_name'] + '</strong>' + '<br>' + 'Price: ' + row['price_range']
                )
    if last_country == row['country_code']:
        marker_cluster.add_child(marker)
    else:
        if last_country is not None:
            marker_cluster.add_to(m)
        marker_cluster = MarkerCluster(icons=[
            DivIcon(
                    icon_size=(32,32),
                    icon_anchor=(0,0),
                    html=f'<div style="font-size:14pt;color:green">{len(marker_cluster._children)}</div>'
                )
        ])
    last_country = row['country_code']
folium_static(m,width=1000 , height= 800)
m.save('index,html')
