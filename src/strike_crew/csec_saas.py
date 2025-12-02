"""Integration helpers for consuming CSec_SaaS data as threat feed articles."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib import error, parse, request

from strike_crew.threat_feed import ThreatArticle


@dataclass
class CSecRecord:
    title: str
    link: str
    summary: str
    published: Optional[datetime]
    categories: List[str]


class CSecSaaSClient:
    """Lightweight client for the CSec_SaaS feed endpoint.

    The base URL and optional API key can be provided directly or via the
    ``CSEC_SAAS_BASE_URL`` and ``CSEC_SAAS_API_KEY`` environment variables.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        feed_path: str = "/api/feed",
        opener: Optional[request.OpenerDirector] = None,
    ):
        self.base_url = base_url or os.getenv("CSEC_SAAS_BASE_URL")
        self.api_key = api_key or os.getenv("CSEC_SAAS_API_KEY")
        self.feed_path = feed_path
        self.opener = opener or request.build_opener()
        self.logger = logging.getLogger(__name__)

    def enabled(self) -> bool:
        return bool(self.base_url)

    def fetch_articles(self, limit: int = 50, days: int = 30) -> List[ThreatArticle]:
        if not self.base_url:
            return []

        feed_url = self._build_feed_url(limit=limit, days=days)
        req = request.Request(feed_url)
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")

        try:
            with self.opener.open(req, timeout=10) as resp:
                payload = resp.read()
        except (error.URLError, error.HTTPError, TimeoutError) as exc:
            self.logger.warning("CSec_SaaS feed unavailable: %s", exc)
            return []

        try:
            raw_items = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError:
            self.logger.warning("CSec_SaaS feed returned invalid JSON")
            return []

        return [self._record_to_article(self._parse_record(item)) for item in raw_items if item]

    def _build_feed_url(self, limit: int, days: int) -> str:
        base = self.base_url.rstrip("/")
        query = parse.urlencode({"limit": limit, "days": days})
        return f"{base}{self.feed_path}?{query}"

    def _parse_record(self, data: Dict[str, Any]) -> CSecRecord:
        title = str(data.get("title") or data.get("name") or "CSec Finding")
        link = str(data.get("link") or data.get("url") or "")
        summary = str(data.get("summary") or data.get("description") or "")
        published = self._parse_datetime(
            data.get("published")
            or data.get("published_at")
            or data.get("timestamp")
            or data.get("created_at")
        )

        categories: List[str] = []
        for key in ("category", "categories", "severity", "status"):
            value = data.get(key)
            if isinstance(value, str) and value:
                categories.append(value)
            elif isinstance(value, list):
                categories.extend(str(v) for v in value if v)

        return CSecRecord(
            title=title,
            link=link,
            summary=summary,
            published=published,
            categories=categories,
        )

    def _record_to_article(self, record: CSecRecord) -> ThreatArticle:
        return ThreatArticle(
            title=record.title,
            link=record.link,
            summary=record.summary,
            published=record.published,
            source="CSec_SaaS",
            categories=record.categories,
        )

    @staticmethod
    def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if not parsed.tzinfo:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except ValueError:
            return None
