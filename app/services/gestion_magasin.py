from database.db import chercher_produits, get_stock, enregistrer_vente, annuler_vente, get_ventes

def rechercher_produit():
    critere = input("Rechercher par (id / nom / categorie) : ").strip().lower()
    if critere == "id":
        val = input("Identifiant ? ")
        resultats = chercher_produits(identifiant=int(val))
    elif critere == "nom":
        val = input("Nom ? ")
        resultats = chercher_produits(nom=val)
    elif critere == "categorie":
        val = input("Catégorie ? ")
        resultats = chercher_produits(categorie=val)
    else:
        print("Critère invalide.")
        return
    for p in resultats:
        print(p)

def consulter_stock():
    produits = get_stock()
    for p in produits:
        print(p)

def enregistrer_vente_console():
    ids = input("IDs des produits vendus (séparés par des virgules) : ")
    try:
        id_list = [int(x.strip()) for x in ids.split(",")]
        vente_id = enregistrer_vente(id_list)
        print(f"Vente enregistrée avec ID : {vente_id}")
    except Exception as e:
        print("Erreur :", e)

def annuler_vente_console():
    vente_id = input("ID de la vente à annuler : ")
    try:
        annuler_vente(int(vente_id))
        print("Vente annulée.")
    except Exception as e:
        print("Erreur :", e)

def afficher_ventes_console():
    ventes = get_ventes()
    if not ventes:
        print("Aucune vente enregistrée.")
        return
    for v in ventes:
        produits_str = ", ".join(v["produits"])
        print(f"ID Vente: {v['id']} | Date: {v['date']} | Total: {v['total']} produit(s)")
        print(f"  Produits: {produits_str}")
