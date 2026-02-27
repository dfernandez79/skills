#!/usr/bin/env python3
"""Fetch latest tech news from multiple sources, filtered by topic.

Usage:
    python3 fetch_news.py <topic> [max_results_per_source]

Examples:
    python3 fetch_news.py "AI agents"
    python3 fetch_news.py "Apple Vision Pro" 5
    python3 fetch_news.py "Rust programming" 10
"""

import re
import sys
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCES = {
    "Hacker News": {
        "type": "algolia",
        "search_url": "https://hn.algolia.com/api/v1/search_by_date",
    },
    "Simon Willison's Blog": {
        "type": "atom",
        "feed_url": "https://simonwillison.net/atom/everything/",
    },
    "MacRumors": {
        "type": "rss",
        "feed_url": "https://feeds.macrumors.com/MacRumors-All",
    },
    "Lobsters": {
        "type": "rss",
        "feed_url": "https://lobste.rs/rss",
    },
}

TIMEOUT = 15
USER_AGENT = "LatestTechNewsSkill/1.0"


def strip_html(text):
    """Remove HTML tags and decode common entities."""
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&apos;", "'")
    text = re.sub(r"&#x[0-9a-fA-F]+;", "", text)
    text = re.sub(r"&#\d+;", "", text)
    return text.strip()


def fetch_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def matches_query(text, query_terms):
    """Check if text matches query terms. All terms must appear."""
    text_lower = text.lower()
    return all(term in text_lower for term in query_terms)


# -- Source-specific fetchers --


def fetch_hn(query, max_results):
    """Fetch from Hacker News via Algolia search API (supports direct search)."""
    params = urllib.parse.urlencode(
        {"query": query, "tags": "story", "hitsPerPage": max_results}
    )
    url = f"{SOURCES['Hacker News']['search_url']}?{params}"
    data = json.loads(fetch_url(url))
    results = []
    for hit in data.get("hits", []):
        hn_url = f"https://news.ycombinator.com/item?id={hit['objectID']}"
        results.append(
            {
                "title": hit.get("title", ""),
                "url": hit.get("url") or hn_url,
                "discussion": hn_url,
                "date": hit.get("created_at", "")[:10],
                "points": hit.get("points", 0),
                "comments": hit.get("num_comments", 0),
            }
        )
    return results


def fetch_rss(feed_url, query_terms, max_results):
    """Fetch and filter an RSS 2.0 feed."""
    xml_bytes = fetch_url(feed_url)
    root = ET.fromstring(xml_bytes)
    results = []
    for item in root.iter("item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        description = strip_html(item.findtext("description", ""))
        pub_date = item.findtext("pubDate", "").strip()

        searchable = f"{title} {description}"
        if query_terms and not matches_query(searchable, query_terms):
            continue

        results.append(
            {
                "title": title,
                "url": link,
                "date": pub_date,
                "snippet": description[:300] if description else "",
            }
        )
        if len(results) >= max_results:
            break
    return results


def fetch_atom(feed_url, query_terms, max_results):
    """Fetch and filter an Atom feed."""
    xml_bytes = fetch_url(feed_url)
    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    results = []
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", "", ns).strip()
        link_el = entry.find("atom:link", ns)
        link = link_el.get("href", "") if link_el is not None else ""
        summary = strip_html(
            entry.findtext("atom:summary", "", ns)
            or entry.findtext("atom:content", "", ns)
            or ""
        )
        updated = entry.findtext("atom:updated", "", ns)

        searchable = f"{title} {summary}"
        if query_terms and not matches_query(searchable, query_terms):
            continue

        results.append(
            {
                "title": title,
                "url": link,
                "date": updated[:10] if updated else "",
                "snippet": summary[:300] if summary else "",
            }
        )
        if len(results) >= max_results:
            break
    return results


def fetch_source(name, query, query_terms, max_results):
    """Dispatch to the right fetcher for a given source."""
    try:
        config = SOURCES[name]
        if config["type"] == "algolia":
            items = fetch_hn(query, max_results)
        elif config["type"] == "atom":
            items = fetch_atom(config["feed_url"], query_terms, max_results)
        elif config["type"] == "rss":
            items = fetch_rss(config["feed_url"], query_terms, max_results)
        else:
            items = []
        return name, items, None
    except Exception as e:
        return name, [], str(e)


def format_results(all_results, query):
    """Format results as Markdown for the agent to present."""
    lines = [f"# Tech News: {query}", ""]
    total = 0
    for name in SOURCES:
        items, error = all_results.get(name, ([], None))
        lines.append(f"## {name}")
        lines.append("")
        if error:
            lines.append(f"*Error: {error}*")
            lines.append("")
            continue
        if not items:
            lines.append(f"*No results matching '{query}'*")
            lines.append("")
            continue
        for i, item in enumerate(items, 1):
            total += 1
            lines.append(f"{i}. **{item['title']}**")
            if item.get("url"):
                lines.append(f"   Link: {item['url']}")
            if item.get("discussion"):
                lines.append(f"   Discussion: {item['discussion']}")
            if item.get("date"):
                lines.append(f"   Date: {item['date']}")
            if item.get("points") is not None and "points" in item:
                lines.append(
                    f"   {item['points']} points, {item.get('comments', 0)} comments"
                )
            if item.get("snippet"):
                snippet = item["snippet"].replace("\n", " ")
                lines.append(f"   > {snippet}")
            lines.append("")
        lines.append("")

    lines.insert(2, f"*Found {total} results across {len(SOURCES)} sources.*")
    lines.insert(3, "")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_news.py <topic> [max_results_per_source]")
        print('Example: fetch_news.py "AI agents" 5')
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 8

    # Build query terms for local filtering (RSS/Atom feeds).
    # Keep meaningful words only (3+ chars). For HN, the Algolia API handles search.
    query_terms = [t.lower() for t in query.split() if len(t) >= 3]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(fetch_source, name, query, query_terms, max_results): name
            for name in SOURCES
        }
        results = {}
        for future in as_completed(futures):
            name, items, error = future.result()
            results[name] = (items, error)

    print(format_results(results, query))


if __name__ == "__main__":
    main()
