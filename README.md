# Système de Caisse Multi-Magasins (Application Web)

## Description

Ce projet est une application de gestion de caisse et de stocks répartis sur plusieurs magasins, avec une interface web. Il permet :

- La recherche de produits  
- L'enregistrement de ventes  
- L'annulation de ventes  
- La consultation du stock  
- L'affichage des ventes  
- La génération d’un rapport consolidé des ventes (UC1)  
- La consultation du stock central et demandes de réapprovisionnement (UC2)  
- La visualisation des performances globales (tableau de bord) (UC3)  
- Mise à jour des produits depuis la maison mère (UC4)  
- Approvisionnement depuis le centre logistique (UC6)

---

## Instructions d'exécution

### 1. Lancer la base de données (à faire une seule fois)  
```bash
docker-compose -f docker-compose.db.yml up -d
```

### 2. Démarrer l’interface Web (depuis un client magasin ou gestionnaire)  
```bash
./run-client-web.sh [ID_MAGASIN]
# Exemple :
./run-client-web.sh 1
```

---

## Exécution des tests

```bash
docker-compose run tests
```

---

## Utilisation

Une fois l’application lancée, ouvrez http://localhost:5000 dans votre navigateur.  
Les fonctionnalités sont accessibles via des boutons clairs :  
- Rechercher un produit  
- Consulter le stock  
- Enregistrer une vente  
- Annuler une vente  
- Afficher les ventes  
- Accéder au tableau de bord et rapport (UC1, UC2, UC3)

---

## Choix technologiques

| Élément                  | Choix                        | Justification                                                               |
|--------------------------|------------------------------|----------------------------------------------------------------------------|
| Langage de programmation | Python 3                     | Simple, maintenu, rapide à développer                                      |
| Framework Web            | Flask                        | Léger, efficace pour une interface web rapide                             |
| Base de données          | PostgreSQL                   | Robuste, relationnelle, supporte plusieurs clients                         |
| ORM                      | SQLAlchemy                   | Abstraction des requêtes SQL, portabilité                                 |
| Conteneurisation         | Docker + Docker Compose      | Déploiement isolé, réutilisable, facile à lancer                          |
| Architecture             | Web + BD centralisée         | Permet la synchronisation des données entre plusieurs magasins            |

---

## Structure du projet

```
LOG430-LABO-2/
├── app/
│   ├── database/
│   │   └── db.py
│   └── services/
│       └── gestion_magasin.py
├── web/
│   ├── app.py
│   ├── templates/
│       └── *.html
│
├── tests/
│   └── test_fonctionnel.py
├── docker-compose.yml
├── docker-compose.db.yml
├── run-client.sh
├── Dockerfile
├── requirements.txt
└── docs/
    ├── UML/
    └── ADR/
```

---

## Auteur

Projet développé par **Nathan Lamy** – ÉTS, ÉTÉ 2025 - LOG430-01