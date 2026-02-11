#!/usr/bin/env python3
"""Comprehensive system test for Strike Crew enhancements."""

import sys
import time
from src.strike_crew.threat_feed import ThreatFeedService
from src.strike_crew.config import OllamaLLMConfig
from src.strike_crew.llm import CustomOllamaLLM

def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_ollama():
    """Test Ollama LLM integration."""
    print_section("TEST 1: Ollama LLM Integration")

    try:
        config = OllamaLLMConfig(
            temperature=0.7,
            model_name="llama3.2:latest"
        )
        llm = CustomOllamaLLM(config)

        print("✓ Ollama LLM initialized successfully")
        print(f"  Model: {config.model_name}")
        print(f"  Base URL: {config.base_url}")

        # Test a simple query
        print("\nTesting LLM response...")
        response = llm.invoke("What is ransomware? Answer in one sentence.")
        print(f"✓ LLM Response: {response.content[:100]}...")

        return True
    except Exception as e:
        print(f"✗ Ollama test failed: {e}")
        return False

def test_feed_sources():
    """Test threat feed sources."""
    print_section("TEST 2: Threat Feed Sources")

    try:
        service = ThreatFeedService()

        print(f"✓ Total sources configured: {len(service.sources)}")

        # Group by category
        categories = {}
        for source in service.sources:
            cat = source.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(source.name)

        print(f"\n✓ Sources by category:")
        for cat, sources in sorted(categories.items()):
            print(f"  {cat.upper()}: {len(sources)} sources")
            for s in sources[:3]:  # Show first 3
                print(f"    - {s}")
            if len(sources) > 3:
                print(f"    ... and {len(sources) - 3} more")

        return True
    except Exception as e:
        print(f"✗ Feed sources test failed: {e}")
        return False

def test_feed_fetching():
    """Test actual feed fetching."""
    print_section("TEST 3: Feed Fetching & Caching")

    try:
        service = ThreatFeedService()

        # First fetch (should hit all sources)
        print("Fetching articles (first request - no cache)...")
        start = time.time()
        articles = service.fetch_recent(days=7, limit=15)
        first_fetch_time = time.time() - start

        print(f"✓ Fetched {len(articles)} articles in {first_fetch_time:.2f}s")

        if articles:
            print(f"\n✓ Sample articles:")
            for i, article in enumerate(articles[:5], 1):
                print(f"  {i}. [{article.source}] {article.title[:60]}...")
                print(f"     Risk Score: {article.risk_score} | Categories: {', '.join(article.categories[:2])}")

        # Second fetch (should use cache)
        print(f"\nFetching again (should use cache)...")
        start = time.time()
        cached_articles = service.fetch_recent(days=7, limit=15)
        cached_fetch_time = time.time() - start

        print(f"✓ Fetched {len(cached_articles)} articles in {cached_fetch_time:.2f}s")

        if cached_fetch_time < first_fetch_time * 0.5:
            print(f"✓ Caching working! ({first_fetch_time:.2f}s → {cached_fetch_time:.2f}s)")

        # Check source diversity
        sources_found = set(a.source for a in articles)
        print(f"\n✓ Articles from {len(sources_found)} different sources:")
        for source in sorted(sources_found)[:10]:
            count = sum(1 for a in articles if a.source == source)
            print(f"  - {source}: {count} articles")

        return True
    except Exception as e:
        print(f"✗ Feed fetching test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_webapp_api():
    """Test webapp API endpoints."""
    print_section("TEST 4: Webapp API Endpoints")

    try:
        import requests

        # Test /api/sources
        print("Testing /api/sources...")
        resp = requests.get("http://localhost:8000/api/sources", timeout=5)
        sources = resp.json()
        print(f"✓ /api/sources: {len(sources)} sources returned")

        # Test /api/feed
        print("\nTesting /api/feed...")
        resp = requests.get("http://localhost:8000/api/feed?days=7&limit=10", timeout=10)
        data = resp.json()
        print(f"✓ /api/feed: {data['summary']['total']} articles returned")

        if data['summary']['top_sources']:
            print(f"\n✓ Top sources:")
            for source, count in data['summary']['top_sources']:
                print(f"  - {source}: {count} articles")

        return True
    except Exception as e:
        print(f"✗ Webapp API test failed: {e}")
        print("  Make sure the webapp is running on port 8000")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  STRIKE CREW SYSTEM TEST")
    print("  Phase 0 & 1 Verification")
    print("="*60)

    results = {
        "Ollama LLM": test_ollama(),
        "Feed Sources": test_feed_sources(),
        "Feed Fetching": test_feed_fetching(),
        "Webapp API": test_webapp_api(),
    }

    print_section("TEST SUMMARY")

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\n{'='*60}")
    print(f"  OVERALL: {passed}/{total} tests passed")
    print(f"{'='*60}\n")

    if passed == total:
        print("🎉 All systems operational!")
        print("\nReady for Phase 2: Deep Content Extraction")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
