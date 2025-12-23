# Sistema de Gestión de Tareas

Sistema completo para la gestión de tareas con funcionalidades de creación, actualización, eliminación y estadísticas.

## Descripción

Este proyecto es un sistema de gestión de tareas desarrollado en Python que permite organizar y controlar el flujo de trabajo mediante la administración de tareas con diferentes estados y prioridades.

## Características

-  Crear tareas con título, descripción y prioridad
-  Actualizar el estado de las tareas
-  Listar y filtrar tareas por estado
-  Ver estadísticas generales
-  Eliminar tareas
-  Cuatro niveles de prioridad: Baja, Media, Alta, Urgente
-  Cuatro estados: Pendiente, En Progreso, Completada, Cancelada

## 📁 Estructura del Proyecto

```
sistema-gestion-tareas/
│
├── app.py                     # Aplicación principal con interfaz de usuario
├── models.py                  # Modelos de datos (Tarea, Estados, Prioridades)
├── test_app.py               # Pruebas unitarias
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
└── pruebas/
    ├── casos_de_prueba.xlsx  # Casos de prueba documentados
    └── informe_final.docx    # Informe de pruebas y resultados
```

## 🛠️ Instalación

1. Clonar o descargar el proyecto
2. Instalar las dependencias (opcional):

```bash
pip install -r requirements.txt
```

## ▶️ Uso

### Ejecutar la aplicación:

```bash
python app.py
```

### Ejecutar las pruebas:

```bash
python test_app.py
```

O usando pytest:

```bash
pytest test_app.py -v
```

## 📖 Módulos

### models.py

Contiene las clases de datos:
- `Tarea`: Clase principal para representar una tarea
- `EstadoTarea`: Enumeración de estados posibles
- `Prioridad`: Enumeración de niveles de prioridad

### app.py

Contiene:
- `GestorTareas`: Clase para gestionar la colección de tareas
- `main()`: Interfaz de línea de comandos
- Funciones auxiliares para la interacción con el usuario

### test_app.py

Suite completa de pruebas unitarias que cubren:
- Creación y manipulación de tareas
- Operaciones CRUD del gestor
- Validación de estados y prioridades
- Generación de estadísticas

## 🎮 Menú Principal

1. Agregar tarea
2. Listar tareas
3. Ver tarea específica
4. Actualizar estado de tarea
5. Eliminar tarea
6. Ver estadísticas
0. Salir

## 🧪 Pruebas

El proyecto incluye pruebas unitarias exhaustivas:

- `TestTarea`: Pruebas para la clase Tarea
- `TestGestorTareas`: Pruebas para el gestor de tareas
- `TestPrioridad`: Validación de prioridades
- `TestEstadoTarea`: Validación de estados

## 📊 Casos de Prueba

Los casos de prueba detallados se encuentran en:
- `pruebas/casos_de_prueba.xlsx` - Casos de prueba documentados
- `pruebas/informe_final.docx` - Informe de resultados y análisis

## 👤 Autor

Desarrollado como proyecto de Python

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📧 Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.

---

**Versión:** 1.0.0  
**Fecha:** Diciembre 2025
