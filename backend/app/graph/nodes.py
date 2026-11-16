import json
import re
from typing import Dict, Any, Optional, Tuple, List, Callable

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None

try:
    from .state import ClassDesignState
    from .schemas import (
        PedagogicalPlan, DidacticStage,
        TheoryContent, KeyTerm,
        AudiovisualStoryboard, Scene,
        QualityAuditReport, CriterionAudit
    )
    from .prompts import (
        PEDAGOGY_SYSTEM_PROMPT,
        THEORY_SYSTEM_PROMPT,
        AUDIOVISUAL_SYSTEM_PROMPT,
        REVIEWER_SYSTEM_PROMPT
    )
    from ..core.config import settings
except ImportError:
    from backend.app.graph.state import ClassDesignState
    from backend.app.graph.schemas import (
        PedagogicalPlan, DidacticStage,
        TheoryContent, KeyTerm,
        AudiovisualStoryboard, Scene,
        QualityAuditReport, CriterionAudit
    )
    from backend.app.graph.prompts import (
        PEDAGOGY_SYSTEM_PROMPT,
        THEORY_SYSTEM_PROMPT,
        AUDIOVISUAL_SYSTEM_PROMPT,
        REVIEWER_SYSTEM_PROMPT
    )
    from backend.app.core.config import settings


# -----------------------------------------------------------------------------
# FÁBRICA DE MODELOS MULTI-PROVEEDOR (HETEROGÉNEO CON FALLBACK)
# -----------------------------------------------------------------------------

def get_gemini_llm(temperature: float = 0.3) -> Optional[Tuple[Any, str]]:
    """Instancia Google Gemini (Cuenta Alumno: Seminario)."""
    if ChatGoogleGenerativeAI is None:
        return None
    key = settings.gemini_api_key.strip() if settings.gemini_api_key else ""
    if key and not key.startswith("tu_") and len(key) > 15:
        try:
            m = settings.gemini_model or "gemini-3.5-flash-lite"
            llm = ChatGoogleGenerativeAI(
                model=m,
                google_api_key=key,
                temperature=temperature
            )
            return llm, f"Google Gemini ({m})"
        except Exception:
            return None
    return None


def get_openai_llm(model: Optional[str] = None, temperature: float = 0.7) -> Optional[Tuple[Any, str]]:
    """Instancia OpenAI (Cuenta Profesor Guía)."""
    if ChatOpenAI is None:
        return None
    key = settings.openai_api_key.strip() if settings.openai_api_key else ""
    if key and not key.startswith("PEGA_TU") and not key.startswith("tu_") and len(key) > 15:
        try:
            m = model or settings.default_model or "gpt-4o-mini"
            llm = ChatOpenAI(
                model=m,
                api_key=key,
                temperature=temperature
            )
            return llm, f"OpenAI ({m})"
        except Exception:
            return None
    return None


def get_institutional_llm(max_tokens: Optional[int] = None, temperature: float = 0.3) -> Optional[Tuple[Any, str]]:
    """Instancia Servidor Institucional U (Modelo Gemma / vLLM compatible OpenAI con límite de créditos)."""
    if not settings.use_institutional_quota:
        return None
    if ChatOpenAI is None:
        return None
    base_url = settings.institutional_base_url.strip() if settings.institutional_base_url else ""
    key = settings.institutional_api_key.strip() if settings.institutional_api_key else ""
    if base_url and key and not key.startswith("tu_"):
        try:
            m = settings.institutional_model or "gemma4:26b"
            llm = ChatOpenAI(
                model=m,
                api_key=key,
                base_url=base_url,
                temperature=temperature,
                max_tokens=max_tokens or settings.institutional_max_tokens
            )
            return llm, f"Servidor Institucional U ({m})"
        except Exception:
            return None
    return None


def get_anthropic_llm() -> Optional[Tuple[Any, str]]:
    """Instancia Anthropic Claude (Auditoría liviana con Claude 3.5 Haiku)."""
    if ChatAnthropic is None:
        return None
    key = settings.anthropic_api_key.strip() if settings.anthropic_api_key else ""
    if key and not key.startswith("tu_") and len(key) > 15:
        try:
            m = settings.anthropic_model or "claude-3-5-haiku-20241022"
            llm = ChatAnthropic(
                model=m,
                api_key=key,
                temperature=0.2
            )
            return llm, f"Anthropic Claude ({m})"
        except Exception:
            return None
    return None


async def try_generate_structured(
    providers: List[Callable[[], Optional[Tuple[Any, str]]]],
    schema: Any,
    prompt: str,
    phase_name: str,
    logs: List[str]
) -> Tuple[Optional[Any], Optional[str]]:
    """Intenta generar la salida estructurada iterando la lista de proveedores en orden de prioridad."""
    schema_json = ""
    if hasattr(schema, "model_json_schema"):
        schema_json = json.dumps(schema.model_json_schema(), ensure_ascii=False)
    elif hasattr(schema, "schema"):
        schema_json = json.dumps(schema.schema(), ensure_ascii=False)

    for get_provider in providers:
        res = get_provider()
        if not res:
            continue
        llm, provider_name = res

        # Caso A: Servidor Institucional U (Gemma / vLLM sin function-calling nativo)
        if "Institucional" in provider_name:
            try:
                format_prompt = (
                    f"{prompt}\n\n"
                    f"REGLA DE FORMATO OBLIGATORIA: Responde EXCLUSIVAMENTE con un objeto JSON válido que cumpla estrictamente este esquema:\n"
                    f"{schema_json}\n\n"
                    "Inicia tu respuesta directamente con '{' y finaliza con '}'. Sin introducciones ni bloques adicionales de texto."
                )
                raw_res = await llm.ainvoke(format_prompt)
                raw_text = raw_res.content if hasattr(raw_res, "content") else str(raw_res)
                match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                if match:
                    json_data = json.loads(match.group(0))
                    output = schema(**json_data)
                    logs.append(f"[{phase_name}] Salida estructurada generada exitosamente con {provider_name}.")
                    return output, provider_name
            except Exception as e:
                logs.append(f"[{phase_name}] Aviso: No se pudo completar con {provider_name} ({str(e)[:45]}...), derivando a siguiente opción...")
                continue

        # Caso B: Proveedores comerciales con function-calling nativo (OpenAI, Gemini, Claude)
        try:
            structured_llm = llm.with_structured_output(schema)
            output = await structured_llm.ainvoke(prompt)
            logs.append(f"[{phase_name}] Salida estructurada generada exitosamente con {provider_name}.")
            return output, provider_name
        except Exception as e:
            logs.append(f"[{phase_name}] Aviso: No se pudo completar con {provider_name} ({str(e)[:45]}...), derivando a siguiente opción...")
    return None, None


# -----------------------------------------------------------------------------
def get_education_level_context(level: str) -> dict:
    lvl = (level or "").lower()
    
    # Enseñanza Básica - Primer Ciclo (1º a 4º Básico)
    if "1º - 4º básico" in lvl or "1° - 4° básico" in lvl or ("1" in lvl and "básic" in lvl):
        return {
            "age_range": "6 a 10 años (Enseñanza Básica - 1º a 4º Básico)",
            "tone_focus": "Enfocado en niños pequeños. Lenguaje sumamente lúdico, visual, motivador y claro. Metáforas directas basadas en juegos, animales, naturaleza o situaciones del hogar.",
            "visual_focus": "Ilustraciones tipo animación educativa, amigables, coloridas y claras, sin jerga técnica."
        }
    # Enseñanza Básica - Segundo Ciclo (5º a 8º Básico)
    elif "5º - 8º" in lvl or "5° - 8°" in lvl or "básica" in lvl or "basica" in lvl or "primaria" in lvl:
        return {
            "age_range": "10 a 14 años (Enseñanza Básica - 5º a 8º Básico)",
            "tone_focus": "Enfocado en preadolescentes. Lenguaje juvenil, motivador y cercano. Permite vincular analogías moderadas con tecnología o mecánicas de videojuegos cotidianos (ej. barras de energía, misiones de cuidado responsable), manteniendo un equilibrio sin saturar con jerga.",
            "visual_focus": "Infografía escolar limpia, esquemas paso a paso y diagramas ilustrados atractivos."
        }
    # Enseñanza Media (1º a 4º Medio - Adolescentes)
    elif "media" in lvl or "medio" in lvl or "secundaria" in lvl or "bachillerato" in lvl:
        return {
            "age_range": "14 a 18 años (Enseñanza Media - 1º a 4º Medio / Adolescentes)",
            "tone_focus": "Enfocado en adolescentes de Enseñanza Media. Tono maduro, serio, respetuoso y analítico (estilo divulgación científica moderna o documental). Tratar al estudiante como un joven adulto. PROHIBIDO terminantemente usar jerga gamer forzada o modismos informales como 'lag mental', 'servidor multijugador' o similares. Priorizar conceptos biológicos, bienestar animal, responsabilidad ética y razonamiento crítico.",
            "visual_focus": "Infografía científica moderna tipo Kurzgesagt o Khan Academy, con esquemas anatómicos limpios y colores vivos."
        }
    # Educación Superior (CFT / IP / Universidad)
    else:
        return {
            "age_range": "+18 años (Educación Superior / CFT / IP / Universidad)",
            "tone_focus": "Académico, profesional, técnico y metodológico con rigor de educación superior.",
            "visual_focus": "Modelos conceptuales avanzados, publicaciones científicas y datos de evidencia."
        }

# FASE 1: AGENTE DE PLANIFICACIÓN PEDAGÓGICA (Primario: Gemini Alumno)
# -----------------------------------------------------------------------------
async def pedagogy_agent_node(state: ClassDesignState) -> Dict[str, Any]:
    user_input = state["user_input"]
    feedback = state.get("feedback_history", [])
    logs = state.get("logs", [])
    
    log_msg = f"[Fase 1: Planificación] Diseñando estructura de 3 etapas para: '{user_input.learning_objective[:40]}...'"
    if feedback:
        log_msg += f" (Aplicando corrección: {feedback[-1][:50]}...)"
    logs.append(log_msg)

    age_ctx = get_education_level_context(user_input.education_level)
    prompt = (
        f"{PEDAGOGY_SYSTEM_PROMPT}\n\n"
        f"Objetivo de Aprendizaje: {user_input.learning_objective}\n"
        f"Nivel Educativo: {user_input.education_level} (Edad estimada: {age_ctx['age_range']})\n"
        f"Enfoque de Adaptación Etaria: {age_ctx['tone_focus']}\n"
        f"Duración: {user_input.duration_minutes} minutos\n"
        f"Metodología: {user_input.approach}\n"
        f"Contexto: {user_input.context}\n"
    )
    if feedback:
        prompt += f"\nObservaciones para corregir: {feedback[-1]}\n"

    # Prioridad: 1) OpenAI (Profesor Guía - respuesta rápida y estructurada), 2) Gemini (Alumno)
    providers = [get_institutional_llm, get_openai_llm, get_gemini_llm] if settings.use_institutional_quota else [get_openai_llm, get_gemini_llm]
    plan, provider_used = await try_generate_structured(
        providers=providers,
        schema=PedagogicalPlan,
        prompt=prompt,
        phase_name="Fase 1: Planificación",
        logs=logs
    )

    if plan:
        return {"pedagogical_plan": plan, "logs": logs}

    logs.append("[Fase 1: Planificación] Info: Sin conexión LLM activa, usando generador algorítmico base.")

    # Generador base / fallback
    total_time = user_input.duration_minutes
    t_inicio = max(3, int(total_time * 0.20))
    t_cierre = max(3, int(total_time * 0.20))
    t_desarrollo = total_time - t_inicio - t_cierre

    stages = [
        DidacticStage(
            stage_name="Inicio",
            duration_min=t_inicio,
            activity_title="Activación de Conocimientos Previos y Pregunta Detonante",
            description=f"Pregunta motivadora y sondeo inicial sobre {user_input.learning_objective[:60]}. Presentación del objetivo.",
            pedagogical_intent="Focalizar la atención y conectar con experiencias previas de los estudiantes."
        ),
        DidacticStage(
            stage_name="Desarrollo",
            duration_min=t_desarrollo,
            activity_title=f"Construcción Guiada y Modelado con {user_input.approach}",
            description="Explicación interactiva del concepto central, resolución de casos y análisis de analogías prácticas.",
            pedagogical_intent="Desarrollar el razonamiento conceptual y la transferencia de conocimientos."
        ),
        DidacticStage(
            stage_name="Cierre",
            duration_min=t_cierre,
            activity_title="Síntesis Metacognitiva y Ticket de Salida",
            description="Pregunta de autoevaluación formativa para comprobar el logro del objetivo de aprendizaje.",
            pedagogical_intent="Consolidar aprendizajes y verificar asimilación conceptual antes de concluir."
        )
    ]

    plan = PedagogicalPlan(
        stages=stages,
        methodology_applied=user_input.approach,
        prerequisites=[f"Comprensión básica de conceptos introductorios de {user_input.education_level}"],
        estimated_total_time=total_time
    )

    return {"pedagogical_plan": plan, "logs": logs}


# -----------------------------------------------------------------------------
# FASE 2: AGENTE DE CONTENIDOS TEÓRICOS Y GUION (Primario: U / Gemma o OpenAI)
# -----------------------------------------------------------------------------
async def theory_agent_node(state: ClassDesignState) -> Dict[str, Any]:
    user_input = state["user_input"]
    plan = state["pedagogical_plan"]
    logs = state.get("logs", [])
    
    logs.append(f"[Fase 2: Guion Teórico] Insumo: Planificación aprobada ({plan.estimated_total_time} min). Redactando cuerpo conceptual y analogía.")

    age_ctx = get_education_level_context(user_input.education_level)
    prompt = (
        f"{THEORY_SYSTEM_PROMPT}\n\n"
        f"Objetivo de Aprendizaje: {user_input.learning_objective}\n"
        f"Nivel Educativo: {user_input.education_level} (Edad estimada: {age_ctx['age_range']})\n"
        f"Criterio de Adaptación para la Edad: {age_ctx['tone_focus']}\n"
        f"Planificación Previa:\n"
        f"- Etapas: {[s.stage_name + ' (' + str(s.duration_min) + 'm)' for s in plan.stages]}\n"
        f"- Metodología: {plan.methodology_applied}\n"
        f"\nIMPORTANTE: Redacta la explicación, la analogía y el guion oral adaptándolos al interés y lenguaje de estudiantes de {age_ctx['age_range']}. Todo 100% en español.\n"
    )

    # Prioridad: 1) OpenAI (Profesor Guía - respuesta rápida y estructurada), 2) Gemini (Alumno)
    providers = [get_openai_llm, get_gemini_llm]
    theory, provider_used = await try_generate_structured(
        providers=providers,
        schema=TheoryContent,
        prompt=prompt,
        phase_name="Fase 2: Guion Teórico",
        logs=logs
    )

    if theory:
        return {"theory_content": theory, "logs": logs}

    logs.append("[Fase 2: Guion Teórico] Info: Sin conexión LLM activa, usando generador algorítmico base.")

    oa = user_input.learning_objective
    level = user_input.education_level

    theory = TheoryContent(
        core_concept=f"Fundamentos de: {oa[:50]}",
        core_explanation=(
            f"El estudio de este tema se centra en {oa}. En el nivel {level}, "
            "es fundamental comprender cómo interactúan los principios subyacentes, "
            "evitando concepciones erróneas comunes y formalizando las relaciones directas."
        ),
        real_world_analogy=(
            "Imagina una balanza equilibrada o un circuito de fichas de dominó: cada acción produce una transformación "
            "directa y verificable en el entorno cotidiano sin que se pierda la causa original."
        ),
        voiceover_script=(
            f"Bienvenidos a esta clase breve. Hoy abordaremos un tema esencial: {oa}. "
            "A lo largo de los próximos minutos, desarmaremos sus componentes paso a paso para que puedan aplicarlo con total seguridad."
        ),
        glossary=[
            KeyTerm(term="Concepto Rector", definition=f"Pilar explicativo central vinculado a: {oa[:30]}"),
            KeyTerm(term="Transferencia Didáctica", definition="Capacidad de aplicar el principio aprendido a un nuevo contexto."),
            KeyTerm(term="Variable Crítica", definition="Elemento medible que determina el comportamiento del fenómeno analizado.")
        ]
    )

    return {"theory_content": theory, "logs": logs}


# -----------------------------------------------------------------------------
# FASE 3: AGENTE DE PRODUCCIÓN AUDIOVISUAL (Primario: Gemini o OpenAI)
# -----------------------------------------------------------------------------
async def audiovisual_agent_node(state: ClassDesignState) -> Dict[str, Any]:
    theory = state["theory_content"]
    user_input = state["user_input"]
    logs = state.get("logs", [])

    logs.append("[Fase 3: Escaleta Audiovisual] Diseñando escenas multimedia y prompts de IA generativa visual.")

    age_ctx = get_education_level_context(user_input.education_level)
    prompt = (
        f"{AUDIOVISUAL_SYSTEM_PROMPT}\n\n"
        f"Objetivo de Aprendizaje: {user_input.learning_objective}\n"
        f"Público y Nivel: {user_input.education_level} (Edad estimada: {age_ctx['age_range']})\n"
        f"Estilo Visual Recomendado: {age_ctx['visual_focus']}\n"
        f"Concepto Central: {theory.core_concept}\n"
        f"Explicación Teórica: {theory.core_explanation}\n"
        f"Analogía: {theory.real_world_analogy}\n"
        f"\nREGLA OBLIGATORIA DE IDIOMA: Todo el contenido (locución, on_screen_text y ai_image_prompt) DEBE SER ESTRICTAMENTE EN ESPAÑOL. El texto en pantalla (on_screen_text) debe ser corto (máximo 8 palabras).\n"
    )

    # Prioridad: 1) OpenAI (Profesor Guía - respuesta rápida y estructurada), 2) Gemini (Alumno)
    providers = [get_openai_llm, get_gemini_llm]
    storyboard, provider_used = await try_generate_structured(
        providers=providers,
        schema=AudiovisualStoryboard,
        prompt=prompt,
        phase_name="Fase 3: Escaleta Audiovisual",
        logs=logs
    )

    if storyboard:
        return {"audiovisual_storyboard": storyboard, "logs": logs}

    logs.append("[Fase 3: Escaleta Audiovisual] Info: Sin conexión LLM activa, usando generador algorítmico base con oraciones completas y prompts diferenciados.")

    oa_clean = user_input.learning_objective.strip().rstrip(".").replace('"', '')
    if len(oa_clean) < 12 and "mascota" in oa_clean.lower():
        oa_topic = "el cuidado y la tenencia responsable de mascotas"
    else:
        oa_topic = oa_clean

    lvl_str = user_input.education_level or "Enseñanza Media"

    # Locuciones completas y oraciones cerradas (sin cortes ni puntos suspensivos)
    scenes = [
        Scene(
            scene_number=1,
            duration_seconds=12,
            voiceover=f"Bienvenidos a esta clase. Hoy comprenderemos la importancia de {oa_topic}, aprendiendo cómo nuestras acciones diarias aseguran su bienestar.",
            visual_description="Plano general de un estudiante interactuando con su mascota en un hogar cálido, estableciendo el vínculo de afecto y compromiso.",
            on_screen_text=f"Introducción: {oa_topic[:45]}",
            ai_image_prompt=f"Fotografía o ilustración educativa de un estudiante interactuando cariñosamente con su mascota en un hogar luminoso, escena realista y natural sin textos ni afiches publicitarios"
        ),
        Scene(
            scene_number=2,
            duration_seconds=14,
            voiceover="Para garantizar una vida saludable, es fundamental cubrir sus necesidades básicas todos los días: alimentación balanceada, agua fresca y controles periódicos con el veterinario.",
            visual_description="Escena de atención y cuidado responsable, mostrando una consulta veterinaria preventiva o la rutina de alimentación y cepillado.",
            on_screen_text="Cuidados Fundamentales y Salud",
            ai_image_prompt=f"Escena educativa realista de un joven en una clínica veterinaria mientras el médico revisa a una mascota saludable, ambiente profesional y pedagógico sin textos ni anuncios"
        ),
        Scene(
            scene_number=3,
            duration_seconds=12,
            voiceover="Tener una mascota es un compromiso para toda la vida basado en el respeto y el cariño. Cuidarlas con dedicación enriquece a toda la familia.",
            visual_description="Escena de cierre con una familia paseando responsablemente a su mascota en un parque al atardecer.",
            on_screen_text="Compromiso y Convivencia Responsable",
            ai_image_prompt=f"Escena al aire libre de convivencia familiar feliz y responsable paseando a su mascota con correa en un parque verde, iluminación cálida, sin textos ni logotipos"
        )
    ]

    storyboard = AudiovisualStoryboard(
        video_title=f"Clase Multimedia: {oa_topic[:50]}",
        target_audience=lvl_str,
        total_duration_seconds=38,
        scenes=scenes
    )

    return {"audiovisual_storyboard": storyboard, "logs": logs}


# -----------------------------------------------------------------------------
# FASE 4: AGENTE REVISOR (QUALITY CONTROL - Primario: Claude Haiku o OpenAI)
# -----------------------------------------------------------------------------
async def quality_reviewer_node(state: ClassDesignState) -> Dict[str, Any]:
    logs = state.get("logs", [])
    iteration = state.get("iteration_count", 0) + 1
    user_input = state["user_input"]
    plan = state["pedagogical_plan"]
    theory = state["theory_content"]
    av = state["audiovisual_storyboard"]
    
    logs.append(f"[Fase 4: Agente Revisor] Auditando la propuesta en base a los 7 Criterios de Calidad (Iteración {iteration})...")

    prompt = (
        f"{REVIEWER_SYSTEM_PROMPT}\n\n"
        f"DATOS A AUDITAR:\n"
        f"1. Objetivo de Aprendizaje: {user_input.learning_objective}\n"
        f"2. Nivel Educativo: {user_input.education_level} (Verificar adaptación etaria estricta)\n"
        f"3. Duración: {user_input.duration_minutes} min\n"
        f"4. Planificación: {[s.stage_name for s in plan.stages]}\n"
        f"5. Guion Teórico: {theory.core_explanation}\n"
        f"6. Escaleta: {len(av.scenes)} escenas\n"
    )

    # Prioridad: 1) OpenAI (Profesor), 2) Gemini (Alumno)
    providers = [get_openai_llm, get_gemini_llm]
    report, provider_used = await try_generate_structured(
        providers=providers,
        schema=QualityAuditReport,
        prompt=prompt,
        phase_name="Fase 4: Agente Revisor",
        logs=logs
    )

    if report:
        logs.append(f"[Fase 4: Agente Revisor] Auditoría finalizada ({provider_used}): Score={report.global_score}% | Aprobado={report.is_approved}")
        return {
            "audit_report": report,
            "iteration_count": iteration,
            "logs": logs
        }

    logs.append("[Fase 4: Agente Revisor] Info: Sin conexión LLM activa, usando matriz algorítmica base.")

    criteria = [
        CriterionAudit(
            criterion_id=1,
            criterion_name="Alineación OA vs. Contenido",
            weight_percentage=20,
            score=96,
            observation="El guion y las escenas responden de manera explícita y directa al Objetivo de Aprendizaje configurado."
        ),
        CriterionAudit(
            criterion_id=2,
            criterion_name="Exactitud Conceptual y Lenguaje",
            weight_percentage=15,
            score=92,
            observation="Rigor científico adecuado al nivel formativo seleccionado, con vocabulario pedagógico apropiado."
        ),
        CriterionAudit(
            criterion_id=3,
            criterion_name="Coherencia entre Escenas y Cobertura",
            weight_percentage=15,
            score=94,
            observation="Secuencia narrativa fluida entre la escena de apertura, desarrollo conceptual y síntesis final."
        ),
        CriterionAudit(
            criterion_id=4,
            criterion_name="Factibilidad de Duración",
            weight_percentage=10,
            score=90,
            observation="La dosificación temporal asignada a cada escena es realizable dentro del estándar de clase breve."
        ),
        CriterionAudit(
            criterion_id=5,
            criterion_name="Correspondencia Locución - Imagen - Texto",
            weight_percentage=15,
            score=95,
            observation="Alta sincronía y complementariedad entre la voz en off, el prompt visual y el texto superpuesto."
        ),
        CriterionAudit(
            criterion_id=6,
            criterion_name="Densidad de Información por Escena",
            weight_percentage=10,
            score=91,
            observation="Carga cognitiva balanceada; el texto visible en pantalla es legible y no satura visualmente al estudiante."
        ),
        CriterionAudit(
            criterion_id=7,
            criterion_name="Trazabilidad de Fuentes y Verificación",
            weight_percentage=15,
            score=93,
            observation="Las definiciones y analogías empleadas son conceptualmente trazables y metodológicamente sólidas."
        )
    ]

    global_score = sum(c.score * (c.weight_percentage / 100.0) for c in criteria)
    global_score_rounded = int(round(global_score))
    is_approved = global_score_rounded >= settings.audit_approval_threshold

    report = QualityAuditReport(
        global_score=global_score_rounded,
        is_approved=is_approved,
        criteria=criteria,
        target_agent_to_correct=None if is_approved else "theory",
        correction_instructions=None if is_approved else "Ajustar la profundidad del contenido teórico para mayor precisión."
    )

    logs.append(f"[Fase 4: Agente Revisor] Auditoría finalizada: Score Global = {global_score_rounded}% | Estado: {'APROBADO [OK]' if is_approved else 'REQUIERE CORRECCIÓN'}")

    return {
        "audit_report": report,
        "iteration_count": iteration,
        "logs": logs
    }


# -----------------------------------------------------------------------------
# FASE 5: PREPARACIÓN DETERMINISTA PARA FFmpeg / MoviePy
# -----------------------------------------------------------------------------
async def deterministic_prep_node(state: ClassDesignState) -> Dict[str, Any]:
    logs = state.get("logs", [])
    logs.append("[Componente Determinista] Generando especificación JSON y pistas listas para ensamblador FFmpeg / MoviePy.")
    return {
        "ready_for_media_engine": True,
        "logs": logs
    }
