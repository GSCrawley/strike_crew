from unittest.mock import MagicMock

from strike_crew.threat_feed import ThreatArticle
from strike_crew.webapp import create_app


def test_api_feed_uses_service():
    mock_service = MagicMock()
    mock_article = ThreatArticle(
        title="Sample",
        link="https://example.com",
        published=None,
        summary="",
        source="Test",
        categories=["news"],
        risk_score=0.5,
    )
    mock_service.fetch_recent.return_value = [mock_article]
    mock_service.summarize.return_value = {"total": 1, "top_sources": [("Test", 1)], "latest": None}
    dashboard = create_app(feed_service=mock_service)

    payload = dashboard.api_feed()
    assert payload["summary"]["total"] == 1
    assert payload["articles"][0]["title"] == "Sample"
    mock_service.fetch_recent.assert_called_once()
