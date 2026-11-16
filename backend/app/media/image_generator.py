import os
import io
import re
import asyncio
import urllib.parse
import logging
import base64
from typing import Optional, Tuple
import httpx
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

logger = logging.getLogger("seminario.media.image")

TARGET_WIDTH = 1280
TARGET_HEIGHT = 720

async def _translate_prompt_for_diffusion(prompt_es: str) -> str:
    """
    Traduce la descripción visual en español a un prompt en inglés
    conciso y descriptivo para modelos de difusión (Stable Diffusion).
    Usa Gemini Flash si está disponible, o un fallback directo.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=(
                    "Translate this Spanish visual scene description into a concise 15-word English prompt "
                    f"for Stable Diffusion (visuals only, no chat, comma separated): {prompt_es}"
                )
            )
            if resp and resp.text:
                clean = resp.text.strip().replace("\n", " ").strip("\"'")
                if len(clean) > 5:
                    logger.info(f"[Prompt Diffusion Traducido]: {clean}")
                    return clean
        except Exception as e:
            logger.warning(f"Error traduciendo prompt con Gemini: {e}")

    # Fallback directo con el texto recibido
    return prompt_es

def _composite_image_16_9(fg_img: Image.Image, output_path: str, width: int = TARGET_WIDTH, height: int = TARGET_HEIGHT):
    """
    Compone la ilustración en una relación de aspecto 16:9 (1280x720) profesional,
    utilizando fondo difuminado ambiental (estilo documental/YouTube) para no deformar la imagen.
    """
    # Fondo ambiental difuminado
    bg = fg_img.resize((width, height), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(28))
    bg = ImageEnhance.Brightness(bg).enhance(0.35)

    # Ajustar imagen nítida al centro dejando espacio para el subtítulo inferior
    fg_w, fg_h = fg_img.size
    scale = min((width - 60) / fg_w, (height - 130) / fg_h)
    new_w, new_h = max(10, int(fg_w * scale)), max(10, int(fg_h * scale))
    resized_fg = fg_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    offset_x = (width - new_w) // 2
    offset_y = (height - 110 - new_h) // 2 + 10
    bg.paste(resized_fg, (offset_x, offset_y))

    bg.save(output_path, "JPEG", quality=92)

async def _fetch_openai_sunburst_image(
    prompt: str,
    output_path: str,
    education_level: str = "Enseñanza Media",
    scene_number: int = 1,
    width: int = TARGET_WIDTH,
    height: int = TARGET_HEIGHT
) -> bool:
    """
    Genera una ilustración didáctica de alta fidelidad utilizando el modelo
    gpt-image-2.6-sunburst de OpenAI.
    Resuelve el problema de Concept Bleeding, elimina la estética de anuncios o afiches,
    y adapta el estilo visual estrictamente a la edad y nivel educativo sin texto impreso.
    """
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not openai_key or openai_key.startswith("tu_") or len(openai_key) < 15:
        return False

    image_model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2.6-sunburst").strip()

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=openai_key)

        # Determinar estética adaptada por nivel etario
        lvl_lower = (education_level or "").lower()
        if "1" in lvl_lower and "básic" in lvl_lower:
            age_style = "Warm and friendly storybook educational illustration, soft natural lighting, gentle 3D digital art suitable for elementary children aged 6 to 10."
        elif "5" in lvl_lower or "8" in lvl_lower or "básic" in lvl_lower:
            age_style = "Vibrant contemporary digital illustration, clean educational comic style, engaging and positive for pre-teens aged 10 to 14."
        elif "superior" in lvl_lower or "univers" in lvl_lower:
            age_style = "Professional documentary photography or high-end clean scientific photograph, realistic and sober."
        else: # Enseñanza Media (14 a 18 años)
            age_style = "Realistic documentary photography or mature modern digital realism, natural lighting, authentic and relatable for high school teenagers aged 14 to 18."

        # Limpiar el prompt de palabras que provoquen estética de anuncio o afiche publicitario
        clean_prompt = prompt
        for trigger in ["infografía científica", "infografía didáctica", "infografía", "lámina infográfica", "diagrama interactivo", "afiche", "anuncio", "poster"]:
            clean_prompt = re.sub(re.escape(trigger), "escena visual educativa", clean_prompt, flags=re.IGNORECASE)

        educational_prompt = (
            f"A cinematic educational scene showing: {clean_prompt}. "
            f"Visual Aesthetic: {age_style} "
            "High aesthetic quality, natural human and animal anatomy, distinct separated subjects, genuine emotional connection, horizontal composition. "
            "STRICT NEGATIVE CONSTRAINT: Absolutely DO NOT include any text, letters, titles, words, numbers, typography, watermarks, banners, flyers, posters, or advertisement layouts. Pure visual scene only. No ad style, no marketing elements."
        )

        logger.info(f"[OpenAI Sunburst] Generando escena {scene_number} con {image_model} ({education_level})...")
        response = await client.images.generate(
            model=image_model,
            prompt=educational_prompt,
            size="1024x1024",
            n=1
        )

        if response and response.data:
            item = response.data[0]
            raw_img = None

            if getattr(item, "b64_json", None):
                img_bytes = base64.b64decode(item.b64_json)
                raw_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            elif getattr(item, "url", None):
                async with httpx.AsyncClient(timeout=25.0) as http_client:
                    r_img = await http_client.get(item.url)
                    if r_img.status_code == 200:
                        raw_img = Image.open(io.BytesIO(r_img.content)).convert("RGB")

            if raw_img:
                _composite_image_16_9(raw_img, output_path, width, height)
                logger.info(f"[OpenAI Sunburst OK] Imagen de escena {scene_number} generada y compuesta exitosamente en 16:9 con {image_model}.")
                return True

    except Exception as e:
        logger.warning(f"[OpenAI Sunburst] Aviso: No se pudo generar con {image_model} ({e}). Derivando a siguiente proveedor...")
    return False

async def _fetch_ai_horde_image(
    prompt: str,
    output_path: str,
    width: int = TARGET_WIDTH,
    height: int = TARGET_HEIGHT
) -> bool:
    """
    Genera una imagen con IA mediante el cluster descentralizado AI Horde (Stable Diffusion).
    Servicio 100% gratuito, anónimo y sin bloqueos de cuota.
    """
    en_prompt = await _translate_prompt_for_diffusion(prompt)
    headers = {
        "apikey": "0000000000",
        "Client-Agent": "SeminarioLicApp:2.0:unab"
    }
    payload = {
        "prompt": f"{en_prompt}, educational science illustration, clear composition, vibrant colors, clean design",
        "params": {
            "steps": 20,
            "width": 512,
            "height": 512,
            "cfg_scale": 7.5,
            "sampler_name": "k_euler",
        },
        "nsfw": False,
        "censor_nsfw": True
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            req_id = None
            for retry in range(3):
                r = await client.post("https://aihorde.net/api/v2/generate/async", json=payload, headers=headers)
                if r.status_code == 202:
                    req_id = r.json().get("id")
                    break
                elif r.status_code == 429:
                    await asyncio.sleep(2.5)
                else:
                    logger.warning(f"[AI Horde] Error al enviar tarea: {r.status_code}")
                    break

            if not req_id:
                return False

            # Polling con timeout de 20 segundos
            for step in range(11):
                await asyncio.sleep(2.0)
                check = await client.get(f"https://aihorde.net/api/v2/generate/check/{req_id}", headers=headers)
                if check.status_code == 200:
                    cdata = check.json()
                    if cdata.get("done"):
                        status = await client.get(f"https://aihorde.net/api/v2/generate/status/{req_id}", headers=headers)
                        if status.status_code == 200:
                            gens = status.json().get("generations", [])
                            if gens and gens[0].get("img"):
                                img_url = gens[0].get("img")
                                r_img = await client.get(img_url)
                                if r_img.status_code == 200 and len(r_img.content) > 2000:
                                    raw_img = Image.open(io.BytesIO(r_img.content)).convert("RGB")
                                    _composite_image_16_9(raw_img, output_path, width, height)
                                    logger.info(f"[AI Horde OK] Imagen generada con éxito para la escena.")
                                    return True
    except Exception as e:
        logger.warning(f"[AI Horde] Excepción durante la generación de imagen: {e}")
    return False

async def _fetch_pollinations_image(
    prompt: str,
    output_path: str,
    width: int = TARGET_WIDTH,
    height: int = TARGET_HEIGHT
) -> bool:
    """Descarga ilustración generada por IA vía Pollinations (modelo flux) como respaldo secundario."""
    try:
        clean_p = urllib.parse.quote(prompt[:120])
        url = f"https://image.pollinations.ai/prompt/{clean_p}?model=flux&width=1024&height=576"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
            r = await client.get(url, headers=headers)
            if r.status_code == 200 and len(r.content) > 3000:
                raw = Image.open(io.BytesIO(r.content)).convert("RGB")
                _composite_image_16_9(raw, output_path, width, height)
                logger.info(f"[Pollinations OK] Imagen generada.")
                return True
    except Exception:
        pass
    return False

def _generate_infographic_visual_slide(
    output_path: str,
    scene_number: int,
    on_screen_text: str,
    education_level: str,
    width: int = TARGET_WIDTH,
    height: int = TARGET_HEIGHT
):
    """
    Genera una lámina infográfica diagramática con diseño moderno y visual
    (estilo Kurzgesagt / Khan Academy), 100% en español, sin párrafos de texto tipo PPT.
    """
    base = Image.new("RGB", (width, height), color=(15, 23, 42)) # Slate 900
    draw = ImageDraw.Draw(base)

    # Gradiente de fondo tecnológico
    for y in range(height):
        ratio = y / height
        r = int(15 * (1 - ratio) + 24 * ratio)
        g = int(23 * (1 - ratio) + 37 * ratio)
        b = int(42 * (1 - ratio) + 75 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Marco con borde de diseño
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(56, 189, 248), width=2)

    # Fuentes del sistema
    font_title = None
    font_badge = None
    font_node = None
    for fp in ["C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\arial.ttf"]:
        if os.path.exists(fp):
            try:
                font_title = ImageFont.truetype(fp, 36)
                font_badge = ImageFont.truetype(fp, 20)
                font_node = ImageFont.truetype(fp, 18)
                break
            except Exception:
                pass
    if not font_title:
        font_title = ImageFont.load_default()
        font_badge = font_title
        font_node = font_title

    # Badge superior en español con nivel educacional chileno
    lvl_clean = education_level.upper() if education_level else "ENSEÑANZA MEDIA"
    badge_str = f"CLASE MULTIMEDIA DIDÁCTICA  •  NIVEL: {lvl_clean}  •  ESCENA {scene_number}"
    draw.text((60, 50), badge_str, fill=(56, 189, 248), font=font_badge)

    # Título central destacado
    title_text = on_screen_text if on_screen_text else f"Concepto Didáctico {scene_number}"
    draw.text((60, 95), title_text[:75], fill=(255, 255, 255), font=font_title)

    # Esquema infográfico de 3 nodos conceptuales interconectados
    draw.line([(250, 340), (1030, 340)], fill=(71, 85, 105), width=6)

    nodes = [
        ("1. Estructura", "Identificación y componentes", (250, 340), (239, 68, 68)), # Rojo
        ("2. Mecanismo", "Función y dinámica biológica", (640, 340), (59, 130, 246)),  # Azul
        ("3. Conexión", "Impacto en el organismo", (1030, 340), (16, 185, 129))       # Verde
    ]

    for n_title, n_desc, (cx, cy), color in nodes:
        # Anillos concéntricos de brillo
        draw.ellipse([(cx - 75, cy - 75), (cx + 75, cy + 75)], outline=color, width=4)
        draw.ellipse([(cx - 65, cy - 65), (cx + 65, cy + 65)], fill=(30, 41, 59))
        draw.text((cx - 45, cy - 10), n_title, fill=(255, 255, 255), font=font_node)
        draw.text((cx - 85, cy + 90), n_desc, fill=(203, 213, 225), font=font_node)

    base.save(output_path, "JPEG", quality=92)

async def generate_scene_image(
    prompt: str,
    output_path: str,
    scene_number: int = 1,
    on_screen_text: str = "",
    education_level: str = "Enseñanza Media",
    width: int = TARGET_WIDTH,
    height: int = TARGET_HEIGHT
) -> str:
    """
    Genera la imagen ilustrativa para una escena educativa (100% en español).
    1. Prioridad: OpenAI gpt-image-2.6-sunburst (Máxima fidelidad, cero concept bleeding).
    2. Respaldo: AI Horde (Stable Diffusion descentralizado, costo $0).
    3. Respaldo secundario: Pollinations Flux.
    4. Respaldo determinista infográfico (Pillow con diseño esquemático y nivel MINEDUC en español).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 1. Prioridad: OpenAI gpt-image-2.6-sunburst (Máxima fidelidad, adaptado a la edad, sin anuncios)
    logger.info(f"[Imagen Escena {scene_number}] Intentando generación de alta fidelidad con OpenAI Sunburst ({education_level})...")
    if await _fetch_openai_sunburst_image(prompt, output_path, education_level, scene_number, width, height):
        return output_path

    # 2. Respaldo: AI Horde (Stable Diffusion descentralizado)
    logger.info(f"[Imagen Escena {scene_number}] Generando imagen con IA (AI Horde) para: '{prompt[:60]}...'")
    if await _fetch_ai_horde_image(prompt, output_path, width, height):
        return output_path

    # 3. Respaldo secundario: Pollinations Flux
    logger.info(f"[Imagen Escena {scene_number}] Intentando respaldo visual con Pollinations...")
    if await _fetch_pollinations_image(prompt, output_path, width, height):
        return output_path

    # 4. Respaldo determinista infográfico (Pillow con diseño esquemático y nivel MINEDUC en español)
    logger.info(f"[Imagen Escena {scene_number}] Generando lámina infográfica didáctica...")
    _generate_infographic_visual_slide(
        output_path=output_path,
        scene_number=scene_number,
        on_screen_text=on_screen_text,
        education_level=education_level,
        width=width,
        height=height
    )
    return output_path
