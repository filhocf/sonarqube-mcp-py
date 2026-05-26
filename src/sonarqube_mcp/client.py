"""SonarQube REST API client."""

import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from typing import Any


class _LowSecurityAdapter(HTTPAdapter):
    """HTTPS adapter that lowers SECLEVEL for legacy internal certificates."""

    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_ciphers("DEFAULT:@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super().init_poolmanager(*args, **kwargs)


class SonarQubeClient:
    """Thin wrapper around SonarQube Web API."""

    def __init__(self, base_url: str, token: str, verify_ssl: bool = False):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (token, "")
        self.session.verify = verify_ssl
        if not verify_ssl:
            self.session.mount("https://", _LowSecurityAdapter())

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/api/{endpoint}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def search_projects(self, query: str | None = None, page_size: int = 50) -> dict:
        params = {"ps": page_size}
        if query:
            params["q"] = query
        try:
            return self._get("projects/search", params)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 403:
                # Fallback: components/search works without admin permission
                params["qualifiers"] = "TRK"
                result = self._get("components/search", params)
                return {"components": result.get("components", []),
                        "paging": result.get("paging", {})}
            raise

    def get_quality_gate_status(self, project_key: str, branch: str | None = None) -> dict:
        params = {"projectKey": project_key}
        if branch:
            params["branch"] = branch
        return self._get("qualitygates/project_status", params)

    def get_measures(self, component: str, metric_keys: str, branch: str | None = None) -> dict:
        params = {"component": component, "metricKeys": metric_keys}
        if branch:
            params["branch"] = branch
        return self._get("measures/component", params)

    def list_quality_gates(self) -> dict:
        return self._get("qualitygates/list")

    def search_issues(self, project_key: str, severities: str | None = None,
                      statuses: str = "OPEN", page_size: int = 50,
                      branch: str | None = None) -> dict:
        params = {"componentKeys": project_key, "statuses": statuses, "ps": page_size}
        if severities:
            params["severities"] = severities
        if branch:
            params["branch"] = branch
        return self._get("issues/search", params)

    def search_hotspots(self, project_key: str, status: str = "TO_REVIEW",
                        branch: str | None = None) -> dict:
        params = {"projectKey": project_key, "status": status}
        if branch:
            params["branch"] = branch
        return self._get("hotspots/search", params)

    def show_hotspot(self, hotspot_key: str) -> dict:
        return self._get("hotspots/show", {"hotspot": hotspot_key})

    def show_rule(self, rule_key: str) -> dict:
        return self._get("rules/show", {"key": rule_key})

    def search_metrics(self) -> dict:
        return self._get("metrics/search", {"ps": 500})

    def list_pull_requests(self, project_key: str) -> dict:
        return self._get("project_pull_requests/list", {"project": project_key})

    def get_component_tree(self, component: str, metric_keys: str,
                           qualifiers: str = "FIL", page_size: int = 100,
                           sort_field: str | None = None,
                           branch: str | None = None) -> dict:
        params = {"component": component, "metricKeys": metric_keys,
                  "qualifiers": qualifiers, "ps": page_size}
        if sort_field:
            params["s"] = sort_field
            params["metricSort"] = metric_keys.split(",")[0]
            params["metricSortFilter"] = "withMeasuresOnly"
        if branch:
            params["branch"] = branch
        return self._get("measures/component_tree", params)

    def get_duplications(self, file_key: str, branch: str | None = None) -> dict:
        params = {"key": file_key}
        if branch:
            params["branch"] = branch
        return self._get("duplications/show", params)
