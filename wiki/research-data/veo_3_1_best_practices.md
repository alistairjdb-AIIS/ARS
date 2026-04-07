# Veo 3.1 Operational Best Practices
**Date:** 2026-04-05
**Sources:** DeepMind prompt guide, Google Cloud Vertex AI docs, existing working pipeline at `/root/healthcalculators-full/brand-film/generate.py`
**Status:** Directional. Synthesis of public docs + proven internal prompts. Not exhaustively A/B-tested per prompt feature.

---

## API Reference (working, verified internally)

- **Base URL:** `https://generativelanguage.googleapis.com/v1beta`
- **Models:**
  - `veo-3.1-generate-preview` — Standard quality, **$0.40/s**
  - `veo-3.1-fast-generate-preview` — Fast, **$0.15/s**
- **Endpoint:** `POST /models/{model}:predictLongRunning?key={API_KEY}`
- **Polling:** `GET /{operation_name}?key={API_KEY}` every 15s until `done: true`
- **Duration:** Default parameter `durationSeconds: 8` (8 seconds is the tested working default)
- **Aspect ratios:** `"16:9"` (horizontal) — confirmed working. 9:16 untested in current pipeline.
- **Sample count:** `sampleCount: 1` per request (submit multiple for variants)

## Payload structure

```json
{
  "instances": [{"prompt": "..."}],
  "parameters": {
    "aspectRatio": "16:9",
    "durationSeconds": 8,
    "sampleCount": 1,
    "negativePrompt": "..."
  }
}
```

---

## The 5-Part Prompt Formula (DeepMind guide)

`[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]`

Or the 7-component breakdown:
1. **Shot framing and motion** — how the camera sees and moves
2. **Style** — visual approach (cinematic, stop-motion, film noir, VHS)
3. **Lighting** — quality and direction of illumination
4. **Character/subject descriptions** — specific physical details
5. **Location** — detailed environmental context
6. **Action** — what things are doing
7. **Dialogue** — character speech (or audio cues)

**Principle:** *The more detail you add, the more control you'll have over the final output.* Write prompts like screenplay shot lists, not marketing copy.

---

## Vocabulary — Use These Exact Terms

### Camera composition
- `wide shot`, `medium shot`, `close-up`, `extreme close-up`, `two-shot`
- `low angle`, `high angle`, `overhead`, `Dutch angle`
- `eye-level`, `bird's-eye view`, `worm's-eye view`

### Camera movement
- `dolly shot` (forward/back), `tracking shot`, `crane shot`
- `slow pan`, `tilt up/down`, `POV shot`, `aerial view`
- `push-in`, `pull-out`, `orbit`, `handheld`
- `locked shot`, `near-static`, `micro organic settle` (for subtle breathing)

### Lens & focus
- `85mm lens`, `50mm`, `35mm`, `macro lens`, `wide-angle lens`
- `shallow depth of field`, `deep focus`, `soft focus`, `rack focus`
- `anamorphic bokeh`, `horizontal bokeh`, `lens dust bokeh`
- `chromatic aberration at frame edges`, `halation`

### Lighting
- `key light`, `fill light`, `rim light`, `back light`, `practical light`
- `warm lamplight`, `cold blue-white`, `teal-blue rim`
- `harsh clinical light`, `soft diffused`, `natural sunlight with lens flares`
- `volumetric haze`, `dust motes in light rays`, `god rays`
- `motivated light` (light source visible in frame)
- Direction: `from above`, `sidelight at 45 degrees`, `backlit`

### Texture / film look
- `35mm film grain`, `16mm film grain`, `slight halation`
- `natural vignette`, `subtle chromatic aberration`
- `soft bokeh`, `dense layered depth`

### Style descriptors
- `cinematic`, `editorial`, `documentary`, `stop motion`, `claymation`
- `found-footage`, `VHS aesthetic`, `film noir`, `hyperrealistic`
- `historical adventure setting`, `contemplative`, `moody`

---

## Negative Prompt Patterns (verified from internal working pipeline)

Always exclude hallucinatable artifacts:

**Standard exclusions (use unless contraindicated):**
```
motion blur, warping, morphing, text, readable characters,
overexposure, logos, watermarks, static noise, flickering shadows
```

**For still-life / object work add:**
```
faces, hands, people, bright backgrounds
```

**For calm/controlled scenes add:**
```
jitter, fast motion, busy frame
```

---

## Action Description Intensity (DeepMind guide)

Match action detail to desired control:

- **Simple:** "Poring over an ancient, sprawling map"
- **Moderate:** "Gesturing with [object] towards the churning sea"
- **Complex:** Multi-clause physics description — "suspension bottoming out, water cascading from roof, tires gripping wet stone"

---

## Audio Integration

Veo 3.1 generates audio with video. Include audio cues in prompt:

```
Audio: soft morning ambience, distant birds, faint wind through leaves
Audio: crunchy footsteps on gravel, distant city murmur
Audio: single clean pulse tone every 1.5 seconds, deep bass undertone, near silence between pulses
```

Audio is generated jointly — don't treat it as separate layer in the prompt.

---

## Working Example (from existing brand-film pipeline)

Register demonstrated in `/root/healthcalculators-full/brand-film/generate.py`:

> "Slow dolly forward through a dark void, 85mm lens, shallow depth of field. Dozens of small luminous fragments — cool blue-white geometric shapes, data points, thin lines — drift chaotically in all directions at different speeds across the frame. No two fragments move in the same direction. Fragments sharp in near plane, soft bokeh in far plane, creating dense layered depth. Single cold blue-white key light from directly above, harsh, clinical, casting no shadows on the fragments because they float in empty space. No fill. Deep black background. 35mm film grain visible throughout, slight chromatic aberration at frame edges, anamorphic horizontal bokeh on far elements. Audio: overlapping notification pings, muffled data sounds, building cacophony, no music."

**Notice:**
- Opens with camera + lens + DOF
- Paragraph-form, not bulleted
- Every visual element has a texture/behavior descriptor
- Explicit depth layers (near/far)
- Light temperature + direction + quality
- Frame edges mentioned (aberration, bokeh)
- Audio last as distinct directive

---

## Operational Lessons (from internal pipeline)

- **Polling interval:** 15s between operation status checks
- **Timeout:** 600s max wait per generation
- **Download:** returned video URI requires API key appended, follow redirects
- **Cost-controlled iteration:** use `fast` model (`$0.15/s`) for craft experiments, `standard` (`$0.40/s`) for final renders
- **Variants:** run same prompt with `variant` suffix in filename to collect multiple samples

---

## Known Gaps / Unverified

- **9:16 aspect ratio:** not tested in current pipeline. May or may not be supported.
- **Durations other than 8s:** current pipeline uses 8s only. Parameter accepts other values per docs but untested internally.
- **Image-to-video:** Veo 3.1 may support image conditioning; not exercised in internal pipeline yet.
- **Multi-shot sequencing:** current pipeline renders each beat separately and concatenates via ffmpeg. No single-prompt multi-shot shown to work.
- **Character consistency across shots:** unverified. Likely requires reference image conditioning if supported.
