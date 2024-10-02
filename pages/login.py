import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import json
import os

dash.register_page(__name__, path='/') # '/' sert à faire la page d'accueil

# Liste des annotateurs déjà connus
data_users = './data/users.json'

def load_users():
    if os.path.exists(data_users):
        with open(data_users, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Fonction pour sauvegarder les utilisateurs
def save_users(users):
    with open(data_users, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4)

users = load_users()

def generate_user_id():
    if users:
        return max(user['id'] for user in users) + 1
    return 1

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
                                        dcc.Dropdown(id='user-dropdown', 
                                                     options=[{'label': user['name'], 'value': user['id']} for user in users],
                                                     placeholder="Sélectionnez votre nom",
                                                     className="mb-3"),
                                        dbc.Input(id='new-user', type='text', 
                                                  placeholder='Ou entrez un nouveau nom..',
                                                  className="mb-3"),
                                        dbc.Button('Se connecter', id='start-button', color='primary', 
                                                   n_clicks=0, className='d-grid gap-2 col-6 mx-auto'), # Centrage du bouton grâce à la grille CSS
                                        html.Div(id='user-message', className='mt-3'),
                                        html.Div(className="mt-3") # Ajout d'un peu d'espace en bas de la card
                                    ]
                                )
                            ],
                            className="shadow-lg p-3 mb-2 bg-white rounded" # Ombrage + Marge Basse + Bord rond blanc
                        ),
                        width=6, # Centrer au milieu de la page
                        className="offset-md-3"  # Centre la colonne dans la page
                    )
                ],
                className="mt-5"
            ),
            dbc.Row(
                dbc.Col(
                    html.Footer([
                        dcc.Markdown("""
                            **© 2024 Projet d'annotation - Dash**
                                     
                            Contributeurs du projet : Thibault DAGUIN, Vadim MARTIN, Maël CHAINE, Manon BONNAUD-DUBOIS
                            """)
                    ],
                        className="text-center mt-5"
                    )
                )
            )
        ],
        fluid=False
    )

@callback(
    Output('user-dropdown', 'options'),
    Output('user-message', 'children'),
    Output('user-name-store', 'data'),
    Output('url', 'href'),
    Input('start-button', 'n_clicks'),
    State('new-user', 'value'),
    State('user-dropdown', 'value')
)

def add_new_user(n_clicks, new_user, selected_user):
    if n_clicks > 0:
        if new_user:
            # Vérifier si l'utilisateur existe déjà
            if any(user['name'] == new_user for user in users):
                return [{'label': user['name'], 'value': user['id']} for user in users], "L'utilisateur existe déjà.", None, dash.no_update
            
            # Ajouter le nouvel utilisateur
            new_user_id = generate_user_id()
            new_user_dict = {'id': new_user_id, 'name': new_user}
            users.append(new_user_dict)
            save_users(users)
            
            updated_options = [{'label': user['name'], 'value': user['id']} for user in users]
            return updated_options, f"Nouvel utilisateur {new_user_dict['name']} ajouté.", new_user_dict['name'], '/accueil'
        
        if selected_user:  # Si un utilisateur est sélectionné
            user_name = next((user['name'] for user in users if user['id'] == selected_user), None)
            return [{'label': user['name'], 'value': user['id']} for user in users], f"Vous êtes loggé en tant que {user_name}.", user_name, '/accueil'

    return (
        [{'label': user['name'], 'value': user['id']} for user in users],
        html.Div([
            html.I(className="fas fa-exclamation-circle text-danger me-2"),  # Icône d'exclamation rouge
            "Vous n'êtes pas loggé."
        ], className='d-flex align-items-center'),  # Aligne l'icône et le texte
        None,
        dash.no_update
    )

def on_login(n_clicks, new_user, selected_user):
    if n_clicks > 0:
        if selected_user:
            return selected_user, f"Vous êtes loggé en tant que {next(user['name'] for user in users if user['id'] == selected_user)}."
        elif new_user:
            return new_user, f"Vous êtes loggé en tant que {new_user}."
    return None, "Vous n'êtes pas loggé."