import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from skimage import io
import os
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime

dash.register_page(__name__, path_template="/verify")

# File paths
dossier_img = './data/cars/'
annotations_file = './data/annotations.json'

# Function to load annotation by ID
def get_annotation_by_id(annotation_id):
    if os.path.exists(annotations_file):
        with open(annotations_file, 'r') as f:
            annotations = json.load(f)
            for annotation in annotations:
                if str(annotation['id']) == str(annotation_id):  # Ensure ID is compared as string
                    return annotation
    return None

# Function to load image by name
def load_image(image_name):
    img_path = os.path.join(dossier_img, image_name)
    if os.path.exists(img_path):
        return io.imread(img_path)
    else:
        print(f"Image {image_name} not found at path {img_path}")
        return None

# Layout for the verify page
layout = html.Div([
    html.H3("Vérifier l'Annotation"),
    dcc.Graph(id='annotation-graph'),
    dbc.Button("Valider", id="valider-button", color="success", n_clicks=0),
    html.Div(id="action-message") 
])

# Callback to display image with annotations
@dash.callback(
    Output('annotation-graph', 'figure'),
    Input('url', 'href')
)
def display_image_with_annotations(href):
    if href:
        # Parse the URL to extract the annotation ID
        parsed_url = urlparse(href)
        params = parse_qs(parsed_url.query)
        annotation_id = params.get('id', [None])[0]

        if annotation_id:
            # Get annotation data by ID
            annotation = get_annotation_by_id(annotation_id)
            if annotation:
                # Load the corresponding image
                image = load_image(annotation['image_name'])
                if image is not None:
                    fig = px.imshow(image)

                    # Iterate through each annotation shape and add it to the figure
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

# Callback to handle "Valider" button click and update the reviewer and review_date
@dash.callback(
    Output('action-message', 'children'),
    Input('valider-button', 'n_clicks'),
    State('url', 'href'),
    State('user_name_store', 'data'),
    prevent_initial_call=True
)
def handle_valider(n_clicks, href, user_name):
    if n_clicks > 0 and user_name:
        # Parse the URL to extract the annotation ID
        parsed_url = urlparse(href)
        params = parse_qs(parsed_url.query)
        annotation_id = params.get('id', [None])[0]

        if annotation_id:
            # Load the annotation and update the reviewer and review_date
            if os.path.exists(annotations_file):
                with open(annotations_file, 'r') as f:
                    annotations = json.load(f)
                
                for annotation in annotations:
                    if str(annotation['id']) == str(annotation_id):  # Ensure ID comparison is correct
                        # Update the reviewer field
                        annotation['reviewer'] = user_name
                        # Add the review date in YYYY-MM-DD format
                        annotation['review_date'] = datetime.now().strftime('%Y-%m-%d')
                        break

                # Save the updated annotations
                with open(annotations_file, 'w') as f:
                    json.dump(annotations, f, indent=2)

                return f"L'annotation a bien été validée par {user_name}."

    return "Une erreur s'est produite lors de la validation."
