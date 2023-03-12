from cliente.modulos.dominio.entidades import Usuario
from cliente.modulos.dominio.repositorios import RepositorioUsuarios

class RepositorioUsuariosSQLAlchemy(RepositorioUsuarios):

    def __init__(self):
        self._fabrica_productos: FabricaProductos = FabricaProductos()

    @property
    def fabrica_productos(self):
        return self._fabrica_productos

    def obtener_por_id(self, id: UUID) -> Orden:
        orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        return self.fabrica_productos.crear_objeto(orden_dto, MapeadorOrden())

    def obtener_todos(self) -> list[Orden]:
        # TODO
        raise NotImplementedError

    def agregar(self, orden: Orden):
        orden_dto = self.fabrica_productos.crear_objeto(orden, MapeadorOrden())

        db.session.add(orden_dto)

    def actualizar(self, orden: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        # TODO
        raise NotImplementedError