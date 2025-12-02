from __future__ import annotations

import datetime as dt
import logging
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from email.utils import parsedate_to_datetime
from urllib import request
from xml.etree import ElementTree as ET


@dataclass
class ThreatSource:
    name: str
    url: str
    category: str = "general"
    region: Optional[str] = None


@dataclass
class ThreatArticle:
    title: str
    link: str
    published: Optional[dt.datetime]
    summary: str
    source: str
    categories: List[str] = field(default_factory=list)
    risk_score: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "link": self.link,
            "published": self.published.isoformat() if self.published else None,
            "summary": self.summary,
            "source": self.source,
            "categories": self.categories,
            "risk_score": round(self.risk_score, 2),
        }


DEFAULT_SOURCES: List[ThreatSource] = [
    ThreatSource("CISA Known Exploited", "https://www.cisa.gov/cybersecurity-advisories/known-exploited-vulnerabilities-catalog.atom", "vulnerabilities", "US"),
    ThreatSource("Krebs on Security", "https://krebsonsecurity.com/feed/", "analysis"),
    ThreatSource("BleepingComputer", "https://www.bleepingcomputer.com/feed/", "news"),
    ThreatSource("Dark Reading", "https://www.darkreading.com/rss.xml", "news"),
    ThreatSource("CISA Alerts", "https://www.cisa.gov/uscert/ncas/alerts.xml", "alerts", "US"),
]


class ThreatFeedService:
    def __init__(self, sources: Optional[List[ThreatSource]] = None, session: Optional[request.OpenerDirector] = None):
        self.sources = sources or DEFAULT_SOURCES
        self.session = session or request.build_opener()
        self.logger = logging.getLogger(__name__)

    def fetch_recent(self, days: int = 14, limit: int = 40) -> List[ThreatArticle]:
        cutoff = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc) - dt.timedelta(days=days)
        articles: List[ThreatArticle] = []

        for source in self.sources:
            try:
                articles.extend(self._fetch_source(source, cutoff))
            except Exception as exc:
                self.logger.warning("Failed to pull feed from %s: %s", source.name, exc)

        articles = [article for article in articles if not cutoff or (article.published or cutoff) >= cutoff]
        for article in articles:
            article.risk_score = self._score_article(article, cutoff)

        articles.sort(key=lambda a: (a.risk_score, a.published or dt.datetime.min), reverse=True)
        return articles[:limit]

    def _fetch_source(self, source: ThreatSource, cutoff: dt.datetime) -> List[ThreatArticle]:
        with self.session.open(source.url, timeout=10) as response:
            payload = response.read()

        parsed = self._parse_feed(payload)
        articles: List[ThreatArticle] = []

        for entry in parsed:
            published = entry["published"]
            if published and published < cutoff:
                continue

            article = ThreatArticle(
                title=entry["title"],
                link=entry["link"],
                published=published,
                summary=entry["summary"],
                source=source.name,
                categories=entry["categories"] or [source.category],
            )
            articles.append(article)

        return articles

    @staticmethod
    def _parse_feed(payload: bytes) -> Iterable[Dict]:
        if isinstance(payload, (bytes, bytearray)):
            payload = payload.lstrip()
        root = ET.fromstring(payload)
        # RSS feeds use item, Atom uses entry
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        parsed_items: List[Dict] = []

        for item in items:
            title = item.findtext("title") or item.findtext("{http://www.w3.org/2005/Atom}title") or "Untitled"
            link = item.findtext("link") or ""
            if not link:
                link_node = item.find("{http://www.w3.org/2005/Atom}link")
                if link_node is not None:
                    link = link_node.attrib.get("href", "")

            summary = item.findtext("description") or item.findtext("summary") or ""
            published_raw = item.findtext("pubDate") or item.findtext("updated") or item.findtext("{http://www.w3.org/2005/Atom}updated")
            published = ThreatFeedService._parse_date(published_raw)
            categories = [c.text for c in item.findall("category") if c.text] or []

            parsed_items.append(
                {
                    "title": title.strip(),
                    "link": link.strip(),
                    "summary": summary.strip(),
                    "published": published,
                    "categories": categories,
                }
            )

        return parsed_items

    @staticmethod
    def _parse_date(value: Optional[str]) -> Optional[dt.datetime]:
        if not value:
            return None
        try:
            dt_value = parsedate_to_datetime(value)
            if not dt_value.tzinfo:
                dt_value = dt_value.replace(tzinfo=dt.timezone.utc)
            return dt_value
        except Exception:
            return None

    @staticmethod
    def _score_article(article: ThreatArticle, cutoff: dt.datetime) -> float:
        recency_weight = 0.65
        category_weight = 0.25
        source_weight = 0.1

        now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
        if article.published:
            recency_days = max((now - article.published).days, 0)
            recency_score = max(0, 1 - recency_days / max(1, (now - cutoff).days))
        else:
            recency_score = 0.3

        severity_keywords = ["cve", "rce", "zero-day", "exploit", "critical", "ransomware"]
        severity_score = 0.2 if any(k.lower() in article.title.lower() for k in severity_keywords) else 0

        source_score = 0.5 if article.source in {"CISA Known Exploited", "CISA Alerts"} else 0.35

        return recency_score * recency_weight + severity_score * category_weight + source_score * source_weight

    @staticmethod
    def summarize(articles: List[ThreatArticle]) -> Dict:
        if not articles:
            return {"total": 0, "top_sources": [], "latest": None}

        top_sources: Dict[str, int] = {}
        for article in articles:
            top_sources[article.source] = top_sources.get(article.source, 0) + 1

        latest = max((a for a in articles if a.published), key=lambda a: a.published, default=None)

        return {
            "total": len(articles),
            "top_sources": sorted(top_sources.items(), key=lambda x: x[1], reverse=True)[:3],
            "latest": latest.to_dict() if latest else None,
        }
