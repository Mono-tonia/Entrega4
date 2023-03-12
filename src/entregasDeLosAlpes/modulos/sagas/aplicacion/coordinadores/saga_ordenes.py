from entregasDeLosAlpes.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from entregasDeLosAlpes.seedwork.aplicacion.comandos import Comando
from entregasDeLosAlpes.seedwork.dominio.eventos import EventoDominio

from entregasDeLosAlpes.modulos.sagas.aplicacion.comandos.cliente import RegistrarUsuario, ValidarUsuario
from entregasDeLosAlpes.modulos.sagas.aplicacion.comandos.vehiculos import PagarReserva, RevertirPago
from entregasDeLosAlpes.modulos.sagas.aplicacion.comandos.bodegas import ConfirmarReserva, RevertirConfirmacion
from entregasDeLosAlpes.modulos.productos.aplicacion.comandos.recibir_orden import RecibirOrden
from entregasDeLosAlpes.modulos.bodegas.aplicacion.comandos.crear_almacenamiento import CrearAlmacenamiento
from entregasDeLosAlpes.modulos.productos.dominio.eventos import OrdenProcesada, OrdenRecibida
from entregasDeLosAlpes.modulos.sagas.dominio.eventos.vehiculos import ProductoEntregado, ProductoDevuelto
from entregasDeLosAlpes.modulos.bodegas.dominio.eventos import BuscarAlmacenamiento
from entregasDeLosAlpes.modulos.vehiculos.dominio.eventos import ProductoEntregado, ProductoRecibido
from entregasDeLosAlpes.modulos.vehiculos.aplicacion.comandos.recibir_producto import RecibirProducto


class CoordinadorOrdenes(CoordinadorOrquestacion):


    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=RecibirOrden, evento=OrdenRecibida, 
                        #error=OrdenRecibidaFallida, 
                        #compensacion=CancelarOrden
                        ),
            Transaccion(index=2, comando=BuscarAlmacenamiento, evento=BuscarAlmacenamiento, 
                        #error=AlmacenamientoNoEncontrado, 
                        #compensacion=AlmacenamientoNoEncontrado
                        ),
            Transaccion(index=3, comando=RecibirProducto, evento=ProductoRecibido, 
                        #error=AlmacenamientoNoCreado, 
                        #compensacion=AlmacenamientoNoCreado
                        ),
            Fin(index=4)
        ]
                                                                                
    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])
    
    def terminar():
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        #Persistir estado en DB
        # Probablemente usted podría usar un repositorio para ello
        ...

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        #Transforma un evento en la entrada de un comando
        ...


# TODO Agregue un Listener/Handler para que se puedan redireccionar eventos de dominio
def oir_mensaje(mensaje):
    if isinstance(mensaje, EventoDominio):
        coordinador = CoordinadorOrdenes()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")
