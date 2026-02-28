#!/usr/bin/env python3
"""Fetch latest tech news from multiple sources.

Usage:
    python3 fetch_news.py [max_results_per_source]

Examples:
    python3 fetch_news.py
    python3 fetch_news.py 5
    python3 fetch_news.py 10
"""

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from sources import AtomSource, HackerNewsSource, RSSSource

SOURCES = [
    HackerNewsSource(),
    AtomSource("Simon Willison's Blog", "https://simonwillison.net/atom/everything/"),
    RSSSource("MacRumors", "https://feeds.macrumors.com/MacRumors-All"),
    RSSSource("Lobsters", "https://lobste.rs/rss", include_snippet=False),
]


def fetch_source(source, max_results):
    """Fetch items from a source, returning (name, items, error)."""
    try:
        items = source.fetch(max_results)
        return source.name, items, None
    except Exception as e:
        return source.name, [], str(e)


def format_results(all_results):
    """Format results as Markdown for the agent to present."""
    lines = ["# Latest Tech News", ""]
    total = 0
    for source in SOURCES:
        items, error = all_results.get(source.name, ([], None))
        lines.append(f"## {source.name}")
        lines.append("")
        if error:
            lines.append(f"*Error: {error}*")
            lines.append("")
            continue
        if not items:
            lines.append("*No results found*")
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
    max_results = int(sys.argv[1]) if len(sys.argv) > 1 else 8

    with ThreadPoolExecutor(max_workers=len(SOURCES)) as executor:
        futures = {
            executor.submit(fetch_source, source, max_results): source
            for source in SOURCES
        }
        results = {}
        for future in as_completed(futures):
            name, items, error = future.result()
            results[name] = (items, error)

    print(format_results(results))


if __name__ == "__main__":
    main()
