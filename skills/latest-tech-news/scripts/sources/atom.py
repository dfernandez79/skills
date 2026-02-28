import xml.etree.ElementTree as ET

from ._common import fetch_url, strip_html


class AtomSource:
    """Fetch news from an Atom feed."""

    def __init__(self, name, feed_url):
        self.name = name
        self.feed_url = feed_url

    def fetch(self, max_results):
        xml_bytes = fetch_url(self.feed_url)
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
