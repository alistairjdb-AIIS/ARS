# ElevenLabs

> AI audio generation platform providing text-to-speech, sound effects, music generation, voice design, and voice cloning via API, with its primary strength being emotionally expressive TTS via audio tags (v3 model) and physically-grounded SFX generation.

**Confidence:** HIGH
**Last compiled:** 2026-04-06
**Sources:** 1 raw file, 1 memory file

---

## Core Findings

### Capabilities

#### Complete API Surface

**Base URL:** `https://api.elevenlabs.io/v1`
**Auth:** `xi-api-key: <key>`

**Text-to-Speech (TTS):**
- `POST /v1/text-to-speech/{voice_id}` -- standard generation
- `POST /v1/text-to-speech/{voice_id}/stream` -- chunked streaming
- `/v1/text-to-speech/{voice_id}/stream-input` -- WebSocket, real-time partial text

**Sound Effects (SFX):**
- `POST /v1/sound-generation` -- text-to-sound, model `eleven_text_to_sound_v2`

**Voice Design:**
- `POST /v1/text-to-voice/design` -- generate 3 voice previews from description
- `POST /v1/text-to-voice/create` -- save a designed voice

**Voice Cloning:**
- Instant Voice Clone (IVC): 1+ minute audio, from Starter plan
- Professional Voice Clone (PVC): 30+ minutes audio, from Creator plan. PVCs NOT optimized for v3 yet -- use Multilingual v2 [VERIFIED]

**Music Generation:**
- Model: `music_v1`. Duration 3s to 5 minutes. Commercially licensed.
- Languages: English, Spanish, German, Japanese, more

**Audio Isolation:**
- `POST /v1/audio-isolation` -- removes background noise, isolates vocals

**Stem Separation:**
- Available via Music API. Separates into vocals, drums, bass, etc. High latency on long files.

**Speech-to-Text (Scribe):**
- `scribe_v2` -- 90+ languages, word-level timestamps, speaker diarization (up to 32 speakers)
- `scribe_v2_realtime` -- ~150ms latency

#### Models

| Model | ID | Languages | Char Limit | Latency | Credit Cost | Best For |
|-------|-----|-----------|------------|---------|-------------|----------|
| Eleven v3 | `eleven_v3` | 70+ | 5,000 | Higher | 1x | Emotional delivery, audio tags, dialogue, cinematic narration |
| Multilingual v2 | `eleven_multilingual_v2` | 29 | 10,000 | Medium | 1x | Polished narration, audiobooks, PVC voices |
| Flash v2.5 | `eleven_flash_v2_5` | 32 | 40,000 | ~75ms | 0.5x | Batch processing, prototyping, drafts |
| Flash v2 | `eleven_flash_v2` | English only | 30,000 | ~75ms | 0.5x | English-only fast generation |

**Decision tree:**
1. Need emotional performance or audio tags? --> **v3**
2. Need highest quality narration or using PVC? --> **Multilingual v2**
3. Need speed or doing batch work? --> **Flash v2.5**
4. Prototyping before committing credits? --> **Flash v2.5** (half credit cost)

#### TTS Voice Settings Matrix

| Parameter | Type | Default | Range | Effect |
|-----------|------|---------|-------|--------|
| `stability` | number | 0.5 | 0-1 | Lower = more emotional range; higher = more consistent |
| `similarity_boost` | number | 0.75 | 0-1 | How closely to match the original voice |
| `style` | number | 0 | 0-1 | Style exaggeration intensity |
| `speed` | number | 1.0 | 0.7-1.2 | Speech speed. Extremes degrade quality |
| `use_speaker_boost` | boolean | true | -- | Enhanced speaker similarity |

**Additional TTS parameters:** `seed` (reproducibility), `previous_text`/`next_text` (continuity), `previous_request_ids`/`next_request_ids` (max 3, for chaining), `language_code` (ISO 639-1), `apply_text_normalization`, `pronunciation_dictionary_locators` (max 3)

**Output formats:**
- MP3: `mp3_22050_32`, `mp3_44100_64`, `mp3_44100_128` (production), `mp3_44100_192` (master)
- PCM: `pcm_16000` through `pcm_48000` (post-processing pipelines)
- WAV: `wav_44100`, `wav_48000` (editing software)
- Opus: `opus_48000_64` through `opus_48000_192` (streaming)

#### Eleven v3 Audio Tags [VERIFIED]

Audio tags in square brackets control delivery. They affect all subsequent text until a new tag appears.

**Emotional:** `[sad]`, `[angry]`, `[happy]`, `[excited]`, `[nervous]`, `[frustrated]`, `[tired]`, `[sorrowful]`, `[curious]`, `[sarcastic]`, `[mischievous]`, `[flustered]`, `[casual]`, `[annoyed]`

**Delivery:** `[whispers]`, `[shouts]`, `[pause]`, `[rushed]`, `[stammers]`, `[drawn out]`, `[fast-paced]`, `[hesitates]`

**Reactions/SFX:** `[laughs]`, `[sighs]`, `[clears throat]`, `[snorts]`, `[crying]`, `[gulps]`, `[swallows]`, `[gunshot]`, `[applause]`, `[explosion]`, `[clapping]`

**Character/Voice:** `[pirate voice]`, `[robotic tone]`, `[childlike tone]`, `[deep voice]`

**Accents:** `[French accent]`, `[Australian accent]`, `[Southern US accent]`, `[strong X accent]`

**Syntax rules:**
- Case-insensitive but lowercase recommended
- Tags persist until replaced by another tag
- ALL CAPS = emphasis on specific words
- Ellipsis (...) = pauses and weight
- Match tags to voice character -- a serious voice won't respond well to `[giggles]` [VERIFIED]

#### SFX Parameters

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `text` | string | required | -- | Descriptive prompt |
| `duration_seconds` | number | null (auto) | 0.5-30 | Auto = 200 credits flat; manual = 40 credits/s |
| `prompt_influence` | number | 0.3 | 0-1 | Higher = stricter adherence |
| `loop` | boolean | false | -- | Creates seamless looping audio |

**Credit math:** Auto duration = 200 credits regardless of length. Manual = 40/s. Break-even is 5 seconds. Use auto for 5+ seconds (cheaper). Use manual only for short impacts under 5 seconds. [VERIFIED]

#### Pricing

| Plan | Price | Credits | ~Minutes TTS | Commercial | Voice Cloning |
|------|-------|---------|-------------|------------|---------------|
| Free | $0 | 10,000 | ~10 min | No | No |
| Starter | $5/mo | 30,000 | ~30 min | Yes | IVC only |
| Creator | $22/mo | 100,000 | ~100 min | Yes | IVC + PVC |
| Pro | $99/mo | 500,000 | ~500 min | Yes | IVC + PVC |
| Scale | $330/mo | Millions | Hundreds of hrs | Yes | IVC + PVC |

**Overage rates:** Creator $0.30/1K chars, Pro $0.24/1K chars, Scale $0.18/1K chars

**Cost per 30s Reel (estimated):** ~1,500-2,000 credits on v3, ~1,000-1,500 on Flash [THEORETICAL -- calculated, not measured from production]

### Prompt Patterns

#### SFX Prompt Structure [VERIFIED]

`[Material/Source] + [Action/Behavior] + [Environment/Space] + [Temporal Arc]`

**Good prompts (specific, spatial, temporal):**
- "Heavy wooden door creaking open slowly in a stone cathedral, with echo"
- "Rain hitting a tin roof, building from light drizzle to heavy downpour over 10 seconds"
- "Sizzling bacon in a cast iron pan, close-mic, kitchen ambience"
- "Cinematic braam, horror, deep bass with metallic overtone"

**Bad prompts (vague):**
- "Door sound" / "Nature" / "Scary sound"

**Prompt parameters that matter:**
1. Material and size ("heavy metal" vs "light wooden" vs "glass")
2. Distance and space ("close-mic" vs "in a large cathedral")
3. Temporal arc ("starts quietly and builds to a crash" vs "sudden sharp impact")
4. Acoustic environment ("dry studio" vs "reverberant hallway")
5. Onomatopoeia ("whoosh," "crackle," "thud" alongside descriptions)
6. Audio terminology (model understands "braam," "glitch," "drone," "stem," "one-shot," "loop")

**Duration strategy:**
- 1-3s: impacts, hits, transitions, UI sounds
- 3-8s: footsteps, mechanical actions, short ambiences
- 8-15s: atmospheric backgrounds, musical loops
- 15-30s: extended ambiences, complex sequences
- Use `loop: true` for indefinite backgrounds

**Prompt influence settings:**
- 0.1-0.3: Creative, exploratory
- 0.3-0.5: Balanced default
- 0.7-1.0: Strict adherence

#### Layering Strategy [VERIFIED]

The model generates single sound events well but struggles with multi-layer scenes. Always layer multiple generations:
1. Generate atmosphere/ambience as one layer
2. Generate foreground action sounds separately
3. Generate musical/tonal elements separately
4. Mix in post with ffmpeg or audio editor

### Operational Patterns

**Integration pipeline for video work:**
1. Generate TTS segments (save as WAV/PCM for editing)
2. Generate SFX layers
3. Generate music bed (if needed)
4. Combine with ffmpeg using `adelay` for timing offsets and `amix` for layering
5. Or integrate in Remotion using `<Audio>` components with `startFrom`/`volume`

**Timing precision:**
- Use `seed` parameter for reproducible outputs when iterating
- Generate audio first, then build animation to match audio duration [VERIFIED -- this is the recommended order]
- Use Scribe (STT) for word-level timestamps to align visual beats

**German language support:**
- Supported on v3, Multilingual v2, and Flash v2.5
- Use `language_code: "de"` to force German processing
- Create pronunciation dictionaries for medical/technical terms
- Number/date normalization may need manual intervention for German formats [VERIFIED]

### Quality Assessment

**Where ElevenLabs excels:**
- Emotionally expressive narration via v3 audio tags (biggest differentiator) [VERIFIED]
- Physically-grounded SFX from specific prompts [VERIFIED]
- German TTS with natural prosody [VERIFIED]
- Voice design from text descriptions [VERIFIED]
- Commercially licensed music generation [VERIFIED]

**Where ElevenLabs fails:**
- Failed generations still cost credits [VERIFIED]
- PVC on v3 is degraded -- use Multilingual v2 for PVC work [VERIFIED]
- Complex multi-element SFX prompts produce "mud" [VERIFIED]
- Non-English number/date handling unreliable [VERIFIED]
- Long-form v3 capped at 5,000 chars per request [VERIFIED]
- 10 service incidents in a 28-day window (Feb 2026) [VERIFIED]
- Emotional mismatch: serious voice rejects playful tags [VERIFIED]
- Accent contamination across multilingual generations [VERIFIED]

---

## Craft Principles (from Film Sound Design Research)

### Murch's Rule of 2.5 [VERIFIED from research]
The audience processes only ~2.5 sonic elements at any moment. Beyond that, sounds congeal into noise. At any moment in a mix, ONE element must dominate.

**Mix hierarchy for Reels:**
- Narration segment: voice 100%, music 15%, SFX 0%
- Transition: SFX 100%, music 30%, voice 0%
- Reveal: single impact SFX 100%, then silence

### Organic Grounding [VERIFIED from research]
Describe physical reality in SFX prompts, not abstract concepts. "Metal tray sliding on marble counter in a quiet clinic" activates richer generation than "medical transition sound." The model was trained on real-world recordings.

### Contrast Creates Perception [VERIFIED from research]
Structure audio as a contrast sequence:
1. Hook (0-3s): attention-grabbing sound
2. Build (3-15s): increasing density, rising pitch/tempo
3. Drop (15-16s): brief silence (0.5-1.0s)
4. Reveal (16-20s): layered, rich payoff
5. Resolve (20-30s): simplicity, voice, brand signature

### Frequency Spectrum Filling [VERIFIED from research]
Layer SFX across frequency bands:
- Low (20-200Hz): bass rumbles, deep whooshes
- Mid (200Hz-2kHz): voice, most SFX, music melody
- High (2kHz-20kHz): sizzle, sparkle, shimmer, clicks

### Silence as Impact [VERIFIED from research]
1-2 seconds of near-silence before a key reveal moment amplifies it. Counterintuitive for social media but effective.

### Sonic Branding [VERIFIED from research]
Establish 2-3 signature sounds and use them in every piece of content:
- Intro signature: 1-2s (brand recognition)
- Transition sound: consistent before/after (transformation)
- Outro signature: 2-3s (like Netflix ta-dum)

After 20+ uses, these sounds carry brand association. Sonic logos trigger emotional responses 86% faster than visual logos.

---

## Operational Rules

- **When choosing a model,** use v3 for emotional narration with audio tags, Multilingual v2 for long-form or PVC voices, Flash v2.5 for drafts/batch work, because model selection is the single biggest quality and cost lever. [VERIFIED]
- **When generating SFX,** describe physical reality (material + action + space + temporal arc), because organic grounding activates the model's real-world training data. [VERIFIED]
- **When SFX duration is 5+ seconds,** use auto duration (200 credits flat), because manual duration costs 40 credits/second and is more expensive past the 5s break-even. [VERIFIED]
- **When mixing audio layers,** ensure only ONE element dominates at any moment (Murch's Rule of 2.5), because the brain cannot track more than ~2.5 competing sonic elements. [VERIFIED]
- **When building Reels audio,** generate audio first and build animation to match, because audio-first workflow produces better sync than bolting audio onto silent video. [VERIFIED]
- **When generating German content,** set `language_code: "de"` and create pronunciation dictionaries for medical/technical terms, because default handling mispronounces numbers, dates, and specialized terminology. [VERIFIED]
- **When budgeting credits,** plan for 2-3x theoretical cost, because failed generations still consume credits. [VERIFIED]
- **When using PVC voices,** use Multilingual v2 (not v3), because PVC is degraded on v3 as of April 2026. [VERIFIED]
- **When building complex soundscapes,** layer individual SFX generations rather than prompting for multi-element scenes, because single-prompt complexity produces "mud." [VERIFIED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `tools/research-data/elevenlabs_sound_design_research.md` | Complete API surface, models, audio tags, SFX prompt engineering, pricing, German language support, film sound design craft, mixing patterns, operational checklists |
| `credentials.md` (memory) | Auth pattern, plan tier (Pro/500K credits), voice IDs, model IDs |

---

## Related Concepts

- [[veo-3-1]] -- Veo generates joint audio with video; ElevenLabs is the supplementary/replacement audio layer when more control is needed
- [[kling-ai]] -- Kling generates silent video; ElevenLabs provides all audio
- [[recraft-v4]] -- Static frames for Reels; ElevenLabs provides the audio layer

---

## Open Questions

- v3 German quality with dermatological terminology -- general reviews positive, but not tested with specialized medical German [THEORETICAL]
- Credit cost per Reel in production -- calculated from rates, may be 2-3x due to failed generations [THEORETICAL]
- Sonic branding compound effect on social media -- extrapolated from traditional media research, untested in short-form context [THEORETICAL]
- Music API credit costs -- not fully documented [THEORETICAL]
- Silence effectiveness on Instagram -- cinema research supports it, but autoplay-with-sound-off may make silence indistinguishable from "no audio" [THEORETICAL]
