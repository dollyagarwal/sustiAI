import importlib
import os
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))


def test_data_collector_prefers_local(monkeypatch):
    # Force environment to prefer in-process MCP
    monkeypatch.setenv("USE_INPROC_MCP", "1")

    # reload the module so it picks up the env var at import time
    import src.sustiai.agents.data_collector as dc
    importlib.reload(dc)

    # If the shim loaded successfully, mcp_tools should not be None and
    # should either be a LocalMCPToolset instance (no ADK) or a list of
    # FunctionTool wrappers when ADK is present.
    from src.sustiai.mcp_tool_local import LocalMCPToolset

    assert getattr(dc, "mcp_tools", None) is not None
    from src.sustiai.mcp_tool_local import LocalMCPToolset

    if hasattr(dc.mcp_tools, "__iter__") and not isinstance(dc.mcp_tools, LocalMCPToolset):
        # ADK path: expect a non-empty list of tools (FunctionTool wrappers)
        assert isinstance(dc.mcp_tools, list)
        assert len(dc.mcp_tools) > 0
    else:
        assert isinstance(dc.mcp_tools, LocalMCPToolset)
