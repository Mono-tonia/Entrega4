"""DTOs para la capa de infrastructura del dominio de bodegas

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from entregasDeLosAlpes.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla bodegas y stock
bodegas_stock = db.Table(
    "bodegas_stock",
    db.Model.metadata,
    db.Column("bodega_id", db.String(40), db.ForeignKey("bodegas.id")),
    db.Column("producto_codigo", db.String(10)),
    db.ForeignKeyConstraint(
        ["producto_codigo"]
    )
)

class Stock(db.Model):
    __tablename__ = "stock"
    producto_codigo = db.Column(db.String(10), nullable=False, primary_key=True)


class Bodegas(db.Model):
    __tablename__ = "bodegas"
    id = db.Column(db.String(40), primary_key=True, nullable=False)
    nombre = db.Column(db.String(10), nullable=False)
    ubicacion = db.Column(db.String(10), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)

    Stock = db.relationship('Stock', secondary=bodegas_stock, backref='bodegas')


almacenamiento_listaBodega = db.Table(
    "almacenamiento_listaBodega",
    db.Model.metadata,
    db.Column("id", db.String(40), db.ForeignKey("almacenamiento.id")),
    db.Column("id_cliente", db.String(40), db.ForeignKey("almacenamiento.id_cliente")),
    db.Column("bodega_id", db.String(40), db.ForeignKey("bodegas.id")),
    db.ForeignKeyConstraint(
        ["bodega_id"]
    )
)

class ListaBodegas(db.Model):
    __tablename__ = "listaBodegas"
    bodega_id = db.Column(db.String(40), nullable=False, primary_key=True)



class Almacenamiento(db.Model):
    __tablename__ = "almacenamiento"
    id = db.Column(db.String(40), primary_key=True, nullable=False)
    id_cliente = db.Column(db.String(40), nullable=False)

    ListaBodegas = db.relationship('ListaBodegas', secondary=almacenamiento_listaBodega, backref='almacenamiento')


class EventosAlmacenamiento(db.Model):
    __tablename__ = "eventos_alamacenamiento"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)


class AlmacenamientoAnalitica(db.Model):
    __tablename__ = "analitica_almacenamiento"
    fecha_recepcion = db.Column(db.Date, primary_key=True)
    total = db.Column(db.Integer, primary_key=True, nullable=False)