"""
Fallow duel Monte Carlo, built on the exact single-attack resolver in
fallow_sim.py.  Two stationary size-3 fighters, full AP / STA / IL / bleed /
morale loop, sampled N times.

    python sim/fallow_fight.py --a-attacks "Longsword cut" "Longsword thrust" --a-armor Hauberk \
        --b-attacks Mace --b-armor HalfArmor --b-defense block -n 5000

Round (combat.tex, Turns and Actions):
  * 8 AP each, minus negative AP carried over; one combat surge per round.
  * Morale test (Will vs 2 x injury penalty, +2 if out of STA) at round start.
  * Turns alternate, first decided by Cunning + d10.  A turn is one action:
    attack, rest, or pass.  Reserve AP for defense while the opponent can still
    attack.  Surge when it buys an attack that would otherwise not fit.
  * Attack choice = best expected fight value per AP over every affordable
    (weapon row x variation x location), using the exact distribution from
    fallow_sim against the defense the opponent is expected to use.
  * Bleed ticks on every STA spent and at round end; 3x bleed at fight end.

ASSUMPTIONS (F-series; the resolver's A-series still apply):
  F1  Wound IL is tracked separately and does not count toward the injury
      penalty or collapse.
  F2  A broken or amputated hand disables the fighter (weapon hand assumed).
  F3  Interrupt / stun on a target that defended interrupts the defense only
      (its AP is already spent, nothing more is lost).  On an undefended
      target (SD) it costs -2 AP (stun -4); AP may go negative and is
      deducted from the next round.
  F4  Rest recovers floor(STA/4), minimum 1.
  F5  Morale miss = routed (limit stress action read as flight); the fight
      ends.  Afraid (no combat surge) clears on a later Will hit.
  F6  A fighter defends whenever it has 2 AP and a defense configured.
  F7  Injury penalty applies to Strike, Defend, the STR damage bonus and the
      block value.  Will is mental and is not affected.
  F8  Bleed intensities from separate injuries stack.
  F9  Unspent AP is lost; surge AP not used by the surge attack is lost.
  F10 Both stationary (SD -5), size 3, no movement, reach or braced attacks.
  F11 Evasive jump = evade +floor((AGI - injury penalty)/3) to Defend, 1 STA;
      space to jump is always available; falls back to evade at 0 STA.
"""
from __future__ import annotations

import argparse
import os
import random
import sys
from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fallow_sim import (ARMORS, D10, WEAPONS, Attacker, Defender, Outcome,  # noqa: E402
                        Situation, attack_distribution, resolve_die,
                        variations_for)

DIE_FACES = list(D10)
DIE_WEIGHTS = [D10[k] for k in DIE_FACES]
ATTACK_AP = {"normal": 3, "heavy1": 4, "heavy2": 5, "heavy3": 6}
ATTACK_STA = {"normal": 0, "heavy1": 0, "heavy2": 1, "heavy3": 1}
SD = -5
WIN = 100.0
COLLAPSE_IL = 40
DEATH_IL = 50


@dataclass
class Fighter:
    name: str = "A"
    STR: int = 10
    AGI: int = 10
    STA: int = 10
    melee: int = 5
    strike_bonus: int = 0
    defend_bonus: int = 0
    will: int = 5
    cunning: int = 5
    attacks: tuple = ("Longsword cut",)
    armor: str = "Skin"
    gauntlets: bool = False
    closed_helmet: bool = False
    defense: str = "evade"         # evade | jump | block | none
    jump_reserve: int = 0          # jump only while STA stays above this
    block2h: bool = False          # block value 2 x STR (two-handed or shield)
    TGH: Optional[float] = None    # default 0.5 x STR
    # policy
    reserve_ap: int = 2
    locations: tuple = ("chest", "head")
    surge: bool = True
    rest_below: int = 3

    def tgh(self) -> float:
        return self.TGH if self.TGH is not None else 0.5 * self.STR


@dataclass
class State:
    sta: int
    il: float = 0.0
    wound_il: int = 0
    bleed: int = 0
    ap: int = 8
    neg_ap: int = 0
    surged: bool = False
    afraid: bool = False
    passed: bool = False
    down: str = ""                 # death | ko | collapse | shocked | disabled | routed
    actions: Counter = field(default_factory=Counter)

    @property
    def pen(self) -> int:
        return int(self.il // 10)


def roll(rng: random.Random) -> int:
    return rng.choices(DIE_FACES, DIE_WEIGHTS)[0]


def fight_value(o: Outcome, target_il: float) -> float:
    """What an outcome is worth toward winning the duel (policy only)."""
    if o.death or o.ko or o.wound in ("shocked", "broken hand", "amputated hand"):
        return WIN
    need = max(1.0, COLLAPSE_IL + 1 - target_il)
    if o.il >= need:
        return WIN
    v = WIN * o.il / COLLAPSE_IL
    v += WIN * o.bleed * 3 / COLLAPSE_IL      # ~3 more round ends
    v += 3 * o.interrupt + 6 * o.stun
    return v


@lru_cache(maxsize=None)
def expected_value(row: str, var: str, loc: str, STR: int, strike: int,
                   armor: str, tgh: float, DL: int, defense: str, block: int,
                   gauntlets: bool, helmet: bool, target_il: int) -> float:
    atk = WEAPONS[row]
    att = Attacker(STR, strike)
    dfn = Defender(ARMORS[armor], tgh, DL, defense, block, gauntlets, helmet)
    dist = attack_distribution(atk, att, dfn, Situation(var, loc))
    return sum(p * fight_value(o, target_il) for p, o in dist)


def defend_value(f: Fighter, s: State) -> int:
    return f.melee + f.defend_bonus - s.pen


def will_jump(f: Fighter, s: State) -> bool:
    return f.defense == "jump" and s.sta - 1 >= f.jump_reserve


def defense_now(f: Fighter, s: State):
    """(DL, resolver defense, block value, STA cost) if the fighter defends now."""
    if will_jump(f, s):
        return defend_value(f, s) + max(0, f.AGI - s.pen) // 3, "evade", 0, 1
    if f.defense == "jump":
        return defend_value(f, s), "evade", 0, 0
    return defend_value(f, s), f.defense, block_value(f, s), 0


def block_value(f: Fighter, s: State) -> int:
    return (2 if f.block2h else 1) * max(0, f.STR - s.pen)


def predicted_defense(g: Fighter, t: State):
    """(DL, defense, block) the opponent is expected to use right now."""
    if t.down or t.ap < 2 or g.defense == "none":
        return SD, "none", 0
    return defense_now(g, t)[:3]


def spend_sta(s: State, n: int):
    s.sta -= n
    s.il += s.bleed * n                       # bleed ticks per STA spent


def apply_status(t: State):
    if t.down:
        return
    if t.il > DEATH_IL:
        t.down = "death"
    elif t.il > COLLAPSE_IL:
        t.down = "collapse"


def best_attack(f: Fighter, s: State, g: Fighter, t: State, avail_ap: int):
    DL, dfs, blk = predicted_defense(g, t)
    best = None
    for row in f.attacks:
        atk = WEAPONS[row]
        for var in variations_for(atk):
            if var == "braced":
                continue
            cost, sta = ATTACK_AP[var], ATTACK_STA[var]
            if cost > avail_ap or sta > s.sta:
                continue
            for loc in f.locations:
                ev = expected_value(row, var, loc, max(0, f.STR - s.pen),
                                    f.melee + f.strike_bonus - s.pen, g.armor, g.tgh(),
                                    DL, dfs, blk, g.gauntlets, g.closed_helmet, int(t.il))
                score = ev / cost
                if best is None or score > best[0]:
                    best = (score, cost, sta, row, var, loc)
    return best


def execute_attack(f, s, g, t, row, var, loc, rng, log):
    if t.ap >= 2 and g.defense != "none" and not t.down:
        t.ap -= 2
        DL, dfs, blk, sta = defense_now(g, t)
        if sta:
            spend_sta(t, sta)
            t.actions["jump"] += 1
            apply_status(t)
    else:
        DL, dfs, blk = SD, "none", 0
    att = Attacker(max(0, f.STR - s.pen), f.melee + f.strike_bonus - s.pen)
    dfn = Defender(ARMORS[g.armor], g.tgh(), DL, dfs, blk, g.gauntlets, g.closed_helmet)
    o = resolve_die(roll(rng), WEAPONS[row], att, dfn, Situation(var, loc))
    s.actions[f"{row}/{var}/{loc}"] += 1
    if log is not None:
        log.append(f"  {f.name}: {row} {var} {loc} vs DL {DL} ({dfs}) -> {o.degree} "
                   f"{o.dtype} T{o.tier} IL {o.il:g} bleed {o.bleed} {','.join(o.spent)} "
                   f"{o.wound} {'STUN' if o.stun else ''} {'KO' if o.ko else ''} "
                   f"{'DEATH' if o.death else ''}")
    t.il += o.il
    t.bleed += o.bleed
    if dfs == "none":                 # F3: a defense absorbs the interrupt
        if o.stun:
            t.ap -= 4
        elif o.interrupt:
            t.ap -= 2
    if o.death:
        t.down = "death"
    elif o.ko:
        t.down = "ko"
    elif o.wound == "shocked":
        t.down = "shocked"
    elif o.wound in ("broken hand", "amputated hand"):
        t.down = "disabled"
    elif o.wound in ("broken leg", "amputated leg"):
        t.wound_il += 20
    apply_status(t)


def take_turn(f, s, g, t, rng, log):
    if s.down or s.ap < 1:
        s.passed = True
        return
    threat = (not t.down) and t.ap >= 3
    reserve = f.reserve_ap if threat else 0
    best = best_attack(f, s, g, t, s.ap - reserve)
    if best is None and f.surge and not s.surged and not s.afraid and s.sta >= 3:
        # would a combat surge buy an attack?
        cand = best_attack(f, s, g, t, s.ap - reserve + 4)
        if cand is not None and s.sta - 3 >= cand[2]:
            s.surged = True
            s.actions["surge"] += 1
            if log is not None:
                log.append(f"  {f.name}: combat surge")
            spend_sta(s, 3)
            apply_status(s)
            if s.down:
                return
            _, cost, sta, row, var, loc = cand
            s.ap -= max(0, cost - 4)          # surge AP pays first, rest is lost
            if sta:
                spend_sta(s, sta)
            execute_attack(f, s, g, t, row, var, loc, rng, log)
            return
    if best is not None:
        _, cost, sta, row, var, loc = best
        s.ap -= cost
        if sta:
            spend_sta(s, sta)
            apply_status(s)
            if s.down:
                return
        execute_attack(f, s, g, t, row, var, loc, rng, log)
        return
    if s.sta < f.rest_below and s.ap >= 4 and not threat:
        s.ap -= 4
        s.sta = min(f.STA, s.sta + max(1, f.STA // 4))
        s.actions["rest"] += 1
        if log is not None:
            log.append(f"  {f.name}: rest -> STA {s.sta}")
        return
    s.passed = True


def morale(f, s, rng, log):
    if s.down:
        return
    DL = 2 * s.pen + (2 if s.sta <= 0 else 0)
    score = roll(rng) + f.will - (1 if s.afraid else 0) - DL
    if score < 0:
        s.down = "routed"
    elif score < 5:
        s.afraid = True
    else:
        s.afraid = False
    if log is not None and (score < 5):
        log.append(f"  {f.name}: morale {score} -> {'ROUTED' if score < 0 else 'afraid'}")


def fight(A: Fighter, B: Fighter, rng: random.Random, use_morale=True,
          max_rounds=20, log=None) -> dict:
    sA, sB = State(A.STA), State(B.STA)
    rounds = 0
    for rnd in range(1, max_rounds + 1):
        rounds = rnd
        if log is not None:
            log.append(f"-- round {rnd}: {A.name} IL {sA.il:g} STA {sA.sta} | "
                       f"{B.name} IL {sB.il:g} STA {sB.sta}")
        for s in (sA, sB):
            s.ap = 8 - s.neg_ap
            s.neg_ap = 0
            s.surged = False
            s.passed = False
        if use_morale:
            morale(A, sA, rng, log)
            morale(B, sB, rng, log)
        if sA.down or sB.down:
            break
        order = [(A, sA, B, sB), (B, sB, A, sA)]
        ca, cb = roll(rng) + A.cunning, roll(rng) + B.cunning
        if cb > ca or (cb == ca and rng.random() < 0.5):
            order.reverse()
        i = 0
        while not (sA.down or sB.down):
            f, s, g, t = order[i % 2]
            if s.passed and not t.passed:
                i += 1
                continue
            if s.passed and t.passed:
                break
            take_turn(f, s, g, t, rng, log)
            i += 1
        if sA.down or sB.down:
            break
        for s in (sA, sB):
            s.il += s.bleed
            apply_status(s)
            if s.ap < 0:
                s.neg_ap = -s.ap
        if sA.down or sB.down:
            break
    for s in (sA, sB):                        # combat ends: 3 x bleed
        if s.down not in ("death",):
            s.il += 3 * s.bleed
            if s.il > DEATH_IL and not s.down:
                s.down = "death"
    if sA.down and not sB.down:
        winner, reason = B.name, sA.down
    elif sB.down and not sA.down:
        winner, reason = A.name, sB.down
    elif sA.down and sB.down:
        winner, reason = "draw", f"{sA.down}/{sB.down}"
    else:
        winner, reason = "draw", "timeout"
    return {"winner": winner, "reason": reason, "rounds": rounds,
            "il": (sA.il, sB.il), "sta": (sA.sta, sB.sta),
            "actions": (sA.actions, sB.actions)}


def simulate(A, B, n=2000, seed=1, use_morale=True, max_rounds=20) -> dict:
    rng = random.Random(seed)
    wins = Counter()
    reasons = {A.name: Counter(), B.name: Counter(), "draw": Counter()}
    rounds = 0
    il = [0.0, 0.0]
    sta = [0.0, 0.0]
    acts = [Counter(), Counter()]
    for _ in range(n):
        r = fight(A, B, rng, use_morale, max_rounds)
        wins[r["winner"]] += 1
        reasons[r["winner"]][r["reason"]] += 1
        rounds += r["rounds"]
        for i in range(2):
            il[i] += r["il"][i]
            sta[i] += r["sta"][i]
            acts[i].update(r["actions"][i])
    return {"n": n, "wins": wins, "reasons": reasons, "rounds": rounds / n,
            "il": [x / n for x in il], "sta": [x / n for x in sta], "actions": acts}


def describe(f: Fighter) -> str:
    return (f"{f.name}: STR {f.STR} AGI {f.AGI} STA {f.STA} melee {f.melee}(+{f.strike_bonus}/+{f.defend_bonus}) "
            f"will {f.will} | {', '.join(f.attacks)} | {f.armor}"
            f"{' +gauntlets' if f.gauntlets else ''}{' +closed helmet' if f.closed_helmet else ''} "
            f"| {f.defense}{' 2h' if f.block2h else ''}"
            f"{f' (reserve {f.jump_reserve} STA)' if f.defense == 'jump' else ''} | reserve {f.reserve_ap}, "
            f"targets {'/'.join(f.locations)}")


def report(A, B, r):
    n = r["n"]
    print(describe(A))
    print(describe(B))
    print(f"n={n}  mean rounds {r['rounds']:.2f}")
    for who in (A.name, B.name, "draw"):
        w = r["wins"][who]
        why = ", ".join(f"{k} {100*v/n:.1f}%" for k, v in r["reasons"][who].most_common())
        print(f"  {who:>6} {100*w/n:5.1f}%   {why}")
    print(f"  mean final IL {A.name} {r['il'][0]:.1f} / {B.name} {r['il'][1]:.1f}   "
          f"mean STA left {r['sta'][0]:.1f} / {r['sta'][1]:.1f}")
    for i, f in enumerate((A, B)):
        tot = sum(r["actions"][i].values())
        mix = ", ".join(f"{k} {100*v/tot:.0f}%" for k, v in r["actions"][i].most_common(5))
        print(f"  {f.name} actions/fight {tot/n:.1f}: {mix}")


def add_fighter_args(p, side):
    d = Fighter()
    g = p.add_argument_group(f"fighter {side}")
    a = lambda name, **kw: g.add_argument(f"--{side}-{name}", **kw)
    a("name", default=side.upper())
    a("str", type=int, default=d.STR)
    a("agi", type=int, default=d.AGI)
    a("sta", type=int, default=d.STA)
    a("melee", type=int, default=d.melee)
    a("strike", type=int, default=0, help="strike bonus")
    a("defend", type=int, default=0, help="defend bonus")
    a("will", type=int, default=d.will)
    a("cunning", type=int, default=d.cunning)
    a("attacks", nargs="+", default=list(d.attacks), metavar="ROW")
    a("armor", choices=list(ARMORS), default=d.armor)
    a("gauntlets", action="store_true")
    a("helmet", action="store_true")
    a("defense", choices=["evade", "jump", "block", "none"], default=d.defense)
    a("jump-reserve", type=int, default=d.jump_reserve, help="keep this much STA; jump above it")
    a("block2h", action="store_true", help="block value 2 x STR")
    a("tgh", type=float, default=None)
    a("reserve", type=int, default=d.reserve_ap)
    a("locations", nargs="+", default=list(d.locations), choices=["chest", "head", "leg", "hand"])
    a("no-surge", action="store_true")
    a("rest-below", type=int, default=d.rest_below)


def fighter_from_args(a, side) -> Fighter:
    v = lambda k: getattr(a, f"{side}_{k}")
    for row in v("attacks"):
        if row not in WEAPONS:
            sys.exit(f"unknown attack row {row!r}; choose from {list(WEAPONS)}")
    return Fighter(v("name"), v("str"), v("agi"), v("sta"), v("melee"), v("strike"), v("defend"),
                   v("will"), v("cunning"), tuple(v("attacks")), v("armor"), v("gauntlets"),
                   v("helmet"), v("defense"), v("jump_reserve"), v("block2h"), v("tgh"), v("reserve"),
                   tuple(v("locations")), not v("no_surge"), v("rest_below"))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_fighter_args(p, "a")
    add_fighter_args(p, "b")
    p.add_argument("-n", type=int, default=2000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--no-morale", action="store_true")
    p.add_argument("--max-rounds", type=int, default=20)
    p.add_argument("--trace", action="store_true", help="print one fight round by round")
    a = p.parse_args(argv)
    A, B = fighter_from_args(a, "a"), fighter_from_args(a, "b")
    if a.trace:
        log = []
        r = fight(A, B, random.Random(a.seed), not a.no_morale, a.max_rounds, log)
        print("\n".join(log))
        print(f"=> {r['winner']} wins ({r['reason']}) after {r['rounds']} rounds; "
              f"IL {r['il'][0]:g}/{r['il'][1]:g}")
        return
    report(A, B, simulate(A, B, a.n, a.seed, not a.no_morale, a.max_rounds))


if __name__ == "__main__":
    main()
