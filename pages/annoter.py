import dash
from dash import dcc, html, Input, Output, callback, State
from skimage import io
import plotly_express as px
import os, json, random, base64, uuid
import dash_bootstrap_components as dbc

# Dossier images et fichiers JSON
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

def charger_image():
    chemin_image = recup_img_aleatoire()
    if chemin_image:
        return io.imread(chemin_image)
    return None

def save_img(content, filename):
    data = content.split(",")[1]
    img_data = base64.b64decode(data)
    filepath = os.path.join(dossier_img, filename)
    with open(filepath, 'wb') as f:
        f.write(img_data)
    return filepath

def get_user_data():
    with open(users_file, 'r') as f:
        users = json.load(f)
    return users

def load_annotations(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def save_annotations(file_path, new_annotation):
    # Charger les annotations existantes
    annotations = load_annotations(file_path)
    annotations.append(new_annotation)

    # Sauvegarder les annotations mises à jour
    with open(file_path, 'w') as f:
        json.dump(annotations, f, indent=4)
        print(f"Annotations sauvegardées : {annotations}")  # Log pour débogage

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
        html.H3("Interface d'annotation"),
        dcc.Graph(id="graph-styled-annotations", figure=fig),

        dcc.Upload(
            id="import-image",
            children=html.Div(
                ['Glissez et déposez une image ici, ou ',
                 html.A('sélectionnez une image')],
                style={
                    'borderWidth': '0.5px', 'borderStyle': 'solid', 'backgroundColor':'rgba(66, 66, 66, 0.15)',
                    'padding': '20px', 'textAlign': 'center', 'width': '50%',
                    'margin': '5px auto', 'cursor': 'pointer'
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

        dbc.Button(
            "Valider l'annotation",
            id="bouton_valider",
            color='success',
            n_clicks=0,
            className='my-3'
        ),

        dbc.Button(
            "Modifier l'annotation",
            id="bouton_reset",
            color='danger',
            n_clicks=0,
            className='my-3'
        ),

        dcc.Store(id='user-name-store')  # Pour stocker le nom d'utilisateur en cours sur la session
    ]
)

# Callback pour le modal
@callback(
    Output('modal', 'is_open'),
    Output('graph-styled-annotations', 'figure', allow_duplicate=True),
    [Input('import-image', 'contents'),
     Input('fermer_modal', 'n_clicks'),
     Input('confirmer_modal', 'n_clicks')],
    [State('graph-styled-annotations', 'figure'),
     State('import-image', 'filename'),
     State('modal', 'is_open')],
    prevent_initial_call=True
)
def activer_modal(contenu_img, cancel_clicks, confirm_clicks, is_open, filename, current_fig):
    if contenu_img is not None and is_open is False:
        return True, current_fig
    
    if cancel_clicks:
        return False, current_fig
    
    if confirm_clicks:
        save_img(contenu_img, filename)
        img = io.imread(os.path.join(dossier_img, filename))
        fig = px.imshow(img)
        fig.update_layout(
            dragmode="drawrect",
            newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="black", width=2)),
        )
        return False, fig
    
    return is_open, current_fig

# Callback liée au bouton Valider l'annotation
@callback(
    Output('graph-styled-annotations', 'figure'), 
    Output('user-name-store', 'data', allow_duplicate=True), 
    Input('bouton_valider', 'n_clicks'), 
    State('graph-styled-annotations', 'relayoutData'), 
    State('import-image', 'filename'), 
    State('user-name-store', 'data'), 
    prevent_initial_call=True 
)
def valider_annotation(n_clicks, relayout_data, filename, user_name):
    if n_clicks:
        if user_name:
            annotation_id = str(uuid.uuid4())
            annotation_data = {
                'id': annotation_id,
                'annotateur_nom': user_name,
                'nom_image': filename,
                'details_annotations': relayout_data
            }

            # Appeler la fonction pour sauvegarder l'annotation
            save_annotations(annotations_file, annotation_data)

            print(f"Relayout data: {relayout_data}")  # Log pour débogage

            # Vérifier si l'annotation a bien été sauvegardée
            with open(annotations_file, 'r') as f:
                saved_annotations = json.load(f)
                print(f"Annotations actuelles : {saved_annotations}")  # Log pour débogage

        return dash.no_update

    return dash.no_update
