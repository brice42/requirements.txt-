import streamlit as st
import random
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.io as pio
st.cache_data

df=pd.read_csv("world-happiness-report-2021.csv")
dy=pd.read_csv("world-happiness-report.csv")
d_full= df.merge(dy, on="Country name")
df4 = pd.read_csv("suicide_total_deaths.csv")
years = df4.columns[df4.columns != 'country']
# Now melt the dataframe using the 'years' variable
DS1=pd.melt(df4, id_vars=['country'], value_vars=years)

# Convert the 'value' column to numeric type, handling errors
DS1['value'] = pd.to_numeric(DS1['value'], errors='coerce')

# Calculate the total suicides, now with numeric values
Total_suicide = DS1["value"].sum()

# Calculate the suicide rate
DS1["taux_suicide"] = (DS1["value"] / Total_suicide) * 100

data =pd.read_csv("Gdp-per-capital-world.csv")
#changer le nom de la colonne country en Country name
data.rename(columns={'country': 'Country name'}, inplace=True)

d_full1= d_full.merge(data, on=["Country name","year"])
d_full1.head(5)

st.title("Projet World_happiness")
st.sidebar.title("Sommaire")
pages=["Exploration", "DataVizualization","Test Statistique", "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)
if page == pages[0] : 
  st.write("### Introduction")
  st.dataframe(df.head(10))
  st.write(df.shape)
  st.write(df.info())
st.dataframe(df.describe())
if st.checkbox("Afficher les NA") :
  st.dataframe(df.isna().sum())
  if page == pages[1] : 
    st.write("### DataVizualization")
fig = plt.figure(figsize=(10, 6))
fig=px.scatter(df, x="Healthy life expectancy", y='Ladder score', color= "Regional indicator", title="ladder score  based on Healthy life expectancy by continent")
#plt.title("Ladder score by continent")
fig

fig = plt.figure(figsize=(10, 6))
fig=px.scatter(df, x="Healthy life expectancy", y='Ladder score', color="Country name", title="ladder score  based on Healthy life expectancy on 2021")
#plt.title("Ladder score by continent")
fig

fig = plt.figure(figsize=(10, 6))
fig=px.scatter(df, x="Logged GDP per capita", y='Ladder score', color="Country name", title="ladder score  based on Logged GDP per capita on 2021")
#plt.title("Ladder score by continent")
fig

fig = plt.figure(figsize=(10, 6))
fig=px.scatter(df, x="Social support", y='Ladder score', color="Country name", title="ladder score  based on Social support on 2021")
#plt.title("Ladder score by continent")
fig

fig = plt.figure(figsize=(10, 6))
fig=px.scatter(df, x="Freedom to make life choices", y='Ladder score', color="Country name", title="ladder score  based on Freedom to make life choices on 2021")
#plt.title("Ladder score by continent")
fig

fig = plt.figure(figsize=(10, 6))
fig=px.scatter(df, x="Generosity", y='Ladder score', color="Country name", title="ladder score  based on Generosity on 2021")
#plt.title("Ladder score by continent")
fig


fig = plt.figure(figsize=(10, 6))
fig =px.bar(df, y="Regional indicator", x="Ladder score", title="Ladder score by regional indicator")
fig

pays_Europe_etudes = df[df['Regional indicator'] == 'Western Europe']['Country name']
fig = go.Figure()
fig.add_traces(go.Bar(name='etudes',x=pays_Europe_etudes,y=df.loc[pays_Europe_etudes.index, 'Ladder score'].sort_values(ascending= False)))
fig.update_layout(showlegend = True,title ='Ladder score in Western Europe', xaxis_title = 'Country name', yaxis_title = 'Ladder score')
fig



pays_afrique_etudes = df[df['Regional indicator'] == 'Sub-Saharan Africa']['Country name']
fig = go.Figure()
fig.add_traces(go.Bar(name='etudes',x=pays_afrique_etudes,y=df.loc[pays_afrique_etudes.index, 'Ladder score'].sort_values(ascending= False)))
fig.update_layout(showlegend = True,title ='Ladder score in Sub-Saharan Africa ', xaxis_title = 'Country name', yaxis_title = 'Ladder score')
fig

pays_asie_etudes = df[df['Regional indicator'] == 'East Asia']['Country name']
fig = go.Figure()
fig.add_traces(go.Bar(name='etudes',x=pays_asie_etudes,y=df.loc[pays_asie_etudes.index, 'Ladder score'].sort_values(ascending= False)))
fig.update_layout(showlegend = True,title ='Ladder score in East Asia ', xaxis_title = 'Country name', yaxis_title = 'Ladder score')
fig


fig = go.Figure()
fig.add_trace(go.Box(x=df['Regional indicator'], y=df['Ladder score']))
fig.update_layout(showlegend= True , title ='Ladder score by Regional indicator',xaxis_title = 'Regional indicator', yaxis_title = 'Ladder score')
fig

# Create basic choropleth map
fig = px.choropleth(d_full1, locations='iso_alpha', color='Ladder score', hover_name='Country name',
                    projection='natural earth', animation_frame='year',
                    title='Ladder score by Country')
fig


df_num = df.select_dtypes(include = "float")
cor= df_num.corr()

# Re-instantiate fig as a go.Figure() object
fig = go.Figure()

# Pass the correlation matrix as the 'z' data for the heatmap.
# Set 'x' and 'y' to the column names of the correlation matrix.
fig.add_trace(go.Heatmap(z=cor.values, x=cor.columns, y=cor.columns))

fig
if page == pages[2] : 
  st.write("### Test Statistique")

# On effectue un test de pearson car il s'agit de deux variables continues
#Le test permet de cofirmer la correction entre les variables
#Ce test permet d'étudier une relation linéaire entre deux variables quantitatives.

# 𝐻0:Les variables X et Y ne sont pas corrélées, c'est-à-dire que la corrélation est nulle ⟺𝑐𝑜𝑟𝑟(𝑋,𝑌)
# 𝐻1:Les variables X et Y sont corrélées⟺𝑐𝑜𝑟𝑟(𝑋,𝑌)≠0


from scipy.stats import pearsonr
#renomer une colonne
df.rename(columns={'Ladder score': 'Ladder_score'}, inplace=True)
df.rename(columns={'Healthy life expectancy': 'Healthy_life_expectancy'}, inplace=True)

pearsonr(x= df['Healthy_life_expectancy'],y=df['Ladder_score'])


print("p-value: ", pearsonr(x = df["Healthy_life_expectancy"], y = df["Ladder_score"])[1])
print("coefficient: ", pearsonr(x = df["Healthy_life_expectancy"], y = df["Ladder_score"])[0])

st.write(" 𝐻0:Les variables X et Y ne sont pas corrélées, c'est-à-dire que la corrélation est nulle ⟺𝑐𝑜𝑟𝑟(𝑋,𝑌)")  
st.write ("𝐻1:Les variables X et Y sont corrélées⟺𝑐𝑜𝑟𝑟(𝑋,𝑌)≠0")
st.write("On effectue un test de person car il sagit de deux variables continues, les resultats sont les suivants:")
st.write("p-value: ", pearsonr(x = df["Healthy_life_expectancy"], y = df["Ladder_score"])[1])
st.write("coefficient: ", pearsonr(x = df["Healthy_life_expectancy"], y = df["Ladder_score"])[0])
st.write("Conclusion : La p-value (PR(>F)) est inférieure à 5% donc on rejette H0 et on conclut H1")
st.write("# on conclut donc a une influence significative du Healthy_life_expectancy sur le Ladder_score")




#fig = plt.figure(figsize=(10, 6))
#sns.barplot(y=df['Regional indicator'], x=df['Ladder score'])
#plt.title("Ladder score by continent")
#st.pyplot(fig)

#fig = go.Figure()
#fig=px.scatter(df, x="Healthy life expectancy", y="Ladder score", title="Ladder score vs Healthy life expectancy in 2021")
#fig.add_trace(go.Scatter(x=df["Healthy life expectancy"], y=df["Ladder score"], color=df["Regional indicator"]))
#fig.update_layout(title="Ladder score vs Healthy life expectancy in 2021")
#st.pyplot(fig)

#fig = px.scatter(df, x="Healthy life expectancy", y="Ladder score", 
 #                c="Regional indicator")
#st.pyplot(fig)
#fig = plt.figure(figsize=(10, 6))
#sns.scatterplot( diag_kind = "kde", hue= "Regional indicator", data = df [['Ladder score' ,'Healthy life expectancy','Regional indicator']])
#plt.show()

#fig = plt.figure(figsize=(10, 6))
#sns.swarmplot(x = 'Regional indicator', y ='Ladder score', data = df)
#st.pyplot(fig)