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
            
            # S'assurer que les annotations sont une liste
            if isinstance(annotations, list):
                # Trouver l'annotation par id
                for annotation in annotations:
                    if str(annotation['id']) == str(annotation_id):
                        return annotation
            else:
                print("Erreur : Le fichier JSON ne contient pas une liste.")
                return None
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
    dcc.Store(id='modification-store', data=False),  # Stocker pour suivre si une modification a eu lieu

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
                dbc.Button("Modifier l'annotation", id="modifier-button", color="primary", n_clicks=0),
                width="auto"
            ),
            dbc.Col(
                dbc.Button("Supprimer l'annotation", id="supprimer-button", color="danger", n_clicks=0, disabled=False),
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
    Output('annotation-graph', 'figure', allow_duplicate=True),
    Input('url', 'href'),
    prevent_initial_call='initial_duplicate'
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
                image = load_image(annotation['nom_image'])
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

# Callback pour gérer les boutons "Valider" et "Supprimer"
@dash.callback(
    [Output('annotation-graph', 'figure', allow_duplicate=True), 
    Output('action-message', 'children', allow_duplicate=True), 
    Output('redirect', 'href')],
    [Input('valider-button', 'n_clicks'), 
    Input('supprimer-button', 'n_clicks')],
    [State('annotation-graph', 'relayoutData'), 
    State('url', 'href'), 
    State('user_name_store', 'data'), 
    State('modification-store', 'data')], 
    prevent_initial_call='initial_duplicate'
)
def handle_buttons(valider_clicks, supprimer_clicks, relayout_data, href, user_name, modification_made):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update

    # Analyser l'URL pour extraire l'ID de l'annotation
    parsed_url = urlparse(href)
    params = parse_qs(parsed_url.query)
    annotation_id = params.get('id', [None])[0]

    # Gérer le clic sur le bouton "Valider"
    if ctx.triggered[0]['prop_id'] == 'valider-button.n_clicks' and user_name:
        if annotation_id:
            # Charger toutes les annotations à partir du fichier JSON
            with open(annotations_file, 'r') as f:
                annotations = json.load(f)

            # Trouver l'annotation à mettre à jour
            updated = False
            for annotation in annotations:
                if str(annotation['id']) == str(annotation_id):
                    # Si modif = True (le bouton de modification a été cliqué), mettre à jour les annotations
                    if modification_made:
                        # Extraire les nouvelles annotations de relayoutData
                        new_annotations = []
                        for shape in relayout_data.get('shapes', []):
                            new_annotations.append({
                                'type': shape['type'],
                                'x0': shape['x0'],
                                'y0': shape['y0'],
                                'x1': shape['x1'],
                                'y1': shape['y1'],
                                'line': shape['line'],
                                'fillcolor': shape.get('fillcolor', ''),
                                'opacity': shape.get('opacity', 1)
                            })

                        # Mettre à jour les formes de l'annotation avec les nouvelles
                        annotation['annotations'] = new_annotations

                    # Toujours mettre à jour les champs reviewer et date_review
                    annotation['reviewer'] = user_name
                    annotation['date_review'] = datetime.now().strftime('%Y-%m-%d')

                    updated = True
                    break  # Arrêter après avoir trouvé et mis à jour la bonne annotation

            if updated:
                # Enregistrer les annotations mises à jour dans le fichier JSON
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                # Charger l'image pour l'annotation sélectionnée
                selected_annotation = get_annotation_by_id(annotation_id)
                if selected_annotation:
                    image = load_image(selected_annotation['nom_image'])
                    if image is not None:
                        # Créer une nouvelle figure pour l'image mise à jour
                        fig = px.imshow(image)

                        # Mettre à jour la mise en page pour permettre de dessiner un nouveau rectangle
                        fig.update_layout(
                            dragmode="drawrect",
                            newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2))
                        )

                        return fig, html.Div("L'annotation a été validée et sauvegardée avec succès.", className='text-center my-3'), '/annotation'

    # Gérer le clic sur le bouton "Supprimer"
    if ctx.triggered[0]['prop_id'] == 'supprimer-button.n_clicks':
        if annotation_id:
            if os.path.exists(annotations_file):
                with open(annotations_file, 'r') as f:
                    annotations = json.load(f)

                # Filtrer l'annotation avec l'ID correspondant
                annotations = [ann for ann in annotations if str(ann['id']) != str(annotation_id)]

                # Enregistrer les annotations mises à jour
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                return dash.no_update, f"L'annotation {annotation_id} a été supprimée.", '/annotation'

    return dash.no_update, "Une erreur s'est produite lors de l'action.", dash.no_update

# Callback pour gérer le clic sur le bouton Modifier
@dash.callback(
    [Output('annotation-graph', 'figure', allow_duplicate=True), 
     Output('action-message', 'children', allow_duplicate=True), 
     Output('supprimer-button', 'disabled'),
     Output('modification-store', 'data')],  
    [Input('modifier-button', 'n_clicks')],
    State('url', 'href'),
    prevent_initial_call='initial_duplicate'
)
def handle_modifier_button(modifier_clicks, href):
    if modifier_clicks:
        # Extraire l'ID de l'annotation de l'URL
        parsed_url = urlparse(href)
        params = parse_qs(parsed_url.query)
        annotation_id = params.get('id', [None])[0]

        if annotation_id:
            # Charger toutes les annotations à partir du fichier JSON
            with open(annotations_file, 'r') as f:
                annotations = json.load(f)

            # Trouver et effacer uniquement le champ 'annotations' pour l'annotation sélectionnée
            updated = False
            for annotation in annotations:
                if str(annotation['id']) == str(annotation_id):
                    # Effacer les formes dans l'annotation
                    annotation['annotations'] = []  # Effacer les annotations pour le véhicule sélectionné
                    updated = True
                    break  # Arrêter après avoir trouvé et mis à jour la bonne annotation

            if updated:
                # Enregistrer les annotations mises à jour dans le fichier JSON
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                # Charger l'image pour l'annotation sélectionnée
                selected_annotation = get_annotation_by_id(annotation_id)
                if selected_annotation:
                    image = load_image(selected_annotation['nom_image'])
                    if image is not None:
                        # Créer une nouvelle figure pour l'image mise à jour
                        fig = px.imshow(image)

                        # Mettre à jour la mise en page pour permettre de dessiner un nouveau rectangle
                        fig.update_layout(
                            dragmode="drawrect",
                            newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2))
                        )

                        return fig, html.Div("L'ancienne annotation a été supprimée. Vous pouvez dessiner une nouvelle annotation.", className='text-center'), True, True  # Définir modification à True

    return dash.no_update, dash.no_update, False, False  # Définir modification à False si non cliqué