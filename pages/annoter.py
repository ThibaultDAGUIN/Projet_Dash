import dash
from dash import dcc, html, Input, Output, callback, State
from skimage import io
import plotly_express as px
import os, json, random, base64
import dash_bootstrap_components as dbc
from datetime import datetime

dossier_img = './data/cars/'
users_file = './data/users.json'
annotations_file = './data/annotations.json'

def recup_img_aleatoire():
    files = os.listdir(dossier_img)
    images = [file for file in files if file.endswith(('png', 'jpg', 'jpeg'))]
    if images:
        random_image = random.choice(images)
        return os.path.join(dossier_img, random_image)
    return None

nom_image = None

def charger_image():
    chemin_image = recup_img_aleatoire()
    if chemin_image:
        global nom_image  # Utilisez la variable globale pour stocker le nom de l'image
        nom_image = os.path.basename(chemin_image)  # Récupérer uniquement le nom du fichier
        return io.imread(chemin_image)
    return None

def save_img(content, filename):
    data = content.split(",")[1]
    img_data = base64.b64decode(data)
    file_unique = f"{filename}"
    filepath = os.path.join(dossier_img, file_unique)
    with open(filepath, 'wb') as f:
        f.write(img_data)
    return filepath

dash.register_page(__name__)

img = charger_image()

if img is not None:
    fig = px.imshow(img)
    fig.update_layout(
        dragmode="drawrect",
        newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
    )
else:
    fig = None

layout = html.Div(
    [
        html.H3("Interface d'annotation", className='text-center my-3'),
        dcc.Graph(id="graph-styled-annotations", figure=fig),
        dbc.Row(
            [
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
                    ),
                    width='auto'
                ),
            ],
            justify='center',
            className='d-flex my-3',
            style={'alignItems': 'center'}
        ),
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
                        "Annuler l'annotation",
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
        dcc.Store(id='user_name_store', storage_type='local'), # Pour stocker le nom d'utilisateur en cours sur la session
    ]
)

@callback(
    Output('modal', 'is_open'), # Ouvrir ou fermer le modal
    Output('graph-styled-annotations', 'figure', allow_duplicate=True), # Mettre à jour l'image affichée
    Input('import-image', 'contents'),
    Input('fermer_modal', 'n_clicks'),
    Input('confirmer_modal', 'n_clicks'),
    State('modal', 'is_open'),
    State('import-image', 'filename'),
    State('graph-styled-annotations', 'figure'),
    prevent_initial_call=True
)

def activer_modal(contenu_img, cancel_clicks, confirm_clicks, is_open, filename, current_fig):
    # Ouvrir le modal lorsque l'image est importée
    if contenu_img is not None and is_open is False:
        return True, current_fig
    
    # Si "Non" est cliqué, fermer le modal sans rien faire
    if cancel_clicks:
        return False, current_fig
    
    # Si "Oui" est cliqué, sauvegarder l'image
    if confirm_clicks:
        save_img(contenu_img, filename)
        
        # Charger l'image sauvegardée pour l'afficher
        img = io.imread(os.path.join(dossier_img, filename))
        fig = px.imshow(img)
        fig.update_layout(
            dragmode="drawrect",
            newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
        )
        return False, fig
    
    # Si aucune action n'a été prise, ne rien changer
    return is_open, current_fig

@callback(
    Output('annotation_data', 'children'),
    Output('graph-styled-annotations', 'figure'),
    Output('bouton_valider', 'disabled', allow_duplicate=True),
    Input("bouton_valider", "n_clicks"),
    State('graph-styled-annotations', 'relayoutData'),
    State('user_name_store', 'data'),
    State('marque_vehicule', 'value'),
    State('couleur_vehicule', 'value'),
    prevent_initial_call='initial_duplicate'
)

def afficher_annotation(n_clicks, relayoutData, user_name, marque, couleur):
    if n_clicks is None and user_name :
        return dash.no_update, dash.no_update, True
        # Vérifier si des annotations existent
    if relayoutData is not None and 'shapes' in relayoutData and relayoutData['shapes']:
        try :

            # Charger les annotations précédentes
            annotations_data = []
            if os.path.exists(annotations_file):
                with open(annotations_file, 'r') as f:
                    annotations_data = json.load(f)

            filtre_shapes = []
            for shape in relayoutData['shapes']:
                filtered_shape = {
                    'type': shape.get('type'),
                    'x0': shape.get('x0'),
                    'y0': shape.get('y0'),
                    'x1': shape.get('x1'),
                    'y1': shape.get('y1'),
                    'line': {
                        'color': shape['line'].get('color'),
                        'width': shape['line'].get('width'),
                        'dash': shape['line'].get('dash')
                    },
                    'fillcolor': shape.get('fillcolor'),
                    'opacity': shape.get('opacity'),
                }
                filtre_shapes.append(filtered_shape)

            # Modifier le fichier json annotation avec le nom de l'annotateur
            new_annotation = {
                'id': len(annotations_data) + 1,
                'nom_image': nom_image,
                'annotateur': user_name,
                'date_annotation': datetime.now().strftime('%Y-%m-%d'),
                'reviewer': '',
                'date_review': '',
                'marque': marque,
                'couleur': couleur,
                'annotations': filtre_shapes
            }

            # Ajouter les nouvelles annotations
            annotations_data.append(new_annotation)

            # Sauvegarder les annotations dans un fichier JSON
            with open(annotations_file, 'w') as f:
                json.dump(annotations_data, f, indent=2)

            # Message de confirmation
            message = f"L'annotation réalisée par {user_name} sur l'image {nom_image} a bien été enregistrée."
            
            # Passer à l'image suivante
            img = charger_image()
            if img is not None:
                fig = px.imshow(img)
                fig.update_layout(
                    dragmode="drawrect",
                    newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
                )
            else:
                fig = None

            return html.Div(message, className='text-center', style={'font-family': 'Roboto, sans-serif'}), fig, True
    
        except Exception as e:
            # Message d'erreur si une exception est levée
            return html.Div("L'annotation a échoué, veuillez réessayer.", style={'font-family': 'Roboto, sans-serif'}), dash.no_update, True

    return html.Div("Veuillez réaliser une annotation avant de valider", className='text-center', style={'font-family': 'Roboto, sans-serif'}), dash.no_update, False

@callback(
    Output('bouton_valider', 'disabled'),
    Input('graph-styled-annotations', 'relayoutData'),
)

def activer_bouton(relayoutData):
    if relayoutData is not None and 'shapes' in relayoutData and relayoutData['shapes']:
        return False
    return True

@callback(
    Output('graph-styled-annotations', 'figure', allow_duplicate=True),
    Input('bouton_reset', 'n_clicks'),
    State('graph-styled-annotations', 'relayoutData'),
    prevent_initial_call=True
)

def reset_annotation(n_clicks, relayoutData):
    if n_clicks > 0:
        # Si des annotations existent, les supprimer
        if relayoutData is not None and 'shapes' in relayoutData:
            relayoutData['shapes'] = [] 

        # Recréer la figure sans annotations
        img = io.imread(os.path.join(dossier_img, nom_image))  # Recharger l'image actuelle
        fig = px.imshow(img)
        fig.update_layout(
            dragmode="drawrect",
            newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
            shapes=relayoutData.get('shapes', []),
        )
        return fig
    return dash.no_update

@callback(
    Output('bouton_reset', 'disabled'),
    Input('graph-styled-annotations', 'relayoutData'),
)

def activer_bouton(relayoutData):
    if relayoutData is not None and 'shapes' in relayoutData and relayoutData['shapes']:
        return False
    return True