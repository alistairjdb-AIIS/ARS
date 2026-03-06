# ARS System Design

## Methodology: Architecture-First via Loops
- Systems are sets of self-sustaining loops, not feature lists.
- Each loop: READ, EVALUATE, CORRECT, ESCALATE, FAIL-VISIBLE, BOUND.
- 12 questions per loop before implementation.
- Build order: inventory loops → answer questions → build most critical first → supervisory layer.
- Tool selection per loop (free or paid), informed by deep research.
- No code before loop inventory.

## Concept: Game-to-Agent Bridge
- Browser game → behavioral data collection → personalized AI agent relationship.
- Phase 1 (Game): Engagement + data + AdSense revenue.
- Phase 2 (Bridge): Imperceptible per-user transition from game to agent surface.
- Phase 3 (Agent): Personalized reasoning partner + subscription revenue.
- The game is the delivery mechanism. The agent relationship is the product.

## Critical Unknown
- Transition gradient (Phase 2) — can it advance without killing retention?
- No blueprint exists. Must be proven via A/B testing with real users.
- Requires Phase 1 users first. Can't test without data.

## Design Decisions

### Target User Type (DECIDED)
- **Primary target: Knowledge workers aged 25-40 who play casual games as break/decompression.**
- Reasoning: Satisfies all three phase constraints simultaneously:
  - Phase 1: They already play casual games (Wordle, NYT Games, 2048, Block Blast). High session frequency.
  - Phase 3: Disposable income + real cognitive needs (work, learning, decisions). Willingness to pay.
  - Bridge: Play with intention — behavioral data carries signal, not noise.
- Niche targeting preferred over broad — going after everyone expands competitive landscape.
- Virality could reach this range organically; niche focus gives competitive wedge.
- Alternative considered: younger (18-24) for higher data volume, rejected due to low Phase 3 conversion probability.

### Game Personalization (DECIDED)
- Game itself does NOT need to be different per user.
- Adaptive difficulty can adjust uniformly for all users.
- Per-user game personalization is optional, not required for launch.

### Bridge Personalization (DECIDED)
- **Standard (uniform) bridge first. No per-user personalization at launch.**
- Same trigger, same introduction framing for all users.
- A/B test a small number of static variants to find best performer.
- Reasoning: Personalized bridge requires labeled conversion data that doesn't exist yet. Standard bridge provides the baseline + data needed to justify personalization later.
- Personalization is a future iteration if standard bridge conversion is insufficient and enough user data exists to train on.
- Cost comparison: standard ~1x eng effort (weeks); personalized ~3-5x (months, ML pipeline, per-user data infra).

### Build Order (DECIDED)
- Get users first (Phase 1), then build bridge (Phase 2).
- Phase 1 can ship without transition gradient being solved.

### Game Mechanic (DECIDED)
- **Daily nonogram (picross) — browser-based, one puzzle per day, streak mechanics, pixel-art image reveal on completion.**
- Evaluated against: word puzzle (Wordle-like), mini-crossword, strategic card game, pattern/sorting puzzle, trivia, physics puzzle, strategy/tower defense.
- Weighted criteria: behavioral data richness (35%), daily return rate (30%), build complexity (20%), competitive whitespace (15%).

**Why nonogram won:**
- **Data richness:** Each cell decision is traceable. Deductive reasoning style, pattern recognition speed, risk tolerance (guessing vs. certainty-seeking), persistence after errors, strategic approach (which rows/columns tackled first). Decision density: 12-27 decisions/min at intermediate level (derived from solve time data, not directly measured — see caveats).
- **Daily return:** One-per-day scarcity mechanic (proven by Wordle/NYT). Streak psychology. Pixel-art reveal = shareable social moment. Intellectually permissible for knowledge workers. 3-8 min sessions fit micro-break pattern.
- **Build feasibility:** 4-6 weeks solo dev. Vanilla JS + Canvas. Open-source solvers/generators exist (HandsomeOne/Nonogram 150 stars, liouh/picross 74 stars). Largest existing browser nonogram is ~2,000 LOC.
- **Whitespace:** No dominant free browser nonogram destination (verified). Top sites: puzzle-nonograms.com (~1.4M monthly visits), nonograms.org (~1.2M). Easybrain dominates mobile (50M+ app downloads) but website is just an app funnel. The "daily nonogram" slot is unclaimed at scale.

**Runner-up:** Mini-crossword. Proven daily-return pattern, freshly opened gap (NYT paywalled Mini Crossword on Aug 27, 2025). Lower data richness but safer market bet. If nonogram fails to attract target users, mini-crossword is the fallback.

**Verified claims:**
- NYT Mini Crossword paywall: confirmed, Aug 27, 2025, hard paywall.
- No dominant browser nonogram: confirmed, fragmented across ~10 small sites.
- JS solver/generator repos: confirmed, multiple on GitHub.
- Build estimate: confirmed by codebase analysis of existing projects.

**Caveats (flagged for downstream phases):**
1. **Behavioral data richness is theoretical, not proven.** No published study has directly measured hesitation, error recovery, or planning depth in human nonogram gameplay. Claim is extrapolated from general puzzle/cognitive research. Must be validated with real player data post-launch.
2. **Target demo overlap is a bet, not a fact.** No nonogram-specific demographic study exists. Puzzle demographics skew female, 35+. One data point (puzzle-nonograms.com: 61% male, largest cohort 25-34) is partially supportive. If actual audience differs from target, bridge and agent can adapt to whoever shows up.
3. **Search demand is niche.** Nonogram volume is far below Wordle/Sudoku/crossword. Not a viral wave — growth depends on execution and marketing.
4. **Decision density figure (5-15/min in original claim) was corrected.** Beginner: 9-16/min, intermediate: 12-27/min, expert: 30-80/min. Derived from solve times, not directly measured anywhere.

**Tech stack:** Vanilla JS + Canvas API. No framework needed. React acceptable if component state management is desired. Phaser is overkill for this mechanic.

**Ad monetization:** AdSense H5 Games program initially, layer AdinPlay/Venatus for gaming-native formats. Conservative Session RPM: $0.50-$1.50 (display only). Interstitials between daily puzzle and result reveal (natural break point). Never interrupt active play.

## Open Questions
- Marketing/content strategy for user acquisition (sequenced after build)
- Where can LLM research excel at producing the right game content (puzzle generation, pixel-art design)?
- Behavioral data schema — what specific events to log from gameplay for bridge phase?

## Research Queue
1. Marketing/content — how to acquire target users
2. Behavioral data schema design — define event taxonomy before build
3. Puzzle content pipeline — pixel-art source images, difficulty calibration, daily curation
