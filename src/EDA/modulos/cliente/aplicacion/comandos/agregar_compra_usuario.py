from EDA.seedwork.aplicacion.comandos import Comando, ComandoHandler    

class AgregarCompraUsuario(Comando):
    id_usuario: uuid.UUID
    id_compra: uuid.UUID

class AgregarCompraUsuarioHandler(ComandoHandler):
    ...