from typing import TypedDict, Optional, List
from .schemas import (
    ClassInput,
    PedagogicalPlan,
    TheoryContent,
    AudiovisualStoryboard,
    QualityAuditReport
)

class ClassDesignState(TypedDict):
    """
    Estado global del grafo en LangGraph.
    Se comparte y muta a través de los nodos del DAG.
    """
    # 1. Insumos del Docente
    user_input: ClassInput
    
    # 2. Entregables acumulados por fase
    pedagogical_plan: Optional[PedagogicalPlan]
    theory_content: Optional[TheoryContent]
    audiovisual_storyboard: Optional[AudiovisualStoryboard]
    audit_report: Optional[QualityAuditReport]
    
    # 3. Control de flujo, loops y auditoría
    iteration_count: int
    max_iterations: int
    feedback_history: List[str]
    ready_for_media_engine: bool
    logs: List[str]
