"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from entregasDeLosAlpes.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla ordenes e rutas
ordenes_rutas = db.Table(
    "ordenes_rutas",
    db.Model.metadata,
    db.Column("orden_id", db.String(40), db.ForeignKey("ordenes.id")),
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

ordenes_productos = db.Table(
    "ordenes_productos",
    db.Model.metadata,
    db.Column("orden_id", db.String(40), db.ForeignKey("ordenes.id")),
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


class Ordenes(db.Model):
    __tablename__ = "ordenes"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_cliente = db.Column(db.Integer, nullable=False)
    fecha_recepcion = db.Column(db.DateTime, nullable=False)
    productos = db.relationship('Producto', secondary=ordenes_productos, backref='ordenes')
    rutas = db.relationship('Ruta', secondary=ordenes_rutas, backref='ordenes')


class EventosOrden(db.Model):
    __tablename__ = "eventos_orden"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

class OrdenAnalitica(db.Model):
    __tablename__ = "analitica_ordenes"
    fecha_recepcion = db.Column(db.Date, primary_key=True)
    total = db.Column(db.Integer, primary_key=True, nullable=False)