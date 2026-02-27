---
name: latest-tech-news
description: Fetches and summarizes the latest tech news from Hacker News, Simon Willison's blog, MacRumors, and Lobsters. Use when users ask about recent tech news, trends, or want updates on specific topics like AI, programming languages, Apple products, open source, etc.
---

# Latest Tech News

Fetch and summarize the latest technology news from curated sources, filtered by topic.

## Sources

| Source | Coverage |
|---|---|
| [Hacker News](https://news.ycombinator.com/) | Startups, programming, tech industry |
| [Simon Willison's Blog](https://simonwillison.net/) | AI/LLMs, Python, web development, open source |
| [MacRumors](https://www.macrumors.com/) | Apple hardware, software, and ecosystem |
| [Lobsters](https://lobste.rs/) | Programming, systems, devops, security |

## How to Fetch News

Run the bundled Python script to retrieve news filtered by topic. The script uses RSS/Atom feeds and the Hacker News Algolia API to fetch results efficiently. It requires only Python 3 standard library — no external dependencies.

```bash
python3 <skill_path>/scripts/fetch_news.py "<topic>" [max_results_per_source]
```

- `<topic>` (required): The search query, e.g. "AI agents", "Rust", "Apple Vision Pro"
- `max_results_per_source` (optional): Number of results per source (default: 8)

Replace `<skill_path>` with the actual path to this skill's directory.

### Examples

```bash
# Broad topic
python3 <skill_path>/scripts/fetch_news.py "AI" 5

# Specific topic
python3 <skill_path>/scripts/fetch_news.py "Rust programming" 5

# Product news
python3 <skill_path>/scripts/fetch_news.py "Apple Vision Pro"
```

## How to Present Results

After running the script, present the results following these guidelines:

1. **Lead with a brief summary** of what was found (e.g., "Here are the latest news items about AI agents from across 4 tech sources").

2. **Group by source** and highlight the most interesting or relevant items. Not every result needs to be shown — curate for quality and relevance.

3. **For each notable item**, include:
   - The title (as a link if a URL is available)
   - A one-sentence summary of why it's relevant to the user's query
   - The date if it helps establish recency

4. **End with a brief synthesis** if there are cross-cutting themes (e.g., "A common thread across these stories is the rapid adoption of coding agents in professional development workflows").

5. If a source returned no results, briefly note it rather than omitting it silently.

## Notes

- Hacker News results come from the Algolia search API, so they support full-text search across all stories. Results are sorted by date (most recent first).
- Simon Willison's blog, MacRumors, and Lobsters results are filtered locally from their RSS/Atom feeds, matching all query words in titles and descriptions. This means only items currently in the feed (typically the most recent ~30 items) are searchable.
- If a topic is very niche and returns few results, suggest the user try broader or alternative terms.
