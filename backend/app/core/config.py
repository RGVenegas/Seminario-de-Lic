import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Cargar variables de entorno: primero raíz, y luego backend si existe
root_env = Path(__file__).resolve().parent.parent.parent.parent / ".env"
backend_env = Path(__file__).resolve().parent.parent.parent / ".env"

if root_env.exists():
    load_dotenv(root_env, override=True)
if backend_env.exists():
    load_dotenv(backend_env, override=True)
if not root_env.exists() and not backend_env.exists():
    load_dotenv()

class Settings(BaseModel):
    app_name: str = "Sistema IA Multiagente para Clases Multimedia"
    version: str = "0.3.0"
    debug: bool = True
    
    # 1. Proveedor OpenAI (Profesor Guía)
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    default_model: str = Field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    
    # 2. Proveedor Google Gemini (Cuenta Alumno)
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"))
    
    # 3. Servidor Institucional (Universidad - Modelo Gemma / Quotas DevHub)
    use_institutional_quota: bool = Field(default_factory=lambda: os.getenv("USE_INSTITUTIONAL_QUOTA", "false").lower() in ("true", "1"))
    institutional_api_key: str = Field(default_factory=lambda: os.getenv("INSTITUTIONAL_API_KEY", ""))
    institutional_base_url: str = Field(default_factory=lambda: os.getenv("INSTITUTIONAL_BASE_URL", ""))
    institutional_model: str = Field(default_factory=lambda: os.getenv("INSTITUTIONAL_MODEL", "gemma4:26b"))
    institutional_max_tokens: int = Field(default_factory=lambda: int(os.getenv("INSTITUTIONAL_MAX_TOKENS", "600")))
    
    # 4. Proveedor Anthropic Claude (Opcional - Auditoría QC)
    anthropic_api_key: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    anthropic_model: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022"))
    
    # Umbral de aprobación del Agente Revisor (85%)
    audit_approval_threshold: int = 85
    max_correction_iterations: int = 2

settings = Settings()
