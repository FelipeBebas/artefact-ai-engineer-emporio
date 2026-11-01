import os
import sys
import base64
import re
import subprocess
import shutil
from pathlib import Path
import markdown

ROOT_DIR = Path(r"e:\@Vault\[01] Conhecimento & Carreira\Portfolio & CV\Artefact")
README_PATH = ROOT_DIR / "README.md"
SCENARIOS_PATH = ROOT_DIR / "docs" / "cenarios_interacao.md"
SCREENSHOT_PATH = ROOT_DIR / "docs" / "assets" / "demo_screenshot.png"
OUTPUT_HTML_PATH = ROOT_DIR / "temp_doc.html"
OUTPUT_PDF_PATH = ROOT_DIR / "README.pdf"
DOCS_PDF_PATH = ROOT_DIR / "Emporio_da_Musica_AI_Engineer_Artefact_Documentation.pdf"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def get_base64_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/png;base64,{b64}"

def get_svg_architecture() -> str:
    return '''<div class="diagram-wrapper">
  <svg viewBox="0 0 820 620" xmlns="http://www.w3.org/2000/svg" class="architecture-svg">
    <defs>
      <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#831843" />
        <stop offset="100%" stop-color="#be123c" />
      </linearGradient>
      <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1e3a8a" />
        <stop offset="100%" stop-color="#2563eb" />
      </linearGradient>
      <linearGradient id="slateGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#334155" />
        <stop offset="100%" stop-color="#1e293b" />
      </linearGradient>
      <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="125%">
        <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.10"/>
      </filter>
      <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#475569" />
      </marker>
      <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#e11d48" />
      </marker>
      <marker id="arrowGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 8 5 L 0 9 z" fill="#10b981" />
      </marker>
    </defs>

    <!-- Outer Card -->
    <rect width="820" height="620" rx="14" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" />

    <!-- 1. Customer -->
    <rect x="300" y="22" width="220" height="38" rx="19" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.8" filter="url(#cardShadow)"/>
    <text x="410" y="46" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="13" font-weight="600" fill="#0f172a" text-anchor="middle">👤 Customer / WhatsApp User</text>

    <!-- Flow: Customer -> UI -->
    <line x1="410" y1="60" x2="410" y2="82" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- 2. UI / API Gateway -->
    <rect x="230" y="82" width="360" height="42" rx="8" fill="url(#blueGrad)" filter="url(#cardShadow)"/>
    <text x="410" y="108" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="13" font-weight="600" fill="#ffffff" text-anchor="middle">💬 Chat UI (Chainlit) &nbsp;|&nbsp; ⚡ REST API (FastAPI)</text>

    <!-- Flow: UI -> Engine -->
    <line x1="410" y1="124" x2="410" y2="146" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- 3. LangGraph Engine -->
    <rect x="180" y="146" width="460" height="42" rx="8" fill="url(#slateGrad)" filter="url(#cardShadow)"/>
    <text x="410" y="172" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" font-weight="600" fill="#ffffff" text-anchor="middle">⚙️ LangGraph StateGraph Engine (MessagesState & MemorySaver Checkpointer)</text>

    <!-- Flow: Engine -> Agent Node -->
    <line x1="410" y1="188" x2="410" y2="212" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Subgraph: Agent Node & Guardrails -->
    <rect x="120" y="214" width="580" height="130" rx="10" fill="#fdf2f8" stroke="#f472b6" stroke-width="1.5" stroke-dasharray="4 3"/>
    <rect x="140" y="206" width="180" height="20" rx="4" fill="#f43f5e" />
    <text x="230" y="220" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">🧠 Agent Node & Guardrails</text>

    <!-- LLM Persona Box -->
    <rect x="150" y="234" width="520" height="38" rx="6" fill="#ffffff" stroke="#fda4af" stroke-width="1.5"/>
    <text x="410" y="258" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" font-weight="600" fill="#881337" text-anchor="middle">🤖 LLM Specialist Persona (Empathetic, Concise & Instruments-Focused)</text>

    <line x1="410" y1="272" x2="410" y2="292" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Scope Guardrail Box -->
    <rect x="230" y="292" width="360" height="38" rx="6" fill="#ffffff" stroke="#e11d48" stroke-width="1.8"/>
    <text x="410" y="316" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" font-weight="700" fill="#be123c" text-anchor="middle">🛡️ Scope Guardrail: Accessories Intercept?</text>

    <!-- Left Path: Refusal -->
    <path d="M 230 311 L 105 311 L 105 372" fill="none" stroke="#e11d48" stroke-width="2" stroke-dasharray="4 2" marker-end="url(#arrowRed)"/>
    <text x="155" y="303" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10" font-weight="700" fill="#be123c" text-anchor="middle">Yes (Strings/Amps)</text>

    <rect x="15" y="374" width="180" height="58" rx="8" fill="#fff1f2" stroke="#f43f5e" stroke-width="1.5" filter="url(#cardShadow)"/>
    <text x="105" y="398" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11" font-weight="700" fill="#9f1239" text-anchor="middle">🚫 Cordial Redirection</text>
    <text x="105" y="416" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="9.5" fill="#4c0519" text-anchor="middle">(Instruments-Only & Referral)</text>

    <!-- Down Path: In-Scope -->
    <line x1="410" y1="330" x2="410" y2="372" stroke="#10b981" stroke-width="2" marker-end="url(#arrowGreen)"/>
    <text x="475" y="354" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10.5" font-weight="700" fill="#047857" text-anchor="middle">No (In-Scope Query)</text>

    <!-- Decision Box -->
    <rect x="300" y="374" width="220" height="42" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5" filter="url(#cardShadow)"/>
    <text x="410" y="400" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" font-weight="700" fill="#065f46" text-anchor="middle">🔍 Tool Invocation Needed?</text>

    <!-- Right Path: Direct Reply -->
    <path d="M 520 395 L 620 395" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)"/>
    <text x="570" y="387" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10" font-weight="600" fill="#475569" text-anchor="middle">No (FAQ)</text>

    <rect x="622" y="374" width="180" height="42" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#cardShadow)"/>
    <text x="712" y="400" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="11.5" font-weight="600" fill="#334155" text-anchor="middle">📝 Direct Reply</text>

    <!-- Down Path: Tools -->
    <line x1="410" y1="416" x2="410" y2="446" stroke="#0d9488" stroke-width="2" marker-end="url(#arrow)"/>
    <text x="430" y="434" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10" font-weight="700" fill="#0f766e" text-anchor="start">Yes (Data / Policy Query)</text>

    <!-- Tool Node Container -->
    <rect x="25" y="448" width="770" height="88" rx="10" fill="#f0fdfa" stroke="#5eead4" stroke-width="1.5"/>
    <rect x="45" y="440" width="160" height="18" rx="4" fill="#0d9488"/>
    <text x="125" y="453" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10" font-weight="700" fill="#ffffff" text-anchor="middle">🛠️ Deterministic Tool Node</text>

    <!-- 4 Tools -->
    <rect x="35" y="466" width="175" height="56" rx="6" fill="#ffffff" stroke="#99f6e4" stroke-width="1.2"/>
    <text x="122" y="487" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10.5" font-weight="700" fill="#134e4a" text-anchor="middle">🎸 consultar_catalogo</text>
    <text x="122" y="506" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="9" fill="#0f766e" text-anchor="middle">SQLite Filter (Price, Stock)</text>

    <rect x="225" y="466" width="175" height="56" rx="6" fill="#ffffff" stroke="#99f6e4" stroke-width="1.2"/>
    <text x="312" y="487" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10.5" font-weight="700" fill="#134e4a" text-anchor="middle">📦 consultar_pedido</text>
    <text x="312" y="506" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="9" fill="#0f766e" text-anchor="middle">Lookup (ID, Tracking, Tel)</text>

    <rect x="415" y="466" width="175" height="56" rx="6" fill="#ffffff" stroke="#99f6e4" stroke-width="1.2"/>
    <text x="502" y="487" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10.5" font-weight="700" fill="#134e4a" text-anchor="middle">💳 consultar_promocoes</text>
    <text x="502" y="506" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="9" fill="#0f766e" text-anchor="middle">Active Discounts (PIX 5%)</text>

    <rect x="605" y="466" width="175" height="56" rx="6" fill="#ffffff" stroke="#99f6e4" stroke-width="1.2"/>
    <text x="692" y="487" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10.5" font-weight="700" fill="#134e4a" text-anchor="middle">📋 consultar_politicas</text>
    <text x="692" y="506" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="9" fill="#0f766e" text-anchor="middle">Zero-Flake Pydantic Enum</text>

    <!-- Path Tools -> Grounding -->
    <path d="M 410 536 L 410 560" fill="none" stroke="#0d9488" stroke-width="2" marker-end="url(#arrow)"/>

    <!-- Grounding Node -->
    <rect x="190" y="560" width="440" height="42" rx="8" fill="url(#primaryGrad)" filter="url(#cardShadow)"/>
    <text x="410" y="586" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="12" font-weight="700" fill="#ffffff" text-anchor="middle">✨ Grounded Answer Synthesis (Zero Hallucinations)</text>
  </svg>
</div>'''

def process_scenarios_html(scenarios_raw: str) -> str:
    # Separate the intro/index and the individual scenarios
    parts = re.split(r'\n---\n', scenarios_raw)
    intro_part = parts[0]
    scenario_parts = parts[1:]

    md_exts = ['tables', 'fenced_code', 'nl2br']
    intro_html = markdown.markdown(intro_part, extensions=md_exts)

    scenario_cards_html = []
    for part in scenario_parts:
        part_trimmed = part.strip()
        if not part_trimmed:
            continue
        card_content = markdown.markdown(part_trimmed, extensions=md_exts)
        # Style customer vs agent quotes specifically
        card_content = re.sub(
            r'<li>\s*<p><strong>Cliente:</strong></p>\s*<blockquote>(.*?)</blockquote>\s*</li>',
            r'<div class="dialogue-box client-box"><strong>👤 Cliente:</strong><blockquote>\1</blockquote></div>',
            card_content,
            flags=re.DOTALL
        )
        card_content = re.sub(
            r'<li>\s*<p><strong>Resposta da Empório da Música:</strong></p>\s*<blockquote>(.*?)</blockquote>\s*</li>',
            r'<div class="dialogue-box agent-box"><strong>🎸 Empório da Música:</strong><blockquote>\1</blockquote></div>',
            card_content,
            flags=re.DOTALL
        )
        scenario_cards_html.append(f'<div class="scenario-card">{card_content}</div>')

    return intro_html + "\n" + "\n".join(scenario_cards_html)

def build_html():
    readme_raw = README_PATH.read_text(encoding="utf-8")
    scenarios_raw = SCENARIOS_PATH.read_text(encoding="utf-8")

    # Replace demo.gif with embedded high-res screenshot
    screenshot_b64 = get_base64_image(SCREENSHOT_PATH)
    img_tag = (
        f'<div class="demo-screenshot-container">'
        f'<img src="{screenshot_b64}" class="demo-img" alt="Empório da Música AI Agent UI Demo" />'
        f'</div>'
    )
    readme_raw = re.sub(r'<img\s+src="docs/assets/demo\.gif"[^>]*>', img_tag, readme_raw)

    # Replace mermaid block with unique placeholder
    DIAGRAM_TOKEN = "<!-- ARCHITECTURE_DIAGRAM_PLACEHOLDER -->"
    readme_raw = re.sub(r'```mermaid[\s\S]*?```', DIAGRAM_TOKEN, readme_raw)

    # Convert README Markdown to HTML
    md_extensions = ['tables', 'fenced_code', 'nl2br']
    readme_html = markdown.markdown(readme_raw, extensions=md_extensions)

    # Substitute diagram
    svg_markup = get_svg_architecture()
    readme_html = readme_html.replace(f"<p>{DIAGRAM_TOKEN}</p>", svg_markup)
    readme_html = readme_html.replace(DIAGRAM_TOKEN, svg_markup)

    # Remove <hr /> elements directly preceding section headers to prevent blank pages
    readme_html = re.sub(r'<hr\s*/?>\s*(?=<h2)', '', readme_html)

    # Insert page breaks on specific section headers
    readme_html = re.sub(
        r'(<h2[^>]*>.*?System Architecture.*?</h2>)',
        r'<div class="page-break"></div>\1',
        readme_html,
        flags=re.IGNORECASE
    )
    readme_html = re.sub(
        r'(<h2[^>]*>.*?Getting Started.*?</h2>)',
        r'<div class="page-break"></div>\1',
        readme_html,
        flags=re.IGNORECASE
    )
    readme_html = re.sub(
        r'(<h2[^>]*>.*?Technical Decisions.*?</h2>)',
        r'<div class="page-break"></div>\1',
        readme_html,
        flags=re.IGNORECASE
    )
    readme_html = re.sub(
        r'(<h2[^>]*>.*?Known Limitations.*?</h2>)',
        r'<div class="page-break"></div>\1',
        readme_html,
        flags=re.IGNORECASE
    )

    # Process Scenarios with clean cards and styled dialogue boxes
    scenarios_html = process_scenarios_html(scenarios_raw)

    full_html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Empório da Música — AI Customer Service Agent Documentation</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 15mm 14mm 15mm 14mm;
    }}

    * {{
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 9.5pt;
      line-height: 1.5;
      color: #1e293b;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }}

    /* Top Badges */
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2.5px solid #831843;
      padding-bottom: 8px;
      margin-bottom: 14px;
    }}
    .badge-primary {{
      background: #831843;
      color: #ffffff;
      font-size: 8pt;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .badge-release {{
      background: #0284c7;
      color: #ffffff;
      font-size: 8pt;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
    }}
    .header-tagline {{
      font-size: 8.5pt;
      color: #64748b;
      font-weight: 500;
    }}

    /* Typography */
    h1 {{
      font-size: 18pt;
      color: #0f172a;
      margin: 2px 0 8px 0;
      line-height: 1.25;
      font-weight: 800;
      letter-spacing: -0.3px;
    }}

    h2 {{
      font-size: 13pt;
      color: #831843;
      border-bottom: 1.5px solid #f1f5f9;
      padding-bottom: 4px;
      margin-top: 18px;
      margin-bottom: 10px;
      page-break-after: avoid;
      font-weight: 700;
    }}

    h3 {{
      font-size: 10.5pt;
      color: #0f172a;
      margin-top: 14px;
      margin-bottom: 6px;
      page-break-after: avoid;
      font-weight: 700;
    }}

    p, li {{
      margin-top: 0;
      margin-bottom: 7px;
      color: #334155;
    }}

    ul, ol {{
      margin-top: 2px;
      margin-bottom: 10px;
      padding-left: 20px;
    }}

    li {{
      margin-bottom: 3px;
    }}

    hr {{
      border: 0;
      height: 1px;
      background: #e2e8f0;
      margin: 14px 0;
    }}

    /* Blockquotes */
    blockquote {{
      background: #f8fafc;
      border-left: 3.5px solid #831843;
      margin: 6px 0 10px 0;
      padding: 7px 12px;
      color: #334155;
      border-radius: 0 6px 6px 0;
      page-break-inside: avoid;
    }}
    blockquote p {{
      margin: 0 0 4px 0;
    }}
    blockquote p:last-child {{
      margin: 0;
    }}

    /* Links */
    a {{
      color: #0284c7;
      text-decoration: underline;
      text-underline-offset: 2px;
      word-break: break-all;
    }}

    /* Code Blocks */
    code {{
      font-family: "Cascadia Code", Consolas, "Courier New", monospace;
      font-size: 8.2pt;
      background-color: #f1f5f9;
      color: #0f172a;
      padding: 1.5px 4.5px;
      border-radius: 3.5px;
      border: 1px solid #e2e8f0;
    }}

    pre {{
      background-color: #0f172a;
      color: #f8fafc;
      padding: 9px 12px;
      border-radius: 6px;
      font-size: 8pt;
      line-height: 1.4;
      overflow-x: auto;
      page-break-inside: avoid;
      margin: 6px 0 10px 0;
      border: 1px solid #1e293b;
    }}
    pre code {{
      background: transparent;
      color: inherit;
      padding: 0;
      border: none;
      font-size: inherit;
    }}

    /* Screenshot container */
    .demo-screenshot-container {{
      text-align: center;
      margin: 6px 0 10px 0;
      page-break-inside: avoid;
    }}
    .demo-img {{
      max-width: 65%;
      max-height: 480px;
      height: auto;
      border-radius: 8px;
      border: 1.5px solid #cbd5e1;
      box-shadow: 0 4px 10px rgba(0,0,0,0.10);
    }}

    /* Diagram */
    .diagram-wrapper {{
      width: 100%;
      margin: 10px 0;
      text-align: center;
      page-break-inside: avoid;
    }}
    .architecture-svg {{
      width: 100%;
      max-width: 760px;
      height: auto;
    }}

    /* Page Breaks */
    .page-break {{
      page-break-before: always;
      break-before: page;
      height: 0;
      margin: 0;
      padding: 0;
    }}

    /* Documentation Section Divider */
    .doc-divider-card {{
      background: linear-gradient(135deg, #042f2e, #0f766e);
      color: #ffffff;
      border-radius: 8px;
      padding: 14px 18px;
      margin-bottom: 18px;
      box-shadow: 0 3px 10px rgba(15, 118, 110, 0.15);
    }}
    .doc-divider-card h2 {{
      color: #ffffff;
      border: none;
      margin: 0 0 6px 0;
      padding: 0;
      font-size: 14pt;
    }}
    .doc-divider-card p {{
      color: #ccfbf1;
      margin: 0;
      font-size: 9pt;
      line-height: 1.45;
    }}

    /* Scenario Card */
    .scenario-card {{
      page-break-inside: avoid;
      break-inside: avoid;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .scenario-card h3 {{
      color: #0f766e;
      margin-top: 2px;
      margin-bottom: 6px;
      font-size: 11pt;
      border-bottom: 1px solid #f0fdfa;
      padding-bottom: 4px;
    }}

    .dialogue-box {{
      margin: 8px 0;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 9.2pt;
    }}
    .client-box {{
      background: #f8fafc;
      border-left: 3.5px solid #64748b;
    }}
    .client-box strong {{
      color: #334155;
    }}
    .client-box blockquote {{
      background: transparent;
      border: none;
      padding: 4px 0 0 0;
      margin: 0;
      font-style: italic;
      color: #1e293b;
    }}

    .agent-box {{
      background: #f0fdfa;
      border-left: 3.5px solid #0d9488;
    }}
    .agent-box strong {{
      color: #0f766e;
    }}
    .agent-box blockquote {{
      background: transparent;
      border: none;
      padding: 4px 0 0 0;
      margin: 0;
      font-style: normal;
      color: #0f172a;
    }}

    /* Table formatting */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0;
      font-size: 8.8pt;
      page-break-inside: avoid;
    }}
    th, td {{
      border: 1px solid #e2e8f0;
      padding: 5px 8px;
      text-align: left;
    }}
    th {{
      background-color: #f1f5f9;
      font-weight: 700;
      color: #0f172a;
    }}
    tr:nth-child(even) td {{
      background-color: #f8fafc;
    }}
  </style>
</head>
<body>

  <div class="header-bar">
    <div>
      <span class="badge-primary">Artefact AI Engineer Case</span>
      <span class="badge-release">Release v1.0.0</span>
    </div>
    <div class="header-tagline">
      Empório da Música &bull; Campo Grande, MS &bull; Outubro 2026
    </div>
  </div>

  <div class="content">
    {readme_html}

    <div class="page-break"></div>

    <div class="doc-divider-card">
      <h2>📑 Parte II: Documentação de Cenários de Interação</h2>
      <p>
        Evidências determinísticas de execução conversacional, validação de políticas da loja (Zero-Flake),
        consultas ao banco de dados relacional SQLite em tempo real e testes de guardrails de escopo (rejeição de acessórios).
      </p>
    </div>

    {scenarios_html}
  </div>

</body>
</html>
'''
    OUTPUT_HTML_PATH.write_text(full_html, encoding="utf-8")
    print(f"Generated HTML at {OUTPUT_HTML_PATH}")

def print_to_pdf(html_file: Path, pdf_file: Path):
    cmd = [
        EDGE_EXE,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file.resolve()}",
        str(html_file.resolve())
    ]
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Edge error: {result.stderr}")
        sys.exit(1)
    
    if pdf_file.exists():
        size_kb = pdf_file.stat().st_size / 1024
        print(f"SUCCESS: Generated {pdf_file.name} ({size_kb:.1f} KB)")
    else:
        print(f"ERROR: {pdf_file.name} was not created!")
        sys.exit(1)

if __name__ == "__main__":
    build_html()
    print_to_pdf(OUTPUT_HTML_PATH, OUTPUT_PDF_PATH)
    shutil.copyfile(OUTPUT_PDF_PATH, DOCS_PDF_PATH)
    print(f"SUCCESS: Copied to {DOCS_PDF_PATH.name}")
