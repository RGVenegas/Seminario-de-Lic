from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .graph.schemas import ClassInput
from .graph.state import ClassDesignState
from .graph.pipeline import class_design_pipeline

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="API RESTful para el Sistema de Inteligencia Artificial Multiagente para Clases Multimedia Breves (LangGraph)"
)

# Habilitar CORS para permitir llamadas desde index.html en localhost / 127.0.0.1
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": settings.app_name,
        "version": settings.version,
        "engine": "LangGraph (DAG Multiagente)",
        "docs_url": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/generate")
async def generate_multimedia_class(user_input: ClassInput):
    """
    Ejecuta el Grafo Acíclico Dirigido (DAG) en LangGraph:
    Orquestador -> Planificación -> Guion Teórico -> Escaleta Audiovisual -> Revisor (7 Criterios) -> Ensamblador Prep
    """
    try:
        initial_state: ClassDesignState = {
            "user_input": user_input,
            "pedagogical_plan": None,
            "theory_content": None,
            "audiovisual_storyboard": None,
            "audit_report": None,
            "iteration_count": 0,
            "max_iterations": settings.max_correction_iterations,
            "feedback_history": [],
            "ready_for_media_engine": False,
            "logs": []
        }

        # Ejecución asíncrona del grafo en LangGraph
        final_state = await class_design_pipeline.ainvoke(initial_state)

        return {
            "success": True,
            "oa": user_input.learning_objective,
            "level": user_input.education_level,
            "duration": user_input.duration_minutes,
            "approach": user_input.approach,
            "pedagogical_plan": final_state.get("pedagogical_plan"),
            "theory_content": final_state.get("theory_content"),
            "audiovisual_storyboard": final_state.get("audiovisual_storyboard"),
            "audit_report": final_state.get("audit_report"),
            "ready_for_media_engine": final_state.get("ready_for_media_engine"),
            "iteration_count": final_state.get("iteration_count"),
            "logs": final_state.get("logs")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al ejecutar el grafo multiagente: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
