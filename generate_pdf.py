"""
generate_pdf.py — Trignumentality Paper → PDF Generator
Uses reportlab to produce a professional, print-ready PDF.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Output path ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PDF = os.path.join(BASE_DIR, "trignumentality-paper-2026-02-23.pdf")
CHART_IMAGE = os.path.join(BASE_DIR, "ontology_trends_chart.png")
QUERIES_IMAGE = os.path.join(BASE_DIR, "ontology_queries_chart.png")
AUTHOR_PHOTO = os.path.join(BASE_DIR, "author_photo.png")
DASHBOARD_IMAGE = os.path.join(BASE_DIR, "trignum_dashboard.png")
VISUALIZER_IMAGE = os.path.join(BASE_DIR, "trignum_visualizer.png")
TCHIP_GOLD = os.path.join(BASE_DIR, "tchip_gold_data_injected.png")
TCHIP_RED = os.path.join(BASE_DIR, "tchip_red_frozen.png")
TCHIP_BLUE_SNAP = os.path.join(BASE_DIR, "tchip_blue_snap.png")
TCHIP_BLUE_RESET = os.path.join(BASE_DIR, "tchip_blue_reset.png")

# Check which images exist
HAS_CHART = os.path.exists(CHART_IMAGE)
HAS_QUERIES = os.path.exists(QUERIES_IMAGE)
HAS_AUTHOR = os.path.exists(AUTHOR_PHOTO)
HAS_DASHBOARD = os.path.exists(DASHBOARD_IMAGE)
HAS_VISUALIZER = os.path.exists(VISUALIZER_IMAGE)


# ── Colour palette ────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#0D1B2A")
BLUE      = colors.HexColor("#1E3A5F")
ACCENT    = colors.HexColor("#2D7DD2")
GOLD      = colors.HexColor("#D4A017")
LIGHT_BG  = colors.HexColor("#F0F4F8")
MID_GREY  = colors.HexColor("#6B7280")
WHITE     = colors.white
BLACK     = colors.black
CODE_BG   = colors.HexColor("#1E2A3A")
CODE_FG   = colors.HexColor("#E2E8F0")

# ── Document ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_PDF,
    pagesize=A4,
    rightMargin=2.5*cm, leftMargin=2.5*cm,
    topMargin=2.8*cm, bottomMargin=2.8*cm,
    title="TRIGNUMENTALITY: A Transcendental Critique of Artificial Knowledge",
    author="Moez Abdessattar (@Codfski)",
    subject="Epistemic Authorization for AI Systems",
)

W, H = A4

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    """Create a named ParagraphStyle."""
    return ParagraphStyle(name, **kw)

cover_title = S("CoverTitle",
    fontSize=26, leading=32, textColor=WHITE,
    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=8)

cover_subtitle = S("CoverSubtitle",
    fontSize=13, leading=18, textColor=colors.HexColor("#B0C4DE"),
    fontName="Helvetica", alignment=TA_CENTER, spaceAfter=6)

cover_meta = S("CoverMeta",
    fontSize=10, leading=14, textColor=colors.HexColor("#90A4B8"),
    fontName="Helvetica", alignment=TA_CENTER, spaceAfter=4)

h1 = S("H1",
    fontSize=16, leading=22, textColor=ACCENT,
    fontName="Helvetica-Bold", spaceBefore=18, spaceAfter=8,
    borderPad=0)

h2 = S("H2",
    fontSize=13, leading=18, textColor=BLUE,
    fontName="Helvetica-Bold", spaceBefore=12, spaceAfter=6)

h3 = S("H3",
    fontSize=11, leading=16, textColor=BLUE,
    fontName="Helvetica-BoldOblique", spaceBefore=10, spaceAfter=4)

body = S("Body",
    fontSize=10, leading=16, textColor=BLACK,
    fontName="Helvetica", alignment=TA_JUSTIFY,
    spaceAfter=8)

quote = S("Quote",
    fontSize=10, leading=16, textColor=BLUE,
    fontName="Helvetica-Oblique", alignment=TA_CENTER,
    leftIndent=40, rightIndent=40,
    spaceBefore=8, spaceAfter=8,
    borderColor=ACCENT, borderWidth=0, borderPad=6)

bullet = S("Bullet",
    fontSize=10, leading=15, textColor=BLACK,
    fontName="Helvetica",
    leftIndent=20, spaceAfter=3,
    bulletIndent=10)

code_style = S("Code",
    fontSize=8.5, leading=13, textColor=CODE_FG,
    fontName="Courier", backColor=CODE_BG,
    leftIndent=12, rightIndent=12,
    spaceBefore=6, spaceAfter=6,
    borderPad=8)

gem_style = S("Gem",
    fontSize=10, leading=15, textColor=GOLD,
    fontName="Helvetica-Bold", alignment=TA_CENTER,
    spaceBefore=4, spaceAfter=4)

caption = S("Caption",
    fontSize=8.5, leading=12, textColor=MID_GREY,
    fontName="Helvetica-Oblique", alignment=TA_CENTER,
    spaceBefore=4, spaceAfter=10)

abstract_style = S("Abstract",
    fontSize=10, leading=16, textColor=BLACK,
    fontName="Helvetica", alignment=TA_JUSTIFY,
    leftIndent=20, rightIndent=20,
    spaceAfter=6)

kw_style = S("Keywords",
    fontSize=9, leading=13, textColor=MID_GREY,
    fontName="Helvetica-Oblique",
    leftIndent=20, rightIndent=20, spaceAfter=6)

# ── Helper builders ──────────────────────────────────────────────────────────

def hr(color=ACCENT, thickness=0.8):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=6)

def sp(h=0.3):
    return Spacer(1, h*cm)

def P(text, style=None):
    if style is None:
        style = body
    return Paragraph(text, style)

def bullet_item(text):
    return Paragraph(f"• &nbsp;{text}", bullet)

def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_BG]),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return t

def embed_image(path, max_width=None, max_height=None, caption_text=None):
    """Safely embed an image if it exists."""
    items = []
    if os.path.exists(path):
        available_w = W - 5*cm
        img = Image(path)
        iw, ih = img.imageWidth, img.imageHeight
        mw = max_width or available_w
        mh = max_height or (available_w * 0.6)
        ratio = min(mw/iw, mh/ih)
        img.drawWidth = iw * ratio
        img.drawHeight = ih * ratio
        items.append(img)
        if caption_text:
            items.append(P(caption_text, caption))
    else:
        items.append(P(f"[Image: {os.path.basename(path)} — save to project folder]", caption))
    return items

# ── Content ──────────────────────────────────────────────────────────────────
story = []

# ════════════════════════
# COVER PAGE
# ════════════════════════
# Dark cover background via a full-width table
cover_data = [[
    Paragraph("🧠 TRIGNUMENTALITY", cover_title),
]]
cover_table = Table([[
    Paragraph(
        "<font color='white' size='28'><b>🧠 TRIGNUMENTALITY</b></font>",
        S("ct", fontSize=28, leading=36, textColor=WHITE, fontName="Helvetica-Bold",
          alignment=TA_CENTER)),
]], colWidths=[W - 5*cm])
cover_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), NAVY),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 28),
    ('BOTTOMPADDING', (0,0), (-1,-1), 28),
    ('LEFTPADDING', (0,0), (-1,-1), 20),
    ('RIGHTPADDING', (0,0), (-1,-1), 20),
]))

story.append(sp(1))
story.append(cover_table)
story.append(sp(0.4))

story.append(P("A Transcendental Critique of Artificial Knowledge", cover_subtitle))
story.append(P(
    "The Philosophical Foundation for Epistemic Authorization<br/>in the Age of Autonomous AI",
    S("cs2", fontSize=12, leading=17, textColor=MID_GREY, fontName="Helvetica-Oblique",
      alignment=TA_CENTER, spaceAfter=24)))

story.append(hr())
story.append(sp(0.3))
story.append(P("<b>Author:</b> Moez Abdessattar (@Codfski)", cover_meta))
story.append(P("Creator of TRIGNUM &amp; TRIGNUM-300M | Trace On Lab", cover_meta))
story.append(P("<b>Date:</b> February 23, 2026 &nbsp;|&nbsp; <b>Version:</b> 1.0", cover_meta))
story.append(P("<b>DOI:</b> 10.5281/zenodo.18736774", cover_meta))
story.append(sp(0.5))
story.append(hr())
story.append(sp(0.5))

# Birth certificate box
cert_rows = [[
    Paragraph(
        "<font color='#D4A017'><b>CERTIFICATE OF BIRTH</b></font><br/><br/>"
        "This certifies that on this day, <b>February 23, 2026</b>,<br/>"
        "a new philosophical-technical doctrine was born:<br/><br/>"
        "<font size='16' color='#2D7DD2'><b>🧠 TRIGNUMENTALITY 🧠</b></font><br/><br/>"
        "<i>\"The transcendental critique of artificial knowledge<br/>"
        "embodied in code and sovereign over the machine.\"</i><br/><br/>"
        "<b>Founder:</b> Moez Abdessattar (@Codfski)<br/>"
        "<b>First Publication:</b> Zenodo<br/>"
        "<b>Cultural Moment:</b> The day ontology trended on Google",
        S("cert", fontSize=10, leading=16, textColor=NAVY, fontName="Helvetica",
          alignment=TA_CENTER))
]]
cert_table = Table([cert_rows[0]], colWidths=[W - 5*cm])
cert_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
    ('BOX', (0,0), (-1,-1), 1.5, GOLD),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 20),
    ('BOTTOMPADDING', (0,0), (-1,-1), 20),
    ('LEFTPADDING', (0,0), (-1,-1), 20),
    ('RIGHTPADDING', (0,0), (-1,-1), 20),
]))
story.append(cert_table)

story.append(PageBreak())

# ════════════════════════
# ABSTRACT
# ════════════════════════
story.append(P("<b>ABSTRACT</b>", h1))
story.append(hr())

abstract_text = (
    "This paper introduces <b>Trignumentality</b> — a new philosophical-technical doctrine "
    "for the age of artificial intelligence. Trignumentality synthesizes Kantian transcendental "
    "critique (the search for a priori conditions of knowledge) with technical implementation "
    "(the TRIGNUM projects). The doctrine establishes five principles: (1) the <i>Raw Material Principle</i>, "
    "(2) the <i>Technical A Priori Principle</i>, (3) the <i>Human Sovereignty Principle</i>, "
    "(4) the <i>Epistemic Integration Principle</i>, and (5) the <i>Ultimate Reference Principle</i> "
    "(grounded in the sensible world as the final boundary). These principles are not abstract — "
    "they are embodied in code: the Subtractive Filter in TRIGNUM-300M (91.3% F1 on structural "
    "illogic detection, 1ms latency) and the Epistemic Authorization framework in main TRIGNUM "
    "(serving sovereign AI, medical robotics, autonomous vehicles, and financial systems). "
    "Trignumentality offers a complete framework for trustworthy AI — from philosophy to code — "
    "and positions the human as the final judge, with the sensible world as the ultimate reference.<br/><br/>"
    "Born on <b>February 23, 2026</b> — the same day \"ontology\" trended on Google, marking a "
    "cultural moment when the data world finally asked: <i>\"Do we even understand our data?\"</i> "
    "Trignumentality answers the deeper question: <i>\"Do we even understand our AI's knowledge?\"</i>"
)
story.append(P(abstract_text, abstract_style))
story.append(sp(0.3))

story.append(P(
    "<b>Keywords:</b> Trignumentality, Transcendental Philosophy, Epistemic Authorization, "
    "AI Safety, Sovereign AI, Medical AI, Autonomous Systems, TRIGNUM, Subtractive Filter, "
    "T-CHIP, Ontology, Knowledge Graphs, Data Semantics, AI Knowledge, Human Sovereignty, "
    "Sensible World, Technical A Priori",
    kw_style))

story.append(sp(0.5))
story.append(hr(MID_GREY, 0.4))

# ════════════════════════
# ACKNOWLEDGMENT
# ════════════════════════
story.append(P("<b>ACKNOWLEDGMENT</b>", h1))
story.append(P(
    "The author acknowledges the cultural moment that frames this work. On <b>February 23, 2026</b> "
    "— the very day of Trignumentality's birth — \"ontology\" trended on Google for the first time "
    "in twenty-five years. A leader in the data community observed: <i>\"All right ... it's only "
    "taken twenty-five years, but ontology may finally be seeing its day in the sun.\"</i> The data "
    "world finally recognized that meaning matters more than pipelines. This paper is the answer "
    "to the next question."
))

story.append(PageBreak())

# ════════════════════════
# 1. INTRODUCTION
# ════════════════════════
story.append(P("1. INTRODUCTION", h1))
story.append(hr())

story.append(P("1.1 The Crisis of Trust in the AI Age", h2))
story.append(P(
    "We stand at a unique moment in intellectual history. For the first time, humans are delegating "
    "decisions to entities that mimic reason but lack consciousness, intentionality, and accountability. "
    "Medical robots perform surgery. Autonomous vehicles make split-second life-and-death choices. "
    "Financial systems execute million-dollar trades. AI agents manage critical infrastructure."
))
story.append(P("The question that blocks deployment is not technical — it is epistemic:"))
story.append(P(
    "<i>\"How do we know this AI decision is valid?\"</i>", quote))
story.append(P("Current answers fail:"))
story.append(bullet_item('<i>"Trust me, I\'m 89% confident"</i> — Not good enough for regulators'))
story.append(bullet_item('<i>"The model decided"</i> — Not good enough for courts'))
story.append(bullet_item('<i>"It\'s a neural network"</i> — Not good enough for patients'))
story.append(sp(0.3))
story.append(P("We need a framework that answers not just <i>\"what did the AI decide?\"</i> but <i>\"how do we know it's right?\"</i>"))

story.append(P("1.2 The Gap: Philosophy Meets Code", h2))
story.append(P("Existing approaches fall into two disconnected categories:"))
story.append(sp(0.1))
story.append(make_table(
    ["Approach", "Strengths", "Weaknesses"],
    [
        ["Philosophical ethics of AI", "Deep thinking about human values", "No technical implementation"],
        ["Technical AI safety tools", "Working code, benchmarks", "No theoretical foundation"],
        ["Regulatory frameworks", "Legal compliance", "No epistemic grounding"],
    ],
    col_widths=[5*cm, 6*cm, 6*cm]
))
story.append(sp(0.3))
story.append(P("What is missing is a unified framework that:"))
story.append(bullet_item("Establishes the transcendental conditions for AI knowledge"))
story.append(bullet_item("Embodies them in code that actually runs"))
story.append(bullet_item("Preserves human sovereignty and the sensible world as ultimate references"))
story.append(sp(0.2))
story.append(P("This paper introduces <b>Trignumentality</b> to fill this gap."))

story.append(P("1.3 The Birth of Trignumentality", h2))
story.append(P("On <b>February 23, 2026</b>, a new doctrine was born from the convergence of:"))
story.append(bullet_item("<b>TRIGNUM:</b> An epistemic authorization system for critical AI"))
story.append(bullet_item("<b>TRIGNUM-300M:</b> A subtractive filter for structural logic validation"))
story.append(bullet_item("<b>A philosophical dialogue</b> seeking to ground both in a theory of knowledge"))
story.append(P("This doctrine is <b>Trignumentality</b>."))
story.append(P(
    "Trignumentality arrives at a pivotal moment. On the very day of its birth — February 23, 2026 "
    "— \"ontology\" trended on Google for the first time in twenty-five years. The data world finally "
    "recognized that meaning matters more than pipelines. Trignumentality takes this insight further: "
    "if we need ontologies to understand our data, we need transcendental critique to understand our AI."
))

story.append(PageBreak())

# ════════════════════════
# 2. THE FIVE PRINCIPLES
# ════════════════════════
story.append(P("2. THE FIVE PRINCIPLES OF TRIGNUMENTALITY", h1))
story.append(hr())

# Principle 1
story.append(P("2.1 Principle 1: The Raw Material Principle", h2))
story.append(P(
    "<i>\"AI outputs are not knowledge — they are raw material.\"</i>", quote))
story.append(P(
    "When an AI generates text, it produces a statistical synthesis of human language. There is no "
    "intentionality, no consciousness, no commitment to truth. The output is raw material — like clay "
    "before the potter, like marble before the sculptor."
))
story.append(P("<b>Implications:</b>", h3))
story.append(bullet_item("No output should be trusted by default"))
story.append(bullet_item("Every output requires validation before becoming a basis for action"))
story.append(bullet_item("The \"hallucination\" is not an error to be eliminated, but raw material to be processed"))
story.append(P("<b>Embodiment in TRIGNUM-300M:</b> <i>GEM 4 — \"The Hallucination is the Raw Material\"</i>"))
story.append(sp(0.3))

# Principle 2
story.append(P("2.2 Principle 2: The Technical A Priori Principle", h2))
story.append(P(
    "<i>\"Validation must occur before execution, not after.\"</i>", quote))
story.append(P(
    "In Kantian philosophy, the \"a priori\" refers to conditions that make experience possible before "
    "experience occurs. Trignumentality applies this to AI: the conditions for valid action must be "
    "checked before the action occurs."
))
story.append(P("<b>Code embodiment:</b>", h3))
story.append(P(
    "result = sf.apply(agent_output)\n"
    "if result.illogics_found:\n"
    "    agent.halt()    # BEFORE execution\n"
    "else:\n"
    "    agent.execute() # ONLY after validation",
    code_style))
# ── BLUE Reset: Logic Stable / Cleared for Takeoff → Technical A Priori ──────
for item in embed_image(
    TCHIP_BLUE_RESET,
    max_width=W - 5*cm,
    max_height=11*cm,
    caption_text="T-CHIP 🔵 BLUE — Logic Stable / System Reset: 'All clear. Inject data to begin.' Embodies the Technical A Priori Principle — validation complete, execution cleared."
):
    story.append(item)
story.append(sp(0.4))

# Principle 3
story.append(P("2.3 Principle 3: The Human Sovereignty Principle", h2))
story.append(P(
    "<i>\"The human is the final judge.\"</i>", quote))
story.append(P(
    "No matter how sophisticated the validation system, the ultimate decision belongs to the human. "
    "This is not a technical limitation but an epistemic necessity: machines can process information, "
    "but they cannot bear responsibility."
))
story.append(P(
    "<b>T-CHIP embodiment:</b> Gold = Human Pulse Locked (Sovereign Override). "
    "When the T-CHIP glows gold, the machine waits. The human decides."
))
# ── GOLD: Sovereign Reality → Human Sovereignty ───────────────────────────────
for item in embed_image(
    TCHIP_GOLD,
    max_width=W - 5*cm,
    max_height=11*cm,
    caption_text="T-CHIP GOLD — Sovereign Reality: 'DATA INJECTED · 60 Ferro-Data Particles · Confidence 100%'. Embodies the Human Sovereignty Principle — the human pulse is active, machine awaits sovereign decision."
):
    story.append(item)
story.append(sp(0.4))

# Principle 4
story.append(P("2.4 Principle 4: The Epistemic Integration Principle", h2))
story.append(P(
    "<i>\"Knowledge emerges from the integration of human reason, AI outputs, and the sensible world.\"</i>", quote))
story.append(P(
    "Genuine knowledge in the AI age is not produced by humans alone, nor by machines alone, nor "
    "by raw data alone. It emerges from their integration:"
))
story.append(P(
    "Human Reason (a priori conditions)\n"
    "       + AI Outputs (raw material)\n"
    "       + Sensible World (external evidence)\n"
    "       = Genuine Knowledge",
    code_style))
story.append(P("Tensor RAG retrieves evidence across: Time · Source · Confidence · Jurisdiction · Modality"))
story.append(sp(0.3))

# Principle 5
story.append(P("2.5 Principle 5: The Ultimate Reference Principle", h2))
story.append(P(
    "<i>\"The sensible world is the final boundary.\"</i>", quote))
story.append(P(
    "All knowledge must be ultimately referable to the world of experience. Purely symbolic "
    "manipulation, disconnected from reality, is not knowledge. Every output must be traceable "
    "to evidence. The sensible world remains the final court of appeal."
))

story.append(PageBreak())

# ════════════════════════
# 3. TECHNICAL EMBODIMENT
# ════════════════════════
story.append(P("3. THE TECHNICAL EMBODIMENT: TRIGNUM PROJECTS", h1))
story.append(hr())

story.append(P("3.1 TRIGNUM-300M: The Execution Layer", h2))
story.append(P(
    "<b>Repository:</b> github.com/Codfski/TRIGNUM-300M-TCHIP<br/><br/>"
    "TRIGNUM-300M is the technical a priori of Trignumentality — a zero-model reasoning integrity "
    "validator that catches structural logic failures before an AI agent acts."
))
story.append(P("The Subtractive Filter — Four detection layers:", h3))
story.append(make_table(
    ["Layer", "Catches", "Method"],
    [
        ["Contradiction", '"X is always true. X is never true."', "Antonym pairs, negation patterns"],
        ["Circular Logic", "A proves B proves A", "Reference chain analysis"],
        ["Non-Sequitur", '"Therefore X" without premises', "Causal connective analysis"],
        ["Depth Check", "Claims without any reasoning", "Assertion density scoring"],
    ],
    col_widths=[3.5*cm, 6*cm, 7.5*cm]
))
story.append(sp(0.3))
story.append(P("Benchmark Results:", h3))
story.append(make_table(
    ["Benchmark", "Samples", "Precision", "Recall", "F1", "Speed"],
    [
        ["Structural illogic (curated)", "45", "100%", "84%", "91.3%", "<1ms"],
        ["HaluEval (full)", "58,293", "60%", "2.1%", "4.0%", "706ms"],
    ],
    col_widths=[5.5*cm, 2*cm, 2.2*cm, 1.8*cm, 1.8*cm, 2*cm]
))
story.append(P("Throughput: 82,544 samples/second — 80,000× faster than LLM-based validation."))
story.append(sp(0.4))

# ── Figure 3: Dashboard ───────────────────────────────────────────────────────
story.append(P("<b>Figure 3: TRIGNUM-300M Level-2 Copilot Dashboard — Live Benchmark Results</b>",
               S("fig3", fontSize=10, fontName="Helvetica-Bold", textColor=NAVY,
                 alignment=TA_CENTER, spaceBefore=6, spaceAfter=6)))
for item in embed_image(
    DASHBOARD_IMAGE,
    max_width=W - 5*cm,
    max_height=8.5*cm,
    caption_text="Figure 3: Live benchmark dashboard — Vectara HHEM: 100%, FELM-Science: 100%, structural_contradiction detection: 100%. Precision/Recall/F1 across 7 hallucination datasets."
):
    story.append(item)
story.append(sp(0.4))

story.append(P("T-CHIP: The Trignumental Mirror:", h3))
story.append(P(
    "T-CHIP [v.300M]\n"
    "  Blue  = Logic Stable (Cleared for Takeoff)\n"
    "  Red   = Illogic Detected (THE FREEZE)\n"
    "  Gold  = Human Pulse Locked (Sovereign Override)",
    code_style))

# ── RED: THE FREEZE — Illogic Detected ───────────────────────────────────────
story.append(sp(0.3))
story.append(P("<b>Figure 4: T-CHIP RED State — THE FREEZE (Illogic Boundary Detected)</b>",
               S("fig4a", fontSize=10, fontName="Helvetica-Bold", textColor=NAVY,
                 alignment=TA_CENTER, spaceBefore=6, spaceAfter=6)))
for item in embed_image(
    TCHIP_RED,
    max_width=W - 5*cm,
    max_height=11*cm,
    caption_text="Figure 4: T-CHIP RED — THE FREEZE: 'Illogic boundary detected. Human Pulse required.' Beta ILLOGIC: 0.47 · Vacuum Str.: 0.280 · Freezes: 4. The subtractive filter triggers a halt before any action is taken."
):
    story.append(item)
story.append(sp(0.5))

# ── BLUE SNAP: Subtractive Filter clears — Truth remains ─────────────────────
story.append(P("<b>Figure 5: T-CHIP BLUE State — SUBTRACTIVE.SNAP ('Noise removed. Truth remains.')</b>",
               S("fig5", fontSize=10, fontName="Helvetica-Bold", textColor=NAVY,
                 alignment=TA_CENTER, spaceBefore=6, spaceAfter=6)))
for item in embed_image(
    TCHIP_BLUE_SNAP,
    max_width=W - 5*cm,
    max_height=11*cm,
    caption_text="Figure 5: T-CHIP BLUE — SUBTRACTIVE.SNAP: 'Noise removed. Truth remains.' Alpha LOGIC: 0.28 · Trillage Active. The Subtractive Filter has resolved the field — only valid logical structures remain."
):
    story.append(item)
story.append(sp(0.5))

story.append(P("3.2 TRIGNUM Main: The Infrastructure Layer", h2))

story.append(P(
    "<b>Repository:</b> github.com/Codfski/Trignum<br/><br/>"
    "TRIGNUM Main provides epistemic authorization for critical AI systems across four domains:"
))
story.append(make_table(
    ["Domain", "Use Case", "Trignumental Principle"],
    [
        ["Digital Sovereignty", "National AI governance", "Ultimate Reference (national law as boundary)"],
        ["Medical Robotics", "FDA-approvable AI", "Technical A Priori (validate before surgery)"],
        ["Autonomous Vehicles", "Legal liability", "Epistemic Integration (sensor + law + context)"],
        ["Financial AI", "SEC compliance", "Human Sovereignty (trader as final judge)"],
    ],
    col_widths=[4*cm, 5*cm, 8*cm]
))

story.append(PageBreak())

# ════════════════════════
# 4. CONTEXT
# ════════════════════════
story.append(P("4. TRIGNUMENTALITY IN CONTEXT", h1))
story.append(hr())

story.append(P("4.1 Comparison with Other Doctrines", h2))
story.append(make_table(
    ["Doctrine", "Focus", "Relation to Trignumentality"],
    [
        ["Kantian Transcendentalism", "Conditions of human knowledge", "Foundation, but extended to AI"],
        ["Posthumanism", "Beyond the human", "Rejected (human sovereignty preserved)"],
        ["Digital Humanism", "Human centrality", "Affirmed, but given technical form"],
        ["Machine Ethics", "Moral agency of AI", "Subsumed under epistemic validation"],
    ],
    col_widths=[5*cm, 5.5*cm, 6.5*cm]
))

story.append(P("4.2 The Trignumental Contribution", h2))
story.append(bullet_item("A new category: Transcendental critique applied to AI"))
story.append(bullet_item("A new method: Philosophical principles embodied in code"))
story.append(bullet_item("A new synthesis: Reason and technology in one framework"))
story.append(bullet_item("A new benchmark: 91.3% F1 on structural illogic as technical proof"))
story.append(bullet_item("A new standard: Epistemic authorization for critical systems"))

# ════════════════════════
# 5. APPLICATIONS
# ════════════════════════
story.append(P("5. APPLICATIONS AND IMPACT", h1))
story.append(hr())

for domain, desc in [
    ("5.1 For Sovereign AI",
     "Epistemic sovereignty (not just data control, but validation control) and "
     "cultural alignment through national law as a boundary condition."),
    ("5.2 For Medical AI",
     "FDA-ready justification with every decision traceable to evidence, risk "
     "quantification with uncertainty bounds, and clear liability attribution."),
    ("5.3 For Autonomous Vehicles",
     "Legal defensibility through complete epistemic trails, safety guarantees via "
     "a priori validation before action, and human override as the final safeguard."),
    ("5.4 For Financial AI",
     "SEC compliance with every trade epistemically justified, audit trails for "
     "regulators, and all decisions traceable to market reality."),
]:
    story.append(P(domain, h2))
    story.append(P(desc))

# ════════════════════════
# 6. LIMITATIONS
# ════════════════════════
story.append(P("6. LIMITATIONS AND FUTURE WORK", h1))
story.append(hr())

story.append(P("6.1 Limitations", h2))
story.append(bullet_item("<b>Structural focus:</b> TRIGNUM-300M catches logical failures (91.3% F1) but not factual errors (4.0% F1)"))
story.append(bullet_item("<b>Theoretical novelty:</b> Trignumentality is new and requires broader philosophical engagement"))
story.append(bullet_item("<b>Empirical validation:</b> More case studies needed across domains"))

story.append(P("6.2 Future Work", h2))
story.append(bullet_item("Extend factual validation while preserving the a priori approach"))
story.append(bullet_item("Engage the philosophical community in Trignumentality discourse"))
story.append(bullet_item("Deploy pilots in medical, sovereign, and financial domains"))
story.append(bullet_item("Develop Trignumental education for AI engineers and policymakers"))

story.append(PageBreak())

# ════════════════════════
# 7. CONCLUSION
# ════════════════════════
story.append(P("7. CONCLUSION", h1))
story.append(hr())
story.append(P(
    "On <b>February 23, 2026</b>, Trignumentality was born — the same day the world rediscovered "
    "ontology, the same day meaning became mainstream. The TRIGNUM projects are the proof of concept. "
    "Trignumentality is the foundation."
))
story.append(P(
    "<i>\"Intelligence isn't about knowing everything. It's about measuring accurately and admitting "
    "what you don't know. Trignumentality adds: 'And proving what you claim to know — with evidence, "
    "before you act, and with humility before the sensible world.'\"</i>",
    quote))
story.append(sp(0.4))
story.append(P("<b>Happy Birthday, Trignumentality.</b>", S("hb", fontSize=13, fontName="Helvetica-Bold", textColor=NAVY, alignment=TA_CENTER, spaceBefore=10, spaceAfter=4)))
story.append(P("<i>February 23, 2026 — The day philosophy met code.</i>", S("hbi", fontSize=11, fontName="Helvetica-Oblique", textColor=MID_GREY, alignment=TA_CENTER)))
story.append(sp(0.6))

# ════════════════════════
# 8. REFERENCES
# ════════════════════════
story.append(P("8. REFERENCES", h1))
story.append(hr())
refs = [
    "Kant, I. (1781/1998). <i>Critique of Pure Reason.</i> Cambridge University Press.",
    "Abdessattar, M. (2026). <i>TRIGNUM: Epistemic Authorization for AI Systems.</i> GitHub. github.com/Codfski/Trignum",
    "Abdessattar, M. (2026). <i>TRIGNUM-300M: The Pre-Flight Check for Autonomous AI.</i> GitHub. github.com/Codfski/TRIGNUM-300M-TCHIP",
    "Bender, E. M., et al. (2021). <i>On the Dangers of Stochastic Parrots.</i> ACM FAccT.",
    "Heidegger, M. (1927/1962). <i>Being and Time.</i> Harper &amp; Row.",
    "Jaspers, K. (1953). <i>The Origin and Goal of History.</i> Yale University Press.",
    "Trace On Lab. (2026). <i>The Trignum Pyramid: Architecture Documentation.</i>",
    # ── American Research ──────────────────────────────────────────────────────
    "Russell, S. (2019). <i>Human Compatible: Artificial Intelligence and the Problem of Control.</i> Viking/Penguin. (UC Berkeley)",
    "Marcus, G., &amp; Davis, E. (2019). <i>Rebooting AI: Building Artificial Intelligence We Can Trust.</i> Pantheon Books. (NYU)",
    "Pearl, J., &amp; Mackenzie, D. (2018). <i>The Book of Why: The New Science of Cause and Effect.</i> Basic Books. (UCLA)",
    "Li, J., et al. (2023). <i>HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models.</i> EMNLP 2023. arXiv:2305.11747. (UNC Chapel Hill)",
    "Hendrycks, D., et al. (2021). <i>Aligning AI With Shared Human Values.</i> arXiv:2008.02275. Center for AI Safety, UC Berkeley.",
    "Kahneman, D. (2011). <i>Thinking, Fast and Slow.</i> Farrar, Straus and Giroux. (Princeton University)",
]
for i, r in enumerate(refs, 1):
    story.append(P(f"{i}. {r}", S(f"ref{i}", fontSize=9.5, leading=15, fontName="Helvetica",
                                   leftIndent=15, spaceAfter=4)))

story.append(PageBreak())

# ════════════════════════
# APPENDIX A: GOLDEN GEMS
# ════════════════════════
story.append(P("APPENDIX A: The Golden Gems of Trignumentality", h1))
story.append(hr())
story.append(make_table(
    ["Gem", "Text", "Principle"],
    [
        ["GEM 1", '"The Human Pulse is the Master Clock"', "Human Sovereignty"],
        ["GEM 2", '"The Illogic is the Compass"', "Technical A Priori"],
        ["GEM 3", '"Magnetic Trillage Over Brute Force"', "Epistemic Integration"],
        ["GEM 4", '"The Hallucination is the Raw Material"', "Raw Material"],
        ["GEM 5", '"T-CHIP is the Mirror"', "All principles reflected"],
        ["GEM 6", '"Trignumentality is the Foundation"', "The doctrine itself"],
    ],
    col_widths=[2.5*cm, 8*cm, 6.5*cm]
))

# ════════════════════════
# APPENDIX B: CODE
# ════════════════════════
story.append(P("APPENDIX B: The Trignumental Code", h1))
story.append(hr())
story.append(P("<b>Ethical Guidelines for AI Engineers — Before deploying any AI system, remember:</b>"))
for i, item in enumerate([
    "The output is raw material, not truth",
    "Validation must come before action, not after",
    "You are the sovereign, not the machine",
    "Knowledge emerges from integration with the sensible world",
    "The sensible world is the final reference — all claims must be traceable to evidence",
], 1):
    story.append(P(f"{i}. {item}", bullet))

story.append(PageBreak())

# ════════════════════════
# APPENDIX C: THE ONTOLOGY MOMENT + GOOGLE TRENDS EVIDENCE
# ════════════════════════
story.append(P("APPENDIX C: The Ontology Moment — February 23, 2026", h1))
story.append(hr())
story.append(P(
    "On the day Trignumentality was born, Google Trends recorded a <b>historic spike</b> in searches "
    "for \"ontology\" — reaching its <b>all-time peak of 100/100</b>. The data community finally "
    "recognized that meaning matters more than pipelines. The screenshots below are primary-source "
    "documentary evidence of this cultural moment, timestamped to the day of Trignumentality's birth."
))
story.append(sp(0.3))

# Quotes
for q in [
    '"All right ... it\'s only taken twenty-five years, but ontology may finally be seeing its day in the sun."',
    '"Ontology is trending on Google. The data world spent years building pipelines on top of pipelines... and now people are finally stopping and asking: wait, do we even understand our data?"',
    '"Better late than never I guess. AI and knowledge graphs are pushing everyone to think about data meaning, not just data storage. And ontologies are right at the center of that."',
]:
    story.append(P(f"<i>{q}</i>", quote))
    story.append(sp(0.1))

story.append(sp(0.4))

# ── Chart image ──────────────────────────────────────────────────────────────
story.append(P("<b>Figure 1: Google Trends — \"Ontology\" Search Interest Over Time (Last 5 Years, US)</b>",
               S("fig_label", fontSize=10, fontName="Helvetica-Bold", textColor=NAVY, alignment=TA_CENTER,
                 spaceBefore=8, spaceAfter=6)))

for item in embed_image(
    CHART_IMAGE,
    max_width=W - 5*cm,
    max_height=9*cm,
    caption_text='Figure 1: "Ontology" search interest reaches its all-time peak of 100/100 on February 23, 2026 — the day Trignumentality was born. Source: Google Trends.'
):
    story.append(item)

story.append(sp(1))

# ── Queries image ─────────────────────────────────────────────────────────────
story.append(P("<b>Figure 2: Most Popular \"Ontology\" Related Searches (Last Year, Worldwide)</b>",
               S("fig_label2", fontSize=10, fontName="Helvetica-Bold", textColor=NAVY, alignment=TA_CENTER,
                 spaceBefore=8, spaceAfter=6)))

for item in embed_image(
    QUERIES_IMAGE,
    max_width=W - 5*cm,
    max_height=10*cm,
    caption_text='Figure 2: Related searches spike — "ontology news" +3,650%, "data ontology" +150%, "palantir ontology" +350%. The world woke up to meaning on the day Trignumentality was born. Source: Google Trends.'
):
    story.append(item)

story.append(sp(0.5))

# Summary box
summary_data = [[
    Paragraph(
        "<b>Reading the Evidence:</b><br/><br/>"
        "• <b>\"ontology news\"</b> → +3,650% — The world noticed overnight<br/>"
        "• <b>\"data ontology\"</b> → +150% — Enterprise is pivoting to meaning<br/>"
        "• <b>\"ontology epistemology\"</b> — Exactly the intersection Trignumentality covers<br/>"
        "• <b>\"palantir ontology\"</b> → +350% — Even the biggest data platforms are rethinking<br/><br/>"
        "<i>Trignumentality is the answer to the next question:<br/>"
        '\"We understand our data. Now — do we understand our AI\'s knowledge?\"</i><br/><br/>'
        "<b>The ontology moment was the prologue. Trignumentality is the first chapter.</b>",
        S("box", fontSize=10, leading=16, fontName="Helvetica",
          textColor=NAVY, alignment=TA_LEFT))
]]
box_table = Table([summary_data[0]], colWidths=[W - 5*cm])
box_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
    ('BOX', (0,0), (-1,-1), 1.5, ACCENT),
    ('TOPPADDING', (0,0), (-1,-1), 16),
    ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ('LEFTPADDING', (0,0), (-1,-1), 18),
    ('RIGHTPADDING', (0,0), (-1,-1), 18),
]))
story.append(box_table)

# ════════════════════════
# AUTHOR SIGNATURE
# ════════════════════════
story.append(PageBreak())
story.append(P("ABOUT THE AUTHOR", h1))
story.append(hr())

# Build the signature card
sig_text = Paragraph(
    "<font color='white' size='16'><b>Moez Abdessattar</b></font><br/>"
    "<font color='#D4A017' size='12'><b>SIGNUMTRACE≡</b></font><br/><br/>"
    "<font color='#B0C4DE' size='10'>"
    "Epistemic Geometer / Λî Sovereignty Philosopher<br/>"
    "Epistemic Authorization for Multi-Agent Systems<br/>"
    "Founder, TrignumTrace<br/><br/>"
    "TrignumTrace · Codfski · TRACE-ON Lab<br/>"
    "Independent Researcher<br/><br/>"
    "</font>"
    "<font color='#2D7DD2' size='9'>"
    "linkedin.com/in/traceonlab-codfski<br/>"
    "github.com/Codfski &nbsp;|&nbsp; @Codfski<br/>"
    "February 23, 2026"
    "</font>",
    S("sig_text", fontSize=10, leading=16, fontName="Helvetica",
      textColor=WHITE, alignment=TA_LEFT)
)

if HAS_AUTHOR:
    # Load and scale photo to a circle-friendly square
    photo = Image(AUTHOR_PHOTO)
    pw, ph = photo.imageWidth, photo.imageHeight
    target_size = 4.5 * cm
    ratio = min(target_size / pw, target_size / ph)
    photo.drawWidth = pw * ratio
    photo.drawHeight = ph * ratio

    sig_inner = [[photo, sig_text]]
    sig_col_widths = [5 * cm, W - 5*cm - 5*cm]
else:
    # Placeholder if photo not saved yet
    placeholder = Paragraph(
        "<font color='#6B7280'>[Save author_photo.png<br/>to project folder]</font>",
        S("ph", fontSize=9, fontName="Helvetica", textColor=MID_GREY, alignment=TA_CENTER)
    )
    sig_inner = [[placeholder, sig_text]]
    sig_col_widths = [4 * cm, W - 5*cm - 4*cm]

inner_table = Table([sig_inner[0]], colWidths=sig_col_widths)
inner_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ('TOPPADDING', (0, 0), (-1, -1), 0),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
]))

# Wrap in dark navy card with gold border
outer_table = Table([[inner_table]], colWidths=[W - 5*cm])
outer_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), NAVY),
    ('BOX', (0, 0), (-1, -1), 2, GOLD),
    ('TOPPADDING', (0, 0), (-1, -1), 24),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 24),
    ('LEFTPADDING', (0, 0), (-1, -1), 16),
    ('RIGHTPADDING', (0, 0), (-1, -1), 16),
]))

story.append(outer_table)

# Date stamp below
story.append(sp(0.4))
story.append(P(
    "<i>Trignumentality — Born February 23, 2026 — The day philosophy met code.</i>",
    S("stamp", fontSize=9, fontName="Helvetica-Oblique", textColor=MID_GREY,
      alignment=TA_CENTER, spaceBefore=6)
))

# ── Build PDF ─────────────────────────────────────────────────────────────────

def on_first_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 7)
    canvas.setFillColor(MID_GREY)
    canvas.drawCentredString(W/2, 1.2*cm,
        "TRIGNUMENTALITY — Abdessattar, M. (2026) — DOI: 10.5281/zenodo.18736774")
    canvas.restoreState()

def on_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MID_GREY)
    canvas.drawCentredString(W/2, 1.2*cm,
        f"TRIGNUMENTALITY — Moez Abdessattar (@Codfski) — February 23, 2026 — Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
print(f"✅ PDF generated: {OUTPUT_PDF}")
