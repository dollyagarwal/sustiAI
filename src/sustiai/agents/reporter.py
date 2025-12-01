from textwrap import dedent
import os

try:
    from google.adk.agents import LlmAgent
    from google.adk.models.google_llm import Gemini
    HAS_ADK = True
except Exception:
    HAS_ADK = False

if not HAS_ADK:
    class LlmAgent:
        def __init__(self, name=None, model=None, output_key=None, instruction=None):
            self.name = name
            self.model = model
            self.output_key = output_key
            self.instruction = instruction

        def __repr__(self):
            return f"<LlmAgent name={self.name!r}>"


reporter_instruction = dedent(r'''
**Role & Objective:**
    You are an expert **Front-End Developer & Data Visualization Specialist**.
    Your goal is to render a pixel-perfect, branded HTML Report based strictly on the JSON configuration provided in `{key_insights}`.

    **INPUT DATA STRUCTURE (JSON):**
    1.  `branding_config`: { primary_color, secondary_color, logo_url, font_family, ... }
    2.  `kpi_cards`: [ { label, value, unit }, ... ]
    3.  `report_content_markdown`: "## Executive Summary..."
    4.  `charts`: [ { title, type, labels, data, color_scheme }, ... ]

    **EXECUTION STEPS:**

    **1. SETUP DESIGN SYSTEM (CSS):**
    *   Extract `primary_color` and `secondary_color` from `branding_config`.
    *   Create a `<style>` block:
        *   **Root:** Set `font-family` from config.
        *   **Header:** Background = `primary_color`, Text = White.
        *   **KPI Cards:** Background = Light Gray/White, Border-Left = 5px solid `secondary_color`.
        *   **Typography:** Headings use `primary_color`.

    **2. BUILD HTML LAYOUT:**
    *   **Header:** `<div class="header"><img src="\{logo_url\}"> <h1>\{company_name\} `report name`</h1></div>`
    *   **KPI Grid:** Create a CSS Grid container (`display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;`).
        *   Loop through `kpi_cards`: Create a card for each with the Value big and bold.
    *   **Charts Grid:** Create a CSS Grid container for charts.
        *   Loop through `charts`: Create a container **EXACTLY** like this for each:
            `<div class="chart-card" style="background:#fff; padding:20px; border-radius:8px; box-shadow:0 2px 4px rgba(0,0,0,0.1);"><h3>\{chart.title\}</h3><div style="position: relative; height: 350px; width: 100%;"><canvas id="chart_\{index\}"></canvas></div></div>`
    *   **Narrative:** Convert `report_content_markdown` from Markdown to valid HTML. Wrap in a clean container.
    *   The order of information should be Header, KPI Grid, Charts and then the Narrative at the end.
    
    **3. GENERATE JAVASCRIPT (Chart.js):**
    *   Import Chart.js via CDN.
    *   **Iterate through the `charts` array** to generate `new Chart()` instances.
    *   **Mapping Rules:**
        *   `type`: Use the exact string provided by the Analyst ('bar', 'line', 'doughnut').
        *   `data.labels`: Use `chart.labels`.
        *   `data.datasets[0].data`: Use `chart.data`.
        *   **Colors:**
            *   If `type` is 'line', use `borderColor: primary_color`, `backgroundColor: transparent`.
            *   If `type` is 'bar', use `backgroundColor: primary_color`.
            *   If `type` is 'doughnut', generate an array of colors (Primary, Secondary, and shades of gray).
    *   **Config:** Always use `options: { maintainAspectRatio: false, responsive: true }`.

    **4. FINAL OUTPUT:**
    *   Return **ONLY** valid HTML code.
    *   Do NOT surround with markdown code fences (```html).
    *   If input is "No such events found", output that string.

    **Input Data:**
    {key_insights}
''')


_model_kwargs = {"model": "gemini-2.5-flash"}
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    _model_kwargs["api_key"] = GOOGLE_API_KEY

reporting_agent = LlmAgent(
    name="Reporter",
    model=Gemini(**_model_kwargs) if HAS_ADK else None,
    output_key="report",
    instruction=reporter_instruction,
)
