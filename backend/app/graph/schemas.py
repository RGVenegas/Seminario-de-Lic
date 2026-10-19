from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# --- Insumos del Docente ---
class ClassInput(BaseModel):
    learning_objective: str = Field(description="Objetivo de Aprendizaje (OA)")
    education_level: str = Field(default="Secundaria (1º - 4º)", description="Nivel escolar o universitario")
    duration_minutes: int = Field(default=20, description="Duración estimada en minutos (15-20 min para MVP)")
    approach: str = Field(default="Clase Invertida (Flipped Classroom)", description="Enfoque didáctico")
    context: str = Field(default="Aula con proyector y trabajo en parejas", description="Contexto del curso")

# --- Fase 1: Planificación Pedagógica ---
class DidacticStage(BaseModel):
    stage_name: Literal["Inicio", "Desarrollo", "Cierre"] = Field(description="Momento de la clase")
    duration_min: int = Field(description="Minutos asignados a este momento")
    activity_title: str = Field(description="Nombre de la actividad central")
    description: str = Field(description="Detalle pedagógico de la actividad")
    pedagogical_intent: str = Field(description="Intención formativa / metacognitiva")

class PedagogicalPlan(BaseModel):
    stages: List[DidacticStage] = Field(description="Secuencia de las 3 etapas didácticas")
    methodology_applied: str = Field(description="Metodología (ABP, 5E, STEM, etc.)")
    prerequisites: List[str] = Field(default_factory=list, description="Saberes previos requeridos")
    estimated_total_time: int = Field(description="Suma total de minutos de la sesión")

# --- Fase 2: Contenidos Teóricos y Guion ---
class KeyTerm(BaseModel):
    term: str = Field(description="Término o concepto técnico")
    definition: str = Field(description="Definición comprensible adaptada al nivel educativo")

class TheoryContent(BaseModel):
    core_concept: str = Field(description="Título del concepto principal")
    core_explanation: str = Field(description="Explicación teórica rigurosa y clara")
    real_world_analogy: str = Field(description="Analogía de la vida cotidiana adaptada a la edad")
    voiceover_script: str = Field(description="Guion de locución para el audio de la clase")
    glossary: List[KeyTerm] = Field(description="Glosario de conceptos clave")

# --- Fase 3: Escaleta Audiovisual y Prompts ---
class Scene(BaseModel):
    scene_number: int = Field(description="Número correlativo de la escena")
    duration_seconds: int = Field(description="Duración en segundos")
    voiceover: str = Field(description="Locución hablada en off")
    visual_description: str = Field(description="Elementos visuales y composición en pantalla")
    on_screen_text: str = Field(description="Texto visible superpuesto")
    ai_image_prompt: str = Field(description="Prompt en inglés para el generador de imágenes de IA")

class AudiovisualStoryboard(BaseModel):
    video_title: str = Field(description="Título atractivo de la clase multimedia")
    target_audience: str = Field(description="Público objetivo")
    total_duration_seconds: int = Field(description="Duración total del video en segundos")
    scenes: List[Scene] = Field(description="Lista de escenas de la escaleta")

# --- Fase 4: Auditoría del Agente Revisor (7 Criterios de Calidad) ---
class CriterionAudit(BaseModel):
    criterion_id: int = Field(description="Identificador del 1 al 7")
    criterion_name: str = Field(description="Nombre del criterio evaluado")
    weight_percentage: int = Field(description="Ponderación del criterio")
    score: int = Field(ge=0, le=100, description="Puntaje obtenido de 0 a 100")
    observation: str = Field(description="Justificación cualitativa del puntaje")

class QualityAuditReport(BaseModel):
    global_score: int = Field(ge=0, le=100, description="Score ponderado de coherencia pedagógica")
    is_approved: bool = Field(description="True si global_score >= 85, False si requiere corrección")
    criteria: List[CriterionAudit] = Field(description="Evaluación individual de los 7 criterios")
    target_agent_to_correct: Optional[Literal["pedagogy", "theory", "audiovisual"]] = Field(
        default=None,
        description="Agente responsable de corregir si fue rechazado"
    )
    correction_instructions: Optional[str] = Field(
        default=None,
        description="Instrucciones precisas para la reescritura en caso de score < 85"
    )
