

import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Enum,
    ForeignKey,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


from sqlalchemy_schemadisplay import create_schema_graph

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, unique=True)
    pricing = Column(Float)
    weight  = Column(Float)
    color   = Column(String)

    shopping_carts = relationship('ShoppingCart', back_populates='product')


class Costumer(Base):
    __tablename__ = 'costumer'

    id         = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name  = Column(String)
    email      = Column(String, unique=True)
    address    = Column(String)

    shopping_carts = relationship('ShoppingCart', back_populates='costumer')


class BillStatus(enum.Enum):
    paid     = 'paid'
    pending  = 'pending'
    refunded = 'refunded'


class Bill(Base):
    __tablename__ = 'bill'

    id          = Column(Integer, primary_key=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Float)
    status      = Column(Enum(BillStatus))

    shopping_carts = relationship('ShoppingCart', back_populates='bill')


class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'

    product_id  = Column(Integer, ForeignKey('product.id'),  primary_key=True)
    costumer_id = Column(Integer, ForeignKey('costumer.id'), primary_key=True)
    bill_id     = Column(Integer, ForeignKey('bill.id'),     primary_key=True)
    quantity    = Column(Integer)
    price       = Column(Float)

    product  = relationship('Product',      back_populates='shopping_carts')
    costumer = relationship('Costumer',     back_populates='shopping_carts')
    bill     = relationship('Bill',         back_populates='shopping_carts')


if __name__ == '__main__':
    #  Genera un SQLite local con tus tablas
    engine = create_engine('sqlite:///db.sqlite')
    Base.metadata.create_all(engine)

    #  Dibuja el esquema estilo QuickDBDiagram
    graph = create_schema_graph(
        metadata=Base.metadata,
        show_datatypes=True,   
        show_indexes=False,    
        rankdir='LR'          
    )
    graph.write_png('diagram.png')
    print("✅ Diagrama generado en diagram.png")
