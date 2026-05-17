"""SonarQube MCP Server — entry point."""

import os
from typing import Annotated, Optional
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from sonarqube_mcp.client import SonarQubeClient

mcp = FastMCP("SonarQube")

# Config from env
SONARQUBE_URL = os.environ.get("SONARQUBE_URL", "http://localhost:9000")
SONARQUBE_TOKEN = os.environ.get("SONARQUBE_TOKEN", "")
SONARQUBE_VERIFY_SSL = os.environ.get("SONARQUBE_VERIFY_SSL", "false").lower() == "true"

client = SonarQubeClient(SONARQUBE_URL, SONARQUBE_TOKEN, verify_ssl=SONARQUBE_VERIFY_SSL)


@mcp.tool(name="search_sonarqube_projects", description="Search for projects in SonarQube")
async def tool_search_projects(
    query: Annotated[Optional[str], Field(description="Search query (project name or key)", default=None)] = None,
    page_size: Annotated[int, Field(description="Max results", default=50)] = 50,
) -> dict:
    try:
        return client.search_projects(query, page_size)
    except Exception as e:
        raise ToolError(f"Error searching projects: {e}")


@mcp.tool(name="get_project_quality_gate_status", description="Get quality gate status for a project")
async def tool_quality_gate(
    project_key: Annotated[str, Field(description="Project key (e.g. 'my-project')")],
) -> dict:
    try:
        return client.get_quality_gate_status(project_key)
    except Exception as e:
        raise ToolError(f"Error getting quality gate: {e}")


@mcp.tool(name="get_component_measures", description="Get metrics for a component (bugs, coverage, etc.)")
async def tool_measures(
    component: Annotated[str, Field(description="Component key (project or file)")],
    metric_keys: Annotated[str, Field(description="Comma-separated metrics (e.g. 'bugs,vulnerabilities,coverage,code_smells')")],
) -> dict:
    try:
        return client.get_measures(component, metric_keys)
    except Exception as e:
        raise ToolError(f"Error getting measures: {e}")


@mcp.tool(name="list_quality_gates", description="List all quality gates defined in SonarQube")
async def tool_list_gates() -> dict:
    try:
        return client.list_quality_gates()
    except Exception as e:
        raise ToolError(f"Error listing quality gates: {e}")


@mcp.tool(name="search_sonar_issues", description="Search for issues (bugs, vulnerabilities, code smells) in a project")
async def tool_search_issues(
    project_key: Annotated[str, Field(description="Project key")],
    severities: Annotated[Optional[str], Field(description="Filter: BLOCKER,CRITICAL,MAJOR,MINOR,INFO", default=None)] = None,
    statuses: Annotated[str, Field(description="Filter: OPEN,CONFIRMED,REOPENED,RESOLVED,CLOSED", default="OPEN")] = "OPEN",
    page_size: Annotated[int, Field(description="Max results", default=50)] = 50,
) -> dict:
    try:
        return client.search_issues(project_key, severities, statuses, page_size)
    except Exception as e:
        raise ToolError(f"Error searching issues: {e}")


@mcp.tool(name="search_security_hotspots", description="Search for security hotspots in a project")
async def tool_search_hotspots(
    project_key: Annotated[str, Field(description="Project key")],
    status: Annotated[str, Field(description="Status: TO_REVIEW, REVIEWED", default="TO_REVIEW")] = "TO_REVIEW",
) -> dict:
    try:
        return client.search_hotspots(project_key, status)
    except Exception as e:
        raise ToolError(f"Error searching hotspots: {e}")


@mcp.tool(name="show_security_hotspot", description="Get details of a specific security hotspot")
async def tool_show_hotspot(
    hotspot_key: Annotated[str, Field(description="Hotspot key")],
) -> dict:
    try:
        return client.show_hotspot(hotspot_key)
    except Exception as e:
        raise ToolError(f"Error showing hotspot: {e}")


@mcp.tool(name="show_rule", description="Get details of a SonarQube rule")
async def tool_show_rule(
    rule_key: Annotated[str, Field(description="Rule key (e.g. 'java:S1234')")],
) -> dict:
    try:
        return client.show_rule(rule_key)
    except Exception as e:
        raise ToolError(f"Error showing rule: {e}")


@mcp.tool(name="search_metrics", description="List all available metrics in SonarQube")
async def tool_search_metrics() -> dict:
    try:
        return client.search_metrics()
    except Exception as e:
        raise ToolError(f"Error searching metrics: {e}")


@mcp.tool(name="list_pull_requests", description="List pull requests analyzed for a project")
async def tool_list_prs(
    project_key: Annotated[str, Field(description="Project key")],
) -> dict:
    try:
        return client.list_pull_requests(project_key)
    except Exception as e:
        raise ToolError(f"Error listing PRs: {e}")


@mcp.tool(name="get_file_coverage_details", description="Get coverage details for files in a project")
async def tool_file_coverage(
    component: Annotated[str, Field(description="Project key")],
    page_size: Annotated[int, Field(description="Max files", default=100)] = 100,
) -> dict:
    try:
        return client.get_component_tree(component, "coverage,lines_to_cover,uncovered_lines",
                                         sort_field="coverage", page_size=page_size)
    except Exception as e:
        raise ToolError(f"Error getting coverage: {e}")


@mcp.tool(name="search_files_by_coverage", description="Find files with lowest coverage")
async def tool_files_by_coverage(
    component: Annotated[str, Field(description="Project key")],
    page_size: Annotated[int, Field(description="Max files", default=20)] = 20,
) -> dict:
    try:
        return client.get_component_tree(component, "coverage", sort_field="coverage", page_size=page_size)
    except Exception as e:
        raise ToolError(f"Error searching by coverage: {e}")


@mcp.tool(name="get_duplications", description="Get code duplications for a file")
async def tool_duplications(
    file_key: Annotated[str, Field(description="File key (e.g. 'project:src/main/File.java')")],
) -> dict:
    try:
        return client.get_duplications(file_key)
    except Exception as e:
        raise ToolError(f"Error getting duplications: {e}")


def main():
    """Start the SonarQube MCP server."""
    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=int(os.environ.get("MCP_PORT", "8959")),
            path="/mcp",
        )
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
