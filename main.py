
# -*- coding: utf-8 -*-

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State  # Importer Input, Output, State


# Activer les pages dynamiques avec use_pages=True
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Hauteur de la navbar pour le padding-top
NAVBAR_HEIGHT = "70px"

# Layout de l'application
app.layout = html.Div([
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("Groupe MC BDD", href="/login", className="d-flex align-items-center"),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [dcc.Link(page["name"], href=page["relative_path"], className="nav-link") for page in dash.page_registry.values()],
                    className="ms-lg-5", navbar=True
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True
            ),
        ]),
        color="dark", dark=True, fixed="top", className="mb-5"
    ),
    html.Div(dash.page_container, style={"padding-top": NAVBAR_HEIGHT})
])

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar(n, is_open):
    if n:
        return not is_open
    return is_open

# Point d'entree de l'application
if __name__ == "__main__":
    app.run_server(debug=True)
