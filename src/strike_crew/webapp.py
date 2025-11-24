from __future__ import annotations

import json
import os
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

from strike_crew.threat_feed import ThreatFeedService


TEMPLATE_PATH = Path(__file__).parent / "templates" / "index.html"


class ThreatDashboard:
    def __init__(self, feed_service: Optional[ThreatFeedService] = None):
        self.feed_service = feed_service or ThreatFeedService()
        self.template = TEMPLATE_PATH.read_text()

    def render_homepage(self) -> bytes:
        rendered = self.template.replace("{{ generated }}", datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
        return rendered.encode("utf-8")

    def api_feed(self, days: int = 14, limit: int = 30) -> dict:
        articles = self.feed_service.fetch_recent(days=days, limit=limit)
        return {"articles": [article.to_dict() for article in articles], "summary": self.feed_service.summarize(articles)}

    def api_sources(self) -> dict:
        return [source.__dict__ for source in self.feed_service.sources]

    def serve(self, host: str = "0.0.0.0", port: int = 8000):
        dashboard = self

        class Handler(BaseHTTPRequestHandler):
            def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK):
                body = json.dumps(payload).encode("utf-8")
                self.send_response(status.value)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _send_html(self, body: bytes):
                self.send_response(HTTPStatus.OK.value)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                parsed = urlparse(self.path)
                if parsed.path == "/api/feed":
                    params = parse_qs(parsed.query)
                    days = int(params.get("days", [14])[0])
                    limit = int(params.get("limit", [30])[0])
                    payload = dashboard.api_feed(days=days, limit=limit)
                    return self._send_json(payload)

                if parsed.path == "/api/sources":
                    return self._send_json(dashboard.api_sources())

                if parsed.path.startswith("/static/"):
                    return self._send_404()

                return self._send_html(dashboard.render_homepage())

            def log_message(self, format, *args):
                # Quiet the default console spam
                return

            def _send_404(self):
                self.send_response(HTTPStatus.NOT_FOUND.value)
                self.end_headers()

        server = HTTPServer((host, port), Handler)
        print(f"Threat dashboard running at http://{host}:{port}")
        server.serve_forever()


def create_app(feed_service: Optional[ThreatFeedService] = None) -> ThreatDashboard:
    return ThreatDashboard(feed_service=feed_service)


def main():
    port = int(os.getenv("PORT", "8000"))
    dashboard = create_app()
    dashboard.serve(port=port)


if __name__ == "__main__":
    main()
