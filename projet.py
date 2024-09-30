import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import json
import os

# Enregistrer la page dans le registre avec le décorateur
dash.register_page(__name__, path='/login', name='Login', order=6)

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Liste des annotateurs déjà connus
data_users = 'users.json'

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

# Layout de la page d'accueil ergonomique
def home_layout():
    return dbc.Container(
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
                                        dbc.Button('Commencer l\'annotation', id='start-button', color='primary', 
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

# Layout pour la page d'annotation (exemple simplifié)
def annotate_layout():
    return dbc.Container([
        html.H1("Page d'annotation"),
        dcc.Link('Retour à l\'accueil', href='/'),
    ], fluid=True)

# App layout général
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback pour ajouter un nouvel utilisateur
@app.callback(
    Output('user-dropdown', 'options'),
    Output('user-message', 'children'),
    Input('start-button', 'n_clicks'),
    State('new-user', 'value'),
    State('user-dropdown', 'options')
)

def add_new_user(n_clicks, new_user, dropdown_options):
    if n_clicks > 0 and new_user:
        # Vérifier si l'utilisateur existe déjà
        if any(user['name'] == new_user for user in users):
            return dropdown_options, "L'utilisateur existe déjà."
        
        # Sinon, ajouter le nouvel utilisateur avec un ID unique
        new_user_id = generate_user_id()
        new_user = {'id': new_user_id, 'name': new_user}
        users.append(new_user)
        save_users(users)  # Sauvegarder dans le fichier JSON
        
        # Mettre à jour les options du dropdown
        updated_options = [{'label': user['name'], 'value': user['id']} for user in users]
        return updated_options, f"Nouvel utilisateur {new_user['name']} ajouté."

    return dropdown_options, "Veuillez entrer un nom valide."


# # Callbacks pour gérer la navigation
# @app.callback(
#     Output('page-content', 'children'),
#     [Input('url', 'pathname')]
# )
# def display_page(pathname):
#     if pathname == '/annotate':
#         return annotate_layout()
#     else:
#         return home_layout()

# if __name__ == '__main__':
#     app.run_server(debug=True)