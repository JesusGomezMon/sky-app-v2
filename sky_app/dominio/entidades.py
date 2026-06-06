"""Entidades del dominio SKY."""
from dataclasses import dataclass, field
from typing import List, Optional
import uuid

from .value_objects import (
    NombreCliente,
    Direccion,
    TipoServicio,
    FechaRegistro,
    TipoServicioEnum,
)


@dataclass
class Servicio:
    id_servicio: str
    tipo_servicio: str
    fecha_contratacion: str
    descripcion: str

    @classmethod
    def agregar_servicio(
        cls, tipo: TipoServicio, descripcion: str = ""
    ) -> "Servicio":
        return cls(
            id_servicio=str(uuid.uuid4())[:8],
            tipo_servicio=tipo.valor.value,
            fecha_contratacion=FechaRegistro.ahora().formato(),
            descripcion=descripcion or f"Servicio de {tipo.valor.value}",
        )

    def actualizar_servicio(self, descripcion: str) -> None:
        self.descripcion = descripcion


@dataclass
class Cliente:
    """Agregado raíz: Cliente controla sus servicios."""

    id_cliente: str
    nombre: str
    direccion: str
    telefono: str
    correo: str
    tipo_cliente: str
    fecha_registro: str
    servicios: List[Servicio] = field(default_factory=list)

    @classmethod
    def crear_cliente(
        cls,
        nombre: NombreCliente,
        direccion: Direccion,
        telefono: str,
        correo: str,
        tipo_cliente: str = "residencial",
    ) -> "Cliente":
        return cls(
            id_cliente=str(uuid.uuid4())[:8],
            nombre=nombre.valor,
            direccion=direccion.valor,
            telefono=telefono,
            correo=correo,
            tipo_cliente=tipo_cliente,
            fecha_registro=FechaRegistro.ahora().formato(),
        )

    def agregar_servicio(self, servicio: Servicio) -> None:
        self.servicios.append(servicio)

    def to_dict(self) -> dict:
        return {
            "id_cliente": self.id_cliente,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "correo": self.correo,
            "tipo_cliente": self.tipo_cliente,
            "fecha_registro": self.fecha_registro,
            "servicios": [
                {
                    "id_servicio": s.id_servicio,
                    "tipo_servicio": s.tipo_servicio,
                    "fecha_contratacion": s.fecha_contratacion,
                    "descripcion": s.descripcion,
                }
                for s in self.servicios
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Cliente":
        servicios = [
            Servicio(
                id_servicio=s["id_servicio"],
                tipo_servicio=s["tipo_servicio"],
                fecha_contratacion=s["fecha_contratacion"],
                descripcion=s["descripcion"],
            )
            for s in data.get("servicios", [])
        ]
        return cls(
            id_cliente=data["id_cliente"],
            nombre=data["nombre"],
            direccion=data["direccion"],
            telefono=data["telefono"],
            correo=data["correo"],
            tipo_cliente=data["tipo_cliente"],
            fecha_registro=data["fecha_registro"],
            servicios=servicios,
        )


@dataclass
class Ejecutivo:
    id_ejecutivo: str
    nombre: str
    area: str

    @classmethod
    def crear(cls, nombre: str, area: str) -> "Ejecutivo":
        return cls(
            id_ejecutivo=str(uuid.uuid4())[:8],
            nombre=nombre,
            area=area,
        )
