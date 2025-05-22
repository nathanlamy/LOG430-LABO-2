import sqlite3
from datetime import datetime

DB_FILE = "magasin.db"

def get_connexion():
    return sqlite3.connect(DB_FILE)

def initialiser_db():
    conn = get_connexion()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        categorie TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        total INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produits_vendus (
        vente_id INTEGER,
        produit_id INTEGER,
        FOREIGN KEY(vente_id) REFERENCES ventes(id),
        FOREIGN KEY(produit_id) REFERENCES produits(id)
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM produits")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO produits (nom, categorie) VALUES (?, ?)", ("Pommes", "Fruits"))
        cursor.execute("INSERT INTO produits (nom, categorie) VALUES (?, ?)", ("Bananes", "Fruits"))
        cursor.execute("INSERT INTO produits (nom, categorie) VALUES (?, ?)", ("Savon", "Hygiène"))

    conn.commit()
    conn.close()

def chercher_produits(identifiant=None, nom=None, categorie=None):
    conn = get_connexion()
    cursor = conn.cursor()
    if identifiant:
        cursor.execute("SELECT * FROM produits WHERE id = ?", (identifiant,))
    elif nom:
        cursor.execute("SELECT * FROM produits WHERE nom LIKE ?", ('%' + nom + '%',))
    elif categorie:
        cursor.execute("SELECT * FROM produits WHERE categorie LIKE ?", ('%' + categorie + '%',))
    else:
        cursor.execute("SELECT * FROM produits")
    resultats = [{"id": row[0], "nom": row[1], "categorie": row[2]} for row in cursor.fetchall()]
    conn.close()
    return resultats

def get_stock():
    return chercher_produits()

def enregistrer_vente(produits_ids):
    conn = get_connexion()
    cursor = conn.cursor()
    total = len(produits_ids)
    date = datetime.now().isoformat()
    cursor.execute("INSERT INTO ventes (date, total) VALUES (?, ?)", (date, total))
    vente_id = cursor.lastrowid
    for pid in produits_ids:
        cursor.execute("INSERT INTO produits_vendus (vente_id, produit_id) VALUES (?, ?)", (vente_id, pid))
    conn.commit()
    conn.close()
    return vente_id

def annuler_vente(vente_id):
    conn = get_connexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produits_vendus WHERE vente_id = ?", (vente_id,))
    cursor.execute("DELETE FROM ventes WHERE id = ?", (vente_id,))
    conn.commit()
    conn.close()

def get_ventes():
    conn = get_connexion()
    cursor = conn.cursor()

    cursor.execute("SELECT id, date, total FROM ventes")
    ventes_brutes = cursor.fetchall()

    ventes = []
    for vente in ventes_brutes:
        vente_id, date, total = vente

        cursor.execute("""
            SELECT produits.nom
            FROM produits_vendus
            JOIN produits ON produits.id = produits_vendus.produit_id
            WHERE produits_vendus.vente_id = ?
        """, (vente_id,))
        produits = [row[0] for row in cursor.fetchall()]

        ventes.append({
            "id": vente_id,
            "date": date,
            "total": total,
            "produits": produits
        })

    conn.close()
    return ventes
