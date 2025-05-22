# ADR 002 – Séparation des responsabilités

**STATUS**: Accepted

**CONTEXT**:  
La logique du projet devenait difficile à maintenir dans un seul fichier.

**DECISION**:  
Adopter une structure en 3 couches : presentation/, services/, database/.

**CONSEQUENCES**:  
Chaque couche a son rôle : affichage, logique métier, persistance. Le code est plus clair.

**COMPLIANCE**:  
Chaque fonctionnalité passe par ces trois modules distincts.

**NOTES**:  
Rédigé par Nathan Lamy - 2025-05-21
