import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_diagram():
    # Dimensions: 10 inches wide by 13.5 inches tall for crisp readability
    fig, ax = plt.subplots(figsize=(10, 13.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 13.5)
    ax.axis('off')

    # Color palette
    c_navy = "#003366"
    c_text_dark = "#0F172A"
    c_blue_bg = "#F8FAFC"
    c_blue_border = "#2563EB"
    c_amber_bg = "#FEF3C7"
    c_amber_border = "#D97706"
    c_red_bg = "#FEE2E2"
    c_red_border = "#DC2626"
    c_green_bg = "#ECFDF5"
    c_green_border = "#059669"

    # Helper for rounded boxes
    def draw_box(x, y, w, h, title, subtitle, doc_tag, bg_color, border_color, text_color=c_text_dark, tag_color="#1E3A8A", title_color=None):
        if title_color is None:
            title_color = border_color
            
        # Shadow
        rect_sh = patches.FancyBboxPatch((x+0.04, y-0.04), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                         facecolor="#E2E8F0", edgecolor="none", zorder=1)
        ax.add_patch(rect_sh)
        # Main Box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor=bg_color, edgecolor=border_color, linewidth=2, zorder=2)
        ax.add_patch(rect)
        
        # Title
        ax.text(x + w/2, y + h - 0.28, title, ha='center', va='center', fontsize=11, fontweight='bold', color=title_color, zorder=3)
        
        # Subtitle
        if subtitle:
            # calculate vertical center for subtitle
            sub_y = (y + 0.62 + (y + h - 0.42)) / 2 if doc_tag else (y + (y + h - 0.42)) / 2
            ax.text(x + w/2, sub_y, subtitle, ha='center', va='center', fontsize=8.8, color=text_color, zorder=3)
        
        # Deliverable Tag Box
        if doc_tag:
            tag_box = patches.FancyBboxPatch((x + 0.25, y + 0.12), w - 0.5, 0.44, boxstyle="round,pad=0.04,rounding_size=0.08",
                                            facecolor="#FFFFFF", edgecolor=tag_color, linewidth=1.4, zorder=3)
            ax.add_patch(tag_box)
            ax.text(x + w/2, y + 0.34, doc_tag, ha='center', va='center', fontsize=9.2, fontweight='bold', color=tag_color, zorder=4)

    # Coordinates:
    # Main column: x = 0.5, w = 6.2 (center = 3.6, right edge = 6.7)
    # Side column (Loop): x = 7.3, w = 2.4 (center = 8.5)
    
    # 1. ENTRADA DEL DOCENTE
    draw_box(0.5, 12.0, 6.2, 1.0, 
             "1. ENTRADA DEL DOCENTE (INTERFAZ WEB)", 
             "Ingreso de parámetros didácticos:\nTema / OA + Nivel Educativo + Duración de clase", 
             None, "#FFFFFF", c_navy)

    # 2. AGENTE PEDAGÓGICO
    draw_box(0.5, 10.1, 6.2, 1.4, 
             "2. AGENTE PEDAGÓGICO (Fase 1: Planificación)", 
             "Estructura los momentos y tiempos de la lección adaptados etariamente", 
             "Entrega: PLANIFICACIÓN DIDÁCTICA (Inicio, Desarrollo y Cierre)", 
             c_blue_bg, c_blue_border)

    # 3. AGENTE TEÓRICO
    draw_box(0.5, 8.2, 6.2, 1.4, 
             "3. AGENTE TEÓRICO (Fase 2: Contenido)", 
             "Toma la planificación y redacta la base conceptual rigurosa y metáforas", 
             "Entrega: GUION TEÓRICO (Marco Científico + Analogía + Glosario)", 
             c_blue_bg, c_blue_border)

    # 4. AGENTE AUDIOVISUAL
    draw_box(0.5, 6.3, 6.2, 1.4, 
             "4. AGENTE AUDIOVISUAL (Fase 3: Escaleta)", 
             "Traduce el guion a formato audiovisual multimedia escena por escena", 
             "Entrega: ESCALETA AUDIOVISUAL (Locución + Subtítulo + Prompt IA)", 
             c_blue_bg, c_blue_border)

    # 5. AGENTE REVISOR (QC)
    draw_box(0.5, 4.25, 6.2, 1.55, 
             "5. AGENTE REVISOR / QUALITY CONTROL (Auditoría)", 
             "Audita 7 Criterios: Coherencia OA-Guion, congruencia Locución-Imagen\n¿Score Global Ponderado >= 85%?", 
             "Emite: REPORTE DE AUDITORÍA PEDAGÓGICA (7 Criterios)", 
             c_amber_bg, c_amber_border, text_color="#78350F", tag_color="#B45309")

    # BUCLE DE MEJORA (Side Box)
    draw_box(7.2, 7.2, 2.5, 2.6,
             "BUCLE DE MEJORA", 
             "Auditoría rechazada:\nRedirige el artefacto\ncon retroalimentación\nespecífica al agente\nresponsable.\n\n(Máximo 2 iteraciones)", 
             None, c_red_bg, c_red_border, text_color="#991B1B")

    # 6. MOTOR DETERMINISTA MULTIMEDIA
    draw_box(0.5, 2.15, 6.2, 1.6, 
             "6. MOTOR DETERMINISTA MULTIMEDIA (MoviePy + Edge-TTS)", 
             "Toma la Escaleta aprobada y ensambla sin alucinaciones de código:\n• Síntesis de voz neural en español (Edge-TTS)\n• Generación de ilustraciones educativas con IA (AI Horde)\n• Estampado de franja inferior (Lower-Third) y composición MoviePy", 
             "Procesa: Sincronización y Renderizado Cuadro a Cuadro", 
             c_green_bg, c_green_border, text_color="#064E3B", tag_color="#047857")

    # 7. RESULTADO FINAL
    draw_box(0.5, 0.4, 6.2, 1.25, 
             "7. RESULTADO FINAL PARA EL DOCENTE", 
             "Video Educativo MP4 continuo sincronizado al milisegundo (1280x720 H.264)\nPaquete pedagógico completo: Planificación + Guion + Escaleta + Audios", 
             None, "#003366", "#001F3F", text_color="#E2E8F0", title_color="#FFFFFF")

    # ARROWS & CONNECTORS
    arrow_props = dict(arrowstyle="-|>,head_width=0.35,head_length=0.45", linewidth=2.0, color="#003366")
    arrow_pass = dict(arrowstyle="-|>,head_width=0.45,head_length=0.55", linewidth=3.0, color="#059669")
    arrow_fail = dict(arrowstyle="-|>,head_width=0.35,head_length=0.45", linewidth=2.0, color="#DC2626")

    # 1 -> 2
    ax.annotate("", xy=(3.6, 11.5), xytext=(3.6, 12.0), arrowprops=arrow_props)
    # 2 -> 3
    ax.annotate("", xy=(3.6, 9.6), xytext=(3.6, 10.1), arrowprops=arrow_props)
    # 3 -> 4
    ax.annotate("", xy=(3.6, 7.7), xytext=(3.6, 8.2), arrowprops=arrow_props)
    # 4 -> 5
    ax.annotate("", xy=(3.6, 5.8), xytext=(3.6, 6.3), arrowprops=arrow_props)

    # 5 -> 6 (APROBADO)
    ax.annotate("", xy=(3.6, 3.75), xytext=(3.6, 4.25), arrowprops=arrow_pass)
    ax.text(3.6, 4.0, "[APROBADO] Score >= 85%", fontsize=9.2, fontweight='bold', color="#059669", 
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#059669", linewidth=1.2))

    # 6 -> 7
    ax.annotate("", xy=(3.6, 1.65), xytext=(3.6, 2.15), arrowprops=arrow_pass)

    # RECHAZADO: 5 -> Loop Box
    # From right of Box 5 (6.7, 5.0) horizontally to (8.45, 5.0) and up to bottom of Loop Box (8.45, 7.2)
    ax.plot([6.7, 8.45], [5.0, 5.0], color="#DC2626", linewidth=2.0, linestyle="--")
    ax.text(7.55, 5.0, "[RECHAZADO]\nScore < 85%", fontsize=8, fontweight='bold', color="#DC2626", ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#DC2626", linewidth=1.0))
    ax.annotate("", xy=(8.45, 7.2), xytext=(8.45, 5.0),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.45", linewidth=2.0, color="#DC2626", linestyle="--"))

    # LOOP BACK: From top of Loop Box (8.45, 9.8) up to 10.8 and left to Box 2 (6.7, 10.8)
    ax.plot([8.45, 8.45], [9.8, 10.8], color="#DC2626", linewidth=2.0, linestyle="--")
    ax.annotate("", xy=(6.7, 10.8), xytext=(8.45, 10.8),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.45", linewidth=2.0, color="#DC2626", linestyle="--"))
    ax.text(7.55, 10.8, "Reenvío con\nobservaciones", fontsize=8, fontweight='bold', color="#DC2626", ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#DC2626", linewidth=1.0))

    plt.tight_layout()
    out_path = "figura1_arquitectura_agentes.png"
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Diagrama guardado exitosamente en: {out_path}")

if __name__ == "__main__":
    draw_diagram()
