# SHIP DECISION Template — canonical reference

The reusable judgment artifact for "is this rendered video ship-ready?"

Created session 36 (v34 → v35 → v36 → v37 → v38 evolution). Lives here because it's
the single source of truth referenced by every `v{N}-ship-decision.md` file.

---

## Version history

| Version | Introduced | Added | Reason |
|---|---|---|---|
| v1 | v34 (Apr 11) | Character match + scene match + motion claims | First use; caught character drift on v34 but missed still+camera-pan |
| v2 | v35 (Apr 11) | **Motion type** row (character / camera / both / none) | Operator caught that v34's "no motion" was character-only; camera was panning. Row forces enumeration. |
| v3 | v39 (Apr 11) | **Object consistency + material fidelity + framing grammar** rows. **Mechanism change: contact sheet.** | Operator caught v37 bugs I missed (spawning cans, cap-on-back, morphing earbuds, breath-as-vape-smoke). 5 stills read independently cannot catch temporal continuity issues. Contact sheet = all frames in one grid image = cross-frame bugs become visible. |

---

## How to use (v3)

### Step 1 — Build the contact sheet

For an 8s clip, extract 10 frames and tile them 5x2:

```bash
ffmpeg -loglevel error -y -i <video.mp4> \
  -vf "fps=10/<duration>,tile=5x2:padding=4:color=white" \
  -frames:v 1 -q:v 2 <contact-sheet.jpg>
```

- For 8s clip: `fps=10/8` = 1.25 fps
- For 10s clip: `fps=1`
- For 30s concat: `fps=10/30` = 0.333 fps

The output is ONE JPG containing all 10 frames as a 5-wide 2-tall grid, read-once.

### Step 2 — Load the reference + the contact sheet

- Read the reference image (character bible, brand reference, or NB2 canon) if applicable
- Read the contact sheet

### Step 3 — Fill the v3 template

```markdown
# SHIP DECISION — <filename>

Reference loaded: <path(s)>
Output loaded: contact-sheet.jpg (<N> frames at <fps> fps)

## Character match vs reference
| Trait | Reference | Observed | Verdict |
|---|---|---|---|
| ... | ... | ... | ✅ / ❌ / partial |

## Scene match
- <prompted element>: ✅ / ❌ / partial
- ...

## Motion type (v2)
- Type: [character / camera / both / none]
- If camera: [pan / tilt / dolly / push-in / shot cut]
- If character: [facial / body / both]

## Object consistency (v3, cross-frame)
- Objects held by character: [stable / spawns / morphs / disappears / count changes]
- Object count in frame: [stable / changes]
- Object topology: [stable / impossible transitions]
- Character body: [stable / morphs / parts drift]
- Clothing/held items: [stable / morph]

## Material fidelity (v3, rendering realism)
- Breath/vapor/smoke: [reads as intended / reads as wrong element]
- Liquid/splash: [reads real / reads CG]
- Cloth/fur/fabric: [reads real / reads plastic]
- Skin/face (if visible): [outside uncanny valley / inside]

## Framing grammar (v3, register conformance)
- Register expected: [anime / photoreal / Pixar / documentary / etc.]
- Motion type observed: <character + camera locked / char + push-in / etc.>
- Register-correct? [yes / no / partial]

## Motion claims (observable in frames)
- <claim 1>: visible in contact sheet [cell N] / not visible
- ...

## Ship/retry decision
<decision> — <one-line reason>
```

---

## When to use which version

- **v1** — never (deprecated)
- **v2** — acceptable for single-clip renders where object consistency isn't a concern (abstract, motion graphics, still-life)
- **v3** — required for any render with characters, held objects, material physics (breath, liquid, fire), or register-specific framing grammar (anime, brand film, photoreal)

---

## Known template blind spots (future v4 candidates)

These are NOT yet in the template. Add when evidence accumulates:

- **Audio fidelity check** — did the audio actually get generated? Does it match the prompt's audio cues? (Current v3 doesn't verify audio — but Veo 3.1 generates audio, so silently missing audio on a shipped clip is a real risk.)
- **Timing check** — do motion beats land on expected time marks? (Brand films often have sync requirements.)
- **Chain continuity** — for multi-clip chains, does clip N+1's first frame actually match clip N's last frame? (Becomes important only for 30s+ content.)

These aren't speculative — each will get added when a specific miss provides the evidence, per OS §7.
