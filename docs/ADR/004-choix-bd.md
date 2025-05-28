# ADR 004 – Choix du mécanisme de base de données

**STATUS**: Accepted

**CONTEXT**:  
Plusieurs clients doivent accéder à une base centralisée.

**DECISION**:  
Utiliser PostgreSQL avec conteneur Docker.

**CONSEQUENCES**:  
Supporte la concurrence et les transactions.Nécessite un conteneur actif.

**COMPLIANCE**:  
Connexion via `DATABASE_URL` dans l’environnement.

**NOTES**:  
Modifié par Nathan Lamy - 2025-05-27
