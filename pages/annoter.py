import dash
from dash import dcc, html, Input, Output, callback, State
from skimage import io
import plotly_express as px
import os
import json
import random
import base64
import dash_bootstrap_components as dbc
from datetime import datetime

# Define paths for images and JSON files
dossier_img = './data/cars/'
users_file = './data/users.json'
annotations_file = './data/annotations.json'

# Function to retrieve a random image
def recup_img_aleatoire():
    files = os.listdir(dossier_img)
    images = [file for file in files if file.endswith(('png', 'jpg', 'jpeg'))]
    if images:
        random_image = random.choice(images)
        return os.path.join(dossier_img, random_image)
    return None

# Function to load an image and return it with its filename
def charger_image():
    chemin_image = recup_img_aleatoire()
    if chemin_image:
        img = io.imread(chemin_image)
        return img, os.path.basename(chemin_image)  # Return both image and filename
    return None, None  # Return None for both if no image is found

# Function to save uploaded image
def save_img(content, filename):
    data = content.split(",")[1]
    img_data = base64.b64decode(data)
    file_unique = f"{filename}"
    filepath = os.path.join(dossier_img, file_unique)
    with open(filepath, 'wb') as f:
        f.write(img_data)
    return filepath

# Register the Dash app page
dash.register_page(__name__)

# Load initial image and filename
img, filename = charger_image()

if img is not None:
    fig = px.imshow(img)
    fig.update_layout(
        dragmode="drawrect",
        newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
    )
else:
    fig = None

# Layout of the Dash app
layout = html.Div(
    [
        html.H3("Interface d'annotation", className='text-center my-3'),
        dcc.Graph(id="graph-styled-annotations", figure=fig),

        # Store the filename in hidden storage
        dcc.Store(id='filename_store', data=filename),

        dcc.Upload(
            id="import-image",
            children=html.Div(
                ['Glissez et déposez une image ici, ou ',
                 html.A('sélectionnez une image')],
                style={
                    'borderWidth': '0.5px', 'borderStyle': 'solid', 'backgroundColor':'rgba(66, 66, 66, 0.15)',
                    'padding': '20px', 'textAlign': 'center', 'width': '50%',
                    'margin': '5px auto', 'cursor': 'pointer',
                    'font-family': 'Roboto, sans-serif',
                }
            ),
            multiple=False
        ),

        dbc.Modal(
            [
                dbc.ModalHeader("Confirmation de l'importation"),
                dbc.ModalBody("Voulez-vous confirmer l'importation de ce fichier ?"),
                dbc.ModalFooter(
                    [
                        dbc.Button("Oui", id="confirmer_modal", color="success"),
                        dbc.Button("Non", id="fermer_modal", color="danger", className="ms-2"),
                    ]
                ),
            ],
            id="modal",
            is_open=False,
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Valider l'annotation",
                        id="bouton_valider",
                        color='success',
                        n_clicks=0,
                    ),
                    width='auto'
                ),
                
                dbc.Col(
                    dbc.Button(
                        "Modifier l'annotation",
                        id="bouton_reset",
                        color='danger',
                        n_clicks=0,
                    ),
                    width='auto'
                ),
            ],
            justify='center',
            className='my-3',
        ),
        html.Pre(id="annotation_data", className='my-3'),
        dcc.Store(id='user_name_store', storage_type='local'), # Store the current user's name in the session
    ]
)

# Callback to handle the upload modal and image display
@callback(
    Output('modal', 'is_open'), # Open or close the modal
    Output('graph-styled-annotations', 'figure', allow_duplicate=True), # Update the displayed image
    Input('import-image', 'contents'),
    Input('fermer_modal', 'n_clicks'),
    Input('confirmer_modal', 'n_clicks'),
    State('modal', 'is_open'),
    State('import-image', 'filename'),
    State('graph-styled-annotations', 'figure'),
    prevent_initial_call=True
)
def activer_modal(contenu_img, cancel_clicks, confirm_clicks, is_open, filename, current_fig):
    # Open the modal when an image is uploaded
    if contenu_img is not None and is_open is False:
        return True, current_fig
    
    # If "No" is clicked, close the modal without doing anything
    if cancel_clicks:
        return False, current_fig
    
    # If "Yes" is clicked, save the image
    if confirm_clicks:
        save_img(contenu_img, filename)
        
        # Load the saved image to display
        img, next_filename = charger_image()  # Get the next image and its filename
        if img is not None:
            fig = px.imshow(img)
            fig.update_layout(
                dragmode="drawrect",
                newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
            )
            # Update the filename in store
            return False, fig

        return False, None  # In case no next image is available
    
    # If no action has been taken, do not change anything
    return is_open, current_fig

# Callback to handle annotation submission
@callback(
    Output('annotation_data', 'children'),
    Output('graph-styled-annotations', 'figure'),
    Output('bouton_valider', 'disabled', allow_duplicate=True),
    Output('filename_store', 'data'),  # Add this output to update the filename store
    Input("bouton_valider", "n_clicks"),
    State('graph-styled-annotations', 'relayoutData'),
    State('user_name_store', 'data'),
    State('filename_store', 'data'), 
    prevent_initial_call=True
)
def afficher_annotation(n_clicks, relayoutData, user_name, filename):
    if n_clicks is None and user_name:
        return dash.no_update, dash.no_update, True, dash.no_update

    if relayoutData is not None and 'shapes' in relayoutData and relayoutData['shapes']:
        try:
            # Load existing annotations
            annotations_data = []
            if os.path.exists(annotations_file):
                with open(annotations_file, 'r') as f:
                    annotations_data = json.load(f)

            # Create a new annotation entry
            new_annotation = {
                'id': len(annotations_data) + 1,
                'image_name': filename,  # Ensure this is set correctly
                'annotateur': user_name,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'reviewer': '',
                "review_date": '',
                'annotations': relayoutData['shapes']
            }

            # Append new annotation and save
            annotations_data.append(new_annotation)
            with open(annotations_file, 'w') as f:
                json.dump(annotations_data, f, indent=2)

            # Confirmation message
            message = f"L'annotation réalisée par {user_name} a bien été enregistrée."

            # Load the next image
            img, next_filename = charger_image()  # Get the next image and filename
            if img is not None:
                fig = px.imshow(img)
                fig.update_layout(
                    dragmode="drawrect",
                    newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
                )
                
                # Update the filename in the store
                return html.Div(message, className='text-center', style={'font-family': 'Roboto, sans-serif'}), fig, True, next_filename

            else:
                return html.Div(message, className='text-center', style={'font-family': 'Roboto, sans-serif'}), None, True, dash.no_update

        except Exception as e:
            return html.Div("L'annotation a échoué, veuillez réessayer.", style={'font-family': 'Roboto, sans-serif'}), dash.no_update, True, dash.no_update

    return html.Div("Veuillez réaliser une annotation avant de valider", className='text-center', style={'font-family': 'Roboto, sans-serif'}), dash.no_update, False, dash.no_update


# Callback to enable/disable the validation button based on annotations
@callback(
    Output('bouton_valider', 'disabled'),
    Input('graph-styled-annotations', 'relayoutData'),
)
def activer_bouton(relayoutData):
    if relayoutData is not None and 'shapes' in relayoutData and relayoutData['shapes']:
        return False
    return True
