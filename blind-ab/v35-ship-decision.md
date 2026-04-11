# v35 SHIP DECISION — Both Outputs (Template v2)

Second use of SHIP DECISION template. **New row added after v34 miss:** `Motion type`.

Reference loaded: `/root/twitter-pipeline/pulse-nb2-proud.png` (NB2 canonical Pulse: round fluffy yellow body, no external ears, big brown eyes, halo, feathered wings, paw-hands).

Frames extracted: 5 per output (0%, 20%, 40%, 60%, 80% of 8.00s).

Wiki references consulted this session: `wiki/tools/veo-3-1.md`, `wiki/registers/anime.md`.

---

## v35-output-a.mp4

**Reference loaded:** `pulse-nb2-proud.png`
**Output loaded:** `v35-frames/a_f0..f4.jpg`

### Character match vs. NB2
| Trait | NB2 canon | Observed | Verdict |
|---|---|---|---|
| Body shape | Round fluffy blob | **Human anime child** (slender, limbed) | ❌ drift |
| External ears | None | **Pointed elf ears** | ❌ drift |
| Eyes | Big brown | Dark (brown?) — anime child style | partial |
| Halo | Gold, above | Gold, above | ✅ |
| Wings | Small feathered | **Large white feathered** (proportionally huge) | partial |
| Paw-hands | Small stubby | Human hands | ❌ drift |
| Skin | N/A (fur) | Dark brown skin tone | N/A |

**Character verdict:** 1/6 traits match (halo). Model rendered "round yellow fluffy angel" as an anime elf child with dramatic wings.

### Scene match
- Window at sunset: ✅
- Wooden windowsill: ✅
- Rooftops/city in distance: present, unprompted but atmospheric
- Warm evening light: ✅
- Register: Studio Ghibli-ish anime ✅

### Motion type (NEW ROW)
| | |
|---|---|
| **Motion type** | **both (character + camera)** |
| If camera | push-in with shot change (f0-f1 wide, f2-f4 close-up) |
| If character | facial + posture change (look down → look up → sparkle-eye "realization" → smile) |

### Motion claims (observable in frames)
- f0→f1: micro-motion, still looking down (subtle)
- f1→f2: **BIG BEAT** — character looks up, stars sparkle in eyes (anime realization trope), camera has push-in to close-up
- f2→f3: eye sparkles continue, small posture shift
- f3→f4: **open-mouth delighted smile**, looking down at drawing
- **Net:** real acting-chain animation, BUT camera composition changes dramatically (wide → close-up → medium) — likely a shot cut, not a single fluid shot

### Ship/retry: **DO NOT SHIP as Pulse**
- Character drift is near-total (1/6). This is not Pulse — it's a dark-skinned anime elf child with giant wings.
- Motion is real and emotionally coherent — the animation itself works, just on the wrong character
- Could ship as "Veo interpreted 'round yellow fluffy angel' as an anime elf child" learning-in-public post
- If goal is Pulse character library: retry with stronger NB2 anchor

---

## v35-output-b.mp4

**Reference loaded:** `pulse-nb2-proud.png`
**Output loaded:** `v35-frames/b_f0..f4.jpg`

### Character match vs. NB2
| Trait | NB2 canon | Observed | Verdict |
|---|---|---|---|
| Body shape | Round fluffy blob | **Round fluffy body**, cat/fox-like | ✅ (closer) |
| External ears | None | **Fox/cat triangular ears** | ❌ drift |
| Eyes | Big brown | **Big brown eyes with highlights** | ✅ |
| Halo | Gold, above | Gold, above, sparkly | ✅ |
| Wings | Small feathered | **Small iridescent wings** (pearl/blue) | partial (wrong color) |
| Paw-hands | Small stubby | Small, holding drawing | ✅ |
| Snout | None (round face) | Small cat-like muzzle | ❌ drift |

**Character verdict:** ~4/6 traits match. Still drift (ears + snout + wing color) but the body-shape anchor held. Significantly closer to NB2 than v35-a.

### Scene match
- Window at sunset: ✅
- Wooden floorboards: ✅
- Warm golden light + god rays through window: ✅
- Curtain in frame: present (unprompted atmospheric)
- Register: Ghibli-adjacent anime ✅

### Motion type (NEW ROW)
| | |
|---|---|
| **Motion type** | **both (character + camera), character-dominant** |
| If camera | moderate push-in (f0 wider, f4 closer), no shot cut |
| If character | facial motion: eye state changes, mouth expression changes, halo sparkle animation |

### Motion claims (observable in frames)
- f0: holding drawing, looking down, neutral expression
- f1: **eyes fully closed, content smile** — quiet contemplation beat
- f2: eyes open, looking up, neutral/curious (camera pushed in)
- f3: small smile beginning, mouth slightly parted
- f4: **delighted open-mouth smile**, looking up, halo sparkles intensify
- **Net:** clean acting chain (holding → contemplation → look up → realization → delight). Character stays CONSISTENT across all 5 frames. Camera push-in is subtle, character motion is dominant.

### Ship/retry: **SHIP-READY**
- Character body shape anchor held — closest Pulse we have generated
- Real character animation with coherent acting chain
- Caption-safe: "Pulse looks at a drawing, closes eyes, looks up, smiles" — each beat is observable
- Caveat: fox/cat ears + snout are character drift; could be relabeled as "Pulse explores an anime sub-style" rather than strict canon
- Motion quality is the best of any Pulse video this session

---

## Comparison summary

| Dimension | v35-output-a | v35-output-b |
|---|---|---|
| Character fidelity to NB2 | 1/6 (elf child) | 4/6 (fluffy creature with ears) |
| Character consistency across frames | ❌ shot-cut framing changes | ✅ held |
| Motion type | character + camera (shot change) | character + camera (push-in) |
| Acting chain coherence | ✅ (but on wrong character) | ✅ |
| Ship-ready as Pulse | no | yes, with caveats |

---

## Notes on the template's second use (v2)

**Motion type row worked.** v34's single "motion visible: yes/no" row hid the still+camera-pan failure. The v2 split into "motion type" + specifics made it immediately visible that v35-a has a shot-cut (wide → close-up) which is a different beast from v35-b's continuous push-in.

**What v2 still misses:** the "shot cut vs single shot" distinction. v35-a has what looks like a scene cut mid-video, not a dolly. Template v3 could add: "Number of apparent shots in the clip."

**Wiki reference integration worked.** Reading `veo-3-1.md` before rendering gave me the "acting beats ≤3" limit and "acting-chain > camera spec" rule — both validated by v35-b's clean acting chain. Reading `anime.md` gave the "static composition + cuts, not continuous movement" framing grammar — which explains why v35-a's apparent shot cut is actually register-consistent for anime.

**v34 vs v35 tool comparison (side note):** v35 rendered real character animation on both outputs, confirming Kling v1-6 was the bottleneck, not the prompts. Veo 3.1 Fast is the right tool for this class of render.
