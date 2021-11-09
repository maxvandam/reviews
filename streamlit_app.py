# import packages
import streamlit as st
import pandas as pd
# import numpy as np
import plotly.express as px
# import matplotlib.pyplot as plt
# import fuzzywuzzy
# import seaborn as sns
import plotly.graph_objects as go

# import plotly.figure_factory as ff
# from statsmodels.formula.api import ols
# import gzip


movieDF = pd.read_csv('moviereviews.csv',encoding = "ISO-8859-1")

movieDF.head()

fig = px.histogram(x=movieDF['Grade'], nbins=10)

st.plotly_chart(fig)

movieDF.sort_values('Grade', ascending=False)

perfectMovies = movieDF[movieDF['Grade'] == 10]

basicsDB = pd.read_csv('https://datasets.imdbws.com/title.basics.tsv.gz', sep='\t')
movieDF1 = movieDF.merge(basicsDB, how='left', on='tconst')
movieDF1 = movieDF1.assign(startYear=lambda x: pd.to_numeric(x['startYear']))
ratingsDB = pd.read_csv('https://datasets.imdbws.com/title.ratings.tsv.gz', sep='\t')
movieDF2 = movieDF1.merge(ratingsDB, how='left', on='tconst')
movieDF2 = movieDF2.assign(runtimeMinutes=lambda x: pd.to_numeric(x['runtimeMinutes']))
st.dataframe(movieDF2)

ratingsDF = movieDF2[['Title', 'Grade', 'averageRating']]
ratingsDF.head()

print(type(movieDF2.loc[0][9]))

ratingsDF2 = ratingsDF.sort_values('averageRating', ascending=False)
ratingsDF2.head()

movieDF1mean = movieDF1.groupby('startYear').mean()
movieDF1mean

movies2016 = movieDF2[movieDF2['startYear'] == 2016]
movies2017 = movieDF2[movieDF2['startYear'] == 2017]
movies2018 = movieDF2[movieDF2['startYear'] == 2018]
movies2019 = movieDF2[movieDF2['startYear'] == 2019]
movies2020 = movieDF2[movieDF2['startYear'] == 2020]
movies2021 = movieDF2[movieDF2['startYear'] == 2021]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=movieDF2['Title'],
    y=movieDF2['Grade'],
    name='Max rating',
    marker_color='blue'
))
fig.add_trace(go.Bar(
    x=movieDF2['Title'],
    y=movieDF2['averageRating'],
    name='IMDB rating',
    marker_color='orangered'
))
fig.update_layout(barmode='group', xaxis_tickangle=-90)
st.plotly_chart(fig)

fig = px.scatter(
    x=movieDF2['Grade'],
    y=movieDF2['averageRating'],
    title='Max ratings vs IMDB ratings',
    labels=dict(x='Max rating', y='IMDB rating'),
    color=movieDF2['runtimeMinutes'],
    hover_name=movieDF2['Title'])
fig.update_layout(legend_title_text='Trend')
st.plotly_chart(fig)
