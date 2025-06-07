import pytest
from app.database.db import (
    initialiser_db,
    enregistrer_vente,
    chercher_produits,
    annuler_vente,
    get_ventes,
    get_stock
)

MAGASIN_ID = 1

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    initialiser_db()

def test_recherche_produit():
    resultats = chercher_produits(nom="Pomme")
    assert any("Pomme" in p["nom"] for p in resultats)

def test_consulter_stock():
    stock = get_stock(magasin_id=MAGASIN_ID)
    assert isinstance(stock, list)
    assert len(stock) > 0

def test_enregistrer_vente():
    produits = chercher_produits(nom="Lait")
    assert produits, "Produit 'Lait' non trouvé"

    vente_id = enregistrer_vente(
        magasin_id=MAGASIN_ID,
        ligne_ventes=[{"produit_id": produits[0]["id"], "quantite": 1}]
    )

    ventes = get_ventes(magasin_id=MAGASIN_ID)
    assert any(v["id"] == vente_id for v in ventes)

def test_annuler_vente():
    produits = chercher_produits(nom="Savon")
    assert produits, "Produit 'Savon' non trouvé"

    vente_id = enregistrer_vente(
        magasin_id=MAGASIN_ID,
        ligne_ventes=[{"produit_id": produits[0]["id"], "quantite": 1}]
    )

    annuler_vente(vente_id)
    ventes = get_ventes(magasin_id=MAGASIN_ID)
    assert all(v["id"] != vente_id for v in ventes)
