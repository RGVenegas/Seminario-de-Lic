<<<<<<< HEAD
# Seminario-de-Lic
=======
# Sistema de Inteligencia Artificial Multiagente para el Diseño de Clases Multimedia

## Información del Proyecto

* **Nombre del Proyecto:** Sistema de IA Multiagente para Diseñar Clases Multimedia Coherentes y Editables
* **Categoría:** Proyecto 3 - Seminario de Inteligencia Artificial / Tecnologías Educativas
* **Estado:** Versión Preliminar (Fase I Completada - Prototipo e Interfaz Interactiva)

---

## 1. Descripción General

El presente proyecto implementa un sistema de Inteligencia Artificial Multiagente orientado al diseño automatizado de propuestas de clases multimedia. A diferencia de las aproximaciones monolíticas basadas en un único prompt, esta solución distribuye el trabajo entre agentes de IA especializados que colaboran para estructurar la planificación pedagógica, los contenidos teóricos, las actividades prácticas, la evaluación formativa y los recursos audiovisuales.

El flujo se complementa con un Agente Revisor (Quality Control) encargado de auditar la coherencia didáctica, comunicacional y curricular del material antes de ponerlo a disposición del docente en una interfaz modular y totalmente editable.

---

## 2. Problemática y Solución

### 2.1 Problemática
La generación aislada de componentes educativos mediante modelos de lenguaje (LLM) suele provocar:
* Inconsistencias entre el Objetivo de Aprendizaje (OA) y las actividades de evaluación.
* Desajustes en la profundidad teórica respecto al nivel educativo objetivo.
* Falta de integración entre los recursos audiovisuales sugeridos y la secuencia didáctica.
* Inexistencia de un mecanismo de validación previo a la entrega.

### 2.2 Solución
Un sistema orquestado que recibe cuatro parámetros fundamentales:
1. Objetivo de Aprendizaje (OA).
2. Nivel Educativo.
3. Duración de la sesión.
4. Características o contexto general del curso.

Con estos insumos, los agentes generan una propuesta integral estructurada en módulos independientes y editables.

---

## 3. Arquitectura del Sistema Multiagente

El sistema se compone de siete agentes especializados con roles y responsabilidades diferenciadas:

### 3.1 Agente Orquestador
* **Función:** Coordina la secuencia de generación, distribuye los parámetros de entrada y compila los módulos producidos por los agentes especialistas.
* **Salida:** JSON estructurado con el estado global de la propuesta.

### 3.2 Agente de Planificación Pedagógica
* **Función:** Diseña la secuencia didáctica dividida en etapas (Inicio, Desarrollo y Cierre), asigna los tiempos de ejecución y define el modelo didáctico (Clase Invertida, Aprendizaje Basado en Problemas, 5E, STEM).
* **Salida:** Estructura temporal y metodológica de la sesión.

### 3.3 Agente de Contenidos Teóricos
* **Función:** Redacta el marco conceptual adaptado al nivel educativo, elabora analogías explicativas y compila el glosario de términos clave.
* **Salida:** Explicación teórica enriquecida.

### 3.4 Agente de Actividades Prácticas
* **Función:** Diseña talleres, dinámicas grupales o individuales, y formula preguntas detonantes para promover la participación activa.
* **Salida:** Ficha de trabajo y guías prácticas.

### 3.5 Agente de Evaluación Formativa
* **Función:** Elabora cuestionarios/quizzes de comprobación y construye rúbricas de evaluación detalladas por nivel de desempeño.
* **Salida:** Instrumentos de evaluación alineados al OA.

### 3.6 Agente de Producción Audiovisual
* **Función:** Desarrolla escaletas para videos cortos, redacta prompts para la generación de infografías/imágenes y escribe guiones para audios explicativos.
* **Salida:** Especificación técnica de recursos multimedia.

### 3.7 Agente Revisor (Quality Control)
* **Función:** Audita la coherencia global entre el Objetivo de Aprendizaje y los productos de los demás agentes. Si detecta desalineaciones, solicita correcciones específicas antes de la aprobación final.
* **Salida:** Reporte de auditoría y Score de Coherencia Pedagógica.

---

## 4. Estructura del Repositorio

```
.
├── PROPUESTA_PROYECTO_SISTEMA_MULTIAGENTE.md  # Documento técnico formal de arquitectura
├── README.md                                  # Guía general del repositorio y hoja de ruta
├── index.html                                 # Interfaz web interactiva del prototipo
├── styles.css                                 # Estilos CSS3 (Glassmorphism / Theme)
└── app.js                                     # Lógica de orquestación, simulación y exportación
```

---

## 5. Instrucciones de Ejecución Local

Para visualizar y probar la demostración interactiva en un entorno local, siga los siguientes pasos:

### Opción 1: Servidor en Python (Recomendado)
1. Abra una terminal en el directorio raíz del proyecto.
2. Ejecute el siguiente comando:
   ```bash
   python -m http.server 8080
   ```
3. Abra su navegador web e ingrese a la dirección: `http://localhost:8080`

### Opción 2: Servidor en Node.js
1. Abra una terminal en el directorio raíz del proyecto.
2. Ejecute el servidor estático con:
   ```bash
   npx serve .
   ```
3. Ingrese a la URL indicada en la consola (por defecto `http://localhost:3000`).

---

## 6. Hoja de Ruta Completa y Plan de Hitos del Proyecto

A continuación se detalla la hoja de ruta integral del proyecto, clasificada por fases y estado de ejecución:

### Fase I: Concepción, Arquitectura y Prototipado Frontend (Estado: COMPLETADO)
* **Hito 1: Análisis y Definición Arquitectónica**
  * Estado: Completado.
  * Entregable: Especificación conceptual en `PROPUESTA_PROYECTO_SISTEMA_MULTIAGENTE.md`.
* **Hito 2: Diseño del Modelo de Agentes y Skills**
  * Estado: Completado.
  * Entregable: Definición de roles, entradas y salidas para los 7 agentes.
* **Hito 3: Interfaz Web Interactiva y Sistema Visual (UI/UX)**
  * Estado: Completado.
  * Entregable: Archivos `index.html` y `styles.css` con estética Glassmorphic.
* **Hito 4: Motor de Simulación y Exportación (PoC)**
  * Estado: Completado.
  * Entregable: Lógica en `app.js` con simulación en tiempo real, edición in-situ y exportación Markdown.

---

### Fase II: Desarrollo del Backend Multiagente en Python (Estado: PASOS A SEGUIR)
* **Hito 5: Configuración del Servidor Backend**
  * Estado: Pendiente.
  * Paso a seguir: Implementar una API RESTful en Python 3.11+ utilizando FastAPI para recibir las solicitudes del cliente frontend.
* **Hito 6: Framework de Orquestación de Agentes**
  * Estado: Pendiente.
  * Paso a seguir: Integrar un framework multiagente (LangChain / LangGraph o CrewAI) para definir formalmente la interacción entre agentes.
* **Hito 7: Conexión con Proveedores de LLMs y Prompts Específicos**
  * Estado: Pendiente.
  * Paso a seguir: Conectar los agentes con APIs de modelos de lenguaje (OpenAI GPT-4o, Google Gemini Pro o Anthropic Claude) y afinar los System Prompts por asignatura.

---

### Fase III: Mecanismo Avanzado de Validación y Persistencia (Estado: PASOS A SEGUIR)
* **Hito 8: Algoritmo de Auto-Corrección y Feedback del Revisor**
  * Estado: Pendiente.
  * Paso a seguir: Programar el ciclo recíproco donde el Agente Revisor rechaza borradores con Score < 85% y re-envía instrucciones específicas de corrección a cada agente.
* **Hito 9: Base de Datos y Gestión de Historial**
  * Estado: Pendiente.
  * Paso a seguir: Implementar una base de datos (SQLite / PostgreSQL) para permitir a los docentes guardar, clonar y versionar sus clases multimedia.

---

### Fase IV: Generación Multimedia y Exportación Multiformato (Estado: PASOS A SEGUIR)
* **Hito 10: Integración de Servicios de Generación Audiovisual**
  * Estado: Pendiente.
  * Paso a seguir: Conectar APIs externas para generar voz sintética (audio podcasts) y síntesis de imágenes/infografías reales a partir de los prompts del Agente Audiovisual.
* **Hito 11: Módulo de Exportación Avanzada (PDF / SCORM / PPTX)**
  * Estado: Pendiente.
  * Paso a seguir: Habilitar la descarga de la propuesta en formato PDF maquetado, presentaciones editables (.pptx) y paquetes SCORM compatibles con plataformas LMS (Moodle, Canvas).

---

### Fase V: Pruebas Piloto y Despliegue en Producción (Estado: PASOS A SEGUIR)
* **Hito 12: Evaluación Pedagógica con Docentes**
  * Estado: Pendiente.
  * Paso a seguir: Realizar pruebas de usabilidad con docentes reales para medir el grado de alineación pedagógica en situaciones de aula auténticas.
* **Hito 13: Contenerización y Despliegue Cloud**
  * Estado: Pendiente.
  * Paso a seguir: Crear imágenes de Docker y desplegar la solución en una plataforma en la nube (ej. Render, AWS o Vercel) para su acceso público.

---

## 7. Stack Tecnológico

* **Frontend Prototipo:** HTML5 Semántico, CSS3 Vanilla (Glassmorphism Design System), JavaScript ES6+.
* **Backend de Producción (Fase II):** Python 3.11+, FastAPI, LangChain / LangGraph / CrewAI.
* **Modelos LLM Evaluados:** GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro.

---

## 8. Licencia y Créditos

Proyecto desarrollado dentro del marco del ramo/curso de Seminario de Inteligencia Artificial para la automatización de la preparación didáctica docente.
>>>>>>> d214335 (feat: propuesta preliminar sistema multiagente de clases multimedia)
