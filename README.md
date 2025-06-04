# Système de Caisse (Application Console)

## Description

Ce projet est une application console simple de type système de caisse, permettant :
- La recherche de produits  
- L'enregistrement de ventes  
- L'annulation de ventes  
- La consultation du stock  
- L'affichage des ventes  

L'application est structurée en 3 couches : interface console, logique service, et accès à une base de données PostgreSQL.

---

## Instructions d'exécution

### Pour commencer le serveur postgres persistant une seule fois avec Docker

    docker-compose -f docker-compose.db.yml up -d

---

## Exécution des tests avec Docker

Pour lancer les tests (présents dans le dossier `tests/`) :

    docker-compose run tests

---

## Exécution du client avec Docker

### 1. Construire l'image Docker

    docker build -t caisse .

### 2. Lancer le programme dans un conteneur

    docker run -it caisse

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

| Élément                  | Choix                        | Justification                                                                 |
|--------------------------|------------------------------|------------------------------------------------------------------------------|
| Langage de programmation | Python 3                     | Simple, portable, maintenu, et déjà installé sur Ubuntu                      |
| Interface utilisateur    | Console                      | Suffisante pour un prototype interactif, rapide à mettre en place            |
| Architecture             | 2-tiers                      | Séparation entre couche présentation (client) et couche persistance (DB)     |
| Base de données          | PostgreSQL                   | Moteur SQL robuste, open-source, adapté à plusieurs clients en simultané     |
| ORM                      | SQLAlchemy                   | Abstraction de la base et compatibilité multi-SGBD                           |
| Conteneurisation         | Docker + Docker Compose      | Permet une exécution portable et reproductible sur différentes machines      |

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
    ├── docker-compose.db.yml
    ├── README.md
    └── requirements.txt

---

## Auteur

Projet développé par Nathan Lamy – ÉTS, ÉTÉ 2025 - LOG430-01