"""Microservicio 1: Gestión de Clientes."""
from typing import List, Optional

from sky_app.dominio.entidades import Cliente
from sky_app.dominio.value_objects import NombreCliente, Direccion, CorreoElectronico
from sky_app.infraestructura.repositorio import RepositorioClientes


class GestionClientes:
    def __init__(self):
        self.repo = RepositorioClientes()

    def crear_cliente(
        self, nombre: str, direccion: str, telefono: str, correo: str, tipo_cliente: str = "residencial"
    ) -> dict:
        cliente = Cliente.crear_cliente(
            nombre=NombreCliente(nombre),
            direccion=Direccion(direccion),
            telefono=telefono,
            correo=CorreoElectronico(correo).valor,
            tipo_cliente=tipo_cliente,
        )
        self.repo.guardar(cliente)
        return {"mensaje": "Cliente registrado", "cliente": cliente.to_dict()}

    def buscar_cliente(self, id_cliente: str = None, nombre: str = None, correo: str = None) -> dict:
        if id_cliente:
            cliente = self.repo.buscar(id_cliente)
            if not cliente:
                return {"error": "Cliente no encontrado"}
            return {"cliente": cliente.to_dict()}
        if correo:
            cliente = self.repo.buscar_por_correo(correo)
            if not cliente:
                return {"error": "Cliente no encontrado"}
            return {"cliente": cliente.to_dict()}
        if nombre:
            clientes = self.repo.buscar_por_nombre(nombre)
            return {"clientes": [c.to_dict() for c in clientes], "total": len(clientes)}
        return {"error": "Proporcione id_cliente, nombre o correo"}

    def actualizar_cliente(self, id_cliente: str, **datos) -> dict:
        cliente = self.repo.buscar(id_cliente)
        if not cliente:
            return {"error": "Cliente no encontrado"}
        if "nombre" in datos:
            cliente.nombre = NombreCliente(datos["nombre"]).valor
        if "direccion" in datos:
            cliente.direccion = Direccion(datos["direccion"]).valor
        if "telefono" in datos:
            cliente.telefono = datos["telefono"]
        if "correo" in datos:
            cliente.correo = CorreoElectronico(datos["correo"]).valor
        if "tipo_cliente" in datos:
            cliente.tipo_cliente = datos["tipo_cliente"]
        self.repo.actualizar(cliente)
        return {"mensaje": "Cliente actualizado", "cliente": cliente.to_dict()}

    def eliminar_cliente(self, id_cliente: str) -> dict:
        if self.repo.eliminar(id_cliente):
            return {"mensaje": "Cliente eliminado"}
        return {"error": "Cliente no encontrado"}

    def listar_clientes(self) -> dict:
        clientes = self.repo.listar_todos()
        return {"clientes": [c.to_dict() for c in clientes], "total": len(clientes)}
