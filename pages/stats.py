# -*- coding: utf-8 -*-

from dash import dcc, html, Input, Output
import dash
import pandas as pd
import json
import plotly.express as px

# Enregistrer la page dans le registre avec le decorateur
dash.register_page(__name__, path='/stats', name='Stats', order=4)

# Charger les donnees CSV
try:
    df = pd.read_csv('data/data_fictive.csv', sep=';', encoding='utf-8')
except Exception as e:
    print(f"Erreur lors du chargement du CSV : {e}")
    df = pd.read_csv('data/data_fictive.csv', sep=';', encoding='ISO-8859-1')

# Charger les utilisateurs a partir du fichier JSON
try:
    with open('data/users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
except Exception as e:
    print(f"Erreur lors du chargement du fichier JSON : {e}")
    users = []

# Convertir les utilisateurs en DataFrame si necessaire
users_df = pd.DataFrame(users)

# Fonctions utilitaires
def count_non_empty(series):
    return series.notna().sum()

def create_distribution_chart(data, title):
    # Reinitialiser l'index pour obtenir un DataFrame avec des colonnes
    data_df = data.reset_index()
    data_df.columns = ['index', 'count']  # Renommer les colonnes pour le graphique
    fig = px.pie(data_frame=data_df, names='index', values='count', title=title)
    return dcc.Graph(figure=fig)

# Composants pour les statistiques globales
def global_stats():
    return html.Div([
        html.H4("Statistiques Globales"),
        html.Div([
            html.P(f"Nombre d'annotations: {len(df)}"),
            html.P(f"Nombre de validations: {count_non_empty(df['Reviewer'])}"),
        ], className="stats-summary"),
        create_distribution_chart(df['User'].value_counts(), "Repartition des utilisateurs"),
        create_distribution_chart(df['Reviewer'].value_counts(), "Repartition des validateurs"),
        create_distribution_chart(df['Couleur'].value_counts(), "Repartition des couleurs"),
        create_distribution_chart(df['Marque'].value_counts(), "Repartition des marques"),
    ])

# Composants pour les statistiques personnelles
def personal_stats():
    return html.Div([
        html.H4("Statistiques Personnelles"),
        dcc.Dropdown(
            id='user-dropdown',
            options=[{'label': user['name'], 'value': user['name']} for user in users],
            value=users[0]['name'] if users else None,
            className="dropdown"
        ),
        html.Div(id='personal-stats-content')
    ])

# Callback pour mettre a jour les statistiques personnelles
@dash.callback(
    Output('personal-stats-content', 'children'),
    Input('user-dropdown', 'value')
)
def update_personal_stats(selected_user):
    if selected_user is None:
        return html.Div("Veuillez selectionner un utilisateur.")

    user_df = df[df['User'] == selected_user]
    return html.Div([
        html.Div([
            html.P(f"Nombre d'annotations: {len(user_df)}"),
            html.P(f"Nombre de validations: {count_non_empty(user_df['Reviewer'])}"),
        ], className="stats-summary"),
        create_distribution_chart(user_df['Couleur'].value_counts(), f"Repartition des couleurs pour {selected_user}"),
        create_distribution_chart(user_df['Marque'].value_counts(), f"Repartition des marques pour {selected_user}"),
    ])

# Layout principal
layout = html.Div([
    html.H3("Statistiques"),
    dcc.Tabs([
        dcc.Tab(label="Stats Globales", children=[global_stats()]),
        dcc.Tab(label="Stats Personnelles", children=[personal_stats()])
    ], className="custom-tabs")
])