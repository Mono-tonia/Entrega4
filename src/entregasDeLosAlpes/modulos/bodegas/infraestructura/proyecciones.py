from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from entregasDeLosAlpes.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from entregasDeLosAlpes.modulos.bodegas.infraestructura.fabricas import FabricaRepositorio
from entregasDeLosAlpes.modulos.bodegas.infraestructura.repositorios import RepositorioAlmacenamiento
from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import Almacenamiento
from entregasDeLosAlpes.modulos.bodegas.infraestructura.dto import Almacenamiento as AlmacenamientoDTO

from entregasDeLosAlpes.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod
from .dto import AlmacenamientoAnalitica

class ProyeccionAlmacenamiento(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionAlmacenamientosTotales(ProyeccionAlmacenamiento):
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
        record = db.session.query(AlmacenamientoAnalitica).filter_by(fecha_recepcion=self.fecha_recepcion.date()).one_or_none()

        if record and self.operacion == self.ADD:
            record.total += 1
        elif record and self.operacion == self.DELETE:
            record.total -= 1 
            record.total = max(record.total, 0)
        else:
            db.session.add(AlmacenamientoAnalitica(fecha_recepcion=self.fecha_recepcion.date(), total=1))
        
        db.session.commit()

class ProyeccionAlmacenamientoLista(ProyeccionAlmacenamiento):
    def __init__(self, id_cliente, listaBod):
        self.id_cliente = id_cliente
        self.listaBod=listaBod

    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioAlmacenamiento)
        
        # TODO Haga los cambios necesarios para que se consideren los itinerarios, demás entidades y asociaciones
        repositorio.agregar(
            Almacenamiento(
                id_cliente=str(self.id_cliente),
                listaBod= self.listaBod))
        
        # TODO ¿Y si la orden ya existe y debemos actualizarla? Complete el método para hacer merge

        # TODO ¿Tal vez podríamos reutilizar la Unidad de Trabajo?
        db.session.commit()

class ProyeccionAlmacenamientoHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionAlmacenamiento):

        # TODO El evento de creación no viene con todos los datos de itinerarios, esto tal vez pueda ser una extensión
        # Asi mismo estamos dejando la funcionalidad de persistencia en el mismo método de recepción. Piense que componente
        # podriamos diseñar para alojar esta funcionalidad
        from entregasDeLosAlpes.config.db import db

        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionAlmacenamientoLista)
@proyeccion.register(ProyeccionAlmacenamientosTotales)
def ejecutar_proyeccion_orden(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionAlmacenamientoHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    