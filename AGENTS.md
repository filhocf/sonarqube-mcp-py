# AGENTS.md

## Project Overview

MCP server for SonarQube — query projects, issues, quality gates, coverage, and security hotspots via REST API. Built with Python (FastMCP), pure Python (no JVM). Supports stdio and Streamable HTTP transport. Entry point: `src/sonarqube_mcp/server.py`.

## Architecture

```
src/sonarqube_mcp/
├── __init__.py          ← Package version
├── server.py            ← FastMCP server, registers all 13 tools, transport selection
└── client.py            ← SonarQube REST API client (thin wrapper, requests.Session)
```

**Data flow:** Tool call → client method → HTTP GET to SonarQube API → return JSON response.

## Key Conventions

- **Lazy connection**: no connection at startup. API calls happen only when tools are invoked.
- **Auth**: token-based (`SONARQUBE_TOKEN` as username, empty password).
- **SSL**: `SONARQUBE_VERIFY_SSL=false` for self-signed certs (common in enterprise).
- **Transport**: `MCP_TRANSPORT=stdio` (default) or `streamable-http` (port via `MCP_PORT`, default 8959).
- **Error handling**: raise `ToolError` for user-facing errors. Network failures return descriptive message.

## Adding a New Tool

1. Add API method to `client.py` (thin wrapper around `self._get(endpoint, params)`).
2. Register tool in `server.py` with `@mcp.tool(name=..., description=...)`.
3. Use `Annotated[type, Field(description=...)]` for parameters.
4. Add test in `tests/test_client.py` (mock `requests.Session.get`).

## Tests

```bash
pytest tests/ -v          # All tests (mocked, no SonarQube needed)
```

- All tests mock HTTP calls — no real SonarQube instance required.
- 12 tests covering all client methods.
