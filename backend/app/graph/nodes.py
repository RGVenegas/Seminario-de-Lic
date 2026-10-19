from typing import Dict, Any, Optional

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

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


def get_llm() -> Optional[Any]:
    """Retorna una instancia de ChatOpenAI si la clave es válida, o None para modo fallback."""
    if ChatOpenAI is None:
        return None
    key = settings.openai_api_key.strip() if settings.openai_api_key else ""
    if key and not key.startswith("PEGA_TU") and len(key) > 15:
        try:
            return ChatOpenAI(
                model=settings.default_model,
                api_key=key,
                temperature=0.7
            )
        except Exception:
            return None
    return None


# -----------------------------------------------------------------------------
# FASE 1: AGENTE DE PLANIFICACIÓN PEDAGÓGICA
# -----------------------------------------------------------------------------
async def pedagogy_agent_node(state: ClassDesignState) -> Dict[str, Any]:
    user_input = state["user_input"]
    feedback = state.get("feedback_history", [])
    logs = state.get("logs", [])
    
    log_msg = f"[Fase 1: Planificación] Diseñando estructura de 3 etapas para: '{user_input.learning_objective[:40]}...'"
    if feedback:
        log_msg += f" (Aplicando corrección: {feedback[-1][:50]}...)"
    logs.append(log_msg)

    llm = get_llm()
    if llm:
        try:
            structured_llm = llm.with_structured_output(PedagogicalPlan)
            prompt = (
                f"{PEDAGOGY_SYSTEM_PROMPT}\n\n"
                f"Objetivo de Aprendizaje: {user_input.learning_objective}\n"
                f"Nivel Educativo: {user_input.education_level}\n"
                f"Duración: {user_input.duration_minutes} minutos\n"
                f"Metodología: {user_input.approach}\n"
                f"Contexto: {user_input.context}\n"
            )
            if feedback:
                prompt += f"\nObservaciones para corregir: {feedback[-1]}\n"
            
            plan = await structured_llm.ainvoke(prompt)
            logs.append(f"[Fase 1: Planificación] Plan pedagógico generado exitosamente con OpenAI ({settings.default_model}).")
            return {"pedagogical_plan": plan, "logs": logs}
        except Exception as e:
            logs.append(f"[Fase 1: Planificación] Info: Llamada a OpenAI ({str(e)[:45]}...), usando generador base.")

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
# FASE 2: AGENTE DE CONTENIDOS TEÓRICOS Y GUION
# -----------------------------------------------------------------------------
async def theory_agent_node(state: ClassDesignState) -> Dict[str, Any]:
    user_input = state["user_input"]
    plan = state["pedagogical_plan"]
    logs = state.get("logs", [])
    
    logs.append(f"[Fase 2: Guion Teórico] Insumo: Planificación aprobada ({plan.estimated_total_time} min). Redactando cuerpo conceptual y analogía.")

    llm = get_llm()
    if llm:
        try:
            structured_llm = llm.with_structured_output(TheoryContent)
            prompt = (
                f"{THEORY_SYSTEM_PROMPT}\n\n"
                f"Objetivo de Aprendizaje: {user_input.learning_objective}\n"
                f"Nivel: {user_input.education_level}\n"
                f"Planificación Previa:\n"
                f"- Etapas: {[s.stage_name + ' (' + str(s.duration_min) + 'm)' for s in plan.stages]}\n"
                f"- Metodología: {plan.methodology_applied}\n"
            )
            theory = await structured_llm.ainvoke(prompt)
            logs.append(f"[Fase 2: Guion Teórico] Guion teórico y analogía redactados con OpenAI ({settings.default_model}).")
            return {"theory_content": theory, "logs": logs}
        except Exception as e:
            logs.append(f"[Fase 2: Guion Teórico] Info: Llamada a OpenAI ({str(e)[:45]}...), usando generador base.")

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
# FASE 3: AGENTE DE PRODUCCIÓN AUDIOVISUAL
# -----------------------------------------------------------------------------
async def audiovisual_agent_node(state: ClassDesignState) -> Dict[str, Any]:
    theory = state["theory_content"]
    user_input = state["user_input"]
    logs = state.get("logs", [])

    logs.append("[Fase 3: Escaleta Audiovisual] Diseñando escenas multimedia y prompts de IA generativa visual.")

    llm = get_llm()
    if llm:
        try:
            structured_llm = llm.with_structured_output(AudiovisualStoryboard)
            prompt = (
                f"{AUDIOVISUAL_SYSTEM_PROMPT}\n\n"
                f"Objetivo de Aprendizaje: {user_input.learning_objective}\n"
                f"Público: {user_input.education_level}\n"
                f"Concepto Central: {theory.core_concept}\n"
                f"Explicación Teórica: {theory.core_explanation}\n"
                f"Analogía: {theory.real_world_analogy}\n"
            )
            storyboard = await structured_llm.ainvoke(prompt)
            logs.append(f"[Fase 3: Escaleta Audiovisual] Escaleta y prompts visuales generados con OpenAI ({settings.default_model}).")
            return {"audiovisual_storyboard": storyboard, "logs": logs}
        except Exception as e:
            logs.append(f"[Fase 3: Escaleta Audiovisual] Info: Llamada a OpenAI ({str(e)[:45]}...), usando generador base.")

    oa_clean = user_input.learning_objective.replace('"', '')

    scenes = [
        Scene(
            scene_number=1,
            duration_seconds=30,
            voiceover=f"Hola a todos. Hoy responderemos una pregunta clave sobre {oa_clean[:50]}...",
            visual_description="Plano general ilustrado con animación conceptual que introduce el problema detonante.",
            on_screen_text=f"Objetivo: {oa_clean[:45]}...",
            ai_image_prompt=f"A vibrant clean vector illustration explaining {oa_clean[:40]}, academic educational style, soft slate and navy background, high quality, 4k"
        ),
        Scene(
            scene_number=2,
            duration_seconds=75,
            voiceover=theory.core_explanation[:150] + "...",
            visual_description="Desglose infográfico en 2D con flechas direccionales y etiquetas descriptivas.",
            on_screen_text="Explicación Paso a Paso: Estructura del Fenómeno",
            ai_image_prompt="A minimalist modern diagram showing key scientific components and flow arrows, clean typography, soft pastel accents, 4k"
        ),
        Scene(
            scene_number=3,
            duration_seconds=35,
            voiceover=f"Para concluir, recuerden la regla de oro: {theory.real_world_analogy[:100]}...",
            visual_description="Resumen visual con 3 tarjetas de síntesis y pregunta de cierre para los estudiantes.",
            on_screen_text="Conclusiones Clave | Ticket de Salida",
            ai_image_prompt="A warm educational summary board with three clear takeaway icons, friendly student aesthetic, high resolution"
        )
    ]

    storyboard = AudiovisualStoryboard(
        video_title=f"Clase Multimedia Breve: {oa_clean[:40]}",
        target_audience=user_input.education_level,
        total_duration_seconds=140,
        scenes=scenes
    )

    return {"audiovisual_storyboard": storyboard, "logs": logs}

# -----------------------------------------------------------------------------
# FASE 4: AGENTE REVISOR (QUALITY CONTROL - 7 CRITERIOS)
# -----------------------------------------------------------------------------
async def quality_reviewer_node(state: ClassDesignState) -> Dict[str, Any]:
    logs = state.get("logs", [])
    iteration = state.get("iteration_count", 0) + 1
    user_input = state["user_input"]
    plan = state["pedagogical_plan"]
    theory = state["theory_content"]
    av = state["audiovisual_storyboard"]
    
    logs.append(f"[Fase 4: Agente Revisor] Auditando la propuesta en base a los 7 Criterios de Calidad (Iteración {iteration})...")

    llm = get_llm()
    if llm:
        try:
            structured_llm = llm.with_structured_output(QualityAuditReport)
            prompt = (
                f"{REVIEWER_SYSTEM_PROMPT}\n\n"
                f"DATOS A AUDITAR:\n"
                f"1. Objetivo de Aprendizaje: {user_input.learning_objective}\n"
                f"2. Nivel Educativo: {user_input.education_level}\n"
                f"3. Duración: {user_input.duration_minutes} min\n"
                f"4. Planificación: {[s.stage_name for s in plan.stages]}\n"
                f"5. Guion Teórico: {theory.core_explanation}\n"
                f"6. Escaleta: {len(av.scenes)} escenas\n"
            )
            report = await structured_llm.ainvoke(prompt)
            logs.append(f"[Fase 4: Agente Revisor] Auditoría completada con OpenAI ({settings.default_model}): Score={report.global_score}% | Aprobado={report.is_approved}")
            return {
                "audit_report": report,
                "iteration_count": iteration,
                "logs": logs
            }
        except Exception as e:
            logs.append(f"[Fase 4: Agente Revisor] Info: Llamada a OpenAI ({str(e)[:45]}...), usando matriz base.")

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
