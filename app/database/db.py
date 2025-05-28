from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

DATABASE_URL = "postgresql+psycopg2://magasin_user:secret@10.194.32.204:5432/magasin"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

produits_vendus_table = Table(
    'produits_vendus',
    Base.metadata,
    Column('vente_id', Integer, ForeignKey('ventes.id')),
    Column('produit_id', Integer, ForeignKey('produits.id'))
)

class Produit(Base):
    __tablename__ = 'produits'
    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    categorie = Column(String, nullable=False)

class Vente(Base):
    __tablename__ = 'ventes'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    total = Column(Integer, nullable=False)
    produits = relationship("Produit", secondary=produits_vendus_table)

def initialiser_db():
    Base.metadata.create_all(engine)
    session = Session()
    if session.query(Produit).count() == 0:
        session.add_all([
            Produit(nom="Pommes", categorie="Fruits"),
            Produit(nom="Bananes", categorie="Fruits"),
            Produit(nom="Savon", categorie="Hygiène")
        ])
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
    return [{"id": p.id, "nom": p.nom, "categorie": p.categorie} for p in produits]

def get_stock():
    return chercher_produits()

def enregistrer_vente(produits_ids):
    session = Session()
    produits = session.query(Produit).filter(Produit.id.in_(produits_ids)).all()
    vente = Vente(date=datetime.now(), total=len(produits), produits=produits)
    session.add(vente)
    session.commit()
    vente_id = vente.id
    session.close()
    return vente_id

def annuler_vente(vente_id):
    session = Session()
    vente = session.query(Vente).filter_by(id=vente_id).first()
    if vente:
        session.delete(vente)
        session.commit()
    session.close()

def get_ventes():
    session = Session()
    ventes = session.query(Vente).all()
    resultats = []
    for v in ventes:
        resultats.append({
            "id": v.id,
            "date": v.date.isoformat(),
            "total": v.total,
            "produits": [p.nom for p in v.produits]
        })
    session.close()
    return resultats
