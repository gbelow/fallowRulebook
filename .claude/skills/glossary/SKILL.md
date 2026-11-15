---
name: glossary
description: >-
  Glossary of Fallow jargon and abbreviations (AP, STA, DL, HOP, IL, TGH, SD,
  DM/SM/RM/VM, IB, ET, EA, RES, prot, INS, bulk, burden, surges, afflictions,
  renown/honor/trust, convictions, etc.) with a one-line meaning and the .tex
  file that defines each. Use whenever a term or abbreviation in the rulebook,
  the companion app, or the user's message is unfamiliar or ambiguous, before
  reading whole chapters to find it.
---

# Fallow glossary

One line per term. Definitions are pointers, not rules: for exact numbers,
open the cited file. Deeper references: `skill-test-core`, `game-loops`,
`size-table`, `advancement`.

For exact procedures, prefer the companion app
(`C:\Users\Administrator\code\chargenfallow\app\domain`, read-only), which
implements every rule and cites the .tex lines. Numbers live in `tables.ts`;
scene mechanics are in `scene/rules/<mechanic>.ts` (attack, damage, grapple,
morale, stealth, chase, cast…); test resolution is in `play/test.ts`.
Exploration is in `exploration/`, downtime in `downtime/`. Grep the term
there before trusting the `attack-resolution` skill, which is older than the
app.

## Core resolution — `play.tex`
- **Skill test** — d10 (0–9, 0 counts as 0) + skill value vs DL. Round fractions down everywhere.
- **DL (difficulty level)** — target number. -5 trivial, 0 average, 5 difficult, 10 very difficult.
- **Degrees of success** — margin ≥ +10 **crit**, ≥ +5 **hit**, ≥ 0 **graze**, else **miss**.
- **0/1/2/3 notation** — values for miss/graze/hit/crit, in that order.
- **HOP (Hit Overflow Point)** — on "overflow-scale" tests (attacks, casts) there is no crit: any hit gives HOP = margin − 5, spent on extra effects (Slice, Smash, Bust, spell improvements…). Piercing attacks and quickened casts treat a graze as a miss. The .tex doesn't state the formula; app: `app/domain/play/test.ts`.
- **Exploding die** — d10 = 9 → add d6 (repeat on 6); d10 = 0 → subtract d6 (repeat on 6). Only when stated.
- **Safe / risky test** — roll 2d10, keep closest to / farthest from 5.
- **Held test** — rolled once per round/scene, kept until a trigger (movement, stealth).
- **Group test** — best value, worst value, or best + bonus per helper, as each rule says.

## Character model — `creating.tex`
- **Skill value** — skill bonus + proficiency bonus. 19 skills; "trainable" = can be raised individually.
- **Proficiency** — bonus shared by several skills: Melee, Ranged, Awareness, Charisma, Conviction, ★Sorcery, ★Devotion.
- **Talent** — growth potential that sets XP cost: **CON, DEX, INT, SPI** (max 5, raised with karma).
- **Attributes** — **STR, AGI, STA**; human baseline 10, max 20. Raised with XP.
- **Levels 0–6** — Novice, Apprentice, Amateur, Professional, Expert, Master, Grandmaster.
- **XP** — downtime training currency (10 days ≈ 1 XP). **Karma** — mission/roleplay reward; buys talents and some abilities.
- **TGH (Natural Toughness)** — 0.5 × STR × DM; damage-tier step size.
- **Size 1–7** — human = 3. **DM** damage multiplier, **SM** skill modifier, **RM** reach multiplier (height = 2m × RM), **VM** volume/weight multiplier.
- **SD (Standard Deflection)** — size-only difficulty to hit: -5 - SM stationary, -2 - SM moving. Floor for any defense.
- **Limit stress action** — forced behaviour on a failed morale test: Coward, Violent, Tanatosis, Abusive, Traitor, Martyr.
- **Conviction** — worldview or temperament track on two axes (Order–Chaos, Extro–Introspective); +1 Will per level; own XP, can be lost/renounced. Eight: Adaptation, Domination, Stoicism, Providentialism (worldview); Fatalism, Ferocity, Guardian, Hedonism (temperament).
- **Focus A–E** — creation priority for Wealth, CON, SPI, INT, DEX.
- **Races** — Surbit (size 2), Dwarf, Human, Halkir, Erthal.
- **★ / `\magic`** — marks magic-only content, dropped in a no-magic game.

## Combat — `combat.tex`
- **Round** ≈ 3 s; **turn order** "first to ask, first to play", ties by Cunning.
- **AP (action points)** — time; 8 per round. **Negative AP** carries into next round.
- **STA** — stamina, spent on effort; **Rest** (4 AP) recovers STA/4.
- **Action surge** — once per round: **movement** (3 STA, AGI/2 AP), **combat** (2 STA, 4 AP), **reaction** (2 STA, 4 AP, reactions only), **focus** (needed for concentration), **recovery** (default, regain STA).
- **Reaction** — triggered action on another's turn; **prepared reaction** costs 1 AP. **Give up action** — abort to react, lose 1 AP.
- **Concentration** — carry unspent AP to next round for an expensive action.
- **Compulsion / severe compulsion** — forced action; severe (self-harming) gives +10 to resist.
- **Standard action** — 3 AP (scales with Prestidigitation): pick up, draw, interact.
- **Movement types** — walk, tread, run, jump, crawl, swim, stand up, trample, ride.
- **Trample / crash** — moving through an occupied space; Force vs Force.
- **IL (injury level)** — accumulated damage; -1 penalty per 10. Collapse at 40 (**injury capacity**), death above 50.
- **Damage tiers T0–T5** — thresholds armor + n × TGH; give IL and bleed.
- **Damage types** — blunt (vs prot), cutting (vs RES), burning/radiant/corrosive/electric (vs INS).
- **Bleed** — +IL per bleed intensity each round and per STA spent.
- **Interruption** — T1+ blunt/electric cancels the current action. **Stun** — interruption + lose 2 AP (T3+).
- **Deflection** — HOPs needed to buy extra effects; human body 4, armor overrides.
- **HOP purchases** — **Bust** (deflection HOP, penetrating), **Slice** (deflection HOP, +25% cut, half if not bladed, repeatable), **Smash** (1 HOP, +1×DM blunt, repeatable), **hand switch** (3). Free with a property: assassinate (+5 HOP), braced, hook. Modifiers: UF +2, closed helmet −5, sharp +1/+2. App: `tables.ts` `HOP_EFFECTS`, `scene/rules/damage.ts`.
- **Damage absorption** — damage loss when one attack passes through several targets or a block.
- **Hardness 1–4** — liquid / flesh-fabric / wood-bone / metal; a weapon cuts only softer things.
- **Locations** — chest (default), hand (-10), leg (0), head (-5).
- **Wound** — separate disabling injury with its own IL to heal.
- **Penalty families** — **Injury** (attributes), **Sensory** (combat/perception skills), **Mental** (cognitive/social/spells).
- **Afflictions** — lame, prone, grappled, immobile, blind/obfuscated, deaf/muffled, corroding, unconscious, afraid, enraged, confused, dominated, intoxicated I–III, tired/exhausted, weakened/malnourished, thirsty/dehydrated, sick.
- **Attack variants** — heavy, sweeping, opportunity, braced, hook, assassinate; ranged: throw, shoot, snipe, quick shot, prepared, coordinated.
- **Defenses** — evade, evasive jump, block, intercept, protect; vs ranged: evasion, guard, cover; vs explosion: avoid, explosion block.
- **Grapple maneuvers** — escape, immobilize, disarm, knockdown; **push and drag** to move.
- **Flanking, follow, flee, high ground** — positional rules.
- **Feint, analyze** — Cunning actions.
- **Morale test** — Will vs DL = aggravating factors + pressure; graze = afraid, miss = limit stress action.
- **Combat social actions** — intimidation, taunt, rally, negotiation, surrender, feign death, call help.
- **Chase** — distance tiers **combat (<50m), shooting, far, horizon**; **quarry/pursuer**; **dash** (movement surge at combat range); **routing**; **chain** (who chases whom); **scouting**.
- **Stealth value** — d10 + Stealth, held for the round vs passive Detection; **stealth event**, **hidden roll**, **senses** (vision, hearing, smell, touch; active/reactive), **sensory impairment** (none/partial/total), **visibility**, **noise**, **signal strength**.

## Gear — `gear.tex`
- **RES** — breakage threshold; armor RES also reduces cutting damage.
- **Prot (protection)** — armor reduction vs blunt. **INS (insulation)** — vs burning/radiant/corrosive/electric.
- **Burden / burden penalty** — gear weight as AGI/STA penalty.
- **Bulk 0–4+** — item size class (tiny, small, medium, large…), each ≈ 3× weight.
- **Slots / quick slots / container** — carrying system; stacks of 3 or 10 at lower bulk.
- **Cover** — shield bonus to defend/guard.
- **Weapon properties** — grapple I/II, sweeping, braced, shaft, short/long I–II, DEF, STR x, hook, one/two hands, heavy I–III, piercing, bladed, penetrating, precise, basher, slow/fast/UF, draw, reload, explosion.
- **Armor classes** — fiber, metallic, rigid; extras gauntlets, closed helmet.
- **Currency** — CP/SP/GP, 10:1. **Sharp** — sharpening condition.

## Story / social — `story.tex`
- **IB (interpretation bonus)** — GM bonus/penalty to a social test for how well the action was played/described.
- **Knowledge test** — 2× knowledge or 2× INT. **Deduction test** — 2× INT.
- **Specific knowledge** — narrow, levelled knowledge (place, region, language, art, faction, religion, animal, vehicle).
- **Enabler** — knowledge needed for an action; -5 per missing level.
- **Contact / trust (-3 to +3)** — relationship with an NPC; types: merchant, mercenary, service, influencer, trainer.
- **Leverages** — **renown** (0–10, status), **honor** (-10 to 10, morality), **popularity** (local recognition), **affiliation**, **titles**, **tags** (seduceable, etiquette, moralist).
- **Missions, deeds** — sources of renown/honor/karma; deeds decay.
- **Assets** — owned non-coin wealth.

## Exploration — `survival.tex`
- **ET (exploration turn)** — 4-hour block, 6 per day.
- **EA (exploration action)** — travel, search, prepare; one roller, everyone takes **wear** (+1 IL base).
- **Point crawl** — map of **nodes** and **connections**, each with events.
- **Survival markers** — hunger, thirst, exhaustion (tired 4–7, exhausted 8–11, confused >11).
- **Exposure** — terrain harshness against resting; **infection exposure**, **tracking DL**, **terrain tags**.
- **Event types** — place, encounter, obstacle, treasure, wear, food, shelter, water; **event DL** -5 to 15.
- **Long camping, travel pace (regular/pushed), baseline metabolism**.

## Abilities — `abilities.tex`
- **Usage** — passive, a cost (AP/STA/ET/IL), attack, reaction.
- **Cost** — "6 XP, DEX 3" = price, talent, training level. I/II/III = ability levels; 1|2|3 = per-level values.
- **Mutations** ★ — CON abilities: physical transfiguration, spiritual mutation, chimerism.

## Sorcery ★ — `spells.tex`
- **Learning routes** — **intuitive** (per-spell skill), **wizard** (knowledge + Sorcery), **cleric** (Devotion + Sorcery; **miracle** = 2× Devotion, risky).
- **Magic knowledges** — Alchemy, Animancy, Biomancy, Shamanism.
- **Spell DL**; **spell types** — instant, sustained, charged, curse.
- **Metamagic (HOP)** — quicken (+3 DL), extend (3), enhance (4), amplify (5), effortless (6).
- **Deity / devotion / cleric** — `creating.tex` and `abilities.tex`.
