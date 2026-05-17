# sonarqube-mcp-py

A Python MCP server for SonarQube — query projects, issues, quality gates, coverage, and security hotspots directly from any MCP-compatible AI agent.

Inspired by the [official SonarQube MCP Server](https://github.com/SonarSource/sonarqube-mcp-server) (Java/Kotlin), reimplemented in Python for lightweight deployment without JVM dependency.

## Install

```bash
uvx sonarqube-mcp-py
# or
pip install sonarqube-mcp-py
```

## Configuration

Set environment variables:

```bash
export SONARQUBE_URL=https://your-sonarqube-instance
export SONARQUBE_TOKEN=squ_your_token_here
export SONARQUBE_VERIFY_SSL=false  # optional, for self-signed certs
```

## Transport

- **stdio** (default): for `mcp.json` integration with Claude Desktop, Cursor, Kiro CLI, etc.
- **HTTP**: set `MCP_TRANSPORT=streamable-http` and optionally `MCP_PORT=8959`

## Available Tools

| Tool | Description |
|------|-------------|
| `search_sonarqube_projects` | Search for projects |
| `get_project_quality_gate_status` | Get quality gate status (OK/ERROR) |
| `get_component_measures` | Get metrics (bugs, coverage, code smells, etc.) |
| `list_quality_gates` | List all quality gate definitions |
| `search_sonar_issues` | Search issues by severity and status |
| `search_security_hotspots` | Find security hotspots to review |
| `show_security_hotspot` | Get hotspot details |
| `show_rule` | Get rule description and examples |
| `search_metrics` | List all available metrics |
| `list_pull_requests` | List analyzed pull requests |
| `get_file_coverage_details` | Get per-file coverage data |
| `search_files_by_coverage` | Find files with lowest coverage |
| `get_duplications` | Get code duplication details |

## MCP Client Configuration

### stdio (mcp.json)
```json
{
  "sonarqube": {
    "command": "sonarqube-mcp-py",
    "env": {
      "SONARQUBE_URL": "https://your-instance",
      "SONARQUBE_TOKEN": "squ_xxx"
    }
  }
}
```

### HTTP (standalone service)
```json
{
  "sonarqube": {
    "url": "http://localhost:8959/mcp"
  }
}
```

Start in HTTP mode:
```bash
MCP_TRANSPORT=streamable-http MCP_PORT=8959 sonarqube-mcp-py
```

## License

MIT
