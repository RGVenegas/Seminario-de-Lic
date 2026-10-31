import os
import asyncio
import logging
from typing import Optional
import edge_tts

logger = logging.getLogger("seminario.media.tts")

# Voz neuronal predeterminada (Español de Chile para contexto UNAB / Latinoamérica)
DEFAULT_VOICE = "es-CL-LorenzoNeural"
ALTERNATIVE_VOICE = "es-CL-CatalinaNeural"

async def generate_tts_audio(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    volume: str = "+0%"
) -> str:
    """
    Sintetiza voz neural de alta calidad utilizando Edge-TTS (sin costo de API).
    
    Args:
        text: Texto de la locución pedagógica a sintetizar.
        output_path: Ruta destino donde se guardará el archivo .mp3.
        voice: Nombre corto de la voz (ej: 'es-CL-LorenzoNeural').
        rate: Modificador de velocidad (ej: '+0%').
        volume: Modificador de volumen (ej: '+0%').
        
    Returns:
        Ruta absoluta del archivo de audio generado.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    clean_text = text.strip()
    if not clean_text:
        clean_text = "Transición de escena didáctica."

    try:
        logger.info(f"Generando TTS con voz '{voice}' para texto: '{clean_text[:50]}...'")
        communicate = edge_tts.Communicate(
            text=clean_text,
            voice=voice,
            rate=rate,
            volume=volume
        )
        await communicate.save(output_path)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"TTS generado exitosamente: {output_path} ({os.path.getsize(output_path)} bytes)")
            return output_path
        else:
            raise RuntimeError("El archivo de audio generado está vacío.")

    except Exception as e:
        logger.warning(f"Error con voz '{voice}': {e}. Reintentando con voz alternativa '{ALTERNATIVE_VOICE}'...")
        try:
            communicate = edge_tts.Communicate(
                text=clean_text,
                voice=ALTERNATIVE_VOICE,
                rate=rate,
                volume=volume
            )
            await communicate.save(output_path)
            return output_path
        except Exception as e2:
            logger.error(f"Falla crítica en TTS: {e2}. Generando pista de contingencia.")
            _generate_fallback_silence(output_path, duration_seconds=max(3, len(clean_text) // 15))
            return output_path

def _generate_fallback_silence(output_path: str, duration_seconds: int = 4):
    """
    Genera un archivo MP3 de silencio en caso de desconexión total de red,
    asegurando que el pipeline de video continúe funcionando.
    """
    import subprocess
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(duration_seconds),
        "-q:a", "9",
        "-acodec", "libmp3lame",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

