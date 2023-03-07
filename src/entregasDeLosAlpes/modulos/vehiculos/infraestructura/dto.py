"""DTOs para la capa de infrastructura del dominio de vehiculos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vehiculos

"""

from entregasDeLosAlpes.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla transportes e itinerarios
transportes_rutas = db.Table(
    "transportes_rutas",
    db.Model.metadata,
    db.Column("transporte_id", db.String(40), db.ForeignKey("transportes.id")),
    db.Column("fecha_salida", db.DateTime),
    db.Column("fecha_llegada", db.DateTime),
    db.Column("origen_codigo", db.String(10)),
    db.Column("destino_codigo", db.String(10)),
    db.ForeignKeyConstraint(
        ["fecha_salida", "fecha_llegada", "origen_codigo", "destino_codigo"],
        ["rutas.fecha_salida", "rutas.fecha_llegada", "rutas.origen_codigo", "rutas.destino_codigo"]
    )
)

class Rutas(db.Model):
    __tablename__ = "rutas"
    fecha_salida = db.Column(db.DateTime, nullable=False, primary_key=True)
    fecha_llegada = db.Column(db.DateTime, nullable=False, primary_key=True)
    origen_codigo = db.Column(db.String(10), nullable=False, primary_key=True)
    destino_codigo= db.Column(db.String(10), nullable=False, primary_key=True)


transportes_productos = db.Table(
    "transportes_productos",
    db.Model.metadata,
    db.Column("transporte_id", db.String(40), db.ForeignKey("transportes.id")),
    db.Column("codigo", db.String(10)),
    db.ForeignKeyConstraint(
        ["codigo"],
        ["productos.codigo"]
    )
)

class Productos(db.Model):
    __tablename__ = "productos"
    codigo = db.Column(db.String(10), nullable=False, primary_key=True)
    nombre = db.Column(db.String(10), nullable=False)
    categoria = db.Column(db.String(10), nullable=False)


class Transportes(db.Model):
    __tablename__ = "transportes"
    id = db.Column(db.String(40), primary_key=True)
    id_cliente = db.Column(db.String(40), nullable=False)
    id_bodega = db.Column(db.String(40), nullable=False)
    fecha_recepcion = db.Column(db.DateTime, nullable=False)
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    productos = db.relationship('Producto', secondary=transportes_productos, backref='transportes')
    rutas = db.relationship('Ruta', secondary=transportes_rutas, backref='transportes')

class EventosTransporte(db.Model):
    __tablename__ = "eventos_transporte"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

class TransporteAnalitica(db.Model):
    __tablename__ = "analitica_transportes"
    fecha_recepcion = db.Column(db.Date, primary_key=True)
    total = db.Column(db.Integer, primary_key=True, nullable=False)