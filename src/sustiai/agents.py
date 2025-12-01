
"""Top-level agents module.

This file keeps backward compatibility so existing code that imports
``src.sustiai.agents`` keeps working. It re-exports the fine-grained
agent modules created under `src/sustiai/agents` and provides the
orchestrator `root_agent` and `runner` objects.
"""

from . import data_collector  # noqa: F401
from . import analyst  # noqa: F401
from . import reporter  # noqa: F401
from . import saver  # noqa: F401
from . import orchestrator  # noqa: F401

try:
    # Expose high-level names for backwards compatibility
    data_collector_agent = data_collector.data_collector_agent
    analyst_agent = analyst.analyst_agent
    reporting_agent = reporter.reporting_agent
    saving_agent = saver.saving_agent
    root_agent = orchestrator.root_agent
    runner = orchestrator.runner
except Exception:
    # If something goes wrong, importing the submodules will already raise
    # and tests/CI will be able to catch it. Keep this file declarative.
    pass

