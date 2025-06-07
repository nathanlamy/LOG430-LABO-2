from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Float, func, extract
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, joinedload
from datetime import datetime
import os

DB_USER = os.getenv("DB_USER", "magasin_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "magasin")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Magasin(Base):
    __tablename__ = 'magasins'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    quartier = Column(String, nullable=False)

class Produit(Base):
    __tablename__ = 'produits'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    categorie = Column(String, nullable=False)
    prix = Column(Float, nullable=False)
    description = Column(String)

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey('produits.id'))
    magasin_id = Column(Integer, ForeignKey('magasins.id'))
    quantite = Column(Integer, nullable=False)
    seuil_critique = Column(Integer, nullable=False)
    produit = relationship("Produit")
    magasin = relationship("Magasin")

class Vente(Base):
    __tablename__ = 'ventes'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    magasin_id = Column(Integer, ForeignKey('magasins.id'))
    magasin = relationship("Magasin")
    lignes = relationship("LigneVente", back_populates="vente")

class LigneVente(Base):
    __tablename__ = 'lignes_vente'
    id = Column(Integer, primary_key=True)
    vente_id = Column(Integer, ForeignKey('ventes.id'))
    produit_id = Column(Integer, ForeignKey('produits.id'))
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)
    vente = relationship("Vente", back_populates="lignes")
    produit = relationship("Produit")

class StockCentral(Base):
    __tablename__ = 'stock_central'
    id = Column(Integer, primary_key=True)
    produit_id = Column(Integer, ForeignKey('produits.id'))
    quantite = Column(Integer, nullable=False)
    seuil_critique = Column(Integer, nullable=False)
    produit = relationship("Produit")


def initialiser_db():
    print("in inti")
    Base.metadata.create_all(engine)
    session = Session()

    if session.query(Produit).count() == 0:
        print("in inti1")
        produits = [
            Produit(nom="Pommes", categorie="Fruits", prix=0.99, description="Pomme rouge juteuse"),
            Produit(nom="Savon", categorie="Hygiène", prix=2.50, description="Savon doux pour les mains"),
            Produit(nom="Lait", categorie="Épicerie", prix=1.99, description="Lait 2% 1L"),
        ]
        session.add_all(produits)

    if session.query(Magasin).count() == 0:
        magasins = [
            Magasin(nom="Magasin Centre", quartier="Downtown"),
            Magasin(nom="Magasin Nord", quartier="Nord"),
            Magasin(nom="Magasin Sud", quartier="Sud"),
            Magasin(nom="Magasin Est", quartier="Est"),
            Magasin(nom="Magasin Ouest", quartier="Ouest"),
        ]
        session.add_all(magasins)
        session.commit()

        # Affecter du stock initial pour chaque magasin
        produits = session.query(Produit).all()
        magasins = session.query(Magasin).all()
        stock_items = []
        for magasin in magasins:
            for produit in produits:
                stock_items.append(Stock(magasin_id=magasin.id, produit_id=produit.id, quantite=50, seuil_critique=10))
        session.add_all(stock_items)
    
    if session.query(StockCentral).count() == 0:
        produits = session.query(Produit).all()
        stock_central = [StockCentral(produit_id=p.id, quantite=200, seuil_critique=30) for p in produits]
        session.add_all(stock_central)


    session.commit()
    session.close()


def chercher_produits(identifiant=None, nom=None, categorie=None):
    session = Session()
    query = session.query(Produit)
    if identifiant:
        produits = query.filter_by(id=identifiant).all()
    elif nom:
        produits = query.filter(Produit.nom.ilike(f"%{nom}%")).all()
    elif categorie:
        produits = query.filter(Produit.categorie.ilike(f"%{categorie}%")).all()
    else:
        produits = query.all()
    session.close()
    return [{"id": p.id, "nom": p.nom, "categorie": p.categorie, "prix": p.prix, "description": p.description} for p in produits]

def get_stock(magasin_id):
    session = Session()
    stocks = session.query(Stock).filter_by(magasin_id=magasin_id).all()
    result = []
    for stock in stocks:
        result.append({
            "produit_id": stock.produit_id,
            "nom": stock.produit.nom,
            "quantite": stock.quantite,
            "seuil_critique": stock.seuil_critique
        })
    session.close()
    return result

def enregistrer_vente(magasin_id, ligne_ventes):
    session = Session()
    total = 0.0
    lignes = []

    for ligne in ligne_ventes:
        produit = session.query(Produit).filter_by(id=ligne["produit_id"]).first()
        if produit:
            quantite = ligne["quantite"]
            prix_unitaire = produit.prix
            total += quantite * prix_unitaire
            ligne_vente = LigneVente(
                produit_id=produit.id,
                quantite=quantite,
                prix_unitaire=prix_unitaire
            )
            lignes.append(ligne_vente)

            # Update stock
            stock = session.query(Stock).filter_by(produit_id=produit.id, magasin_id=magasin_id).first()
            if stock:
                stock.quantite -= quantite

    vente = Vente(date=datetime.now(), total=round(total, 2), magasin_id=magasin_id, lignes=lignes)
    session.add(vente)
    session.commit()
    vente_id = vente.id
    session.close()
    return vente_id

def annuler_vente(vente_id):
    session = Session()
    vente = session.query(Vente).filter_by(id=vente_id).first()
    if vente:
        for ligne in vente.lignes:
            stock = session.query(Stock).filter_by(produit_id=ligne.produit_id, magasin_id=vente.magasin_id).first()
            if stock:
                stock.quantite += ligne.quantite
        session.delete(vente)
        session.commit()
    session.close()

def get_ventes(magasin_id=None):
    session = Session()
    query = session.query(Vente)
    if magasin_id:
        query = query.filter_by(magasin_id=magasin_id)
    ventes = query.all()
    resultats = []
    for v in ventes:
        resultats.append({
            "id": v.id,
            "date": v.date.isoformat(),
            "total": v.total,
            "magasin": v.magasin.nom if v.magasin else None,
            "produits": [
                {
                    "nom": l.produit.nom,
                    "quantite": l.quantite,
                    "prix_unitaire": l.prix_unitaire
                } for l in v.lignes
            ]
        })
    session.close()
    return resultats

def generer_rapport_consolide():
    session = Session()

    ventes_par_magasin = (
        session.query(Magasin.nom, func.sum(Vente.total))
        .join(Vente)
        .group_by(Magasin.nom)
        .all()
    )

    produits_les_plus_vendus = (
        session.query(Produit.nom, func.sum(LigneVente.quantite))
        .join(LigneVente)
        .group_by(Produit.nom)
        .order_by(func.sum(LigneVente.quantite).desc())
        .all()
    )

    session.close()
    return ventes_par_magasin, produits_les_plus_vendus

def consulter_stock_central():
    session = Session()
    stocks = session.query(StockCentral).options(joinedload(StockCentral.produit)).all()
    session.close()
    return stocks

def reapprovisionner_magasin(magasin_id, produit_id, quantite):
    session = Session()
    central = session.query(StockCentral).filter_by(produit_id=produit_id).first()
    if not central or central.quantite < quantite:
        session.close()
        return False

    # Réduire le stock central
    central.quantite -= quantite

    # Ajouter au stock magasin
    stock = session.query(Stock).filter_by(magasin_id=magasin_id, produit_id=produit_id).first()
    if stock:
        stock.quantite += quantite
    else:
        stock = Stock(magasin_id=magasin_id, produit_id=produit_id, quantite=quantite, seuil_critique=10)
        session.add(stock)

    session.commit()
    session.close()
    return True

def get_tableau_de_bord():
    session = Session()

    # 1. Chiffre d'affaires par magasin
    chiffre_affaires = (
        session.query(Magasin.nom, func.sum(Vente.total))
        .join(Vente)
        .group_by(Magasin.nom)
        .all()
    )

    # 2. Produits en rupture de stock
    ruptures = (
        session.query(Magasin.nom, Produit.nom, Stock.quantite, Stock.seuil_critique)
        .join(Stock.produit)
        .join(Stock.magasin)
        .filter(Stock.quantite < Stock.seuil_critique)
        .all()
    )

    # 3. Produits en surstock
    surstock = (
        session.query(Magasin.nom, Produit.nom, Stock.quantite, Stock.seuil_critique)
        .join(Stock.produit)
        .join(Stock.magasin)
        .filter(Stock.quantite > (Stock.seuil_critique + 100))
        .all()
    )

    # 4. Tendances hebdomadaires
    tendances = (
        session.query(
            extract('week', Vente.date).label('semaine'),
            func.sum(Vente.total)
        )
        .group_by('semaine')
        .order_by('semaine')
        .all()
    )

    session.close()
    return {
        "chiffre_affaires": chiffre_affaires,
        "ruptures": ruptures,
        "surstock": surstock,
        "tendances": tendances
    }
