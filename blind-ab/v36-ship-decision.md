# v36 SHIP DECISION — Kling v3 (closes 3-way comparison)

Third use of SHIP DECISION template (v2 with motion-type row).

Reference loaded: `/root/twitter-pipeline/pulse-nb2-proud.png` (NB2 canonical Pulse).
Output loaded: `v36-frames/f0..f5.jpg` (6 frames across 10.04s).
Config accepted on first try: `kling-v3` / `mode=pro` / `duration=10` / `cfg_scale=0.7` / `aspect=16:9`.

---

## v36-kling-v3.mp4

### Character match vs. NB2
| Trait | NB2 canon | Observed | Verdict |
|---|---|---|---|
| Body shape | Round fluffy blob | **Very round fluffy body, squash-and-stretch proportions** | ✅ (closest yet) |
| External ears | None | **Cat/fox-style triangular ears** | ❌ drift |
| Eyes | Big brown | Big brown with bright highlights | ✅ |
| Halo | Gold, above | Gold, above | ✅ |
| Wings | Small feathered | Small feathered (visible both sides) | ✅ |
| Paw-hands | Small stubby | Small, holding crumpled paper | ✅ |
| Blush / face | Soft cheeks | Pink blush, small mouth | ✅ |

**Character verdict:** ~6/7 traits match. Drift only on external ears. Closest rendering of NB2 Pulse this entire session — beats v35-b (4/7) and v34 (5/6) meaningfully.

### Scene match
- Window sunset backlight ✅
- Wooden floorboards ✅
- Interior warm light ✅
- Apartment / room background visible through window ✅
- Register: clean anime/Ghibli ✅

### Motion type
| | |
|---|---|
| **Motion type** | **character-only, locked camera** |
| Camera | **static** — no pan, no push-in, no cut; framing constant across 10s |
| Character | facial only — expression shifts, no body movement |

### Motion beats (observable in frames)
- f0→f3 (0-5s): held contemplation — character looks at paper, small pout, nearly identical frames (micro-motion only). Establishes the moment.
- f3→f4 (~6.7s): **real beat shift** — eyes widen slightly, mouth opens into a small "o", head tilts. A surprise/realization moment.
- f4→f5 (~8.3s): resolve — mouth closes into a content smile, eyes soften, head tilts gently.
- **Net:** one clear acting beat with 5 seconds of setup. This is the 2-beat structure wiki/registers/anime.md recommends (held composition + one beat), not the 3-stacked-beats I almost wrote.

### Ship/retry: **SHIP-READY — BEST OF SESSION**
- Character body + halo + wings + eyes + paws all match NB2
- Single locked shot, no camera artifact
- Clean acting chain (contemplation → realization → smile)
- 10s duration = enough to land the beat AND breathe
- Anime-register-correct framing grammar per wiki
- Caption-safe: "Pulse holds a drawing. Looks at it. A moment. Then a small smile."
- Caveat: still has fox/cat ears (not NB2 canon). Could be an accepted stylistic variation, or retry with `no external ears` higher in the prompt.

---

## 3-way tool comparison (closes the Kling-vs-Veo question)

| | v34-b (kling-v1-6 std) | v35-b (veo-3.1-fast) | v36 (kling-v3 pro) |
|---|---|---|---|
| Duration | 5s | 8s | 10s |
| Motion type | still + camera pan | character + camera | **character only, locked** |
| Character fidelity (NB2) | ~4/6 | ~4/7 | **~6/7** |
| Character consistency | held | held | **held + more detail** |
| Anime framing grammar (held shot + beat) | N/A (no real beats) | push-in (not locked) | **locked + one beat** ✅ |
| Best of session? | no | was, until this one | **YES** |

**The lesson the operator corrected me on is now evidenced.** `kling-v1-6` is not just "an older version that's cheaper" — it's a **different capability class** from `kling-v3`. v1-6 produces still+camera; v3 produces real character animation with locked cameras in anime framing. The "Kling can't animate characters" conclusion from v34 was wrong because v34 used the wrong Kling. v36 = right Kling + best config = new session floor.

**Concrete correction to the tool lesson:** retract from `feedback-internal-dialogue.md` the scoped observation that kling-v1-6 produced still+camera, and replace with: "kling-v3 pro mode with cfg_scale 0.7 and duration 10s produces locked-shot character animation that matches anime framing grammar better than Veo 3.1 Fast for this brief. v1-6 is superseded. The rule is 'always latest,' the evidence is 'v3 produced the session floor.'"

---

## Template v2 performance on third use

**Motion type row worked — again.** Without it I might have claimed "similar to v35-b, real character motion with push-in camera." The row forced me to note that v36's camera is LOCKED, not push-in. That distinction is the thing that makes v36 match anime framing grammar (per wiki/registers/anime.md line 64: "anime favors static compositions with cuts, not continuous camera movement").

**Proposed template v3 addition:** add a "Framing grammar" row that checks the motion type against the register's conventions. For anime: locked + beat = correct; continuous pan = wrong. This would have made v36's superiority visible earlier.
