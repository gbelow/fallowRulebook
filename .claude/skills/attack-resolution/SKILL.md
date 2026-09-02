---
name: attack-resolution
description: >-
  Simulate attack resolution in the Fallow rulebook — apply any attack type with
  any modifiers and state the damage dealt against a target wearing given armor.
  Use when asked to calculate or simulate damage, resolve an attack, compare
  weapons/armor, or compute expected damage per attack or per AP.
---

# Attack Resolution Simulator

Resolve any attack end-to-end: attack roll → degree → damage → armor → injury
tier → IL/wounds. The user's typical question is "what does weapon X do against
armor Y", so always finish with concrete damage and IL numbers, not just a
miss/hit chance.

## 0. Source of truth

Rules change as the user edits the book. Before resolving:
- Weapon/armor/shield stats: read the current tables in `gear.tex` (never from
  memory — the user is actively updating these tables).
- Test resolution and attack/defense/SOP rules: `play.tex` ("How skills work")
  and `combat.tex`.
- Skill value formulas and size multipliers: `creating.tex`.

## 1. Gather inputs

Ask for (or assume defaults and state them) per combatant:

**Attacker:** STR, DEX, size (→ DM/SM/MM), Melee or Ranged proficiency level,
Strike/Accuracy skill bonus, weapon + which attack form (row in the weapon
table), attack variation, armor/condition of the weapon, relevant afflictions.

**Defender:** size (→ SM, DM), armor (name → RES, Protection, Deflection,
Insulation), TGH (default 0.5 × STR × DM), shield, defense action (evade /
evasive jump / block / intercept / guard / no defense), Defend or Reflex value
or SD, IL so far, gauntlets/closed helmet.

**Situation:** distance (ranged), mounted, high ground, cover, underwater,
flanking, aimed location, grappled.

## 2. Skill values

Skill value = proficiency bonus + skill bonus (talent gates XP cost, not value).

| Skill | Value |
|---|---|
| Strike | Melee + strike bonus |
| Defend | Melee + defend bonus |
| Grapple | Melee + STR − 10 (+5×SM) |
| Accuracy | Ranged + accuracy bonus |
| Reflex | Ranged + Awareness (+ −1×SM) |

Size table (size 1–7): DM 0.5/0.75/1/1.5/2/3/4 · SM −2/−1/0/+1/+2/+3/+4 ·
MM 0.5/1/1/1.5/1.5/2/2.5.

## 3. Assemble the attack roll

**Skill value, then add situational modifiers:**

Melee (to hit): opportunity attack +2 · heavy II −2, heavy III −3 · small weapon
in a grapple +2 · mounted −2 (mount-dependent) · injury/sensory penalties (−1
per 10 IL; Strike/Defend are sensory) · other agreed modifiers.

Ranged (to hit): the text defines no distance-based to-hit falloff — range is
bounded only by the weapon's max range and Shoot's 30m cap (Snipe removes the
cap for +2 AP; vertical range = half horizontal). Quick Shot has no to-hit
penalty in the text, only ≤10m range and −1 AP. Mounted & moving −2. Untrained
bows: +3 AP per shot instead of a penalty. Shots >50m fired from outside the
combat area (chase/skirmish only) take −5.

**DL = defender's defense value:**
- Melee: Defend value if actively defending; else SD.
- Ranged: Reflex value if reacting (evasion/guard); else SD.
- SD = −2 − SM (moving) or −5 − SM (stationary). No penalty can push a defense
  below SD.
- Evasive jump adds +AGI/3 to the defense test.

**Degrees of success** (score = d10 + skill value + mods − DL):
≥ +10 critical · ≥ +5 hit · ≥ 0 graze · else miss. Round every fraction down.

**Exploding die:** d10 = 10 → add 10 + 1d6, keep rolling d6 while it shows 6
(keep adding). d10 = 1 → adds 0, then subtract 1d6, keep subtracting while
rolling 6. Safe test: roll 2d10, keep the one closest to 5 (tie: average or
reroll). Risky: keep the farthest from 5. Only when the rules allow it.

**AP/STA cost** (track it; users care about damage per AP): strike 3 AP ·
heavy I +1AP · heavy II +2AP+1STA · heavy III +3AP+1STA · sweep +1AP · braced
+2AP+1STA · assassinate +1AP · ranged: AP from weapon row (e.g. "3+5" = shot +
reload, e.g. crossbow "4+4" = shot then reload) · quick shot −1AP · snipe +2AP.
Defense: evade 2AP · evasive jump +1STA ·
block 2AP · intercept 3AP · reflex evasion 2AP.

## 4. Compute damage

1. **Read the weapon row** (Blunt and Cut columns).
   - Plain numbers (e.g. Cut 16) are multiplied by the attacker's weapon DM.
     This scaling applies to any extra damage effects added to the attack.
   - Entries like "STR" or "0.5x STR" use the attacker's STR (× DM if the
     wielder is not size 3 — oversized weapons also use STR−5 and +1 AP).
   - Any non-plain multiplier in the Cut column (e.g. "1.5x", "2x") is a
     mistake in the tables — all damage values are plain numbers. Flag it to
     the user instead of computing with it.
2. **Add variation bonuses** (these increase cutting damage too): heavy I
   +0.5×STR, II +1×STR, III +1.5×STR · braced +1.5×STR · hook +STR/2 (vs
   evasive jump) or +STR (vs running) · extra cut SOP +1×DM per SOP (bladed
   only, scales slowly — 1 per SOP vs TGH per heavy degree). Smash adds no
   damage — it is SOP-only (stun/interrupt, step 6).
3. **Degree multiplier:** graze 50% (round down) · miss 0 · hit and crit 100%
   (a crit's benefit is a bigger SOP pool, not more base damage; explosions are
   the exception: crit 200%, hit 100%, graze 50%).
4. **Pick damage type:** the attack can cut only if the weapon's material
   hardness exceeds the target's surface hardness (liquids 1, flesh/fabric 2,
   wood/bone/horn 3, metal/rock 4). If it can cut, the attacker chooses the
   more advantageous type — Cut vs armor RES or Blunt vs armor Protection,
   whichever yields the better tier against that armor. If it cannot cut, the
   attack is blunt. Metal armor can never be cut without the penetrating
   property (SOP, cost = deflection) — regardless of the Cut value.

## 5. Apply armor and convert to injuries

Compare final damage to thresholds **armor + N × TGH**, where "armor" is
Protection for blunt and RES for cutting. Shortcut: **tier =
floor((damage − armor) / TGH)**, capped at T6; damage below the armor value
deals no IL.

| Tier | Threshold | IL | Wound |
|---|---|---|---|
| T0 | armor | 1 | 0 |
| T1 | armor+TGH | 5 | 0 |
| T2 | armor+2×TGH | 10 | 50% |
| T3 | armor+3×TGH | 20 | 100% |
| T4 | armor+4×TGH | 30 | 100% |
| T5 | armor+5×TGH | 40 | 100% |
| T6 | armor+6×TGH | 50 | 100% |

**Key invariants (use these to sanity-check any matchup):**
- Each heavy degree adds +TGH damage (0.5×STR×DM) = **exactly one tier at any
  STR**. Braced (+1.5×STR) = same as heavy III = +3 tiers over base.
- Piercing weapons: graze = miss, **half IL but full tier effects** (wound %,
  bleed cures, and T0/T1 poison delivery) — so piercing values run one tier
  higher than blunt/cut of equivalent lethality.
- Penetrating "bust window": cutting metal needs damage > RES just to split
  rings; real damage tiers need another ~+5–10 over RES. Mail-breaker weapons
  are tuned to land in that window vs flexible metal and at T0–T1 vs plate.

Highest tier whose threshold the damage meets or exceeds. Notes:
- Cutting that does not exceed armor RES is stopped by the armor (no IL to the
  wearer); check gear breakage instead (step 6).
- Piercing weapons: grazes count as misses, and hits deal half the IL.
- Rigid armors with two RES values (e.g. 20/10): armor-bypass SOP hits the
  inner layer.
- Burn/radiant/corrosive/electric defend by INS(ulation) instead, per gear.tex.
- Wound chance is rolled per the Wound % column; head hits: any wound or stun
  → unconsciousness, blunt T1 50%/T2 100% wound, T4+ 50% instant death; hand
  max 5 IL; leg max 10 IL.
- IL then gives −1 injury penalty per 10 IL (base IT = 10); collapse at 40 IL,
  death past 50 IL (4×/5× IT).

## 6. After-effects (mention when they trigger)

- **SOP** = points of score above the defender's DL on a hit or crit. Spend on:
  armor bypass (cost = target's deflection; precise weapons only; hits the
  inner layer of rigid armor — no effect vs non-rigid) · penetrating
  (cost = deflection; lets the weapon cut equal hardness, i.e. metal) ·
  extra cut (1 SOP = +1×DM cut, bladed) · smash (cost = deflection; stun if
  ≥T1, interrupt if ≥T0 — smash-property weapons
  only) · localized damage (head 5, hand 10 or 5 vs blocking target, leg 0).
  Weigh SOP purchases against their full cost: deflection points + to-hit
  penalties of heavy attacks make top-end results commitment+luck events, not
  routine output.
- **Interruption:** T1+ blunt or electric, or push → lose action, min 2 AP
  (smash/stun min 4).
- **Gear breakage (optional rule):** cutting or blunt ≥ RES → 1-in-6 break,
  both ≥ RES → 50%, either ≥ 2×RES → instant. Broken armor = pitted.
- **Bleed:** T2+ wounds to chest/head bleed +1 IL per round per cure owed.
- **Morale:** T1+ injury lets the enemy side intimidate; injuries raise the
  next morale DL (IL > 10 → +3).

## 7. Expected-damage mode (weapon vs armor comparisons)

For "which weapon is better against this armor":
1. Compute the exact distribution of the exploding die (write a tiny Python
   script; enumerate d10 outcomes, expand 10/1 chains recursively to a
   truncation like ±30).
2. P(crit/hit/graze/miss) = P(score−DL ≥ 10 / ≥5 / ≥0 / <0). Apply piercing
   graze→miss here.
3. Damage is deterministic per degree → tier, IL, and wound chance are
   deterministic per degree. Report a table: per degree → damage, tier, IL,
   wound %. Then expected IL per attack = Σ P(degree) × IL(degree), and
   expected IL per AP (divide by the attack's AP cost). Include SOP yield
   (average SOP on hit+) since it buys effects, not damage.
4. Vary DL: sweep the defender DL (or armor set) across a plausible range
   (e.g. −5..+15) rather than one point, or the comparison is noise.
5. State assumed inputs (STR, proficiencies, DM, TGH) up front.
6. **Ladder report** (preferred for calibration work): since heavy degrees and
   braced are exact tier steps, report each weapon form as a tier ladder —
   standard / h1 / h2 / h3 / braced (+smash where property allows) — against
   each armor class (flesh, fiber, flexible metal, rigid, reinforced).
   Outliers are rows where the ladder jumps two tiers or crosses the design
   bands (normal attacks T1–T2 on armored targets; plate T2–T3 max from
   committed attacks; no one-shot T5 on flexible metal except committed
   −3-to-hit events; cloth/flesh freely cut at T3+).
   Calibration stance: every weapon and armor is a concept, not a fixed
   number — variations are made at the table's discretion. The bands above are
   design guidelines for spotting accidents, not a prescription; the goal is
   that each stat can be tuned independently without anything becoming
   overpowered.

## 8. Interpretations to flag

These are ambiguous in the text — use the reading below and say so when it
matters:
- Armor is a threshold band (step 5), not subtraction; Protection vs blunt,
  RES vs cutting.
- SOP = score − DL, only on hit/crit.
- Melee crits add no extra damage beyond SOP; only explosions crit at 200%.
- Ranged accuracy is flat within weapon range by design — confirmed with the
  user (2026-09-02): there is no distance-to-hit falloff, only hard range
  caps (weapon max range, Shoot's 30m limit, Snipe removing it). spells.tex's
  "distance penalty" wording (e.g. Lasers: "does not receive any distance
  penalty up to 50m") is loose phrasing, not evidence of a hidden formula.
  Do not invent a falloff number.
- Penetrating's SOP cost (= target's deflection) has two distinct payoffs:
  it lets cutting damage apply against same-hardness (metal) targets, *and*,
  for that same cost, it separately lets the attack ignore fiber armor's RES
  entirely (combat.tex, Success Overflow / Penetrating) — the two are not
  additive purchases, either payoff costs one deflection-worth of SOP.