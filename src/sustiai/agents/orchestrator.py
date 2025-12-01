"""Orchestrator / runner for the report pipeline.

Creates a SequentialAgent pipeline
and exposes a runner helper. The module is import-friendly in environments
without the ADK/GenAI SDKs.
"""
from textwrap import dedent

from .data_collector import data_collector_agent
from .analyst import analyst_agent
from .reporter import reporting_agent
from .saver import saving_agent

try:
    from google.adk.agents import SequentialAgent
    from google.adk.runners import InMemoryRunner
    from google.adk.plugins.logging_plugin import LoggingPlugin
    HAS_ADK = True
except Exception:
    HAS_ADK = False

if not HAS_ADK:
    class SequentialAgent:
        def __init__(self, name=None, sub_agents=None):
            self.name = name
            self.sub_agents = sub_agents or []

        def __repr__(self):
            return f"<SequentialAgent name={self.name!r} sub_agents={len(self.sub_agents)!r}>"

    class InMemoryRunner:
        def __init__(self, agent=None, plugins=None):
            self.agent = agent
            self.plugins = plugins or []

        def __repr__(self):
            return f"<InMemoryRunner agent={getattr(self.agent,'name',None)!r}>"

    class LoggingPlugin:
        def __repr__(self):
            return "<LoggingPlugin/>"


# Build the pipeline (keeps the same sub_agents ordering as the notebook)
root_agent = SequentialAgent(
    name="ReportPipeline",
    sub_agents=[data_collector_agent, analyst_agent, reporting_agent, saving_agent],
)

# Create a runner object that users can import - in real environments this
# will be the InMemoryRunner from the ADK; the fallback above keeps imports stable.
runner = InMemoryRunner(agent=root_agent, plugins=[LoggingPlugin()])

__all__ = ["root_agent", "runner"]
