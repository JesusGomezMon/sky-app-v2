"""Microservicio 4: Respaldo y Recuperación."""
import json
import shutil
from datetime import datetime
from pathlib import Path

from sky_app.infraestructura.repositorio import CLIENTES_DIR, BACKUPS_DIR


class Respaldos:
    def __init__(self):
        BACKUPS_DIR.mkdir(exist_ok=True)

    def generar_respaldo(self) -> dict:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = BACKUPS_DIR / f"backup_{timestamp}"
        destino.mkdir()
        archivos = list(CLIENTES_DIR.glob("cliente_*.json"))
        for archivo in archivos:
            shutil.copy2(archivo, destino / archivo.name)
        return {
            "mensaje": "Respaldo generado",
            "backup_id": f"backup_{timestamp}",
            "archivos": len(archivos),
        }

    def listar_respaldos(self) -> dict:
        backups = sorted(BACKUPS_DIR.glob("backup_*"), reverse=True)
        return {
            "respaldos": [
                {
                    "id": b.name,
                    "archivos": len(list(b.glob("*.json"))),
                }
                for b in backups
            ]
        }

    def restaurar(self, backup_id: str) -> dict:
        origen = BACKUPS_DIR / backup_id
        if not origen.exists():
            return {"error": f"Respaldo '{backup_id}' no encontrado"}
        for archivo in origen.glob("*.json"):
            shutil.copy2(archivo, CLIENTES_DIR / archivo.name)
        return {"mensaje": f"Restaurado desde {backup_id}"}
