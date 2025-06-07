from flask import Flask, render_template, request, redirect
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

MAGASIN_ID = int(os.getenv("MAGASIN_ID", 1))  # défaut à 1 si non défini

from app.database.db import (
    chercher_produits,
    get_stock,
    enregistrer_vente,
    annuler_vente,
    get_ventes,
    generer_rapport_consolide,
    consulter_stock_central,
    reapprovisionner_magasin,
    get_tableau_de_bord
)

app = Flask(__name__)

@app.route("/")
def menu_principal():
    return render_template("menu.html", magasin_id=MAGASIN_ID)

@app.route("/produits")
def produits():
    critere = request.args.get("critere")
    valeur = request.args.get("valeur")
    if critere == "id":
        resultats = chercher_produits(identifiant=int(valeur))
    elif critere == "nom":
        resultats = chercher_produits(nom=valeur)
    elif critere == "categorie":
        resultats = chercher_produits(categorie=valeur)
    else:
        resultats = []
    return render_template("produits.html", produits=resultats)

@app.route("/stock")
def stock():
    produits = get_stock(magasin_id=MAGASIN_ID)
    return render_template("stock.html", produits=produits)

@app.route("/ventes", methods=["GET", "POST"])
def ventes():
    if request.method == "POST":
        ids = request.form.get("ids")
        id_list = [{"produit_id": int(x.strip()), "quantite": 1} for x in ids.split(",")]
        enregistrer_vente(MAGASIN_ID, id_list)
        return redirect("/ventes")
    ventes = get_ventes(magasin_id=MAGASIN_ID)
    return render_template("ventes.html", ventes=ventes)


@app.route("/annuler_vente", methods=["POST"])
def annuler():
    vente_id = request.form.get("vente_id")
    try:
        annuler_vente(int(vente_id))
    except:
        pass
    return redirect("/ventes")

@app.route("/rapport")
def afficher_rapport():
    ventes_par_magasin, produits_les_plus_vendus = generer_rapport_consolide()
    return render_template("rapport.html",
                           ventes=ventes_par_magasin,
                           produits=produits_les_plus_vendus)

@app.route("/stock-central")
def stock_central():
    stocks = consulter_stock_central()
    return render_template("stock_central.html", stocks=stocks)

@app.route("/approvisionner/<int:produit_id>", methods=["POST"])
def approvisionner(produit_id):
    quantite = int(request.form["quantite"])
    success = reapprovisionner_magasin(MAGASIN_ID, produit_id, quantite)
    if not success:
        return "Stock insuffisant au centre", 400
    return redirect("/stock-central")

@app.route("/tableau-de-bord")
def tableau_de_bord():
    stats = get_tableau_de_bord()

    return render_template("dashboard.html", stats=stats)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
