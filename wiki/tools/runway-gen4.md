# Runway Gen-4 / Gen-4.5

> Runway's video generation models — Gen-4 Turbo (image-to-video, cheapest), Gen-4.5 (text-to-video + image-to-video, A2D hybrid architecture), and Gen-4 Aleph (video-to-video). Runway's differentiator is character consistency via reference images; its weakness is photoreal human face quality per frame.

**Confidence:** MEDIUM (API mechanics VERIFIED from docs; quality assessment from community reports, not internal A/B testing)
**Last compiled:** 2026-04-07
**Sources:** Runway API docs, Curious Refuge Labs review, practitioner guides, Prompt-A-Video research paper, cross-tool comparison analyses

---

## Core Findings

### API Mechanics

**Authentication:** [VERIFIED-docs]
- Bearer token: `Authorization: Bearer $RUNWAYML_API_SECRET`
- Required header: `X-Runway-Version: 2024-11-06`
- Base URL: `https://api.dev.runwayml.com/v1`
- SDKs: Python (`runwayml`), Node.js (`@runwayml/sdk`)

**Important:** Load API secret from env var. Never hardcode. [Standing rule — see [[feedback-never-hardcode-secrets]]]

**Endpoints:** [VERIFIED-docs]

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/image_to_video` | POST | Image-to-video (all models) |
| `/v1/text_to_video` | POST | Text-to-video (Gen-4.5 only) |
| `/v1/tasks/{id}` | GET | Poll task status |
| `/v1/tasks/{id}` | DELETE | Cancel/delete task |
| `/v1/uploads` | POST | Upload large files (up to 200MB) |

**Model Identifiers (exact strings for API):** [VERIFIED-docs]

| Model String | Input | Credits/sec | Cost/sec |
|-------------|-------|-------------|----------|
| `gen4_turbo` | Image REQUIRED | 5 | $0.05 |
| `gen4.5` | Text and/or Image | 12 | $0.12 |
| `gen4_aleph` | Video + Text/Image | 15 | $0.15 |

Credits cost $0.01 per credit. [VERIFIED-docs]

**Critical capability gate:** [VERIFIED-docs]

| Model | Text-to-Video | Image-to-Video |
|-------|:------------:|:--------------:|
| `gen4.5` | YES | YES |
| `gen4_turbo` | NO — image REQUIRED | YES |
| `gen4_aleph` | NO | YES (video input) |

Gen-4 Turbo cannot generate from text alone. If you want text-only generation on Runway, you must use Gen-4.5 at 2.4x the cost.

**Parameters:** [VERIFIED-docs]

| Parameter | Type | Values | Notes |
|-----------|------|--------|-------|
| `model` | string | See above | Required |
| `promptText` | string | Max ~1000 chars | Text prompt |
| `promptImage` | string | HTTPS URL or base64 data URI | Optional for gen4.5, REQUIRED for gen4_turbo |
| `duration` | integer | 2-10 seconds | Default: 5 |
| `ratio` | string | e.g. `"1280:720"` | Model-dependent |
| `seed` | integer | 0-4294967295 | Reproducibility |
| `webhookUrl` | string | HTTPS URL | Async notification |

**Aspect ratios:** [VERIFIED-docs]
- Gen-4.5 text-to-video: `1280:720`, `720:1280` only (limited)
- Gen-4.5 image-to-video: `1280:720`, `1584:672`, `1104:832`, `720:1280`, `832:1104`, `672:1584`, `960:960`
- Gen-4 Turbo: `1280:720`, `1584:672`, `1104:832`, `720:1280`, `832:1104`, `960:960`

**Async workflow:** All generation is async. POST creates a task, returns task ID. Poll `GET /v1/tasks/{id}` until status is `completed`, or use SDK's `wait_for_task_output()`. [VERIFIED-docs]

**Python example:**
```python
import os
from runwayml import RunwayML

client = RunwayML(api_key=os.environ["RUNWAYML_API_SECRET"])

# Text-to-video (Gen-4.5 only)
task = client.text_to_video.create(
    model="gen4.5",
    prompt_text="...",
    duration=10,
    ratio="1280:720"
)

# Image-to-video (Gen-4 Turbo or Gen-4.5)
task = client.image_to_video.create(
    model="gen4_turbo",
    prompt_image="https://...",  # or base64 data URI
    prompt_text="...",
    duration=10,
    ratio="1280:720"
)

# Poll for completion
result = client.tasks.retrieve(task.id)
# or use: client.wait_for_task_output(task.id)
```

### Runway Also Hosts Veo

Runway's API provides access to Google Veo models at higher cost: [VERIFIED-docs]

| Model | Credits/sec | Cost/sec |
|-------|-------------|----------|
| `veo3.1` (no audio) | 20 | $0.20 |
| `veo3.1` (with audio) | 40 | $0.40 |
| `veo3` | 40 | $0.40 |

This means you can use Runway as a single API gateway for both Runway-native and Veo models.

### Prompt Dialect

**Runway speaks a different prompt language than Kling or Veo.** This is the most important operational finding. [VERIFIED-community + research]

Prompts do NOT transfer between tools. Each model responds to different vocabulary and structure:

| Tool | Dialect | Best Structure |
|------|---------|---------------|
| **Runway** | Force/physics prose | Character action > environmental interaction > camera > visual mood |
| **Kling** | Action/timeline | Beat-marked sequences (0-4s, 4-8s), concrete physical actions |
| **Veo** | Structured/data-like | Shot-list format, technical specs, sensory detail |

**Runway-specific patterns:** [VERIFIED-community]

1. **Keep it simple.** One action per sentence. Short, clear descriptions. 2-4 sentences covering scene, camera, motion, pacing.
2. **Force-reaction language.** Emphasize momentum, resistance, impact rather than pure appearance. "She stumbles back, catching herself on the doorframe" not "a woman near a door."
3. **Show, don't tell emotion.** "Slowly lowers their head, eyes welling with tears" not "the character is sad."
4. **Specific verbs.** "Sprints," "glides," "leaps" over "moves" or "goes."
5. **Do NOT re-describe the reference image.** If using image-to-video, describe only what CHANGES. Re-describing visible elements causes reduced motion or unexpected results.

**What transfers from Kling/Veo:**
- Basic camera terminology (dolly, pan, track) — works
- Subject descriptions (age, clothing, position) — universal
- Film aesthetic keywords ("35mm film grain," "golden hour") — works

**What does NOT transfer:**
- Acting-chain beat structure (Kling's strength) — Runway doesn't process the same way
- Lens specs in technical format (Veo's JSON-like approach) — Runway prefers prose
- Timeline/beat markers (Kling's `0-4s` structure) — not how Runway works

### Quality Modifiers Suppress Motion

**Research-backed finding (Prompt-A-Video, NeurIPS):** Image-derived quality descriptors ("cinematic," "photorealistic," "8K detailed") applied to video prompts actively reduce motion magnitude. Quality modifiers compete with motion descriptors for model attention. [VERIFIED-research]

This applies to ALL video models, not just Runway:
- Every word spent on aesthetic descriptors is attention not spent on motion
- "Cinematic" may be interpreted as "slow/stable" rather than "high quality"
- Strip image-derived quality modifiers. Replace with motion-specific language.

**Instead of:** "Cinematic 8K detailed photorealistic"
**Use:** "Steady tracking shot" (achieves cinematic feel while preserving motion)

### Photoreal Human Quality

**Runway Gen-4 is weak for photoreal human faces.** [VERIFIED-community, multiple independent sources]

Curious Refuge Labs rated Gen-4:
- Overall: **4.3/10**
- Cinematic realism: **3.3/10**
- Worst cases described as "poorly done CGI from 2010"

**Specific failure modes:** [VERIFIED-community]
- Face details "fall apart" after the first 2 seconds
- Hands render as "blobs" rather than distinct fingers
- Group scenes with multiple people degrade into "blobs of colors"
- Unwanted slow-motion rendering occurs without prompting
- Characters "improvise" — turning wrong way, adding unrequested actions
- Flickering "nearly guaranteed" in dynamic scenes
- Significant gap between Runway's marketing demos and actual user results

**Gen-4.5 improves** on temporal consistency, prompt comprehension, and human motion realism — but the core face-degradation issues persist, just less severely. [VERIFIED-community]

**Ranking for photoreal humans (community consensus):** [VERIFIED-community]
1. **Kling v3** — best single-shot face quality and temporal consistency
2. **Veo 3.1** — highest visual fidelity overall
3. **Runway Gen-4.5** — best character consistency across shots, weaker per-frame face quality
4. **Runway Gen-4 Turbo** — cheapest, noticeably lower quality

### Architecture: A2D Hybrid

Gen-4.5 uses an Autoregressive-to-Diffusion (A2D) hybrid architecture, adapted from Qwen2.5-VL. [VERIFIED-community]

**What this means operationally:**
- The autoregressive component provides language-model-grade scene understanding (multi-element composition, cause-effect, narrative logic)
- The diffusion component handles pixel-level fidelity
- Good at *composing complex scenes with humans* (spatial reasoning, multiple characters)
- Face identity preservation comes through the reference embedding pipeline, not the core architecture
- This is why Runway needs reference images to match Kling's text-to-video face quality

### Reference Image Workflow

This is Runway's actual strength — character consistency across shots via reference images. [VERIFIED-community + docs]

**What makes a good reference image:** [VERIFIED-docs + community]
1. Well-lit, simple background (busy backgrounds bleed into generation)
2. Clear face visibility (single photo establishes face, build, attire)
3. High resolution ("quality of input image is critical")
4. Supported formats: JPEG, PNG, WebP (not GIF). Max 16MB via URL, 5MB via base64

**Multi-reference workflow:** [VERIFIED-community]
- Up to 3 reference images supported
- Use contextual bridging: "The same person from reference 1 now in the environment from reference 2"
- Pair character reference with style-defining image for visual language consistency

**Critical rules:** [VERIFIED-community]
- DO use anchoring phrases: "same character," "maintaining appearance," "exact features"
- DO let references handle identity; use prompts only for narrative direction
- DO NOT re-describe features already visible in the reference (causes reduced motion)
- DO NOT request conflicting changes (different hair color + "maintaining reference")

**Architecture note:** Runway's reference conditioning is central to its human generation quality — unlike Kling, whose face quality comes from training data (Kuaishou's billions of human performance clips), Runway extracts identity from the provided image at inference time. Without reference images, Runway's human generation quality drops significantly. [VERIFIED-community + THEORETICAL architecture inference]

### Content Moderation

[VERIFIED-docs]
- Input text and images screened before generation. Outputs also screened.
- **SAFETY.INPUT failures: credits are NOT refunded.** Retrying not recommended.
- Named public figures blocked (same as anime finding — Runway blocks real names)
- Logos/watermarks in source images trigger `INTERNAL.BAD_OUTPUT` failures
- Meta-prompts ("write a prompt for...") cause failures
- Explicit text generation requests in prompts cause failures

### Pricing Strategy

**Two-tier workflow for photoreal:** [VERIFIED-community]

| Phase | Model | Cost/10s | Use |
|-------|-------|----------|-----|
| Iteration/drafts | `gen4_turbo` | $0.50 | Requires reference image. Fast (~30s generation). Test compositions. |
| Finals | `gen4.5` | $1.20 | Text-to-video available. Higher temporal consistency. |
| Best quality | `veo3.1` (via Runway) | $2.00-4.00 | Highest photoreal quality but 4-8x cost. |

---

## Operational Rules

1. **When generating photoreal humans on Runway,** provide a high-quality reference image, because Runway's face quality without reference is significantly weaker than Kling's text-to-video. [VERIFIED-community]

2. **When writing Runway prompts,** use force/physics language and short prose (2-4 sentences), because Runway's prompt dialect differs from Kling/Veo and over-specification suppresses motion. [VERIFIED-community + research]

3. **When doing image-to-video,** do NOT re-describe what is visible in the reference image, because this causes reduced motion or unexpected results. Describe only what CHANGES. [VERIFIED-docs + community]

4. **When choosing between Gen-4 Turbo and Gen-4.5,** use Gen-4 Turbo ($0.05/s) for reference-image iteration and Gen-4.5 ($0.12/s) for text-to-video or final quality, because Gen-4 Turbo cannot do text-to-video. [VERIFIED-docs]

5. **When comparing Runway output to Kling/Veo,** use tool-optimized prompts (same intent, different syntax), because identical prompts systematically disadvantage whichever model's dialect is most different. [VERIFIED-research]

6. **When stripping quality modifiers,** remove "cinematic," "photorealistic," "8K," "detailed" from video prompts, because image-derived quality descriptors suppress motion magnitude. Replace with motion-specific language. [VERIFIED-research]

7. **When authenticating,** use `RUNWAYML_API_SECRET` env var with Bearer auth and `X-Runway-Version: 2024-11-06` header. [VERIFIED-docs]

8. **When testing for character consistency across shots,** use Runway with reference images — this is its strength over Kling (which generates independently per clip) and Veo. [VERIFIED-community]

9. **When a generation fails with SAFETY.INPUT,** do NOT retry — credits are not refunded. Rephrase the prompt significantly. [VERIFIED-docs]

---

## Deep Reference

- **When** writing Runway prompts for photoreal → **read** this article §Prompt Dialect **for** force/physics language patterns, what transfers from Kling/Veo, what doesn't
- **When** choosing between Runway models → **read** this article §Pricing Strategy **for** two-tier iteration workflow and capability gates
- **When** preparing reference images → **read** this article §Reference Image Workflow **for** quality requirements, multi-reference bridging, do's and don'ts
- **When** comparing across tools → **read** [[photoreal]] §Tool Selection **for** per-tool strengths + the prompt-dialect translation requirement
- **When** crafting acting chains for Runway → **read** [[acting-chains-beat-camera]] **for** core principles (they apply) but note Runway processes them as prose, not beat-marked timelines

---

## Related Concepts

- [[kling-ai]] — Outperforms Runway for per-frame face quality without reference images. Kling's 3D VAE architecture encodes spatiotemporal trajectories; Runway relies on reference conditioning.
- [[veo-3-1]] — Higher raw photoreal quality. Available through Runway's API at 2-4x cost. Joint audio generation is unique advantage.
- [[photoreal]] — Register-level prompting patterns (imperfection prompting, narrative coherence, too-perfect veto) apply regardless of tool.
- [[acting-chains-beat-camera]] — Core acting-chain principles transfer to Runway, but format must be adapted to prose (not beat-marked timeline).
- [[prompting-craft-depth]] — Quality-modifier-suppresses-motion finding changes how craft depth is applied across all tools.

---

## Open Questions

- Does Gen-4.5 text-to-video match Kling for photoreal human faces? No internal A/B test yet. [UNKNOWN — this is the test we're about to run]
- Does Gen-4 Turbo's reference-image workflow produce better face consistency than Kling 3.0 Elements? [UNKNOWN]
- What is the actual moderation boundary for medical/dermatological content? [UNKNOWN — relevant for DermaMedicum]
- Does reference-image consistency hold across chains of 10+ clips for multi-scene storytelling? [UNKNOWN]
- Does the A2D architecture's autoregressive component actually improve narrative logic in generated video, or is this marketing? [UNKNOWN]
- Exact rate limits and quota system for API usage. [UNKNOWN]

---

## Source Files

| File | Contribution |
|------|-------------|
| Runway API Documentation (docs.dev.runwayml.com) | API mechanics, endpoints, parameters, pricing, moderation, model identifiers |
| Curious Refuge Labs Gen-4 Review | 4.3/10 quality rating, face degradation after 2s, marketing vs reality gap |
| Prompt-A-Video (arXiv 2412.15156) | Quality modifiers suppress motion, model-specific prompt optimization required |
| Cross-tool prompting analysis (CreativeAI Ninja) | Runway force-language dialect, Kling timeline dialect, Veo structured dialect |
| ImagineArt reference image guide | Multi-reference workflow, anchoring phrases, do's/don'ts |
| credentials.md (memory) | API key location |
