"""Menú interactivo para demostración local."""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sky_app.microservicios.gestion_clientes import GestionClientes
from sky_app.microservicios.gestion_servicios import GestionServicios
from sky_app.microservicios.consultas import Consultas
from sky_app.microservicios.respaldos import Respaldos
from sky_app.microservicios.monitoreo import Monitoreo


def menu():
    gc = GestionClientes()
    gs = GestionServicios()
    cq = Consultas()
    rb = Respaldos()
    mon = Monitoreo()

    while True:
        print("\n=== SKY App v2.0 - Menú ===")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente")
        print("4. Modificar cliente")
        print("5. Eliminar cliente")
        print("6. Agregar servicio")
        print("7. Consultar historial")
        print("8. Generar respaldo")
        print("9. Estado del sistema")
        print("0. Salir")
        op = input("\nOpción: ").strip()

        if op == "1":
            nombre = input("Nombre: ")
            direccion = input("Dirección: ")
            telefono = input("Teléfono: ")
            correo = input("Correo: ")
            r = gc.crear_cliente(nombre, direccion, telefono, correo)
            print(json.dumps(r, indent=2, ensure_ascii=False))
        elif op == "2":
            print(json.dumps(gc.listar_clientes(), indent=2, ensure_ascii=False))
        elif op == "3":
            id_c = input("ID cliente: ")
            print(json.dumps(gc.buscar_cliente(id_cliente=id_c), indent=2, ensure_ascii=False))
        elif op == "4":
            id_c = input("ID cliente: ")
            campo = input("Campo (nombre/direccion/telefono/correo): ")
            valor = input("Nuevo valor: ")
            print(json.dumps(gc.actualizar_cliente(id_c, **{campo: valor}), indent=2, ensure_ascii=False))
        elif op == "5":
            id_c = input("ID cliente: ")
            print(json.dumps(gc.eliminar_cliente(id_c), indent=2, ensure_ascii=False))
        elif op == "6":
            id_c = input("ID cliente: ")
            tipo = input("Tipo (Internet/Telefonía/TV): ")
            desc = input("Descripción: ")
            print(json.dumps(gs.agregar_servicio(id_c, tipo, desc), indent=2, ensure_ascii=False))
        elif op == "7":
            id_c = input("ID cliente: ")
            print(json.dumps(cq.historial_servicios(id_c), indent=2, ensure_ascii=False))
        elif op == "8":
            print(json.dumps(rb.generar_respaldo(), indent=2, ensure_ascii=False))
        elif op == "9":
            print(json.dumps(mon.reporte(), indent=2, ensure_ascii=False))
        elif op == "0":
            break


if __name__ == "__main__":
    menu()
