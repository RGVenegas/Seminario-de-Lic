import os
import sys
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Asegurar path para importar backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.graph.schemas import AudiovisualStoryboard, Scene
from backend.app.media.video_assembler import assemble_multimedia_video

async def test_full_media_assembly():
    print("=" * 70)
    print("DEMOSTRACIÓN DE ENSAMBLADO MULTIMEDIA: IMÁGENES IA + TTS NEURAL + VIDEO")
    print("=" * 70)

    # Escaleta de prueba con 3 escenas didácticas breves
    storyboard = AudiovisualStoryboard(
        video_title="La Ley de Conservación de la Energía",
        target_audience="Estudiantes de Secundaria",
        total_duration_seconds=15,
        scenes=[
            Scene(
                scene_number=1,
                duration_seconds=5,
                voiceover="Bienvenidos a esta cápsula didáctica. Hoy exploraremos uno de los principios más fascinantes de la física: la ley de conservación de la energía.",
                visual_description="Plano general de una montaña rusa ascendiendo con gráficos dinámicos.",
                on_screen_text="Ley de Conservación de la Energía: La base de la física universal",
                ai_image_prompt="A dynamic roller coaster climbing up a steep hill against a bright blue sky, clear educational science photography, 8k resolution"
            ),
            Scene(
                scene_number=2,
                duration_seconds=5,
                voiceover="Al llegar a la cima, el carro acumula energía potencial gravitatoria. Al caer en picada, esa energía se convierte en vertiginosa energía cinética.",
                visual_description="Infografía animada con barras de energía potencial y cinética intercambiándose.",
                on_screen_text="Transformación: Energía Potencial a Energía Cinética",
                ai_image_prompt="Diagram of kinetic and potential energy exchange, glowing blue and green energy vectors, clean modern science classroom illustration"
            ),
            Scene(
                scene_number=3,
                duration_seconds=5,
                voiceover="La energía jamás desaparece ni se crea de la nada; simplemente cambia de forma. ¡Nos vemos en la próxima lección!",
                visual_description="Resumen conceptual con fórmula fundamental E total = Ec + Ep.",
                on_screen_text="Principio Fundamental: La energía no se destruye, solo se transforma",
                ai_image_prompt="A glowing lightbulb surrounded by icons of wind, solar, and kinetic energy, symbolizing energy transformation, clean minimalist background"
            )
        ]
    )

    output_dir = os.path.join("backend", "output")
    result = await assemble_multimedia_video(
        storyboard=storyboard,
        output_dir=output_dir,
        voice="es-CL-LorenzoNeural",
        job_id="test_demo_clase"
    )

    print("\n" + "=" * 70)
    print("RESULTADO DEL ENSAMBLADO:")
    print("=" * 70)
    print(f"Estado:              EXITOSO")
    print(f"Título:              {result['title']}")
    print(f"Archivo generado:    {result['video_filename']}")
    print(f"Ruta física:         {result['video_path']}")
    print(f"Tamaño en disco:     {os.path.getsize(result['video_path']) / 1024:.1f} KB")
    print(f"Duración total:      {result['total_duration_seconds']} segundos")
    print(f"Número de escenas:   {result['scenes_count']}")
    for s in result["scenes"]:
        print(f"  - Escena {s['scene_number']}: {s['duration_seconds']}s | Audio: {s['audio_url']} | Imagen: {s['image_url']}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_full_media_assembly())

