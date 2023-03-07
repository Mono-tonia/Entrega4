from entregasDeLosAlpes.seedwork.infraestructura.vistas import Vista
from entregasDeLosAlpes.modulos.bodegas.dominio.entidades import Almacenamiento
from entregasDeLosAlpes.config.db import db
from .dto import Almacenamiento as AlmacenamientoDTO

class VistaAlmacenamiento(Vista):
    def obtener_por(id=None, id_cliente=None,**kwargs) -> [Almacenamiento]:
        params = dict()

        if id:
            params['id'] = str(id)

        if id_cliente:
            params['id_cliente'] = str(id_cliente)        
            
        # TODO Convierta AlmacenamientoDTO a Almacenamiento y valide que la consulta es correcta
        return db.session.query(AlmacenamientoDTO).filter_by(**params)
