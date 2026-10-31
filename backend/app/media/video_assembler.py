import os
import uuid
import logging
from typing import Dict, Any, List, Union
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

from .tts_generator import generate_tts_audio, DEFAULT_VOICE
from .image_generator import generate_scene_image, TARGET_WIDTH, TARGET_HEIGHT
from ..graph.schemas import AudiovisualStoryboard, Scene

logger = logging.getLogger("seminario.media.video")

def _apply_lower_third_subtitle(image_path: str, subtitle_text: str, scene_number: int):
    """
    Superpone una barra inferior (lower-third) con estilo televisivo didáctico
    para mostrar el texto en pantalla (on_screen_text) durante la locución, 100% en español.
    """
    if not subtitle_text or not os.path.exists(image_path):
        return

    try:
        base_img = Image.open(image_path).convert("RGBA")
        overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        w, h = base_img.size
        banner_y0 = h - 110
        banner_y1 = h - 30

        # Fondo translúcido azul oscuro con borde celeste
        draw.rounded_rectangle(
            [(40, banner_y0), (w - 40, banner_y1)],
            radius=12,
            fill=(15, 23, 42, 225),
            outline=(56, 189, 248, 220),
            width=2
        )

        # Cargar fuente
        font_main = None
        font_badge = None
        for fp in ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf"]:
            if os.path.exists(fp):
                try:
                    font_main = ImageFont.truetype(fp, 26)
                    font_badge = ImageFont.truetype(fp, 16)
                    break
                except Exception:
                    pass
        if not font_main:
            font_main = ImageFont.load_default()
            font_badge = font_main

        # Etiqueta de escena en español
        draw.text((65, banner_y0 + 10), f"ESCENA {scene_number}  |  CONCEPTO CLAVE", fill=(56, 189, 248), font=font_badge)

        # Texto del subtítulo (garantizado en español)
        display_text = subtitle_text[:95] + ("..." if len(subtitle_text) > 95 else "")
        draw.text((65, banner_y0 + 35), display_text, fill=(255, 255, 255), font=font_main)

        combined = Image.alpha_composite(base_img, overlay).convert("RGB")
        combined.save(image_path, "JPEG", quality=92)
    except Exception as e:
        logger.warning(f"No se pudo estampar subtítulo inferior en escena {scene_number}: {e}")

async def assemble_multimedia_video(
    storyboard: Union[AudiovisualStoryboard, Dict[str, Any]],
    output_dir: str = "backend/output",
    voice: str = DEFAULT_VOICE,
    job_id: str = None
) -> Dict[str, Any]:
    """
    Construye el video educativo completo combinando:
    1. Locución neural por escena (Edge-TTS)
    2. Ilustración didáctica o científica por escena (Wikipedia Commons / IA / Infografía)
    3. Barra de subtítulos interactiva (Lower Third en español)
    4. Sincronización y concatenación final en MP4 (H.264 + AAC)
    
    Returns:
        Diccionario con metadatos del video generado y rutas relativas para el cliente web.
    """
    if not job_id:
        job_id = f"clase_{uuid.uuid4().hex[:8]}"
        
    abs_output_dir = os.path.abspath(output_dir)
    os.makedirs(abs_output_dir, exist_ok=True)
    
    job_media_dir = os.path.join(abs_output_dir, job_id)
    os.makedirs(job_media_dir, exist_ok=True)

    # Extraer escenas
    if isinstance(storyboard, AudiovisualStoryboard):
        scenes = storyboard.scenes
        title = storyboard.video_title
        target_audience = storyboard.target_audience or "Enseñanza Media"
    elif isinstance(storyboard, dict):
        scenes_data = storyboard.get("scenes", [])
        scenes = [Scene(**s) if isinstance(s, dict) else s for s in scenes_data]
        title = storyboard.get("video_title", "Clase Multimedia")
        target_audience = storyboard.get("target_audience", "Enseñanza Media")
    else:
        raise ValueError("Formato de escaleta audiovisual inválido.")

    if not scenes:
        raise ValueError("La escaleta no contiene escenas para renderizar.")

    logger.info(f"Iniciando ensamblado multimedia para '{title}' ({len(scenes)} escenas, nivel: {target_audience})...")
    
    scene_clips = []
    scenes_meta = []
    open_audio_clips = []

    try:
        for idx, scene in enumerate(scenes, start=1):
            scene_num = scene.scene_number or idx
            audio_path = os.path.join(job_media_dir, f"scene_{scene_num}.mp3")
            image_path = os.path.join(job_media_dir, f"scene_{scene_num}.jpg")

            logger.info(f"[Escena {scene_num}/{len(scenes)}] Generando audio TTS ({voice})...")
            await generate_tts_audio(
                text=scene.voiceover,
                output_path=audio_path,
                voice=voice
            )

            # Cargar clip de audio para obtener la duración exacta
            audio_clip = AudioFileClip(audio_path)
            open_audio_clips.append(audio_clip)
            exact_duration = audio_clip.duration

            logger.info(f"[Escena {scene_num}/{len(scenes)}] Obteniendo ilustración (duración: {exact_duration:.1f}s)...")
            await generate_scene_image(
                prompt=scene.ai_image_prompt,
                output_path=image_path,
                scene_number=scene_num,
                on_screen_text=scene.on_screen_text,
                education_level=target_audience
            )

            # Aplicar lower third subtítulo sobre la imagen
            _apply_lower_third_subtitle(image_path, scene.on_screen_text, scene_num)

            # Crear ImageClip sincronizado a la duración del audio
            clip = ImageClip(image_path).with_duration(exact_duration).with_audio(audio_clip)
            scene_clips.append(clip)

            scenes_meta.append({
                "scene_number": scene_num,
                "duration_seconds": round(exact_duration, 2),
                "voiceover": scene.voiceover,
                "on_screen_text": scene.on_screen_text,
                "audio_url": f"/media/{job_id}/scene_{scene_num}.mp3",
                "image_url": f"/media/{job_id}/scene_{scene_num}.jpg"
            })

        # Concatenar todas las escenas en una pista de video continua
        logger.info(f"Concatenando {len(scene_clips)} escenas con MoviePy...")
        final_video = concatenate_videoclips(scene_clips, method="compose")
        total_duration = final_video.duration

        final_filename = f"{job_id}_video.mp4"
        final_video_path = os.path.join(abs_output_dir, final_filename)

        logger.info(f"Exportando MP4 final: {final_video_path}...")
        final_video.write_videofile(
            final_video_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=4,
            logger=None
        )

        final_video.close()
        for c in scene_clips:
            c.close()
        for a in open_audio_clips:
            a.close()

        logger.info(f"Video ensamblado con éxito! Duración total: {total_duration:.1f}s, Archivo: {final_filename}")

        return {
            "success": True,
            "job_id": job_id,
            "title": title,
            "video_filename": final_filename,
            "video_path": final_video_path,
            "video_url": f"/media/{final_filename}",
            "total_duration_seconds": round(total_duration, 2),
            "scenes_count": len(scenes),
            "scenes": scenes_meta
        }

    except Exception as e:
        logger.error(f"Error durante el ensamblado del video: {e}")
        for c in scene_clips:
            try: c.close()
            except Exception: pass
        for a in open_audio_clips:
            try: a.close()
            except Exception: pass
        raise RuntimeError(f"Falla al ensamblar video multimedia: {str(e)}")
