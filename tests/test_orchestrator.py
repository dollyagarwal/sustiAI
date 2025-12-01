import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.sustiai.agents import orchestrator


def test_root_agent_and_runner_present():
    assert hasattr(orchestrator, "root_agent")
    assert hasattr(orchestrator, "runner")
    assert getattr(orchestrator.root_agent, "name", None) == "ReportPipeline"
