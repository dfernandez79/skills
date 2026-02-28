from html.parser import HTMLParser

from ._common import fetch_url


class _HNPageParser(HTMLParser):
    """Parse Hacker News front page HTML."""

    def __init__(self):
        super().__init__()
        self.stories = []  # List of {id, url, title}
        self.metadata = {}  # Map of id -> {points, comments}
        self.current_story_id = None
        self.in_titleline = False
        self.in_score = False
        self.in_comments = False
        self.current_url = None
        self.current_title = None
        self.last_story_id = None  # Track the last story ID for metadata

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "tr" and "athing" in attrs_dict.get("class", ""):
            self.current_story_id = attrs_dict.get("id")
            self.last_story_id = self.current_story_id
            self.current_url = None
            self.current_title = None
            self.in_titleline = False
        elif tag == "a" and self.in_titleline and self.current_url is None:
            self.current_url = attrs_dict.get("href", "")
        elif tag == "span" and "titleline" in attrs_dict.get("class", ""):
            self.in_titleline = True
        elif tag == "span" and attrs_dict.get("class") == "score":
            self.in_score = True
        elif tag == "a" and "item?id=" in attrs_dict.get("href", ""):
            self.in_comments = True

    def handle_endtag(self, tag):
        if tag == "span" and self.in_titleline:
            self.in_titleline = False
        elif tag == "span" and self.in_score:
            self.in_score = False
        elif tag == "a" and self.in_comments:
            self.in_comments = False

    def handle_data(self, data):
        if self.in_titleline and not self.current_title:
            self.current_title = data.strip()
            if self.current_story_id and self.current_url and self.current_title:
                self.stories.append(
                    {
                        "id": self.current_story_id,
                        "url": self.current_url,
                        "title": self.current_title,
                    }
                )
                self.current_story_id = None
                self.current_url = None
                self.current_title = None
        elif self.in_score:
            parts = data.strip().split()
            if parts and parts[0].isdigit():
                story_id = self.last_story_id
                if story_id:
                    if story_id not in self.metadata:
                        self.metadata[story_id] = {}
                    self.metadata[story_id]["points"] = int(parts[0])
        elif self.in_comments:
            parts = data.strip().split()
            if parts and parts[0].isdigit():
                story_id = self.last_story_id
                if story_id:
                    if story_id not in self.metadata:
                        self.metadata[story_id] = {}
                    self.metadata[story_id]["comments"] = int(parts[0])


class HackerNewsSource:
    """Fetch news from the Hacker News front page."""

    def __init__(self):
        self.name = "Hacker News"
        self.url = "https://news.ycombinator.com/"

    def fetch(self, max_results):
        html = fetch_url(self.url).decode("utf-8")

        parser = _HNPageParser()
        parser.feed(html)

        results = []
        for story in parser.stories[:max_results]:
            story_id = story["id"]
            url = story["url"]
            title = story["title"]

            # Make relative URLs absolute
            if url.startswith("item?id="):
                url = f"https://news.ycombinator.com/{url}"

            hn_url = f"https://news.ycombinator.com/item?id={story_id}"
            meta = parser.metadata.get(story_id, {"points": 0, "comments": 0})

            results.append(
                {
                    "title": title,
                    "url": url,
                    "discussion": hn_url,
                    "date": "",
                    "points": meta.get("points", 0),
                    "comments": meta.get("comments", 0),
                }
            )

        return results
