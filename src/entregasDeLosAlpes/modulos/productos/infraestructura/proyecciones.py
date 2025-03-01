from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from entregasDeLosAlpes.modulos.productos.infraestructura.fabricas import FabricaRepositorio
from entregasDeLosAlpes.modulos.productos.infraestructura.repositorios import RepositorioOrdenes
from entregasDeLosAlpes.modulos.productos.dominio.entidades import Orden
from entregasDeLosAlpes.modulos.productos.infraestructura.dto import Ordenes as OrdenDTO

from entregasDeLosAlpes.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod
from .dto import OrdenAnalitica

class ProyeccionOrden(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionOrdenesTotales(ProyeccionOrden):
    ADD = 1
    DELETE = 2
    UPDATE = 3

    def __init__(self, fecha_recepcion, operacion):
        self.fecha_recepcion = millis_a_datetime(fecha_recepcion)
        self.operacion = operacion

    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        # NOTE esta no usa repositorios y de una vez aplica los cambios. Es decir, no todo siempre debe ser un repositorio
        record = db.session.query(OrdenAnalitica).filter_by(fecha_recepcion=self.fecha_recepcion.date()).one_or_none()

        if record and self.operacion == self.ADD:
            record.total += 1
        elif record and self.operacion == self.DELETE:
            record.total -= 1 
            record.total = max(record.total, 0)
        else:
            db.session.add(OrdenAnalitica(fecha_recepcion=self.fecha_recepcion.date(), total=1))
        
        db.session.commit()

class ProyeccionOrdenesLista(ProyeccionOrden):
    def __init__(self, id_orden, id_cliente, estado, fecha_recepcion, fecha_actualizacion):
        self.id_orden = id
        self.id_cliente = id_cliente
        self.estado = estado
        self.fecha_recepcion = millis_a_datetime(fecha_recepcion)
        self.fecha_actualizacion = millis_a_datetime(fecha_actualizacion)
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        
        # TODO Haga los cambios necesarios para que se consideren los itinerarios, demás entidades y asociaciones
        repositorio.agregar(
            Orden(
                id=str(self.id_orden), 
                id_cliente=str(self.id_cliente), 
                estado=str(self.estado), 
                fecha_recepcion=self.fecha_recepcion, 
                fecha_actualizacion=self.fecha_actualizacion))
        
        # TODO ¿Y si la orden ya existe y debemos actualizarla? Complete el método para hacer merge

        # TODO ¿Tal vez podríamos reutilizar la Unidad de Trabajo?
        db.session.commit()

class ProyeccionOrdenHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionOrden):

        # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
        # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
        # podriamos diseñar para alojar esta funcionalidad
        from entregasDeLosAlpes.config.db import db

        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionOrdenesLista)
@proyeccion.register(ProyeccionOrdenesTotales)
def ejecutar_proyeccion_orden(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionOrdenHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    