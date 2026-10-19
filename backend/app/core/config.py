import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Cargar variables de entorno desde .env (en backend o raíz)
root_env = Path(__file__).resolve().parent.parent.parent.parent / ".env"
backend_env = Path(__file__).resolve().parent.parent.parent / ".env"

if backend_env.exists():
    load_dotenv(backend_env)
elif root_env.exists():
    load_dotenv(root_env)
else:
    load_dotenv()

class Settings(BaseModel):
    app_name: str = "Sistema IA Multiagente para Clases Multimedia"
    version: str = "0.2.0"
    debug: bool = True
    
    # Proveedores de LLM y claves
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    anthropic_api_key: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    
    # Modelo económico por defecto (recomendado por el profesor)
    default_model: str = Field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    
    # Umbral de aprobación del Agente Revisor (85%)
    audit_approval_threshold: int = 85
    max_correction_iterations: int = 2

settings = Settings()

