# Fallow — System Rulebook

This is the rulebook for a tabletop RPG (TTRPG) written in LaTeX. The rules are written to be efficient: stated as briefly and precisely as possible, with each piece of information stated only once and little explanation offered. Match this style when editing — concise, precise, no redundant explanation.

The system is designed to be played with or without magic.

## File structure

`main.tex` is the root file; everything else is loaded from it.

- `intro.tex` — stated the game's design philosophy and intent. Answers who this game is for and what should be expected.
- `play.tex` — describes the game's loops. Answers what play is supposed to look and feel like.
- `creating.tex` — character model. Describes the static characteristics of a character and the rules for player character creation, including the master skill list and value formulas.
- `combat.tex` — mechanics of combat and any situation that requires the grid.
- `gear.tex` — properties of gear, gear sheets, and gear-related mechanics.
- `intrigue.tex` — the social system and usage of social skills. Mechanics for an intrigue game.
- `survival.tex` — exploration mechanics and resources for an exploration game.
- `abilities.tex` — abilities characters can obtain.
- `spells.tex` — spells characters can obtain, plus casting and learning rules.
- `war.tex` — tools for a war-centered game.
- `horror.tex` — tools for a horror game. Currently empty. Future work.
- `monsters.tex` — list of NPCs to throw into the game. Currently very limited and provisory.
- `thinking.tex` — just a scratchpad. Not a part of the book. Disregard.

## Cross-cutting mechanics to know

**Skill test resolution is universal, but lives in `play.tex`.** The core mechanic — skill test = d10 + skill value vs a difficulty level (DL), with degrees of success (critical ≥ +10, hit ≥ +5, graze ≥ +0, else failure), the exploding die, and safe/risky tests — is defined once in `play.tex` ("How skills work") but applies to every chapter: combat, intrigue, survival, and spellcasting all build on it. When a question touches skill tests, start there, not in the chapter that triggered the question. (The master skill list and value formulas, by contrast, live in `creating.tex`.)

**Game loops (`play.tex`):** four loops — **big loop** (campaign framing: dungeon crawl, arena, or story, chosen per table), **scene** (moment-to-moment action, grid-based), **exploration** (point-crawl resource management between nodes), **downtime** (growth: skills, abilities, contacts, gear). Scenes run in one of four modes — combat, chase, social, stealth — that bleed into and hand off to each other: failed stealth can trigger combat, a lost morale test in combat can trigger an escape into a chase, a chase can restart combat elsewhere. When reasoning about one mode, keep its hand-offs to the others in mind. Use the `game-loops` skill for the fuller compressed reference (mode objectives, disengagement options) instead of re-reading all of `play.tex` each time.

## How I help with this project

Beyond editing the rules text, I'm expected to support:

- **Comparative analysis** — compare this system with other TTRPGs on speed of play, game style, target audience, marketing strategy, and similar dimensions.
- **Combat strategy** — discuss tactics, matchups, and the strategic implications of the rules.
- **Formatting and editing** — tidy formatting, enforce the concise/house style, and act as editor.
- **Game tools** — create random tables, items, and similar play aids consistent with the system's mechanics and tone.
- **Human made** — All .tex files must remain human made. No AI editing is allowed for text unless asked for. Stylistic changes are allowed.

When generating new content (items, tables, NPCs, abilities), keep it consistent with the rules and terminology already established in the files above.

## How to analyse

 - When asked for analysis, favor numbered lists with pros and cons.

 - When asked for reviews, compare with other games that share the same mechanics and how their reception went

 - Make questions when you are not sure about how a mechanics works. Flag ambiguity.

 ## Design Principles

 - Mechanics should be as fast as possible to resolve and have as little bookkeeping as possible for the same tactical depth.

 - Verissimilitude is a design goal. 

 - The can should be playable and whole with or without magic. Magical features are marked with \magic 

 - Strategy and risk management. This game is about making an informed decisions. High impact demands high commitment: outcomes should read as consequences of player decisions, never as arbitrary happenstance.

 - Players should trust the system to contain mechanics to answer any tactical situation.

 - Combat should not contain interpretation, it is a puzzle with RNG. The other loops can include co-creation tools.

 - No classes or levels: any character can take any combination of skills, but investing in some delays others, so no character is good at everything. All skills are meant to hold roughly equal value.

 - Cost/impact/avoidance triangle: an ability, spell, or offensive action can only have 2 of 3 — cheap (low time/stamina/resource cost), high impact (damage/effect), and hard to avoid (costly or hard to prevent/evade). Check new abilities/spells/items against this before proposing them.

 - Rules vs guides: rules state an exact procedure with clear consequences; guides state factors and their rough weight but leave the call to the GM. Preserve that distinction when writing or editing text — don't harden a guide into a rule or vice versa.

 - Player skill vs character skill: a well-described action can earn the GM's interpretation bonus on top of the character's skill value; flatly stated intent still resolves, just without that bonus.