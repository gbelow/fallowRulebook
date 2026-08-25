---
name: size-table
description: >-
  Quick reference for the Fallow size system — the size 1–7 table (DM, SM, MM,
  VM), skill modifiers by size, Standard Deflection, and creature/weapon/gear
  scaling rules. Use whenever a question involves creature size, scaling a
  creature or weapon up or down, size-based hit difficulty (SD), or how size
  changes STR-derived values, movement, reach, weight, or consumption.
---

# Size Table Quick Reference

Source of truth: `creating.tex` §Size (table + definitions), with cross-cutting
rules in `gear.tex` (weapon size/scaling), `combat.tex` (lifting, push),
`abilities.tex` (Grow!/Shrink!), `survival.tex` (rations). Re-read `creating.tex`
if exactness matters — the user edits these tables actively.

## Master table (size 1–7)

| Size | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| DM (damage) | 0.5 | 0.75 | 1 | 1.5 | 2 | 3 | 4 |
| SM (skill) | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
| MM (movement) | 0.5 | 1 | 1 | 1.5 | 1.5 | 2 | 2.5 |
| VM (volume/weight) | 0.1 | 0.33 | 1 | 3.33 | 10 | 33.3 | 100 |

Size 3 = human baseline (≈50 kg). Weight scales ×3 per category, ×10 per 2
categories. Reference points: size 1 ≈ cat (5 kg), size 5 ≈ horse (500 kg).

## What each multiplier touches

- **DM** — multiplies all STR-derived values: damage (weapon plain numbers and
  STR contributions), TGH, armor defenses, abilities, and STR-scaling spells.
- **SM** — added to/subtracted from skills per the skill modifier table below.
- **MM** — multiplies all movement speeds AND weapon ranges.
- **VM** — multiplies character weight, item weight when scaling, and consumable
  doses (a potion dose = 1× VM of the size-3 content).

## Skill modifiers (×SM)

| Skill | Mod |
|---|---|
| Grapple | +5×SM |
| Reflex | −1×SM |
| SD | −1×SM |
| Stealth | −3×SM |
| Climbing | −2×SM |

## Standard Deflection (SD)

SD = the floor difficulty to hit a target, based only on size and movement:
- Moving target: **−2 − SM**
- Stationary target: **−5 − SM**

No penalty of any kind can push a character's deflection below their SD.

## Grid occupation

- Size 3 (human form): 1 square or hex.
- Every +2 size categories: square grid grows 1 square per dimension; hex grid
  occupies 3 spaces (token in the middle of 3), then 7. Other shapes possible.
- Two size-3 creatures may share a space but cannot end a turn there.
- A creature may share space with another **2 sizes larger** than itself.

## Scaling rules

**Scaling a creature (same shape):** strength grows with muscle cross-section,
weight with volume — so each size category up gives **−1 STR and −1 natural
AGI** (DM more than compensates in raw output). Grow!/Shrink! abilities encode
this: +1 size = −3 STR −1 AGI; −1 size = +3 STR +1 AGI.

**Scaling a weapon:** tables are human-sized (size 3) baselines. Multiply damage
and RES by **DM**, reach/range by **MM**.

**Wielding a weapon of the wrong size:**
- One category too large: +1 AP on all attacks with it, and all STR
  contributions use **STR−5** (applies to every STR contribution: braced, hook,
  heavy).
- Two categories too large: impossible.
- Large Hands ability: use weapons one category up with +1 AP and STR−3; hands
  count as a larger-size weapon without the AP cost.

## Size elsewhere (quick hooks)

- **Lifting:** STR scales ×3.33 per 5 STR (follows VM). Baseline: STR 10 human
  lifts ~20 kg (one size category below own) in 3 AP + 1 STA.
- **Push DL:** 50 kg (size 3) = DL 0; ±5 DL per size category; +1 DL per m/s of
  speed for size-3 objects.
- **Grapple assists:** helpers of a smaller size category add max +2.
- **Sweeping attacks:** no size bonus/penalty to strike.
- **Rations:** portion ≈ 500 g food / 500 ml water at size 3; scales with VM.
- **Child:** counts as a size 2 creature.
