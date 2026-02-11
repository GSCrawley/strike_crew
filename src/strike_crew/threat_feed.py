from __future__ import annotations

import datetime as dt
import gzip
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional
from urllib.error import HTTPError, URLError

from email.utils import parsedate_to_datetime
from urllib import request
from xml.etree import ElementTree as ET
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


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
    # === EXISTING (Fixed) ===
    ThreatSource("CISA Known Exploited", "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json", "vulnerabilities", "US"),
    ThreatSource("Krebs on Security", "https://krebsonsecurity.com/feed/", "analysis"),
    ThreatSource("BleepingComputer", "https://www.bleepingcomputer.com/feed/", "news"),
    ThreatSource("Dark Reading", "https://www.darkreading.com/rss.xml", "news"),
    ThreatSource("CISA Alerts", "https://www.cisa.gov/uscert/ncas/alerts.xml", "alerts", "US"),

    # === NEW: Government & Official ===
    ThreatSource("US-CERT Current Activity", "https://www.cisa.gov/uscert/ncas/current-activity.xml", "alerts", "US"),
    ThreatSource("NCSC UK Alerts", "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml", "alerts", "UK"),
    ThreatSource("CERT-EU", "https://cert.europa.eu/cert/newsletter/en/latest_Security_News_.xml", "alerts", "EU"),
    ThreatSource("Australian Cyber Security Centre", "https://www.cyber.gov.au/rss.xml", "alerts", "AU"),

    # === NEW: Vulnerability Databases ===
    ThreatSource("NVD Recent CVEs", "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml", "vulnerabilities"),
    ThreatSource("Exploit-DB", "https://www.exploit-db.com/rss.xml", "exploits"),
    ThreatSource("Packet Storm", "https://packetstormsecurity.com/feeds/news/", "exploits"),

    # === NEW: Malware & IOC Feeds ===
    ThreatSource("abuse.ch Malware", "https://urlhaus.abuse.ch/rss/", "malware"),
    ThreatSource("abuse.ch SSL Blacklist", "https://sslbl.abuse.ch/blacklist/sslblacklist.rss", "malware"),

    # === NEW: Threat Intelligence & Analysis ===
    ThreatSource("The Hacker News", "https://feeds.feedburner.com/TheHackersNews", "news"),
    ThreatSource("SecurityWeek", "https://www.securityweek.com/feed/", "news"),
    ThreatSource("Threatpost", "https://threatpost.com/feed/", "news"),
    ThreatSource("Talos Intelligence Blog", "https://blog.talosintelligence.com/rss/", "analysis"),
    ThreatSource("Schneier on Security", "https://www.schneier.com/blog/atom.xml", "analysis"),

    # === NEW: Vendor-Specific ===
    ThreatSource("Microsoft Security Blog", "https://www.microsoft.com/en-us/security/blog/feed/", "vendor"),
    ThreatSource("Google Security Blog", "https://security.googleblog.com/feeds/posts/default", "vendor"),
    ThreatSource("Cisco Talos", "https://blog.talosintelligence.com/rss/", "vendor"),
]


class ThreatFeedService:
    def __init__(self, sources: Optional[List[ThreatSource]] = None, session: Optional[request.OpenerDirector] = None):
        self.sources = sources or DEFAULT_SOURCES

        # Create custom opener with browser headers to avoid 403 errors
        if session is None:
            opener = request.build_opener()
            opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'),
                ('Accept', 'application/rss+xml, application/xml, text/xml, application/atom+xml, */*'),
                ('Accept-Language', 'en-US,en;q=0.9'),
                ('Accept-Encoding', 'gzip, deflate, br'),
                ('DNT', '1'),
                ('Connection', 'keep-alive'),
                ('Upgrade-Insecure-Requests', '1'),
            ]
            self.session = opener
        else:
            self.session = session

        self.logger = logging.getLogger(__name__)

        # Add caching
        self._cache = {}
        self._cache_ttl = 300  # 5 minutes

    def fetch_recent(self, days: int = 14, limit: int = 40) -> List[ThreatArticle]:
        # Check cache first
        cache_key = f"feed_{days}_{limit}"
        if cache_key in self._cache:
            cached_time, cached_data = self._cache[cache_key]
            if time.time() - cached_time < self._cache_ttl:
                self.logger.info("Returning cached feed data")
                return cached_data

        # Fetch fresh data
        articles = self._fetch_all_sources(days, limit)

        # Cache results
        self._cache[cache_key] = (time.time(), articles)
        return articles

    def _fetch_all_sources(self, days: int, limit: int) -> List[ThreatArticle]:
        """Actual fetching logic with retry support."""
        cutoff = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc) - dt.timedelta(days=days)
        articles: List[ThreatArticle] = []

        for source in self.sources:
            try:
                articles.extend(self._fetch_source_with_retry(source, cutoff))
            except Exception as exc:
                self.logger.warning("Failed to pull feed from %s after retries: %s", source.name, exc)

        articles = [article for article in articles if not cutoff or (article.published or cutoff) >= cutoff]
        for article in articles:
            article.risk_score = self._score_article(article, cutoff)

        articles.sort(key=lambda a: (a.risk_score, a.published or dt.datetime.min), reverse=True)
        return articles[:limit]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((HTTPError, URLError, ConnectionError))
    )
    def _fetch_source_with_retry(self, source: ThreatSource, cutoff: dt.datetime) -> List[ThreatArticle]:
        """Fetch with automatic retry on transient failures."""
        return self._fetch_source(source, cutoff)

    def _fetch_source(self, source: ThreatSource, cutoff: dt.datetime) -> List[ThreatArticle]:
        with self.session.open(source.url, timeout=10) as response:
            payload = response.read()
            content_type = response.headers.get('Content-Type', '')
            content_encoding = response.headers.get('Content-Encoding', '')

        # Handle gzip compression
        if content_encoding == 'gzip' or (payload and payload[:2] == b'\x1f\x8b'):
            try:
                payload = gzip.decompress(payload)
            except Exception as e:
                self.logger.warning(f"Failed to decompress gzip content from {source.name}: {e}")

        # Check if JSON or XML
        if 'json' in content_type or source.url.endswith('.json'):
            parsed = self._parse_json_feed(payload, source)
        else:
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
    def _parse_json_feed(payload: bytes, source: ThreatSource) -> Iterable[Dict]:
        """Parse JSON feeds (e.g., CISA KEV)."""
        import json
        data = json.loads(payload)

        parsed_items: List[Dict] = []

        # Handle CISA KEV format
        if source.name == "CISA Known Exploited" and "vulnerabilities" in data:
            for vuln in data.get("vulnerabilities", []):
                parsed_items.append({
                    "title": f"{vuln.get('cveID', 'Unknown')}: {vuln.get('vulnerabilityName', 'No title')}",
                    "link": f"https://nvd.nist.gov/vuln/detail/{vuln.get('cveID', '')}",
                    "summary": vuln.get("shortDescription", "No description"),
                    "published": ThreatFeedService._parse_date(vuln.get("dateAdded")),
                    "categories": ["vulnerability", "known-exploited"],
                })

        # Add support for other JSON feed formats here

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
