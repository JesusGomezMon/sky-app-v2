"""Microservicio 5: Monitoreo."""
import os
import platform
from datetime import datetime
from pathlib import Path

from sky_app.infraestructura.repositorio import CLIENTES_DIR, BACKUPS_DIR


class Monitoreo:
    def estado_sistema(self) -> dict:
        clientes = list(CLIENTES_DIR.glob("cliente_*.json"))
        backups = list(BACKUPS_DIR.glob("backup_*"))
        return {
            "estado": "operativo",
            "timestamp": datetime.now().isoformat(),
            "clientes_registrados": len(clientes),
            "respaldos_disponibles": len(backups),
            "plataforma": platform.system(),
            "python": platform.python_version(),
        }

    def reporte(self) -> dict:
        estado = self.estado_sistema()
        errores = []
        if not CLIENTES_DIR.exists():
            errores.append("Directorio de clientes no existe")
        if len(clientes := list(CLIENTES_DIR.glob("cliente_*.json"))) == 0:
            errores.append("No hay clientes registrados (sistema vacío)")
        for archivo in clientes:
            try:
                import json
                with open(archivo, encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError:
                errores.append(f"Archivo corrupto: {archivo.name}")
        return {
            **estado,
            "errores_detectados": errores,
            "saludable": len(errores) == 0,
        }

    def health(self) -> dict:
        return {"status": "ok", "servicio": "SKY App v2.0"}
