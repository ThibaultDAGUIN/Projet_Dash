# -*- coding: utf-8 -*-


from dash import html
import dash

# Enregistrer la page dans le registre avec le décorateur
dash.register_page(__name__, path='/contribuer', name='Contribuer', order=2)

layout = html.Div([
    html.H3("Annotation d'une image"),
    html.P("Page d'annotation d'une image."),
])