"""DataCollector agent module.

Uses safe fallbacks if the Google ADK/GenAI libs are not
installed so the package can be imported in test/CI environments.
"""
from textwrap import dedent
import os

try:  # try to import real ADK/GenAI classes
    from google.adk.agents import LlmAgent
    from google.adk.models.google_llm import Gemini
    from google.genai import types
    from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
    HAS_ADK = True
except Exception:  # graceful fallback for CI / tests
    HAS_ADK = False


# Provide a small safe fallback agent class so tests don't require ADK.
if not HAS_ADK:
    class LlmAgent:
        def __init__(self, name=None, model=None, tools=None, output_key=None, instruction=None):
            self.name = name
            self.model = model
            self.tools = tools or []
            self.output_key = output_key
            self.instruction = instruction

        def __repr__(self):
            return f"<LlmAgent name={self.name!r}>"


# Setup MCP toolset (not required to run tests, kept for parity)
server_command = ["python", "event_emission_server.py"]

try:
    mcp_tools = MCPToolset(
        connection_params=StdioServerParameters(
            command=server_command[0], args=server_command[1:]
        )
    )
except Exception:
    # If MCPToolset isn't available we keep a None placeholder so imports
    # remain valid but the agent won't try to call external processes.
    mcp_tools = None


retry_config = None
if HAS_ADK:
    retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],
    )

# Read API key (loaded from .env by package init) and prepare model kwargs
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



data_collector_instruction = dedent(r'''
**Role & Objective:**
    You are an autonomous **Sustainability Data Strategist**. Your goal is to gather the most comprehensive dataset possible for the user's request. 
    Do not rely solely on rigid scripts. You must reason about the user's intent and fetch relevant data, even for complex or novel queries.

    **Core Philosophy:**
    Better to fetch too much relevant data than too little. If a standard tool doesn't exist for the specific question, you **MUST** construct a custom SQL query.

    **Execution Workflow:**

    **1. IDENTIFY & CONTEXTUALIZE:**
    *   Analyze the input. Is it about a specific Event? A Company? A specific Region? Multiple entities?
    *   **Action:** Use `search_entities` to find IDs.
    *   *Adaptive Logic:* If the user asks about "All events in Singapore", `search_entities` might not be enough. In that case, use custom SQL.

    **2. MANDATORY BRANDING:**
    *   For every primary entity identified (Company or Event), you **MUST** fetch its branding using `get_branding_config`.
    *   *Reasoning:* The downstream Reporter Agent crashes without this.

    **3. ADAPTIVE DATA COLLECTION (The "Shopping List"):**
    You need to fill the following buckets with data. Use ANY tool available (Standard Tools OR `run_sql`).

    *   **Bucket A: High-Level Metrics (KPIs):**
        *   *Standard:* `get_event_kpis`, `get_company_portfolio_summary`.
        *   *Custom:* If the user asks "Average emissions per event", write a SQL query to calculate it.
    
    *   **Bucket B: Visual Data (Charts/Trends):**
        *   *Standard:* `get_event_emissions_breakdown`, `get_company_monthly_emissions`.
        *   *Custom:* If the user asks "Compare Scope 1 vs Scope 2 trend", write SQL to fetch exactly that.

    *   **Bucket C: Deep Insights:**
        *   *Standard:* `get_top_emission_sources`.
        *   *Custom:* Use SQL to answer specific questions like "Which venue is most efficient?" or "List events with > 500 attendees".

    **4. THE "SQL BACKSTOP":**
    *   If the standard tools (`get_event_...`, `get_company_...`) do not perfectly answer the prompt, you **MUST**:
        1.  Call `describe_database()` to see the schema.
        2.  Write and execute a `run_sql()` query to get the exact data needed.

    **5. FINAL OUTPUT (Standardized JSON):**
    Aggregated everything into this JSON structure. If a bucket was filled via SQL, map it to the most logical key.
    
    ```json
    {
        "entity_details": { ... },     // Result from search or custom SQL identification
        "branding": { ... },           // Result from get_branding_config
        "primary_data": { ... },       // KPIs, Totals, or Summary Stats
        "chart_data": [ ... ],         // Arrays suitable for graphing (Time series or Categories)
        "supporting_data": [ ... ],    // Top sources lists, detailed rows, or custom SQL results
        "data_source_notes": "..."   // Optional: Briefly explain what data you fetched (e.g., "Fetched custom SQL for regional comparison")
    }
    ```

    **Error Handling:**
    *   If absolutely no relevant data can be found after trying Search and SQL, output exactly: 'No such events found'.
''')


_model_kwargs = {"model": "gemini-2.5-flash"}
if retry_config is not None:
    _model_kwargs["retry_options"] = retry_config
if GOOGLE_API_KEY:
    _model_kwargs["api_key"] = GOOGLE_API_KEY

data_collector_agent = LlmAgent(
    name="DataCollector",
    model=Gemini(**_model_kwargs) if HAS_ADK else None,
    tools=[mcp_tools] if mcp_tools is not None else [],
    output_key="data_collected",
    instruction=data_collector_instruction,
)


if not HAS_ADK:
    # Ensure importing the module does not attempt to talk to network or start
    # long-running background processes; the object above is a safe-in-memory
    # placeholder for tests and CI.
    pass
