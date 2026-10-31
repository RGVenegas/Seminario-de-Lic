from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# --- Entrada del Usuario ---
class ClassInput(BaseModel):
    learning_objective: str = Field(description="Objetivo de Aprendizaje (OA) principal a abordar")
    education_level: str = Field(description="Nivel educativo según sistema chileno (Básica 1º-4º, Básica 5º-8º, Media 1º-4º, Educación Superior)")
    duration_minutes: int = Field(default=15, description="Duración total estimada de la clase en minutos (MVP: 15-20 min)")
    approach: str = Field(default="Clase Invertida (Flipped Classroom)", description="Enfoque pedagógico rector")
    context: Optional[str] = Field(default=None, description="Contexto del aula y recursos tecnológicos disponibles")

# --- Fase 1: Planificación Pedagógica ---
class DidacticStage(BaseModel):
    stage_name: Literal["Inicio", "Desarrollo", "Cierre"] = Field(description="Nombre de la etapa didáctica")
    duration_min: int = Field(description="Duración en minutos de esta etapa")
    activity_title: str = Field(description="Título descriptivo de la actividad")
    description: str = Field(description="Detalle de lo que realizan docente y estudiantes")
    pedagogical_intent: str = Field(description="Propósito formativo específico de la etapa")

class PedagogicalPlan(BaseModel):
    estimated_total_time: int = Field(description="Suma total de minutos de las etapas")
    methodology_applied: str = Field(description="Metodología adaptada al objetivo")
    prerequisites: List[str] = Field(description="Saberes previos requeridos")
    stages: List[DidacticStage] = Field(description="Las 3 etapas secuenciales obligatorias")

# --- Fase 2: Guion Teórico y Contenidos ---
class KeyTerm(BaseModel):
    term: str = Field(description="Término o concepto técnico")
    definition: str = Field(description="Definición precisa adaptada a la edad del público objetivo")

class TheoryContent(BaseModel):
    core_concept: str = Field(description="Título del concepto principal")
    core_explanation: str = Field(description="Explicación teórica rigurosa, clara y adaptada a la edad")
    real_world_analogy: str = Field(description="Analogía de la vida cotidiana potente y adaptada a los intereses del estudiante")
    voiceover_script: str = Field(description="Guion de locución fluido en español para el audio de la clase")
    glossary: List[KeyTerm] = Field(description="Glosario de conceptos clave en español")

# --- Fase 3: Escaleta Audiovisual y Prompts (100% Español) ---
class Scene(BaseModel):
    scene_number: int = Field(description="Número correlativo de la escena")
    duration_seconds: int = Field(description="Duración en segundos")
    voiceover: str = Field(description="Locución hablada en off en español")
    visual_description: str = Field(description="Elementos visuales y composición en pantalla en español")
    on_screen_text: str = Field(description="Texto clave visible en pantalla en español (máximo 8 palabras)")
    ai_image_prompt: str = Field(description="Descripción visual detallada en español para ilustrar la escena didáctica")

class AudiovisualStoryboard(BaseModel):
    video_title: str = Field(description="Título atractivo de la clase multimedia en español")
    target_audience: str = Field(description="Público objetivo y nivel escolar")
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
