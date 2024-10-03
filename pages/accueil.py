import dash
from dash import html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div([
    dcc.Store(id='user_name_store', storage_type='local'), # Pour stocker le nom d'utilisateur en cours sur la session
    html.H1("C'est la page de contexte"),
    html.Div("C'est la page de contexte"),
    html.Div(id='welcome_message')  # Dans ton layout
])

# Callback pour afficher le message de bienvenue avec le nom d'utilisateur
@dash.callback(
    Output('welcome_message', 'children'),
    Input('user_name_store', 'data')
)
def afficher_nom_user(user_name):
    if user_name:
        return html.H4(f"Bienvenue {user_name} !", className="text-center")
    else:
        return html.H4("Bienvenue, veuillez vous connecter.", className="text-center")