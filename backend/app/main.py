import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .core.config import settings
from .graph.schemas import ClassInput, AudiovisualStoryboard
from .graph.state import ClassDesignState
from .graph.pipeline import class_design_pipeline
from .media.video_assembler import assemble_multimedia_video

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="API RESTful para el Sistema de Inteligencia Artificial Multiagente para Clases Multimedia Breves (LangGraph)"
)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de archivos
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
os.makedirs(output_dir, exist_ok=True)

# Montar directorio multimedia para streaming de video y audio
app.mount("/media", StaticFiles(directory=output_dir), name="media")


class RenderVideoRequest(BaseModel):
    storyboard: AudiovisualStoryboard
    voice: Optional[str] = "es-CL-LorenzoNeural"


# Servir Frontend Web directamente en la raíz
@app.get("/")
async def serve_index():
    index_path = os.path.join(project_root, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "online", "service": settings.app_name}


@app.get("/styles.css")
async def serve_css():
    css_path = os.path.join(project_root, "styles.css")
    return FileResponse(css_path, media_type="text/css")


@app.get("/app.js")
async def serve_js():
    js_path = os.path.join(project_root, "app.js")
    return FileResponse(js_path, media_type="application/javascript")


@app.get("/api/info")
async def get_system_info():
    return {
        "status": "online",
        "service": settings.app_name,
        "version": settings.version,
        "engine": "LangGraph (DAG Multiagente)",
        "multimedia": "Edge-TTS + IA Visual + MoviePy",
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


@app.post("/api/render-video")
async def render_video_endpoint(req: RenderVideoRequest):
    """
    Sintetiza la locución de cada escena con Edge-TTS, genera las ilustraciones
    y ensambla el video MP4 continuo sincronizado con subtítulos inferiores.
    """
    try:
        result = await assemble_multimedia_video(
            storyboard=req.storyboard,
            output_dir=output_dir,
            voice=req.voice or "es-CL-LorenzoNeural"
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al renderizar el video multimedia: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
