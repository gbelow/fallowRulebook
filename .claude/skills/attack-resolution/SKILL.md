---
name: attack-resolution
description: >-
  Simulate attack resolution in the Fallow rulebook — apply any attack type with
  any modifiers and state the damage dealt against a target wearing given armor.
  Use when asked to calculate or simulate damage, resolve an attack, compare
  weapons/armor, compute expected damage per attack or per AP, or check what a
  declared location (head/hand/leg) does.
---

# Attack Resolution Simulator

Resolve an attack end-to-end: declare → roll → degree → defense → damage →
armor → tier → IL, bleed, effects, wound → HOP purchases. The usual question
is "what does weapon X do against armor Y", so always end with concrete
tier/IL numbers, not just a hit chance.

## 0. Source of truth

The user edits the book between messages. Re-read the current text before
resolving — never work from this file's numbers alone:
- Weapon, shield, armor tables, weapon properties, breakage, gear condition:
  `gear.tex`.
- Test ladder, exploding die, safe/risky: `play.tex` ("How skills work").
- Damage, additional effects, absorption, location, wounds, afflictions,
  Strike/Defend/Grapple, Accuracy/Reflex, positioning, morale: `combat.tex`.
- Skill formulas, TGH, SD, size table: `creating.tex`.
- The app's procedure: `chargenfallow/app/domain/character/rules/damage.ts`
  (read-only). Flag any app/book disagreement.

Terminology: overflow points are **HOP (Hit Overflow Points)**.

## 1. Inputs (ask, or assume and state)

**Attacker:** STR, size (→ DM/SM/RM), Melee or Ranged proficiency, weapon
row (RES, Blunt, Cut, AP for ranged, properties, range), attack variation,
declared location, condition (sharp/dull), oversized weapon, sensory penalty.

**Defender:** STR, size, armor row (RES, Protection, Insulation, Deflection),
gauntlets / closed helmet, TGH (default 0.5 × STR × DM), shield, chosen
defense, Defend or Reflex value, Force, current IL.

**Situation:** moving or stationary, grappled, mounted, high ground, cover,
flanking, underwater, distance, give-up-action interruption.

## 2. Skill values

| Skill | Value |
|---|---|
| Strike, Defend | Melee |
| Grapple | Melee + (STR − 10) + 5 × SM |
| Force | (STR − 10) + 5 × SM |
| Accuracy | Ranged |
| Reflex | Ranged − 1 × SM |

Size 1–7: DM 0.5/0.75/1/1.5/2/3/4 · SM −2/−1/0/+1/+2/+3/+4 ·
RM 1/1/1/1.5/1.5/2/2.5. Gear is size 3; scaling multiplies damage and RES by
DM, reach by RM. Oversized weapon (one size up): +1 AP per attack and STR − 5
in every STR contribution (base, heavy, braced, hook). Two sizes up:
impossible. One size smaller: STR + 5 with it. No ranged weapon larger than
the wielder.

## 3. Declare, then roll

**Declared before the roll:** attack variation(s) and location.

**Location penalty:** chest 0 · leg 0 · head −5 · hand −10. Creature
vulnerabilities work the same way, per their description.

**To-hit modifiers:** heavy II −2, heavy III −3 · mounted ≈ −2 (melee;
Accuracy only while the mount moves) · reaction after a give-up action −2 ·
sensory penalties (IL −1 per 10, Obfuscated/Muffled −3, stealth section) on
Strike, Defend, Accuracy, Reflex · high ground: +2 to melee defense for both
sides · routing pursuers +2 Strike/Accuracy.

**Ranged distance:** no penalty under 10 m; Throw/Shoot −2 per 20 m, Snipe
(+2 AP, may fire outside the combat area) −1 per 20 m, Quick Shot (−1 AP,
needs STR ≥ requirement + 2) −3 per 20 m. Outside the combat area: 3 × the
shot's distance penalty. Vertical range is half. Ranged attacks require
concentration.

**Opportunity attack** (reaction, no to-hit bonus): triggered by
concentration actions (at declaration), standard actions, standing up in
melee range, or moving toward a melee weapon within its range; also by
flanking. Only a defense may answer it. Sweeping attacks do not trigger it.

**Braced** (reaction vs a target moving toward the weapon, or action while
mounted and running) and **hook** (action, or reaction vs a running target
moving away) fire on movement **between two spaces both inside the weapon's
range**.

**DL:** melee → Defend if the target spends AP, else SD. Ranged → Reflex if
it reacts, else SD. **SD = −5 − SM stationary, −2 − SM moving**; immobile
−5 − SM; no penalty pushes a defense below SD. Evasive jump adds +AGI/2.
Grappled: only intercept. Mounted defender: only block and intercept.
Assassinate only against SD.

**Score** = d10 (0–9) + skill + mods − DL. The exploding die applies only
where a skill or ability says so — not to attacks by default. Safe: 2d10 keep
nearest 5; risky: keep farthest.

**Degrees for attacks:** miss < 0 ≤ graze < 5 ≤ hit. An attack has no
critical; points past a hit are **HOP = score − 5**. Explosions are the
exception: zones give critical 150% / hit 100% / graze 50%.
**Piercing:** a graze is a miss.

## 4. What the defense does with the degree

A hit always lands at full damage.

| Defense | AP | Graze | Miss |
|---|---|---|---|
| None (SD) | 0 | 50% | nothing |
| Evade | 2 | 50% | nothing |
| Evasive jump | 3 + 1 STA | 50%; +AGI/2 to Defend, jump away | nothing |
| Block (DEF) | 2 | absorption at block value | absorption at 1.5 × block value |
| Block with shield | 2 | as Block, **+Cover to Defend** | as Block |
| Intercept (DEF, short range) | 3 | stopped unless attacker Force ≥ defender + 5 | stopped unless attacker Force ≥ defender + 8 |
| Reflex evasion (ranged) | 3 (spent as movement) | may jump for cover; 50% if not | nothing; may movement surge |
| Guard (ranged, self or adjacent) | 2 | absorption at block value, +Cover to Reflex | absorption at 1.5 × block value |

**Block value** = 2 × STR one-handed, 4 × STR two-handed or shield, × DM.
**Absorption:** absorption value ≥ damage → 0; ≥ damage/2 → half; else full.
App ruling (not in the book): a block absorbs no more than the object's RES —
flag if it matters. Fast ranged weapons can only be blocked by a shield; slow
ones can be guarded with weapons; UF gets +2 HOP on a hit. An intercept that
stops the attack may start a grapple (grapple-property attack) or disarm
(+1 AP +1 STA). Sweeps pass to the next target by absorption, a character's
absorption value being its T2 threshold.

## 5. Damage

1. **Base:** table Blunt and Cut × weapon DM. Melee adds +0.5 × STR × DM to
   both. Ranged rows are used as listed (STR is a requirement, not a bonus).
2. **Variations** (add to blunt **and** cut):
   heavy I +0.5 × STR × DM (+1 AP) · heavy II +1 × STR × DM (+2 AP +1 STA,
   −2) · heavy III +1.5 × STR × DM (+3 AP +1 STA, −3) · braced +1.5 × STR ×
   DM (+2 AP +1 STA on a hit; triggers a trample) · hook +STR/2 × DM vs
   evasive jump, +STR × DM vs running (+2 AP +1 STA on a hit) · sweeping
   +1 AP, no bonus · assassinate +1 AP, +5 HOP (precise, short range).
   Heavy I–III means heavy I is the minimum. Variations combine, except
   braced and hook, which combine with nothing.
3. **Degree / defense** from step 4.
4. **Underwater:** non-grapple damage halved; fire/radiant/acid halved;
   projectile range 3 m; explosions half radius, blunt doubled.
5. **What cuts:** the weapon cuts if its hardness exceeds the target's
   (liquid 1 < fabric/flesh 2 < wood/bone/horn 3 < metal/rock 4; weapons are
   metal unless stated). If it cannot cut, **cut damage is halved** (Bust
   restores it vs same hardness). Metal armor cannot be cut without
   penetrating.
6. **Which counts:** compare blunt vs Protection and cut vs RES (burn,
   radiant, electric, corrosive vs Insulation); the type that gets furthest
   past its armor sets the injury, but the effects of both apply (blunt tier
   still interrupts/stuns).

## 6. Tier, IL, bleed, effects

Threshold for tier N = **armor + N × TGH**. Shortcut:
**tier = floor((damage − armor) / TGH)**, capped at 5; below armor → no
injury. Any tier reached is at least 1 IL.

| Tier | IL | Bleed |
|---|---|---|
| T0 | 1 | 0 |
| T1 | 5 | 0 |
| T2 | 10 | 1 |
| T3 | 20 | 2 |
| T4 | 30 | 3 |
| T5 | 50 | 4 |

- **Bleed** (blunt and cut): +1 IL per intensity for every STA spent and at
  the beginning of every round; at combat/chase end deals 3 × intensity and
  stops.
- **Piercing:** half IL per tier; cannot amputate; breaks objects only at
  > 3 × RES.
- **Electric:** vs INS, half IL, interrupts/stuns like blunt. Cut at T0+
  applies poison and electric as if unarmored.
- **Burning/radiant:** vs INS, half IL; counter += incoming, test the total,
  then halve the counter; burns again each round start.
- **Corrosive:** vs INS; T0–T1 leaves the target corroding at that tier
  every round (armored targets only).
- **Interruption:** T1+ blunt or electric → the current action/movement is
  lost with its spent AP/STA (running and jumping exempt).
  **Stun:** T3+ blunt or electric → interruption and −2 AP.
  **Basher:** interrupts at T0, stuns at T2.
- **Thresholds:** −1 per 10 IL to STR/AGI/STA uses and sensory skills;
  collapse (immobile) at 40; death above 50.

**Sanity invariants** (attacker STR = defender STR): the base melee bonus and
each heavy degree are +1 TGH = one tier; heavy III and braced = +3 tiers.

## 7. Location and wounds

| Location | Body cap | Notes |
|---|---|---|
| Chest | none | default |
| Leg | T3 | T3 blunt/cut → broken leg (lame, 20 IL wound); T5 → amputated |
| Hand | T2 | no armor without gauntlets; T2 blunt/cut → broken hand (useless, 10 IL wound); T4 → amputated |
| Head | none | interrupts become stuns; stuns become unconscious ≥ 1 min; T4 → instant death; closed helmet: −5 HOP |

Any location: T4 blunt → Shocked (immobile, 5 IL wound). The body takes the
capped tier's IL and bleed; the wound reads the real tier. Wound IL is tracked
separately. Piercing cannot amputate.

**Hand switch:** 3 HOP after the roll, if the target blocked or intercepted
without a shield.

## 8. HOP purchases

After a hit, in any affordable combination:
- **Bust** — deflection HOP; penetrating (piercing) weapons; full cut vs
  same hardness (e.g. metal armor).
- **Slice** — deflection HOP each, repeatable; +25% cut (bladed) or +12.5%
  (others).
- **Smash** — 1 HOP each; +1 × DM blunt.
- **Hand switch** — 3 HOP (step 7).

Deflection: body +4; armor per table (+4 to +8); pitted −1. Penetrating+
customisation: +1/+2 vs deflection. Sharp: +x HOP on a hit; dull forbids
bladed.

**Hook knockdown:** a hook attack aimed at legs or head makes its post-hit
effect a knockdown attempt, which cannot be reacted against if the target is
running or jumping.
**Trample / braced crash:** Force vs Force; a runner adds movement speed;
target may pay 2 AP + 1 STA for +3 (automatic from a braced attack); head hit
+3. Difference < 5 → both stunned, higher blocks or passes, draw blocks.
≥ 5 → winner not stunned, a losing target falls prone.

**Gear breakage:** cut or blunt ≥ RES (and the item can be cut) → 1-in-6;
both ≥ RES → 50%; any ≥ 2 × RES → breaks. Broken armor = pitted.

## 9. Morale (combat.tex "Morale")

Will vs **DL = 0 + aggravating factors**: injured +1 per injury penalty ·
immobile +3, grappled +2 · total sensory impairment within 10 m +2 ·
suffocating +3 · STA < 3 +2 · pressure (GM). Triggered at round start when
factors ≥ 3, under afraid/enraged/confused, or by Intimidation/Taunt
(+1 + Charisma/2; highest only). Rally lowers allies' next DL by the same.
Normal, safe or risky as the player chooses. Graze = afraid (enraged for a
Taunt); miss = limit stress action (only with an enemy within 30 m; resolved
at round start, worst result first). Social actions cost 5 AP, count as Rest,
resolve at round end. Immobile and unconscious characters don't test.

## 10. Expected-damage mode

1. Plain d10 0–9 unless an ability makes the test exploding (then expand
   9/0 chains with d6, continuing on 6, to ±30).
2. P(hit/graze/miss) from score − DL ≥ 5 / ≥ 0 / < 0; piercing graze → miss.
3. Damage per degree is deterministic: report per degree damage, tier, IL,
   bleed, effects, wound; then expected IL per attack and per AP, mean HOP on
   a hit.
4. Sweep DL (−5 … +15) or armor class, not a single point.
5. State assumed STR, proficiencies, DM, TGH up front.
6. **Ladder report:** each weapon as standard / h1 / h2 / h3 / braced vs
   flesh, fiber, flexible metal, rigid, reinforced.

## 11. Known gaps to flag, not resolve

- `gear.tex` Sharpening gives "+1 on a hit and +2 on a crit", but attacks
  have no critical; "Sharp" condition says "+x HOP".
- Ranged "Maximum distance penalty is 3x the attack's distance penalty" —
  unclear what it caps.
- Block absorption capped at RES exists only in the app.
- Hook knockdown: whether it is a grapple-maneuver test (crit to drop) or
  automatic is unstated.
