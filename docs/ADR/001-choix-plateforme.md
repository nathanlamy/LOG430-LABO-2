# ADR 001 – Choix de la plateforme

**STATUS**: Accepted

**CONTEXT**:  
Initialement, le projet devait être simple, rapide à exécuter et portable, dans une VM Ubuntu. Une interface console avait été choisie pour sa légèreté.

**DECISION**:  
Migrer vers une application web légère en Python avec Flask. Cela permet une meilleure accessibilité et évolutivité pour les utilisateurs (employés et gestionnaires).

**CONSEQUENCES**:  
L’application devient accessible via un navigateur web. Elle reste légère grâce à Flask, tout en offrant une expérience utilisateur améliorée par rapport à la console. Cela permet aussi une intégration plus facile des futurs cas d’utilisation (rapports, tableaux de bord...).

**COMPLIANCE**:  
Le système est désormais basé sur Flask et HTML minimal, conteneurisé via Docker pour assurer la portabilité.

**NOTES**:  
Mise à jour par Nathan Lamy – 2025-06-06


