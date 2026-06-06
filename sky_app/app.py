"""API REST principal - SKY App v2.0"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify

from sky_app.microservicios.gestion_clientes import GestionClientes
from sky_app.microservicios.gestion_servicios import GestionServicios
from sky_app.microservicios.consultas import Consultas
from sky_app.microservicios.respaldos import Respaldos
from sky_app.microservicios.monitoreo import Monitoreo

app = Flask(__name__)

clientes_ms = GestionClientes()
servicios_ms = GestionServicios()
consultas_ms = Consultas()
respaldos_ms = Respaldos()
monitoreo_ms = Monitoreo()


@app.route("/")
def inicio():
    return jsonify({
        "aplicacion": "SKY App v2.0",
        "descripcion": "Gestión de clientes SKY - Microservicios DDD",
        "endpoints": {
            "clientes": "/api/clientes",
            "servicios": "/api/servicios",
            "consultas": "/api/consultas",
            "respaldos": "/api/respaldos",
            "monitoreo": "/api/monitoreo/health",
        },
    })


# --- Gestión de Clientes ---
@app.route("/api/clientes", methods=["GET"])
def listar_clientes():
    return jsonify(clientes_ms.listar_clientes())


@app.route("/api/clientes", methods=["POST"])
def crear_cliente():
    data = request.get_json(force=True)
    return jsonify(clientes_ms.crear_cliente(
        nombre=data["nombre"],
        direccion=data["direccion"],
        telefono=data["telefono"],
        correo=data["correo"],
        tipo_cliente=data.get("tipo_cliente", "residencial"),
    ))


@app.route("/api/clientes/<id_cliente>", methods=["GET"])
def buscar_cliente(id_cliente):
    return jsonify(clientes_ms.buscar_cliente(id_cliente=id_cliente))


@app.route("/api/clientes/<id_cliente>", methods=["PUT"])
def actualizar_cliente(id_cliente):
    data = request.get_json(force=True)
    return jsonify(clientes_ms.actualizar_cliente(id_cliente, **data))


@app.route("/api/clientes/<id_cliente>", methods=["DELETE"])
def eliminar_cliente(id_cliente):
    return jsonify(clientes_ms.eliminar_cliente(id_cliente))


@app.route("/api/clientes/buscar", methods=["GET"])
def buscar_por_nombre():
    nombre = request.args.get("nombre", "")
    return jsonify(clientes_ms.buscar_cliente(nombre=nombre))


# --- Gestión de Servicios ---
@app.route("/api/servicios", methods=["POST"])
def agregar_servicio():
    data = request.get_json(force=True)
    return jsonify(servicios_ms.agregar_servicio(
        id_cliente=data["id_cliente"],
        tipo_servicio=data["tipo_servicio"],
        descripcion=data.get("descripcion", ""),
    ))


@app.route("/api/servicios/<id_cliente>/<id_servicio>", methods=["PUT"])
def actualizar_servicio(id_cliente, id_servicio):
    data = request.get_json(force=True)
    return jsonify(servicios_ms.actualizar_servicio(
        id_cliente, id_servicio, data.get("descripcion", "")
    ))


# --- Consultas ---
@app.route("/api/consultas/<id_cliente>", methods=["GET"])
def consultar_cliente(id_cliente):
    return jsonify(consultas_ms.consultar_cliente(id_cliente))


@app.route("/api/consultas/<id_cliente>/historial", methods=["GET"])
def historial_servicios(id_cliente):
    return jsonify(consultas_ms.historial_servicios(id_cliente))


@app.route("/api/consultas/resumen", methods=["GET"])
def resumen_general():
    return jsonify(consultas_ms.resumen_general())


# --- Respaldos ---
@app.route("/api/respaldos", methods=["POST"])
def generar_respaldo():
    return jsonify(respaldos_ms.generar_respaldo())


@app.route("/api/respaldos", methods=["GET"])
def listar_respaldos():
    return jsonify(respaldos_ms.listar_respaldos())


@app.route("/api/respaldos/<backup_id>/restaurar", methods=["POST"])
def restaurar_respaldo(backup_id):
    return jsonify(respaldos_ms.restaurar(backup_id))


# --- Monitoreo ---
@app.route("/api/monitoreo/health", methods=["GET"])
def health():
    return jsonify(monitoreo_ms.health())


@app.route("/api/monitoreo/estado", methods=["GET"])
def estado():
    return jsonify(monitoreo_ms.estado_sistema())


@app.route("/api/monitoreo/reporte", methods=["GET"])
def reporte():
    return jsonify(monitoreo_ms.reporte())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
