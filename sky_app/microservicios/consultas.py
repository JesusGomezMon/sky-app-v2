"""Microservicio 3: Consulta de Información."""
from sky_app.infraestructura.repositorio import RepositorioClientes


class Consultas:
    def __init__(self):
        self.repo = RepositorioClientes()

    def consultar_cliente(self, id_cliente: str) -> dict:
        cliente = self.repo.buscar(id_cliente)
        if not cliente:
            return {"error": "Cliente no encontrado"}
        return {"cliente": cliente.to_dict()}

    def historial_servicios(self, id_cliente: str) -> dict:
        cliente = self.repo.buscar(id_cliente)
        if not cliente:
            return {"error": "Cliente no encontrado"}
        return {
            "id_cliente": id_cliente,
            "nombre": cliente.nombre,
            "historial": [
                {
                    "id_servicio": s.id_servicio,
                    "tipo_servicio": s.tipo_servicio,
                    "fecha_contratacion": s.fecha_contratacion,
                    "descripcion": s.descripcion,
                }
                for s in cliente.servicios
            ],
            "total_servicios": len(cliente.servicios),
        }

    def resumen_general(self) -> dict:
        clientes = self.repo.listar_todos()
        total_servicios = sum(len(c.servicios) for c in clientes)
        return {
            "total_clientes": len(clientes),
            "total_servicios": total_servicios,
            "clientes": [
                {
                    "id_cliente": c.id_cliente,
                    "nombre": c.nombre,
                    "servicios": len(c.servicios),
                }
                for c in clientes
            ],
        }
