---
name: latest-tech-news
description: Fetches and summarizes the latest tech news from Hacker News, Simon Willison's blog, MacRumors, and Lobsters. Use when users ask about recent tech news, trends, or want updates on specific topics like AI, programming languages, Apple products, open source, etc.
---

# Latest Tech News

Fetch and summarize the latest technology news from curated sources, filtered by topic.

## Sources

| Source                                              | Coverage                                      |
| --------------------------------------------------- | --------------------------------------------- |
| [Hacker News](https://news.ycombinator.com/)        | Startups, programming, tech industry          |
| [Simon Willison's Blog](https://simonwillison.net/) | AI/LLMs, Python, web development, open source |
| [MacRumors](https://www.macrumors.com/)             | Apple hardware, software, and ecosystem       |
| [Lobsters](https://lobste.rs/)                      | Programming, systems, devops, security        |

## How to Fetch News

Run the bundled Python script to retrieve the latest news. It requires only Python 3 standard library — no external dependencies.

```bash
python3 <skill_path>/scripts/fetch_news.py [max_results_per_source]
```

- `max_results_per_source` (optional): Number of results per source (default: 8)

Replace `<skill_path>` with the actual path to this skill's directory.

### Examples

```bash
# Broad topic
python3 <skill_path>/scripts/fetch_news.py 5
```

## How to Filter the Results

The script will return the latest news items from each source. Returning the title and URL for each item. You can filter these results based on relevance to the user's query. For example, if the user is interested in "AI agents," look for items that mention AI, machine learning, or related terms in the title or summary.

Hacker News and Lobsters only report the title and URL, so you may need to infer relevance from the title and if that isn't enough from the actual content of the linked article.

Simon Willison's blog and MacRumors often include a summary or description that can help determine relevance.

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
