"""
📝 **Instructions** :
- Installez toutes les bibliothèques nécessaires en fonction des imports présents dans le code, utilisez la commande suivante :conda create -n projet python pandas numpy streamlit plotly seaborn ..........
- cd /d "H:/Mes documents/SAE601" 
- Complétez les sections en écrivant votre code où c’est indiqué.
- Ajoutez des commentaires clairs pour expliquer vos choix.
- Utilisez des emoji avec windows + ;
- Interprétez les résultats de vos visualisations (quelques phrases).
"""

### 1. Importation des librairies et chargement des données
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Chargement des données
df = pd.read_csv('ds_salaries.csv')


st.set_page_config(layout= ("wide"))

### 10. Filtrage avancé des données avec deux st.multiselect, un qui indique "Sélectionnez le niveau d'expérience" et l'autre "Sélectionnez la taille d'entreprise"
#votre code 
st.title("📊 Visualisation des Salaires en Data Science")   
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")
st.subheader(" Filtres Globaux")

experience_levels = df['experience_level'].unique()
selected_experience = st.multiselect("Sélectionnez le niveau d'expérience", experience_levels, default=experience_levels)


company_sizes = df['company_size'].unique()
selected_company_size = st.multiselect("Sélectionnez la taille d'entreprise", company_sizes, default=company_sizes)


df_filtered10 = df[
    (df['experience_level'].isin(selected_experience)) &
    (df['company_size'].isin(selected_company_size))
]



### 2. Exploration visuelle des données
#votre code 



if st.checkbox("Afficher un aperçu des données"):
    st.write(df_filtered10.head())


#Statistique générales avec describe pandas  
st.subheader("📌 Statistiques générales")
st.write(df_filtered10.describe())


### 3. Distribution des salaires en France par rôle et niveau d'expérience, uilisant px.box et st.plotly_chart
#votre code 
st.subheader("📈 Distribution des salaires en France")
#Création d'un graphique en boîte interactif
col1, col2= st.columns(2)

with col1:


    df_fr =  df_filtered10[df_filtered10['employee_residence'] == 'FR']
    st.write(px.box(df_fr, x='experience_level', y='salary_in_usd', color='experience_level')  )
with col2:
    st.write(px.bar(df_fr, x='experience_level', y='salary_in_usd', color='company_size'))

st.write("Il est possible de voir que  l'expérience du slarié augmente son salaire. Mais on voit aussi que les entreprises qui payent le plus ne sont pas les plus grandes entreprises")

### 4. Analyse des tendances de salaires :
#### Salaire moyen par catégorie : en choisisant une des : ['experience_level', 'employment_type', 'job_title', 'company_location'], utilisant px.bar et st.selectbox 
st.subheader("📌 Statistiques générales")
option = st.selectbox('Categorie',('experience_level', 'employment_type', 'job_title', 'company_location'))

salaire_moy = df_filtered10.groupby(option)["salary_in_usd"].mean()

fig = px.bar(salaire_moy)
st.write(fig)

st.write("On voit ici la moyenne des salaires en fonction de chaque niveau d'expérience")


### 5. Corrélation entre variables
# Sélectionner uniquement les colonnes numériques pour la corrélation
numeric_df = df_filtered10.select_dtypes(include=[np.number]) 
correlation_matrix = numeric_df.corr()





# Affichage du heatmap avec sns.heatmap
#votre code 
st.subheader("🔗 Corrélations entre variables numériques")
colo1, colo2 ,colo3= st.columns(3)

with colo2:
    st.pyplot( sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm').get_figure() ) # Créer une carte de chaleur pour visualiser la matrice de corrélation


### 6. Analyse interactive des variations de salaire
# Une évolution des salaires pour les 10 postes les plus courants
# count of job titles pour selectionner les postes
# calcule du salaire moyen par an
#utilisez px.line
#votre code 
st.subheader("Évolution des salaires pour les 10 postes les plus courants")

salary_avg_per_job = df_filtered10.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()

# top 10 jobs
top_10_jobs = df_filtered10['job_title'].value_counts().head(10).index
filtered_data = salary_avg_per_job[salary_avg_per_job['job_title'].isin(top_10_jobs)]


fig = px.line(filtered_data, 
              x='work_year', 
              y='salary_in_usd', 
              color='job_title', 
              title="Évolution des salaires des 10 postes les plus courants", 
              labels={'salary_in_usd': 'Salaire moyen en USD', 'work_year': 'Année de travail'})
fig.update_layout(xaxis=dict(type='category'))
st.plotly_chart(fig)

### 7. Salaire médian par expérience et taille d'entreprise
# utilisez median(), px.bar
#votre code 
st.subheader("Salaire médian par expérience et taille d'entreprise")
salary_med_per_xp = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median().reset_index()

# Créer le graphique à barres
fig = px.bar(salary_med_per_xp, x='experience_level', y='salary_in_usd', color='company_size', barmode='group',
             labels={'experience_level': 'Niveau d\'expérience', 'salary_in_usd': 'Salaire en USD', 'company_size': 'Taille de l\'entreprise'},
             title="Répartition des salaires par niveau d'expérience et taille d'entreprise")

st.plotly_chart(fig)


### 8. Ajout de filtres dynamiques
#Filtrer les données par salaire utilisant st.slider pour selectionner les plages 
#votre code 
st.subheader("Repartition salaire avec slider")
colo1, colo2 ,colo3= st.columns(3)

with colo1:
    salary_min, salary_max = st.slider(
    'Sélectionnez la plage de salaire en USD',
    min_value=int(df_filtered10['salary_in_usd'].min()),
    max_value=int(df_filtered10['salary_in_usd'].max()),
    value=(int(df_filtered10['salary_in_usd'].min()), int(df_filtered10['salary_in_usd'].max())),
    step=1000
        )
    st.write(f"Plage de salaire sélectionnée : {salary_min} USD à {salary_max} USD")   
    
with colo2 :
    df_filtered = salary_med_per_xp[(salary_med_per_xp['salary_in_usd'] >= salary_min) & (salary_med_per_xp['salary_in_usd'] <= salary_max)]

    fig = px.bar(df_filtered, x='experience_level', y='salary_in_usd', color='company_size', barmode='group',
             labels={'experience_level': 'Niveau d\'expérience', 'salary_in_usd': 'Salaire en USD', 'company_size': 'Taille de l\'entreprise'},
             title="Répartition des salaires filtrée par plage de salaire")


    st.plotly_chart(fig)


### 9.  Impact du télétravail sur le salaire selon le pays
st.subheader("Impact du télétravail sur le salaire selon le pays")


pays = df_filtered10['employee_residence'].unique()

# pour choisir un pays

selected_country = st.selectbox("Sélectionnez un pays", pays)

# Filtrer les données pour le pays sélectionné
df_pays = df_filtered10[df_filtered10['employee_residence'] == selected_country]

#impact du télétravail sur le salaire
df_impact = df_pays.groupby('remote_ratio')['salary_in_usd'].mean().reset_index()


fig = px.bar(df_impact, x='remote_ratio', y='salary_in_usd',
             title=f"Impact du télétravail sur le salaire à {selected_country}",
             labels={'remote_ratio': 'Ratio de télétravail', 'salary_in_usd': 'Salaire moyen en USD'})

df_employment_type = df_pays.groupby('employment_type')['salary_in_usd'].mean().reset_index()

fig2 = px.bar(df_employment_type, x='employment_type', y='salary_in_usd',
              title=f"Répartition des salaires par type d'emploi à {selected_country}",
              labels={'employment_type': 'Type d\'emploi', 'salary_in_usd': 'Salaire moyen en USD'})



colo1, colo2 = st.columns(2)

with colo1:
    st.plotly_chart(fig)

with colo2:
    st.plotly_chart(fig2)


st.write(df)