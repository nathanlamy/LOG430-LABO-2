# ADR 003 – Stratégie de persistance

**STATUS**: Accepted

**CONTEXT**:  
Le système doit garantir la cohérence des données lors des ventes, même avec plusieurs clients accédant à la base en simultané.

**DECISION**:  
Utiliser PostgreSQL comme système de gestion de base de données, avec SQLAlchemy pour la gestion des transactions. Les opérations critiques (ventes, suppressions) sont encapsulées dans une session explicite.

**CONSEQUENCES**:  
Les transactions sont automatiquement gérées par SQLAlchemy avec `session.commit()` et `session.rollback()` en cas d'erreur. Cela offre robustesse et extensibilité sans complexité manuelle.

**COMPLIANCE**:  
Chaque opération d’écriture ou suppression passe par une session SQLAlchemy commitée manuellement.


**NOTES**:  
Modifié par Nathan Lamy - 2025-05-27
