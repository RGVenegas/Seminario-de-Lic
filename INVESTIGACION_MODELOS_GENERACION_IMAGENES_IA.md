# Investigación: Evaluación y Selección del Mejor Modelo de Generación de Imágenes por IA

> **Bitácora y Backlog de Investigación — Seminario de Licenciatura / Titulación**  
> **Fecha de Registro:** Octubre - Noviembre 2026  
> **Estado:** Documentado como justificación técnica y trabajo futuro

---

## 1. Observación y Caso Práctico Detectado

> *"Investigar cuál es la mejor IA para generar imágenes, ya que en base a la descripción la IA aún comete errores en los dibujos, quizás porque no está muy entrenada en ese sentido.*
>
> *Ejemplo:*
> * **Instrucción:** *Niño con su mascota al lado*
> * **Dibujo resultante:** *Un niño con orejas de perro.*
>
> *Toca ver qué IA lo hace mejor."*

---

## 2. Diagnóstico Técnico del Problema: *Attribute Binding / Concept Bleeding*

El fenómeno observado (un niño que resulta con rasgos o orejas de animal cuando se le pide "un niño junto a su perro") es un problema clásico y documentado en modelos de difusión y visión generativa conocido como:

1. **Confusión de atributos (*Attribute Binding Failure* / *Concept Bleeding*):**
   * En modelos de difusión livianos o de generaciones tempranas (como Stable Diffusion 1.5 o v2 base), el codificador de texto (*CLIP text encoder*) procesa tokens como `["child", "dog", "ears", "fur"]` sin una delimitación espacial estricta de a qué sujeto pertenece cada atributo.
   * Al proyectar el ruido latente a la imagen final, los conceptos se "mezclan" o "contagian", asignando características del perro (orejas caninas, pelaje, hocico) a la figura del niño.
2. **Capacidad de razonamiento espacial del modelo:**
   * Modelos más antiguos no comprenden preposiciones espaciales complejas como *"al lado de"*, *"sosteniendo a"*, *"a la izquierda de"*. Tienden a generar una composición híbrida o sobrepuesta.

---

## 3. Justificación Académica para la Defensa del Seminario / Memoria de Título

Esta sección está redactada formalmente para responder a la comisión evaluadora o incluir en el informe escrito ante la pregunta:  
**"¿Por qué el sistema no siempre genera imágenes 100% precisas y a veces confunde elementos?"**

### Argumentos Técnicos y Metodológicos:

1. **Decisión de Arquitectura: Viabilidad y Operación a Costo Cero ($0 USD)**  
   * El proyecto se diseñó bajo el principio de **democratización educativa y sostenibilidad económica**, garantizando que un docente o establecimiento pueda generar lecciones multimedia ilimitadas sin requerir tarjetas de crédito ni presupuesto recurrente.
   * Por ello, el pipeline utiliza **AI Horde (Stable Diffusion descentralizado)** en lugar de soluciones comerciales como OpenAI DALL-E 3 (que cobra ~$0.04 USD por imagen / ~$0.16 USD por video de 4 escenas).
   * **Trade-off:** La gratuidad implica utilizar modelos de difusión basados en CLIP con parámetros acotados (~1B a 2B parámetros), los cuales presentan una menor capacidad de aislamiento semántico en comparación con modelos comerciales masivos.

2. **Diferencia entre el Razonamiento Textual (LLM) y la Síntesis Visual (Difusión)**  
   * Los agentes pedagógicos (basados en LLMs como GPT-4o o Gemini) razonan y estructuran la clase con altísima precisión didáctica y lingüística.
   * Sin embargo, el generador visual es un modelo probabilístico de difusión latente que reconstruye píxeles a partir de ruido gaussiano. Cuando una escena contiene **múltiples sujetos de distinta naturaleza** (humano + animal cuadrúpedo), el espacio latente del modelo libre tiende a promediar las características morfológicas si no cuenta con guías de atención cruzada (*Cross-Attention Control*) avanzadas.

3. **Independencia y Modularidad del Sistema (Arquitectura Desacoplada)**  
   * En términos de ingeniería de software, el **Agente Audiovisual genera la escaleta y los prompts de forma agnóstica al motor visual**.
   * Esto significa que la limitación visual **no es un fallo de diseño del sistema multiagente**, sino una restricción temporal del proveedor de renderizado libre seleccionado. Si en el futuro una institución educativa financia el uso de DALL-E 3, Google Imagen 3 o FLUX.1, basta con cambiar el proveedor en el backend sin modificar ninguna otra fase del grafo.

---

## 4. Matriz Comparativa de Modelos de Generación Visual

| Modelo / Proveedor | Fidelidad al Prompt (*Prompt Adherence*) | Manejo de Múltiples Sujetos | Costo / Disponibilidad API | Observación Técnica |
| :--- | :---: | :---: | :---: | :--- |
| **OpenAI DALL-E 3** | **Muy Alto (9.5/10)** | Excelente | Comercial (~$0.04 USD por imagen) | Utiliza internamente un LLM que reescribe el prompt separando explícitamente coordenadas y sujetos. **Elimina el error del niño con orejas de perro.** |
| **Google Imagen 3** *(Google DeepMind)* | **Excelente (9.5/10)** | Excelente | Requiere facturación en Google Cloud / Vertex AI | Máxima fidelidad fotorrealista e infográfica, sin confusiones morfológicas. |
| **FLUX.1 (Schnell / Dev)** *(Black Forest Labs)* | **Excelente (9.5/10)** | Excelente | Opciones gratuitas / bajísimo costo en Hugging Face | Arquitectura moderna *flow-matching* de 12B parámetros con codificador T5. Gran comprensión espacial. |
| **Stable Diffusion (AI Horde)** *(Actual en el proyecto)* | **Medio (6.5/10)** | Propenso a mezclas | **100% Gratuito y descentralizado** | Permite pruebas ilimitadas a costo cero. Presenta *concept bleeding* en escenas complejas de varios sujetos. |

---

## 5. Estrategias de Mitigación Inmediata con la IA Actual

Mientras se mantenga el motor gratuito, el sistema mitiga este problema mediante:

1. **Desacoplamiento sintáctico en el prompt generado:**
   * En lugar de: *"Niño jugando con su perro"*
   * Formular con separación espacial estricta:  
     `"A 10-year-old human student sitting on the left side, distinct human anatomy, smiling, separated from a golden retriever dog sitting on the right grass, two distinct subjects, clean educational illustration"`
2. **Prompts Negativos (*Negative Prompts*):**  
   `negative_prompt: "hybrid creature, animal ears on human, furry, chimera, fusion, deformed limbs, merged bodies"`
