import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client
import fitz

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=35, bottom=35, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_e2_document():
    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

        # Encabezado
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "Plantilla acumulativa | Ingeniería Civil Informática"
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hp.runs[0].font.name = "Arial"
        hp.runs[0].font.size = Pt(8)
        hp.runs[0].font.color.rgb = RGBColor(100, 116, 139)

        # Pie de página
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "CINF200 | Entrega 2 (E2)"
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fp.runs[0].font.name = "Arial"
        fp.runs[0].font.size = Pt(8)
        fp.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    # Estilos base
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(9)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.10
    normal_style.paragraph_format.space_after = Pt(2.5)

    def add_h(text, size=11, bold=True, color=(0, 51, 102), before=3, after=1.5):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = RGBColor(*color)
        return p

    def add_p(text, before=0, after=2.5, bold=False, italic=False, color=(30, 41, 59), size=9):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = RGBColor(*color)
        return p

    # =========================================================================
    # PÁGINA 1: PORTADA
    # =========================================================================
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("Universidad Andrés Bello\nFacultad de Ingeniería · Escuela de Informática")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0, 51, 102)

    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_code = p_code.add_run("CINF200")
    r_code.font.name = "Arial"
    r_code.font.size = Pt(11.5)
    r_code.font.bold = True
    r_code.font.color.rgb = RGBColor(185, 28, 28)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Plantilla acumulativa de informe\nVersión de trabajo para E1, E2 y E3")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(16.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Entrega 2 (E2): Implementación del Grafo DAG en LangGraph, Orquestación Multi-Proveedor y Ensamblado Determinista Multimedia")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(71, 85, 105)
    p_sub.paragraph_format.space_after = Pt(24)

    t0 = doc.add_table(rows=8, cols=2)
    t0.alignment = WD_TABLE_ALIGNMENT.CENTER
    t0_data = [
        ("Campo", "Información"),
        ("Asignatura", "CINF200 — Seminario de Licenciatura en Ciencias de la Ingeniería"),
        ("Carrera", "Ingeniería Civil Informática"),
        ("Periodo", "Octavo semestre"),
        ("Estudiantes / equipo", "Rodrigo Venegas · Pablo Loncon · Francisco Espinoza"),
        ("Docente tutor", "Docente Tutor / Comisión Evaluadora CINF200"),
        ("Sede", "Viña del mar"),
        ("Semestre / Entrega", "2026-2 · Entrega 2 (E2)")
    ]
    for row_idx, (c1, c2) in enumerate(t0_data):
        row = t0.rows[row_idx]
        cell_1, cell_2 = row.cells[0], row.cells[1]
        cell_1.text, cell_2.text = c1, c2
        cell_1.width, cell_2.width = Inches(2.2), Inches(4.5)
        set_cell_margins(cell_1, top=55, bottom=55, left=90, right=90)
        set_cell_margins(cell_2, top=55, bottom=55, left=90, right=90)
        if row_idx == 0:
            set_cell_background(cell_1, "003366")
            set_cell_background(cell_2, "003366")
            for c in (cell_1, cell_2):
                p = c.paragraphs[0]
                p.runs[0].font.bold = True
                p.runs[0].font.size = Pt(9)
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            if row_idx % 2 == 1:
                set_cell_background(cell_1, "F8FAFC")
                set_cell_background(cell_2, "F8FAFC")
            cell_1.paragraphs[0].runs[0].font.bold = True
            cell_1.paragraphs[0].runs[0].font.size = Pt(8.5)
            cell_2.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 2: RESUMEN, PALABRAS CLAVE E ÍNDICE GENERAL (HASTA SECCIÓN 4)
    # =========================================================================
    add_h("Resumen", size=12.5, before=0, after=2)
    add_p(
        "El presente proyecto aborda la problemática de la desalineación pedagógica, curricular y comunicacional "
        "que ocurre al utilizar modelos de Inteligencia Artificial Generativa aislados o monolíticos (Single Prompt) "
        "para la preparación de material educativo. Para reducir el riesgo técnico y garantizar la factibilidad del "
        "periodo académico, la primera versión (MVP) de la solución se concentra exclusivamente en la generación "
        "secuencial de una clase multimedia breve (15 a 20 minutos de duración conceptual), estructurada a partir de "
        "un Objetivo de Aprendizaje (OA), nivel educativo y tiempo disponible."
    )
    add_p(
        "La solución propuesta reemplaza el enfoque monolítico por una Arquitectura Multiagente guiada por un Grafo "
        "Acíclico Dirigido (DAG), coordinada mediante LangGraph en Python 3.12 con tipado estricto en Pydantic. El flujo se divide en 3 fases "
        "secuenciales estrictamente dependientes (Planificación Pedagógica, Desarrollo Teórico & Guion, y Producción "
        "Audiovisual), donde cada etapa cuenta con un ciclo de revisión interno de 4 pasos (Producir ➔ Verificar ➔ "
        "Corregir ➔ Aprobar). Adicionalmente, se incluye un Agente Revisor (Quality Control) dotado de una matriz cualitativa/cuantitativa "
        "de 7 criterios peda-comunicacionales con un umbral de aprobación del 85%. Como hito central de E2, se consolidó una "
        "Fábrica Multi-Proveedor Heterogénea (Google Gemini 2.5 Flash / 3.5 Flash Lite, OpenAI GPT-4o-mini y Servidor Institucional Quotas DevHub con control de "
        "consumo de tokens) y un Motor Determinista Multimedia basado en Edge-TTS (con voz neural chilena es-CL-LorenzoNeural), IA visual descentralizada "
        "(AI Horde / Stable Diffusion) y MoviePy para el ensamblado de video MP4 continuo con subtítulos interactivos lower-third. Todo el sistema ha sido "
        "adaptado al currículum chileno (MINEDUC), reduciendo el tiempo de diseño docente de 6 horas a menos de 1 minuto."
    )

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(2)
    p_kw.paragraph_format.space_after = Pt(6)
    r_kwt = p_kw.add_run("Palabras clave: ")
    r_kwt.font.bold = True
    r_kwt.font.size = Pt(9)
    r_kwt.font.color.rgb = RGBColor(0, 51, 102)
    r_kwd = p_kw.add_run("Inteligencia Artificial Multiagente · Grafo Acíclico Dirigido (DAG) · LangGraph · Alineación Pedagógica · MoviePy/FFmpeg · Clases Multimedia Editables")
    r_kwd.font.size = Pt(9)

    add_h("Índice general", size=11.5, before=3, after=2)
    index_p1 = [
        ("Resumen", "2"),
        ("Palabras clave", "2"),
        ("Índice general", "2"),
        ("Índice de tablas", "3"),
        ("Índice de figuras", "3"),
        ("1. Introducción", "4"),
        ("2. Problema y fundamentación", "4"),
        ("   2.1 Diagnóstico, necesidad y contexto", "4"),
        ("   2.2 Pregunta de investigación o desafío de ingeniería", "5"),
        ("   2.3 Pertinencia tecnológica y valor organizacional", "5"),
        ("   2.4 Factibilidad, responsabilidad y riesgos", "5"),
        ("3. Objetivos", "5"),
        ("   3.1 Objetivo general", "5"),
        ("   3.2 Objetivos específicos", "5"),
        ("4. Estado del arte y antecedentes", "6")
    ]
    for itm, pg in index_p1:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.space_before = Pt(0)
        p_it.paragraph_format.space_after = Pt(1)
        r_it1 = p_it.add_run(itm)
        r_it1.font.size = Pt(8.5)
        dots = max(3, 75 - len(itm) - len(pg))
        r_dots = p_it.add_run(" " + "." * dots + " " + pg)
        r_dots.font.size = Pt(8.5)
        r_dots.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 3: ÍNDICE GENERAL (CONT.), ÍNDICE DE TABLAS Y DE FIGURAS
    # =========================================================================
    index_p2 = [
        ("5. Metodología", "6"),
        ("6. Requisitos, alcance y planificación", "7"),
        ("   6.1 Requisitos y criterios de aceptación", "7"),
        ("   6.2 Alcance, restricciones y supuestos", "7"),
        ("   6.3 Plan de trabajo y gestión", "7"),
        ("7. Diseño y arquitectura de la solución", "8"),
        ("8. Implementación y producto mínimo viable", "9"),
        ("9. Evaluación y resultados", "9"),
        ("   9.1 Criterios, métricas y protocolo de evaluación", "9"),
        ("   9.2 Resultados técnicos", "10"),
        ("   9.3 Valor, impacto y limitaciones", "10"),
        ("10. Discusión", "10"),
        ("11. Conclusiones y trabajo futuro", "10"),
        ("Referencias", "11"),
        ("Anexos", "11"),
        ("   Anexo A. Declaración de uso de inteligencia artificial", "11"),
        ("   Anexo B. Contribución individual", "11"),
        ("   Anexo C. Evidencias complementarias de E3", "12")
    ]
    for itm, pg in index_p2:
        p_it = doc.add_paragraph()
        p_it.paragraph_format.space_before = Pt(0)
        p_it.paragraph_format.space_after = Pt(1)
        r_it1 = p_it.add_run(itm)
        r_it1.font.size = Pt(8.5)
        dots = max(3, 75 - len(itm) - len(pg))
        r_dots = p_it.add_run(" " + "." * dots + " " + pg)
        r_dots.font.size = Pt(8.5)
        r_dots.font.color.rgb = RGBColor(100, 116, 139)

    add_h("Índice de tablas", size=11.5, before=6, after=2)
    tables_idx = [
        ("Tabla 0: Metadatos Institucionales del Proyecto", "Portada"),
        ("Tabla 1: Matriz Causal (Monolítico vs. DAG Multiagente)", "Sección 2.1"),
        ("Tabla 2: Pipeline Metodológico de Agentes y Síntesis Multimedia", "Sección 5"),
        ("Tabla 3: Matriz de Delimitación de Alcance para MVP", "Sección 6.2"),
        ("Tabla 4: Matriz de Auditoría del Agente Revisor (7 Criterios)", "Sección 9.1"),
        ("Tabla 5: Indicadores y Métricas del Protocolo de Evaluación", "Sección 9.3"),
        ("Tabla 6: Matriz de Contribución Individual por Integrante", "Anexo B"),
        ("Tabla 7: Evidencias Complementarias del Proyecto (E3)", "Anexo C")
    ]
    for t_it, t_pg in tables_idx:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(1)
        r_ti = p_t.add_run(t_it)
        r_ti.font.size = Pt(8.5)
        dots = max(3, 72 - len(t_it) - len(t_pg))
        r_dots = p_t.add_run(" " + "." * dots + " " + t_pg)
        r_dots.font.size = Pt(8.5)
        r_dots.font.color.rgb = RGBColor(100, 116, 139)

    add_h("Índice de figuras", size=11.5, before=5, after=2)
    p_f = doc.add_paragraph()
    r_fi = p_f.add_run("Figura 1: Arquitectura del Sistema Multiagente DAG por Fases con Loops Acotados")
    r_fi.font.size = Pt(8.5)
    dots = max(3, 72 - len(r_fi.text) - len("Sección 7 (Pág. 8)"))
    r_dots = p_f.add_run(" " + "." * dots + " Sección 7 (Pág. 8)")
    r_dots.font.size = Pt(8.5)
    r_dots.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 4: 1. INTRODUCCIÓN Y 2. PROBLEMA Y FUNDAMENTACIÓN (CON TABLA 1)
    # =========================================================================
    add_h("1. Introducción", size=12, before=0, after=2)
    add_p(
        "La acelerada masificación de las herramientas de Inteligencia Artificial Generativa (IAG) en las instituciones "
        "educativas ha transformado el diseño de materiales docentes. Pese al notable potencial de los Modelos de "
        "Lenguaje de Gran Escala (LLMs), los profesores enfrentan una dificultad recurrente al utilizarlos: los "
        "enfoques tradicionales basados en un solo prompt (Single Prompt) tienden a generar guiones didácticos "
        "desarticulados, donde los contenidos teóricos no responden al Objetivo de Aprendizaje (OA) configurado, la "
        "locución hablada contradice el texto visible en pantalla y la densidad informativa satura la capacidad del estudiante."
    )
    add_p(
        "Este proyecto propone una solución de ingeniería basada en un Sistema de IA Multiagente estructurado "
        "bajo una arquitectura de Grafo Acíclico Dirigido (DAG). En lugar de sobrecargar un único llamado a la API, "
        "el sistema distribuye las tareas entre agentes especializados en planificación pedagógica, desarrollo de "
        "contenidos y producción audiovisual. La ejecución es coordinada de manera determinista y modular "
        "mediante el framework LangGraph, separando la generación del conocimiento de la producción multimedia "
        "técnica (FFmpeg / MoviePy / Edge-TTS), reduciendo el tiempo de preparación docente de 6 horas a menos de 1 minuto por recurso."
    )

    add_h("2. Problema y fundamentación", size=12, before=3, after=1.5)
    add_p("A continuación se presenta el diagnóstico detallado del problema de desalineación didáctica en sistemas de IA monolíticos, fundamentando la necesidad de una arquitectura por fases independientes.")

    add_h("2.1 Diagnóstico, necesidad y contexto", size=10.5, before=2, after=1.5)

    # Tabla 1: Matriz Causal
    t1 = doc.add_table(rows=5, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_data = [
        ("Causa Raíz (Monolítico)", "Efecto Didáctico", "Solución DAG Multiagente"),
        ("Sobrecarga de contexto en 1 prompt", "Alucinación y dispersión del Objetivo (OA)", "Descomposición en 3 fases secuenciales independientes en LangGraph"),
        ("Falta de dependencias de tiempo", "Escaleta de video generada sin guion aprobado", "Grafo DAG donde la salida aprobada de la fase anterior es insumo"),
        ("Modelo complaciente sin auditoría", "Texto desfasado con locución y sobrecarga", "Agente Revisor (QC) con matriz de 7 criterios (Score >= 85%)"),
        ("Llamadas API intentando crear video", "Fallas de sintaxis y falta de editabilidad", "Ensamblador determinista desacoplado (FFmpeg / MoviePy / Edge-TTS)")
    ]
    for row_idx, (c1, c2, c3) in enumerate(t1_data):
        row = t1.rows[row_idx]
        for col_idx, text in enumerate((c1, c2, c3)):
            cell = row.cells[col_idx]
            cell.text = text
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(8)
            if row_idx == 0:
                set_cell_background(cell, "003366")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if row_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")

    add_p(
        "El diagnóstico técnico-pedagógico identifica que el fallo de los LLMs monolíticos radica en la pérdida de foco "
        "conceptual ante llamadas multi-propósito. Al exigir planificación didáctica, desarrollo conceptual y escaleta "
        "audiovisual en una sola consulta, el modelo incurre en alucinaciones didácticas y violaciones de la Teoría de la Carga Cognitiva.\n"
        "Los docentes de educación secundaria y terciaria requieren herramientas automatizadas que garanticen rigor "
        "metodológico sin aumentar la carga de trabajo administrativo. La solución responde a esta necesidad mediante una Matriz "
        "Causal que relaciona las falencias del modelo monolítico con las oportunidades de la arquitectura DAG:"
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 5: 2.2 A 2.4 Y 3. OBJETIVOS
    # =========================================================================
    add_h("2.2 Pregunta de investigación o desafío de ingeniería", size=10.5, before=0, after=1.5)
    add_p("¿Cómo diseñar e implementar un sistema de IA multiagente basado en grafos acíclicos dirigidos (DAG) y ensamblaje determinista que garantice la alineación pedagógica, la factibilidad temporal y la coherencia audiovisual en la generación de clases multimedia breves?")

    add_h("2.3 Pertinencia tecnológica y valor organizacional", size=10.5, before=2.5, after=1.5)
    add_p("La pertinencia tecnológica se fundamenta en la combinación de orquestación inteligente de estados mutables mediante LangGraph (Python 3.12) con motores deterministas de video (FFmpeg / MoviePy / Edge-TTS). Esto permite a las instituciones educativas estandarizar la calidad pedagógica de sus recursos, asegurando que cada clase generada cumpla con los estándares curriculares y ofreciendo un paquete de assets completamente editables para el docente.")

    add_h("2.4 Factibilidad, responsabilidad y riesgos", size=10.5, before=2.5, after=1.5)
    add_p(
        "Para asegurar la viabilidad del proyecto durante el periodo académico, la primera versión (MVP) acota su "
        "alcance exclusivamente a la generación de una clase multimedia breve (15-20 min), difiriendo la complejidad de "
        "múltiples exportadores SCORM o integraciones con LMS masivos.\n"
        "Entre los riesgos técnicos identificados destacan los bucles infinitos en los loops de revisión (mitigados con un "
        "límite estricto de 2 iteraciones por fase), la latencia por llamadas a API (optimizada mediante esquemas JSON estructurados "
        "en Pydantic) y la gestión de créditos institucionales (mitigado mediante interruptor de cuota USE_INSTITUTIONAL_QUOTA y conmutación "
        "heterogénea hacia Google Gemini y OpenAI)."
    )

    add_h("3. Objetivos", size=12, before=3, after=1.5)
    add_p("A continuación se definen el objetivo general y los objetivos específicos verificables del proyecto.")

    add_h("3.1 Objetivo general", size=10.5, before=2, after=1.5)
    add_p("Desarrollar un sistema de IA multiagente guiado por una arquitectura de Grafo Acíclico Dirigido (DAG) y ensamblaje determinista para la generación secuencial de una clase multimedia breve, garantizando la coherencia pedagógica y audiovisual mediante ciclos acotados de auditoría de calidad.")

    add_h("3.2 Objetivos específicos", size=10.5, before=2, after=1.5)
    oes_e2 = [
        ("OE1: Diseñar e implementar el pipeline pedagógico secuencial estructurado en 3 fases principales (Planificación Pedagógica, Desarrollo Teórico y Producción Audiovisual) para garantizar la continuidad y alineación temática.", " [COMPLETADO EN E2]"),
        ("OE2: Codificar el Agente Revisor (Quality Control) incorporando una matriz de auditoría cualitativa y cuantitativa estructurada en 7 criterios peda-comunicacionales con un umbral mínimo de aprobación del 85%.", " [COMPLETADO EN E2]"),
        ("OE3: Construir el motor de orquestación backend en Python 3.12 apoyado en el framework LangGraph para gestionar la persistencia del estado mutable y controlar los loops de corrección (máximo 2 iteraciones por fase).", " [COMPLETADO EN E2]"),
        ("OE4: Integrar un componente determinista de ensamblaje multimedia basado en FFmpeg y MoviePy para la renderización de escaletas, locución y subtítulos sin riesgo de alucinación en el código de video.", " [COMPLETADO EN E2]")
    ]
    for oet, oes in oes_e2:
        p_oe = doc.add_paragraph()
        p_oe.paragraph_format.space_before = Pt(0.5)
        p_oe.paragraph_format.space_after = Pt(1.5)
        r1 = p_oe.add_run(f"• {oet}")
        r1.font.size = Pt(8.5)
        r2 = p_oe.add_run(oes)
        r2.font.bold = True
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = RGBColor(16, 185, 129)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 6: 4. ESTADO DEL ARTE, 5. METODOLOGÍA Y 6.1 REQUISITOS (INICIO)
    # =========================================================================
    add_h("4. Estado del arte y antecedentes", size=12, before=0, after=1.5)
    add_p(
        "El marco teórico de la solución se consolida en tres pilares fundamentales:\n"
        "1. Alineación Constructiva (Biggs & Tang, 2011): Fundamenta que el aprendizaje efectivo exige sincronía "
        "absoluta entre los Objetivos de Aprendizaje (OA), las actividades diseñadas y la evaluación. Nuestro Agente "
        "Revisor audita sistemáticamente esta alineación.\n"
        "2. Teoría de la Carga Cognitiva y Aprendizaje Multimedia (Sweller, 2011; Mayer, 2014): Demuestra que la "
        "sobrecarga de información escrita sumada a locuciones no concordantes inhibe la retención. La arquitectura "
        "regula la densidad de información por escena y exige coincidencia locución-imagen-texto.\n"
        "3. Orquestación Multiagente Basada en Grafos (Wu et al., 2023; LangChain, 2024): A diferencia de los "
        "sistemas de agentes conversacionales genéricos (como AutoGen tradicional) que corren riesgo de ciclos "
        "divergentes, LangGraph permite formalizar el flujo como un Grafo Acíclico Dirigido (DAG) con estados "
        "explícitos y condiciones de parada acotadas.\n"
        "Brecha Identificada: No existe actualmente en el mercado ni en la literatura académica una plataforma que "
        "combine la generación secuencial DAG con una matriz de auditoría didáctica de 7 criterios y un motor "
        "determinista de video desacoplado de las alucinaciones de IA."
    )

    add_h("5. Metodología", size=12, before=2, after=1)
    add_p(
        "El proyecto adopta una metodología de ingeniería de software orientada a componentes modulares. El desarrollo "
        "se estructura en un pipeline desacoplado que combina agentes cognitivos secuenciales en LangGraph con un motor "
        "determinista multimedia en MoviePy y Edge-TTS. La Tabla 2 resume la matriz metodológica de etapas, insumos, "
        "procesamiento didáctico, artefactos generados y mecanismos de control de calidad aplicados:",
        size=8.2
    )

    # Tabla 2: Metodología
    t_metod = doc.add_table(rows=8, cols=5)
    t_metod.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_metod_data = [
        ("Fase / Módulo", "Componente", "Insumo (Input)", "Técnica / Procesamiento", "Salida y Control de Calidad"),
        ("Fase 1: Planificación", "Agente Pedagógico (LLM)", "OA, Nivel Educativo, Duración", "Dosificación temporal por momentos didácticos (Inicio, Desarrollo, Cierre)", "LessonPlan (JSON) · Ciclo 4 pasos (máx. 2 iteraciones)"),
        ("Fase 2: Contenido", "Agente Teórico (LLM)", "Planificación aprobada", "Redacción conceptual rigurosa, analogías cotidianas y glosario etario", "TheoreticalScript (JSON) · Control de rigor y vocabulario"),
        ("Fase 3: Escaleta", "Agente Audiovisual (LLM)", "Plan + Guion aprobados", "Guionización escena por escena, locución hablada y prompts visuales", "AudiovisualStoryboard (JSON) · Sincronía locución-pantalla"),
        ("Fase 4: Auditoría (QC)", "Agente Revisor (LLM)", "Escaleta consolidada", "Auditoría analítica con 7 criterios didácticos y comunicacionales ponderados", "AuditReport · Umbral Score >= 85% (Rechazo genera feedback)"),
        ("Síntesis de Voz (TTS)", "Motor Edge-TTS", "Locución por escena (voiceover)", "Síntesis neural de voz en español de alta naturalidad y fluidez", "Pistas .mp3 individuales · Medición de duración real"),
        ("Ilustraciones con IA", "Stable Diffusion + PIL", "Prompts visuales en inglés", "Inferencia generativa 16:9 (1280x720) y estampado Lower-Third", "Imágenes .jpg compuestas · Prompts negativos anti-deformación"),
        ("Ensamblado Multimedia", "MoviePy / FFmpeg", "Audios .mp3 + Imágenes .jpg", "Concatenación continua cuadro a cuadro desacoplada de código LLM", "Video educativo MP4 (1280x720 H.264) continuo garantizado")
    ]
    col_widths_m = [Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.8), Inches(1.6)]
    for r_i, r_data in enumerate(t_metod_data):
        row = t_metod.rows[r_i]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.text = val
            cell.width = col_widths_m[c_i]
            set_cell_margins(cell, top=25, bottom=25, left=35, right=35)
            p_cell = cell.paragraphs[0]
            p_cell.runs[0].font.size = Pt(7.2)
            if r_i == 0:
                set_cell_background(cell, "003366")
                p_cell.runs[0].font.bold = True
                p_cell.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_i % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                if c_i == 0:
                    p_cell.runs[0].font.bold = True

    add_p(
        "Loops Acotados de 4 Pasos: Cada una de las 3 fases cognitivas ejecuta internamente el ciclo Producir ➔ Verificar ➔ "
        "Corregir ➔ Aprobar, con un límite estricto de máximo 2 iteraciones para prevenir bucles divergentes.",
        size=7.8
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 7: 6. REQUISITOS (RF Y RNF COMPLETOS), 6.2 ALCANCE (TABLA 3) Y 6.3 HITOS
    # =========================================================================
    add_h("6. Requisitos, alcance y planificación", size=12, before=0, after=1.5)
    add_p("Se presentan los requisitos del sistema, la delimitación formal del alcance para el MVP y la hoja de ruta actualizada de hitos.", size=8.2)

    add_h("6.1 Requisitos y criterios de aceptación", size=10.5, before=1.5, after=1)
    add_p("• Requisitos Funcionales:", size=8.2)
    add_p("  - RF1: Ingreso de parámetros didácticos (OA, Nivel Educativo, Duración en minutos, Enfoque pedagógico).", size=8.0)
    add_p("  - RF2: Orquestación DAG secuencial con LangGraph garantizando dependencias de salida inmutables.", size=8.0)
    add_p("  - RF3: Ciclos de revisión con un límite estricto de máximo 2 iteraciones por fase.", size=8.0)
    add_p("  - RF4: Evaluación cuantitativa mediante el Agente Revisor con matriz de 7 criterios (Umbral Score >= 85%).", size=8.0)
    add_p("  - RF5: Renderizado de video MP4 continuo y exportación de assets editables mediante MoviePy y Edge-TTS.", size=8.0)
    add_p("• Requisitos No Funcionales:", size=8.2)
    add_p("  - RNF1 (Modularidad): Código desacoplado en FastAPI + LangGraph en Python 3.12 con tipado estricto Pydantic.", size=8.0)
    add_p("  - RNF2 (Concurrencia): Procesamiento asíncrono de tareas de inferencia y renderizado determinista.", size=8.0)
    add_p("  - RNF3 (Usabilidad): Interfaz web moderna con estética Glassmorphism para revisión docente en tiempo real.", size=8.0)

    add_h("6.2 Alcance, restricciones y supuestos", size=10.5, before=2, after=1)
    add_p("A continuación se presenta la Tabla 3 completada con la especificación del alcance incluido y excluido para la primera versión (MVP):", size=8.5)

    add_h("6.3 Plan de trabajo y gestión", size=10.5, before=1.5, after=1)
    add_p("El proyecto se estructura en 12 hitos clave de ejecución distribuidos entre las entregas E1, E2 y E3:", size=8.0)
    hitos_p7 = [
        ("• Hito 1 (Completado):", "Definición de arquitectura DAG secuencial y acotamiento de alcance a MVP (Clase Multimedia Breve)."),
        ("• Hito 2 (Completado):", "Especificación detallada de agentes, loops de 4 pasos y matriz de 7 criterios del Agente Revisor."),
        ("• Hito 3 (Completado):", "Prototipo web interactivo (HTML5/CSS) y simulación del flujo de estados."),
        ("• Hito 4 (Completado en E2):", "Configuración del backend en FastAPI con Python 3.12."),
        ("• Hito 5 (Completado en E2):", "Programación del grafo de estados mutables y nodos de agentes con LangGraph."),
        ("• Hito 6 (Completado en E2):", "Integración de prompts estructurados por fase y esquemas JSON con Pydantic."),
        ("• Hito 7 (Completado en E2):", "Desarrollo de los ciclos acotados de revisión (Producir ➔ Verificar ➔ Corregir ➔ Aprobar)."),
        ("• Hito 8 (Completado en E2):", "Programación del módulo determinista de video (MoviePy / Edge-TTS / AI Horde) para la renderización MP4."),
        ("• Hito 9 (Completado en E2):", "Pruebas de integración, evaluación del Agente Revisor y optimización de latencia."),
        ("• Hito 10 (En progreso / E3):", "Mejora de la Calidad de imágenes creadas por la IA para un mejor entendimiento y visualización de la clase."),
        ("• Hito 11 (E3):", "Empaquetado multimodal y exportación de activos didácticos editables (guiones, audios, imágenes y formato SCORM/HTML5)."),
        ("• Hito 12 (E3):", "Optimización de rendimiento (paralelización asíncrona de síntesis multimedia) y preparación para la defensa final de titulación.")
    ]
    for ht, hd in hitos_p7:
        p_h = doc.add_paragraph()
        p_h.paragraph_format.space_before = Pt(0)
        p_h.paragraph_format.space_after = Pt(0.5)
        r_ht = p_h.add_run(f"{ht} ")
        r_ht.font.size = Pt(8)
        r_ht.font.bold = True
        if "Completado" in ht:
            r_ht.font.color.rgb = RGBColor(16, 185, 129)
        else:
            r_ht.font.color.rgb = RGBColor(217, 119, 6)
        r_hd = p_h.add_run(hd)
        r_hd.font.size = Pt(8)

    # Tabla 2: Alcance
    t2 = doc.add_table(rows=6, cols=2)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_data = [
        ("Elemento", "Contenido"),
        ("Usuarios / actores", "Docentes de educación secundaria y terciaria, diseñadores instruccionales y centros de innovación educativa."),
        ("Alcance incluido", "Generación secuencial de una clase multimedia breve (15-20 min), guion pedagógico, escaleta escena por escena, reporte QC, ilustraciones educativas con IA y video MP4 continuo ensamblado con voz neural en español."),
        ("Alcance excluido", "Exportación SCORM/PPTX masiva, gestión de usuarios/autenticación completa y persistencia en base de datos de producción."),
        ("Riesgos principales", "Bucles infinitos en loops de corrección (mitigado con máx. 2 iteraciones), latencia de APIs (mitigado con JSON estricto) e inconsistencias visuales en modelos de difusión abiertos (mitigado con prompts negativos y optimización visual en E3)."),
        ("Plan de trabajo", "Desarrollo modular estructurado en 12 hitos, abarcando desde la definición de la arquitectura DAG y pipeline multiagente, hasta la optimización de fidelidad conceptual de imágenes con IA, empaquetado de recursos y defensa final de titulación (E3).")
    ]
    for row_idx, (c1, c2) in enumerate(t2_data):
        row = t2.rows[row_idx]
        cell_1, cell_2 = row.cells[0], row.cells[1]
        cell_1.text, cell_2.text = c1, c2
        cell_1.width, cell_2.width = Inches(2.1), Inches(4.7)
        set_cell_margins(cell_1, top=30, bottom=30, left=50, right=50)
        set_cell_margins(cell_2, top=30, bottom=30, left=50, right=50)
        cell_1.paragraphs[0].runs[0].font.size = Pt(8)
        cell_2.paragraphs[0].runs[0].font.size = Pt(8)
        if row_idx == 0:
            set_cell_background(cell_1, "003366")
            set_cell_background(cell_2, "003366")
            for c in (cell_1, cell_2):
                c.paragraphs[0].runs[0].font.bold = True
                c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            if row_idx % 2 == 1:
                set_cell_background(cell_1, "F8FAFC")
                set_cell_background(cell_2, "F8FAFC")
            cell_1.paragraphs[0].runs[0].font.bold = True

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 8: 7. DISEÑO Y ARQUITECTURA DE LA SOLUCIÓN (FIGURA 1)
    # =========================================================================
    add_h("7. Diseño y arquitectura de la solución", size=12, before=0, after=2)
    add_p(
        "La arquitectura del sistema se diseña como un Grafo Acíclico Dirigido (DAG) desacoplado en dos grandes bloques: "
        "la Orquestación Inteligente basada en agentes cognitivos (LangGraph) y el Motor Determinista Multimedia (MoviePy + Edge-TTS). "
        "A continuación, la Figura 1 detalla la topología de los agentes especializados, los entregables pedagógicos generados "
        "en cada fase y el bucle de retroalimentación con control estricto de calidad:",
        size=8.5
    )

    # Inserción de Figura 1: Diagrama de Agentes
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(2)
    p_img.paragraph_format.space_after = Pt(2)
    run_img = p_img.add_run()
    run_img.add_picture("figura1_arquitectura_agentes.png", width=Inches(4.9))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(2)
    r_cap = p_cap.add_run("Figura 1: Arquitectura del Sistema Multiagente DAG por Fases con Loops Acotados y Productos Didácticos.")
    r_cap.font.size = Pt(8)
    r_cap.font.italic = True
    r_cap.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 9: FLUJO (1-4), 8. IMPLEMENTACIÓN, 9. EVALUACIÓN Y TABLA 3
    # =========================================================================
    add_h("Flujo de Estados y Componentes del DAG Multiagente", size=10.5, before=0, after=2)
    flujo_p8 = [
        ("1. Entrada del Usuario:", "El docente ingresa el OA, nivel, duración y contexto a través de la interfaz web."),
        ("2. Orquestador LangGraph:", "Inicializa el estado global JSON y transiciona secuencialmente por la Fase 1 (Planificación), Fase 2 (Contenido & Guion) y Fase 3 (Escaleta Audiovisual)."),
        ("3. Agente Revisor (QC):", "Audita la salida consolidada calculando el Score de Coherencia Pedagógica. Si Score < 85%, genera observaciones dirigidas al agente correspondiente; si Score >= 85%, emite el estado APROBADO."),
        ("4. Ensamblador Determinista:", "Recibe la escaleta aprobada y los audios/imágenes, ejecutando MoviePy/FFmpeg en segundo plano para construir el video MP4 final.")
    ]
    for flt, fld in flujo_p8:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.space_before = Pt(0)
        p_f.paragraph_format.space_after = Pt(1.5)
        r_ft = p_f.add_run(f"{flt} ")
        r_ft.font.bold = True
        r_ft.font.size = Pt(8.5)
        r_fd = p_f.add_run(fld)
        r_fd.font.size = Pt(8.5)

    add_h("8. Implementación y producto mínimo viable", size=12, before=2.5, after=1.5)
    add_p("El MVP construido demuestra la viabilidad técnica del pipeline completo:")
    add_p("• Prototipo Web Interactivo: Desarrollado en HTML5, CSS3 con estética Glassmorphism moderna y JavaScript para la interacción con la API y reproductor multimedia.")
    add_p("• Backend FastAPI + LangGraph: Implementado en Python 3.12 con tipado estricto (Pydantic), permitiendo simular y ejecutar las transiciones de estados del DAG con soporte multi-proveedor (Gemini, OpenAI, Quotas).")
    add_p("• Generador de Reportes y Test Suite: Script automatizado en Python (test_multimedia.py) para emitir el informe formal de evaluación pedagógica y validar el renderizado continuo.")
    add_p("• Lanzador de Inicio Rápido: Archivo iniciar_servidor.bat para despliegue automático con un clic en sistemas operativos Windows.")

    add_h("9. Evaluación y resultados", size=12, before=2.5, after=1.5)
    add_p("Se detalla el protocolo de evaluación, las métricas alcanzadas por el Agente Revisor y el impacto en la eficiencia docente.")

    add_h("9.1 Criterios, métricas y protocolo de evaluación", size=10.5, before=2, after=1)

    # Tabla 3: Matriz de 7 Criterios
    t3 = doc.add_table(rows=8, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_data = [
        ("#", "Criterio de Auditoría", "Descripción y Verificación", "Peso"),
        ("1", "Alineación OA vs. Contenido", "Audita que cada sección responda directamente al Objetivo de Aprendizaje.", "20%"),
        ("2", "Exactitud Conceptual y Lenguaje", "Comprueba precisión técnica y adapta vocabulario al nivel configurado.", "15%"),
        ("3", "Coherencia de Escenas", "Verifica secuencia temática fluida sin vacíos didácticos.", "15%"),
        ("4", "Factibilidad Temporal", "Controla que la extensión encaje en el tiempo de clase configurado.", "10%"),
        ("5", "Correspondencia Locución-Imagen-Texto", "Audita sintonía entre lo hablado, proyectado y leído en pantalla.", "15%"),
        ("6", "Densidad por Escena", "Evita sobrecarga cognitiva evaluando cantidad de texto vs. pantalla.", "10%"),
        ("7", "Trazabilidad de Fuentes", "Detecta afirmaciones técnicas que requieren validación de fuentes reales.", "15%")
    ]
    for row_idx, rvals in enumerate(t3_data):
        row = t3.rows[row_idx]
        c1, c2, c3 = row.cells[0], row.cells[1], row.cells[2]
        c1.text, c2.text, c3.text = rvals[0], rvals[1], f"{rvals[2]} ({rvals[3]})"
        c1.width, c2.width, c3.width = Inches(0.35), Inches(2.2), Inches(4.25)
        set_cell_margins(c1, top=30, bottom=30, left=45, right=45)
        set_cell_margins(c2, top=30, bottom=30, left=50, right=50)
        set_cell_margins(c3, top=30, bottom=30, left=50, right=50)
        c1.paragraphs[0].runs[0].font.size = Pt(8)
        c2.paragraphs[0].runs[0].font.size = Pt(8)
        c3.paragraphs[0].runs[0].font.size = Pt(8)
        if row_idx == 0:
            for c in (c1, c2, c3):
                set_cell_background(c, "003366")
                c.paragraphs[0].runs[0].font.bold = True
                c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        else:
            if row_idx % 2 == 1:
                set_cell_background(c1, "F8FAFC")
                set_cell_background(c2, "F8FAFC")
                set_cell_background(c3, "F8FAFC")
            c2.paragraphs[0].runs[0].font.bold = True

    add_p("El protocolo de evaluación combina la verificación automatizada del Agente Revisor con pruebas funcionales de renderizado multimedia. A continuación se presenta la Tabla 5 con los indicadores de desempeño:", size=8.5)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 9: 9.2 RESULTADOS, 9.3 IMPACTO, 10. DISCUSIÓN Y 11. CONCLUSIONES
    # =========================================================================
    add_h("9.2 Resultados técnicos", size=10.5, before=0, after=1.5)
    add_p(
        "En los ensayos de evaluación automatizada realizados en E2, el Agente Revisor obtuvo un Score Global de Coherencia "
        "Pedagógica del 90.4%, superando ampliamente el umbral de aprobación del 85%:\n"
        "• Alineación OA vs. Contenido: 95/100.\n"
        "• Exactitud Conceptual y Lenguaje: 92/100.\n"
        "• Coherencia de Escenas y Cobertura: 88/100.\n"
        "• Factibilidad Temporal: 90/100.\n"
        "• Correspondencia Locución - Imagen - Texto: 90/100 (resuelto el desacople enciclopédico previo).\n"
        "• Densidad de Información por Escena: 85/100.\n"
        "• Trazabilidad y Fuentes: 90/100."
    )

    add_h("9.3 Valor, impacto y limitaciones", size=10.5, before=2, after=1.5)
    add_p("El impacto principal radica en la drástica reducción del tiempo necesario para crear una clase multimedia alineada curricularmente (de 6 horas de trabajo manual a 45 segundos de procesamiento automatizado). Entre las limitaciones se reconoce la dependencia de cuotas de las API de los LLMs y el tiempo de renderizado de video en hardware estándar.")

    # Tabla 4: Indicadores y Métricas
    t4 = doc.add_table(rows=4, cols=4)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_data = [
        ("Indicador", "Método de medición", "Resultado", "Interpretación"),
        ("Score Global QC", "Matriz de 7 criterios pedagógicos y comunicacionales", "90.4% / 100%", "Excelente alineación didáctica (Umbral >= 85%)"),
        ("Tiempo Generación", "Medición de latencia desde prompt inicial hasta render MP4", "< 1 minuto (26-45s)", "Reducción del 98% respecto a creación manual (6 hrs)"),
        ("Sincronía Locución-Texto", "Auditoría visual/auditiva escena por escena", "1.0 (Sin desfase)", "Cero desfases entre locución hablada, subtítulos e imágenes")
    ]
    for row_idx, rvals in enumerate(t4_data):
        row = t4.rows[row_idx]
        for col_idx, text in enumerate(rvals):
            cell = row.cells[col_idx]
            cell.text = text
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            if row_idx == 0:
                set_cell_background(cell, "003366")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if row_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")

    add_h("10. Discusión", size=12, before=2.5, after=1.5)
    add_p(
        "Los resultados demuestran la superioridad del enfoque DAG frente a las llamadas monolíticas tradicionales. "
        "La incorporación de loops acotados de 4 pasos evita que el sistema incurra en alucinaciones o desalineación didáctica, "
        "mientras que el control estricto de máximo 2 iteraciones previene los bucles infinitos característicos de agentes conversacionales sin estado. "
        "El desacople del motor de video mediante MoviePy garantiza que no existan errores de código al generar el archivo final MP4.\n"
        "Asimismo, se analizó el fenómeno de 'Concept Bleeding' o 'Attribute Binding Failure' característico de modelos de difusión abiertos "
        "(como generar un niño con orejas de perro al pedir 'niño con su mascota al lado'). Se demostró que la arquitectura multiagente "
        "desacoplada aísla la generación pedagógica del motor de renderizado, permitiendo mitigar el error mediante prompts negativos o conectar "
        "motores comerciales como DALL-E 3 sin alterar el diseño del sistema."
    )

    add_h("11. Conclusiones y trabajo futuro", size=12, before=2.5, after=1.5)
    add_p("El proyecto ha demostrado con éxito que la orquestación multiagente mediante grafos acíclicos dirigidos (DAG) resuelve efectivamente el problema de desalineación pedagógica de la IA en la creación de recursos didácticos. Se cumplieron los objetivos de acotar el MVP a clases multimedia breves, diseñar la matriz de 7 criterios para el Agente Revisor e integrar la orquestación con LangGraph y MoviePy.")
    add_p("Trabajo Futuro:")
    add_p("1. Integrar motores de clonación de voz sintética de alta fidelidad (ElevenLabs / Edge-TTS neural en español).")
    add_p("2. Expandir los exportadores para soportar paquetes SCORM e integraciones nativas con Canvas y Moodle.")
    add_p("3. Incorporar modelos de IA especializados por disciplina (Ciencias, Humanidades, Matemáticas).")
    add_p("4. Optimización del motor de difusión para eliminar artefactos visuales (Attribute Binding Failure / Concept Bleeding) en las ilustraciones generadas por IA (Hito 10 / E3).")

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 11: REFERENCIAS, ANEXOS A Y B (TABLA 5)
    # ==========================================================================

    add_h("Referencias", size=12, before=0, after=1.5)
    refs_text = [
        "[1] J. Biggs y C. Tang, Teaching for quality learning at university, 4th ed. Berkshire, UK: McGraw-Hill Education, 2011.",
        "[2] R. E. Mayer, The Cambridge handbook of multimedia learning, 2nd ed. Cambridge, UK: Cambridge University Press, 2014.",
        "[3] J. Sweller, «Cognitive load theory», Psychology of Learning and Motivation, vol. 55, pp. 37-76, 2011.",
        "[4] Q. Wu et al., «AutoGen: Enabling next-gen LLM applications via multi-agent conversation», arXiv preprint arXiv:2308.08155, 2023.",
        "[5] LangChain, «LangGraph: Building Language Agents as Graphs», Documentación Oficial, 2024.",
        "[6] Ministerio de Educación de Chile (MINEDUC), «Bases Curriculares de la Educación Básica y Media», Santiago de Chile, 2020."
    ]
    for rf in refs_text:
        p_rf = doc.add_paragraph(rf)
        p_rf.paragraph_format.space_before = Pt(0)
        p_rf.paragraph_format.space_after = Pt(1.5)
        p_rf.runs[0].font.size = Pt(8)

    add_h("Anexos", size=12, before=3, after=1.5)
    add_p("A continuación se adjuntan los anexos obligatorios del informe de titulación.")

    add_h("Anexo A. Declaración de uso de inteligencia artificial", size=10.5, before=2, after=1)
    add_p(
        "En el desarrollo de este trabajo se utilizó asistencia de Inteligencia Artificial Generativa (LLMs) con fines de refactorización "
        "de código, estructuración de esquemas JSON para LangGraph y edición estilística de documentación técnica. Todas las arquitecturas "
        "de software, decisiones de diseño pedagógico, matrices de auditoría y códigos fuente fueron revisados, validados y auditados críticamente "
        "por el equipo de estudiantes responsables, asumiendo la autoría y responsabilidad total sobre el contenido presentado."
    )

    add_h("Anexo B. Contribución individual", size=10.5, before=2, after=1)
    add_p("A continuación se presenta la Tabla 6 completada con el desglose de responsabilidades y evidencias del equipo de trabajo:")

    # Tabla 5: Contribución Individual
    t5 = doc.add_table(rows=4, cols=3)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_data = [
        ("Integrante", "Responsabilidades / contribuciones", "Evidencias"),
        ("Rodrigo Venegas", "Líder de Arquitectura DAG, configuración de LangGraph, integración multi-proveedor (Gemini/OpenAI/Quotas), motor FastAPI y test_multimedia.py.", "Repositorio GitHub / Commits Backend y Pipeline DAG"),
        ("Pablo Loncon", "Diseño de Prompts por Fase, desarrollo del Agente Revisor QC (7 criterios), adaptación a niveles MINEDUC y prototipo frontend Glassmorphism.", "Repositorio GitHub / Schemas Pydantic y UI Prototype"),
        ("Francisco Espinoza", "Integración del ensamblador determinista de video (MoviePy), síntesis de voz neural en español (Edge-TTS), conector AI Horde y sincronización de subtítulos.", "Repositorio GitHub / Media Engine y Videos MP4")
    ]
    for row_idx, (c1, c2, c3) in enumerate(t5_data):
        row = t5.rows[row_idx]
        for col_idx, text in enumerate((c1, c2, c3)):
            cell = row.cells[col_idx]
            cell.text = text
            cell.width = Inches(1.8) if col_idx == 0 else (Inches(2.7) if col_idx == 1 else Inches(2.2))
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            if row_idx == 0:
                set_cell_background(cell, "003366")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if row_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                if col_idx == 0:
                    cell.paragraphs[0].runs[0].font.bold = True

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 12: ANEXO C (TABLA 6: EVIDENCIAS COMPLEMENTARIAS) Y FIRMAS
    # =========================================================================
    add_h("Anexo C. Evidencias complementarias de E3", size=11, before=0, after=1.5)
    add_p("A continuación se presenta la Tabla 7 completada con el registro de enlaces y ubicación de los entregables del proyecto:")

    t6 = doc.add_table(rows=6, cols=3)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    t6_data = [
        ("Producto", "Enlace o ubicación", "Descripción / estado"),
        ("MVP / Evidencia Técnica", "https://github.com/RGVenegas/Seminario-de-Lic", "Prototipo funcional web + Backend LangGraph + MoviePy + Edge-TTS."),
        ("Póster del Proyecto", "contexto/Presentacion_E1_CINF200.html", "Resumen visual de arquitectura DAG y matriz de 7 criterios."),
        ("Presentación Final", "contexto/Presentacion_E1_CINF200.html", "Diapositivas de defensa de diseño e innovación técnica."),
        ("Portafolio del Curso", "https://github.com/RGVenegas/Seminario-de-Lic", "Repositorio público con código, commits, tests y documentación."),
        ("Defensa Individual", "Registro Académico CINF200", "Defensa oral de arquitectura y contribución por estudiante.")
    ]
    for row_idx, (c1, c2, c3) in enumerate(t6_data):
        row = t6.rows[row_idx]
        for col_idx, text in enumerate((c1, c2, c3)):
            cell = row.cells[col_idx]
            cell.text = text
            cell.width = Inches(1.9) if col_idx == 0 else (Inches(2.6) if col_idx == 1 else Inches(2.3))
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            if row_idx == 0:
                set_cell_background(cell, "003366")
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if row_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                if col_idx == 0:
                    cell.paragraphs[0].runs[0].font.bold = True

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(36)
    p_sig.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sig = p_sig.add_run(
        "_____________________________________________\n"
        "Equipo de Proyecto: Rodrigo Venegas · Pablo Loncon · Francisco Espinoza\n"
        "Ingeniería Civil Informática · Universidad Andrés Bello (Sede Viña del mar)\n"
        "Semestre 2026-2 · Entrega 2 (E2)"
    )
    r_sig.font.size = Pt(8.5)
    r_sig.font.italic = True
    r_sig.font.color.rgb = RGBColor(100, 116, 139)

    out_docx = os.path.abspath("INFORME_E2_CINF200.docx")
    out_pdf = os.path.abspath("INFORME_E2_CINF200.pdf")

    print(f"Guardando {out_docx}...")
    doc.save(out_docx)
    print("Exportando a PDF con Word COM...")
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        wb = word.Documents.Open(out_docx)
        wb.SaveAs(out_pdf, FileFormat=17)
        wb.Close()
        word.Quit()
        print(f"PDF generado exitosamente: {out_pdf}")
    except Exception as e:
        print(f"Error Word COM: {e}")

    pdf = fitz.open(out_pdf)
    print(f"\n==========================================")
    print(f"TOTAL FINAL DE PÁGINAS DEL PDF: {pdf.page_count}")
    print(f"==========================================")
    for i in range(pdf.page_count):
        pg = pdf.load_page(i)
        txt = pg.get_text().strip().split('\n')[0] if pg.get_text() else ''
        print(f"  Página {i+1}: {txt[:45]}")

if __name__ == "__main__":
    create_e2_document()
