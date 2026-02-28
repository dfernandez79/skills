import xml.etree.ElementTree as ET

from ._common import fetch_url, strip_html


class RSSSource:
    """Fetch news from an RSS 2.0 feed."""

    def __init__(self, name, feed_url, include_snippet=True):
        self.name = name
        self.feed_url = feed_url
        self.include_snippet = include_snippet

    def fetch(self, max_results):
        xml_bytes = fetch_url(self.feed_url)
        root = ET.fromstring(xml_bytes)
        results = []
        for item in root.iter("item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            description = strip_html(item.findtext("description", ""))
            pub_date = item.findtext("pubDate", "").strip()

            item_data = {
                "title": title,
                "url": link,
                "date": pub_date,
            }
            if self.include_snippet and description:
                item_data["snippet"] = description[:300]
            results.append(item_data)
            if len(results) >= max_results:
                break
        return results
