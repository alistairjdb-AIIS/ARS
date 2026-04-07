# ElevenLabs + Sound Design: Operational Research

**Last verified:** April 2026
**Consumer:** Agent on any task requiring audio — Reels, brand films, product demos, animated content
**Decision:** How to produce audio (TTS, SFX, music) via ElevenLabs API and how to apply sound design craft to elevate the output

---

## LAYER 1: TOOL MASTERY

### 1. Complete API Surface

#### Text-to-Speech (TTS)
**Endpoint:** `POST /v1/text-to-speech/{voice_id}`

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `text` | string | required | — | Content to speak |
| `model_id` | string | `eleven_multilingual_v2` | See models table | Choose per use case |
| `voice_settings.stability` | number | 0.5 | 0–1 | Lower = more emotional range; higher = more consistent |
| `voice_settings.similarity_boost` | number | 0.75 | 0–1 | How closely to match the original voice |
| `voice_settings.style` | number | 0 | 0–1 | Style exaggeration intensity |
| `voice_settings.speed` | number | 1.0 | 0.7–1.2 | Speech speed. Extremes degrade quality |
| `voice_settings.use_speaker_boost` | boolean | true | — | Enhanced speaker similarity |
| `output_format` | string | `mp3_44100_128` | See formats | Codec_samplerate_bitrate |
| `seed` | integer | null | 0–4294967295 | Same seed + same input = same output |
| `previous_text` / `next_text` | string | null | — | Context for continuity between segments |
| `previous_request_ids` / `next_request_ids` | array | null | max 3 | Request chaining for consistent long-form |
| `language_code` | string | null | ISO 639-1 | Force specific language |
| `apply_text_normalization` | string | `auto` | auto/on/off | Number/date reading |
| `pronunciation_dictionary_locators` | array | null | max 3 | Custom pronunciation rules |

**Streaming:** `POST /v1/text-to-speech/{voice_id}/stream` — same params, returns chunked audio
**WebSocket:** `/v1/text-to-speech/{voice_id}/stream-input` — real-time partial text input

**Output Formats:**
- MP3: `mp3_22050_32`, `mp3_44100_64`, `mp3_44100_128`, `mp3_44100_192` (use 128 for production, 192 for master quality)
- PCM: `pcm_16000` through `pcm_48000` (for post-processing pipelines)
- WAV: `wav_44100`, `wav_48000` (for editing software)
- Opus: `opus_48000_64` through `opus_48000_192` (for streaming)

#### Sound Effects (SFX)
**Endpoint:** `POST /v1/sound-generation`

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `text` | string | required | — | Descriptive prompt for the sound |
| `model_id` | string | `eleven_text_to_sound_v2` | — | Only v2 available |
| `duration_seconds` | number | null (auto) | 0.5–30 | Auto = 200 credits flat; manual = 40 credits/second |
| `prompt_influence` | number | 0.3 | 0–1 | Higher = stricter adherence to prompt |
| `loop` | boolean | false | — | Creates seamless looping audio (v2 only) |

**Credit math for SFX:**
- Auto duration: 200 credits per generation (regardless of length)
- Manual duration: 40 credits/second (so a 5s effect = 200 credits, same as auto)
- Manual becomes cheaper only for effects < 5s
- For effects > 5s, manual costs MORE (e.g., 10s = 400 credits vs 200 auto)
- **Optimization:** Use auto duration for anything 5+ seconds. Use manual only for short impacts (< 5s) where you need precise length.

#### Voice Design
**Endpoint:** `POST /v1/text-to-voice/design`

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `voice_description` | string | required | 20–1000 chars. Describe age, accent, tone, pacing, quality |
| `model_id` | string | `eleven_multilingual_ttv_v2` | Also: `eleven_ttv_v3` |
| `text` | string | null | 100–1000 chars preview text |
| `auto_generate_text` | boolean | false | Let AI pick preview text |
| `guidance_scale` | number | 5 | Lower = more creative; higher = stricter. High values risk artificial sound |
| `loudness` | number | 0.5 | -1 to 1. 0 = ~-24 LUFS |
| `seed` | integer | null | Reproducibility |
| `should_enhance` | boolean | false | AI expands simple descriptions into detailed ones |
| `quality` | number | null | Higher quality = less variety |
| `reference_audio_base64` | string | null | v3 model only — reference audio sample |
| `prompt_strength` | number | null | 0–1, v3 only — balance prompt vs reference |

**Returns:** 3 voice previews, each with `generated_voice_id` + base64 audio sample.

**Save a designed voice:** `POST /v1/text-to-voice/create` with the `generated_voice_id`.

#### Voice Cloning

**Instant Voice Clone (IVC):**
- Needs 1+ minute of audio
- Available from Starter plan
- Uses conditioning signal at inference time (not fine-tuned)
- Less consistent when asked to express emotions different from reference
- Good for: quick prototyping, variety

**Professional Voice Clone (PVC):**
- Needs 30+ minutes of high-quality recordings
- Available from Creator plan
- Actually fine-tunes model parameters on your voice
- Much higher consistency and emotional range
- **Warning:** PVCs are NOT fully optimized for Eleven v3 yet (as of April 2026). Use Multilingual v2 for PVC work.

#### Music Generation
**Endpoint:** Available via API (paid subscribers)
- Model: `music_v1`
- Duration: 3 seconds to 5 minutes
- Output: MP3 (44.1kHz, 128-192kbps) or WAV
- Parameters: `seed`, `loudness`, `quality`, `guidance_scale`, `music_length_ms`
- Supports vocals or instrumental only
- Languages: English, Spanish, German, Japanese, and more
- **Commercially licensed** — cleared for film, TV, podcasts, social media, ads, gaming

#### Audio Isolation (Voice Isolator)
**Endpoint:** `POST /v1/audio-isolation`
- Removes background noise, isolates vocals
- Input: multipart form with audio file
- Streaming variant available
- Not optimized for isolating vocals from music specifically

#### Stem Separation
**Endpoint:** Available via Music API
- Separates audio into individual stems (vocals, drums, bass, etc.)
- Warning: High latency for long files

#### Speech-to-Text (Scribe)
- Model: `scribe_v2` — 90+ languages, word-level timestamps, speaker diarization (up to 32 speakers)
- Realtime: `scribe_v2_realtime` — ~150ms latency
- **Use case for agent:** Transcribe existing video narration for timing reference before generating replacement audio

### 2. Models: When to Use What

| Model | ID | Languages | Char Limit | Latency | Cost | Best For |
|-------|-----|-----------|------------|---------|------|----------|
| **Eleven v3** | `eleven_v3` | 70+ | 5,000 | Higher | 1x | Emotional delivery, audio tags, character dialogue, cinematic narration |
| **Multilingual v2** | `eleven_multilingual_v2` | 29 | 10,000 | Medium | 1x | Polished narration, audiobooks, professional voiceover, PVC voices |
| **Flash v2.5** | `eleven_flash_v2_5` | 32 | 40,000 | ~75ms | 0.5x | Batch processing, prototyping, drafts, real-time apps |
| **Flash v2** | `eleven_flash_v2` | English only | 30,000 | ~75ms | 0.5x | English-only fast generation |

**Decision tree:**
1. Need emotional performance or audio tags? -> **v3**
2. Need highest quality narration or using PVC? -> **Multilingual v2**
3. Need speed or doing batch work? -> **Flash v2.5**
4. Prototyping before committing credits? -> **Flash v2.5** (half the credit cost)

### 3. Eleven v3 Audio Tags — Complete Reference

Audio tags are words in square brackets that v3 interprets for delivery control. They affect all subsequent text until a new tag appears.

**Emotional:**
`[sad]`, `[angry]`, `[happy]`, `[excited]`, `[nervous]`, `[frustrated]`, `[tired]`, `[sorrowful]`, `[curious]`, `[sarcastic]`, `[mischievous]`, `[flustered]`, `[casual]`, `[annoyed]`

**Delivery:**
`[whispers]`, `[shouts]`, `[pause]`, `[rushed]`, `[stammers]`, `[drawn out]`, `[fast-paced]`, `[hesitates]`

**Reactions/SFX:**
`[laughs]`, `[sighs]`, `[clears throat]`, `[snorts]`, `[crying]`, `[gulps]`, `[swallows]`
`[gunshot]`, `[applause]`, `[explosion]`, `[clapping]`

**Character/Voice:**
`[pirate voice]`, `[robotic tone]`, `[childlike tone]`, `[deep voice]`

**Accents:**
`[French accent]`, `[Australian accent]`, `[Southern US accent]`, `[strong X accent]`

**Experimental:**
`[sings]`, `[woo]`

**Syntax rules:**
- Case-insensitive (`[happy]` = `[HAPPY]`), but lowercase recommended
- Tags persist until replaced by another tag
- Combine with punctuation: `"It was a VERY long day [sigh] ... nobody listens anymore"`
- ALL CAPS = emphasis on specific words
- Ellipsis (...) = pauses and weight
- Match tags to voice character — a serious voice won't respond well to `[giggles]`

**What changes:** Audio tags are the single biggest differentiator of v3. They turn flat narration into performance. For Reels narration, this means you can script emotional beats directly into the text.

### 4. Sound Effects Prompt Engineering

#### What makes a good SFX prompt

**Structure:** [Material/Source] + [Action/Behavior] + [Environment/Space] + [Temporal Arc]

**Good prompts (specific, spatial, temporal):**
- "Heavy wooden door creaking open slowly in a stone cathedral, with echo"
- "Rain hitting a tin roof, building from light drizzle to heavy downpour over 10 seconds"
- "Old mechanical typewriter, rapid keystrokes with carriage return bell"
- "Sizzling bacon in a cast iron pan, close-mic, kitchen ambience"
- "Cinematic braam, horror, deep bass with metallic overtone"

**Bad prompts (vague, no spatial/temporal info):**
- "Door sound" (which door? what material? opening or closing? what room?)
- "Nature" (too broad, no specificity)
- "Scary sound" (no physical grounding)

#### Prompt parameters that matter

1. **Material and size:** "Heavy metal" vs "light wooden" vs "glass"
2. **Distance and space:** "Close-mic" vs "in a large cathedral" vs "from across a parking lot"
3. **Temporal arc:** "Starts quietly and builds to a crash" vs "sudden sharp impact"
4. **Acoustic environment:** "Dry studio recording" vs "reverberant hallway" vs "outdoors with wind"
5. **Onomatopoeia:** Adding "whoosh," "crackle," "thud" alongside descriptions helps
6. **Audio terminology:** The model understands "braam," "glitch," "drone," "stem," "one-shot," "loop"

#### Duration strategy
- 1–3 seconds: impacts, hits, transitions, UI sounds
- 3–8 seconds: footsteps sequences, mechanical actions, short ambiences
- 8–15 seconds: atmospheric backgrounds, musical loops
- 15–30 seconds: extended ambiences, complex sequences
- Use `loop: true` for backgrounds that need to play indefinitely

#### Prompt influence settings
- **0.1–0.3 (low):** More creative, unexpected variations. Good for exploring.
- **0.3–0.5 (medium):** Balanced. Good default for most work.
- **0.7–1.0 (high):** Strict adherence. Use when you know exactly what you want.

#### Layering strategy (critical for production quality)
The model generates single sound events well but struggles with complex multi-layer scenes. **Always layer multiple generations:**
1. Generate atmosphere/ambience as one layer
2. Generate foreground action sounds separately
3. Generate any musical/tonal elements separately
4. Mix in post with ffmpeg or audio editor

This mirrors how professional sound designers work — no single recording captures a scene. Every scene is built from layers.

### 5. German Language (DermaMedicum)

**Model support:**
- Multilingual v2: German supported, 29 languages total
- Flash v2.5: German supported, 32 languages
- v3: German supported, 70+ languages

**Quality assessment:**
- German TTS quality is strong. Reviewers report natural prosody and good pronunciation.
- Available voices include "Rick" (warm, neutral German accent) and regional variants (Bavarian, Austrian-German).
- Voice Library has German voices available.
- v3 supports `[German accent]` audio tag for accent control.

**Known issues:**
- Accent bleeding: when switching from another language/accent, traces of the previous accent may persist
- Number/date normalization may need manual intervention for German formats (e.g., "14.03.2026" vs "March 14, 2026")
- Use `language_code: "de"` to force German processing
- For DermaMedicum medical terminology, create a pronunciation dictionary for dermatological terms (e.g., "Hyaluronsaeure," "Botulinumtoxin," "Microneedling")

**Operational recommendation for DermaMedicum:**
1. Use **v3** with German voice for emotional narration (short segments, < 5000 chars)
2. Use **Multilingual v2** for longer educational content
3. Create a pronunciation dictionary for medical/dermatological German terms
4. Test with native speaker before deploying — AI German is good but not perfect on medical terminology

### 6. Integration: Syncing Audio with Video

#### Pipeline for Remotion-based workflow

```
1. Script text with timing markers
2. Generate TTS segments via API (save as WAV/PCM for editing)
3. Generate SFX layers via API
4. Generate music bed (if needed) via Music API
5. Combine layers with ffmpeg:
   ffmpeg -i video.mp4 -i narration.wav -i sfx.wav -i music.wav \
     -filter_complex "[1:a]adelay=2000|2000[narr];[2:a]adelay=5000|5000[sfx];[3:a]volume=0.3[music];[narr][sfx][music]amix=inputs=3" \
     -c:v copy output.mp4
6. Or integrate directly in Remotion using <Audio> components with startFrom/volume
```

#### Timing precision
- ElevenLabs returns audio as a file — duration is deterministic per generation
- Use `seed` parameter for reproducible outputs when iterating on timing
- For precise sync: generate audio first, then build animation to match audio duration
- Alternative: use Scribe (STT) to get word-level timestamps from generated audio, then align visual beats to word timing

#### Remotion integration pattern
```typescript
import { Audio, Sequence, useCurrentFrame } from 'remotion';

// Layer audio tracks with precise timing
<Sequence from={0}>
  <Audio src={narration} volume={1.0} />
</Sequence>
<Sequence from={60}> {/* 2 seconds at 30fps */}
  <Audio src={swooshSfx} volume={0.8} />
</Sequence>
<Sequence from={0}>
  <Audio src={musicBed} volume={0.15} />
</Sequence>
```

### 7. Known Failure Modes and Credit Waste

#### What ElevenLabs does badly
1. **Failed generations still cost credits.** Glitches, mid-sentence language switches, volume fluctuations — you pay for all of them. Budget 2–3x the theoretical credit cost for real projects.
2. **PVC on v3 is degraded.** Professional Voice Clones don't work well on v3 yet. Use Multilingual v2 for PVC.
3. **Complex SFX prompts produce mud.** Don't try to describe an entire scene in one SFX prompt. Layer individual sounds.
4. **Non-English number/date handling.** German, French, etc. may mispronounce numbers, dates, addresses. Pre-normalize in your script.
5. **Long-form v3 is limited.** v3 caps at 5,000 characters per request (~5 min). For longer content, chain requests with `previous_request_ids`.
6. **Dubbing burns credits fast.** The dubbing tool can consume credits unpredictably. Monitor closely.
7. **Voice cloning from poor source audio.** IVC quality is entirely dependent on source audio quality. Bad in = bad out.
8. **Emotional mismatch.** A serious/professional voice won't respond to playful tags. Match voice character to intended delivery.
9. **Accent contamination.** When generating multilingual content, accents from previous generations can bleed through. Generate each language in a fresh request.
10. **Service reliability.** 10 incidents in a 28-day window logged in Feb 2026. Build retry logic.

#### What never to do
- Don't use the free tier for production (no commercial license, requires attribution)
- Don't generate long-form on v3 when Multilingual v2 handles it better
- Don't set SFX duration manually for > 5 seconds (auto is cheaper)
- Don't use PVC voices with v3 model (use Multilingual v2)
- Don't expect one SFX generation to produce a complete soundscape
- Don't skip pronunciation dictionaries for medical/technical content

### 8. Pricing Optimization

#### Plans (April 2026)

| Plan | Price | Credits | ~Minutes TTS | Commercial | Voice Cloning |
|------|-------|---------|-------------|------------|---------------|
| Free | $0 | 10,000 | ~10 min | No (attribution required) | No |
| Starter | $5/mo | 30,000 | ~30 min | Yes | IVC only |
| Creator | $22/mo | 100,000 | ~100 min | Yes | IVC + PVC (30 voices) |
| Pro | $99/mo | 500,000 | ~500 min | Yes | IVC + PVC |
| Scale | $330/mo | Millions | Hundreds of hours | Yes | IVC + PVC |
| Business | $1,320/mo | Millions | Hundreds of hours | Yes | IVC + PVC |

#### Credit optimization strategies

1. **Use Flash v2.5 for drafts.** It costs 0.5 credits per character vs 1.0 for v2/v3. Prototype on Flash, finalize on v3/v2.
2. **SFX auto duration for 5+ seconds.** 200 credits flat vs 40/second manual.
3. **Script editing before generation.** Every character costs credits. Trim scripts ruthlessly before sending to API.
4. **Seed parameter for iteration.** When adjusting voice settings or timing, use the same seed to get reproducible output — avoids regenerating to find "the good take" again.
5. **Batch during rollover window.** Credits roll over for up to 2 months on Creator+ plans. If you know a big project is coming, let credits accumulate.
6. **Monitor with analytics.** Track credit consumption per generation type. SFX and dubbing consume differently than TTS.

#### Cost per deliverable (estimates)

For a 30-second Reel with narration + SFX + music bed:
- Narration (~150 words, ~900 chars): ~900 credits on v3, ~450 on Flash
- 3 SFX layers (auto duration): 600 credits
- Music bed (via Music API): separate credit pool, varies
- **Total per Reel: ~1,500–2,000 credits on v3, ~1,000–1,500 on Flash**
- On Creator plan (100K credits): ~50–65 Reels per month
- On Pro plan (500K credits): ~250–330 Reels per month

#### Overage rates
| Plan | Per 1,000 chars |
|------|----------------|
| Creator | $0.30 |
| Pro | $0.24 |
| Scale | $0.18 |
| Business | $0.12 |

---

## LAYER 2: SOUND DESIGN CRAFT

### Film Sound Design Masters

#### Walter Murch — The Architect

**Core principles:**

1. **The Rule of 2.5:** The audience can process only two and a half sonic elements at any moment. When Murch's premixes for Apocalypse Now sounded like "mud" at uniform levels, he discovered that only ~2.5 things could be active at one time. Beyond that, sounds congeal into undifferentiated noise.
   - **API application:** When layering TTS narration + SFX + music bed, never have more than 2.5 competing for attention at the same time. One must always dominate. In a 30s Reel: narration dominates the mid-section, SFX dominate transitions, music bed fills the rest at low volume.

2. **The Rule of Six (editing cuts, applied to audio transitions):** An ideal transition satisfies: (1) true to the emotion of the moment, (2) advances the story, (3) rhythmically right, (4) respects attention focus, (5) respects spatial grammar, (6) respects continuity. **Emotion is #1 — sacrifice everything else to preserve it.**
   - **API application:** When choosing between a "technically accurate" sound and an "emotionally right" sound, always pick emotion. A dermatology Reel about skin transformation should *feel* transformative — the whoosh at the reveal matters more than medical accuracy of the sound.

3. **Worldizing:** Murch played back recorded sound through speakers in real environments and re-recorded it to add natural room tone and spatial character.
   - **API application:** Use SFX prompt environment descriptors ("in a clinical room," "in a modern spa") to add spatial character. Layer room tone under clinical narration.

4. **Organic movement between formats:** Murch wanted Apocalypse Now to move organically between mono, stereo, and surround, creating a pulse. Sound should breathe.
   - **API application:** Don't make every moment of a Reel equally "produced." Let some moments be sparse (just a single voice, close), others dense (layered SFX + music). The contrast creates rhythm.

#### Ben Burtt — The Alchemist

**Core principles:**

1. **Organic source material:** Every iconic Star Wars sound started with a real-world recording. The lightsaber = film projector hum + broken TV feedback. Blaster = hitting a guy-wire on a radio tower. Darth Vader breathing = scuba regulator. George Lucas told Burtt: "If we do documentary-type recording, by its very nature it will have an authenticity to it."
   - **API application:** When prompting ElevenLabs SFX, ground descriptions in real physical objects and actions. "Metal surgical instrument placed on a glass tray" beats "medical sound." The model was trained on real-world recordings — specificity activates the right training data.

2. **Sound as character identity:** For WALL-E, Burtt spent 4–5 months finding different sounds for the robot's hands, arms, eyes, and wheel treads — each conveying different moods (agitated to relaxed). Every character element had its own sonic identity.
   - **API application:** For recurring content (DermaMedicum treatment series), establish sonic signatures. A specific transition sound for "before," a specific one for "after." A signature sound for the practice itself. Consistency builds recognition across Reels.

3. **Silence as impact:** "Silence can be a major element in helping you get impact in the sound." Orchestration requires crescendos AND pauses.
   - **API application:** Not every frame needs sound. Strategic silence before a reveal amplifies the reveal. In a Reel: 0.5–1.0 seconds of silence before the key transformation moment. The algorithm doesn't penalize silence — viewers' brains fill the gap with anticipation.

#### Gary Rydstrom — The Layering Master

**Core principles:**

1. **Frequency spectrum filling:** The T-Rex roar works because different sounds fill different frequency ranges. Baby elephant = high-frequency scream (the memorable part). Tiger/alligator = low-frequency rumble (the felt part). Lion = mid-frequency texture. Whale blowhole = breathing. No single source would work alone.
   - **API application:** When building a multi-layer soundscape, think in frequency bands:
     - **Low (20–200Hz):** Bass rumbles, deep whooshes, room tone
     - **Mid (200Hz–2kHz):** Voice, most SFX, music melody
     - **High (2kHz–20kHz):** Sizzle, sparkle, air, shimmer, clicks
   - Generate SFX that target specific frequency ranges. "Deep bass rumble" + "high-pitched crystalline shimmer" + narration in the mid range. Don't stack everything in the same frequency band.

2. **Sound tells what's off-screen:** In Jurassic Park, the audience knew the T-Rex was coming before they saw it, because the sound told them. Several minutes of tension were built from sound alone.
   - **API application:** In Reels, sound can extend the story beyond the frame. A dermatology Reel about laser treatment doesn't need to show the laser if you hear it. Sound creates space the visual doesn't occupy.

3. **Scale through sound:** Rydstrom made dinosaurs feel massive not just through low frequencies, but through the *layered complexity* of the sound. Simple sounds feel small; complex layered sounds feel big.
   - **API application:** For "big reveal" moments in Reels, layer 3+ SFX generations. Single sounds feel flat. Layered sounds feel cinematic.

#### Skip Lievsay — The Minimalist

**Core principles:**

1. **Sound design haiku:** Lievsay described No Country for Old Men as "almost like sound design haiku, a minimum number of sounds that could be made to tell the story." The film has only 16 minutes of music in a 2-hour runtime.
   - **API application:** Not every Reel needs wall-to-wall sound. Some DermaMedicum content (e.g., educational explainers) might work better with minimal sound — just voice + one carefully chosen ambient element. Less is often more.

2. **Removing the safety net:** "The idea here was to remove the safety net that lets the audience feel like they know what's going to happen." Without a music score telegraphing danger, the audience has to feel it themselves.
   - **API application:** Avoid "library music" clichés that telegraph the emotion. When every Reel uses the same upbeat track, the audience zones out. Unexpected silence or sparse sound design creates attention.

3. **Invisibility as success:** "The better we do our job, the less people realize what's going on." Sound design should feel inevitable, not noticeable.
   - **API application:** Generated sound should serve the content, not showcase itself. If a viewer notices "that's an AI sound effect," it's failed. Subtlety wins.

### Music Theory Applied to Sound

#### Tempo and Emotional Response
- **60–90 BPM:** Calm, contemplative, sad. Use for: patient testimonials, educational content, before-and-after reflection.
- **90–120 BPM:** Neutral to energetic. Use for: most Reels content, product demos, brand films.
- **120–150 BPM:** Excited, urgent, surprising. Use for: transformation reveals, hook moments, CTAs.
- **150+ BPM:** Intense, overwhelming. Rarely appropriate for medical/professional content.

**Application:** Match the pacing of visual cuts to audio tempo. If music bed is at 120 BPM (2 beats/second), visual transitions should land on beats — every 0.5 seconds or every 1.0 seconds. Misaligned cuts feel amateurish.

#### Tension and Release
- Cross-rhythms create tension by disrupting expectations
- Syncopation (off-beat emphasis) creates energy
- Resolution to the expected beat creates satisfaction
- **Application:** Build tension in first 2/3 of a Reel (ascending sound, increasing complexity), then release at the reveal moment (resolving chord, clean tone, or silence followed by a single clear sound).

#### Thelma Schoonmaker / Scorsese: Sound-Driven Editing
- "There's a great deal of mystery in film editing... You're supposed to feel that a film has pace and rhythm, but you're not necessarily supposed to be worried about how it was accomplished."
- In Raging Bull, slow motion matched to Cavalleria rusticana. Sound DEFINED the edit rhythm.
- Frank Warner created a crackle to match 1940s/50s camera flashbulb sounds — sound anchors temporal authenticity.
- **Application:** Build animations to audio, not the reverse. Generate the voice/SFX/music first. Then choreograph visual transitions to the audio rhythm. This is the opposite of how most AI video is made (silent video, audio bolted on) — and the difference is immediately perceptible.

### Writing / Rhetoric Applied to Sound

#### "Show Don't Tell" in Audio
- Voice-over narration works when it fills gaps visuals cannot explain. It fails when it describes what the audience can already see.
- "Wallpapering" = narrating what's visible. Audiences find this patronizing.
- The best documentary narration acts like "an expert sitting next to you, whispering the who, what, when, where, and why precisely when you need to know it."
- **Application for DermaMedicum:** Don't narrate "Here you can see the skin becoming smoother." Instead, let the animation show it while the narration adds what can't be seen: "Kollagen wird in der Tiefe neu aufgebaut" (collagen rebuilds from within). Sound adds the invisible layer.

#### Podcast Production Mastery (Radiolab / Jad Abumrad)
- Abumrad studied Bach counterpoint: 4 independent voices that all serve one musical story. He applies this to editing — 5 different interviews woven in counterpoint, all speaking to the same point from different angles.
- Sound design in Radiolab builds a "sense of building truth" — wonder seeds questions, then anxiety builds before the reveal.
- Granular synthesis: stretching and looping small audio fragments to create long drones and atmosphere.
- **Application:** For educational DermaMedicum content, the Radiolab structure works: pose a question (hook), build curiosity through layered information, resolve with the answer. Sound design mirrors this arc — sparse at the question, building through the middle, resolving at the end.

#### What Makes Narration Compelling vs. Annoying
**Compelling:**
- Conversational tone (written for the ear, not the eye)
- Tone varies with content (serious for serious, light for light)
- Fills gaps the visual can't cover
- Pacing matches the content rhythm

**Annoying:**
- Monotone delivery (same energy throughout)
- Redundant to the visual (describes what you already see)
- Corporate/stiff language
- Too fast (no breathing room) or too slow (patronizing)

**Application:** Use v3 audio tags to vary tone within a single narration. `[curious] Was passiert wirklich unter der Haut? ... [confident] Hyaluronsaeure bindet Feuchtigkeit in der Dermis.` The emotional shift keeps the listener engaged.

### Psychology of Sound

#### ASMR and Emotional Triggers
- Lower-pitched, complex sounds are especially effective triggers
- Slow-paced, detail-focused content triggers the response
- fMRI shows ASMR activates nucleus accumbens (reward), insula (interoception), somatosensory cortex
- Only 10–20% of population experiences true ASMR tingles, but the relaxation effect is broader
- **Application:** For DermaMedicum treatment Reels, ASMR-adjacent sound design (soft, close-mic clinical sounds, gentle product application sounds) triggers relaxation associations with the practice. This is already a proven genre on Instagram (skincare ASMR). Generate SFX like: "Close-mic, gentle application of cream on skin, soft spreading sound, quiet clinical room ambience."

#### The Cocktail Party Effect
- Humans can focus on one sound source amidst competing noise using spatial hearing, pitch discrimination, and attention control
- This works BEST as a binaural effect (both ears)
- The brain can only track one stream of speech at a time
- **Application for mixing:** Never have two voices speaking simultaneously. Never have narration competing with loud SFX. The human brain will try to track one and lose the other. Murch's Rule of 2.5 is the practical limit.

#### Sonic Branding
- Intel bong: 5 notes, 80%+ global recognition. 30+ years of consistent deployment.
- Netflix ta-dum: 2 notes. Sets cinematic tone instantly.
- Ideal sonic logo: ~6 notes — long enough to be memorable, short enough to be distinctive.
- Sonic logos trigger emotional responses 86% faster than visual logos.
- Audio branding increases brand recognition by 96% compared to visual elements alone.

**Application for DermaMedicum:**
- Create a 2–3 second sonic signature for the practice. Generate via SFX API: "Soft, clean, modern chime, two notes ascending, spa-like, clinical but warm"
- Use it at the end of every Reel (like Netflix ta-dum)
- After 20+ Reels, the sound itself carries brand association
- This is a compound asset — every future Reel reinforces it

#### The Power of Silence
- Silence in film uses psychoacoustics: the brain fills gaps, heightens awareness
- Absence of sound creates anticipation and unease
- In A Quiet Place: the entire premise is silence. In No Country for Old Men: only 16 minutes of music in 2 hours.
- "In a medium driven by sound and visuals, silence is one of the most powerful and underused tools"
- **Application:** In a 30-second Reel, 1–2 seconds of near-silence before the key reveal moment. This is counterintuitive for social media (where constant stimulation is the norm) but it's exactly why it works — it breaks the pattern.

### Short-Form Video Audio Trends (2025–2026)

- Trending Reels audio changes every 48–72 hours
- Algorithm favors content with trending audio (boost to reach)
- BUT: trending audio is only a discovery advantage. Original sound design is a differentiation advantage.
- For DermaMedicum (business account): limited access to licensed music. Original AI-generated audio is the practical solution AND the differentiation.
- Best-performing audio types: feel-good throwbacks, lo-fi beats, motivational dialogue, meme sounds, emotional vocals
- **Application:** Use ElevenLabs Music API to generate lo-fi or ambient beds that match trending energy without copyright issues. Combine with original narration for a sound profile that's both on-trend and unique.

---

## CROSS-DOMAIN PATTERNS

After studying film sound design, music theory, podcast production, psychology, and rhetoric, these patterns appear across 3+ domains:

### PATTERN: The Hierarchy of Attention

**DOMAINS:**
- Film (Murch's Rule of 2.5 — only 2.5 sonic elements can be tracked)
- Psychology (Cocktail Party Effect — brain tracks one speech stream)
- Music (Arrangement theory — only 3–4 parts are distinguishable at once)
- Podcast (Radiolab edits never have overlapping speech without one being backgrounded)

**MECHANISM:** Human auditory processing has a hard bandwidth limit. The brain uses selective attention to foreground one stream and suppress others. Adding more elements past the limit doesn't add richness — it creates noise. This is neurological, not cultural.

**APPLICATION:** In every audio mix for a Reel: ONE element dominates at any moment. Narration segment: voice at 100%, music at 15%, SFX at 0%. Transition: SFX at 100%, music at 30%, voice at 0%. Reveal: single impact SFX at 100%, then silence. Never mix at uniform levels.

**FALSIFIABLE:** Evidence against: a mix with 4+ equal-volume elements that audiences rate as more engaging than a hierarchical mix. If auditory attention bandwidth is wider than 2.5, the rule needs updating.

---

### PATTERN: Organic Grounding

**DOMAINS:**
- Film (Burtt: all sci-fi sounds derived from real-world recordings for "authenticity")
- Film (Rydstrom: dinosaur sounds from real animals, not synthesizers)
- Psychology (ASMR: real-world sounds trigger physiological response; synthetic ones rarely do)
- Sonic branding (most memorable logos use acoustic/organic timbres, not pure synthesis)
- Rhetoric (Radiolab: real interview voices woven together, never synthetic narration)

**MECHANISM:** The human auditory system evolved to process natural sounds over millions of years. It has deep pattern recognition for organic/physical sounds (impact, air, water, animal vocalization) and relatively shallow recognition for synthetic ones. Organic sounds carry implicit physics information (size, distance, material, energy) that the brain decodes automatically.

**APPLICATION:** When prompting ElevenLabs SFX, always describe physical reality, not abstract concepts. "Metal tray sliding on marble counter in a quiet clinic" activates richer generation than "medical transition sound." The model's training data is real-world recordings — prompts that describe real physics activate the best training examples.

**FALSIFIABLE:** Evidence against: AI-generated synthetic/electronic sounds consistently rated as more emotionally engaging than organic-grounded ones for the same use case. If audiences prefer abstract synthesis, the organic principle is aesthetic preference, not universal.

---

### PATTERN: Contrast Creates Perception

**DOMAINS:**
- Film (Murch: organic movement between mono/stereo/surround creates "pulse")
- Film (Lievsay: silence makes the few sounds in No Country feel enormous)
- Music theory (tension-release cycles drive emotional response; static harmony bores)
- Psychology (ASMR: quiet triggers work because they contrast with normal environmental volume)
- Rhetoric (Radiolab: wonder builds through uncertainty before resolution)
- Scoring (Hans Zimmer: Dunkirk's ticking clock works because of the silent spaces between ticks)
- Sonic branding (Netflix ta-dum works because it follows silence — the moment before content)

**MECHANISM:** The auditory system is primarily a change detector, not a level detector. Neurons fire on onset and offset, not during sustained stimulation. Constant stimulation causes adaptation (listener fatigue). Contrast — loud/quiet, dense/sparse, fast/slow, harmonic/dissonant — resets attention and creates the perception of events.

**APPLICATION:** Structure every Reel's audio as a contrast sequence:
1. Hook (0–3s): Attention-grabbing sound (contrast with the silence before the Reel plays)
2. Build (3–15s): Increasing density, rising pitch/tempo
3. Drop (15–16s): Brief silence or extreme reduction (0.5–1.0 seconds)
4. Reveal (16–20s): Payoff sound — layered, rich, satisfying
5. Resolve (20–30s): Return to simplicity, voice narration, brand signature sound

This mirrors the visual tension-reveal pattern already in the DermaMedicum animation styles.

**FALSIFIABLE:** Evidence against: content with uniform audio density performing better in engagement metrics than contrast-structured audio. If constant stimulation outperforms contrast on social media (different from cinema), the pattern is domain-limited.

---

### PATTERN: Sound as Invisible Storyteller

**DOMAINS:**
- Film (Rydstrom: T-Rex heard before seen — sound told what was off-screen)
- Documentary (narration adds what can't be seen — the "invisible expert")
- Rhetoric ("show don't tell" — narration fills gaps visuals can't)
- Podcast (entire medium is sound-only storytelling — no visuals to rely on)
- Horror (sound creates threat from what's unseen — A Quiet Place, Jaws)

**MECHANISM:** Sound extends the perceptual space beyond the visual frame. It can convey information about what's coming (anticipation), what's happening out of view (spatial extension), and what's happening at a scale too small or abstract to show (scientific processes, emotional states). Vision is directional; hearing is omnidirectional. Sound fills the space that vision doesn't cover.

**APPLICATION:** For DermaMedicum Reels about treatments that work beneath the skin surface: animation shows the exterior transformation, but SOUND tells the story of what's happening inside. A gentle "cellular" sound during the treatment phase. A building shimmer during the "collagen rebuilding" phase. A clean, resolving tone at the "results" phase. The viewer sees the surface; they hear the mechanism.

**FALSIFIABLE:** Evidence against: identical video content with and without narrative audio performing equally on comprehension and engagement. If audio adds no measurable information or emotional engagement beyond the visual, this pattern is ornamental.

---

### PATTERN: Signature Repetition Builds Recognition

**DOMAINS:**
- Sonic branding (Intel, Netflix, Apple — decades of same sound)
- Film (John Williams leitmotifs — Darth Vader's theme, Jaws 2-note shark theme)
- ASMR (familiar triggers become more effective over time, not less)
- Podcast (Radiolab's intro sound is instantly recognizable to listeners)
- Rhetoric (rhetorical devices: anaphora, epistrophe — repetition creates memory)

**MECHANISM:** Memory consolidation through spaced repetition. Each exposure strengthens the neural pathway connecting the sound to its associated meaning/emotion. After sufficient repetition, the sound becomes a shortcut — triggering the full emotional response without the original context. This is classical conditioning applied to brand association.

**APPLICATION:** Establish these signature sounds for DermaMedicum and use them in EVERY Reel:
1. **Intro signature:** 1–2 second sound at the start (brand recognition)
2. **Transition sound:** Consistent "before/after" transition (treatment transformation)
3. **Outro signature:** 2–3 second closing sound (like Netflix ta-dum)
Generate each once via ElevenLabs SFX, then reuse across all Reels. After 20+ Reels, these sounds carry the brand. Prompt examples:
- Intro: "Soft modern chime, two ascending notes, clean and clinical, warm"
- Transition: "Smooth crystalline whoosh, ascending, spa-like shimmer, 1.5 seconds"
- Outro: "Gentle two-note resolution, warm, professional, soft reverb tail, 2 seconds"

**FALSIFIABLE:** Evidence against: A/B test showing Reels with randomly varied audio signatures performing equal to or better than consistent ones on brand recall metrics. If novelty outperforms consistency, the repetition principle is weaker for short-form social content.

---

### PATTERN: Emotion Over Accuracy

**DOMAINS:**
- Film (Murch's Rule of Six: emotion is #1 priority — sacrifice everything else for it)
- Film (Burtt: lightsaber sound is physically wrong — no sound in space — but emotionally perfect)
- Film (Rydstrom: T-Rex sounds from baby elephants — zoologically wrong, emotionally right)
- Music (dissonant chords resolve — the resolution is "wrong" in terms of pure frequency ratios but emotionally satisfying)
- Documentary (Errol Morris: "sometimes reinterpreted sounds appear truer than the originals")
- Advertising (voice-over research: "every inflection can sway decisions and shape perceptions")

**MECHANISM:** The auditory system processes emotional content faster than analytical content (amygdala responds in ~20ms; cortical analysis takes ~150ms+). Sound is processed emotionally before it's processed analytically. An emotionally "right" sound feels true even if it's physically inaccurate. An emotionally "wrong" sound feels false even if it's technically correct.

**APPLICATION:** When generating audio for DermaMedicum Reels, optimize for emotional accuracy, not physical accuracy. A hyaluronic acid injection doesn't actually make a "hydrating shimmer" sound — but it SHOULD, because that's what the treatment does emotionally (replenishing, refreshing, filling). The "emotionally true" sound communicates the treatment's value better than silence or a realistic needle sound.

Prompt: "Gentle liquid shimmer sound, like water being absorbed, soft and refreshing, 2 seconds" > "Needle injection clinical sound"

**FALSIFIABLE:** Evidence against: audience testing where physically accurate sounds consistently outperform emotionally-designed sounds on trust and engagement metrics. If medical audiences specifically distrust "emotional" sounds as manipulative, the pattern inverts for clinical content.

---

## OPERATIONAL CHECKLISTS

### Pre-Production Sound Checklist (before generating any audio)

- [ ] What is the ONE emotion this Reel should leave the viewer with?
- [ ] Where are the silence moments? (Minimum 1 per Reel)
- [ ] What is the foreground/background hierarchy at each moment?
- [ ] Does the narration add invisible information, or wallpaper the visual?
- [ ] Which signature sounds apply? (intro, transition, outro)
- [ ] Language: German? English? Both?
- [ ] Medical terminology: added to pronunciation dictionary?

### Generation Order (always audio-first for best sync)

1. Generate narration segments (v3 for emotional, v2 for long-form)
2. Generate transition SFX (keep a library of reusable ones)
3. Generate scene-specific SFX (ambience, impacts, reveals)
4. Generate or select music bed (Music API or library)
5. Assemble layers with timing in Remotion or ffmpeg
6. Check: at any moment, is more than one element competing for attention?
7. Check: does the audio arc match the visual arc? (build-drop-reveal)

### DermaMedicum Sound Palette

| Element | Prompt Template | Duration | Reuse? |
|---------|----------------|----------|--------|
| Brand intro | "Soft modern chime, two ascending notes, clean clinical warm" | 1.5s | Every Reel |
| Before/after transition | "Smooth crystalline whoosh, ascending, spa-like shimmer" | 1.5s | Every treatment Reel |
| Brand outro | "Gentle two-note resolution, warm professional, soft reverb tail" | 2.0s | Every Reel |
| Clinical ambience | "Quiet modern medical office, soft air conditioning, clean room tone" | 15s loop | Background layer |
| Treatment activation | "Gentle energy pulse, warm light shimmer, subtle bass" | 2.0s | Treatment start |
| Skin transformation | "Soft organic morphing sound, like fabric smoothing, gentle" | 3.0s | Results moment |
| Hydration SFX | "Liquid shimmer, like water absorbed by soft material, refreshing" | 2.0s | Hyaluronic acid |
| Precision SFX | "Fine focused beam, clean high frequency, precise and clinical" | 1.5s | Laser treatments |

### Python Quick-Start Template

```python
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# --- TTS with v3 + audio tags ---
narration = client.text_to_speech.convert(
    text="[curious] Was passiert wirklich unter der Haut? ... [confident] Hyaluronsaeure bindet Feuchtigkeit in der Dermis.",
    voice_id="VOICE_ID_HERE",  # German voice from library
    model_id="eleven_v3",
    output_format="wav_44100",
    voice_settings={
        "stability": 0.4,        # Lower for more expression
        "similarity_boost": 0.75,
        "style": 0.3,
        "speed": 0.95,           # Slightly slower for German medical content
    },
    language_code="de",
)
with open("narration.wav", "wb") as f:
    for chunk in narration:
        f.write(chunk)

# --- SFX generation ---
sfx = client.text_to_sound_effects.convert(
    text="Smooth crystalline whoosh, ascending, spa-like shimmer, clean and modern",
    duration_seconds=1.5,
    prompt_influence=0.5,
)
with open("transition.wav", "wb") as f:
    for chunk in sfx:
        f.write(chunk)

# --- Voice design (one-time setup) ---
previews = client.text_to_voice.design(
    voice_description="A warm, professional German female voice in her mid-30s. Calm and reassuring but not monotone. Natural German accent with clear pronunciation. Suitable for medical and wellness content. Conversational but authoritative.",
    model_id="eleven_ttv_v3",
    auto_generate_text=True,
    guidance_scale=4,
    should_enhance=True,
)
# Listen to previews, then save the best one:
# client.text_to_voice.create(voice_name="DermaMedicum", generated_voice_id=previews.previews[0].generated_voice_id)
```

### ffmpeg Audio Assembly Template

```bash
# Layer narration + SFX + music with timing offsets
ffmpeg -i video.mp4 \
  -i narration.wav \
  -i transition_sfx.wav \
  -i music_bed.wav \
  -filter_complex "
    [1:a]adelay=2000|2000,volume=1.0[narr];
    [2:a]adelay=4500|4500,volume=0.8[sfx];
    [3:a]volume=0.15[music];
    [narr][sfx][music]amix=inputs=3:duration=first
  " \
  -c:v copy \
  -c:a aac -b:a 192k \
  output_with_audio.mp4
```

---

## UNVERIFIED / HYPOTHESIZED (flagged for future sessions)

1. **v3 German quality claim:** Based on general reviews, not tested with DermaMedicum-specific dermatological terminology. Needs empirical test with native German speaker.
2. **Credit cost estimates per Reel:** Calculated from published rates, not measured from actual production. Real costs may be 2-3x due to failed generations.
3. **Sonic branding compound effect:** The claim that 20+ Reels with consistent audio builds brand recognition is extrapolated from traditional media research (Intel, Netflix). Short-form social media may have different dynamics.
4. **ASMR adjacency for medical content:** The hypothesis that ASMR-style sound design works for dermatology Reels is based on the skincare ASMR genre's success, not tested with DermaMedicum's specific audience.
5. **Music API credit costs:** Not fully documented in public sources. Needs empirical measurement.
6. **Silence working on Instagram:** Cinema research supports silence for impact. Instagram's autoplay-with-sound-off environment may make silence indistinguishable from "no audio." Needs testing with sound-on audiences specifically.
