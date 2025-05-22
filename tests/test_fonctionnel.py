import pytest
from app.database.db import (
    initialiser_db,
    enregistrer_vente,
    chercher_produits,
    annuler_vente,
    get_ventes,
    get_stock
)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    initialiser_db()

def test_recherche_produit():
    resultats = chercher_produits(nom="Pomme")
    assert any("Pomme" in p["nom"] for p in resultats)

def test_consulter_stock():
    stock = get_stock()
    assert isinstance(stock, list)
    assert len(stock) > 0

def test_enregistrer_vente():
    produits = chercher_produits(nom="Pomme")
    assert produits, "Produit 'Pomme' non trouvé"
    vente_id = enregistrer_vente([produits[0]["id"]])
    ventes = get_ventes()
    assert any(v["id"] == vente_id for v in ventes)

def test_annuler_vente():
    produits = chercher_produits(nom="Bananes")
    assert produits, "Produit 'Bananes' non trouvé"
    vente_id = enregistrer_vente([produits[0]["id"]])
    annuler_vente(vente_id)
    ventes = get_ventes()
    assert all(v["id"] != vente_id for v in ventes)
