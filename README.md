# Feature Prioritizer

Un outil de priorisation de features basé sur un score impact/effort, avec recommandation IA.

Construit en 2-3h pour démontrer une capacité à livrer un produit fonctionnel end-to-end.

## Stack technique

- Python + Flask — API REST
- Anthropic API (Claude) — recommandation IA
- HTML / CSS / JS vanilla — interface web
- Postman — documentation API

## Lancer le projet

### 1. Cloner le repo

git clone https://gitlab.com/ton-pseudo/feature-prioritizer.git
cd feature-prioritizer

### 2. Installer les dépendances

python -m venv venv
source venv/bin/activate
pip install flask anthropic python-dotenv

### 3. Configurer la clé API

Créer un fichier .env à la racine :
ANTHROPIC_API_KEY=ta_clé_ici

### 4. Lancer le serveur

python app.py

Ouvrir http://127.0.0.1:5000 dans le navigateur.

## Endpoints API

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | /features | Récupère toutes les features triées par score |
| POST | /features | Ajoute une feature |
| DELETE | /features/:id | Supprime une feature |
| POST | /analyze | Génère une recommandation IA |

## Formule de score

score = impact / effort

| Impact | Effort | Quadrant |
|--------|--------|----------|
| ≥ 3 | ≤ 3 | Quick win |
| ≥ 3 | > 3 | Planifier |
| < 3 | ≤ 3 | Fill-in |
| < 3 | > 3 | À éviter |
