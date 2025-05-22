# ADR 003 – Stratégie de persistance

**STATUS**: Accepted

**CONTEXT**:  
Il faut assurer que chaque vente enregistrée reste cohérente.

**DECISION**:  
Utiliser SQLite avec commit explicite après chaque opération complète.

**CONSEQUENCES**:  
Pas de transaction partielle. Simplicité assurée, mais sans rollback complexe.

**COMPLIANCE**:  
Chaque écriture est confirmée par un `conn.commit()`.

**NOTES**:  
Rédigé par Nathan Lamy - 2025-05-21
