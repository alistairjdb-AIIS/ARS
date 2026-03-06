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

## Open Questions
- What game mechanic to build? (Desk research needed — evaluating multiple options)
- Marketing/content strategy for user acquisition (sequenced after game mechanic decision)
- Where can LLM research excel at producing the right game?

## Research Queue
1. Game mechanic evaluation — what mechanic, for target user type, maximizes play frequency + behavioral data richness?
2. Marketing/content — how to acquire target users (sequenced after #1)
