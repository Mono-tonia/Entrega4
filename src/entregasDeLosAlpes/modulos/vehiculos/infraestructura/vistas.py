from entregasDeLosAlpes.seedwork.infraestructura.vistas import Vista
from entregasDeLosAlpes.modulos.vehiculos.dominio.entidades import Transporte
from entregasDeLosAlpes.config.db import db
from .dto import Transportes as TransporteDTO

class VistaTransporte(Vista):
    def obtener_por(id=None, estado=None, id_cliente=None, id_bodega=None, **kwargs) -> [Transporte]:
        params = dict()

        if id:
            params['id'] = str(id)
        
        if estado:
            params['estado'] = str(estado)
        
        if id_cliente:
            params['id_cliente'] = str(id_cliente)

        if id_bodega:
            params['id_bodega'] = str(id_bodega)
            
        # TODO Convierta TransporteDTO a Transporte y valide que la consulta es correcta
        return db.session.query(TransporteDTO).filter_by(**params)
