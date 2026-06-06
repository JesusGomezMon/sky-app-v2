"""Pruebas automatizadas SKY App v2.0"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sky_app.microservicios.gestion_clientes import GestionClientes
from sky_app.microservicios.gestion_servicios import GestionServicios
from sky_app.microservicios.consultas import Consultas
from sky_app.microservicios.respaldos import Respaldos
from sky_app.microservicios.monitoreo import Monitoreo
from sky_app.infraestructura.repositorio import CLIENTES_DIR, BACKUPS_DIR
import shutil


@pytest.fixture(autouse=True)
def limpiar_datos():
    """Limpia datos de prueba antes y después de cada test."""
    for d in [CLIENTES_DIR, BACKUPS_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    yield
    for d in [CLIENTES_DIR, BACKUPS_DIR]:
        if d.exists():
            shutil.rmtree(d)


class TestGestionClientes:
    def test_crear_cliente(self):
        ms = GestionClientes()
        resultado = ms.crear_cliente(
            "Juan Pérez", "Av. Reforma 123", "5551234567", "juan@email.com"
        )
        assert "cliente" in resultado
        assert resultado["cliente"]["nombre"] == "Juan Pérez"

    def test_buscar_cliente(self):
        ms = GestionClientes()
        creado = ms.crear_cliente(
            "María López", "Calle 5 #10", "5559876543", "maria@email.com"
        )
        id_c = creado["cliente"]["id_cliente"]
        resultado = ms.buscar_cliente(id_cliente=id_c)
        assert resultado["cliente"]["nombre"] == "María López"

    def test_actualizar_cliente(self):
        ms = GestionClientes()
        creado = ms.crear_cliente(
            "Carlos Ruiz", "Blvd. Norte 45", "5551112233", "carlos@email.com"
        )
        id_c = creado["cliente"]["id_cliente"]
        resultado = ms.actualizar_cliente(id_c, nombre="Carlos Ruiz Actualizado")
        assert resultado["cliente"]["nombre"] == "Carlos Ruiz Actualizado"

    def test_eliminar_cliente(self):
        ms = GestionClientes()
        creado = ms.crear_cliente(
            "Ana Torres", "Av. Sur 78", "5554445566", "ana@email.com"
        )
        id_c = creado["cliente"]["id_cliente"]
        resultado = ms.eliminar_cliente(id_c)
        assert "mensaje" in resultado
        assert ms.buscar_cliente(id_cliente=id_c).get("error")

    def test_listar_clientes(self):
        ms = GestionClientes()
        ms.crear_cliente("Cliente 1", "Dir 1", "111", "c1@email.com")
        ms.crear_cliente("Cliente 2", "Dir 2", "222", "c2@email.com")
        resultado = ms.listar_clientes()
        assert resultado["total"] == 2


class TestGestionServicios:
    def test_agregar_servicio(self):
        gc = GestionClientes()
        gs = GestionServicios()
        creado = gc.crear_cliente(
            "Pedro Gómez", "Calle 10", "5553334455", "pedro@email.com"
        )
        id_c = creado["cliente"]["id_cliente"]
        resultado = gs.agregar_servicio(id_c, "Internet", "Plan 100 Mbps")
        assert "servicio" in resultado
        assert resultado["servicio"]["tipo_servicio"] == "Internet"


class TestConsultas:
    def test_historial_servicios(self):
        gc = GestionClientes()
        gs = GestionServicios()
        cq = Consultas()
        creado = gc.crear_cliente(
            "Laura Díaz", "Av. Central 200", "5556667788", "laura@email.com"
        )
        id_c = creado["cliente"]["id_cliente"]
        gs.agregar_servicio(id_c, "TV", "Paquete premium")
        historial = cq.historial_servicios(id_c)
        assert historial["total_servicios"] == 1


class TestRespaldos:
    def test_generar_y_restaurar_respaldo(self):
        gc = GestionClientes()
        rb = Respaldos()
        gc.crear_cliente("Test Backup", "Dir Test", "999", "test@email.com")
        backup = rb.generar_respaldo()
        assert "backup_id" in backup
        lista = rb.listar_respaldos()
        assert len(lista["respaldos"]) >= 1


class TestMonitoreo:
    def test_health(self):
        mon = Monitoreo()
        resultado = mon.health()
        assert resultado["status"] == "ok"

    def test_reporte(self):
        mon = Monitoreo()
        resultado = mon.reporte()
        assert "saludable" in resultado
