import json
from datetime import datetime, timezone
from types import SimpleNamespace

import json
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

from strike_crew.csec_saas import CSecSaaSClient
from strike_crew.threat_feed import ThreatArticle, ThreatFeedService


class DummyResponse:
    def __init__(self, payload: bytes):
        self.payload = payload

    def read(self):
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class DummyOpener:
    def __init__(self, payload: bytes):
        self.payload = payload
        self.last_request = None

    def open(self, req, timeout=10):
        self.last_request = req
        return DummyResponse(self.payload)


class FakeCSecClient:
    def __init__(self):
        self.called = False

    def enabled(self):
        return True

    def fetch_articles(self, limit: int, days: int):
        self.called = True
        return [
            ThreatArticle(
                title="CSec Finding",
                link="https://csec.local/finding",
                summary="",
                published=datetime.now(timezone.utc),
                source="CSec_SaaS",
                categories=["alert"],
            )
        ]


class CSecIntegrationTests(unittest.TestCase):
    def test_csec_client_parses_feed_payload(self):
        payload = json.dumps(
            [
                {
                    "title": "CSec Alert",
                    "url": "https://csec.local/alert",
                    "summary": "New critical finding",
                    "published": "2024-08-01T12:00:00Z",
                    "category": "alert",
                }
            ]
        ).encode()
        opener = DummyOpener(payload)
        client = CSecSaaSClient(base_url="https://csec.local", opener=opener)

        articles = client.fetch_articles(limit=5, days=7)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "CSec Alert")
        self.assertEqual(articles[0].source, "CSec_SaaS")
        self.assertEqual(articles[0].categories, ["alert"])
        self.assertEqual(articles[0].link, "https://csec.local/alert")

    def test_feed_service_merges_csec_client(self):
        fake_client = FakeCSecClient()
        service = ThreatFeedService(
            sources=[],
            session=SimpleNamespace(open=lambda *args, **kwargs: None),
            csec_client=fake_client,
        )

        articles = service.fetch_recent(days=1, limit=5)

        self.assertTrue(fake_client.called)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].source, "CSec_SaaS")
