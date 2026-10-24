# -*- coding: utf-8 -*-
"""
Module kết nối CSDL đồ thị Dgraph (Dgraph Client)
Giao tiếp trực tiếp với Dgraph Alpha qua HTTP API (/query, /mutate, /alter, /admin, /health).
Đáp ứng Mục 8 trong thang điểm: Kết nối CSDL với phần mềm ứng dụng.
"""

import json
import os
import urllib.request
import urllib.error


def load_env_file(env_path=None):
    if env_path is None:
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


load_env_file()


class DgraphClient:
    def __init__(self, alpha_url=None, zero_url=None):
        self.alpha_url = (alpha_url or os.environ.get("DGRAPH_ALPHA_URL", "http://localhost:8080")).rstrip("/")
        self.zero_url = (zero_url or os.environ.get("DGRAPH_ZERO_URL", "http://localhost:6080")).rstrip("/")

    def _request(self, base_url, path, data_bytes=None, content_type="application/json", method="GET"):
        url = f"{base_url}{path}"
        headers = {}
        if content_type:
            headers["Content-Type"] = content_type
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8")
            try:
                return json.loads(raw)
            except Exception:
                return {"raw": raw}

    def check_health(self):
        try:
            health = self._request(self.alpha_url, "/health", method="GET")
            return {"connected": True, "alpha_url": self.alpha_url, "health": health}
        except Exception as e:
            return {"connected": False, "alpha_url": self.alpha_url, "error": str(e)}

    def query_dql(self, dql_string, variables=None):
        """Thực thi câu lệnh truy vấn DQL trên Dgraph Alpha (/query)."""
        if variables:
            payload = json.dumps({"query": dql_string, "variables": variables}).encode("utf-8")
            return self._request(self.alpha_url, "/query", payload, "application/json", "POST")
        return self._request(self.alpha_url, "/query", dql_string.encode("utf-8"), "application/dql", "POST")

    def mutate_json(self, set_obj=None, delete_obj=None):
        """Thực thi thêm/sửa/xóa đỉnh và cạnh bằng JSON Mutation (/mutate?commitNow=true)."""
        body = {}
        if set_obj is not None:
            body["set"] = set_obj
        if delete_obj is not None:
            body["delete"] = delete_obj
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        return self._request(self.alpha_url, "/mutate?commitNow=true", payload, "application/json", "POST")

    def mutate_rdf(self, set_nquads="", delete_nquads=""):
        """Thực thi thêm/xóa cạnh hoặc thuộc tính kèm Facets bằng RDF N-Quads."""
        parts = ["{"]
        if set_nquads.strip():
            parts.append("  set {\n" + set_nquads.strip() + "\n  }")
        if delete_nquads.strip():
            parts.append("  delete {\n" + delete_nquads.strip() + "\n  }")
        parts.append("}")
        rdf_body = "\n".join(parts).encode("utf-8")
        return self._request(self.alpha_url, "/mutate?commitNow=true", rdf_body, "application/rdf", "POST")

    def export_database(self, fmt="rdf"):
        """Gọi GraphQL /admin endpoint của Dgraph Alpha để Export dữ liệu ra RDF hoặc JSON."""
        gql = {
            "query": f'mutation {{ export(input: {{ format: "{fmt}" }}) {{ response {{ code message }} exportedFiles }} }}'
        }
        return self._request(self.alpha_url, "/admin", json.dumps(gql).encode("utf-8"), "application/json", "POST")

