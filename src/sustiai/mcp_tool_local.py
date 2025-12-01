"""A small in-process 'MCPToolset' shim that directly calls the
functions defined in src.sustiai.mcp_server.

This avoids using the stdio-based MCP client when running locally or
in CI and keeps the behavior deterministic for tests.
"""
from __future__ import annotations

from typing import Any, Dict, List
from . import mcp_server


class LocalMCPToolset:
    """Expose the same helper functions as the original mcp_server so
    agents can call them directly instead of using the stdio toolset.
    """

    def describe_database(self) -> str:
        return mcp_server.describe_database()

    def search_entities(self, query_string: str) -> Dict[str, List[Dict[str, Any]]]:
        return mcp_server.search_entities(query_string)

    def get_branding_config(self, company_id: int) -> Dict[str, Any]:
        return mcp_server.get_branding_config(company_id)

    def get_event_kpis(self, event_id: int) -> Dict[str, Any]:
        return mcp_server.get_event_kpis(event_id)

    def get_event_emissions_breakdown(self, event_id: int) -> List[Dict[str, Any]]:
        return mcp_server.get_event_emissions_breakdown(event_id)

    def get_company_portfolio_summary(self, company_id: int) -> Dict[str, Any]:
        return mcp_server.get_company_portfolio_summary(company_id)

    def get_company_monthly_emissions(self, company_id: int, year: str) -> List[Dict[str, Any]]:
        return mcp_server.get_company_monthly_emissions(company_id, year)

    def run_sql(self, query_text: str) -> List[Dict[str, Any]]:
        return mcp_server.run_sql(query_text)


__all__ = ["LocalMCPToolset"]
