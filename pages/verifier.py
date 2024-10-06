import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from skimage import io
import os
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime

dash.register_page(__name__, path_template="/verifier")

# Chemins des fichiers
dossier_img = './data/cars/'
annotations_file = './data/annotations.json'

# Fonction pour charger une annotation par ID
def get_annotation_by_id(annotation_id):
    if os.path.exists(annotations_file):
        with open(annotations_file, 'r') as f:
            annotations = json.load(f)
            for annotation in annotations:
                if str(annotation['id']) == str(annotation_id):  # S'assurer que l'ID est comparé en tant que chaîne
                    return annotation
    return None

# Fonction pour charger une image par nom
def load_image(image_name):
    img_path = os.path.join(dossier_img, image_name)
    if os.path.exists(img_path):
        return io.imread(img_path)
    else:
        print(f"Image {image_name} non trouvée au chemin {img_path}")
        return None

# Mise en page pour la page de vérification
layout = html.Div([
    html.H3("Vérifier l'Annotation", className='text-center my-3'),
    dcc.Graph(id='annotation-graph'),
    
    # Centrer les boutons en utilisant une ligne Bootstrap
    dbc.Row(
        [
            dbc.Col(
                dbc.Button("Valider l'annotation", id="valider-button", color="success", n_clicks=0),
                width="auto"
            ),
            dbc.Col(
                dbc.Button("Supprimer l'annotation", id="supprimer-button", color="danger", n_clicks=0),
                width="auto"
            )
        ],
        justify="center",  # Centrer les boutons
        className="my-3"  # Ajouter une marge verticale
    ),
    
    html.Div(id="action-message"),
    dcc.Location(id="redirect", refresh=True)
])

# Callback pour afficher l'image avec les annotations
@dash.callback(
    Output('annotation-graph', 'figure'),
    Input('url', 'href')
)
def display_image_with_annotations(href):
    if href:
        # Analyser l'URL pour extraire l'ID de l'annotation
        parsed_url = urlparse(href)
        params = parse_qs(parsed_url.query)
        annotation_id = params.get('id', [None])[0]

        if annotation_id:
            # Obtenir les données d'annotation par ID
            annotation = get_annotation_by_id(annotation_id)
            if annotation:
                # Charger l'image correspondante
                image = load_image(annotation['nom_image'])  # Changer 'image_name' en 'nom_image'
                if image is not None:
                    fig = px.imshow(image)

                    # Parcourir chaque forme d'annotation et l'ajouter à la figure
                    for ann in annotation['annotations']:
                        fig.add_shape(
                            type=ann['type'],
                            x0=ann['x0'],
                            y0=ann['y0'],
                            x1=ann['x1'],
                            y1=ann['y1'],
                            line=dict(
                                color=ann['line']['color'],
                                width=ann['line']['width'],
                                dash=ann['line']['dash']
                            ),
                            fillcolor=ann['fillcolor'],
                            opacity=ann['opacity']
                        )

                    return fig
    return {}

# Callback combiné pour gérer les clics sur les boutons "Valider" et "Supprimer"
@dash.callback(
    [Output('action-message', 'children'), Output('redirect', 'href')],
    [Input('valider-button', 'n_clicks'), Input('supprimer-button', 'n_clicks')],
    State('url', 'href'),
    State('user_name_store', 'data'),
    prevent_initial_call=True
)
def handle_buttons(valider_clicks, supprimer_clicks, href, user_name):
    # Déterminer quel bouton a été cliqué
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update

    # Analyser l'URL pour extraire l'ID de l'annotation
    parsed_url = urlparse(href)
    params = parse_qs(parsed_url.query)
    annotation_id = params.get('id', [None])[0]

    # Gérer le clic sur le bouton "Valider"
    if ctx.triggered[0]['prop_id'] == 'valider-button.n_clicks' and user_name:
        if annotation_id:
            # Charger l'annotation et mettre à jour le reviewer et la date de révision
            if os.path.exists(annotations_file):
                with open(annotations_file, 'r') as f:
                    annotations = json.load(f)

                for annotation in annotations:
                    if str(annotation['id']) == str(annotation_id):  # S'assurer que la comparaison de l'ID est correcte
                        # Mettre à jour le champ reviewer
                        annotation['reviewer'] = user_name
                        # Ajouter la date de révision au format AAAA-MM-JJ
                        annotation['date_review'] = datetime.now().strftime('%Y-%m-%d')  # Changer en 'date_review'
                        break

                # Enregistrer les annotations mises à jour
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                # Rediriger vers la page des annotations
                return f"L'annotation a bien été validée par {user_name}.", '/annotation'

    # Gérer le clic sur le bouton "Supprimer"
    if ctx.triggered[0]['prop_id'] == 'supprimer-button.n_clicks':
        if annotation_id:
            # Charger les annotations et supprimer celle spécifiée
            if os.path.exists(annotations_file):
                with open(annotations_file, 'r') as f:
                    annotations = json.load(f)

                # Filtrer l'annotation avec l'ID correspondant
                annotations = [ann for ann in annotations if str(ann['id']) != str(annotation_id)]

                # Enregistrer les annotations mises à jour
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                # Rediriger vers la page des annotations
                return f"L'annotation {annotation_id} a été supprimée.", '/annotation'

    return "Une erreur s'est produite lors de la validation.", dash.no_update
