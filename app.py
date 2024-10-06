import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[
    dbc.themes.BOOTSTRAP, 
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
    "https://fonts.googleapis.com/css2?family=Roboto&display=swap",
    ])

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dbc.NavbarSimple(
        children=[
            dbc.NavLink('Accueil', href='/accueil'),
            dbc.NavLink('À propos', href='/apropos'),
            dbc.NavLink('Interface d\'annotation', href='/annoter'),
            dbc.NavLink('Liste des annotations', href='/annotation'),
            dbc.NavLink('Statistiques', href='/stats'),
            html.Span(id='user_status', className='text-light align-self-center', style={'font-size': '0.9rem', 'marginLeft': '100px', 'marginRight':'20px'}),
            dbc.Button('Déconnexion', color='danger', outline=True, className='text-light align-self-center', style={'font-size': '0.8rem'}, id='logout_button', n_clicks=0),
        ],
        brand="Groupe MC BDD",
        color="#333333",
        dark=True,
        id='navbar',
    ),
    dash.page_container,
    dcc.Store(id='user_name_store', storage_type='local')  # Pour stocker le nom d'utilisateur en cours sur la session
])

@callback(
    Output('user_status', 'children', allow_duplicate=True),
    Input('user_name_store', 'data'),
    prevent_initial_call='True'
)

def afficher_message_loggé(user_name):
    if user_name:
        return f"Vous êtes loggé en tant que {user_name}."
    return "Vous n'êtes pas loggé."

@callback(
    Output('navbar', 'style'),
    Input('url', 'pathname'),
)

def toggle_navbar(pathname):
    # On masque la navbar sur la page de login
    if pathname == '/':
        return {'display': 'none'}
    return {'display': 'block'}

@callback(
    Output('url', 'href', allow_duplicate=True),
    Input('logout_button', 'n_clicks'),
    prevent_initial_call=True
)

def handle_logout(n_clicks):
    if n_clicks > 0:
        return '/'  # Redirection vers la page de connexion
    return dash.no_update

if __name__ == '__main__':
    app.run(debug=True)