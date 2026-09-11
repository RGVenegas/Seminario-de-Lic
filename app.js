/* ==========================================================================
   LÓGICA DEL SISTEMA MULTIAGENTE DE CLASES MULTIMEDIA (app.js)
   Orquestación, Simulación de Agentes, Renderizado Dinámico & Edición
   ========================================================================== */

// Base de Datos de Presets Didácticos para Demostración
const PRESETS = {
  fisica: {
    oa: "Comprender la Ley de Conservación de la Energía (la energía no se crea ni se destruye, solo se transforma) y aplicar sus principios a situaciones cotidianas.",
    level: "Secundaria (1º - 4º)",
    duration: "90 Minutos",
    approach: "Clase Invertida (Flipped Classroom)",
    context: "Aula equipada con proyector y trabajo colaborativo en parejas.",
    
    pedagogy: `
      <div class="module-card">
        <div class="module-header">
          <div class="module-title"><i class="fa-solid fa-play"></i> Etapa 1: Inicio / Enganche Didáctico</div>
          <span class="tag-time">15 Minutos</span>
        </div>
        <p><strong>Actividad de Apertura:</strong> Recuperación de saberes previos mediante pregunta detonante: <em>"¿A dónde va a parar la energía de una pelota rebotando hasta detenerse?"</em>. Proyección del audio interactivo de introducción de 2 minutos.</p>
      </div>

      <div class="module-card">
        <div class="module-header">
          <div class="module-title"><i class="fa-solid fa-gears"></i> Etapa 2: Desarrollo y Aplicación Práctica</div>
          <span class="tag-time">55 Minutos</span>
        </div>
        <p><strong>Trabajo Colaborativo:</strong> Estudio de casos prácticos (Montaña Rusa y Péndulo de Newton). Los estudiantes identifican las transformaciones entre Energía Potencial Gravitatoria ($E_p$) y Energía Cinética ($E_c$).</p>
      </div>

      <div class="module-card">
        <div class="module-header">
          <div class="module-title"><i class="fa-solid fa-flag-checkered"></i> Etapa 3: Cierre y Metacognición</div>
          <span class="tag-time">20 Minutos</span>
        </div>
        <p><strong>Síntesis y Evaluación:</strong> Cuestionario interactivo de 5 preguntas (quiz formativo). Ticket de salida metacognitivo: <em>"Un ejemplo de conservación de energía en tu casa es..."</em>.</p>
      </div>
    `,

    theory: `
      <div class="module-card">
        <h3 style="color: var(--primary-navy); margin-bottom: 10px;"><i class="fa-solid fa-atom"></i> Concepto Central: Conservación de la Energía</h3>
        <p>La <strong>Ley de Conservación de la Energía</strong> establece que la cantidad total de energía en un sistema aislado permanece constante a lo largo del tiempo. La energía puede transformarse de una forma a otra (ej. de mecánica a térmica), pero no puede crearse ni destruirse.</p>
        <br>
        <p><strong>Ecuación Fundamental:</strong> $E_{total} = E_c + E_p = \text{Constante}$</p>
      </div>

      <div class="module-card">
        <h4 style="color: var(--primary-indigo); margin-bottom: 8px;"><i class="fa-solid fa-lightbulb"></i> Analogía Didáctica (Adaptada al Nivel)</h4>
        <p>Imagina que tienes <strong>100 monedas en tu billetera</strong>. Puedes cambiar 50 monedas por un billete, o transferir 20 monedas a tu cuenta digital. Al final del día, aunque la forma de tu dinero haya cambiado (físico o digital), sigues teniendo exactamente $100. La energía funciona igual.</p>
      </div>

      <div class="module-card">
        <h4 style="color: var(--accent-teal); margin-bottom: 8px;"><i class="fa-solid fa-book"></i> Glosario Clave para el Estudiante</h4>
        <ul>
          <li><strong>Energía Cinética ($E_c$):</strong> Energía asociada al movimiento de un cuerpo.</li>
          <li><strong>Energía Potencial ($E_p$):</strong> Energía almacenada debido a la posición o configuración de un objeto.</li>
          <li><strong>Disipación Térmica:</strong> Transformación de energía útil en calor por rozamiento o fricción.</li>
        </ul>
      </div>
    `,

    activities: `
      <div class="module-card">
        <div class="module-header">
          <div class="module-title"><i class="fa-solid fa-user-group"></i> Taller Práctico: "Simulador de Montaña Rusa"</div>
          <span class="tag-time">Parejas / 35 Min</span>
        </div>
        <p><strong>Objetivo de la Actividad:</strong> Identificar los puntos de máxima energía cinética y potencial en una trayectoria curvilínea.</p>
        <br>
        <ol style="margin-left: 20px;">
          <li>Construir un circuito simple usando una manguera transparente y una canica de vidrio.</li>
          <li>Medir la altura inicial $h_1$ y observar si la canica logra completar un bucle (*loop*).</li>
          <li>Registrar en la guía práctica las transformaciones $E_p \rightarrow E_c \rightarrow \text{Calor por fricción}$.</li>
        </ol>
      </div>

      <div class="module-card">
        <h4 style="color: var(--accent-amber); margin-bottom: 8px;"><i class="fa-solid fa-comments"></i> Pregunta Detonante para Discusión</h4>
        <p><em>"Si la energía se conserva siempre, ¿por qué los científicos insisten en que debemos 'ahorrar energía' en el planeta?"</em></p>
      </div>
    `,

    evaluation: `
      <div class="module-card">
        <h4 style="color: var(--primary-navy); margin-bottom: 12px;"><i class="fa-solid fa-square-poll-vertical"></i> Quiz Formativo (5 Preguntas)</h4>
        <ol style="margin-left: 20px; font-size: 0.9rem;">
          <li><strong>¿Qué ocurre con la energía cinética de un vehículo al frenar en seco?</strong><br><small style="color: var(--text-muted);">a) Se destruye<br>b) Se transforma en calor por fricción en las balatas [Correcta]<br>c) Se almacena como masa</small></li>
          <li style="margin-top: 10px;"><strong>En el punto más alto de un columpio, la energía es mayoritariamente:</strong><br><small style="color: var(--text-muted);">a) Potencial Gravitatoria [Correcta]<br>b) Cinética pura<br>c) Eléctrica</small></li>
        </ol>
      </div>

      <div class="module-card">
        <h4 style="color: var(--primary-indigo); margin-bottom: 12px;"><i class="fa-solid fa-table"></i> Rúbrica de Evaluación de la Actividad</h4>
        <table class="rubric-table">
          <thead>
            <tr>
              <th>Criterio</th>
              <th>Excelente (3 pts)</th>
              <th>En Desarrollo (2 pts)</th>
              <th>Inicial (1 pt)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Comprensión del OA</td>
              <td>Explica correctamente la transformación $E_p \leftrightarrow E_c$.</td>
              <td>Confunde algunos momentos de máxima energía.</td>
              <td>No relaciona los conceptos con el experimento.</td>
            </tr>
            <tr>
              <td>Trabajo en Equipo</td>
              <td>Colabora activamente y registra datos.</td>
              <td>Participa parcialmente en la medición.</td>
              <td>No realiza aportes al grupo.</td>
            </tr>
          </tbody>
        </table>
      </div>
    `,

    audiovisual: `
      <div class="module-card">
        <h4 style="color: var(--primary-navy); margin-bottom: 10px;"><i class="fa-solid fa-film"></i> Escaleta / Guion de Video Corto (3 Minutos)</h4>
        <p><strong>Título del Video:</strong> "La Energía Nunca Muere: El Viaje de una Montaña Rusa"</p>
        <p><strong>Escena 1 (0:00 - 0:45):</strong> Tomas dinámicas de una montaña rusa subiendo. Narrador en off explica la energía almacenada en la cima.</p>
        <p><strong>Escena 2 (0:45 - 2:00):</strong> Animación 2D superpuesta mostrando barras de energía $E_p$ (verde) y $E_c$ (azul) intercambiándose en la bajada.</p>
        <p><strong>Escena 3 (2:00 - 3:00):</strong> Cierre con analogía del mundo real y llamado a la acción para la clase.</p>
      </div>

      <div class="module-card">
        <h4 style="color: var(--primary-indigo); margin-bottom: 10px;"><i class="fa-solid fa-image"></i> Prompt para Generación de Infografía (IA Generativa Visual)</h4>
        <pre style="background: #f8fafc; padding: 12px; border-radius: 8px; font-family: var(--font-code); font-size: 0.82rem; color: #1e293b; border: 1px solid var(--border-light); white-space: pre-wrap;">"A clean vector educational infographic explaining the Law of Conservation of Energy, featuring a rollercoaster loop with color-coded energy bars (Green for Potential, Blue for Kinetic), white background with subtle slate lines, clean academic typography, high resolution."</pre>
      </div>

      <div class="module-card">
        <h4 style="color: var(--accent-teal); margin-bottom: 10px;"><i class="fa-solid fa-microphone"></i> Guion de Audio Podcast (Apertura de Clase)</h4>
        <p><em>[Música de fondo suave y tecnológica]</em><br><strong>Locutor:</strong> "Hola a todos. ¿Sabían que la misma energía que usó un dinosaurio para correr sigue aquí en la Tierra transformándose en luz, viento o movimiento? Hoy descubriremos la regla de oro del universo..."</p>
      </div>
    `
  },

  biologia: {
    oa: "Explicar el proceso de fotosíntesis en las plantas y su importancia en el flujo de energía dentro de la cadena trófica.",
    level: "Primaria (5º - 6º)",
    duration: "45 Minutos",
    approach: "Aprendizaje Basado en Problemas (ABP)",
    context: "Trabajo con hojas recolectadas del patio escolar.",
    
    pedagogy: `
      <div class="module-card">
        <div class="module-header">
          <div class="module-title"><i class="fa-solid fa-seedling"></i> Etapa 1: Pregunta Problema</div>
          <span class="tag-time">10 Minutos</span>
        </div>
        <p><strong>Pregunta detonante:</strong> <em>"Si las plantas no comen como nosotros, ¿de dónde sacan la energía para crecer tan grandes?"</em></p>
      </div>
      <div class="module-card">
        <div class="module-header">
          <div class="module-title"><i class="fa-solid fa-sun"></i> Etapa 2: Exploración de la Fotosíntesis</div>
          <span class="tag-time">25 Minutos</span>
        </div>
        <p>Observación guiada con lupa de estomas en hojas verdes y armado del esquema interactivo Sol + Agua + $CO_2 \rightarrow$ Glucosa + $O_2$.</p>
      </div>
      <div class="module-card">
        <div class="module-header">
          <div class="module-title"><i class="fa-solid fa-leaf"></i> Etapa 3: Cierre</div>
          <span class="tag-time">10 Minutos</span>
        </div>
        <p>Dibujo individual del ciclo de fotosíntesis y autoevaluación caritas.</p>
      </div>
    `,
    theory: `
      <div class="module-card">
        <h3 style="color: var(--accent-teal);"><i class="fa-solid fa-plant-wilt"></i> ¿Qué es la Fotosíntesis?</h3>
        <p>La fotosíntesis es el proceso mediante el cual las plantas verdes fabrican su propio alimento utilizando la luz del Sol, agua del suelo y dióxido de carbono del aire.</p>
      </div>
    `,
    activities: `
      <div class="module-card">
        <h4>Experimento "Burbujas de Oxígeno"</h4>
        <p>Colocar una planta acuática (Elodea) en un vaso con agua bajo la luz de una lámpara y contar las burbujas de oxígeno producidas en 5 minutos.</p>
      </div>
    `,
    evaluation: `
      <div class="module-card">
        <h4>Lista de Cotejo Formativa</h4>
        <ul>
          <li>Identifica los 3 ingredientes necesarios para la fotosíntesis.</li>
          <li>Reconoce el oxígeno como el gas liberado a la atmósfera.</li>
        </ul>
      </div>
    `,
    audiovisual: `
      <div class="module-card">
        <h4>Prompt Infografía Ilustrada para Niños</h4>
        <pre style="background: #f8fafc; padding: 12px; border-radius: 8px; color: #1e293b; border: 1px solid var(--border-light);">"Cute colorful cartoon illustration showing a happy plant absorbing sunlight, water droplets, and CO2, releasing oxygen bubbles, friendly educational style for kids."</pre>
      </div>
    `
  },

  historia: {
    oa: "Analizar las causas y consecuencias de la Revolución Industrial en la transformación del trabajo y la vida urbana.",
    level: "Bachillerato / Media",
    duration: "90 Minutos",
    approach: "Modelo de Indagación 5E",
    context: "Analítica comparativa de fuentes históricas y grabados del siglo XIX.",
    pedagogy: `<div class="module-card"><h4>Secuencia 5E: Enganchar, Explorar, Explicar, Elaborar, Evaluar</h4><p>Análisis de testimonios de obreros textiles y contraste con la automatización moderna.</p></div>`,
    theory: `<div class="module-card"><h4>La Máquina de Vapor y la Revolución Fabril</h4><p>Estudio de la transición de la producción artesanal a la industrialización masiva.</p></div>`,
    activities: `<div class="module-card"><h4>Debate de Rol: Artesanos vs Industriales</h4><p>Juego de roles sobre las condiciones laborales de 1840.</p></div>`,
    evaluation: `<div class="module-card"><h4>Ensayo Corto de Análisis Crítico</h4><p>Rúbrica de evaluación sobre causalidad histórica.</p></div>`,
    audiovisual: `<div class="module-card"><h4>Guion de Video Documental corto</h4><p>Escaleta sobre las ciudades industriales de Manchester y Birmingham en 1850.</p></div>`
  }
};

let currentPresetKey = 'fisica';
let isEditMode = false;

// Carga Inicial
document.addEventListener('DOMContentLoaded', () => {
  loadPreset('fisica');
});

// Función para cargar o alternar (toggle) un preset
function loadPreset(key, evt) {
  const targetBtn = evt ? evt.currentTarget : document.querySelector(`.chip-btn[data-preset="${key}"]`);
  const isAlreadyActive = targetBtn && targetBtn.classList.contains('active');

  // Si el chip ya está activo y se vuelve a presionar, desmarcar (toggle off)
  if (isAlreadyActive && evt) {
    targetBtn.classList.remove('active');
    currentPresetKey = null;
    return;
  }

  currentPresetKey = key;
  const p = PRESETS[key];

  // Desmarcar todos los botones y activar únicamente el seleccionado
  document.querySelectorAll('.chip-btn').forEach(btn => btn.classList.remove('active'));
  if (targetBtn) targetBtn.classList.add('active');

  // Llenar formulario
  document.getElementById('learningObjective').value = p.oa;
  document.getElementById('educationLevel').value = p.level;
  document.getElementById('classDuration').value = p.duration;
  document.getElementById('pedagogicalApproach').value = p.approach;
  if (p.context) document.getElementById('courseContext').value = p.context;

  // Llenar vista previa
  renderPresetContent(p);
}

// Renderizado de contenidos en pestañas
function renderPresetContent(p) {
  if (document.getElementById('content-pedagogy')) document.getElementById('content-pedagogy').innerHTML = p.pedagogy;
  if (document.getElementById('content-theory')) document.getElementById('content-theory').innerHTML = p.theory;
  if (document.getElementById('content-audiovisual')) document.getElementById('content-audiovisual').innerHTML = p.audiovisual;
}

// Cambio de Pestañas (Tabs)
function switchTab(tabId, btnElement) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content-panel').forEach(panel => panel.classList.remove('active'));

  btnElement.classList.add('active');
  document.getElementById(tabId).classList.add('active');
}

// Simulación de Orquestación Multiagente (DAG Secuencial en LangGraph)
async function handleGenerate(e) {
  e.preventDefault();
  
  const btn = document.getElementById('btnGenerate');
  const spinner = document.getElementById('terminalSpinner');
  const statusLog = document.getElementById('statusLogText');
  
  btn.disabled = true;
  spinner.classList.add('visible');

  // Reset visual de tarjetas de agentes en el DAG
  const agentCards = ['orchestrator', 'pedagogy', 'content', 'av', 'reviewer', 'ffmpeg'];
  agentCards.forEach(id => {
    const card = document.getElementById(`agent-${id}`);
    if (card) {
      card.className = 'agent-card';
      card.querySelector('.agent-status-badge').innerText = 'En espera';
    }
  });

  const steps = [
    { agent: 'orchestrator', status: '[LangGraph Engine] Inicializando grafo de estado DAG y parametrizando OA...', delay: 600 },
    { agent: 'pedagogy', status: '[Fase 1: Planificación] Ejecutando loop: Producir -> Verificar -> Corregir -> Aprobar...', delay: 850 },
    { agent: 'content', status: '[Fase 2: Guion Teórico] Recibiendo planificación validada. Generando locución y explicaciones...', delay: 850 },
    { agent: 'av', status: '[Fase 3: Escaleta Audiovisual] Insumo: Teoría aprobada. Diseñando escenas, locución y prompts...', delay: 850 },
    { agent: 'reviewer', status: '[Fase 4: Agente Revisor] Auditando la propuesta en base a los 7 Criterios de Calidad (Score: 94%)...', delay: 1000 },
    { agent: 'ffmpeg', status: '[Componente Determinista] Invocando FFmpeg / MoviePy para ensamblado y renderizado de video MP4...', delay: 700 }
  ];

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const card = document.getElementById(`agent-${step.agent}`);
    if (!card) continue;
    
    // Marcar como activo
    if(step.agent === 'reviewer') {
      card.className = 'agent-card reviewing';
      card.querySelector('.agent-status-badge').innerText = 'Auditando (7 Criterios)';
    } else if(step.agent === 'ffmpeg') {
      card.className = 'agent-card active';
      card.querySelector('.agent-status-badge').innerText = 'Ensamblando Video';
    } else {
      card.className = 'agent-card active';
      card.querySelector('.agent-status-badge').innerText = 'Procesando Loop';
    }
    
    statusLog.innerText = step.status;
    await new Promise(resolve => setTimeout(resolve, step.delay));
    
    // Marcar como completado
    card.className = 'agent-card completed';
    card.querySelector('.agent-status-badge').innerText = 'Aprobado ✓';
  }

  statusLog.innerText = 'Pipeline DAG completado con éxito. Clase multimedia breve ensamblada y validada por el Agente Revisor.';
  spinner.classList.remove('visible');
  btn.disabled = false;

  // Actualizar contenido si el usuario ingresó un Objetivo de Aprendizaje personalizado
  const customOA = document.getElementById('learningObjective').value;
  const isCustom = !currentPresetKey || (PRESETS[currentPresetKey] && !PRESETS[currentPresetKey].oa.includes(customOA));

  if (customOA && isCustom) {
    const level = document.getElementById('educationLevel').value;
    const duration = document.getElementById('classDuration').value;
    const approach = document.getElementById('pedagogicalApproach').value;
    const context = document.getElementById('courseContext').value || "Aula con proyector y trabajo guiado.";

    const shortTopic = customOA.length > 50 ? customOA.substring(0, 50) + "..." : customOA;

    PRESETS.custom = {
      oa: customOA,
      level: level,
      duration: duration,
      approach: approach,
      context: context,
      pedagogy: `
        <div class="module-card">
          <div class="module-header">
            <div class="module-title"><i class="fa-solid fa-bullseye"></i> Plan Personalizado Didáctico</div>
            <span class="tag-time">${duration}</span>
          </div>
          <p><strong>Objetivo de Aprendizaje Configurado:</strong> ${customOA}</p>
          <p style="margin-top: 6px; font-size: 0.85rem; color: var(--text-muted);"><strong>Metodología Aplicada:</strong> ${approach} | <strong>Nivel:</strong> ${level}</p>
        </div>

        <div class="module-card">
          <div class="module-header">
            <div class="module-title"><i class="fa-solid fa-play"></i> Etapa 1: Inicio / Enganche Didáctico</div>
            <span class="tag-time">5 Minutos</span>
          </div>
          <p><strong>Actividad de Apertura:</strong> Planteamiento de pregunta detonante sobre <em>"${shortTopic}"</em> para activar saberes previos y motivar al estudiante.</p>
        </div>

        <div class="module-card">
          <div class="module-header">
            <div class="module-title"><i class="fa-solid fa-gears"></i> Etapa 2: Desarrollo Conceptual y Aplicación</div>
            <span class="tag-time">10 Minutos</span>
          </div>
          <p><strong>Secuencia didáctica central:</strong> Explicación conceptual interactiva, análisis de ejemplos prácticos y discusión guiada bajo enfoque ${approach}.</p>
        </div>

        <div class="module-card">
          <div class="module-header">
            <div class="module-title"><i class="fa-solid fa-flag-checkered"></i> Etapa 3: Cierre y Metacognición</div>
            <span class="tag-time">5 Minutos</span>
          </div>
          <p><strong>Síntesis y Evaluación:</strong> Preguntas de comprobación rápida y ticket de salida sobre las conclusiones clave alcanzadas.</p>
        </div>
      `,
      theory: `
        <div class="module-card">
          <h3 style="color: var(--primary-navy); margin-bottom: 10px;"><i class="fa-solid fa-atom"></i> Cuerpo Conceptual Principal</h3>
          <p>Desarrollo teórico estructurado por los agentes para abordar el objetivo de aprendizaje: <strong>"${customOA}"</strong>.</p>
        </div>

        <div class="module-card">
          <h4 style="color: var(--primary-indigo); margin-bottom: 8px;"><i class="fa-solid fa-lightbulb"></i> Analogía Explicativa Adaptada (${level})</h4>
          <p>Explicación basada en situaciones de la vida real para facilitar la asimilación del tema por parte de los estudiantes de ${level}.</p>
        </div>

        <div class="module-card">
          <h4 style="color: var(--accent-teal); margin-bottom: 8px;"><i class="fa-solid fa-book"></i> Glosario de Términos Clave</h4>
          <ul>
            <li><strong>Concepto Clave 1:</strong> Definición técnica alineada al tema.</li>
            <li><strong>Concepto Clave 2:</strong> Término fundamental para la evaluación.</li>
          </ul>
        </div>
      `,
      audiovisual: `
        <div class="module-card">
          <h4 style="color: var(--primary-navy); margin-bottom: 10px;"><i class="fa-solid fa-film"></i> Escaleta / Guion de Video Corto</h4>
          <p><strong>Escena 1 (Inicio):</strong> Introducción animada motivadora y presentación del tema principal.</p>
          <p><strong>Escena 2 (Desarrollo):</strong> Explicación visual paso a paso con gráficos y locución adaptada.</p>
          <p><strong>Escena 3 (Cierre):</strong> Conclusión didáctica y llamado a la acción.</p>
        </div>

        <div class="module-card">
          <h4 style="color: var(--primary-indigo); margin-bottom: 10px;"><i class="fa-solid fa-image"></i> Prompt para Infografía (IA Generativa Visual)</h4>
          <pre>"Educational vector infographic explaining: ${customOA}, clean academic layout, high resolution, suitable for ${level} students."</pre>
        </div>
      `
    };
    renderPresetContent(PRESETS.custom);
  }
}

// Toggle de Modo Edición directa
function toggleEditMode() {
  isEditMode = !isEditMode;
  const btn = document.getElementById('btnEditToggle');
  const editableBoxes = document.querySelectorAll('.editable-box');

  editableBoxes.forEach(box => {
    box.contentEditable = isEditMode ? "true" : "false";
  });

  if (isEditMode) {
    btn.style.background = '#dbeafe';
    btn.style.borderColor = 'var(--primary-blue)';
    btn.style.color = 'var(--primary-navy)';
    btn.innerHTML = '<i class="fa-solid fa-check"></i> <span>Guardar Cambios</span>';
  } else {
    btn.style.background = 'var(--bg-card)';
    btn.style.borderColor = 'var(--border-light)';
    btn.style.color = 'var(--text-main)';
    btn.innerHTML = '<i class="fa-solid fa-pen-to-square"></i> <span>Editar Contenido</span>';
  }
}

// Exportar a Markdown
function exportMarkdown() {
  const oa = document.getElementById('learningObjective').value;
  const level = document.getElementById('educationLevel').value;
  const duration = document.getElementById('classDuration').value;

  const pedEl = document.getElementById('content-pedagogy');
  const thEl = document.getElementById('content-theory');
  const avEl = document.getElementById('content-audiovisual');
  const auditEl = document.getElementById('auditChecklist');

  const pedText = pedEl ? pedEl.innerText : '';
  const thText = thEl ? thEl.innerText : '';
  const avText = avEl ? avEl.innerText : '';
  const auditText = auditEl ? auditEl.innerText : '';

  const mdContent = `# Propuesta de Clase Multimedia Breve
**Objetivo de Aprendizaje:** ${oa}
**Nivel Educativo:** ${level} | **Duración:** ${duration}
**Estado Auditoría Agente Revisor:** DAG VALIDADO & APROBADO (Score 94%)

---

## 1. Planificación Didáctica
${pedText}

---

## 2. Guion Teórico y Locución
${thText}

---

## 3. Escaleta Audiovisual y Prompts Visuales
${avText}

---

## 4. Auditoría de Calidad Pedagógica (7 Criterios)
${auditText}
`;

  const blob = new Blob([mdContent], { type: 'text/markdown;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Propuesta_Clase_Breve_${level.replace(/[^a-zA-Z0-9]/g, '_')}.md`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
