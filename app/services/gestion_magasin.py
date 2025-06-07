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
        print(f"[{p['id']}] {p['nom']} - {p['categorie']} (${p['prix']}) - {p['description']}")

def consulter_stock():
    magasin_id = int(input("ID du magasin : "))
    produits = get_stock(magasin_id)
    for p in produits:
        print(f"Produit ID: {p['produit_id']} | Nom: {p['nom']} | Quantité: {p['quantite']} | Seuil critique: {p['seuil_critique']}")

def enregistrer_vente_console():
    magasin_id = int(input("ID du magasin : "))
    lignes = []
    while True:
        produit_id = input("Produit ID (ou vide pour terminer) : ")
        if not produit_id.strip():
            break
        quantite = input("Quantité : ")
        try:
            lignes.append({
                "produit_id": int(produit_id),
                "quantite": int(quantite)
            })
        except ValueError:
            print("Entrée invalide. Réessayez.")
    if lignes:
        try:
            vente_id = enregistrer_vente(magasin_id, lignes)
            print(f"Vente enregistrée avec ID : {vente_id}")
        except Exception as e:
            print("Erreur lors de l'enregistrement :", e)
    else:
        print("Aucune vente enregistrée.")

def annuler_vente_console():
    vente_id = input("ID de la vente à annuler : ")
    try:
        annuler_vente(int(vente_id))
        print("Vente annulée.")
    except Exception as e:
        print("Erreur :", e)

def afficher_ventes_console():
    magasin_id_input = input("ID du magasin (laisser vide pour tous) : ")
    magasin_id = int(magasin_id_input) if magasin_id_input.strip() else None
    ventes = get_ventes(magasin_id=magasin_id)
    if not ventes:
        print("Aucune vente enregistrée.")
        return
    for v in ventes:
        print(f"ID Vente: {v['id']} | Date: {v['date']} | Total: ${v['total']:.2f} | Magasin: {v['magasin']}")
        for produit in v['produits']:
            print(f"  - {produit['nom']} x{produit['quantite']} @ ${produit['prix_unitaire']}")