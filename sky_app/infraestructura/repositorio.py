"""Repositorio de persistencia en archivos JSON."""
import json
import os
from pathlib import Path
from typing import List, Optional

from sky_app.dominio.entidades import Cliente

BASE_DIR = Path(__file__).resolve().parent.parent
CLIENTES_DIR = BASE_DIR / "clientes"
BACKUPS_DIR = BASE_DIR / "backups"


def _asegurar_directorios():
    CLIENTES_DIR.mkdir(exist_ok=True)
    BACKUPS_DIR.mkdir(exist_ok=True)


def _ruta_cliente(id_cliente: str) -> Path:
    return CLIENTES_DIR / f"cliente_{id_cliente}.json"


class RepositorioClientes:
    def __init__(self):
        _asegurar_directorios()

    def guardar(self, cliente: Cliente) -> None:
        with open(_ruta_cliente(cliente.id_cliente), "w", encoding="utf-8") as f:
            json.dump(cliente.to_dict(), f, indent=2, ensure_ascii=False)

    def buscar(self, id_cliente: str) -> Optional[Cliente]:
        ruta = _ruta_cliente(id_cliente)
        if not ruta.exists():
            return None
        with open(ruta, encoding="utf-8") as f:
            return Cliente.from_dict(json.load(f))

    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        resultados = []
        for archivo in CLIENTES_DIR.glob("cliente_*.json"):
            with open(archivo, encoding="utf-8") as f:
                cliente = Cliente.from_dict(json.load(f))
                if nombre.lower() in cliente.nombre.lower():
                    resultados.append(cliente)
        return resultados

    def listar_todos(self) -> List[Cliente]:
        clientes = []
        for archivo in sorted(CLIENTES_DIR.glob("cliente_*.json")):
            with open(archivo, encoding="utf-8") as f:
                clientes.append(Cliente.from_dict(json.load(f)))
        return clientes

    def eliminar(self, id_cliente: str) -> bool:
        ruta = _ruta_cliente(id_cliente)
        if ruta.exists():
            ruta.unlink()
            return True
        return False

    def actualizar(self, cliente: Cliente) -> None:
        self.guardar(cliente)
