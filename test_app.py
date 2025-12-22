"""
Pruebas unitarias para el Sistema de Gestión de Tareas
"""
import unittest
from app import GestorTareas
from models import Tarea, EstadoTarea, Prioridad


class TestTarea(unittest.TestCase):
    """Pruebas para la clase Tarea"""
    
    def test_crear_tarea(self):
        """Prueba la creación de una tarea"""
        tarea = Tarea("Tarea de prueba", "Descripción de prueba", Prioridad.ALTA)
        self.assertEqual(tarea.titulo, "Tarea de prueba")
        self.assertEqual(tarea.descripcion, "Descripción de prueba")
        self.assertEqual(tarea.prioridad, Prioridad.ALTA)
        self.assertEqual(tarea.estado, EstadoTarea.PENDIENTE)
    
    def test_marcar_completada(self):
        """Prueba marcar una tarea como completada"""
        tarea = Tarea("Tarea de prueba")
        tarea.marcar_completada()
        self.assertEqual(tarea.estado, EstadoTarea.COMPLETADA)
        self.assertIsNotNone(tarea.fecha_completada)
    
    def test_marcar_en_progreso(self):
        """Prueba marcar una tarea en progreso"""
        tarea = Tarea("Tarea de prueba")
        tarea.marcar_en_progreso()
        self.assertEqual(tarea.estado, EstadoTarea.EN_PROGRESO)
    
    def test_cancelar_tarea(self):
        """Prueba cancelar una tarea"""
        tarea = Tarea("Tarea de prueba")
        tarea.cancelar()
        self.assertEqual(tarea.estado, EstadoTarea.CANCELADA)


class TestGestorTareas(unittest.TestCase):
    """Pruebas para la clase GestorTareas"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.gestor = GestorTareas()
    
    def test_agregar_tarea(self):
        """Prueba agregar una tarea"""
        tarea = self.gestor.agregar_tarea("Nueva tarea", "Descripción", Prioridad.MEDIA)
        self.assertIsNotNone(tarea.id)
        self.assertEqual(len(self.gestor.tareas), 1)
        self.assertEqual(tarea.titulo, "Nueva tarea")
    
    def test_obtener_tarea(self):
        """Prueba obtener una tarea por ID"""
        tarea = self.gestor.agregar_tarea("Tarea 1")
        tarea_obtenida = self.gestor.obtener_tarea(tarea.id)
        self.assertIsNotNone(tarea_obtenida)
        self.assertEqual(tarea_obtenida.titulo, "Tarea 1")
    
    def test_obtener_tarea_inexistente(self):
        """Prueba obtener una tarea que no existe"""
        tarea = self.gestor.obtener_tarea(999)
        self.assertIsNone(tarea)
    
    def test_listar_tareas(self):
        """Prueba listar todas las tareas"""
        self.gestor.agregar_tarea("Tarea 1")
        self.gestor.agregar_tarea("Tarea 2")
        self.gestor.agregar_tarea("Tarea 3")
        tareas = self.gestor.listar_tareas()
        self.assertEqual(len(tareas), 3)
    
    def test_listar_tareas_por_estado(self):
        """Prueba listar tareas filtradas por estado"""
        tarea1 = self.gestor.agregar_tarea("Tarea 1")
        tarea2 = self.gestor.agregar_tarea("Tarea 2")
        tarea3 = self.gestor.agregar_tarea("Tarea 3")
        
        tarea2.marcar_completada()
        tarea3.marcar_completada()
        
        pendientes = self.gestor.listar_tareas(EstadoTarea.PENDIENTE)
        completadas = self.gestor.listar_tareas(EstadoTarea.COMPLETADA)
        
        self.assertEqual(len(pendientes), 1)
        self.assertEqual(len(completadas), 2)
    
    def test_eliminar_tarea(self):
        """Prueba eliminar una tarea"""
        tarea = self.gestor.agregar_tarea("Tarea a eliminar")
        resultado = self.gestor.eliminar_tarea(tarea.id)
        self.assertTrue(resultado)
        self.assertEqual(len(self.gestor.tareas), 0)
    
    def test_eliminar_tarea_inexistente(self):
        """Prueba eliminar una tarea que no existe"""
        resultado = self.gestor.eliminar_tarea(999)
        self.assertFalse(resultado)
    
    def test_actualizar_tarea(self):
        """Prueba actualizar una tarea"""
        tarea = self.gestor.agregar_tarea("Tarea original")
        resultado = self.gestor.actualizar_tarea(
            tarea.id,
            titulo="Tarea actualizada",
            descripcion="Nueva descripción"
        )
        self.assertTrue(resultado)
        self.assertEqual(tarea.titulo, "Tarea actualizada")
        self.assertEqual(tarea.descripcion, "Nueva descripción")
    
    def test_estadisticas(self):
        """Prueba las estadísticas del gestor"""
        tarea1 = self.gestor.agregar_tarea("Tarea 1")
        tarea2 = self.gestor.agregar_tarea("Tarea 2")
        tarea3 = self.gestor.agregar_tarea("Tarea 3")
        tarea4 = self.gestor.agregar_tarea("Tarea 4")
        
        tarea2.marcar_completada()
        tarea3.marcar_completada()
        tarea4.cancelar()
        
        stats = self.gestor.estadisticas()
        
        self.assertEqual(stats['total'], 4)
        self.assertEqual(stats['pendientes'], 1)
        self.assertEqual(stats['completadas'], 2)
        self.assertEqual(stats['canceladas'], 1)
    
    def test_ids_unicos(self):
        """Prueba que los IDs sean únicos y secuenciales"""
        tarea1 = self.gestor.agregar_tarea("Tarea 1")
        tarea2 = self.gestor.agregar_tarea("Tarea 2")
        tarea3 = self.gestor.agregar_tarea("Tarea 3")
        
        self.assertEqual(tarea1.id, 1)
        self.assertEqual(tarea2.id, 2)
        self.assertEqual(tarea3.id, 3)


class TestPrioridad(unittest.TestCase):
    """Pruebas para la enumeración Prioridad"""
    
    def test_valores_prioridad(self):
        """Prueba los valores de prioridad"""
        self.assertEqual(Prioridad.BAJA.value, "baja")
        self.assertEqual(Prioridad.MEDIA.value, "media")
        self.assertEqual(Prioridad.ALTA.value, "alta")
        self.assertEqual(Prioridad.URGENTE.value, "urgente")


class TestEstadoTarea(unittest.TestCase):
    """Pruebas para la enumeración EstadoTarea"""
    
    def test_valores_estado(self):
        """Prueba los valores de estado"""
        self.assertEqual(EstadoTarea.PENDIENTE.value, "pendiente")
        self.assertEqual(EstadoTarea.EN_PROGRESO.value, "en_progreso")
        self.assertEqual(EstadoTarea.COMPLETADA.value, "completada")
        self.assertEqual(EstadoTarea.CANCELADA.value, "cancelada")


if __name__ == "__main__":
    unittest.main()
