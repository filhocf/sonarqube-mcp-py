"""SonarQube MCP Server — entry point."""

import os
from mcp.server.fastmcp import FastMCP
from sonarqube_mcp.client import SonarQubeClient

mcp = FastMCP("SonarQube")

# Config from env
SONARQUBE_URL = os.environ.get("SONARQUBE_URL", "http://localhost:9000")
SONARQUBE_TOKEN = os.environ.get("SONARQUBE_TOKEN", "")
SONARQUBE_VERIFY_SSL = os.environ.get("SONARQUBE_VERIFY_SSL", "false").lower() == "true"

client = SonarQubeClient(SONARQUBE_URL, SONARQUBE_TOKEN, verify_ssl=SONARQUBE_VERIFY_SSL)


@mcp.tool()
def search_sonarqube_projects(query: str | None = None, page_size: int = 50) -> dict:
    """Search for projects in SonarQube"""
    return client.search_projects(query, page_size)


@mcp.tool()
def get_project_quality_gate_status(project_key: str, branch: str | None = None) -> dict:
    """Get quality gate status for a project"""
    return client.get_quality_gate_status(project_key, branch)


@mcp.tool()
def get_component_measures(component: str, metric_keys: str, branch: str | None = None) -> dict:
    """Get metrics for a component (bugs, coverage, etc.)"""
    return client.get_measures(component, metric_keys, branch)


@mcp.tool()
def list_quality_gates() -> dict:
    """List all quality gates defined in SonarQube"""
    return client.list_quality_gates()


@mcp.tool()
def search_sonar_issues(project_key: str, severities: str | None = None,
                        statuses: str = "OPEN", page_size: int = 50,
                        branch: str | None = None) -> dict:
    """Search for issues (bugs, vulnerabilities, code smells) in a project"""
    return client.search_issues(project_key, severities, statuses, page_size, branch)


@mcp.tool()
def search_security_hotspots(project_key: str, status: str = "TO_REVIEW",
                             branch: str | None = None) -> dict:
    """Search for security hotspots in a project"""
    return client.search_hotspots(project_key, status, branch)


@mcp.tool()
def show_security_hotspot(hotspot_key: str) -> dict:
    """Get details of a specific security hotspot"""
    return client.show_hotspot(hotspot_key)


@mcp.tool()
def show_rule(rule_key: str) -> dict:
    """Get details of a SonarQube rule"""
    return client.show_rule(rule_key)


@mcp.tool()
def search_metrics() -> dict:
    """List all available metrics in SonarQube"""
    return client.search_metrics()


@mcp.tool()
def list_pull_requests(project_key: str) -> dict:
    """List pull requests analyzed for a project"""
    return client.list_pull_requests(project_key)


@mcp.tool()
def get_file_coverage_details(component: str, page_size: int = 100,
                              branch: str | None = None) -> dict:
    """Get coverage details for files in a project"""
    return client.get_component_tree(component, "coverage,lines_to_cover,uncovered_lines",
                                     sort_field="coverage", page_size=page_size, branch=branch)


@mcp.tool()
def search_files_by_coverage(component: str, page_size: int = 20,
                             branch: str | None = None) -> dict:
    """Find files with lowest coverage"""
    return client.get_component_tree(component, "coverage", sort_field="coverage",
                                     page_size=page_size, branch=branch)


@mcp.tool()
def get_duplications(file_key: str, branch: str | None = None) -> dict:
    """Get code duplications for a file"""
    return client.get_duplications(file_key, branch)


def main():
    """Start the SonarQube MCP server."""
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        mcp.settings.host = os.environ.get("MCP_HOST", "127.0.0.1")
        mcp.settings.port = int(os.environ.get("MCP_PORT", "8959"))
        mcp.settings.stateless_http = True
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
