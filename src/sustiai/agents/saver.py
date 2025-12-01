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


saving_instruction = dedent(r'''
You are provided with an html code for the events report in `{report}`, your only job is to save it using `save_html` tool in the default filepath of the tool
''')

_model_kwargs = {"model": "gemini-2.5-flash"}
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    _model_kwargs["api_key"] = GOOGLE_API_KEY

saving_agent = LlmAgent(
    name="Saver",
    model=Gemini(**_model_kwargs) if HAS_ADK else None,
    instruction=saving_instruction,
    # Always provide a list for `tools` (ADK validation requires a list type).
    tools=[],
    output_key="final_report",
)
