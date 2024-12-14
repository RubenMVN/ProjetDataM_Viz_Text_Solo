from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
from FonctionMining import *
from nltk.stem import SnowballStemmer
from FonctionMining import stopWords
stopWords = [unidecode(sw) for sw in stopWords]
stemmer = SnowballStemmer('french')
import pandas as pd
import regex as re
import plotly.express as px
from io import BytesIO

#Import du df dans le fichier et modification
data = pd.read_csv("/ProjetDataM_Viz_Text_Solo/data.csv", delimiter=";")
df = pd.DataFrame(data)
df["Date"] = df['Date'].apply(lambda x: re.search(r"\d{4}-\d{2}-\d{2}", x).group(0))
df['Month'] = df['Date'].apply(lambda x: re.search(r"\d{4}-(\d{2})-\d{2}", x).group(1))
df['Year'] = df['Date'].apply(lambda x: re.search(r"(\d{4})-\d{2}-\d{2}", x).group(1))
df_pivot = df.pivot_table(index='Date', columns='Security', values='Open', aggfunc='mean')
df_pivot.fillna(0, inplace=True)
df_pivot.reset_index(inplace=True)

#Presentation/Affichage du site
st.set_page_config(page_title="ProjetDataM_Viz_Text")
st.title("Projet Data Management")
page = st.sidebar.radio("Choix de la page",["Home", "Wordclouds", "Graphiques"])

def page1():
    #Affichage de différentes données sur mes dataframes
    st.header("Home")

    st.subheader("Informations")
    st.markdown(
        """
        <div style="border: 2px solid midnightblue; padding: 10px; border-radius: 5px; background-color: slategray;color:white;font-family: Arial, sans serif;">
            <p><strong>Informations sur notre base de données :</strong></p>
            <p>Voici les informations sur notre jeu de données:<br>Notre jeu de données provient du site datahub.io, il contient 8739472 observations (624248*14) et 14 variables.<br> Voici nos variables :<br>Security(object) : représente le nom de la société; <br>Date(datetime64[ns]):La date ; <br>Open(float64): représente le cout à l'ouverture du marché; <br>High(float64): représente la valeur maximum atteinte ce jour; <br>Low(float64): représente la valeur minimum atteinte ce jour; <br>Close(float64): représente la valeur à la fermeture du marché; <br>Volume(int64): désigne le nombre total d’actions, de contrats ou d’instruments financiers échangés sur une période donnée, ici le jour; <br>Dividends(float64): dividende versé; <br>Stock Splits(float64): opération par laquelle une entreprise divise le prix de ses actions en augmentant le nombre total d’actions en circulation; <br>GICS Sector(object): niveaux de classification du GICS, un système utilisé pour organiser les entreprises cotées en bourse en fonction de leur secteur d’activité.; <br>GICS Sub-Industry(object): regroupe les entreprises en fonction de leurs activités les plus détaillées au sein d’une industrie donnée; <br>Symbol(object): Acronyme de la société; <br>Month(int32): représente le mois; <br>Year(int32): représente l'année<br>Il n'y a aucune valeur manquante.</p>
        </div>
        """,
        unsafe_allow_html=True,
        )


    st.markdown("Dataframe")
    st.dataframe(df)
    st.markdown("Données sur mon dataframe")
    st.dataframe(df.describe())
    st.markdown("Dataframe pivot")
    st.dataframe(df_pivot)
    st.markdown("Données suplémentaires sur le dataframe")
    st.dataframe(df_pivot.describe())

def page2():
    from TextMining import Texte

    def generate_wordcloud(contenu, background_color):
        #Code pour générer un wordcloud
        wordc = WordCloud(width=800, height=400, background_color=background_color).generate(contenu)
        fig = plt.figure(figsize=(10, 5), facecolor='white')
        plt.imshow(wordc, interpolation='bilinear')
        plt.axis('off')
        buffer = BytesIO()
        plt.savefig(buffer, format='PNG', bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        return fig,buffer

    fig1, buffer1 = generate_wordcloud(Texte, "blue")
    st.write("**WordCloud 1**")
    st.pyplot(fig1)
    st.download_button("Télécharge notre wordcloud",buffer1,"wordcloud.png",mime='image/png')


    # Ajout de fichier pour permettre à l'utilisateur de générer son propre wordcloud et le télécharger
    file = st.file_uploader("Choisissez un fichier type txt pour le wordcloud")
    if file:
        try:
            contenu = file.read().decode("utf-8")
            file2 = stem_cleaner(contenu, stemmer, stopWords)
            fig2,buffer2 = generate_wordcloud(file2, "green")
        except Exception as e:
            st.markdown("")

    if file is not None:
        try:
            st.write("**WordCloud 2**")
            st.pyplot(fig2)
            st.download_button("Télécharge ton wordcloud", buffer2, "wordcloud.png", mime='image/png')
        except Exception as e:
            st.markdown("Il y a eu une erreur.")
            st.markdown("Avez vous bien uploader un fichier de type text")

def page3():
    #Premier graphique avec un filtre interactif
    societe = df_pivot.columns[1:]
    filtre_Societe = st.sidebar.multiselect("Societés", societe)
    fig_lines = px.line(df_pivot, x="Date", y=filtre_Societe ,title="Stocks")
    st.plotly_chart(fig_lines)

if page == "Home":
    page1()
if page == "Wordclouds":
    page2()
if page == "Graphiques":
    page3()

