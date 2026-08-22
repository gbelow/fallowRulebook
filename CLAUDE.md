# Fallow — System Rulebook

This is the rulebook for a tabletop RPG (TTRPG) written in LaTeX. The rules are written to be efficient: stated as briefly and precisely as possible, with each piece of information stated only once and little explanation offered. Match this style when editing — concise, precise, no redundant explanation.

The system is designed to be played with or without magic.

## File structure

`main.tex` is the root file; everything else is loaded from it.

- `intro.tex` — stated the game's design philosophy and intent. Answers who this game is for and what should be expected.
- `play.tex` — describes the game's loops. Answers what play is supposed to look and feel like. claude should always know what is in this file in any prompt about the game's mechanics.
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
- `thinking.tex` — creation notes only. Disregard.

## Cross-cutting mechanics to know

**Skill test resolution is universal, but lives in `combat.tex`.** The core mechanic — skill test = d10 + skill value vs a difficulty level (DL), with degrees of success (critical ≥ +10, hit ≥ +5, graze ≥ +0, else failure), the exploding die, and safe/risky tests — is defined once at the top of `combat.tex` ("How skills work") but applies to every chapter: combat, intrigue, survival, and spellcasting all build on it. When a question touches skill tests, start there, not in the chapter that triggered the question. (The master skill list and value formulas, by contrast, live in `creating.tex`.)

## How I help with this project

Beyond editing the rules text, I'm expected to support:

- **Comparative analysis** — compare this system with other TTRPGs on speed of play, game style, target audience, marketing strategy, and similar dimensions.
- **Combat strategy** — discuss tactics, matchups, and the strategic implications of the rules.
- **Formatting and editing** — tidy formatting, enforce the concise/house style, and act as editor.
- **Game tools** — create random tables, items, and similar play aids consistent with the system's mechanics and tone.

When generating new content (items, tables, NPCs, abilities), keep it consistent with the rules and terminology already established in the files above.
