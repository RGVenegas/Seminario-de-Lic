from typing import Literal
from langgraph.graph import StateGraph, START, END
from .state import ClassDesignState
from .nodes import (
    pedagogy_agent_node,
    theory_agent_node,
    audiovisual_agent_node,
    quality_reviewer_node,
    deterministic_prep_node
)
from ..core.config import settings

def route_after_review(state: ClassDesignState) -> Literal["approved", "retry_pedagogy", "retry_theory", "retry_audiovisual"]:
    """
    Función de enrutamiento condicional post-auditoría.
    Evalúa si la clase cumple el umbral mínimo (85%) o si debe reingresar a un loop acotado.
    """
    audit = state.get("audit_report")
    iteration = state.get("iteration_count", 0)
    max_iters = state.get("max_iterations", settings.max_correction_iterations)

    # 1. Si está aprobada por el revisor
    if audit and audit.is_approved:
        return "approved"

    # 2. Salvaguarda contra loops infinitos: si alcanzó el máximo de reintentos
    if iteration >= max_iters:
        return "approved"

    # 3. Enrutamiento hacia el agente específico con feedback
    target = audit.target_agent_to_correct if audit else "theory"
    if target == "pedagogy":
        return "retry_pedagogy"
    elif target == "theory":
        return "retry_theory"
    elif target == "audiovisual":
        return "retry_audiovisual"

    return "approved"

def create_class_design_graph():
    """
    Construye y compila el Grafo Acíclico Dirigido (DAG) en LangGraph.
    """
    workflow = StateGraph(ClassDesignState)

    # Registro de Nodos (Agentes)
    workflow.add_node("pedagogy_agent", pedagogy_agent_node)
    workflow.add_node("theory_agent", theory_agent_node)
    workflow.add_node("audiovisual_agent", audiovisual_agent_node)
    workflow.add_node("quality_reviewer", quality_reviewer_node)
    workflow.add_node("deterministic_prep", deterministic_prep_node)

    # Aristas Secuenciales (Flujo Principal DAG)
    workflow.add_edge(START, "pedagogy_agent")
    workflow.add_edge("pedagogy_agent", "theory_agent")
    workflow.add_edge("theory_agent", "audiovisual_agent")
    workflow.add_edge("audiovisual_agent", "quality_reviewer")

    # Arista Condicional de Auditoría y Loops de Corrección
    workflow.add_conditional_edges(
        "quality_reviewer",
        route_after_review,
        {
            "approved": "deterministic_prep",
            "retry_pedagogy": "pedagogy_agent",
            "retry_theory": "theory_agent",
            "retry_audiovisual": "audiovisual_agent"
        }
    )

    # Fin del flujo
    workflow.add_edge("deterministic_prep", END)

    # Compilación del grafo ejecutable
    return workflow.compile()

# Instancia singleton del pipeline compilado
class_design_pipeline = create_class_design_graph()
