"""Objetos de valor del dominio SKY."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re


class TipoServicioEnum(str, Enum):
    INTERNET = "Internet"
    TELEFONIA = "Telefonía"
    TV = "TV de paga"


@dataclass(frozen=True)
class NombreCliente:
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")


@dataclass(frozen=True)
class CorreoElectronico:
    valor: str

    def __post_init__(self):
        if not self.valor or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.valor.strip()):
            raise ValueError("Correo electronico invalido")


@dataclass(frozen=True)
class Direccion:
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor.strip()) < 5:
            raise ValueError("La dirección debe tener al menos 5 caracteres")


@dataclass(frozen=True)
class TipoServicio:
    valor: TipoServicioEnum

    @classmethod
    def desde_texto(cls, texto: str) -> "TipoServicio":
        mapa = {
            "internet": TipoServicioEnum.INTERNET,
            "telefonia": TipoServicioEnum.TELEFONIA,
            "telefonía": TipoServicioEnum.TELEFONIA,
            "tv": TipoServicioEnum.TV,
            "tv de paga": TipoServicioEnum.TV,
        }
        clave = texto.strip().lower()
        if clave not in mapa:
            raise ValueError(f"Tipo de servicio inválido: {texto}")
        return cls(valor=mapa[clave])


@dataclass(frozen=True)
class FechaRegistro:
    valor: datetime

    @classmethod
    def ahora(cls) -> "FechaRegistro":
        return cls(valor=datetime.now())

    def formato(self) -> str:
        return self.valor.strftime("%Y-%m-%d %H:%M:%S")
