# Guía de Funcionamiento del Sistema Multiagente

## Explicación Sencilla de Operación, Flujo y Entregables del Prototipo

> **Aviso Importante sobre esta Versión:**  
> Los datos, puntajes e informes de evaluación mostrados en este prototipo son **simulados (ficticios / de demostración)**. Se incluyeron con el único propósito de ilustrar visualmente cómo funcionará la interfaz y el flujo de auditoría antes de conectar el servidor backend a las APIs reales de Inteligencia Artificial.

---

### 1. ¿Qué es y qué hace el programa?

El programa es una **plataforma web interactiva** que simula el trabajo colaborativo de un **equipo de 7 agentes de Inteligencia Artificial especializados**.

En lugar de solicitar a un único modelo de IA (como ChatGPT de forma directa) que genere todo el material de una clase —lo que suele provocar desorden o inconsistencias—, este sistema recibe los datos de la clase que el docente desea preparar y distribuye las tareas entre agentes expertos en planificación, contenidos teóricos, actividades, evaluación y producción audiovisual, bajo la supervisión de un agente auditor de calidad.

---

### 2. ¿Cómo funciona por dentro? (El Flujo de los 7 Agentes)

Al iniciar la orquestación, el programa activa de forma secuencial los siguientes agentes:

1. **Orquestador:** Recibe los datos de entrada (Objetivo de Aprendizaje, Nivel Educativo, Duración, Contexto) y coordina el trabajo.
2. **Agente de Planificación Pedagógica:** Diseña la estructura temporal de la clase en tres etapas: Inicio, Desarrollo y Cierre.
3. **Agente de Contenidos Teóricos:** Redacta el marco conceptual con lenguaje adecuado al nivel escolar, crea analogías sencillas y compila un glosario.
4. **Agente de Actividades Prácticas:** Diseña dinámicas en parejas o grupales, talleres aplicados y preguntas detonantes de discusión.
5. **Agente de Evaluación Formativa:** Genera cuestionarios de comprobación (quizzes) y elabora rúbricas de evaluación detalladas en tablas.
6. **Agente de Producción Audiovisual:** Escribe el guion para un video corto (3 minutos), guiones de audio y prompts para generar infografías con IA.
7. **Agente Revisor (Quality Control):** Audita que exista coherencia total entre el Objetivo de Aprendizaje, las actividades y la evaluación, emitiendo un porcentaje de aprobación (Score de Coherencia).

---

### 3. Guía Paso a Paso: ¿Cómo se usa?

1. **Abrir la aplicación:**
   - Hacer doble clic en el archivo `index.html` o ingresar en el navegador a `http://localhost:8080`.
2. **Ingresar o seleccionar los datos de la clase:**
   - Se puede pulsar uno de los botones de **ejemplo rápido (1-Click)** para Física, Biología o Historia, o ingresar un Objetivo de Aprendizaje personalizado en la casilla correspondiente.
3. **Ejecutar la IA Multiagente:**
   - Hacer clic en el botón azul **"Orquestar Agentes IA"**.
4. **Visualizar el proceso en vivo:**
   - Observar cómo las tarjetas de los 7 agentes cambian de estado (*En espera ➔ Generando ➔ Completado*) junto al registro de la terminal.
5. **Explorar y modificar el resultado:**
   - Navegar por las pestañas superiores para revisar la propuesta generada.

---

### 4. ¿Qué resultados produce el sistema?

El sistema genera una **Propuesta de Clase Multimedia completa y coherente**, organizada en 6 pestañas principales:

* **Pestaña 1 (Planificación Didáctica):** Cronograma de la sesión con distribución de minutos por etapa.
* **Pestaña 2 (Contenidos Teóricos):** Explicaciones conceptuales, analogías adaptadas y glosario.
* **Pestaña 3 (Actividades Prácticas):** Ficha del taller o experimento práctico para los estudiantes.
* **Pestaña 4 (Evaluación Formativa):** Quiz de comprobación con pauta de respuestas y tabla de rúbrica.
* **Pestaña 5 (Recursos Multimedia):** Escaleta de video explicativo, prompts para infografía y guion de audio.
* **Pestaña 6 (Reporte de Auditoría):** Certificado de coherencia emitido por el Agente Revisor *(Datos simulados para demostración)*.

---

### 5. Funcionalidades Clave para la Presentación

* **Edición In-Situ (Modo Edición):** Al hacer clic en el botón **"Editar Contenido"**, el texto en pantalla se vuelve editable directamente en el navegador, demostrando que el docente tiene el control final sobre el material.
* **Exportación en Markdown / PDF:** Permite descargar el documento en formato `.md` o generar la vista para imprimir en PDF.
