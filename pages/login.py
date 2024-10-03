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
                    html.H1("Bienvenue sur l'interface d'annotation du groupe M2VT", className="text-center mt-5")
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
                                        dcc.Dropdown(id='user_dropdown', 
                                                     options=[{'label': user['name'], 'value': user['id']} for user in users],
                                                     placeholder="Sélectionnez votre nom",
                                                     className="mb-3"),
                                        dbc.Input(id='new_user', type='text', 
                                                  placeholder='Ou entrez un nouveau nom..',
                                                  className="mb-3"),
                                        dbc.Button('Se connecter', id='start_button', color='primary', 
                                                   n_clicks=0, className='d-grid gap-2 col-6 mx-auto'), # Centrage du bouton grâce à la grille CSS
                                        html.Div(id='user_message', className='mt-3'),
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
            ),
            dcc.Store(id='user_name_store', storage_type='local'),  # Pour stocker le nom d'utilisateur en cours sur la session
        ],
        fluid=False
    )

@callback(
    Output('user_dropdown', 'options'),
    Input('user_dropdown', 'value'),
)

def update_user_dropdown(selected_user):
    # Mettre à jour la liste des utilisateurs
    users = load_users()
    return [{'label': user['name'], 'value': user['id']} for user in users]

@callback(
    Output('user_message', 'children'), # Message de connexion
    Output('user_name_store', 'data'), # Stocker le nom d'utilisateur
    Output('url', 'href'), # Redirection vers la page d'accueil
    Input('start_button', 'n_clicks'), # Clic sur le bouton de connexion
    State('new_user', 'value'), # Valeur du nouvel utilisateur
    State('user_dropdown', 'value') # Valeur de l'utilisateur sélectionné
)

def gestion_connexion(n_clicks, new_user, selected_user):
    # Gère la connexion d'un utilisateur ou d'un nouvel utilisateur
    if n_clicks > 0:
        if new_user:
            return add_new_user(new_user)
        
        if selected_user:
            return select_existing_user(selected_user)
    
    return not_connected(), None, dash.no_update

def add_new_user(new_user):
    # Ajoute un nouvel utilisateur
    users = load_users()

    # Vérifier si l'utilisateur existe déjà
    if any(user['name'] == new_user for user in users):
        return "L'utilisateur existe déjà.", None, dash.no_update
    
    # Ajouter le nouvel utilisateur
    new_user_id = generate_user_id()
    new_user_data = {
        'id': new_user_id,
        'name': new_user
        }
    users.append(new_user_data)
    save_users(users)

    return f"Nouvel utilisateur {new_user_data['name']} ajouté.", new_user_data['name'], '/accueil'

def select_existing_user(selected_user):
    # Retourne les infos d'un utilisateur existant
    users = load_users()
    user_name = next((user['name'] for user in users if user['id'] == selected_user), None)
    return f"Vous êtes loggé en tant que {user_name}.", user_name, '/accueil'

def not_connected():
    # Retourne un message si l'utilisateur n'est pas connecté
    return html.Div([
        html.I(className="fas fa-exclamation-circle text-danger me-2"),  # Icône d'exclamation rouge
        "Vous n'êtes pas loggé."
    ], className='d-flex align-items-center')

def afficher_message_loggé():
    # Affiche un message si l'utilisateur est connecté
    return html.Div(id='user_status', className='text-right mt-2')
