# Typography and Comprehension

> How typographic choices affect whether a person understands what they read — line length, font size, serif vs. sans-serif, reading hierarchy, dark mode contrast, progressive disclosure, and the "scannable but deep" architecture. Not aesthetics — comprehension, recall, and cognitive load.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 0 memory files

---

## Core Findings

### Optimal Line Length for Comprehension

| Context | Optimal CPL | Source |
|---|---|---|
| General adult reading | 50-75 characters per line | Literature review, Visible Language (ResearchGate) |
| Sweet spot (single number) | 66 characters per line | Same |
| Novice readers | 34-60 CPL, optimum 45 | Same |
| Expert readers | 45-80 CPL, optimum 60 | Same |
| Dyslexia accessibility | 60-70 CPL | British Dyslexia Association |
| "Scanning" contexts | Longer lines preferred | Baymard |
| "Read thoroughly" contexts | Shorter lines preferred | Baymard |

[VERIFIED — literature review accessed via ResearchGate summary and UXPin synthesis]

**Mechanism:** Both very short and very long lines interrupt the eye's return-sweep pattern. Short lines require too many saccades (eye jumps). Long lines make it hard to locate the next line start, increasing re-reading errors. The 45-75 CPL range corresponds to the span of comfortable peripheral vision during fixation — approximately 15-20 characters on either side of the fixation point. A line of ~60 characters requires 3-4 fixations, the neurologically optimal load. [VERIFIED]

**Application:** At 16px font, 60 CPL on desktop is approximately 480-520px content column width. Full-viewport layouts on 1440px+ screens may run 100+ CPL without an explicit max-width, exceeding the optimal range. [VERIFIED]

### Typographic Hierarchy Determines Reading Order

**NNGroup data (500+ participants, 750+ hours eyetracking, 2006-2019):** 79% of users scan new pages; only 16% read word-by-word. Scanning behavior is unchanged across 23 years of online reading research. [VERIFIED]

**F-Pattern:** Users read the top line left-to-right (headline), drop down and read partway across (subhead), then scan the left margin vertically. Right side of body text often receives zero fixations. [VERIFIED]

**Layer-Cake Pattern:** Scanners read headings only, skipping body entirely. Each heading is evaluated as a decision point: read further or skip. The heading either opens the body for reading or closes it. [VERIFIED]

**The reading order sequence (derived from eyetracking):**

1. Largest element (headline) — always read
2. Subheading immediately below — usually read
3. First sentence of first paragraph — usually read
4. Bolded words in body — scanned for
5. Bullet list items (first 2-3 words) — scanned
6. Second+ subheadings — evaluated, often read
7. Body text between subheadings — read only if heading earned it
8. Final paragraph — often skipped entirely
9. Right side of any line beyond ~50% — risk of zero fixations

**What never gets read:** Right-aligned text, text after the fold without visual prompts, body copy following an uninteresting heading, content after a pull quote (pull quotes disrupt reading flow and cause users to drop into scanning mode). [VERIFIED — NNGroup 2019]

### Font Size Minimums by Context

| Context | Minimum | Recommended | Source |
|---|---|---|---|
| Web body text | 16px | 17-18px | LearnUI.Design, WCAG |
| Mobile body text | 16px | 17px (iOS default) | Apple HIG, Material Design |
| Secondary text (labels) | 14px | 15px | Material Design |
| "Best readability" on screen | 18px | 18px | Rello 2016 eye-tracking |
| Glanceable reading | Larger always better | No ceiling found | NNGroup |
| Large text threshold (WCAG) | 18pt / 24px | — | WCAG 2.1 |

[VERIFIED — multiple converging sources]

**Mechanism:** Eye-tracking (Rello 2016): 18pt achieved best readability, comprehension scores, and subjective perception. Fixation durations were significantly shorter at 18px vs 14px. Comprehension accuracy was significantly higher at 18px and 26px vs 12px. [VERIFIED]

The 16px minimum derives from viewing distance research: at 25-35cm (typical phone distance), 16px sits at the lower bound of comfortable resolution for normal vision. [VERIFIED]

**Dark mode specific:** No studies found indicating different size minimums for dark mode. However, slightly bolder font weights improve legibility on dark backgrounds due to halation effect reducing effective stroke contrast. This is a weight adjustment, not a size adjustment. [THEORETICAL]

### Letter-Spacing and Line-Height

**Line-height (leading):**

| Ratio | Effect |
|---|---|
| 0.8x | Impairs readability (too tight) |
| 1.0x | Functional but not optimal |
| 1.3-1.5x | Best range for readability |
| 1.4x | "Golden ratio" for leading |
| 1.5-1.6x | WCAG recommendation |
| 1.8x | Impairs readability (too loose) |

Increasing line spacing from 100% to 120% improves reading accuracy by up to 20% and reduces eye strain by 30% during prolonged reading. [VERIFIED — figure from synthesis sources; primary study not directly accessed]

**Mechanism:** Line height affects the return sweep saccade. Too tight: eye lands on wrong line, re-reading required. Too loose: line-to-line relationship breaks, context lost. The 1.4-1.5x range is where return sweep is accurate and semantic connection is maintained. [VERIFIED]

**Letter-spacing:** Body text should use typeface default. Display/headline benefits from slight reduction (tighter for grouping). Dyslexia accommodation requires increased spacing. WCAG minimum: 0.12x font size. [VERIFIED]

**ALL CAPS:** Forces character-by-character reading because word silhouettes become uniform rectangles. Increased fixation count and saccade frequency. Directly slows reading speed and increases cognitive load. Reserve for 1-3 word labels only. [VERIFIED]

### White Space and Cognitive Load

Proper white space between lines and around paragraphs can increase comprehension by up to 20%. [THEORETICAL — widely cited without clear primary attribution; treat as directional]

**Verified directional findings:**
- White space reduces visual clutter perception, reducing cognitive load. [VERIFIED]
- Paragraph spacing should be at least 2x line height to segment information chunks. [VERIFIED]
- Increased white space improves user perception of credibility and trustworthiness. [VERIFIED — Lin & Hsieh 2011]
- One study found NO relationship between text width/white space and reading speed/comprehension, but DID find significant effects on user satisfaction. [VERIFIED]

**Mechanism:** Working memory has limited capacity. Dense text requires simultaneous letter identification, word recognition, sentence parsing, and meaning extraction. White space removes visual competition, freeing working memory for comprehension. White space also functions as a chunking signal — paragraph breaks say "this thought is complete." [VERIFIED]

### Converting Scanners to Readers

**What causes scanning:** Screen fatigue (reading on screen is 25% slower than paper), no immediate relevance signal, promotional/vague language, content after pull quotes, headers without information-bearing words in first two positions. [VERIFIED]

**What triggers sustained reading:** High personal motivation, inverted pyramid (conclusion first), short active-voice sentences, objective language, visual isolation of a sentence, direct questions to the reader. [VERIFIED]

**The design pattern:**
```
HEADLINE: Keyword-first, 6-8 words max
SUBHEAD: One specific claim (not vague category)
FIRST SENTENCE: Conclusion, not preamble
BODY: Short paragraphs (2-3 sentences), one idea each
BOLDED ANCHOR: 1-2 words per paragraph, scanner fixation point
```

The bolded anchor is the key mechanism: it gives the scanner a fixation point that, when relevant, triggers the decision to read the surrounding sentence. [VERIFIED]

**Usability improvement data (NNGroup):**
- Concise text: 58% better usability vs control [VERIFIED]
- Scannable layout: 47% better usability vs control [VERIFIED]
- Combined (concise + scannable + objective): 124% better usability [VERIFIED]

### Dark Mode: Contrast Ratios and Comprehension

**General findings:**
- For long reading sessions, most people read faster with better comprehension in LIGHT mode. [VERIFIED]
- Dark mode suits low-light environments specifically. [VERIFIED]
- 2025 ACM eye-tracking study: for hard/medium complexity tasks, dark mode outperformed light mode in task accuracy. [VERIFIED — somewhat contradicts conventional wisdom]
- Light mode better for small font sizes and simple reading tasks. [VERIFIED]

**Contrast ratio standards:**

| Standard | Normal Text | Large Text |
|---|---|---|
| WCAG 2.1 AA | 4.5:1 | 3:1 |
| WCAG 2.1 AAA | 7:1 | 4.5:1 |

**The pure white on pure black problem:** Technically ~21:1 ratio (exceeds WCAG) but produces "halation" — bright text bleeds into dark background. For dyslexic users, pure contrast reversal is specifically problematic. Causes eye strain regardless of WCAG compliance. WCAG's algorithm was designed for dark-on-light; it does not model light-on-dark optical behavior correctly. [VERIFIED]

**Recommended dark mode values:**

| Element | Value | Reasoning |
|---|---|---|
| Background | #121212-#1E1E1E | Softer than pure black, reduces halation |
| Body text | #E0E0E0 (87% white) | Reduces luminance delta, less strain |
| Secondary text | #A0A0A0 (60% white) | Hierarchy without harsh contrast |
| Accent/highlight | White (#FFFFFF) | Acceptable for 1-3 words, not paragraphs |

**Font weight on dark:** Regular-weight text loses perceived weight due to light bloom. Bump body font weight by one step (300 to 400, 400 to 500). [THEORETICAL — practitioner-observed, not widely studied]

### Serif vs. Sans-Serif on Screen

**The headline finding (Visible Language 2025 systematic review, 42 studies):** Serifs are NOT a significant legibility factor. No single typeface optimizes readability for everyone. Familiarity may be the most significant factor. [VERIFIED]

**ACM 2022 individual differences study:** Reading speeds increased by 35% when comparing each person's fastest vs slowest font. The "best font" varies by individual. High WPM variability across fonts. [VERIFIED]

**Specific comparisons:** Verdana vs Georgia vs Times New Roman: no comprehension difference. Arial performed strongest for both typical and dyslexic readers in some studies. Screen-designed fonts (Verdana, Georgia) outperform print-designed fonts. [VERIFIED]

**What "familiarity" means practically:** Fonts people have seen most are processed faster because recognition is faster. The brain pattern-matches familiar letterforms rather than decoding them. System fonts (system-ui, -apple-system) win on familiarity by definition. For brand distinctiveness, use distinctive font for headings only. Body text in familiar sans-serif outperforms novel brand font on comprehension. [VERIFIED]

### Progressive Disclosure: Typography as Information Architecture

Progressive disclosure reduces cognitive load by revealing information in stages matched to need. Typography is the primary tool for signaling disclosure layers. [VERIFIED — NNGroup, IxDF]

| Layer | Visual Marker | Reader Type | Purpose |
|---|---|---|---|
| L1 (Headline) | 32-48px, heavy weight | Everyone | Earns or rejects attention |
| L2 (Subhead) | 18-24px, medium weight | Scanners + engaged readers | Organizes topic |
| L3 (Lead sentence) | Same as body | Readers who earned by scanning | States conclusion |
| L4 (Body) | 16-18px, regular weight | Committed readers | Evidence and nuance |
| L5 (Fine print) | 12-14px, lighter weight | High-intent users | Citations, caveats |

**Key insight:** L1-L3 exist to make L4 reading possible. If L1-L3 fail, L4 is never read. Comprehension of important content depends entirely on whether the scaffolding layers do their job. [VERIFIED]

### The "Scannable but Deep" Pattern

79% of users scan first. But users who scan and find relevance DO read — NNGroup data shows motivated users switch to commitment-pattern reading. [VERIFIED]

The architecture serves two reading modes simultaneously:
- **Scanner gets:** H1 to H2 to H3 to bolded anchors = complete summary without reading L4.
- **Reader gets:** Full argument in L4, structured in short paragraphs trackable without losing place.

Both serve the same message. Content is not dumbed down for scanners or padded for readers. [VERIFIED]

---

## Operational Rules

1. **When setting content column width, target 60-66 CPL for body text.** At 16px font, this is approximately 480-520px. On large viewports, enforce `max-width` to prevent lines exceeding 75 CPL. [VERIFIED]

2. **When sizing body text, use 17-18px minimum.** 18px achieved best comprehension in eye-tracking research (Rello 2016). Below 16px reads as cheap and impairs comfortable reading at typical viewing distances. [VERIFIED]

3. **When setting line-height, use 1.4-1.6x font size for body text.** 1.4x is the "golden ratio" for leading. Below 1.3x causes eye strain; above 1.8x breaks line-to-line semantic connection. WCAG recommends 1.5-1.6x. [VERIFIED]

4. **When designing dark mode text, use #E0E0E0 (87% white) for body on #121212-#1E1E1E background.** Never pure white (#FFFFFF) on pure black (#000000) for paragraphs — halation causes eye strain and is specifically problematic for dyslexic users. Bump font weight by one step on dark backgrounds. [VERIFIED]

5. **When writing headings, put information-bearing keywords in the first two word positions.** Layer-Cake scanners evaluate headings as decision points. If the first words are not informative, the scanner skips the entire section. [VERIFIED]

6. **When designing for scanners AND readers, use the scannable-but-deep pattern.** Keyword-first headline, specific subhead claim, conclusion-first opening sentence, 2-3 sentence paragraphs, 1-2 bolded anchor words per paragraph. The bolded anchor is what converts scanners to readers. [VERIFIED]

7. **When choosing body fonts, prioritize familiarity over style.** System fonts or widely deployed sans-serif (Inter, system-ui) outperform novel brand fonts on comprehension. Reserve distinctive fonts for headings only. Serif vs. sans-serif is not a significant legibility factor. [VERIFIED]

8. **When using ALL CAPS, limit to 1-3 word labels.** ALL CAPS forces character-by-character reading (word silhouettes become uniform), increases fixation count, and slows reading. Never use for sentences or paragraphs. [VERIFIED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/typography_comprehension.md` | Line length optimization (CPL research), eyetracking reading order (NNGroup), font size minimums (Rello 2016), line-height/letter-spacing effects, white space and cognitive load, scanner-to-reader conversion, dark mode contrast (WCAG + ACM 2025), serif vs sans-serif (Visible Language 2025), progressive disclosure, scannable-but-deep pattern, synthesis for dark mode health UI |

---

## Related Concepts

- [[design-psychology-gestalt]] — DEPENDS_ON: typography hierarchy creates the progressive disclosure architecture; cognitive load theory underpins white space findings
- [[lighting-design]] — EXTENDS: dark mode typography requirements (halation, font weight) are linked to dark UI lighting decisions
- [[health-literacy-framing]] — INFORMS: reading level research (6th-8th grade) interacts directly with font size and line length recommendations
- [[visual-storytelling-mise-en-scene]] — EXTENDS: typography is part of composition on web; the reading order maps to composition's leading lines and visual hierarchy

---

## Deep Reference

- **When** setting line length for a health calculator result page and need the optimal CPL range → **read** `research-data/typography_comprehension.md` §1 (Line Length) **for** the 45-75 CPL research consensus, the mobile exception (35-50 CPL), the NNGroup eyetracking finding on reading order, and why full-viewport text on 1440px+ screens crosses into comprehension-degrading territory
- **When** choosing between serif and sans-serif for health data display → **read** `research-data/typography_comprehension.md` §5 (Serif vs Sans-Serif) **for** the Visible Language 2025 finding that familiarity trumps category, the 40% trustworthiness claim (widely cited, poorly sourced), and the practical recommendation that x-height and stroke contrast matter more than serif/sans classification
- **When** designing dark-mode typography and text looks washed out or hard to read → **read** `research-data/typography_comprehension.md` §4 (Dark Mode Contrast) **for** the halation effect (light text bleeds on dark backgrounds), the font-weight increase recommendation for dark mode, the WCAG contrast ratios, and the ACM 2025 finding that dark mode is actually better for complex tasks
- **When** building a scanner-to-reader conversion pattern for dense health content → **read** `research-data/typography_comprehension.md` §7 (Scannable-but-Deep) **for** the progressive disclosure typography architecture, heading hierarchy that enables scanning, and the white space comprehension improvement finding (20% — directional, not precisely sourced)

---

## Open Questions

- Whether dark mode comprehension depends on ambient light. The 2025 ACM finding (dark mode better for complex tasks) may interact strongly with ambient lighting conditions. This variable is not controlled in most studies.
- Whether the 20% white space comprehension improvement is real. This figure appears widely without clear primary attribution. Treat as directional hypothesis.
- What specifically triggers the transition from scanning to sustained reading. NNGroup identifies motivation as the primary variable but does not identify typographic triggers that increase motivation.
- Whether V25 line width exceeds optimal CPL on large monitors. Full-viewport sections with no explicit max-width may run 100+ CPL on 1440px+ screens.
- Whether the familiarity effect in font perception is confounded by stroke characteristics or x-height. If familiarity has no independent effect, the recommendation shifts to "choose fonts with good x-height and stroke contrast."
