"""
Modelos de datos para el sistema de gestión de tareas
"""
from datetime import datetime
from enum import Enum


class EstadoTarea(Enum):
    """Estados posibles de una tarea"""
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class Prioridad(Enum):
    """Niveles de prioridad"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class Tarea:
    """Clase que representa una tarea"""
    
    def __init__(self, titulo, descripcion="", prioridad=Prioridad.MEDIA):
        self.id = None
        self.titulo = titulo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = EstadoTarea.PENDIENTE
        self.fecha_creacion = datetime.now()
        self.fecha_vencimiento = None
        self.fecha_completada = None
    
    def marcar_completada(self):
        """Marca la tarea como completada"""
        self.estado = EstadoTarea.COMPLETADA
        self.fecha_completada = datetime.now()
    
    def marcar_en_progreso(self):
        """Marca la tarea como en progreso"""
        self.estado = EstadoTarea.EN_PROGRESO
    
    def cancelar(self):
        """Cancela la tarea"""
        self.estado = EstadoTarea.CANCELADA
    
    def __str__(self):
        return f"[{self.prioridad.value}] {self.titulo} - {self.estado.value}"
    
    def __repr__(self):
        return f"Tarea(id={self.id}, titulo='{self.titulo}', estado={self.estado.value})"
