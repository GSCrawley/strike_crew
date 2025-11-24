import unittest
from unittest.mock import Mock

from strike_crew.threat_feed import ThreatArticle, ThreatFeedService, ThreatSource


SAMPLE_FEED = """
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Threats</title>
    <item>
      <title>Critical RCE found in example service</title>
      <link>https://example.com/rce</link>
      <pubDate>Wed, 07 Aug 2024 12:00:00 GMT</pubDate>
      <description>Proof-of-concept exploit was published.</description>
      <category>vulnerability</category>
    </item>
    <item>
      <title>Ransomware group expands targeting</title>
      <link>https://example.com/ransomware</link>
      <pubDate>Tue, 06 Aug 2024 09:00:00 GMT</pubDate>
      <description>New affiliates identified.</description>
      <category>threat-actor</category>
    </item>
  </channel>
</rss>
"""


def build_service():
    session = Mock()
    response = Mock()
    response.read.return_value = SAMPLE_FEED.encode()
    response.__enter__ = lambda s: response
    response.__exit__ = lambda *args: False
    session.open.return_value = response
    source = ThreatSource("UnitTest", "https://example.com/feed", "news")
    return ThreatFeedService(sources=[source], session=session)


class ThreatFeedTests(unittest.TestCase):
    def test_fetch_recent_parses_feed(self):
        service = build_service()
        articles = service.fetch_recent(days=800)
        self.assertEqual(len(articles), 2)
        self.assertTrue(all(isinstance(article, ThreatArticle) for article in articles))
        titles = {article.title for article in articles}
        self.assertIn("Critical RCE found in example service", titles)
        self.assertIn("Ransomware group expands targeting", titles)

    def test_summarize_reports_top_source(self):
        service = build_service()
        articles = service.fetch_recent(days=800)
        summary = service.summarize(articles)
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["top_sources"][0][0], "UnitTest")
        self.assertEqual(summary["latest"]["title"], "Critical RCE found in example service")
