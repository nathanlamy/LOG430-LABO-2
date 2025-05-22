# Système de Caisse (Application Console)

## Description

Ce projet est une application console simple de type système de caisse, permettant :
- La recherche de produits  
- L'enregistrement de ventes  
- L'annulation de ventes  
- La consultation du stock  
- L'affichage des ventes  

L'application est structurée en 3 couches : interface console, logique service, et accès à une base de données SQLite.

---

## Instructions d'exécution

### En local

    docker-compose run caisse
    ou
    python3 app/main.py

---

## Tests

Actuellement, les tests peuvent être écrits à l’aide de `pytest`.

Pour lancer les tests (présents dans le dossier `tests/`) :

    docker-compose run caisse pytest
    ou
    pytest

---

## Exécution avec Docker

### 1. Construire l'image Docker

    docker build -t caisse .

### 2. Lancer le programme dans un conteneur

    docker run -it caisse

---

## Compilation

Aucune compilation nécessaire. Le projet est entièrement en Python.

---

## Utilisation

Une fois l'application lancée, un menu interactif s'affiche :

    --- Menu Principal ---
    1. Rechercher un produit
    2. Consulter le stock
    3. Enregistrer une vente
    4. Annuler une vente
    5. Afficher les ventes
    0. Quitter

---

## Choix technologiques

| Élément                  | Choix                 | Justification                                                                 |
|--------------------------|-----------------------|--------------------------------------------------------------------------------|
| Langage de programmation | Python 3              | Simple, portable, déjà installé sur Ubuntu                                     |
| Interface                | Console               | Suffisante pour un prototype fonctionnel                       |
| Architecture             | 3 couches (MVC léger) | Séparation claire entre présentation, logique service et persistance           |
| Base de données          | SQLite                | SGBD léger, local, sans configuration serveur                                  |
| Stockage                 | Fichier `.db` local   | Permet de tester sans dépendances externes ni installation supplémentaire     |

---

## Structure du projet

    projet-caisse/
    ├── main.py
    ├── menu.py
    ├── services/
    │   └── gestion_magasin.py
    ├── database/
    │   └── db.py
    ├── docs/
    │   ├── UML/
    │   └── ADR/
    ├── tests/
    │   └── test_fonctionnel.py
    ├── magasin.db
    ├── Dockerfile
    ├── docker-compose.yml
    ├── README.md
    └── requirements.txt

---

## Auteur

Projet développé par Nathan Lamy – ÉTS, ÉTÉ 2025 - LOG430-01