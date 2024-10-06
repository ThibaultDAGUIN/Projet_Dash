# -*- coding: utf-8 -*-

from dash import dcc, html, Input, Output
import dash
import pandas as pd
import json
import plotly.express as px
import dash_bootstrap_components as dbc


# Enregistrer la page dans le registre avec le decorateur
dash.register_page(__name__, path='/stats', name='Statistiques', order=4)

# Charger les donnees JSON
try:
    with open('data/annotations.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Convertir la liste de dictionnaires en DataFrame
        df = pd.json_normalize(data)
        # Remplacer les valeurs vides par NaN dans la colonne reviewer
        df['reviewer'] = df['reviewer'].replace("", pd.NA)
except Exception as e:
    print(f"Erreur lors du chargement du annotations.json : {e}")
    df = pd.DataFrame()

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
    # return series.notna().sum()
    return series.dropna().count()

def create_distribution_chart(data, title, color_column=None):
    data_df = data.reset_index()
    data_df.columns = ['index', 'count']
    
    if color_column is not None:
        fig = px.pie(data_frame=data_df, names='index', values='count', title=title, color='index',
                     color_discrete_map=color_column)
    else:
        fig = px.pie(data_frame=data_df, names='index', values='count', title=title)
    
    return dcc.Graph(figure=fig)

# Exemple d'utilisation avec un dictionnaire de couleurs
color_map = {
    # 'Rouge': 'red',
    # 'Bleu': 'blue',
    # 'Vert': 'green',
    # 'Jaune': 'yellow',
    # 'Noir': 'black',
    # 'Blanc': 'white',
    # 'Gris': 'gray',
    # 'Orange': 'orange',
    # 'Violet': 'purple',
    # 'Rose': 'pink',
    # 'Marron': 'brown'
    
    'Rouge': '#FF6F61',  # Rouge doux
    'Bleu': '#3585CD',   # Bleu 
    'Vert': '#98FB98',   # Vert pâle
    'Jaune': '#FFD700',  # Jaune doré
    'Noir': '#303030',   # Gris foncé
    'Blanc': '#F5F5F5',  # Blanc cassé
    'Gris': '#A9A9A9',   # Gris clair
    'Orange': '#FFA07A', # Orange saumon
    'Violet': '#9370DB', # Violet moyen
    'Rose': '#FFB6C1',   # Rose clair
    'Marron': '#D2B48C'  # Marron clair

}
# Composants pour les statistiques globales
def global_stats():
    return html.Div([
        # html.H4("Statistiques Globales"),
        # html.Div([
        #     html.P(f"Nombre d'annotations: {len(df)}"),
        #     html.P(f"Nombre de validations: {count_non_empty(df['reviewer'])}"),
        # ], className="stats-summary"),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Nombre d'annotations", className="card-title text-center"),
                        html.P(f"{len(df)}", className="card-text display-6 text-center")
                    ]),
                    className="bg-primary text-white mb-4 m-2"
                ),
                width=6
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Nombre de validations", className="card-title text-center"),
                        html.P(f"{count_non_empty(df['reviewer'])}", className="card-text display-6 text-center")
                    ]),
                    className="bg-success text-white mb-4 m-2"
                ),
                width=6
            ),
        ]),
        dbc.Row([
            dbc.Col(create_distribution_chart(df['annotateur'].value_counts(), "Repartition des utilisateurs"), width=6),
            dbc.Col(create_distribution_chart(df['reviewer'].value_counts(), "Repartition des validateurs"), width=6),
        ], className="p-3"),

        dbc.Row([
            dbc.Col(create_distribution_chart(df['couleur'].value_counts(), "Repartition des couleurs", color_map), width=6),
            dbc.Col(create_distribution_chart(df['marque'].value_counts(), "Repartition des marques"), width=6),
        ], className="p-3"),
    ])

# Composants pour les statistiques personnelles
def personal_stats():
    return html.Div([
        html.H4("Veuillez selectionner un utilisateur", className="mt-2 mb-2"),
        dcc.Dropdown(
            id='user-dropdown',
            options=[{'label': user['name'], 'value': user['name']} for user in users],
            value=users[0]['name'] if users else None,
            className="dropdown mb-2"
        ),
        html.Div(id='personal-stats-content', className="p-2")
    ], className="p-2")

# Callback pour mettre a jour les statistiques personnelles
@dash.callback(
    Output('personal-stats-content', 'children'),
    Input('user-dropdown', 'value')
)
def update_personal_stats(selected_user):
    if selected_user is None:
        return html.Div("Veuillez selectionner un utilisateur.")

    user_df = df[df['annotateur'] == selected_user]
    return html.Div([
        # html.Div([
        #     html.P(f"Nombre d'annotations: {len(user_df)}"),
        #     html.P(f"Nombre de validations: {count_non_empty(user_df['reviewer'])}"),
        # ], className="stats-summary"),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Nombre d'annotations", className="card-title text-center"),
                        html.P(f"{len(user_df)}", className="card-text display-6 text-center")
                    ]),
                    className="bg-primary text-white mb-4 m-2"
                    
                ),
                width=6
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Nombre de validations", className="card-title text-center"),
                        html.P(f"{count_non_empty(user_df['reviewer'])}", className="card-text display-6 text-center")
                    ]),
                    className="bg-success text-white mb-4 m-2"
                ),
                width=6
            ),
        ]),
        
        dbc.Row([
            dbc.Col(create_distribution_chart(user_df['couleur'].value_counts(), f"Repartition des couleurs pour {selected_user}", color_map), width=6),
            dbc.Col(create_distribution_chart(user_df['marque'].value_counts(), f"Repartition des marques pour {selected_user}"), width=6),
        ]
        ,className="p-1"
        ),
        
    ])

# Layout principal
layout = html.Div([
    # html.H3("Statistiques"),
    dcc.Tabs([
        dcc.Tab(label="Stats Globales", children=[global_stats()]),
        dcc.Tab(label="Stats Personnelles", children=[personal_stats()])
    ], className="custom-tabs")
])