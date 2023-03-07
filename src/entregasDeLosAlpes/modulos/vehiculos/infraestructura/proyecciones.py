from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.fabricas import FabricaRepositorio
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.repositorios import RepositorioTransportes
from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Transporte
from entregasDeLosAlpes.modulos.vehiculos.infraestructura.dto import Transporte as TransporteDTO

from entregasDeLosAlpes.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod
from .dto import TransporteAnalitica

class ProyeccionTransporte(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionTransportesTotales(ProyeccionTransporte):
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
        record = db.session.query(TransporteAnalitica).filter_by(fecha_recepcion=self.fecha_recepcion.date()).one_or_none()

        if record and self.operacion == self.ADD:
            record.total += 1
        elif record and self.operacion == self.DELETE:
            record.total -= 1 
            record.total = max(record.total, 0)
        else:
            db.session.add(TransporteAnalitica(fecha_recepcion=self.fecha_recepcion.date(), total=1))
        
        db.session.commit()

class ProyeccionTransportesLista(ProyeccionTransporte):
    def __init__(self, id_transporte, id_cliente, id_bodega, estado, fecha_recepcion, fecha_entrega):
        self.id_transporte = id
        self.id_cliente = id_cliente
        self.id_bodega = id_bodega
        self.estado = estado
        self.fecha_recepcion = millis_a_datetime(fecha_recepcion)
        self.fecha_entrega = millis_a_datetime(fecha_entrega)
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioTransportes)
        
        # TODO Haga los cambios necesarios para que se consideren los itinerarios, demás entidades y asociaciones
        repositorio.agregar(
            Transporte(
                id=str(self.id_transporte), 
                id_cliente=str(self.id_cliente), 
                id_bodega=str(self.id_bodega), 
                estado=str(self.estado), 
                fecha_recepcion=self.fecha_recepcion, 
                fecha_entrega=self.fecha_entrega))
        
        # TODO ¿Y si la transporte ya existe y debemos actualizarla? Complete el método para hacer merge

        # TODO ¿Tal vez podríamos reutilizar la Unidad de Trabajo?
        db.session.commit()

class ProyeccionTransporteHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionTransporte):

        # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
        # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
        # podriamos diseñar para alojar esta funcionalidad
        from entregasDeLosAlpes.config.db import db

        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionTransportesLista)
@proyeccion.register(ProyeccionTransportesTotales)
def ejecutar_proyeccion_transporte(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionTransporteHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    