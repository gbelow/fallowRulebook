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

Resolve an attack end-to-end: declare → roll → degree → damage → armor →
tier → IL, bleed, wound, location effect → overflow purchases. The user's
usual question is "what does weapon X do against armor Y", so always end with
concrete tier/IL numbers, not just a hit chance.

## 0. Source of truth

The user edits the book between messages. Before resolving, re-read the
current text — never work from this file's numbers alone:
- Weapon, shield, armor tables and weapon properties: `gear.tex`.
- Test ladder and exploding die: `play.tex` ("How skills work").
- Attacks, defenses, damage tiers, overflow effects, localized damage, wounds,
  afflictions: `combat.tex` (Damage and Injuries, Melee Combat, Ranged
  Combat).
- Skill formulas, size table, SD: `creating.tex`.

Terminology: the user now calls overflow points **HOP (Hit Overflow Points)**.

## 1. Inputs (ask, or assume and state)

**Attacker:** STR, size (→ DM/SM/RM), Melee or Ranged proficiency, Strike or
Accuracy bonus, weapon row (Blunt, Cut, properties, range), attack variation,
declared location, weapon condition (sharp/dull), afflictions (IL penalty).

**Defender:** size, armor row (RES, Protection, Insulation, Deflection),
gauntlets / closed helmet, TGH (default 0.5 × STR × DM), shield, chosen
defense (evade, evasive jump, block, intercept, reflex evasion, guard, none →
SD), Defend or Reflex value, current IL.

**Situation:** moving or stationary, grappled, mounted, high ground, cover,
flanking, underwater, distance.

## 2. Skill values

| Skill | Value |
|---|---|
| Strike | Melee + strike bonus |
| Defend | Melee + defend bonus |
| Grapple | Melee + (STR − 10) + 5 × SM |
| Force | (STR − 10) + 5 × SM |
| Accuracy | Ranged + accuracy bonus |
| Reflex | Ranged + Awareness − 1 × SM |

Size 1–7: DM 0.5/0.75/1/1.5/2/3/4 · SM −2/−1/0/+1/+2/+3/+4 ·
RM 0.5/1/1/1.5/1.5/2/2.5. Weapons scale damage and RES by DM, reach by RM.
Oversized weapon (one size up): +1 AP per attack, STR − 5 for every STR
contribution (heavy, braced, hook). Two sizes up: impossible.

## 3. Declare, then roll

**Declarations happen before the roll:** attack variation, and location.

**Location penalties (to the attack test):** chest 0 · leg 0 · head −5 ·
hand −10. Separately, any attack can *switch* to the hand after the roll for 3
HOP if the target blocked or intercepted without a shield (the accidental hand
hit). Vulnerabilities on creatures work the same way, per their description.

**Approach triggers (reactions, no preparation cost):** opportunity attack
(+2, normal AP cost) and braced attack both fire on a step **between two
spaces that are both inside the weapon's range** — a long I weapon triggers
on 2 m → 1 m, a long II on 3 m → 2 m and 2 m → 1 m; stepping from outside
range to the edge of range (3 m → 2 m against long I) triggers nothing. A
braced attack can trigger only once per turn (anyone's turn), so several per
round is legal. The target may cancel the step and reuse its AP to defend.

**To-hit modifiers:** opportunity attack +2 · heavy II −2, heavy III −3 ·
mounted ≈ −2 (accuracy only while the mount moves) · slow ranged weapon −2 if
the target defends actively · high ground: both sides +2 to melee defense ·
bad visibility −2 · IL penalty −1 per 10 IL (Strike, Defend, Accuracy, Reflex
are all sensory) · ranged >50 m from outside the combat area −5. There is no
distance falloff inside weapon range — range is capped, not decayed (Shoot
≤30 m, Snipe +2 AP any distance, Quick Shot −1 AP ≤10 m).

**DL:** melee → Defend value if the target spends AP, else SD. Ranged → Reflex
value if reacting, else SD. **SD = −5 − SM stationary, −2 − SM moving**; no
penalty can push a defense below SD. Evasive jump adds +AGI/3 to Defend.
Grappled targets cannot evade or block, only intercept. Assassinate only
works against SD.

**Score** = d10 + skill + mods − DL. Exploding die: a 10 adds 1d6 and keeps
adding while the d6 shows 6; a 1 adds nothing and subtracts 1d6, continuing
on 6. Safe test: 2d10 keep the one nearest 5; risky: keep the farthest.

**Degrees for attacks:** miss < 0 ≤ graze < 5 ≤ hit. There is no critical on
an attack — everything above +5 is **HOP = score − 5**. (Explosions are the
exception: their zones give crit 200% / hit 100% / graze 50%.)

**Piercing weapons:** a graze is a miss.

## 4. What the defense does with the degree

Hits always land at full damage. Graze/miss outcomes depend on the defense:

| Defense | AP | Graze | Miss |
|---|---|---|---|
| None (SD) | 0 | 50% damage | nothing |
| Evade | 2 | 50% | nothing |
| Evasive jump | 2 + 1 STA | 50%, +AGI/3 to Defend | nothing |
| Block (DEF item) | 2 | damage − block value | damage − 1.5 × block |
| Block with shield | 2 | as Block, **+Cover to Defend** (all shields +2) | as Block |
| Intercept (DEF, short range) | 3 | stopped unless attacker Force ≥ defender + 5 | stopped unless attacker Force ≥ defender + 8 |
| Reflex evasion (ranged) | 2 | 50%, may jump for cover | nothing |
| Guard (shield vs ranged) | 2 | damage − block value | damage − 1.5 × block |

Block value = STR one-handed, 2 × STR two-handed or shield, scaled by size.
Shield Cover is a test bonus to Defend when blocking with the shield and to
Guard; it is the shield's only to-hit effect (2026-09-17: +2 for every
shield; the tower's extra is full cover vs ranged, not more Cover). It does
**not** apply to Intercept (only the Defensive Advance
ability adds it there) and never applies in a grapple, where blocking is
impossible. Fast ranged weapons can only be
blocked with a shield. A blocking object with damage ≥ its RES risks breaking
(step 8).

## 5. Damage

1. Read the weapon row: Blunt and Cut are plain numbers keyed to STR 10,
   multiplied by the weapon's DM. If a row shows `STR` or a multiple, flag it
   rather than computing — the user removed those.
2. Add variation bonuses (they apply to blunt **and** cut):
   heavy I +0.5 × STR (+1 AP) · heavy II +1 × STR (+2 AP +1 STA, −2) ·
   heavy III +1.5 × STR (+3 AP +1 STA, −3) · braced +1.5 × STR (+2 AP +1 STA,
   reaction vs approach or mounted charge; also triggers trample) · hook rider
   (+1 AP +1 STA bought **after** the hit) +STR/2 vs evasive jump, +STR vs
   running. Heavy I–III on a row means heavy I is the minimum attack.
   Braced and hook combine with nothing.
3. Extra cut (HOP): +1 × DM cut per HOP, bladed only; +2 × DM if bladed and
   piercing; sharp condition +1.5 × DM (not for bladed + piercing); dull
   forbids extra cut.
4. Degree multiplier: hit 100% · graze 50% (round down) · miss 0.
5. Underwater: non-grapple damage halved; fire/radiant/acid halved.
6. **Type:** the weapon cuts only if its hardness exceeds the target's
   (liquid 1 < fabric/flesh 2 < wood/bone/horn 3 < metal/rock 4). Metal armor
   cannot be cut without buying **Penetrating** (HOP = deflection, penetrating
   weapons only). If it can cut, use the better of Cut vs RES or Blunt vs
   Protection; otherwise blunt.

## 6. Tier, IL, bleed

Threshold for tier N = **armor + N × TGH** (armor = RES for cutting,
Protection for blunt, Insulation for burn/radiant/corrosive/electric).
Shortcut: **tier = floor((damage − armor) / TGH)**, capped at 5; below the
armor value → no injury.

| Tier | IL | Bleed |
|---|---|---|
| T0 | 1 | 0 |
| T1 | 5 | 0 |
| T2 | 10 | 1 |
| T3 | 20 | 2 |
| T4 | 30 | 3 |
| T5 | 50 | 4 |

- **Bleed:** +1 IL per intensity for every STA spent and at every round end;
  at combat end deals 3 × intensity and stops. Vicious doubles it.
  Cauterization removes 2.
- **Piercing:** half IL per tier, rounded down (0/2/5/10/15/25; tier effects,
  wounds, KO, and bleed unchanged), cannot amputate.
- **Electric:** half IL, interrupts at T1+, stuns at T3+; ignores INS if the
  weapon also does T0+ cutting. Burn/radiant T0+ → burning. Corrosive T0–T1 →
  corroding at that tier every round until armor is removed.
- **Interruption:** T1+ blunt or electric, or a push → lose the action, min
  2 AP. Stun = interrupt with min 4 AP.
- **Injury effects:** −1 to STR/AGI/STA uses and to sensory skills per 10 IL;
  collapse (immobile) at 40; death past 50. One T5 is 50 IL = collapse, not
  death, unless IL was already above 0.

**Invariants for sanity checks:** each heavy degree = +TGH = exactly one tier
at any STR; braced = heavy III = +3 tiers. Every 5 points of overflow is worth
one location step (leg → head) or one deflection-priced effect on an unarmored
target.

## 7. Location and wounds

Location is declared in step 3. Apply after the tier is known:

| Location | Body cap | Effect |
|---|---|---|
| Chest | none | Shocked wound on T4 blunt + smash (immobile, 5 IL wound) |
| Leg | T3 (20 IL, bleed 2) | T3 blunt/cut → broken leg (lame, 20 IL wound); T5 → amputated (no heal) |
| Hand | T2 (10 IL, bleed 1) | no armor unless gauntlets; T2 blunt/cut → broken hand (useless, 10 IL wound); T4 → amputated (no heal) |
| Head | none | T3 blunt/cut/electric, or any stun → unconscious ≥1 min; T4 → instant death; armor bypass always hits flesh; closed helmet forbids bypass |

"Body cap" means the body receives the capped tier's whole row (IL and
bleed); the wound still reads the real tier. Wound IL is tracked separately
and heals only by Medicine (Bone Setting 0/1/2/2 per sleep) or magic.
Lame = careful movement and crawling only.

Head math worth remembering: Smash (deflection HOP, needs T1) + head = KO at
T1 damage — the sap. Assassinate (vs SD, +1 AP, short precise weapon, auto
bypass) + head −5 is the reliable surprise KO/kill.

## 8. Overflow purchases (HOP)

Spend HOP after a hit, in any combination the attacker can afford:
- **Armor bypass** — cost = target deflection; precise weapons; hits the inner
  RES of layered armor (e.g. 16/10 → 10). Unlayered armor cannot be bypassed.
- **Penetrating** — cost = deflection; penetrating weapons; lets the attack cut
  same-hardness targets (metal). Against fiber armor, or once already
  penetrating, behaves like extra cut instead.
- **Extra cut** — 1 HOP each, rates in step 5.3.
- **Smash** — cost = deflection; stun if the damage is T1+.
- **Hand switch** — 3 HOP if the target blocked/intercepted without a shield.

Deflection: body +4; armor +5 to +8 per the table; pitted −2. The head and
Shocked compete only through the roll now, not through HOP.

**Trip (hook attack):** no second roll. Attacker Force vs target Balance +
Force; moving party's speed is added to the attacker; head or leg targeted
+5; higher wins → prone. **Trample:** Force vs Force; runner adds speed;
higher → target back one space, +5 → prone; head targeted +5.

**Gear breakage (optional):** damage ≥ RES → 1-in-6; both types ≥ RES → 50%;
any damage ≥ 2 × RES → breaks. Piercing only breaks at > 2 × RES. Hardness 1–2
never breaks anything. Broken armor = pitted.

**Morale (2026-09-17):** tests happen at the **start of the round** (so the
limit action has AP to run on) and only when triggered: aggravating factors
5+ (injured +2 per penalty, out of STA +2, burning/suffocating +5, oblivious
+3, disoriented +2), while afraid / enraged / confused, or after an
Intimidation / Taunt (+1 + Charisma/2 as a factor; Charisma is a 0–5
proficiency, so +1 to +3). The die explodes as usual,
but the player may roll the morale test **safe or risky** (2d10, keep the
nearest / farthest from 5). Safe roughly quarters the rout chance but pushes
results into the afraid band when Will < DL; risky does the reverse. With
Will ≥ DL, safe is strictly better. Graze = afraid (no voluntary combat surge), miss = the character's
**limit action** (Coward, Violent, Tanatosis, Abusive, Traitor, Martyr —
`creating.tex`). Rest and social actions (5 AP) resolve at end of round; Rest
may take AP negative if the next round starts positive.

## 9. Expected-damage mode

For "which is better against armor Y":
1. Enumerate the exploding d10 exactly (small Python script; expand the 10/1
   chains recursively to ±30).
2. P(hit/graze/miss) from score − DL ≥ 5 / ≥ 0 / < 0; piercing graze → miss.
3. Damage per degree is deterministic, so tier, IL, bleed and wound are too.
   Report per degree: damage, tier, IL, bleed, wound; then expected IL per
   attack and per AP, and mean HOP on a hit.
4. Sweep DL (−5 … +15) or armor class rather than a single point; a single DL
   is noise.
5. State assumed STR, proficiencies, DM, TGH up front.
6. **Ladder report** for calibration: each weapon form as standard / h1 / h2 /
   h3 / braced against flesh, fiber, flexible metal, rigid, reinforced. Design
   bands: normal attacks T1–T2 on armored targets; plate T2–T3 from committed
   attacks; no one-shot T5 on flexible metal outside −3-to-hit events;
   cloth/flesh freely cut at T3+. Bands are for spotting accidents, not
   prescriptions — every weapon and armor is a concept the table may vary.

## 10. Settled readings — do not re-litigate

- Armor is a threshold band, not subtraction.
- Attacks have no critical; a "crit" trigger written on an attack simply
  never fires and is not a defect.
- Regular arrows doing nothing to mail is correct; bodkins carry penetrating.
- Head death at T4 is intended; the head is the anti-large-creature tool.
- Bleed is a clock, not a disability; bleeding while unconscious is fine.
- Gauntlets and closed helmets are separate purchases for any armor.
- Location effects being nearly free against SD and rare against an active
  defender is the system working ("defending matters more as fighters get
  better").
- A steep penalty on a rare shot (hand −10) is a skill shot, not a dead
  option.
- Fall lethality (miss → head) is intended; only the DL choice is at issue.
- Forced movement never scales with the roll; flat distance.
- One skill per action: a secondary effect compares characteristics (Force,
  Balance), never the attack skill again, and HOP buys declarations, not
  bonus points on that comparison.
