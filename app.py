"""
Sistema de Gestión de Tareas
Aplicación principal
"""
from models import Tarea, EstadoTarea, Prioridad
from datetime import datetime


class GestorTareas:
    """Clase principal para gestionar tareas"""
    
    def __init__(self):
        self.tareas = []
        self.siguiente_id = 1
    
    def agregar_tarea(self, titulo, descripcion="", prioridad=Prioridad.MEDIA):
        """Agrega una nueva tarea al sistema"""
        tarea = Tarea(titulo, descripcion, prioridad)
        tarea.id = self.siguiente_id
        self.siguiente_id += 1
        self.tareas.append(tarea)
        return tarea
    
    def obtener_tarea(self, tarea_id):
        """Obtiene una tarea por su ID"""
        for tarea in self.tareas:
            if tarea.id == tarea_id:
                return tarea
        return None
    
    def listar_tareas(self, estado=None):
        """Lista todas las tareas, opcionalmente filtradas por estado"""
        if estado:
            return [t for t in self.tareas if t.estado == estado]
        return self.tareas
    
    def eliminar_tarea(self, tarea_id):
        """Elimina una tarea del sistema"""
        tarea = self.obtener_tarea(tarea_id)
        if tarea:
            self.tareas.remove(tarea)
            return True
        return False
    
    def actualizar_tarea(self, tarea_id, **kwargs):
        """Actualiza los campos de una tarea"""
        tarea = self.obtener_tarea(tarea_id)
        if not tarea:
            return False
        
        for clave, valor in kwargs.items():
            if hasattr(tarea, clave):
                setattr(tarea, clave, valor)
        return True
    
    def estadisticas(self):
        """Genera estadísticas sobre las tareas"""
        total = len(self.tareas)
        pendientes = len([t for t in self.tareas if t.estado == EstadoTarea.PENDIENTE])
        en_progreso = len([t for t in self.tareas if t.estado == EstadoTarea.EN_PROGRESO])
        completadas = len([t for t in self.tareas if t.estado == EstadoTarea.COMPLETADA])
        canceladas = len([t for t in self.tareas if t.estado == EstadoTarea.CANCELADA])
        
        return {
            'total': total,
            'pendientes': pendientes,
            'en_progreso': en_progreso,
            'completadas': completadas,
            'canceladas': canceladas
        }


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("   SISTEMA DE GESTIÓN DE TAREAS")
    print("="*50)
    print("1. Agregar tarea")
    print("2. Listar tareas")
    print("3. Ver tarea específica")
    print("4. Actualizar estado de tarea")
    print("5. Eliminar tarea")
    print("6. Ver estadísticas")
    print("0. Salir")
    print("="*50)


def main():
    """Función principal"""
    gestor = GestorTareas()
    
    # Agregar algunas tareas de ejemplo
    gestor.agregar_tarea("Completar documentación", "Documentar las funciones principales", Prioridad.ALTA)
    gestor.agregar_tarea("Revisar código", "Code review del módulo principal", Prioridad.MEDIA)
    gestor.agregar_tarea("Crear pruebas unitarias", "Implementar tests", Prioridad.ALTA)
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            titulo = input("Título de la tarea: ")
            descripcion = input("Descripción: ")
            print("\nPrioridad: 1-Baja, 2-Media, 3-Alta, 4-Urgente")
            prioridad_input = input("Seleccione prioridad (2): ").strip() or "2"
            prioridades = {
                "1": Prioridad.BAJA,
                "2": Prioridad.MEDIA,
                "3": Prioridad.ALTA,
                "4": Prioridad.URGENTE
            }
            prioridad = prioridades.get(prioridad_input, Prioridad.MEDIA)
            
            tarea = gestor.agregar_tarea(titulo, descripcion, prioridad)
            print(f"\n✓ Tarea agregada exitosamente (ID: {tarea.id})")
        
        elif opcion == "2":
            tareas = gestor.listar_tareas()
            if not tareas:
                print("\nNo hay tareas registradas.")
            else:
                print("\n" + "="*80)
                print(f"{'ID':<5} {'Título':<30} {'Prioridad':<12} {'Estado':<15}")
                print("="*80)
                for tarea in tareas:
                    print(f"{tarea.id:<5} {tarea.titulo[:28]:<30} {tarea.prioridad.value:<12} {tarea.estado.value:<15}")
                print("="*80)
        
        elif opcion == "3":
            tarea_id = int(input("ID de la tarea: "))
            tarea = gestor.obtener_tarea(tarea_id)
            if tarea:
                print("\n" + "="*60)
                print(f"ID: {tarea.id}")
                print(f"Título: {tarea.titulo}")
                print(f"Descripción: {tarea.descripcion}")
                print(f"Prioridad: {tarea.prioridad.value}")
                print(f"Estado: {tarea.estado.value}")
                print(f"Fecha creación: {tarea.fecha_creacion.strftime('%Y-%m-%d %H:%M')}")
                print("="*60)
            else:
                print("\n✗ Tarea no encontrada.")
        
        elif opcion == "4":
            tarea_id = int(input("ID de la tarea: "))
            tarea = gestor.obtener_tarea(tarea_id)
            if tarea:
                print("\n1. Pendiente")
                print("2. En progreso")
                print("3. Completada")
                print("4. Cancelada")
                estado_opcion = input("Nuevo estado: ")
                
                if estado_opcion == "1":
                    tarea.estado = EstadoTarea.PENDIENTE
                elif estado_opcion == "2":
                    tarea.marcar_en_progreso()
                elif estado_opcion == "3":
                    tarea.marcar_completada()
                elif estado_opcion == "4":
                    tarea.cancelar()
                
                print("\n✓ Estado actualizado.")
            else:
                print("\n✗ Tarea no encontrada.")
        
        elif opcion == "5":
            tarea_id = int(input("ID de la tarea a eliminar: "))
            confirmacion = input("¿Está seguro? (s/n): ")
            if confirmacion.lower() == 's':
                if gestor.eliminar_tarea(tarea_id):
                    print("\n✓ Tarea eliminada.")
                else:
                    print("\n✗ Tarea no encontrada.")
        
        elif opcion == "6":
            stats = gestor.estadisticas()
            print("\n" + "="*40)
            print("   ESTADÍSTICAS")
            print("="*40)
            print(f"Total de tareas:     {stats['total']}")
            print(f"Pendientes:          {stats['pendientes']}")
            print(f"En progreso:         {stats['en_progreso']}")
            print(f"Completadas:         {stats['completadas']}")
            print(f"Canceladas:          {stats['canceladas']}")
            print("="*40)
        
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        
        else:
            print("\n✗ Opción no válida.")


if __name__ == "__main__":
    main()
