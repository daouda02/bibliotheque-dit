# Bibliothèque Numérique DIT — Système de Recommandation

Projet d'examen Outils de Versioning — Master 2 IA — DIT Dakar

## Stack technique
- **Backend** : Django REST Framework (Livres, Utilisateurs, Emprunts) + FastAPI (Recommandation)
- **Base de données** : PostgreSQL (partagée, une DB par service)
- **Frontend** : HTML/CSS/JS + AJAX
- **Conteneurisation** : Docker + Docker Compose (profils dev/prod)
- **Versioning données/modèle** : DVC (remote Google Drive)

## Lancement rapide

```bash
# 1. Copier et remplir les variables
cp .env.example .env
# Éditer .env avec vos vraies valeurs

# 2. Mode développement (hot-reload)
docker compose --profile dev up --build

# 3. Mode production
docker compose --profile prod up --build -d
```

## Services et ports

| Service         | Port  | URL                             |
|-----------------|-------|---------------------------------|
| Frontend        | 80    | http://localhost                |
| Livres          | 8001  | http://localhost:8001/api/livres/      |
| Utilisateurs    | 8002  | http://localhost:8002/api/utilisateurs/|
| Emprunts        | 8003  | http://localhost:8003/api/emprunts/    |
| Recommandation  | 8004  | http://localhost:8004/recommendations/1|
| PostgreSQL      | 5432  | (interne Docker)                |

## Endpoints principaux

### Livres (port 8001)
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /api/livres/ | Lister tous les livres |
| POST | /api/livres/ | Ajouter un livre |
| GET | /api/livres/<id>/ | Détail d'un livre |
| PUT/PATCH | /api/livres/<id>/ | Modifier un livre |
| DELETE | /api/livres/<id>/ | Supprimer un livre |
| GET | /api/livres/recherche/?q=python | Recherche |
| GET/POST | /api/livres/<id>/disponibilite/ | Disponibilité |

### Utilisateurs (port 8002)
| Méthode | URL | Description |
|---------|-----|-------------|
| GET/POST | /api/utilisateurs/ | Liste / Créer |
| GET/PUT/DELETE | /api/utilisateurs/<id>/ | Détail |
| GET | /api/utilisateurs/recherche/?q=... | Recherche |
| GET | /api/utilisateurs/<id>/profil/ | Profil complet |
| PATCH | /api/utilisateurs/<id>/activation/ | Activer/Désactiver |

### Emprunts (port 8003)
| Méthode | URL | Description |
|---------|-----|-------------|
| GET/POST | /api/emprunts/ | Liste / Créer emprunt |
| GET | /api/emprunts/<id>/ | Détail emprunt |
| POST | /api/emprunts/<id>/retour/ | Retourner un livre |
| GET | /api/emprunts/utilisateur/<id>/ | Historique utilisateur |
| GET | /api/emprunts/retards/ | Emprunts en retard |
| GET | /api/emprunts/export/ | Export CSV (pour DVC) |

### Recommandation (port 8004)
| Méthode | URL | Description |
|---------|-----|-------------|
| GET | /recommendations/<user_id> | Recommandations |
| POST | /train | Ré-entraîner le modèle |
| GET | /model/info | Infos sur le modèle |

## DVC — Pipeline ML

```bash
# Initialiser DVC
dvc init
dvc remote add -d gdrive gdrive://<VOTRE_DOSSIER_ID>

# Exporter les données depuis le service Emprunts
curl http://localhost:8003/api/emprunts/export/ -o dvc/data/loans.csv

# Ajouter et versionner
dvc add dvc/data/loans.csv

# Lancer le pipeline complet
dvc repro

# Voir les métriques
dvc metrics show

# Comparer deux versions
dvc metrics diff HEAD~1
```

## Workflow Git utilisé

```
main          ← code stable (production)
  └── develop ← intégration continue
        ├── feature/service-livres
        ├── feature/service-utilisateurs
        ├── feature/service-emprunts
        ├── feature/service-recommandation
        ├── feature/frontend
        ├── feature/docker
        └── feature/dvc
```
