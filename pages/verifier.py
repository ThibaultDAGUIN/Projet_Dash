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



# Paths to files
dossier_img = './data/cars/'
annotations_file = './data/annotations.json'

# Function to load an annotation by ID
def get_annotation_by_id(annotation_id):
    if os.path.exists(annotations_file):
        with open(annotations_file, 'r') as f:
            annotations = json.load(f)
            
            if isinstance(annotations, list):
                for annotation in annotations:
                    if str(annotation['id']) == str(annotation_id):
                        return annotation
    return None

# Function to load an image by name
def load_image(image_name):
    img_path = os.path.join(dossier_img, image_name)
    if os.path.exists(img_path):
        return io.imread(img_path)
    else:
        print(f"Image {image_name} not found at path {img_path}")
        return None

# Layout for the verification page
layout = html.Div([
    dcc.Store(id='modification-store', data=False),  # Store to track if modification happened

    html.H3("Vérifier l'Annotation", className='text-center my-3'),
    dcc.Graph(id='annotation-graph'),
    
    # Dropdowns for vehicle brand and color
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                placeholder="Marque du véhicule",
                id="marque_vehicule",
                style={'width': '400px', 'text-align': 'center'},
                options=[
                    {'label': 'Audi', 'value': 'Audi'},
                    {'label': 'BMW', 'value': 'BMW'},
                    {'label': 'Citroën', 'value': 'Citroen'},
                    {'label': 'Dacia', 'value': 'Dacia'},
                    {'label': 'Fiat', 'value': 'Fiat'},
                    {'label': 'Ford', 'value': 'Ford'},
                    {'label': 'Mercedes', 'value': 'Mercedes'},
                    {'label': 'Peugeot', 'value': 'Peugeot'},
                    {'label': 'Renault', 'value': 'Renault'},
                    {'label': 'Toyota', 'value': 'Toyota'},
                    {'label': 'Volkswagen', 'value': 'Volkswagen'},
                    {'label': 'Mazda', 'value': 'Mazda'},
                    {'label': 'Tesla', 'value': 'Tesla'},
                    {'label': 'Porsche', 'value': 'Porsche'},
                    {'label': 'Autre', 'value': 'Autre'},
                ],
                #    value=marque_value,
            ),
            width='auto'
        ),
        
        dbc.Col(
            dcc.Dropdown(
                placeholder="Couleur du véhicule",
                id="couleur_vehicule",
                style={'width': '400px', 'text-align': 'center'},
                options=[
                    {'label': 'Blanc', 'value': 'Blanc'},
                    {'label': 'Noir', 'value': 'Noir'},
                    {'label': 'Bleu', 'value': 'Bleu'},
                    {'label': 'Rouge', 'value': 'Rouge'},
                    {'label': 'Vert', 'value': 'Vert'},
                    {'label': 'Jaune', 'value': 'Jaune'},
                    {'label': 'Gris', 'value': 'Gris'},
                    {'label': 'Marron', 'value': 'Marron'},
                    {'label': 'Orange', 'value': 'Orange'},
                    {'label': 'Violet', 'value': 'Violet'},
                    {'label': 'Rose', 'value': 'Rose'},
                    {'label': 'Autre', 'value': 'Autre'},
                ],
                # value=couleur_value,
            ),
            width='auto'
        ),
    ],
    justify='center',
    className='d-flex my-3',
    style={'alignItems': 'center'}
    ),

    # Center buttons using a Bootstrap row
    dbc.Row([
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
    justify="center",  # Center buttons
    className="my-3"  # Add vertical margin
    ),

    html.Div(id="action-message"),
    dcc.Location(id="redirect", refresh=True)
])

# Callback to display the image with annotations
@dash.callback(
    Output('annotation-graph', 'figure', allow_duplicate=True),
    Input('url', 'href'),
    prevent_initial_call='initial_duplicate'
)
def display_image_with_annotations(href):
    if href:
        # Parse the URL to extract the annotation ID
        parsed_url = urlparse(href)
        params = parse_qs(parsed_url.query)
        annotation_id = params.get('id', [None])[0]

        if annotation_id:
            # Get the annotation by ID
            annotation = get_annotation_by_id(annotation_id)
            if annotation:
                # Load the corresponding image
                image = load_image(annotation['nom_image'])
                if image is not None:
                    fig = px.imshow(image)

                    # Iterate through each annotation shape and add to the figure
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

# Callback to handle button actions (validate and delete)
@dash.callback(
    [Output('annotation-graph', 'figure', allow_duplicate=True), 
    Output('action-message', 'children', allow_duplicate=True), 
    Output('redirect', 'href')],
    [Input('valider-button', 'n_clicks'), 
    Input('supprimer-button', 'n_clicks')],
    [State('annotation-graph', 'relayoutData'), 
    State('url', 'href'), 
    State('user_name_store', 'data'), 
    State('modification-store', 'data'),
    State('marque_vehicule', 'value'), 
    State('couleur_vehicule', 'value')], 
    prevent_initial_call='initial_duplicate'
)
def handle_buttons(valider_clicks, supprimer_clicks, relayout_data, href, user_name, modification_made, marque, couleur):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update

    # Parse the URL to extract the annotation ID
    parsed_url = urlparse(href)
    params = parse_qs(parsed_url.query)
    annotation_id = params.get('id', [None])[0]

    # Handle "Validate" button click
    if ctx.triggered[0]['prop_id'] == 'valider-button.n_clicks' and user_name:
        if annotation_id:
            # Load all annotations from the JSON file
            with open(annotations_file, 'r') as f:
                annotations = json.load(f)

            # Find the annotation to update
            updated = False
            for annotation in annotations:
                if str(annotation['id']) == str(annotation_id):
                    # If modification button has been clicked, update annotations
                    if modification_made:
                        # Extract new annotations from relayoutData
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

                        # Update the annotation's shapes with the new ones
                        annotation['annotations'] = new_annotations

                    # Update reviewer and review date fields
                    annotation['reviewer'] = user_name
                    annotation['date_review'] = datetime.now().strftime('%Y-%m-%d')

                    # Update marque and couleur from the dropdowns
                    annotation['marque'] = marque  # Update marque
                    annotation['couleur'] = couleur  # Update couleur

                    updated = True
                    break  # Stop after finding and updating the right annotation

            if updated:
                # Save the updated annotations back to the JSON file
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                # Load the image for the selected annotation
                selected_annotation = get_annotation_by_id(annotation_id)
                if selected_annotation:
                    image = load_image(selected_annotation['nom_image'])
                    if image is not None:
                        # Create a new figure for the updated image
                        fig = px.imshow(image)

                        # Update the layout to enable drawing a new rectangle
                        fig.update_layout(
                            dragmode="drawrect",
                            newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2))
                        )

                        return fig, html.Div("L'annotation a été validée et sauvegardée avec succès.", className='text-center my-3'), '/annotation'

    # Handle "Delete" button click
    if ctx.triggered[0]['prop_id'] == 'supprimer-button.n_clicks':
        if annotation_id:
            if os.path.exists(annotations_file):
                with open(annotations_file, 'r') as f:
                    annotations = json.load(f)

                # Filter out the annotation with the corresponding ID
                annotations = [ann for ann in annotations if str(ann['id']) != str(annotation_id)]

                # Save the updated annotations
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                return dash.no_update, f"L'annotation {annotation_id} a été supprimée.", '/annotation'

    return dash.no_update, "Une erreur s'est produite lors de l'action.", dash.no_update

# Callback to handle the click on the "Edit" button
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
        # Extract the annotation ID from the URL
        parsed_url = urlparse(href)
        params = parse_qs(parsed_url.query)
        annotation_id = params.get('id', [None])[0]

        if annotation_id:
            # Load all annotations from the JSON file
            with open(annotations_file, 'r') as f:
                annotations = json.load(f)

            # Find and clear only the 'annotations' field for the selected annotation
            updated = False
            for annotation in annotations:
                if str(annotation['id']) == str(annotation_id):
                    # Clear the shapes in the annotation
                    annotation['annotations'] = []  # Clear the annotations for the selected vehicle
                    updated = True
                    break  # Stop after finding and updating the right annotation

            if updated:
                # Save the updated annotations back to the JSON file
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                # Load the image for the selected annotation
                selected_annotation = get_annotation_by_id(annotation_id)
                if selected_annotation:
                    image = load_image(selected_annotation['nom_image'])
                    if image is not None:
                        # Create a new figure for the updated image
                        fig = px.imshow(image)

                        # Update the layout to enable drawing a new rectangle
                        fig.update_layout(
                            dragmode="drawrect",
                            newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2))
                        )

                        return fig, html.Div("L'ancienne annotation a été supprimée. Vous pouvez dessiner une nouvelle annotation.", className='text-center'), True, True  # Set modification to True

    return dash.no_update, dash.no_update, False, False  # Set modification to False if not clicked