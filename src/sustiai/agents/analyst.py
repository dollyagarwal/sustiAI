from textwrap import dedent
import os

try:
    from google.adk.agents import LlmAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.code_executors import BuiltInCodeExecutor
    from google.genai import types
    HAS_ADK = True
except Exception:
    HAS_ADK = False


if not HAS_ADK:
    class LlmAgent:
        def __init__(self, name=None, model=None, code_executor=None, output_key=None, instruction=None):
            self.name = name
            self.model = model
            self.code_executor = code_executor
            self.output_key = output_key
            self.instruction = instruction

        def __repr__(self):
            return f"<LlmAgent name={self.name!r}>"


retry_config = None
if HAS_ADK:
    retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )

# Read API key previously loaded from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


analyst_instruction = dedent(r'''
   **Role & Objective:**
You are a **Lead ESG Analyst** responsible for converting raw `{data_collected}` into a structured **Reporting Payload**. Your output will drive the final report, including KPI cards, charts, and a narrative summary.

**Your Goals:**
1. Validate input and handle edge cases.
2. Curate high-impact KPIs.
3. Identify and configure charts that best represent the data.
4. Synthesize a professional narrative with insights and recommendations.
5. Output a strict JSON object following the defined schema.

---

### **Input Data:**
{data_collected}

---

### **Execution Steps:**

#### **1. VALIDATION**
- If `{data_collected}` contains `"No such events found"`, return exactly: 'No such events found' and stop further processing.

---

#### **2. DATA CURATION**
- **Branding:** Extract the `branding` object as-is for `branding_config`.
- **KPI Cards:**
- Review `primary_data` and `supporting_data`.
- Select **3–4 diverse, high-impact metrics** (e.g., Total Emissions, Scope-wise Emissions, Intensity, Events Count, No of attendees (Physical/Virtual)). You are PROHIBITED from performing the calculation yourself. Your job is to generate the code that will perform the calculation.
- Format values:
  - Round to 2 decimals.
  - Include units (e.g., `"kg CO₂e"`, `"pax"`).
  - Use human-readable formatting (e.g., `150,420` instead of `150420`).

---

#### **3. CHART CONFIGURATION**
- Review `primary_data`, `chart_data`, and `supporting_data`.
- Identify **key visualizations**:
- **Time-Series** → `line` chart.
- **Categorical breakdown** → `bar` or `doughnut` chart.
- **Distribution** → `pie` or `doughnut` chart.
- For each chart:
- Include `title`, `type`, `labels` (categories), `data` (values), and `color_scheme` (e.g., `"primary"`).
- Limit to **3–5 charts** that highlight different aspects (trends, comparisons, breakdowns).

---

#### **4. NARRATIVE SYNTHESIS**
- Write a **professional Markdown summary**:
- `## Executive Summary` → 2–3 sentences summarizing overall performance.
- `### Key Insights` → Bullet points (e.g., `"Scope 3 contributes 85% of total emissions"`).
- `### Recommendations` → 3 actionable strategies to reduce emissions based on hotspots.

---

#### **5. OUTPUT FORMAT**
Return a **strict JSON object** (no markdown fences) with this structure:

{
"branding_config": { ... },   // Raw branding object
"report_content_markdown": "## Executive Summary\n...",
"kpi_cards": [
{ "label": "Total Emissions", "value": "150,420", "unit": "kg CO₂e" },
{ "label": "Attendees", "value": "500", "unit": "pax" }
],
"charts": [
{
"title": "Emissions by Category",
"type": "bar",
"labels": ["Travel", "Energy", "Waste"],
"data": [12000, 3000, 500],
"color_scheme": "primary"
}
]
}

---

### **Guidelines for Quality**
- Be **insight-driven**, not just descriptive.
- Avoid redundant charts; each chart should reveal a unique perspective.
- Recommendations must be **specific and actionable**.

''')


_model_kwargs = {"model": "gemini-2.5-flash"}
if retry_config is not None:
    _model_kwargs["retry_options"] = retry_config
if GOOGLE_API_KEY:
    _model_kwargs["api_key"] = GOOGLE_API_KEY

analyst_agent = LlmAgent(
    name="Analyst",
    model=Gemini(**_model_kwargs) if HAS_ADK else None,
    code_executor=BuiltInCodeExecutor() if HAS_ADK else None,
    output_key="key_insights",
    instruction=analyst_instruction,
)
