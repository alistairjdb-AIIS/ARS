# Kling AI

> AI video generation model specializing in photoreal human faces and skin textures, outperforming Veo 3.1 for close-up human work based on controlled blind A/B testing, with JWT-based API authentication.

**Confidence:** MEDIUM
**Last compiled:** 2026-04-06
**Sources:** 0 raw research files, 2 memory files (credentials + curriculum A/B findings)

---

## Core Findings

### Capabilities

**API surface:**
- **Base URL:** `https://api.klingai.com`
- **Endpoints:**
  - `/v1/videos/text2video` -- text-to-video generation [VERIFIED]
  - `/v1/videos/image2video` -- image-to-video generation [VERIFIED]
- **Status:** Key verified April 3, 2026. Credits available, test generation succeeded. [TESTED]

**Generation parameters:**
- Clip duration: 5-10 seconds (observed from A/B tests) [TESTED]
- Output: photoreal video clips [TESTED]

**Auth pattern (JWT):**
- Algorithm: HS256
- JWT claims:
  - `iss`: Access Key
  - `exp`: now + 1800 seconds (30 min)
  - `nbf`: now - 5 seconds
- Signed with: Secret Key
- Token passed as Bearer auth

```python
import jwt
import time

def get_kling_token(access_key, secret_key):
    now = int(time.time())
    payload = {
        "iss": access_key,
        "exp": now + 1800,
        "nbf": now - 5
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

headers = {
    "Authorization": f"Bearer {get_kling_token(ACCESS_KEY, SECRET_KEY)}"
}
```

**Important:** Load access key and secret key from environment variables. Never hardcode credentials. [VERIFIED -- lesson from Veo key revocation incident]

### Prompt Patterns

Based on controlled blind A/B testing (N=3 as of 2026-04-06):

**What works for photoreal humans [TESTED]:**
- **Imperfection prompting:** Specific physical imperfections (laugh lines, age spots, crooked nose) produce more realistic output than generic descriptions
- **Acting-chain specificity:** Describe stimulus > processing > response rather than static poses. This is the same pattern that works for stylized characters on Veo 3.1.
- **Film grain language:** Including film grain and analog texture descriptions improves photorealism
- **Restraint in camera direction:** Do NOT over-specify camera choreography. Let the model handle framing. "Be the acting director, not the DP."

**What works for /animate pipeline integration [TESTED, N=2]:**
- The /animate skill adds value through what it helps LEAVE OUT, not what it adds (v19 finding)
- Restraint produces more physically plausible outputs (no impossible steam, natural emotional sequences)
- Match restraint level to content register: subtle content = restrained prompt, energetic content = rich prompt (v20 finding)

### Operational Patterns

- **JWT token refresh:** Tokens expire after 30 minutes. Generate a new token for each API session or implement auto-refresh. [VERIFIED]
- **Quota management:** Kling rendered successfully when Veo hit daily quota (v18 test), making it a practical backup for quota-limited Veo usage. [TESTED]
- **Use case routing:** Kling for photoreal human faces, Veo for environments/objects/stylized characters. [TESTED]

### Quality Assessment

**Where Kling AI excels:**
- Photoreal human faces -- outperforms Veo 3.1 for face photorealism [TESTED, cross-model finding from v18]
- Skin textures and aging details [TESTED]
- Human emotional expressions and subtle acting [TESTED]

**Where Kling AI is untested or weaker:**
- Environments and objects without humans -- no comparative data vs Veo [THEORETICAL]
- Stylized characters -- limited testing (v20 was Pixar-Pokemon hybrid, results mixed) [TESTED, N=1]
- Audio generation -- Kling generates silent video; requires [[elevenlabs]] for audio [VERIFIED]
- Joint audio+video -- Veo 3.1 generates audio jointly, Kling does not [VERIFIED]

**A/B Test Results (from curriculum, as of 2026-04-06):**

| Test | Subject | Winner | Finding |
|------|---------|--------|---------|
| v18 | Elderly man reading letter | Research-crafted | Imperfection prompting + acting chain + film grain language worked. Confirmed Kling as strong for face photorealism |
| v19 | Coffee shop woman | /animate-crafted | Value in RESTRAINT: more physically plausible, more natural emotional sequence, better framing from NOT specifying camera |
| v20 | Pixar x Pokemon creature | Crafted-without-animate | Restrained approach produced static output; direct crafted had more fluidity. Content register mismatch for restraint |

**Score:** Research-crafted 1, /animate-crafted 1, Direct-crafted 1, Terse 0.

---

## Operational Rules

- **When generating photoreal human video,** use Kling AI instead of Veo 3.1, because blind A/B testing confirms Kling outperforms Veo for face photorealism. [TESTED]
- **When prompting for human faces,** include specific physical imperfections (laugh lines, age spots, crooked nose, etc.), because imperfection prompting produces more realistic output and avoids the "too perfect" veto. [TESTED]
- **When describing human action,** use acting-chain structure (stimulus > processing > response) rather than static pose descriptions, because acting specificity improves output across both Kling and Veo. [TESTED]
- **When specifying camera work,** be minimal -- describe framing loosely and let the model handle specifics, because camera choreography over-specification hurts output quality ("Be the acting director, not the DP"). [TESTED]
- **When authenticating,** generate a fresh JWT (HS256) with access key as `iss`, exp = now + 1800, nbf = now - 5, signed with secret key, because tokens expire after 30 minutes. [VERIFIED]
- **When Veo hits daily quota,** fall back to Kling for human-subject work, because Kling has independent quota and rendered successfully during Veo quota exhaustion. [TESTED]
- **When content needs audio,** pair with [[elevenlabs]] for all audio layers, because Kling generates silent video only. [VERIFIED]
- **When matching restraint to register,** use restrained prompts for subtle emotional content and rich prompts for energetic/spectacle content, because the v19-v20 /animate comparison showed restraint level must match content energy. [TESTED]

---

## Source Files

| File | Contribution |
|------|-------------|
| `credentials.md` (memory) | JWT auth pattern, base URL, endpoints, key verification status |
| `project-curriculum-elements.md` (memory) | A/B test results v18-v20, cross-model finding (Kling > Veo for faces), imperfection prompting, acting-chain specificity, restraint-to-register matching |

---

## Related Concepts

- [[veo-3-1]] -- Primary video generation tool; Kling complements for human faces where Veo is weaker. Veo generates joint audio; Kling does not.
- [[elevenlabs]] -- Required audio partner for all Kling-generated video (TTS, SFX, music)
- [[recraft-v4]] -- Static frame/thumbnail generation to accompany Kling video clips
- [[runway-gen4]] — CONTRASTS: Runway requires reference images for comparable face quality while Kling achieves superior per-frame photoreal faces from text alone; Runway's strength is character consistency across shots via reference conditioning

---

## Deep Reference

- **When** setting up JWT authentication for Kling API calls → **read** `memory/credentials.md` §(Kling AI) **for** access key, secret key, JWT construction (HS256, iss=AccessKey, exp=now+1800, nbf=now-5, sign with SecretKey), base URL (`https://api.klingai.com`), and confirmed endpoints (`/v1/videos/text2video`, `/v1/videos/image2video`)
- **When** deciding whether to use Kling or Veo for a specific shot → **read** `memory/project-curriculum-elements.md` §(Element 4 — Photoreal humans) **for** the cross-model finding (Kling outperforms Veo for photoreal human faces), the v18 evidence (imperfection prompting + acting chain + film grain worked on Kling for elderly man), v19 evidence (/animate restraint value), and the v20 nuance (restraint lost to energy for stylized creature content)
- **When** prompting Kling for photoreal humans and need the imperfection technique → **read** `memory/feedback-character-prompt-specificity.md` §(v19 finding) **for** the restraint principle (/animate adds value through what it helps leave out), acting-chain specificity that works across both Veo and Kling, and why NOT specifying camera produced better framing (profile = candid/observed vs front-facing = posed)

---

## Open Questions

- Full API parameter documentation -- only text2video and image2video endpoints confirmed; parameter details (aspect ratio, duration control, model variants, pricing per second) not documented in available sources [THEORETICAL]
- Environments/objects quality -- no comparative A/B data vs Veo for non-human subjects [THEORETICAL]
- Pricing structure -- not documented in available memory files [UNKNOWN]
- Rate limits and quota system -- Kling has independent quota from Veo but exact limits unknown [THEORETICAL]
- Image-to-video capabilities -- endpoint exists but not tested in A/B framework [THEORETICAL]
- Stylized character quality -- only 1 test (v20), insufficient N for conclusions [TESTED, N=1]
- Long-clip generation -- 5-10s observed, max duration unknown [THEORETICAL]
