"""
Sistema de Gestión de Tareas
API con Flask para pruebas con Postman
"""
from datetime import datetime

from flask import Flask, jsonify, request, abort

from models import Tarea, EstadoTarea, Prioridad


class GestorTareas:
    """Gestor en memoria de tareas"""

    def __init__(self):
        self.tareas = []
        self.siguiente_id = 1

    def agregar_tarea(self, titulo, descripcion="", prioridad=Prioridad.MEDIA):
        tarea = Tarea(titulo, descripcion, prioridad)
        tarea.id = self.siguiente_id
        self.siguiente_id += 1
        self.tareas.append(tarea)
        return tarea

    def obtener_tarea(self, tarea_id):
        return next((t for t in self.tareas if t.id == tarea_id), None)

    def listar_tareas(self, estado=None):
        if estado:
            return [t for t in self.tareas if t.estado == estado]
        return self.tareas

    def eliminar_tarea(self, tarea_id):
        tarea = self.obtener_tarea(tarea_id)
        if tarea:
            self.tareas.remove(tarea)
            return True
        return False

    def actualizar_tarea(self, tarea_id, **kwargs):
        tarea = self.obtener_tarea(tarea_id)
        if not tarea:
            return None

        if "titulo" in kwargs:
            tarea.titulo = kwargs["titulo"]
        if "descripcion" in kwargs:
            tarea.descripcion = kwargs["descripcion"]
        if "prioridad" in kwargs and isinstance(kwargs["prioridad"], Prioridad):
            tarea.prioridad = kwargs["prioridad"]
        if "estado" in kwargs and isinstance(kwargs["estado"], EstadoTarea):
            if kwargs["estado"] == EstadoTarea.PENDIENTE:
                tarea.estado = EstadoTarea.PENDIENTE
                tarea.fecha_completada = None
            elif kwargs["estado"] == EstadoTarea.EN_PROGRESO:
                tarea.marcar_en_progreso()
                tarea.fecha_completada = None
            elif kwargs["estado"] == EstadoTarea.COMPLETADA:
                tarea.marcar_completada()
            elif kwargs["estado"] == EstadoTarea.CANCELADA:
                tarea.cancelar()

        return tarea

    def estadisticas(self):
        total = len(self.tareas)
        pendientes = len([t for t in self.tareas if t.estado == EstadoTarea.PENDIENTE])
        en_progreso = len([t for t in self.tareas if t.estado == EstadoTarea.EN_PROGRESO])
        completadas = len([t for t in self.tareas if t.estado == EstadoTarea.COMPLETADA])
        canceladas = len([t for t in self.tareas if t.estado == EstadoTarea.CANCELADA])

        return {
            "total": total,
            "pendientes": pendientes,
            "en_progreso": en_progreso,
            "completadas": completadas,
            "canceladas": canceladas,
        }


def _tarea_to_dict(tarea: Tarea) -> dict:
    """Serializa una tarea para respuestas JSON"""
    return {
        "id": tarea.id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "prioridad": tarea.prioridad.value,
        "estado": tarea.estado.value,
        "fecha_creacion": tarea.fecha_creacion.isoformat(),
        "fecha_completada": tarea.fecha_completada.isoformat() if tarea.fecha_completada else None,
    }


def _parse_prioridad(valor: str) -> Prioridad:
    if not valor:
        return Prioridad.MEDIA
    valor_normalizado = valor.strip().lower()
    for prioridad in Prioridad:
        if prioridad.value == valor_normalizado:
            return prioridad
    abort(400, description="Prioridad invalida. Usa: baja, media, alta, urgente")


def _parse_estado(valor: str) -> EstadoTarea:
    if not valor:
        abort(400, description="Estado requerido")
    valor_normalizado = valor.strip().lower()
    for estado in EstadoTarea:
        if estado.value == valor_normalizado:
            return estado
    abort(400, description="Estado invalido. Usa: pendiente, en_progreso, completada, cancelada")


def create_app() -> Flask:
    app = Flask(__name__)
    gestor = GestorTareas()

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    @app.route("/tareas", methods=["GET"])
    def listar_tareas():
        estado_param = request.args.get("estado")
        estado = _parse_estado(estado_param) if estado_param else None
        tareas = gestor.listar_tareas(estado)
        return jsonify([_tarea_to_dict(t) for t in tareas])

    @app.route("/tareas/<int:tarea_id>", methods=["GET"])
    def obtener_tarea(tarea_id):
        tarea = gestor.obtener_tarea(tarea_id)
        if not tarea:
            abort(404, description="Tarea no encontrada")
        return jsonify(_tarea_to_dict(tarea))

    @app.route("/tareas", methods=["POST"])
    def crear_tarea():
        data = request.get_json(silent=True) or {}
        titulo = data.get("titulo")
        if not titulo:
            abort(400, description="El campo 'titulo' es obligatorio")
        descripcion = data.get("descripcion", "")
        prioridad = _parse_prioridad(data.get("prioridad"))
        tarea = gestor.agregar_tarea(titulo, descripcion, prioridad)
        return jsonify(_tarea_to_dict(tarea)), 201

    @app.route("/tareas/<int:tarea_id>", methods=["PATCH"])
    def actualizar_tarea(tarea_id):
        data = request.get_json(silent=True) or {}
        tarea = gestor.obtener_tarea(tarea_id)
        if not tarea:
            abort(404, description="Tarea no encontrada")

        updates = {}
        if "titulo" in data:
            updates["titulo"] = data["titulo"]
        if "descripcion" in data:
            updates["descripcion"] = data["descripcion"]
        if "prioridad" in data:
            updates["prioridad"] = _parse_prioridad(data["prioridad"])
        if "estado" in data:
            updates["estado"] = _parse_estado(data["estado"])

        tarea_actualizada = gestor.actualizar_tarea(tarea_id, **updates)
        return jsonify(_tarea_to_dict(tarea_actualizada))

    @app.route("/tareas/<int:tarea_id>", methods=["DELETE"])
    def eliminar_tarea(tarea_id):
        eliminada = gestor.eliminar_tarea(tarea_id)
        if not eliminada:
            abort(404, description="Tarea no encontrada")
        return jsonify({"mensaje": "Tarea eliminada"})

    @app.route("/tareas/estadisticas", methods=["GET"])
    def obtener_estadisticas():
        return jsonify(gestor.estadisticas())

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
