import asyncio
import sys
import os

# Asegurar que el path incluye el directorio raíz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from backend.app.graph.schemas import ClassInput
from backend.app.graph.state import ClassDesignState
from backend.app.graph.pipeline import class_design_pipeline

async def test_run():
    print("==================================================")
    print("PROBANDO EJECUCIÓN DEL GRAFO LANGGRAPH MULTIAGENTE")
    print("==================================================")

    test_input = ClassInput(
        learning_objective="Comprender la Ley de Conservación de la Energía y sus aplicaciones cotidianas.",
        education_level="Secundaria (1º - 4º)",
        duration_minutes=20,
        approach="Clase Invertida (Flipped Classroom)",
        context="Aula interactiva con proyector y trabajo en parejas."
    )

    initial_state: ClassDesignState = {
        "user_input": test_input,
        "pedagogical_plan": None,
        "theory_content": None,
        "audiovisual_storyboard": None,
        "audit_report": None,
        "iteration_count": 0,
        "max_iterations": 2,
        "feedback_history": [],
        "ready_for_media_engine": False,
        "logs": []
    }

    print("\nInvocando grafo con StateGraph.ainvoke()...\n")
    final_state = await class_design_pipeline.ainvoke(initial_state)

    print("\n--- REGISTRO DE EJECUCIÓN (LOGS DEL GRAFO) ---")
    for log in final_state["logs"]:
        print(f" -> {log}")

    print("\n--- RESULTADOS DEL REPORTE DE AUDITORÍA (FASE 4) ---")
    audit = final_state["audit_report"]
    print(f"Score Global: {audit.global_score}% | Aprobado: {audit.is_approved}")
    for crit in audit.criteria:
        print(f"  [{crit.score}/100] Criterio {crit.criterion_id}: {crit.criterion_name} ({crit.weight_percentage}%)")

    print("\n--- RESUMEN DE SALIDAS GENERADAS ---")
    plan = final_state["pedagogical_plan"]
    print(f"Etapas pedagógicas: {[s.stage_name for s in plan.stages]}")
    theory = final_state["theory_content"]
    print(f"Concepto central: {theory.core_concept}")
    print(f"Términos glosario: {[t.term for t in theory.glossary]}")
    av = final_state["audiovisual_storyboard"]
    print(f"Escenas generadas: {len(av.scenes)} | Título de video: '{av.video_title}'")
    print(f"Listo para Ensamblador FFmpeg: {final_state['ready_for_media_engine']}")

    print("\n==================================================")
    print("✅ TEST COMPLETADO CON ÉXITO: El Grafo opera correctamente")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(test_run())
