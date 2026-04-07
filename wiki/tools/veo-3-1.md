# Google Veo 3.1

> AI video generation model from Google DeepMind that jointly generates video and audio from text prompts, optimized for cinematic photoreal output with precise camera, lighting, and audio control.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 0 memory files

---

## Core Findings

### Capabilities

**Models and pricing:**

| Model ID | Tier | Cost | Use |
|----------|------|------|-----|
| `veo-3.1-generate-preview` | Standard | $0.40/s | Final renders |
| `veo-3.1-fast-generate-preview` | Fast | $0.15/s | Craft experiments, iteration |

- **Duration:** 8 seconds is the tested working default [TESTED]
- **Aspect ratio:** 16:9 confirmed working [TESTED]; 9:16 untested [THEORETICAL]
- **Sample count:** 1 per request; submit multiple requests for variants [TESTED]
- **Audio:** Generated jointly with video -- not a separate layer. Include audio cues directly in the prompt. [VERIFIED]
- **Image-to-video:** May be supported per docs but not exercised in any internal pipeline [THEORETICAL]

**API surface:**

- **Base URL:** `https://generativelanguage.googleapis.com/v1beta`
- **Generate:** `POST /models/{model}:predictLongRunning?key={API_KEY}`
- **Poll:** `GET /{operation_name}?key={API_KEY}` -- poll every 15s until `done: true`
- **Timeout:** 600s max wait per generation [TESTED]
- **Download:** Returned video URI requires API key appended; follow redirects [TESTED]

**Payload structure:**
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

### Prompt Patterns

#### The 5-Part Prompt Formula (DeepMind guide) [VERIFIED]

`[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]`

Expanded to 7 components:
1. **Shot framing and motion** -- how the camera sees and moves
2. **Style** -- visual approach (cinematic, stop-motion, film noir, VHS)
3. **Lighting** -- quality and direction of illumination
4. **Character/subject descriptions** -- specific physical details
5. **Location** -- detailed environmental context
6. **Action** -- what things are doing
7. **Dialogue / Audio** -- character speech or audio cues

**Principle:** Write prompts like screenplay shot lists, not marketing copy. The more detail, the more control. [VERIFIED]

#### Vocabulary Reference

**Camera composition:** `wide shot`, `medium shot`, `close-up`, `extreme close-up`, `two-shot`, `low angle`, `high angle`, `overhead`, `Dutch angle`, `eye-level`, `bird's-eye view`, `worm's-eye view`

**Camera movement:** `dolly shot`, `tracking shot`, `crane shot`, `slow pan`, `tilt up/down`, `POV shot`, `aerial view`, `push-in`, `pull-out`, `orbit`, `handheld`, `locked shot`, `near-static`, `micro organic settle`

**Lens and focus:** `85mm lens`, `50mm`, `35mm`, `macro lens`, `wide-angle lens`, `shallow depth of field`, `deep focus`, `soft focus`, `rack focus`, `anamorphic bokeh`, `horizontal bokeh`, `lens dust bokeh`, `chromatic aberration at frame edges`, `halation`

**Lighting:** `key light`, `fill light`, `rim light`, `back light`, `practical light`, `warm lamplight`, `cold blue-white`, `teal-blue rim`, `harsh clinical light`, `soft diffused`, `natural sunlight with lens flares`, `volumetric haze`, `dust motes in light rays`, `god rays`, `motivated light`, `from above`, `sidelight at 45 degrees`, `backlit`

**Texture / film look:** `35mm film grain`, `16mm film grain`, `slight halation`, `natural vignette`, `subtle chromatic aberration`, `soft bokeh`, `dense layered depth`

**Style descriptors:** `cinematic`, `editorial`, `documentary`, `stop motion`, `claymation`, `found-footage`, `VHS aesthetic`, `film noir`, `hyperrealistic`

#### Audio Integration

Include audio cues as a distinct directive at the end of the prompt:
```
Audio: soft morning ambience, distant birds, faint wind through leaves
Audio: crunchy footsteps on gravel, distant city murmur
Audio: single clean pulse tone every 1.5 seconds, deep bass undertone
```

Audio is generated jointly with video. Do not treat it as a separate layer. [VERIFIED]

#### Action Description Intensity

Match detail to desired control:
- **Simple:** "Poring over an ancient, sprawling map"
- **Moderate:** "Gesturing with [object] towards the churning sea"
- **Complex:** Multi-clause physics -- "suspension bottoming out, water cascading from roof, tires gripping wet stone"

#### Negative Prompt Patterns [TESTED]

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

#### Working Example (from internal pipeline) [TESTED]

> "Slow dolly forward through a dark void, 85mm lens, shallow depth of field. Dozens of small luminous fragments -- cool blue-white geometric shapes, data points, thin lines -- drift chaotically in all directions at different speeds across the frame. No two fragments move in the same direction. Fragments sharp in near plane, soft bokeh in far plane, creating dense layered depth. Single cold blue-white key light from directly above, harsh, clinical, casting no shadows on the fragments because they float in empty space. No fill. Deep black background. 35mm film grain visible throughout, slight chromatic aberration at frame edges, anamorphic horizontal bokeh on far elements. Audio: overlapping notification pings, muffled data sounds, building cacophony, no music."

Structure demonstrated:
- Opens with camera + lens + DOF
- Paragraph-form, not bulleted
- Every visual element has a texture/behavior descriptor
- Explicit depth layers (near/far)
- Light temperature + direction + quality
- Frame edges mentioned (aberration, bokeh)
- Audio last as distinct directive

### Operational Patterns

- **Polling interval:** 15s between operation status checks [TESTED]
- **Timeout:** 600s max wait [TESTED]
- **Cost-controlled iteration:** Use `fast` model ($0.15/s) for experiments, `standard` ($0.40/s) for final renders [TESTED]
- **Variants:** Run same prompt with `variant` suffix in filename to collect multiple samples [TESTED]
- **API key handling:** Load via env var `VEO_API_KEY`. Never hardcode in committed scripts -- Google auto-scans public repos and revokes exposed keys. [TESTED -- key was revoked after accidental exposure]
- **Cost per 8s clip:** $1.20 (fast) or $3.20 (standard) [VERIFIED]

### Quality Assessment

**Where Veo 3.1 excels:**
- Photoreal environments, objects, still-life scenes [TESTED across 10+ A/B tests]
- Camera and lighting control via precise vocabulary [TESTED]
- Joint audio generation (unique capability vs competitors) [VERIFIED]
- Stylized characters: anime, Pixar-style, cartoon [TESTED across v11-v17]

**Where Veo 3.1 struggles:**
- Photoreal human faces -- Kling AI outperforms for this [TESTED, cross-model finding from A/B v18]
- Gooseneck-pour steam physics (overly-wide steam artifact) [TESTED]
- Character consistency across shots (unverified, likely requires image conditioning) [THEORETICAL]
- Multi-shot sequencing in single prompt (not shown to work) [THEORETICAL]

**Key finding from blind A/B testing (N=8 photoreal, N=7 stylized):**
- Primary quality axis is **narrative coherence** (does the output tell ONE physical story?), not prompt depth [TESTED]
- Binary quality veto: **"too perfect"** -- any element that looks unnaturally perfect vetoes the output regardless of other strengths [TESTED]
- Prompt-depth is a proxy, not the causal axis [TESTED, reframed after N=8]

---

## Operational Rules

- **When generating video,** load API key from `VEO_API_KEY` env var, because Google auto-revokes hardcoded keys in public repos. [TESTED]
- **When iterating on craft,** use `veo-3.1-fast-generate-preview` ($0.15/s), because the fast model costs 2.6x less and is adequate for evaluating prompt effectiveness. [TESTED]
- **When writing prompts,** open with camera + lens + DOF, then subject, then action, then lighting, then audio last, because this mirrors the 5-part formula and matches proven working prompts. [VERIFIED]
- **When prompting for realism,** strip perfectionist language and introduce imperfections, because "too perfect" is a binary veto in quality assessment. [TESTED]
- **When working with photoreal humans,** use [[kling-ai]] instead, because Kling AI outperforms Veo for face photorealism. [TESTED]
- **When prompting for stylized characters,** use acting-chain specificity (stimulus > processing > response) and avoid camera choreography over-specification, because acting direction improves output while DP-level camera instruction hurts it. [TESTED]
- **When building multi-shot sequences,** render each beat separately and concatenate via ffmpeg, because single-prompt multi-shot is unverified. [TESTED]
- **When limiting beat count,** keep to 2-3 acting beats per 8-second clip, because 5+ beats cause visible scene transitions and fluidity breaks. [TESTED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `tools/research-data/veo_3_1_best_practices.md` | API reference, 5-part formula, vocabulary, negative prompts, operational lessons, working example |
| `project-curriculum-elements.md` (memory) | A/B test findings: narrative coherence axis, too-perfect veto, beat count limits, Kling vs Veo for faces, acting-chain specificity |

---

## Related Concepts

- [[kling-ai]] -- Outperforms Veo for photoreal human faces; complementary tool
- [[elevenlabs]] -- Alternative/supplementary audio generation when Veo's joint audio is insufficient
- [[recraft-v4]] -- Static frame generation for storyboard/reference before Veo video generation

---

## Open Questions

- 9:16 aspect ratio support -- not tested in any pipeline [THEORETICAL]
- Durations other than 8s -- parameter accepts other values per docs but untested internally
- Image-to-video conditioning -- may be supported but not exercised
- Character consistency across shots -- unverified without reference image conditioning
- Multi-shot sequencing from a single prompt -- untested
