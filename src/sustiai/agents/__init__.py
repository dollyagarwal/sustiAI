"""Agents package

This package splits the agents into separate modules so they
can be imported cleanly. The modules include safe fallbacks so CI / local
environments without the Google ADK / GenAI SDK can still import them.
"""

from .data_collector import data_collector_agent
from .analyst import analyst_agent
from .reporter import reporting_agent
from .saver import saving_agent

__all__ = [
    "data_collector_agent",
    "analyst_agent",
    "reporting_agent",
    "saving_agent",
]
