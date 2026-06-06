"""Microservicio 2: Gestión de Servicios."""
from sky_app.dominio.entidades import Servicio
from sky_app.dominio.value_objects import TipoServicio
from sky_app.infraestructura.repositorio import RepositorioClientes


class GestionServicios:
    def __init__(self):
        self.repo = RepositorioClientes()

    def agregar_servicio(
        self, id_cliente: str, tipo_servicio: str, descripcion: str = ""
    ) -> dict:
        cliente = self.repo.buscar(id_cliente)
        if not cliente:
            return {"error": "Cliente no encontrado"}
        servicio = Servicio.agregar_servicio(
            TipoServicio.desde_texto(tipo_servicio), descripcion
        )
        cliente.agregar_servicio(servicio)
        self.repo.guardar(cliente)
        return {
            "mensaje": "Servicio agregado",
            "servicio": {
                "id_servicio": servicio.id_servicio,
                "tipo_servicio": servicio.tipo_servicio,
                "fecha_contratacion": servicio.fecha_contratacion,
                "descripcion": servicio.descripcion,
            },
        }

    def actualizar_servicio(
        self, id_cliente: str, id_servicio: str, descripcion: str
    ) -> dict:
        cliente = self.repo.buscar(id_cliente)
        if not cliente:
            return {"error": "Cliente no encontrado"}
        for servicio in cliente.servicios:
            if servicio.id_servicio == id_servicio:
                servicio.actualizar_servicio(descripcion)
                self.repo.guardar(cliente)
                return {"mensaje": "Servicio actualizado", "cliente": cliente.to_dict()}
        return {"error": "Servicio no encontrado"}
