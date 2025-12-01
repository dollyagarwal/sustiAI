import sys
import pathlib

# Ensure repo root is on sys.path so tests can import `src.sustiai` when
# running under pytest (CI may not have the project installed).
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from src.sustiai import agents


def test_agents_package_imports():
    # Ensure the package re-exports agent objects
    assert hasattr(agents, "data_collector_agent")
    assert hasattr(agents, "analyst_agent")
    assert hasattr(agents, "reporting_agent")
    assert hasattr(agents, "saving_agent")


def test_agents_have_instruction_text():
    # Agents created from notebook prompts should keep the instruction text
    assert getattr(agents.data_collector_agent, "instruction", None) is not None
    assert getattr(agents.analyst_agent, "instruction", None) is not None
    assert getattr(agents.reporting_agent, "instruction", None) is not None
