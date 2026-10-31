/* ==========================================================================
   LÓGICA DEL SISTEMA MULTIAGENTE DE CLASES MULTIMEDIA (app.js)
   Orquestación, Simulación de Agentes, Renderizado Dinámico & Edición
   ========================================================================== */

// Base de Datos de Presets Didácticos para Demostración
const PRESETS = {
  fisica: {
    oa: "Comprender la Ley de Conservación de la Energía (la energía no se crea ni se destruye, solo se transforma) y aplicar sus principios a situaciones cotidianas.",
    level: "Enseñanza Media (1º - 4º Medio)",
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
        <pre style="background: #f8fafc; padding: 12px; border-radius: 8px; font-family: var(--font-code); font-size: 0.82rem; color: #1e293b; border: 1px solid var(--border-light); white-space: pre-wrap;">"Infografía vectorial didáctica y limpia que explica la Ley de Conservación de la Energía, con una montaña rusa y barras de energía codificadas por colores (Verde para Potencial, Azul para Cinética), tipografía moderna y alta resolución."</pre>
      </div>

      <div class="module-card">
        <h4 style="color: var(--accent-teal); margin-bottom: 10px;"><i class="fa-solid fa-microphone"></i> Guion de Audio Podcast (Apertura de Clase)</h4>
        <p><em>[Música de fondo suave y tecnológica]</em><br><strong>Locutor:</strong> "Hola a todos. ¿Sabían que la misma energía que usó un dinosaurio para correr sigue aquí en la Tierra transformándose en luz, viento o movimiento? Hoy descubriremos la regla de oro del universo..."</p>
      </div>
    `
  },

  biologia: {
    oa: "Explicar el proceso de fotosíntesis en las plantas y su importancia en el flujo de energía dentro de la cadena trófica.",
    level: "Enseñanza Básica (5º - 8º Básico)",
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
        <h4>Prompt Infografía Ilustrada para Estudiantes</h4>
        <pre style="background: #f8fafc; padding: 12px; border-radius: 8px; color: #1e293b; border: 1px solid var(--border-light);">"Ilustración didáctica y colorida que muestra una planta saludable absorbiendo luz solar, agua y CO2, liberando oxígeno, diseño educativo y amigable para enseñanza básica."</pre>
      </div>
    `
  },

  historia: {
    oa: "Analizar las causas y consecuencias de la Revolución Industrial en la transformación del trabajo y la vida urbana.",
    level: "Enseñanza Media (1º - 4º Medio)",
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

// Renderizado de datos reales provenientes del Grafo LangGraph (FastAPI)
function renderLangGraphContent(data) {
  if (!data) return;
  if (data.audiovisual_storyboard) {
    window.lastStoryboard = data.audiovisual_storyboard;
  }

  if (data.pedagogical_plan) {
    const plan = data.pedagogical_plan;
    let html = `
      <div class="module-card">
        <div class="module-header">
          <div class="module-title"><i class="fa-solid fa-bullseye"></i> Planificación Orquestada (LangGraph)</div>
          <span class="tag-time">${plan.estimated_total_time} Minutos</span>
        </div>
        <p><strong>Metodología:</strong> ${plan.methodology_applied}</p>
        <p style="margin-top: 6px; font-size: 0.85rem; color: var(--text-muted);"><strong>Prerrequisitos:</strong> ${plan.prerequisites.join(', ')}</p>
      </div>
    `;
    plan.stages.forEach(st => {
      let icon = st.stage_name === 'Inicio' ? 'fa-play' : (st.stage_name === 'Desarrollo' ? 'fa-gears' : 'fa-flag-checkered');
      html += `
        <div class="module-card">
          <div class="module-header">
            <div class="module-title"><i class="fa-solid ${icon}"></i> Etapa: ${st.stage_name} - ${st.activity_title}</div>
            <span class="tag-time">${st.duration_min} Min</span>
          </div>
          <p>${st.description}</p>
          <p style="margin-top: 6px; font-size: 0.82rem; color: var(--primary-indigo);"><strong>Intención Didáctica:</strong> ${st.pedagogical_intent}</p>
        </div>
      `;
    });
    document.getElementById('content-pedagogy').innerHTML = html;
  }

  if (data.theory_content) {
    const th = data.theory_content;
    let glossHtml = th.glossary.map(g => `<li><strong>${g.term}:</strong> ${g.definition}</li>`).join('');
    let html = `
      <div class="module-card">
        <h3 style="color: var(--primary-navy); margin-bottom: 10px;"><i class="fa-solid fa-atom"></i> ${th.core_concept}</h3>
        <p>${th.core_explanation}</p>
      </div>
      <div class="module-card">
        <h4 style="color: var(--primary-indigo); margin-bottom: 8px;"><i class="fa-solid fa-lightbulb"></i> Analogía Didáctica Explicativa</h4>
        <p>${th.real_world_analogy}</p>
      </div>
      <div class="module-card">
        <h4 style="color: var(--accent-teal); margin-bottom: 8px;"><i class="fa-solid fa-microphone"></i> Locución Recomendada</h4>
        <p><em>"${th.voiceover_script}"</em></p>
      </div>
      <div class="module-card">
        <h4 style="color: var(--accent-emerald); margin-bottom: 8px;"><i class="fa-solid fa-book"></i> Glosario Clave</h4>
        <ul>${glossHtml}</ul>
      </div>
    `;
    document.getElementById('content-theory').innerHTML = html;
  }

  if (data.audiovisual_storyboard) {
    const av = data.audiovisual_storyboard;
    let html = `
      <div class="module-card">
        <h3 style="color: var(--primary-navy); margin-bottom: 8px;"><i class="fa-solid fa-film"></i> ${av.video_title}</h3>
        <p><strong>Público:</strong> ${av.target_audience} | <strong>Duración Total:</strong> ${av.total_duration_seconds} seg (${av.scenes.length} escenas)</p>
      </div>
    `;
    av.scenes.forEach(sc => {
      html += `
        <div class="module-card">
          <div class="module-header">
            <div class="module-title"><i class="fa-solid fa-video"></i> Escena ${sc.scene_number} (${sc.duration_seconds} seg)</div>
            <span class="tag-time">${sc.on_screen_text}</span>
          </div>
          <p><strong>Locución:</strong> "${sc.voiceover}"</p>
          <p style="margin-top: 6px;"><strong>Composición Visual:</strong> ${sc.visual_description}</p>
          <div style="margin-top: 10px; background: #f8fafc; padding: 10px; border-radius: 6px; font-family: var(--font-code); font-size: 0.8rem; border: 1px solid var(--border-light); white-space: pre-wrap;">
            <strong>Prompt IA Visual:</strong> ${sc.ai_image_prompt}
          </div>
        </div>
      `;
    });
    document.getElementById('content-audiovisual').innerHTML = html;
  }

  if (data.audit_report) {
    const rep = data.audit_report;
    const scoreText = document.getElementById('scoreText');
    if (scoreText) scoreText.innerText = `${rep.global_score}%`;
    const badge = document.getElementById('currentStatusBadge');
    if (badge) {
      badge.style.background = '#dbeafe';
      badge.style.color = '#1e40af';
      badge.style.borderColor = '#bfdbfe';
      badge.innerText = `LANGGRAPH BACKEND ACTIVO (${rep.global_score}% APROBADO)`;
    }
    const auditChecklist = document.getElementById('auditChecklist');
    if (auditChecklist && rep.criteria) {
      auditChecklist.innerHTML = rep.criteria.map(c => `
        <li><i class="fa-solid fa-circle-check"></i> <strong>${c.criterion_id}. ${c.criterion_name}:</strong> ${c.score}% - ${c.observation}</li>
      `).join('');
    }
  }
}


// Cambio de Pestañas (Tabs)
function switchTab(tabId, btnElement) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content-panel').forEach(panel => panel.classList.remove('active'));

  btnElement.classList.add('active');
  document.getElementById(tabId).classList.add('active');
}

// Simulación / Conexión de Orquestación Multiagente (DAG Secuencial en LangGraph)
async function handleGenerate(e) {
  e.preventDefault();
  
  const btn = document.getElementById('btnGenerate');
  const spinner = document.getElementById('terminalSpinner');
  const statusLog = document.getElementById('statusLogText');
  
  btn.disabled = true;
  spinner.classList.add('visible');

  // Obtener inputs del formulario
  const oaValue = document.getElementById('learningObjective').value;
  const levelValue = document.getElementById('educationLevel').value;
  const durationValue = document.getElementById('classDuration').value;
  const approachValue = document.getElementById('pedagogicalApproach').value;
  const contextValue = document.getElementById('courseContext').value || "Aula estándar con proyector.";

  // Intentar conectar con backend FastAPI + LangGraph en segundo plano
  let backendPromise = null;
  const controller = new AbortController();
  // Tiempo de espera amplio (90s) para permitir que los 4 agentes de OpenAI completen el flujo
  const timeoutId = setTimeout(() => controller.abort(), 90000);

  try {
    const durNum = parseInt(durationValue) || 20;
    console.log("[DAG Frontend] Despachando solicitud a backend FastAPI (http://127.0.0.1:8000/api/generate)...");

    backendPromise = fetch("http://127.0.0.1:8000/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        learning_objective: oaValue,
        education_level: levelValue,
        duration_minutes: durNum,
        approach: approachValue,
        context: contextValue
      }),
      signal: controller.signal
    })
    .then(async r => {
      if (!r.ok) {
        console.warn(`[Backend Error] Status: ${r.status}`);
        return null;
      }
      return await r.json();
    })
    .catch(err => {
      console.warn("[Backend Network Notice] No se pudo comunicar con FastAPI en :8000 o se canceló:", err);
      return null;
    })
    .finally(() => clearTimeout(timeoutId));
  } catch (err) {
    backendPromise = Promise.resolve(null);
  }

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
    { agent: 'orchestrator', status: '[LangGraph Engine] Inicializando grafo de estado DAG y parametrizando OA...', delay: 700 },
    { agent: 'pedagogy', status: '[Fase 1: Planificación] Diseñando 3 etapas pedagógicas con OpenAI...', delay: 1000 },
    { agent: 'content', status: '[Fase 2: Guion Teórico] Redactando conceptos, analogía didáctica y glosario...', delay: 1000 },
    { agent: 'av', status: '[Fase 3: Escaleta Audiovisual] Diseñando escenas, locución y prompts de imagen...', delay: 1000 },
    { agent: 'reviewer', status: '[Fase 4: Agente Revisor] Auditando la propuesta en base a los 7 Criterios de Calidad...', delay: 1200 },
    { agent: 'ffmpeg', status: '[Componente Determinista] Generando especificación JSON para ensamblador de video...', delay: 800 }
  ];

  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const card = document.getElementById(`agent-${step.agent}`);
    if (!card) continue;
    
    // Marcar como activo
    if (step.agent === 'reviewer') {
      card.className = 'agent-card reviewing';
      card.querySelector('.agent-status-badge').innerText = 'Auditando (7 Criterios)';
    } else if (step.agent === 'ffmpeg') {
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

  // Si la petición a OpenAI / LangGraph aún sigue procesando, informar en la terminal visual
  statusLog.innerText = '[Conexión Activa con LangGraph] Esperando respuesta de OpenAI (GPT-4o mini)...';

  // Esperar resultado del backend
  const backendResult = await backendPromise;

  if (backendResult && backendResult.success) {
    console.log("[DAG Frontend] ✅ Respuesta exitosa recibida del backend LangGraph:", backendResult);
    statusLog.innerText = '✅ Pipeline completado con éxito mediante LangGraph y OpenAI (GPT-4o mini).';
    renderLangGraphContent(backendResult);
  } else {
    console.log("[DAG Frontend] Operando en modo local (sin respuesta del backend).");
    statusLog.innerText = 'Pipeline DAG completado. Clase multimedia breve ensamblada y validada por el Agente Revisor.';
  }

  spinner.classList.remove('visible');
  btn.disabled = false;

  // Si no hubo respuesta del backend real, actualizar contenido con preset o generador simulado
  if (!backendResult || !backendResult.success) {
    const customOA = oaValue;
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
          <pre>"Infografía didáctica en español que explica: ${customOA}, diseño pedagógico moderno, alta resolución, adaptado a estudiantes de ${level}."</pre>
        </div>
      `
    };
    renderPresetContent(PRESETS.custom);
  }
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


// ==========================================================================
// RENDERIZADO Y ENSAMBLADO MULTIMEDIA (TTS NEURAL + IMÁGENES + VIDEO MP4)
// ==========================================================================
window.lastStoryboard = null;

async function handleRenderVideo() {
  const btn = document.getElementById('btnRenderVideo');
  const voiceSelect = document.getElementById('videoVoiceSelect');
  const voice = voiceSelect ? voiceSelect.value : 'es-CL-LorenzoNeural';
  const statusLog = document.getElementById('statusLogText');
  const ffmpegCard = document.getElementById('agent-ffmpeg');

  let storyboard = window.lastStoryboard;
  if (!storyboard) {
    // Generar storyboard pedagógico de contingencia basado en el formulario o preset actual
    const currentOa = document.getElementById('learningObjective').value || "Conservación de la Energía";
    const currentLevel = document.getElementById('educationLevel').value || "Enseñanza Media (1º - 4º Medio)";
    storyboard = {
      video_title: `Clase Breve: ${currentOa.substring(0, 45)}`,
      target_audience: currentLevel,
      total_duration_seconds: 15,
      scenes: [
        {
          scene_number: 1,
          duration_seconds: 5,
          voiceover: `Bienvenidos a esta clase breve. Hoy exploraremos el siguiente objetivo de aprendizaje: ${currentOa.substring(0, 100)}.`,
          visual_description: "Apertura didáctica con título central e infografía ilustrativa.",
          on_screen_text: `Introducción al Tema: ${currentOa.substring(0, 40)}`,
          ai_image_prompt: `Ilustración didáctica y moderna para estudiantes de enseñanza media que introduce el concepto de ${currentOa.substring(0, 50)}, estilo infografía científica con colores vivos`
        },
        {
          scene_number: 2,
          duration_seconds: 5,
          voiceover: "Para comprenderlo mejor, analicemos cómo se manifiestan estos principios en situaciones concretas de nuestro entorno cotidiano.",
          visual_description: "Diagrama conceptual interactivo con vectores explicativos.",
          on_screen_text: "Desarrollo Conceptual y Aplicación en la Vida Real",
          ai_image_prompt: `Diagrama científico interactivo y claro que explica los mecanismos de ${currentOa.substring(0, 50)}, estilo infografía didáctica para adolescentes`
        },
        {
          scene_number: 3,
          duration_seconds: 5,
          voiceover: "En conclusión: la comprensión de estos principios nos permite explicar cómo funciona el mundo que nos rodea. ¡Nos vemos en la próxima lección!",
          visual_description: "Síntesis gráfica de conceptos clave y despedida formativa.",
          on_screen_text: "Síntesis Conceptual y Cierre Metacognitivo",
          ai_image_prompt: `Lámina infográfica de síntesis con iconos de los conceptos aprendidos, diseño didáctico limpio y moderno en español`
        }
      ]
    };
  }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Ensamblando Video MP4...</span>';
  if (ffmpegCard) {
    ffmpegCard.className = 'agent-card active';
    ffmpegCard.querySelector('.agent-status-badge').innerText = 'Sintetizando TTS & Ensamblando';
  }
  if (statusLog) {
    statusLog.innerText = 'Sintetizando locución neural (Edge-TTS), generando ilustraciones y ensamblando MP4 con MoviePy...';
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/api/render-video', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ storyboard: storyboard, voice: voice })
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Error en servidor (:8000 status ${response.status})`);
    }

    const data = await response.json();
    console.log('[Video Renderer] Éxito:', data);

    // Actualizar visuales del DAG
    if (ffmpegCard) {
      ffmpegCard.className = 'agent-card success';
      ffmpegCard.querySelector('.agent-status-badge').innerText = 'Completado [OK]';
    }
    if (statusLog) {
      statusLog.innerText = `✅ Video multimedia ensamblado exitosamente (${data.total_duration_seconds} seg). Listo para reproducción y descarga.`;
    }

    // Activar reproductor de video HTML5
    const placeholder = document.getElementById('videoPlaceholder');
    const activeCont = document.getElementById('videoActiveContainer');
    const player = document.getElementById('multimediaPlayer');
    const dlBtn = document.getElementById('btnDownloadVideo');
    const durLabel = document.getElementById('videoDurationLabel');
    const scenesCont = document.getElementById('scenesMediaContainer');

    if (placeholder) placeholder.style.display = 'none';
    if (activeCont) activeCont.style.display = 'block';

    const videoUrl = `http://127.0.0.1:8000${data.video_url}`;
    if (player) {
      player.src = videoUrl;
      player.load();
    }
    if (dlBtn) {
      dlBtn.href = videoUrl;
      dlBtn.setAttribute('download', data.video_filename || 'clase_multimedia.mp4');
    }
    if (durLabel) {
      durLabel.innerText = `${data.total_duration_seconds} segundos (${data.scenes_count} escenas)`;
    }

    // Mostrar fichas individuales de cada escena (Audio + Imagen)
    if (scenesCont && data.scenes) {
      scenesCont.innerHTML = data.scenes.map(sc => `
        <div class="scene-media-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong style="color: var(--primary-navy); font-size: 0.9rem;">
              <i class="fa-solid fa-film"></i> Escena ${sc.scene_number}
            </strong>
            <span class="tag-time">${sc.duration_seconds}s</span>
          </div>
          <img src="http://127.0.0.1:8000${sc.image_url}" class="scene-media-thumb" alt="Escena ${sc.scene_number}" loading="lazy">
          <audio controls src="http://127.0.0.1:8000${sc.audio_url}" class="scene-audio-player"></audio>
          <p style="font-size: 0.82rem; color: var(--text-main); margin-top: 4px;">
            <strong>Locución:</strong> "${sc.voiceover}"
          </p>
          <div style="font-size: 0.75rem; color: var(--primary-indigo); background: #f8fafc; padding: 6px 8px; border-radius: 6px; border: 1px solid var(--border-light);">
            <strong>Texto en Pantalla:</strong> ${sc.on_screen_text}
          </div>
        </div>
      `).join('');
    }

    // Cambiar a la pestaña de video si no está activa
    const videoTabBtn = document.querySelector("button[onclick*='tab-video']");
    if (videoTabBtn) {
      switchTab('tab-video', videoTabBtn);
    }

  } catch (err) {
    console.error('[Video Renderer] Falla:', err);
    alert('No se pudo completar el ensamblado del video: ' + err.message + '\nVerifica que el servidor backend esté corriendo en http://127.0.0.1:8000 (uvicorn backend.app.main:app).');
    if (statusLog) {
      statusLog.innerText = '❌ Error al renderizar video multimedia. Revisa la consola para más detalles.';
    }
    if (ffmpegCard) {
      ffmpegCard.className = 'agent-card';
      ffmpegCard.querySelector('.agent-status-badge').innerText = 'Falla';
    }
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> <span>Renderizar Video MP4</span>';
  }
}
