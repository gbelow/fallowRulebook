"""
Fallow duel referee: rolls one exploding d10 at a time and resolves a single
declared attack with the exact resolver in fallow_sim.py, so a narrated fight
can be audited roll by roll.

    python sim/referee.py roll --label "Cunning A"
    python sim/referee.py attack --weapon "Halberd axe" --var heavy1 --loc chest \
        --str 13 --strike 8 --armor Hauberk --tgh 6.5 --dl 8 --defense block --block 26

Rolls are drawn from a counter file (--state) so a fight is reproducible from
its seed; pass --die to resolve a roll already made.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fallow_sim import (ARMORS, WEAPONS, Attacker, Defender, Situation,  # noqa: E402
                        degree_of, fixed_bonus, resolve_degree)

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".referee_state.json")


def _next_rng(state_path: str, seed: int) -> random.Random:
    n = 0
    if os.path.exists(state_path):
        with open(state_path) as f:
            n = json.load(f).get("n", 0)
    with open(state_path, "w") as f:
        json.dump({"n": n + 1, "seed": seed}, f)
    return random.Random(f"{seed}:{n}")


def explode(rng: random.Random) -> tuple[int, str]:
    """play.tex exploding d10: 10 -> +d6 (chain on 6); 1 -> -d6 (chain on 6)."""
    d = rng.randint(1, 10)
    trail = [str(d)]
    total = d
    if d in (10, 1):
        sign = 1 if d == 10 else -1
        while True:
            e = rng.randint(1, 6)
            trail.append(("+" if sign > 0 else "-") + str(e))
            total += sign * e
            if e != 6:
                break
    return total, " ".join(trail)


def cmd_roll(a):
    for _ in range(a.n):
        rng = _next_rng(a.state, a.seed)
        total, trail = explode(rng)
        print(f"{a.label}: d10 = {total}   [{trail}]")


def cmd_attack(a):
    atk = WEAPONS[a.weapon]
    att = Attacker(STR=a.str, strike=a.strike, DM=a.dm, sharp=a.sharp, dull=a.dull)
    dfn = Defender(armor=ARMORS[a.armor], TGH=a.tgh, DL=a.dl, defense=a.defense,
                   block=a.block, gauntlets=a.gauntlets, closed_helmet=a.helmet)
    sit = Situation(variation=a.var, location=a.loc, to_hit_mod=a.mod)
    fixed = fixed_bonus(atk, att, dfn, sit)
    if a.die is None:
        rng = _next_rng(a.state, a.seed)
        die, trail = explode(rng)
    else:
        die, trail = a.die, "given"
    score = die + fixed
    degree, hop = degree_of(score)
    o = resolve_degree(degree, hop, atk, att, dfn, sit)
    print(f"{a.label}: {a.weapon} {a.var} @{a.loc} vs {a.armor} ({a.defense}, DL {a.dl})")
    print(f"  die {die} [{trail}] + fixed {fixed:+d} (strike {a.strike}, mod {a.mod:+d}, "
          f"loc {atk and __import__('fallow_sim').LOCATION_PENALTY[a.loc]:+d}, DL {-a.dl:+d}) "
          f"= score {score:+d} -> {degree.upper()}, HOP {hop}")
    if o.degree == "miss" and o.damage == 0:
        print("  no damage")
        return
    print(f"  spent {list(o.spent) or '-'} | {o.dtype} damage {o.damage:g} -> tier "
          f"{'none' if o.tier < 0 else 'T%d' % o.tier} (body T{o.body_tier}) "
          f"| IL {o.il:g} | bleed {o.bleed} | wound '{o.wound}' "
          f"| interrupt={o.interrupt} stun={o.stun} ko={o.ko} death={o.death}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--state", default=STATE)
    p.add_argument("--label", default="roll")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("roll")
    r.add_argument("-n", type=int, default=1)
    r.set_defaults(fn=cmd_roll)
    k = sub.add_parser("attack")
    k.add_argument("--weapon", required=True, choices=sorted(WEAPONS))
    k.add_argument("--var", default="normal")
    k.add_argument("--loc", default="chest")
    k.add_argument("--str", type=int, default=10)
    k.add_argument("--strike", type=int, default=5)
    k.add_argument("--dm", type=float, default=1.0)
    k.add_argument("--sharp", action="store_true")
    k.add_argument("--dull", action="store_true")
    k.add_argument("--mod", type=int, default=0)
    k.add_argument("--armor", default="Skin", choices=sorted(ARMORS))
    k.add_argument("--tgh", type=float, default=5.0)
    k.add_argument("--dl", type=int, default=-5)
    k.add_argument("--defense", default="none", choices=["none", "evade", "block"])
    k.add_argument("--block", type=int, default=0)
    k.add_argument("--gauntlets", action="store_true")
    k.add_argument("--helmet", action="store_true")
    k.add_argument("--die", type=int)
    k.set_defaults(fn=cmd_attack)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
