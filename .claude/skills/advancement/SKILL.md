---
name: advancement
description: >-
  Quick reference for Fallow's downtime advancement system — how skills,
  proficiencies, attributes, knowledges, talents, abilities, spells, and
  convictions level up, their XP/karma cost formulas, and what talent each
  uses. Use whenever a question touches XP costs, karma, leveling up,
  learning an ability or spell, or what a skill's talent/proficiency is.
---

Source of truth: `creating.tex` §"Talent and Learning" and §Intellect/Knowledge
for the core formulas; `abilities.tex` §"Acquiring abilities" for abilities;
`spells.tex` §"Learning spells" for spells. Re-read those if exactness
matters — this is a compressed map, not a replacement.

## The stack

**Attribute** (STR/AGI/STA, CON is separate) → **Talent** (CON/DEX/INT/SPI,
bought with karma) → **Proficiency** (bought with XP, broad, feeds many
skills) → **Skill** (bought with XP, narrow, single use). Skill value =
skill bonus + proficiency bonus. Default value for everything is 0.

## Talents

4 talents: **CON** (health/mutation), **DEX** (athletics/combat), **INT**
(knowledge/sorcery/most social/cunning), **SPI** (conviction/devotion/morale).
Chosen in priority order at character creation; after that, **only karma**
increases them. Cost to reach talent level n: **4+4n**. Max talent value 5.

**Karma** rewards (not XP): completing missions/objectives (≈2/3 of award),
plus loyalty to character concept, creative system use, participation in
dramatic moments (≈1/3 combined) — harder missions and attempted-but-failed
hard objectives are worth more than many easy completions. Budget ≈4-6
karma/session → roughly one talent level every 3-5 sessions.

## Skills, proficiencies, attributes (XP-bought)

**Training pace:** 10 days of downtime = 1 XP, plus money scaled to the
difficulty of what's being learned.

**Cost to reach level n:**
- Proficiency: **4+4n**
- Skill: **2+2n** (exactly half a proficiency's cost)
- If the relevant **talent is lower than n**, multiply the cost by
  **2^(n−talent)**. Training past your talent ceiling is exponentially
  expensive — this is what keeps characters from being good at everything.
- Attribute (STR/AGI/STA): cost = target value ÷ 2. If the average of the 3
  attributes exceeds 10+CON−SM, cost doubles; +100% again per point further
  above that. Hard cap 20. Swapping 1 point between two attributes costs 2 XP
  flat.

**Level names** (0-6, same scale for skills/proficiencies/knowledge): 0
Novice (common sense only) → 1 Apprentice (basics) → 2 Amateur (basics
mastered + some advanced) → 3 Professional → 4 Expert (reproduce almost
anything in the field) → 5 Master (peak results) → 6 Grandmaster (pushes the
era's boundaries). Expected range 0-5; higher is possible but costly (talent
cap is 5).

**Trainable vs not:** a skill marked non-trainable has no skill bonus of its
own — it only rises via its proficiency (and knowledge, for knowledge-driven
skills). See the master skill table in `creating.tex` §"Character Skills and
Actions" for which skill uses which proficiency and talent (e.g. Strike/
Defend → Melee, DEX talent; Persuasion/Insight/Deception → Charisma, INT
talent; Cunning/Exploration → INT talent).

## Knowledge

Learned exactly like any skill, INT as talent, same 0-6 scale. Two uses:
- **Knowledge test** (does the character know/recall X): skill value = 2×
  that knowledge.
- **Deduction test** (reason from known facts): skill value = 2×INT, if the
  needed facts are already known.

**As an enabler:** acting without the knowledge a task requires costs −5 per
missing knowledge level on the relevant test. **As a talent:** knowledge
level substitutes for talent when learning spells/sorcery abilities — spells
carry a knowledge-level requirement gating their difficulty.

Formal areas (Alchemy/Animancy/Biomancy/Shamanism are \magic-tagged):
Architecture, Chemistry, Medicine, Geography, Politics, Smithing, Survival,
Zoology, plus the three magic knowledges. **Specific/informal knowledge**
(a place, a language, a faction, an animal, a vehicle) is learned the same
way but its XP cost is arbitrary/GM-set by difficulty; INT is still the
talent normally. It's generated passively by relevant downtime activity, not
just paid for directly.

## Abilities

Bought with XP during downtime, using the same cost logic as skills/
proficiencies from character creation. Each ability can only be acquired
once; multi-level abilities (I/II/III) list a fixed XP cost plus an
escalating talent/skill requirement per level (e.g. `6 XP, CON 3/5` means
level I needs CON 3, level II needs CON 5 — same XP each time it's bought).
An ability cannot be acquired unless its listed requirements (talent,
skill/proficiency level, prerequisite abilities, knowledge) are already met.
Some abilities are instead granted automatically at a knowledge or
conviction level rather than bought.

## Spells

Three independent learning paths (see `spells.tex` §"Learning spells"):

- **Intuitive:** 6 XP, talent = Sorcery proficiency (or Devotion, if the
  spell is on a deity's list). Cannot be used for spells with a knowledge
  requirement above 3. Skill starts at 0; each further point costs 1 XP for
  +1, then 2 XP for +1 more, etc. (mirrors the skill formula), each purchase
  also raising the effective knowledge requirement it satisfies by 1.
- **Wizard:** skill to cast = Knowledge level + Sorcery. Spells are learned
  from grimoires/experimentation during an exploration turn (materials
  required): sorcery test, DL +5 per missing knowledge point vs. the spell's
  requirement, learned on hit/crit — no further knowledge penalty once
  learned. Wizards can also freely attempt any magical interaction at
  DL +5 per missing knowledge point, but only in a risky manner.
- **Cleric:** skill to cast = Devotion level + Sorcery, automatic access to
  the deity's whole spell list once the devotion level requirement is met.
  Miracles (any spell, any devotion level) use 2×Devotion, −3 per devotion
  level short of the spell's requirement, must be risky, and only work
  inside the deity's influence area (easier inside a temple/holy place).

A spell learned intuitively keeps its skill level if later learned via
wizard/cleric method (always takes the higher of the two).

## Conviction (SPI)

Two convictions (worldview + instinct) chosen at creation, starting level 0.
Each tracks its own XP with its own defined promoted/prohibited attitudes
(gain XP for acting on it, lose XP for acting against it — session-capped,
usually once/turn). SPI is the talent for the cost formula. Conviction
abilities unlock automatically per level (no separate purchase). Negative
XP at session end drops a level; hitting 0 renounces the conviction.
