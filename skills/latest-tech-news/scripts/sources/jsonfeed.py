import json

from ._common import fetch_url, strip_html


class JSONFeedSource:
    """Fetch news from a JSON Feed (https://jsonfeed.org)."""

    def __init__(self, name, feed_url, include_snippet=True):
        self.name = name
        self.feed_url = feed_url
        self.include_snippet = include_snippet

    def fetch(self, max_results):
        json_bytes = fetch_url(self.feed_url)
        feed = json.loads(json_bytes)
        results = []

        items = feed.get("items", [])
        for item in items[:max_results]:
            title = item.get("title", "").strip()
            url = item.get("url", "").strip()

            # JSON Feed supports multiple date fields
            date = (
                item.get("date_published", "") or item.get("date_modified", "")
            ).strip()

            # Get content from various possible fields
            content = ""
            if "content_html" in item:
                content = strip_html(item["content_html"])
            elif "content_text" in item:
                content = item["content_text"]
            elif "summary" in item:
                content = strip_html(item["summary"])

            item_data = {
                "title": title,
                "url": url,
                "date": date[:10] if date else "",
            }

            if self.include_snippet and content:
                item_data["snippet"] = content[:300]

            results.append(item_data)

            if len(results) >= max_results:
                break

        return results
