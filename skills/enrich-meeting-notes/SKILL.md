---
name: enrich-meeting-notes
description: "Enriches meeting notes using a transcript. Invoke with /enrich-meeting-notes and attach two files: the original meeting notes and the meeting transcript. Produces improved, comprehensive meeting notes in Markdown."
user_invocable: true
command: enrich-meeting-notes
---

# Enrich Meeting Notes

Combine rough meeting notes with a full transcript to produce polished, comprehensive meeting notes in Markdown.

## Invocation

```
/enrich-meeting-notes
```

The user must attach two files:

1. **Meeting notes** — the original notes taken during the meeting (any text format)
2. **Transcript** — the full meeting transcript (any text format)

If only one attachment is provided, ask the user to attach the missing file. If no attachments are provided, ask for both.

## How to Identify the Attachments

- The **meeting notes** are typically shorter, structured with bullet points or headings, and may contain shorthand or incomplete sentences.
- The **transcript** is typically longer, conversational, and contains speaker labels or timestamps.
- If it is ambiguous which file is which, ask the user to clarify.

## Processing Steps

### 1. Analyze the Original Notes

Read the meeting notes and identify:

- The overall structure and sections the note-taker organized around
- Key topics, decisions, and action items already captured
- Gaps — topics mentioned briefly or missing detail

### 2. Analyze the Transcript

Read the transcript and extract:

- Discussion points not captured in the notes
- Context and reasoning behind decisions
- Specific commitments, owners, and deadlines mentioned verbally
- Corrections to anything inaccurately captured in the notes
- Key quotes that add clarity or emphasis

### 3. Generate Enriched Meeting Notes

Produce a single Markdown document that merges both sources.
Use the same language as the original notes and transcript. If the meeting is in Spanish write the enriched notes in Spanish, if in English write in English, etc.

Follow this structure:

```markdown
# Meeting: [Title or Topic]

**Date:** [date if available]
**Attendees:** [list if available from transcript or notes]

## Summary

[2-3 sentence high-level summary of what the meeting covered and its outcomes]

## Discussion

### [Topic 1]

[Detailed notes combining the original notes with transcript context.
Include relevant details, reasoning, and context from the discussion.]

### [Topic 2]

[...]

## Decisions

- [Decision 1 — with context on why it was made]
- [Decision 2]

## Action Items

- [ ] [Action item] — **Owner** (deadline if mentioned)
- [ ] [Action item] — **Owner**

## Open Questions

- [Any unresolved questions or topics deferred to a future meeting]

## Key Quotes

> "[Notable quote that captures an important point]" — Speaker

## Notes

[Any additional context, links mentioned, or reference material discussed]
```

## Guidelines

- **Preserve the original structure** when the notes are well-organized. Enhance rather than replace.
- **Add, don't remove.** If the original notes contain something not in the transcript, keep it — the note-taker may have captured something from chat or a side conversation.
- **Attribute action items** to specific people when the transcript makes ownership clear.
- **Use direct quotes sparingly** — only when a quote captures a decision rationale or important nuance better than a paraphrase.
- **Flag contradictions.** If the notes and transcript disagree on a detail, note both versions and flag it for the user to resolve.
- **Omit filler.** Do not include small talk, off-topic tangents, or repeated back-and-forth unless it led to a meaningful conclusion.
- **Keep section headings short and descriptive.** Use the topic name, not "Discussion Item 3."
- **Omit empty sections.** If there are no open questions or key quotes worth including, drop those sections rather than leaving them empty.

## Output

Output the enriched meeting notes directly as Markdown text. Do not wrap the output in a code block — produce it as formatted content the user can copy or save.
