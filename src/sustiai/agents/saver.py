from textwrap import dedent
import os

try:
    from google.adk.agents import LlmAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.tools import FunctionTool
    HAS_ADK = True
except Exception:
    HAS_ADK = False

if not HAS_ADK:
    class LlmAgent:
        def __init__(self, name=None, model=None, instruction=None, tools=None, output_key=None):
            self.name = name
            self.model = model
            self.instruction = instruction
            self.tools = tools or []
            self.output_key = output_key

        def __repr__(self):
            return f"<LlmAgent name={self.name!r}>"


def save_html(html_code: str, file_path: str = "reports/company.html") -> str:
    """
    This helps save the html file into memory. 
    Send the "company" in the the file_path parameter along with reports directory. Example: "reports/{company}.html 
    where company is the name of the company for which report is generated
    """
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_code)
    return file_path


saving_instruction = dedent(r'''
You are provided with an html code for the events report in `{report}`, your only job is to save it using `save_html` tool and return the file path where it is saved.
''')

_model_kwargs = {"model": "gemini-2.5-flash-lite"}
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    _model_kwargs["api_key"] = GOOGLE_API_KEY



saving_agent = LlmAgent(
    name="Saver",
    model=Gemini(**_model_kwargs) if HAS_ADK else None,
    instruction=saving_instruction,
    # Always provide a list for `tools` (ADK validation requires a list type).
    tools=[save_html],
    output_key="final_report",
)
