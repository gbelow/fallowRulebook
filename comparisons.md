1. Resolution engine & speed of play — vs D&D 5e, Pathfinder 2e, Mythras/BRP, Savage Worlds,
  Cypher. Where does "roll once, four outcomes, no confirmation rolls" put Below on the
  speed/depth axis? Trade-off: GM-judged DLs vs fixed DCs.

  -- fast enough for experienced players. electronic tools help, especially GMs. Requires training to be good.

  2. Damage & lethality model — vs Rolemaster (crit tables), Hârnmaster, Mythras, GURPS.
  Below's tiered injury tolerance + wounds + SOP "buy effects on overflow" is a middle path
  between abstract HP and location-wound tracking. I can map where it lands on the bookkeeping
  ↔ realism axis.

  -- good crunch per time. too complex for a definitive analysis. lethal, but backed by game philosophy

  3. AP/STA economy & tactical depth — vs Lancer (its action economy), 5e
  (action/bonus/reaction), Shadowrun (edge/action phases), Pathfinder 2e (three actions).
  Below's "AP as time, STA as burst, reactions cost AP, prepared triggers" is unusual — I can
  show what tactics it enables that others can't.

  -- 

  4. Modular/optional magic & audience fit — vs low-magic systems (Hârn, Mythras, Forbidden
  Lands) and "magic-first" ones. How does gating spells behind knowledge + making the whole
  magic chapter removable affect table experience and the "play with or without magic" pitch?

  5. Advancement philosophy & player incentives — vs Burning Wheel ( Beliefs/artha), Pendragon
  (traits/passions), 5e (milestone/XP). Below's karma-for-character-loyalty + convictions
  with XP loss is a strong RP-incentive design. Worth comparing what behavior each system
  actually rewards.

  6. Market positioning & target audience — where Below sits among current commercial TTRPGs:
  crunchier than OSR, more simulationist than PbtA/FitD, more grounded than 5e, less
  tactical-symmetrical than PF2e/Lancer. I can sketch a positioning map and a likely buyer
  profile + competitive set for a marketing strategy.

  7. The size-scaling / physics engine — a deep-dive on the DM/SM/MM/VM system vs how GURPS,
  Rolemaster, or D&D handle creature scaling. This is Below's most original mechanical
  artifact; worth examining in isolation.

  Positioning in one paragraph

  Below occupies the space between Mythras/Hârnmaster (simulationist, lethal, skill-based)
  and The Riddle of Steel / Song of Swords (AP-pool dueling, weapon-driven tactics), with
  Forbidden Lands' explorable resource attrition and a modular-magic pitch nobody since
  GURPS has seriously attempted. It is crunchier than OSR, more grounded than 5e, less
  symmetrical/balanced than PF2e or Lancer — and unlike all of those, it is explicitly a
  game for people who want to master a system, not pick one up in an evening. That's a
  viable niche (the Hârn and Riddle of Steel communities have survived decades on it), but
  it means every failure below is amplified: a system whose pitch is "trust the internal
  consistency" dies by undefined terms.

  ---
  Pillar-by-pillar evaluation

  1. "Fast to resolve" — the most clearly failed pillar

  intro.tex:32 claims the math is "meant to be done in the head" and combat is fast. Your
  own note in comparisons.md item 2 half-admits this ("too complex for a definitive
  analysis"). Count the operations on one landed sword blow:

  1. Opposed declaration (attacker 3 AP, defender picks among 4 defense types, 2–3 AP)
  2. d10 + Strike vs defense value, exploding-die chain possible
  3. SOP decision point (armor bypass / penetrating / extra cut / smash — each priced by
  the target's deflection, a third distinct stat named "deflection" alongside SD and shield
  deflection)
  4. Damage = energy ×SHP vs armor + k×TGH threshold lookup → tier
  5. Tier → IL + wound% → location rules if SOP was spent on the head/hand
  6. Bleed counter bookkeeping

  That is Rolemaster pacing, not 5e pacing. 5e survives its market share on one roll vs AC
  plus subtraction; PF2e keeps speed via fixed DCs and four degrees with no tier tables.
  The skill test in Below is genuinely fast — as fast as anything on the market — but the
  damage pipeline behind it is the slowest part of the game, and the book's own structure
  buries it across three sections (thresholds, wounds, localized damage). The morale test
  at the top of every round for every combatant adds another die per combatant per round on
  top.

  Verdict: the pillar holds for scenes, exploration, and social. It fails in the exact
  place the intro says it applies "especially": combat.

  2. "Every rule answers another" — a real success, poorly discoverable

  This is the pillar I'd defend hardest. Test the claim where it matters: full plate
  (gear.tex:314, RES 20/10, prot 10). Counters that exist within the rules: rondel and
  stiletto bypass in grapples, warhammer smash (SOP), braced attacks, fire — burn ignores
  RES and attacks insulation 8 against pitch at 15/turn (gear.tex:396) — historically
  correct anti-armor answers. Armor ↔ weapon properties ↔ hardness layers ↔ grappling form
  a genuine counterplay web that neither 5e (plate is just AC 18) nor Mythras (armor is
  flat AP subtraction) achieves. That's the strongest competitive differentiator after the
  size engine.

  Where it fails: counterplay requires cross-chapter mastery (combat SOP rules + gear
  properties + hardness + fire rules), and the rules are honest about it (intro.tex:30:
  "the game becomes better the more players understand the mechanics"). PF2e solves the
  same problem with tight symmetry and explicit trait tags; Lancer with a fixed action
  menu. Below chooses depth over learnability, which is coherent — but it means the
  counterplay is invisible to new tables, and "overpowered until you know the answer" reads
  as broken balance in playtest feedback you'll get from anyone who hasn't internalized
  the system.
  

  3. The AP/STA economy — genuinely novel; your comparisons.md item 3 is blank, so here it
  is

  vs Lancer (static action menu), PF2e (three actions), 5e (action/bonus/reaction),
  Shadowrun (edge/initiative passes):

  What Below's design enables that none of them can express:
  - Time as a spendable, bankable, stealable resource. Ending a turn with saved AP,
  negative AP from resting, feints that force opponents to burn AP (combat.tex:15) — you
  can win by draining the clock, not the HP. No competitor has a win condition shaped like
  this.
  - Prepared reactions with player-authored triggers (1 AP to prepare, arbitrary trigger
  text). This is the best "readied action" implementation in the hobby — 5e's Ready is a
  fossil next to it.
  - STA as burst limiter produces the boxing-round endurance arc the intro promises —
  fights end when someone's lungs give out, which matches the historical-fencing fantasy
  better than any HP-derived system.
  - "First to ask, first to play" makes initiative a social/tactical contest rather than a
  pre-roll — bold, and thematically consistent with player-skill-over-character-skill.

  Where it fails:
  - Cognitive load contradicts pillar 1. Tracking per-combatant AP spent on other people's
  turns (reactions, surges, compulsions, opportunity attacks) is the exact bookkeeping that
  made Shadowrun and Rolemaster famously slow at 5+ combatants.
  - "First to ask, first to play" systematically rewards assertive players, not characters.
  The cunning-test arbitration patches it, but combined with feint-forcing and
  prepared-trigger text, the system gives its most powerful verbs to whoever talks fastest
  at the table. Lancer/PF2e's rigid order is boring but fair; this is interesting but
  biased.
  - combat.tex:9: the turn token is granted and never referenced again — an orphan rule
  that suggests this subsystem got redesigned mid-stream and the text wasn't fully
  re-audited.

  4. "Play with or without magic" — the pitch holds for two loops and quietly breaks on the
  third

  The ingredient-based magic (alchemy needs charges and gear, biomancy needs bodies,
  shamanism needs clouds — spells.tex:61 "making it rain in the desert is impossible if
  there is no water in the sky") is the most elegant solution to modular magic I've seen;
  GURPS' answer (magic as point-costed advantages) never felt removable, and Forbidden
  Lands never claims it. The mundane-tools-of-war chapter mirroring spells (gear.tex:387,
  fire/smoke/caltrops that magic amplifies rather than replaces) is textbook good design.

  Where it fails: Animancy contradicts the founding claim. intro.tex:24: "Magic is
  conceived merely as telepathic control over natural phenomena. If the physical
  ingredients are not present, magic is not possible." Telepathic Link, Possession,
  Command, Alter Memories, Disintegrate Mind (spells.tex:165–218) have no physical
  ingredient, contradict no physics by being "telepathic control" in only the loosest
  sense, and — this is the real damage — they bypass the social system's core constraints.
  The intrigue chapter's best rule is "every social test must have irreversible
  consequences" (intrigue.tex:45); Sleep, Charm, Suggestion and Command ignore the IB
  economy, the acting requirement, and the repetition limit entirely. So:
  - In a no-magic game, the social loop is a pure roleplay/IB/contacts game — complete,
  coherent.
  - In a with-magic game, any Animancy 2+ character replaces the party's entire social
  build with 3 AP.

  Two different games, not one game with an optional module. "A game without it is
  complete" (intro.tex:24) is true but slightly dishonest marketing — the with-magic game
  invalidates a whole chapter of its own rules.

  5. Player skill vs character skill — the IB asymmetry (revised)

  The ±10 extremes of the Interpretation Bonus (intrigue.tex:14) are concession markers,
  not operative modifiers: the IB ladder itself says +10 is "almost a guaranteed success"
  better handled by skipping the test, and -10 is "just to avoid giving straight vetos"
  (intrigue.tex:19,23) — the territory D&D's DMG handles with "just say yes/no" auto-
  concession. The effective range is ±5, which on the degree bands (crit +10 / hit +5 /
  graze +0) is exactly one degree of success — roughly advantage-sized in 5e terms, not a
  system-dwarfing judgment. Holding the situation constant, a Persuasion 8 character still
  beats a Persuasion 0 character with good acting by ~4 points in the common ±2 band, and
  intrigue.tex:51 provides the reverse valve (skill alone can skip the scene). The intro's
  "all skills roughly the same value" claim survives this objection.

  Why competitors refuse to price performance quality at all:
  - Player/character separation (Gygaxian inheritance): Charisma is the character's
    eloquence; grading the speech taxes the player's rhetorical talent instead of the
    build.
  - Auditability: graded quality modifiers are pure GM taste — unreproducible across
    tables, and exactly the class of situational modifier 5e deleted in favor of
    advantage. PF2e needs DCs a stranger can reproduce.
  - Incentives: dice for performance trains players to act at the referee rather than the
    scene, and rewards extroverts over shy players. Burning Wheel routes rewards through
    written Beliefs (artha) to keep the loop on character goals, not table charisma.
  - PbtA/FitD price fiction elsewhere: fiction is the trigger, quality enters as
    position/effect negotiated before the roll — the decision layer, not a post-hoc grade
    of the speech.

  Below is thus the only system pricing performance quality directly on the die — coherent
  with its player-skill-over-character-skill philosophy, and not obviously wrong given that
  5e's DMG suggests inspiration for good roleplay (capped, binary, widely ignored). The
  remaining exposure is not the size of the IB but its bundling: one number mixes "how
  likely is this ask" (situation) with "how well was it delivered" (acting), and only the
  second competes with skill investment. The ladder already half-separates them in prose;
  making that explicit would close it.

  6. Advancement — wealth is a super-stat

  The karma/convictions architecture is genuinely good: convictions with individual XP, XP
  loss on betrayal, renunciation at 0 (creating.tex:452) is Pendragon-passions-grade
  incentive design, and limit actions give characters a mechanical personality in a way
  neither 5e nor PF2e attempts.

  Where it fails:
  - Training costs money (creating.tex:92), and character creation prices Wealth priority A
  at 100 GP while DEX priority A grants 60 XP. If GP→XP conversion exists at any
  reasonable rate, wealth priority dominates the priority array for any campaign expected
  to reach downtime — wealth isn't gear budget (as in PF2e), it's directly convertible into
  skill. Long campaigns degenerate toward "whoever took wealth A wins the build race." The
  cross-check between the salary tables, training costs, and creation XP never happens
  anywhere in the book.
  - Karma rewards "creative use of the system" (creating.tex:118) — advancement flows to
  system-mastery players. Coherent with the design philosophy, but it means new players
  advance measurably slower than engine-optimizers at the same table, which is a retention
  problem no competitor has because none of them make GM-discretion advancement the only
  advancement (5e abandoned roleplay-XP for milestones for exactly this reason).
  - The morale→conviction-XP-loss link (combat.tex:145, commented out) was abandoned
  mid-design — correctly, I'd argue, since punishing a character for a GM-called stress
  test is punishing them for the GM's die. But its ghost confirms the tension was real.

  7. Verisimilitude / the size engine — original, and it mostly pays

  The DM/SM/MM/VM system is the most original mechanical artifact here (your comparisons.md
  item 7). It does what GURPS does with cube-square scaling but in one table a GM can hold
  in their head, and the -1 STR/-1 AGI per size step with weight tripling per category
  (creating.tex:164) is honest biomechanics. Horses genuinely get harder to hurt and easier
  to hit. Nobody else does this at this resolution.

  Where it fails: every weapon and armor must be rescaled by the GM per size category
  ("adjust the DM to the appropriate size," gear.tex:38), offloading arithmetic to the
  table — again colliding with pillar 1. GURPS eats the same cost and is famous for it.