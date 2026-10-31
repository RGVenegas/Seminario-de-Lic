# Investigación: Evaluación y Selección del Mejor Modelo de Generación de Imágenes por IA

> **Bitácora y Backlog de Investigación — Seminario de Licenciatura / Titulación**  
> **Fecha de Registro:** Octubre 2026  
> **Estado:** Pendiente / En investigación y pruebas comparativas

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
   * En modelos de difusión más livianos o de generaciones tempranas (como Stable Diffusion 1.5 o v2 base), el codificador de texto (*CLIP text encoder*) procesa tokens como `["child", "dog", "ears", "fur"]` sin una delimitación espacial estricta de a qué sujeto pertenece cada atributo.
   * Al proyectar el ruido latente a la imagen final, los conceptos se "mezclan" o "contagian", asignando características del perro (orejas caninas, pelaje, hocico) a la figura del niño.
2. **Capacidad de razonamiento espacial del modelo:**
   * Modelos más antiguos no comprenden preposiciones espaciales complejas como *"al lado de"*, *"sosteniendo a"*, *"a la izquierda de"*. Tienden a generar una composición híbrida o sobrepuesta.

---

## 3. Matriz Comparativa de Modelos Candidatos a Investigar

A continuación se detallan las opciones de IA generativa de imágenes a evaluar para determinar cuál ofrece mayor precisión anatómica, respeto al prompt (*prompt adherence*) y viabilidad de costos/cuotas para el proyecto:

| Modelo / Proveedor | Fidelidad al Prompt (*Prompt Adherence*) | Manejo de Múltiples Sujetos | Costo / Disponibilidad API | Observación Técnica |
| :--- | :---: | :---: | :---: | :--- |
| **FLUX.1 (Schnell / Dev)** *(Black Forest Labs)* | **Excelente (9.5/10)** | Excelente | Gratuito vía Hugging Face Inference / Replicate (muy bajo costo) | Modelo de arquitectura *flow-matching* de última generación (12B parámetros con T5 text encoder). Resuelve casi por completo el *concept bleeding*. Distingue perfectamente persona y mascota por separado. |
| **Google Imagen 3** *(Google DeepMind / AI Studio)* | **Excelente (9.5/10)** | Excelente | Disponible con API Key de Gemini / Vertex AI | Excelente comprensión del lenguaje natural en español e inglés. Gran realismo y renderizado anatómico correcto (sin orejas de perro en niños). |
| **OpenAI DALL-E 3** | **Muy Alto (9/10)** | Muy Bueno | Comercial (~$0.04 USD por imagen standard) | Optimizado con LLM para reescribir internamente el prompt detallando la separación espacial de los elementos. |
| **SDXL 1.0 / SDXL Turbo** *(Stability AI)* | **Bueno (7.5/10)** | Regular a Bueno | Gratuito vía AI Horde o local | Mejora considerablemente sobre SD 1.5, pero aún puede presentar fugas de atributos si el prompt no usa modificadores negativos fuertes (*negative prompts*). |
| **Recraft V3** | **Sobresaliente (9.8/10)** | Excelente | API de pago con nivel de prueba | Especializado en diseño gráfico, infografías vectoriales y pedagógicas. Número 1 actual en benchmarks de texto y composición espacial. |
| **Stable Diffusion 1.5 / Base Horde** *(Actual)* | **Medio (6.5/10)** | Propenso a errores | 100% Gratuito y descentralizado | Es el motor gratuito actual de AI Horde. Funciona bien para conceptos globales o paisajes, pero comete errores de mezcla de atributos en escenas con niños + animales. |

---

## 4. Estrategias de Mitigación Inmediata con la IA Actual (AI Horde / SD)

Mientras se realiza la investigación comparativa y pruebas con nuevos proveedores de API, se pueden aplicar las siguientes técnicas en el pipeline para minimizar el error:

1. **Desacoplamiento explícito en el prompt generado por Gemini:**
   * En lugar de: `"A boy next to his pet dog"`
   * Formular con separación de capas y sujetos:
     `"A 10-year-old school student standing on the left, smiling, completely human features, distinct separation, a friendly golden retriever dog sitting on the right grass floor, two separate subjects, high quality educational illustration"`
2. **Inclusión de Prompts Negativos (*Negative Prompts*):**
   * `negative_prompt: "hybrid creature, animal ears on human, furry, deformed, fusion, chimera, bad anatomy, mutated, extra limbs"`
3. **Prueba directa del modelo FLUX.1 en el backend:**
   * Integrar la llamada a `FLUX.1-schnell` (disponible gratuitamente o a bajísima latencia en varias plataformas de inferencia comunitaria).

---

## 5. Próximos Pasos del Experimento

1. [ ] Crear un script de pruebas comparativas (`scripts/benchmark_image_models.py`) con 5 casos difíciles:
   - Caso 1: *Niño con su mascota perro al lado (evaluar si mantiene la separación humana/animal).*
   - Caso 2: *Profesor señalando una pizarra con un corazón anatómico.*
   - Caso 3: *Estudiante con microscopio observando una célula vegetal.*
   - Caso 4: *Dos personas conversando, una sosteniendo un libro y la otra una manzana.*
   - Caso 5: *Bicicleta apoyada en un árbol en un parque.*
2. [ ] Evaluar métricas de: tiempo de generación, costo por llamada, presencia de anomalías visuales y adherencia semántica.
3. [ ] Seleccionar el modelo ganador e integrarlo como proveedor primario en [`backend/app/media/image_generator.py`](file:///d:/Codigos%20de%20prueba/Seminario-de-Lic/backend/app/media/image_generator.py).
