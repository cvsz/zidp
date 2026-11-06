from __future__ import annotations

import importlib.util
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import threading
import unittest
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "test-idp-dev.py"
SPEC = importlib.util.spec_from_file_location("zidp_dev_smoke", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load the ZIDP development smoke-test module")
ZIDP_SMOKE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ZIDP_SMOKE)


class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = json.dumps({"status": "ok"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


class LocalRequestProxyTests(unittest.TestCase):
    def test_loopback_request_bypasses_environment_proxies(self) -> None:
        server = HTTPServer(("127.0.0.1", 0), _HealthHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            proxy = "http://127.0.0.1:1"
            with patch.dict(
                os.environ,
                {
                    "HTTP_PROXY": proxy,
                    "HTTPS_PROXY": proxy,
                    "ALL_PROXY": proxy,
                    "NO_PROXY": "",
                    "http_proxy": proxy,
                    "https_proxy": proxy,
                    "all_proxy": proxy,
                    "no_proxy": "",
                },
                clear=False,
            ):
                status, body, target = ZIDP_SMOKE.request(
                    f"http://127.0.0.1:{server.server_port}/health"
                )

            self.assertEqual(status, 200)
            self.assertEqual(json.loads(body), {"status": "ok"})
            self.assertTrue(target.startswith("http://127.0.0.1:"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
