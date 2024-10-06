```md
# Projet Dash - Application d'annotation d'images

## Description

Cette application Dash permet d'annoter et de vérifier des images de véhicules. Elle propose une interface utilisateur simple pour naviguer entre différentes pages : accueil, interface d'annotation, vérification, statistiques, et plus encore.

L'application est construite avec [Dash](https://plotly.com/dash/) et utilise [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) pour le style et la mise en page.

### Fonctionnalités :
- **Page d'accueil :** Présente une introduction à l'application.
- **Interface d'annotation :** Permet aux utilisateurs d'annoter des images.
- **Liste des annotations :** Affiche les annotations faites sur les images.
- **Statistiques :** Montre des statistiques basées sur les annotations.
- **Login et Déconnexion :** Gère la connexion et la déconnexion des utilisateurs.

## Prérequis

Avant d'exécuter l'application, assurez-vous d'avoir installé les dépendances requises.

### Installation des dépendances

1. **Python** : Vous devez avoir Python installé sur votre machine. [Télécharger Python](https://www.python.org/downloads/).

2. **Installer les dépendances** :
   Exécutez la commande suivante dans le terminal pour installer toutes les bibliothèques Python nécessaires :

   ```bash
   pip install -r requirements.txt
   ```

### Exécution de l'application

Pour démarrer l'application, exécutez la commande suivante dans le terminal :

```bash
python app.py
```

L'application sera accessible via votre navigateur à l'adresse suivante : `http://127.0.0.1:8050`.

## Structure du projet

```
Projet_Dash/
├── app.py              # Fichier principal de l'application
├── data/               # Dossier contenant les images et les données JSON
├── pages/              # Dossier contenant les différentes pages de l'application
├── requirements.txt    # Liste des dépendances Python
└── README.md           # Documentation de l'application
```

### Contribution

N'hésitez pas à forker ce projet et à contribuer en créant des pull requests pour toute amélioration ou correction de bug.

### Licence

Ce projet est sous licence [MIT](LICENSE).
```