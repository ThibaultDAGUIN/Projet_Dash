# -*- coding: utf-8 -*-


# pages/login.py
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import json
import os

# Enregistrer la page dans le registre avec le décorateur
dash.register_page(__name__, path='/login', name='Login', order=1)

# Fichier JSON pour stocker les utilisateurs
data_users = 'users.json'

# Charger les utilisateurs existants depuis le fichier JSON
def load_users():
    if os.path.exists(data_users):
        with open(data_users, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Fonction pour sauvegarder les utilisateurs dans le fichier JSON
def save_users(users):
    with open(data_users, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4)

# Générer un ID unique pour chaque nouvel utilisateur
def generate_user_id():
    users = load_users()
    if users:
        return max(user['id'] for user in users) + 1
    return 1

# Charger les utilisateurs au démarrage
users = load_users()

# Layout de la page de connexion
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Bienvenue sur l'interface d'annotation", className="text-center mt-5")
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Identifiez-vous"),
                            dbc.CardBody(
                                [
                                    html.H5("Sélectionnez un utilisateur ou ajoutez-en un nouveau", className="card-title"),
                                    dcc.Dropdown(
                                        id='user-dropdown',
                                        options=[{'label': user['name'], 'value': user['id']} for user in users],
                                        placeholder="Sélectionnez votre nom",
                                        className="mb-3"
                                    ),
                                    dbc.Input(
                                        id='new-user',
                                        type='text',
                                        placeholder='Ou entrez un nouveau nom...',
                                        className="mb-3"
                                    ),
                                    dbc.Button(
                                        'Commencer l\'annotation',
                                        id='start-button',
                                        color='primary',
                                        n_clicks=0,
                                        className='d-grid gap-2 col-6 mx-auto'
                                    ),
                                    html.Div(id='user-message', className='mt-3')
                                ]
                            )
                        ],
                        className="shadow-lg p-3 mb-2 bg-white rounded"
                    ),
                    width=6,
                    className="offset-md-3"
                )
            ],
            className="mt-5"
        ),
        dbc.Row(
            dbc.Col(
                html.Footer(
                    dcc.Markdown(
                        """
                        **© 2024 Projet d'annotation - Dash**

                        Contributeurs du projet : Thibault DAGUIN, Vadim MARTIN, Maël CHAINE, Manon BONNAUD-DUBOIS
                        """
                    ),
                    className="text-center mt-5"
                )
            )
        )
    ],
    fluid=False
)

# Callback pour ajouter un nouvel utilisateur
@callback(
    Output('user-dropdown', 'options'),
    Output('user-message', 'children'),
    Input('start-button', 'n_clicks'),
    State('new-user', 'value'),
    State('user-dropdown', 'options')
)
def add_new_user(n_clicks, new_user, dropdown_options):
    users = load_users()  # Charger la liste actuelle des utilisateurs
    if n_clicks > 0 and new_user:
        # Vérifier si l'utilisateur existe déjà
        if any(user['name'] == new_user for user in users):
            return dropdown_options, "L'utilisateur existe déjà."

        # Ajouter le nouvel utilisateur
        new_user_id = generate_user_id()
        new_user_data = {'id': new_user_id, 'name': new_user}
        users.append(new_user_data)
        save_users(users)  # Sauvegarder les utilisateurs

        # Mettre à jour les options du dropdown
        updated_options = [{'label': user['name'], 'value': user['id']} for user in users]
        return updated_options, f"Nouvel utilisateur {new_user} ajouté."

    return dropdown_options, "Veuillez entrer un nom valide."
