# -*- coding: utf-8 -*-


from dash import html
import dash

# Enregistrer la page dans le registre avec le décorateur
dash.register_page(__name__, path='/apropos', name='A propos',order=5)

layout = html.Div([
    html.H3("A propos de nous"),
    html.P("Page de présentation de l'équipe."),
])