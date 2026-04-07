# Wiki Schema

## Article Template

Every article follows this format:

```markdown
# [Concept Name]

> [1-2 sentence concept statement. What this IS, not what this article covers.]

**Confidence:** HIGH | MEDIUM | LOW
**Last compiled:** [date]
**Sources:** [N] raw files, [N] memory files

---

## Core Findings

[Compiled knowledge organized by sub-topic, not by source.
Each claim tagged inline: [TESTED], [VERIFIED], [THEORETICAL]]

### [Sub-topic 1]
...

---

## Operational Rules

[Actionable decision rules for consuming agents.
Format: "When [situation], do [action], because [finding]."]

---

## Deep Reference

[Context-triggered pointers to calibration data, lookup tables, and tool-specific constraints in source files.
The wiki is concise — these pointers make dropped detail discoverable.
Format: "**When** [situation] → **read** `[source §section]` **for** [what you'll find]"]

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/filename.md` | [1-line what this source adds] |

---

## Related Concepts

- [[concept-name]] — [relationship type]: [why this connection matters]

Relationship types: DEPENDS_ON (this article's claims rely on that concept), INFORMS (this article's findings change decisions in that concept), CONTRASTS (opposite approach or competing axis), EXTENDS (builds on that concept with additional specificity)

**Bidirectional rule:** Every link A→B must have a corresponding B→A. If you add [[foo]] to article bar, add [[bar]] to article foo. The relationship type may differ in each direction (A DEPENDS_ON B, B INFORMS A). Hook-enforced.

---

## Open Questions

- [Unresolved contradictions, untested hypotheses, known gaps]
```

## Conventions

- **One article per concept** — multiple sources merge into one article
- **Cross-references** use `[[article-filename]]` (without path or extension)
- **Confidence tags**: HIGH = tested in A/B or verified against multiple sources, MEDIUM = single credible source or research-derived, LOW = theoretical or single-claim
- **Claim tags**: [TESTED] = confirmed via A/B test or direct experiment, [VERIFIED] = corroborated across 2+ independent sources, [THEORETICAL] = derived from principles but not empirically tested in our system
- **Source paths** are relative to `/root/wiki/research-data/` for research files, `/root/.claude/projects/-root/memory/` for memory files

## Ingest Workflow

When new research arrives (new .md in research-data/, new A/B findings, new memory file):

1. **Classify** — Read the new file. Determine which existing wiki articles it touches (match concepts, not filenames). Determine if a NEW article is needed.
2. **Semantic extraction** (NOT mechanical summarization) — For each affected article:
   - **First: identify DECISIONS.** Ask: "What decisions does a practitioner make when using this knowledge?" The article should be organized around decision moments, not topic headings.
   - Add new source to Source Files table
   - Merge new findings into Core Findings via semantic extraction (integrate around decisions, don't append by source)
   - Update Operational Rules if findings change decisions
   - Update confidence tags if evidence strengthens or weakens
   - Add new cross-links if they emerge
   - Surface new Open Questions if contradictions appear
   - **Update Deep Reference pointers via semantic extraction** — For each decision the practitioner makes, ask: "What detail in the source would CHANGE this decision?" Add context-triggered pointers where the answer is yes. Format: `**When** [decision moment the practitioner is in] → **read** [source §section] **for** [what specifically changes their choice]`. The "When" trigger is a SITUATION, not a topic. The "for" describes what SHIFTS, not "more detail."
   - **Push raw research to GitHub** — Raw files are the permanent substrate. The wiki points back to them via Deep Reference. Never delete raw research after compilation.
2b. **Contradiction check** — If new findings contradict existing wiki content:
   - Do NOT silently overwrite
   - Add both versions to the article with [CONTRADICTION] tag
   - Flag in log.md with "Contradiction detected" marker
   - Surface to operator for resolution
   - Confidence tag drops to LOW on the contradicted claim until resolved
3. **Create** — If concept not yet represented, create new article using template. Add to `index.md`. Cross-reference from related articles.
4. **Log** — Append to `log.md`:
   ```
   ## [date] — Ingested: [source filename]
   - **New articles:** [list or "none"]
   - **Updated articles:** [list with 1-line change description]
   - **Confidence changes:** [list or "none"]
   ```
5. **Lint** — Run abbreviated lint on affected articles only.

## Lint Process

Run every 5 sessions or weekly. Output to `wiki/lint-report.md`.

### Checks

1. **Orphan detection** — Scan all `[[concept]]` references. Verify each resolves to an actual file. Flag broken links and articles with zero inbound references.
2. **Contradiction detection** — For concepts appearing in 2+ articles, compare claims. Flag conflicting operational rules (critical) and conflicting findings (informational).
3. **Staleness detection** — Compare each article's "Last compiled" date against source file modification dates. Flag articles with sources modified after compilation.
4. **Coverage gaps** — Compare source files against articles. Flag any source not referenced by any article.
5. **Confidence decay** — Flag articles where all findings are [LOW] or [THEORETICAL], or where evidence base is a single source.

### Output Format

```markdown
# Wiki Lint Report — [date]

## Critical (fix before next session)
## Warning (fix within 3 sessions)
## Info (awareness only)

## Health Summary
- Total articles: N
- Orphan articles: N
- Broken cross-links: N
- Stale articles: N
- Average sources per article: N
```
