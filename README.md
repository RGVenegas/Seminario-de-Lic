# Seminario-de-Lic

# Sistema de Inteligencia Artificial Multiagente para el Diseño de Clases Multimedia Coherentes y Editables

## Información del Proyecto

* **Nombre del Proyecto:** Sistema de IA Multiagente para Diseñar Clases Multimedia Coherentes y Editables
* **Categoría:** Proyecto 3 - Seminario de Inteligencia Artificial / Tecnologías Educativas
* **Estado:** Versión Preliminar (Fase I Completada - Prototipo e Interfaz Interactiva)

---

## 1. Descripción General

El presente proyecto implementa un sistema de Inteligencia Artificial Multiagente orientado al diseño automatizado de propuestas de clases multimedia. A diferencia de las aproximaciones monolíticas basadas en un único prompt —que suelen provocar desorden, alucinaciones o inconsistencias didácticas—, esta solución distribuye el trabajo entre agentes de IA especializados organizados en un **Grafo Acíclico Dirigido (DAG)** secuencial.

Para **reducir el riesgo técnico**, la primera versión (MVP) del sistema se enfoca exclusivamente en la generación secuencial de una **clase multimedia breve** (15 a 20 minutos de desarrollo conceptual), garantizando dependencias reales entre la planificación pedagógica, la redacción teórica, la producción audiovisual y la auditoría de calidad.

---

## 2. Problemática y Solución

### 2.1 Problemática

La generación aislada de componentes educativos mediante modelos de lenguaje (LLM) tradicionales suele provocar:

* **Desalineación Pedagógica:** Inconsistencias entre el Objetivo de Aprendizaje (OA) y el desarrollo conceptual o las actividades.
* **Desalineación Curricular:** Desajustes en la profundidad teórica y lenguaje respecto al nivel educativo objetivo.
* **Desalineación Comunicacional:** Falta de integración entre los recursos audiovisuales sugeridos, la locución y la secuencia didáctica.
* **Ausencia de Validación:** Inexistencia de un mecanismo de control de calidad previo a la entrega del material al docente.

### 2.2 Solución

Un sistema multiagente orquestado en **LangGraph** que recibe cuatro parámetros fundamentales:

1. Objetivo de Aprendizaje (OA).
2. Nivel Educativo.
3. Duración Estimada de la sesión.
4. Características o contexto general del curso.

Con estos insumos, el sistema procesa el flujo por fases dependientes, aplicando ciclos acotados de revisión de 4 pasos (**`Producir ➔ Verificar ➔ Corregir ➔ Aprobar`**) antes de someter el resultado al Agente Revisor y enviarlo al motor determinista de ensamblaje de video (**FFmpeg / MoviePy**).

---

## 3. Arquitectura del Sistema Multiagente (DAG Secuencial)

El sistema se compone de agentes especializados organizados en un flujo dependiente por fases:

### 3.1 Agente Orquestador (LangGraph Engine)

* **Función:** Administra el grafo de estado, gestiona las dependencias entre nodos y controla las transiciones y loops de corrección.
* **Salida:** Estado global JSON del flujo didáctico.

### 3.2 Fase 1: Agente de Planificación Pedagógica

* **Función:** Diseña la secuencia didáctica dividida en tres etapas (Inicio, Desarrollo y Cierre), asigna la dosificación de tiempos y define la metodología (Clase Invertida, ABP, 5E, STEM).
* **Salida:** Estructura temporal y metodológica validada.

### 3.3 Fase 2: Agente de Contenidos Teóricos y Guion

* **Función:** Recibe la planificación aprobada y redacta el cuerpo conceptual adaptado al nivel escolar, analogías explicativas, locución y el glosario de términos clave.
* **Salida:** Guion teórico enriquecido.

### 3.4 Fase 3: Agente de Producción Audiovisual

* **Función:** Toma el guion teórico y la planificación para generar la escaleta escena por escena (locución, imagen en pantalla, texto superpuesto) y prompts visuales para IA generativa.
* **Salida:** Escaleta multimedia técnica y prompts visuales.

### 3.5 Fase 4: Agente Revisor (Quality Control - 7 Criterios)

* **Función:** Audita la propuesta integral mediante una matriz cualitativa de **7 tópicos de calidad**:
  1. Alineación OA vs. Contenido.
  2. Exactitud conceptual y adecuación de lenguaje según nivel.
  3. Coherencia entre escenas y cobertura didáctica.
  4. Factibilidad de tiempos de la sesión.
  5. Correspondencia exacta entre locución, imagen y texto visible.
  6. Control de densidad de información por escena (carga cognitiva).
  7. Trazabilidad de fuentes y comprobación de afirmaciones.
* **Salida:** Reporte de auditoría y Score de Coherencia Pedagógica.

### 3.6 Componente Determinista: Ensamblador de Video (FFmpeg / MoviePy)

* **Función:** Concatenación determinista de pistas de audio (voz sintética), imágenes generadas y renderizado final del archivo de video MP4.
* **Salida:** Clase multimedia breve lista para reproducción y edición.

---

## 4. Estructura del Repositorio

```
.
├── backend/                                   # Backend en Python (FastAPI + LangGraph)
│   ├── app/
│   │   ├── core/config.py                     # Configuración y umbrales de auditoría
│   │   ├── graph/
│   │   │   ├── schemas.py                     # Modelos Pydantic de entrada, salida y 7 criterios
│   │   │   ├── state.py                       # ClassDesignState (TypedDict global)
│   │   │   ├── prompts.py                     # Prompts especializados por agente
│   │   │   ├── nodes.py                       # Funciones de cada agente del DAG
│   │   │   └── pipeline.py                    # StateGraph compilado con loops y aristas condicionales
│   │   └── main.py                            # Servidor FastAPI (endpoints /api/generate y /docs)
│   ├── requirements.txt                       # Dependencias: fastapi, langgraph, langchain-core, langchain-openai
│   └── test_pipeline.py                       # Test de ejecución autónoma del grafo LangGraph
├── GUIA_FUNCIONAMIENTO_PROYECTO.md            # Guía explicativa con los 6 casos de prueba de evaluación
├── PROPUESTA_PROYECTO_SISTEMA_MULTIAGENTE.md  # Documento técnico formal de arquitectura (raíz)
├── README.md                                  # Guía general del repositorio y hoja de ruta
├── index.html                                 # Interfaz web interactiva del prototipo (PoC)
├── styles.css                                 # Estilos CSS3 (Glassmorphism & Estilos de Impresión PDF)
└── app.js                                     # Cliente interactivo (conecta con FastAPI o modo offline)
```

---

## 5. Instrucciones de Ejecución Local

### Opción 1: Ejecución Completa (Backend LangGraph + Frontend)

1. **Instalar dependencias del backend:**

   ```bash
   pip install -r backend/requirements.txt
   ```

   *O instalar manualmente los paquetes clave de LangChain / LangGraph:*

   ```bash
   pip install langchain-openai langgraph fastapi uvicorn pydantic python-dotenv
   ```
2. **Configurar API Key de OpenAI (en archivo `.env`):**

   ```env
   OPENAI_API_KEY=tu_api_key_aqui
   OPENAI_MODEL=gpt-4o-mini
   ```
3. **Probar el grafo de LangGraph de forma autónoma con la LLM:**

   ```bash
   python backend/test_pipeline.py
   ```
4. **Iniciar el servidor API FastAPI:**

   ```bash
   python -m uvicorn backend.app.main:app --reload --port 8000
   ```

   *Acceso a documentación interactiva Swagger:* `http://127.0.0.1:8000/docs`
5. **Servir la interfaz web:**
   En otra terminal en la raíz del proyecto:

   ```bash
   python -m http.server 8080 --bind 127.0.0.1
   ```

   Abrir en el navegador: `http://localhost:8080` (La interfaz se conectará automáticamente a LangGraph).

### Opción 2: Solo Frontend (Modo Demostración Rápida / Standalone)

Hacer doble clic sobre el archivo [index.html](file:///c:/Users/Rodrigo/Desktop/Seminario-de-Lic/index.html) o servirlo mediante `python -m http.server 8080 --bind 127.0.0.1`. Si el backend no está iniciado, la interfaz operará en modo demostración local sin interrupciones.

---

## 6. Hoja de Ruta Completa y Plan de Hitos del Proyecto

A continuación se detalla la hoja de ruta integral del proyecto, clasificada por fases y estado de ejecución:

### Fase I: Concepción, Arquitectura y Prototipado Frontend (Estado: COMPLETADO - Entrega E1)

* **Hito 1: Análisis y Definición Arquitectónica DAG**
  * Estado: Completado.
  * Entregable: Especificación conceptual del DAG secuencial y enfoque MVP en `PROPUESTA_PROYECTO_SISTEMA_MULTIAGENTE.md`.
* **Hito 2: Diseño del Modelo de Agentes, Loops y 7 Criterios QC**
  * Estado: Completado.
  * Entregable: Definición de roles, loops de 4 pasos y matriz de 7 criterios de auditoría.
* **Hito 3: Interfaz Web Interactiva y Sistema Visual (UI/UX)**
  * Estado: Completado.
  * Entregable: Archivos `index.html` y `styles.css` con estética Glassmorphic e impresión PDF integrada.
* **Hito 4: Motor de Simulación y Exportación (PoC)**
  * Estado: Completado.
  * Entregable: Lógica en `app.js` con simulación del DAG en tiempo real, generación dinámica para OA personalizados, edición in-situ y exportación Markdown.

---

### Fase II: Desarrollo del Backend Multiagente en Python (Estado: EN PROGRESO / BASE IMPLEMENTADA)

* **Hito 5: Configuración del Servidor Backend (FastAPI)**
  * Estado: Base Implementada.
  * Entregable: API RESTful en `backend/app/main.py` con endpoint `/api/generate`, soporte CORS y documentación Swagger.
* **Hito 6: Framework de Orquestación con LangGraph**
  * Estado: Base Implementada y Probada.
  * Entregable: Grafo compilado en `backend/app/graph/pipeline.py` con nodos (`pedagogy`, `theory`, `audiovisual`, `reviewer`), esquemas Pydantic y script de verificación `test_pipeline.py`.
* **Hito 7: Conexión con LLMs (API Keys / Sistema de Cuotas Institucional)**
  * Estado: Pendiente.
  * Paso a seguir: Conectar los agentes con APIs de modelos de lenguaje (OpenAI GPT-4o, Gemini Pro, Claude o Sistema de Cuotas de la Universidad).

---

### Fase III: Mecanismo Avanzado de Validación y Persistencia (Estado: PASOS A SEGUIR - Mes 4)

* **Hito 8: Algoritmo de Auto-Corrección y Feedback del Revisor**
  * Estado: Pendiente.
  * Paso a seguir: Programar el ciclo condicional donde el Agente Revisor rechaza borradores con Score < 85% y solicita reescrituras específicas.
* **Hito 9: Base de Datos y Gestión de Historial**
  * Estado: Pendiente.
  * Paso a seguir: Implementar SQLite / PostgreSQL para versionado y guardado de clases.

---

### Fase IV: Generación Multimedia y Exportación Multiformato (Estado: PASOS A SEGUIR - Mes 5)

* **Hito 10: Integración del Componente Determinista de Video (FFmpeg / MoviePy)**
  * Estado: Pendiente.
  * Paso a seguir: Conectar herramientas deterministas de renderizado y síntesis de voz/imágenes para generar el video MP4 final.
* **Hito 11: Módulo de Exportación Avanzada**
  * Estado: Pendiente.
  * Paso a seguir: Exportación extendida a PDF maquetado y paquetes editables.

---

### Fase V: Pruebas Piloto y Despliegue en Producción (Estado: PASOS A SEGUIR - Mes 6)

* **Hito 12: Evaluación Pedagógica con Docentes**
  * Estado: Pendiente.
  * Paso a seguir: Realizar pruebas de usabilidad pedagógica con docentes reales en aula.
* **Hito 13: Contenerización y Despliegue Cloud**
  * Estado: Pendiente.
  * Paso a seguir: Contenerizar con Docker y desplegar la solución en la nube.

---

## 7. Stack Tecnológico

* **Frontend Prototipo:** HTML5 Semántico, CSS3 Vanilla (Glassmorphism & Print Styles), JavaScript ES6+.
* **Backend de Producción (Fase II):** Python 3.11+, FastAPI, **LangGraph** (Orquestador de grafos de estado y loops multiagente), **LangChain / langchain-openai** (Integración con LLMs y salidas estructuradas).
* **Ensamblado Determinista Multimedia:** **FFmpeg / MoviePy** (Concatenación de audio, imágenes y renderizado MP4).
* **Modelos LLM Integrados y Evaluados:** OpenAI (GPT-4o / GPT-4o-mini), Claude 3.5 Sonnet, Gemini Pro y Sistema de Cuotas Institucional.

---

## 8. Notas de Arquitectura e Investigaciones en Curso

* [Aclaración de Orquestación y Sistema Multiagente](notas_arquitectura/ACLARACION_ORQUESTADOR_Y_MULTIAGENTES.md)
* [Requerimiento de Formato Multimedia (Imágenes + TTS)](notas_arquitectura/REQUERIMIENTO_PROFESOR_MULTIMEDIA_TTS.md)
* [Investigación de Modelos de Generación de Imágenes IA (Fidelidad de Sujetos y Concept Bleeding)](notas_arquitectura/INVESTIGACION_MODELOS_GENERACION_IMAGENES_IA.md)

---

## 9. Licencia y Créditos

Proyecto desarrollado dentro del marco del ramo/curso de Seminario de Inteligencia Artificial para la automatización de la preparación didáctica docente.
