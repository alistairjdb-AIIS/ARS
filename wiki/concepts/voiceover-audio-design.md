# Voiceover and Audio Design

> Educational Reels require voice at t=0 (not a music intro), 120-140 WPM for German and 130-150 WPM for English, keywords-only on screen (Mayer's Redundancy Principle), and a -16 LUFS voice mix. The target register is "smooth-authoritative" -- forward-projecting energy at "let me show you something" intensity, with clean downward-inflection endings and 0.3-0.5s functional micro-pauses between facts.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 0 memory files

---

## Core Findings

### Voice Delivery Rules

1. **120-140 WPM for German** (130-150 WPM English equivalent). Below 120 WPM enters meditational territory. [VERIFIED -- research synthesis]
2. **Voice starts at t=0** -- no music intro. Produces +22% completion, +31% saves (Meta 2024 Creators Report). [VERIFIED]
3. **Narrate throughout** -- no music-only sections longer than 1 second in educational content. [VERIFIED]
4. **0.3-0.5s micro-pauses** between facts. These are functional pauses (processing time), not contemplative pauses. [VERIFIED]
5. **0.5-0.8s pause BEFORE key stat** -- anticipation is more effective than post-stat processing time. [VERIFIED]
6. **Clean sentence endings** with downward inflection = certainty signal. [VERIFIED]
7. **Energy register: "let me show you something"** -- forward-projecting, not retreating. [VERIFIED]

### Smooth-Authoritative vs Meditational Register

| Dimension | Meditational (rejected) | Target |
|-----------|------------------------|--------|
| Pace | 100-120 WPM | 130-150 WPM |
| Pauses | 1-2s contemplative | 0.3-0.5s functional |
| Energy | Low, retreating | Mid-high, forward |
| Endings | Trail off | Land clean, downward |
| Overall | "Guide you inward" | "Show you something" |

The meditational register is explicitly rejected for educational Reels content. It may be appropriate for wellness/meditation content (cf. Calm's brand voice) but signals passivity rather than authority in an educational context. [VERIFIED]

### Voice + Text Relationship (Mayer's Redundancy Principle)

The core principle: graphics + narration outperform graphics + narration + full text displayed simultaneously. [VERIFIED -- Mayer's Cognitive Theory of Multimedia Learning, peer-reviewed]

Application to Reels structure:

**Hook (0-2s):** Full sentence on screen + voice simultaneously. This is the ONE exception to the keywords-only rule -- the hook needs maximum multi-channel reinforcement. [VERIFIED]

**Body (2s+):** Voice carries full information. Screen shows 2-5 keyword phrases only. Never full narration sentences on screen after the hook. [VERIFIED]

**Stat reveals:** Show the number on screen 0.3s BEFORE voice says it. The visual-first reveal creates anticipation that the voice then confirms. [VERIFIED]

**CTA:** Voice + text together. Reinforcement is correct for instructions/calls-to-action (Mayer's signaling principle). [VERIFIED]

**Keywords-only exception:** Short redundant phrases near visuals DO help comprehension. The prohibition is on full sentences duplicating narration, not on all text. [VERIFIED]

### Audio Mix Specifications

- Voice target: **-16 LUFS** (Instagram standard). [VERIFIED]
- Background music bed: **-18 to -24 dB below voice**. [VERIFIED]
- **Burned-in animated captions** outperform auto-captions for quality and brand consistency. [VERIFIED]

### Educational Structure Template (12-15s)

```
[0.0-0.5s]  HOOK: Voice + full text + motion
[0.5-2.0s]  PROBLEM: What viewer gets wrong
[2.0-2.5s]  TRANSITION: 0.3s pause + visual cut
[2.5-8.0s]  EXPLANATION: Voice narrates, keywords appear
[8.0-8.5s]  BEAT DROP: 0.5s pause before stat
[8.5-10.0s] STAT: Number on screen, voice confirms
[10-12s]    CONTEXT: "What this means for you"
[12-15s]    CTA: Voice + text
```

### Supporting Evidence

- Meta 2024 Creators Report: voiceover in first 3 seconds = +22% completion, +31% saves. [VERIFIED -- HIGH confidence]
- Emplifi (10,110 Reels): human speech in first 3 seconds = +25% retention at 10s. [VERIFIED -- HIGH confidence]
- 80% of Reels viewed with sound on (Meta). [VERIFIED -- HIGH confidence]
- Mayer's Redundancy Principle: graphics + narration > graphics + narration + full text. [VERIFIED -- HIGH confidence, peer-reviewed]

---

## Operational Rules

1. **When producing any educational Reel, start voice at exactly t=0 with no music intro** -- the +22% completion and +31% saves lift is the single largest production technique effect measured, because Meta's 2024 data confirms voice-first drives both retention and save behavior.

2. **When setting voice pace, target 130-150 WPM for English and 120-140 WPM for German** -- below 120 WPM enters meditational register which signals passivity rather than authority, because the pace must convey "let me show you something" energy.

3. **When displaying text during narration, use keywords only (2-5 phrases) after the initial hook** -- full sentences on screen while narrating creates cognitive overload per Mayer's Redundancy Principle, because the brain cannot read and listen simultaneously without one channel degrading.

4. **When revealing statistics, show the number on screen 0.3s BEFORE the voice says it** -- visual-first stat reveals create an anticipation beat that the voice then confirms, which is more engaging than simultaneous delivery.

5. **When inserting pauses, use 0.3-0.5s between facts and 0.5-0.8s BEFORE key stats** -- these are functional processing pauses, not contemplative ones, because the anticipation pause before a stat drives more engagement than a processing pause after it.

6. **When mixing audio, set voice at -16 LUFS and music bed at -18 to -24 dB below voice** -- -16 LUFS is the Instagram standard and ensures consistent loudness across the platform.

7. **When adding captions, use burned-in animated captions rather than auto-captions** -- burned-in captions allow brand-consistent typography and timing control that auto-captions cannot provide.

---

## Source Files

| File | Contribution |
|------|-------------|
| `research-data/educational_reels_voiceover_2026.md` | All voice delivery rules, audio mix specs, Mayer's Redundancy Principle application, smooth-authoritative vs meditational register, educational structure template |

---

## Related Concepts

- [[reels-pacing-structure]] — DEPENDS_ON: the structural template that voiceover timing fits within
- [[hook-first-half-second]] — INFORMS: voice at t=0 is a critical component of the hook mechanism
- [[engagement-scoring-matrix]] — INFORMS: audio design affects Hook, Pacing, and Production Quality dimensions
- [[reels-algorithm-signals]] -- Meta's AI analyzes voiceover audio for content categorization
- [[continuity-editing-scene-flow]] — INFORMS: continuity editing uses audio bridging (J-cuts, L-cuts, ambient sound continuity) as one of its primary techniques for hiding cuts, and voiceover design determines how those audio bridges are constructed

---

## Deep Reference

- **When** mixing voice and background music and need exact dB levels → **read** `research-data/educational_reels_voiceover_2026.md` §(Audio Mix) **for** voice at -16 LUFS (Instagram standard), background music bed at -18 to -24 dB below voice, and why burned-in animated captions outperform auto-captions
- **When** the voiceover sounds meditational instead of authoritative and need to diagnose → **read** `research-data/educational_reels_voiceover_2026.md` §(Smooth-Authoritative vs Meditational) **for** the dimension-by-dimension comparison table (pace 100-120 WPM = meditational vs 130-150 = target, 1-2s contemplative pauses = meditational vs 0.3-0.5s functional, "guide you inward" energy = rejected vs "show you something" = target)
- **When** deciding when to show text on screen vs let voice carry → **read** `research-data/educational_reels_voiceover_2026.md` §(Voice + Text Relationship) **for** Mayer's Redundancy Principle applied per segment: hook (0-2s) = full sentence + voice simultaneously, body (2s+) = voice carries full info + 2-5 keyword phrases only, stat reveals = number on screen 0.3s BEFORE voice says it, CTA = voice + text together

---

## Open Questions

- Does the 120-140 WPM German target hold for medical/scientific content where terminology is dense? Slower pace might aid comprehension of technical terms.
- Does the Mayer Redundancy Principle fully transfer from e-learning environments (where it was established) to autoplay social media where attention is more fragile?
- If music-intro Reels outperform voice-first for certain verticals (e.g., lifestyle, fashion), is the voice-first rule actually universal or educational-specific?
- What is the optimal voice gender, age, and accent for medical educational content in German? The research establishes pace and energy but not demographic characteristics.
