# Cahier des Charges & Spécifications - Flag Quiz Application

Ce document regroupe l'ensemble des choix techniques, architecturaux et visuels validés pour le développement de l'application de quiz de drapeaux.

---

## 1. Vue d'ensemble du Projet

* **Concept** : Un jeu interactif d'apprentissage/test de connaissances sur les drapeaux du monde.
* **Type d'interaction** : Un drapeau est affiché, et l'utilisateur doit **saisir manuellement** le nom du pays dans un champ texte (pas de QCM).
* **Plateforme / Framework** : Python avec l'interface graphique **CustomTkinter** et la bibliothèque **Pillow** (PIL) pour la gestion d'images.

---

## 2. Fonctionnalités & UX Flow

1. **Saisie textuelle intelligente** :
   * Tolérance automatique sur la casse (majuscules/minuscules).
   * Suppression des espaces superflus.
   * Prise en compte de la suppression des accents (ex: "perou" pour "Pérou").
   * Support des alias pour les noms complexes (ex: "USA" ou "Etats-Unis" pour "États-Unis d'Amérique").
2. **Boucle de jeu** :
   * Affichage aléatoire des drapeaux.
   * Compteur de score et de série en cours (streak).
   * Feedback visuel immédiat lors de la validation (changement de couleur de la bordure ou du bouton).
   * Possibilité de passer une question avec affichage de la bonne réponse.

---

## 3. Architecture & Structure du Code

```text
flag_quiz/
├── assets/
│   └── flags/          # Cartes/images des drapeaux (.png ou .svg)
├── data/
│   └── countries.json  # Données des pays (noms, alias, codes ISO)
├── src/
│   ├── __init__.py
│   ├── logic.py        # Normalisation des chaînes et comparaison des réponses
│   └── app.py          # Interface graphique CustomTkinter
├── Structure.md
├── main.py             # Point d'entrée de l'application
└── requirements.txt    # Dépendances (customtkinter, pillow)
```

### Modèle de données (`data/countries.json`)

```json
[
  {
    "code": "fr",
    "name": "France",
    "aliases": ["Republique Francaise"],
    "flag": "assets/flags/fr.png"
  },
  {
    "code": "us",
    "name": "États-Unis",
    "aliases": ["USA", "Etats Unis", "Etats-Unis d'Amerique"],
    "flag": "assets/flags/us.png"
  }
]
```

---

## 4. Direction Artistique (DA) & Palette de Couleurs

L'interface adopte un style **pop, vibrant et dynamique** basé sur une palette de 5 couleurs spécifiques.

### Palette Validée

| Rôle dans l'UI | Nom | Code Hex | Description d'usage |
| :--- | :--- | :--- | :--- |
| **Fond / Structure** | Bleu Soft | `#788DFF` | Arrière-plan principal de la fenêtre et des cartes |
| **Action Principale** | Rose Pop | `#FA4DEA` | Boutons d'action principaux (Valider, Rejouer) |
| **Zone de Saisie** | Cyan Vif | `#00D8FC` | Bordures du champ texte au focus et icônes |
| **Succès / Victoire** | Vert Anis | `#9EE939` | Flash visuel de bonne réponse & affichage du score |
| **Alerte / Secondaire** | Orange Pêche | `#FAB14D` | Bouton "Passer", indices et feedback d'erreur |

### Configuration des constantes dans le code Python

```python
COLOR_BG = "#788DFF"           # Fond principal
COLOR_PRIMARY = "#FA4DEA"      # Bouton principal / Accentuation
COLOR_INPUT_BORDER = "#00D8FC" # Bordure du champ texte
COLOR_SUCCESS = "#9EE939"      # Bonne réponse
COLOR_WARNING = "#FAB14D"      # Bouton Passer / Mauvaise réponse
COLOR_TEXT = "#FFFFFF"         # Texte contrasté
```

---

## 5. Disposition de l'Interface Graphique (Layout)

```text
+---------------------------------------------------+
|  [ Score: 12/20 ]               [ Série: 🔥 5 ]   | <- Header
+---------------------------------------------------+
|                                                   |
|                +-----------------+                |
|                |                 |                |
|                |     DRAPEAU     |                | <- Carte d'affichage
|                |                 |                |    du drapeau
|                +-----------------+                |
|                                                   |
|             Entrez le nom du pays :               |
|                                                   |
|        [ Ex: Mexique...             ] [ Valider ] | <- Champ texte (#00D8FC)
|                                                   |    + Bouton Rose (#FA4DEA)
|               [  Passer cette question  ]         | <- Bouton Orange (#FAB14D)
+---------------------------------------------------+
```