"""Tests for SonarQube MCP server."""

import pytest
from unittest.mock import patch, MagicMock
from sonarqube_mcp.client import SonarQubeClient


@pytest.fixture
def client():
    return SonarQubeClient("http://sonar.test", "test-token", verify_ssl=False)


class TestClient:
    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_search_projects(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"components": [{"key": "proj1"}]})
        result = client.search_projects("proj")
        assert "components" in result
        mock_get.assert_called_once()

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_quality_gate_status(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"projectStatus": {"status": "OK"}})
        result = client.get_quality_gate_status("my-project")
        assert result["projectStatus"]["status"] == "OK"

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_get_measures(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"component": {"measures": []}})
        result = client.get_measures("proj", "bugs,coverage")
        assert "component" in result

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_search_issues(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"issues": [], "total": 0})
        result = client.search_issues("proj", severities="CRITICAL")
        assert "issues" in result

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_search_hotspots(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"hotspots": []})
        result = client.search_hotspots("proj")
        assert "hotspots" in result

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_show_rule(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"rule": {"key": "java:S1234"}})
        result = client.show_rule("java:S1234")
        assert result["rule"]["key"] == "java:S1234"

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_list_quality_gates(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"qualitygates": []})
        result = client.list_quality_gates()
        assert "qualitygates" in result

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_search_metrics(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"metrics": []})
        result = client.search_metrics()
        assert "metrics" in result

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_list_pull_requests(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"pullRequests": []})
        result = client.list_pull_requests("proj")
        assert "pullRequests" in result

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_get_component_tree(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"components": []})
        result = client.get_component_tree("proj", "coverage")
        assert "components" in result

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_get_duplications(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"duplications": []})
        result = client.get_duplications("proj:src/File.java")
        assert "duplications" in result

    @patch("sonarqube_mcp.client.requests.Session.get")
    def test_auth_header(self, mock_get, client):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {})
        client.search_projects()
        assert client.session.auth == ("test-token", "")
