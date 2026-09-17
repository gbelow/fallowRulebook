"""
Fallow single-attack resolver: exact enumeration of the exploding d10.

Pipeline (combat.tex / gear.tex / play.tex, 2026-09-17):
  declare (variation, location) -> roll -> degree -> HOP -> HOP policy
  -> damage -> cut-or-blunt -> tier -> location cap -> IL / bleed / wound.

Everything after the die is deterministic, so a cell of the sweep is an exact
probability distribution over outcomes, not a sample.  Run with no arguments
for a calibration ladder; see `python fallow_sim.py -h`.

ASSUMPTIONS the text does not pin down (search for "ASSUME"):
  A1  Bypass on layered metal armor hits the inner RES, but the inner layer is
      still metal, so cutting it still needs Penetrating.
  A2  Piercing halves IL per tier, rounded down: 0/2/5/10/15/25.
  A3  HOP policy is greedy: try every affordable set of {bypass, penetrating,
      smash}, spend the rest on extra cut, keep the best outcome.
  A4  Cut vs blunt: higher tier wins; tie -> blunt (it interrupts at T1+).
  A5  Heavy / braced STR bonuses are floored.
  A6  Penetrating used as extra cut (fiber armor, or already penetrating)
      adds 2 x DM per HOP (the bladed+piercing rate).
  A7  Body armor also covers head and legs; the hand has no armor unless
      gauntlets (text).  Head bypass hits flesh (text).
  A8  Whip and claws are given hardness 4 and 3 respectively.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

# ----------------------------------------------------------------------------
# Dice
# ----------------------------------------------------------------------------

def d6_chain(depth: int = 8) -> dict[int, Fraction]:
    """Distribution of: roll 1d6, keep adding while it shows 6."""
    out: dict[int, Fraction] = {}
    p = Fraction(1)
    base = 0
    for _ in range(depth):
        for face in range(1, 6):
            out[base + face] = out.get(base + face, 0) + p * Fraction(1, 6)
        base += 6
        p *= Fraction(1, 6)
    out[base] = out.get(base, 0) + p     # truncation mass on the last value
    return out


def exploding_d10() -> dict[int, Fraction]:
    """Exact distribution of the Fallow d10 (play.tex, Exploding die)."""
    chain = d6_chain()
    out: dict[int, Fraction] = {}
    tenth = Fraction(1, 10)
    for face in range(2, 10):
        out[face] = out.get(face, 0) + tenth
    for k, p in chain.items():
        out[10 + k] = out.get(10 + k, 0) + tenth * p   # 10 explodes up
        out[1 - k] = out.get(1 - k, 0) + tenth * p     # 1 explodes down
    return out


D10 = {k: float(v) for k, v in exploding_d10().items()}   # exact, then float for speed

# ----------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Attack:
    name: str
    blunt: int
    cut: int
    props: frozenset
    hardness: int = 4          # metal unless stated
    res: int = 20
    heavy_max: int = 0         # highest heavy degree allowed
    heavy_min: int = 0         # heavy I-III means heavy I is the minimum

    def has(self, p: str) -> bool:
        return p in self.props


def A(name, blunt, cut, props, hardness=4, res=20):
    props = props.split()
    hmax = hmin = 0
    for p in props:
        if p.startswith("heavy"):
            deg = p[5:]                      # heavy1, heavy1-2, heavy2-3 ...
            if "-" in deg:
                lo, hi = deg.split("-")
                hmin, hmax = int(lo), int(hi)
            else:
                hmax = int(deg)
    props = [p for p in props if not p.startswith("heavy")]
    return Attack(name, blunt, cut, frozenset(props), hardness, res, hmax, hmin)


# Melee attack rows from gear.tex (thrown / ranged rows omitted).
WEAPONS = {a.name: a for a in [
    A("Punch",              5,  0, "heavy1 smash", hardness=2),
    A("Claws",              0,  5, "hooked", hardness=3, res=10),
    A("Gauntlet",           8,  0, "heavy1 smash", res=25),
    A("Dagger",             4, 15, "piercing bladed precise heavy1 DEF", res=15),
    A("Club",               8,  0, "DEF heavy1", res=15),
    A("Stiletto",           4, 15, "penetrating precise piercing heavy1", res=15),
    A("Whip",               0,  6, "", res=10),
    A("ShortSword thrust",  4, 16, "precise piercing bladed"),
    A("ShortSword cut",     8, 16, "sweep DEF heavy1 bladed"),
    A("Rapier",             5, 16, "precise piercing penetrating", res=15),
    A("ShortSpear",         6, 24, "braced piercing penetrating heavy1"),
    A("Mace",              12,  0, "heavy1-2 smash", res=50),
    A("BattleAxe",         10, 15, "heavy1-2 bladed", res=25),
    A("Longsword cut",     10, 18, "sweep DEF heavy1 bladed"),
    A("Longsword halfsw",   4, 16, "piercing penetrating precise heavy1"),
    A("Longsword thrust",   4, 16, "piercing"),
    A("Pike",               6, 24, "braced piercing heavy1"),
    A("Halberd spear",      6, 24, "braced piercing penetrating heavy1"),
    A("Halberd hook",       5, 12, "hook bladed", res=30),
    A("Halberd axe",       12, 20, "heavy1-3 bladed", res=30),
    A("Warhammer spear",    6, 24, "braced piercing penetrating heavy1"),
    A("Warhammer hook",     5, 12, "hook bladed", res=30),
    A("Warhammer head",    14,  0, "heavy2-3 smash", res=100),
    A("Bardiche",          12, 20, "heavy1-3 sweep bladed", res=30),
    A("Greatsword cut",    12, 18, "sweep DEF heavy1-2 bladed", res=30),
    A("Greatsword thrust",  6, 20, "piercing heavy1 braced"),
]}


@dataclass(frozen=True)
class Armor:
    name: str
    res: int
    inner: Optional[int]       # inner-layer RES; None = unlayered
    prot: int
    ins: int
    deflection: int
    hardness: int              # 2 fiber, 4 metal


ARMORS = {a.name: a for a in [
    Armor("Skin",        0, None, 0, 0, 4, 2),
    Armor("Clothing",    3, None, 0, 2, 4, 2),
    Armor("FurCoat",     7, None, 2, 6, 5, 2),
    Armor("ThickHide",   8, None, 4, 7, 5, 2),
    Armor("Gambeson",   10, None, 3, 6, 5, 2),
    Armor("Padded",     12, None, 6, 8, 5, 2),
    Armor("ChainShirt",  8, None, 3, 5, 5, 4),
    Armor("Hauberk",    10, None, 5, 6, 5, 4),
    Armor("Brigandine", 12, 8,    8, 8, 6, 4),
    Armor("HalfArmor",  16, 10,  10, 7, 5, 4),
    Armor("FullArmor",  16, 10,  10, 8, 7, 4),
    Armor("Reinforced", 18, 10,  12, 8, 8, 4),
]}

TIER_IL = [1, 5, 10, 20, 30, 50]
TIER_BLEED = [0, 0, 1, 2, 3, 4]
LOCATION_PENALTY = {"chest": 0, "leg": 0, "head": -5, "hand": -10}
LOCATION_CAP = {"chest": 5, "leg": 3, "head": 5, "hand": 2}
# heavy degree -> (STR multiplier, to-hit penalty); AP/STA not modelled here
HEAVY = {0: (0.0, 0), 1: (0.5, 0), 2: (1.0, -2), 3: (1.5, -3)}
VARIATIONS = ["normal", "heavy1", "heavy2", "heavy3", "braced"]


@dataclass
class Attacker:
    STR: int = 10
    strike: int = 5            # Melee + strike bonus
    DM: float = 1.0
    sharp: bool = False
    dull: bool = False


@dataclass
class Defender:
    armor: Armor = ARMORS["Skin"]
    TGH: float = 5.0
    DL: int = -5               # Defend value if defending, else SD (-5 - SM)
    defense: str = "none"      # none | evade | block
    block: int = 0             # block value (STR, 2xSTR, ...) for defense=block
    gauntlets: bool = False
    closed_helmet: bool = False


@dataclass
class Situation:
    variation: str = "normal"
    location: str = "chest"
    to_hit_mod: int = 0        # opportunity +2, visibility -2, IL penalty ...


WOUND_VALUE = {"": 0, "broken hand": 20, "amputated hand": 40,
               "broken leg": 25, "amputated leg": 50, "shocked": 30}


@dataclass
class Outcome:
    degree: str                # miss | graze | hit
    hop: int = 0
    spent: tuple = ()
    dtype: str = "-"
    damage: float = 0.0
    tier: int = -1             # real tier, -1 = below armor
    body_tier: int = -1
    il: float = 0.0
    bleed: int = 0
    wound: str = ""
    interrupt: bool = False
    stun: bool = False
    ko: bool = False
    death: bool = False

    def value(self) -> float:
        """Greedy HOP policy scoring (ASSUME A3)."""
        return (self.il + 3 * self.bleed + WOUND_VALUE[self.wound]
                + 5 * self.stun + 100 * self.ko + 1000 * self.death)

    def key(self):
        return (self.degree, self.dtype, self.tier, self.spent, self.wound,
                self.stun, self.ko, self.death)

# ----------------------------------------------------------------------------
# Resolution
# ----------------------------------------------------------------------------

def _tier(damage: float, armor: float, tgh: float) -> int:
    if damage < armor:
        return -1
    if tgh <= 0:
        return 5
    return min(5, int(math.floor((damage - armor) / tgh)))


def _heavy_degree(variation: str) -> int:
    return {"normal": 0, "heavy1": 1, "heavy2": 2, "heavy3": 3, "braced": 0}[variation]


def resolve_degree(degree: str, hop: int, atk: Attack, att: Attacker,
                   dfn: Defender, sit: Situation) -> Outcome:
    """Best outcome the attacker can buy with `hop` at this degree."""
    if degree == "miss" and dfn.defense != "block":
        return Outcome("miss")
    if degree == "graze" and atk.has("piercing"):
        return Outcome("miss")

    loc = sit.location
    hv = _heavy_degree(sit.variation)
    str_mult = 1.5 if sit.variation == "braced" else HEAVY[hv][0]
    bonus = math.floor(str_mult * att.STR)                        # ASSUME A5
    base_blunt = atk.blunt * att.DM + bonus
    base_cut = atk.cut * att.DM + bonus

    # --- location armor ---------------------------------------------------
    arm = dfn.armor
    if loc == "hand" and not dfn.gauntlets:
        arm = ARMORS["Skin"]
    can_bypass = atk.has("precise") and (
        (loc == "head" and not dfn.closed_helmet)                 # bypass hits flesh
        or (loc != "head" and arm.inner is not None))
    can_pen = atk.has("penetrating")
    can_smash = atk.has("smash")
    can_cut_extra = atk.has("bladed") and not att.dull
    cut_rate = (2 if atk.has("piercing") else 1) * att.DM
    if att.sharp and can_cut_extra and not atk.has("piercing"):
        base_cut += 1.5 * att.DM

    best: Optional[Outcome] = None
    options = [("bypass", can_bypass), ("penetrating", can_pen), ("smash", can_smash)]
    for flags in itertools.product([False, True], repeat=3):
        if any(f and not ok for (_, ok), f in zip(options, flags)):
            continue
        chosen = tuple(name for (name, _), f in zip(options, flags) if f)
        cost = len(chosen) * arm.deflection
        if cost > hop:
            continue
        rest = hop - cost
        bypass = "bypass" in chosen
        pen = "penetrating" in chosen
        smash = "smash" in chosen

        res, prot = arm.res, arm.prot
        if bypass:
            if loc == "head":
                res, prot = 0, 0
            else:
                res = arm.inner
        # ASSUME A1: inner layer keeps the outer material
        can_cut = atk.hardness > arm.hardness or (pen and atk.hardness == arm.hardness)
        if loc == "head" and bypass:
            can_cut = True                                        # flesh
        # penetrating: free extra cut vs softer targets, extra cut with the
        # leftover HOP once the deflection has been paid vs same hardness
        pen_as_extra = atk.has("penetrating") and (arm.hardness < atk.hardness or pen)
        cut, blunt = base_cut, base_blunt
        if rest > 0 and (can_cut_extra or pen_as_extra):
            cut += rest * cut_rate                                # ASSUME A6

        mult, reduce = 1.0, 0.0
        if degree == "graze":
            if dfn.defense == "block":
                reduce = dfn.block
            else:
                mult = 0.5
        elif degree == "miss":                                   # only with block
            reduce = 1.5 * dfn.block
        cut = max(0.0, math.floor(cut * mult) - reduce)
        blunt = max(0.0, math.floor(blunt * mult) - reduce)

        t_cut = _tier(cut, res, dfn.TGH) if can_cut and atk.cut > 0 else -1
        t_blunt = _tier(blunt, prot, dfn.TGH) if atk.blunt > 0 else -1
        if t_cut > t_blunt:                                       # ASSUME A4
            dtype, dmg, tier = "cut", cut, t_cut
        else:
            dtype, dmg, tier = "blunt", blunt, t_blunt

        o = Outcome(degree, hop, chosen, dtype, dmg, tier)
        if tier >= 0:
            body = min(tier, LOCATION_CAP[loc])
            o.body_tier = body
            il = TIER_IL[body]
            if atk.has("piercing"):
                il = il // 2                                      # ASSUME A2
            o.il = il
            o.bleed = TIER_BLEED[body] * (2 if atk.has("vicious") else 1)
            o.interrupt = dtype == "blunt" and tier >= 1
            o.stun = smash and tier >= 1
            amput = not atk.has("piercing")
            if loc == "hand":
                if tier >= 4 and amput:
                    o.wound = "amputated hand"
                elif tier >= 2:
                    o.wound = "broken hand"
            elif loc == "leg":
                if tier >= 5 and amput:
                    o.wound = "amputated leg"
                elif tier >= 3:
                    o.wound = "broken leg"
            elif loc == "chest":
                if tier >= 4 and dtype == "blunt" and smash:
                    o.wound = "shocked"
            elif loc == "head":
                if tier >= 4:
                    o.death = True
                elif tier >= 3 or o.stun:
                    o.ko = True
        if best is None or o.value() > best.value():
            best = o
    return best if best is not None else Outcome(degree, hop)


def check_variation(atk: Attack, variation: str) -> None:
    hv = _heavy_degree(variation)
    if hv and hv > atk.heavy_max:
        raise ValueError(f"{atk.name} has no heavy {hv}")
    if variation == "normal" and atk.heavy_min:
        raise ValueError(f"{atk.name} requires at least heavy {atk.heavy_min}")
    if variation == "braced" and not atk.has("braced"):
        raise ValueError(f"{atk.name} cannot brace")


def fixed_bonus(atk: Attack, att: Attacker, dfn: Defender, sit: Situation) -> int:
    """Everything added to the die: skill + modifiers - DL."""
    check_variation(atk, sit.variation)
    hv = _heavy_degree(sit.variation)
    return att.strike + sit.to_hit_mod + HEAVY[hv][1] + LOCATION_PENALTY[sit.location] - dfn.DL


def degree_of(score: int):
    degree = "hit" if score >= 5 else "graze" if score >= 0 else "miss"
    return degree, max(0, score - 5)


def resolve_die(die: int, atk: Attack, att: Attacker, dfn: Defender, sit: Situation) -> Outcome:
    """Outcome of one specific die result."""
    degree, hop = degree_of(die + fixed_bonus(atk, att, dfn, sit))
    return resolve_degree(degree, hop, atk, att, dfn, sit)


def attack_distribution(atk: Attack, att: Attacker, dfn: Defender, sit: Situation):
    """[(probability, Outcome)] over the exploding d10."""
    fixed = fixed_bonus(atk, att, dfn, sit)
    cache: dict = {}
    dist = []
    for die, p in D10.items():
        key = degree_of(die + fixed)
        if key not in cache:
            cache[key] = resolve_degree(key[0], key[1], atk, att, dfn, sit)
        dist.append((p, cache[key]))
    return dist

# ----------------------------------------------------------------------------
# Summaries
# ----------------------------------------------------------------------------

def summarize(dist) -> dict:
    s = {"p_hit": 0.0, "p_graze": 0.0, "p_miss": 0.0, "e_il": 0.0, "e_bleed": 0.0,
         "p_injury": 0.0, "p_T2+": 0.0, "p_T3+": 0.0, "p_T4+": 0.0, "p_wound": 0.0,
         "p_stun": 0.0, "p_ko": 0.0, "p_death": 0.0, "e_hop_hit": 0.0, "mode_type": "-"}
    types: dict = {}
    for p, o in dist:
        p = float(p)
        s["p_" + o.degree] += p
        s["e_il"] += p * o.il
        s["e_bleed"] += p * o.bleed
        if o.tier >= 0:
            s["p_injury"] += p
            types[o.dtype] = types.get(o.dtype, 0) + p
        s["p_T2+"] += p * (o.tier >= 2)
        s["p_T3+"] += p * (o.tier >= 3)
        s["p_T4+"] += p * (o.tier >= 4)
        s["p_wound"] += p * bool(o.wound)
        s["p_stun"] += p * o.stun
        s["p_ko"] += p * o.ko
        s["p_death"] += p * o.death
        if o.degree == "hit":
            s["e_hop_hit"] += p * o.hop
    if s["p_hit"]:
        s["e_hop_hit"] /= s["p_hit"]
    if types:
        s["mode_type"] = max(types, key=types.get)
    return s


def variations_for(atk: Attack) -> list:
    out = []
    if atk.heavy_min == 0:
        out.append("normal")
    for h in range(max(1, atk.heavy_min), atk.heavy_max + 1):
        out.append(f"heavy{h}")
    if atk.has("braced"):
        out.append("braced")
    return out

# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def cmd_single(a):
    atk = WEAPONS[a.weapon]
    att = Attacker(a.str, a.strike, a.dm, a.sharp, a.dull)
    tgh = a.tgh if a.tgh is not None else 0.5 * a.def_str * a.dm
    dfn = Defender(ARMORS[a.armor], tgh, a.dl, a.defense, a.block, a.gauntlets, a.helmet)
    sit = Situation(a.variation, a.location, a.mod)
    dist = attack_distribution(atk, att, dfn, sit)
    print(f"{atk.name} [{sit.variation}, {sit.location}]  STR {att.STR} strike {att.strike}"
          f"  vs {dfn.armor.name} TGH {tgh:g} DL {dfn.DL} ({dfn.defense})")
    agg: dict = {}
    sample: dict = {}
    dmg: dict = {}
    for p, o in dist:
        agg[o.key()] = agg.get(o.key(), 0) + p
        sample[o.key()] = o
        lo, hi = dmg.get(o.key(), (o.damage, o.damage))
        dmg[o.key()] = (min(lo, o.damage), max(hi, o.damage))
    print(f"{'P':>7} {'deg':6} {'type':5} {'tier':>4} {'dmg':>9} {'IL':>4} {'bl':>2}  spent / effects")
    for key, p in sorted(agg.items(), key=lambda kv: -kv[1]):
        o = sample[key]
        lo, hi = dmg[key]
        rng = f"{lo:g}" if lo == hi else f"{lo:g}-{hi:g}"
        fx = " ".join(x for x in [",".join(o.spent), o.wound, "STUN" if o.stun else "",
                                  "KO" if o.ko else "", "DEATH" if o.death else ""] if x)
        print(f"{float(p):7.3f} {o.degree:6} {o.dtype:5} {o.tier:>4} {rng:>9} "
              f"{o.il:>4g} {o.bleed:>2}  {fx}")
    s = summarize(dist)
    print("\n" + "  ".join(f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}"
                           for k, v in s.items()))


def cmd_sweep(a):
    weapons = a.weapons or list(WEAPONS)
    armors = a.armors or list(ARMORS)
    strs = a.strs or [8, 10, 12, 14, 16]
    tghs = a.tghs or [4, 5, 6, 8]
    dls = a.dls or [-5, 0, 5, 10]
    locs = a.locations or ["chest"]
    rows = []
    for wname in weapons:
        atk = WEAPONS[wname]
        for var in (a.variations or variations_for(atk)):
            if var not in variations_for(atk):
                continue
            for STR in strs:
                att = Attacker(STR, a.strike)
                for aname in armors:
                    for tgh in tghs:
                        for dl in dls:
                            dfn = Defender(ARMORS[aname], tgh, dl)
                            for loc in locs:
                                s = summarize(attack_distribution(atk, att, dfn, Situation(var, loc)))
                                rows.append({"weapon": wname, "variation": var, "STR": STR,
                                             "armor": aname, "TGH": tgh, "DL": dl,
                                             "location": loc, **s})
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {len(rows)} rows to {a.csv}")
    else:
        cols = ["weapon", "variation", "STR", "armor", "TGH", "DL", "location",
                "p_hit", "e_il", "p_T2+", "p_T3+", "p_wound", "p_ko", "p_death", "mode_type"]
        print(" ".join(f"{c:>10}" for c in cols))
        for r in rows:
            print(" ".join(f"{r[c]:>10.3f}" if isinstance(r[c], float) else f"{str(r[c]):>10}"
                           for c in cols))


def cmd_ladder(a):
    """Calibration ladder: each weapon form x variation vs the armor classes."""
    classes = ["Skin", "Gambeson", "Hauberk", "HalfArmor", "Reinforced"]
    att = Attacker(a.str, a.strike)
    print(f"E[IL] per attack (P(T2+)%), STR {a.str} strike {a.strike} vs TGH {a.tgh:g} "
          f"DL {a.dl}, chest, greedy HOP")
    print(f"{'attack':22}{'var':8}" + "".join(f"{c:>16}" for c in classes))
    for wname, atk in WEAPONS.items():
        for var in variations_for(atk):
            cells = []
            for c in classes:
                dfn = Defender(ARMORS[c], a.tgh, a.dl)
                s = summarize(attack_distribution(atk, att, dfn, Situation(var, "chest")))
                cells.append(f"{s['e_il']:5.2f} ({100*s['p_T2+']:3.0f}%)")
            print(f"{wname:22}{var:8}" + "".join(f"{c:>16}" for c in cells))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("single", help="full outcome distribution for one attack")
    s.add_argument("weapon", choices=list(WEAPONS))
    s.add_argument("armor", choices=list(ARMORS))
    s.add_argument("--str", type=int, default=10)
    s.add_argument("--strike", type=int, default=5)
    s.add_argument("--dm", type=float, default=1.0)
    s.add_argument("--def-str", type=int, default=10, help="defender STR (TGH = 0.5 x STR x DM)")
    s.add_argument("--tgh", type=float, default=None, help="override TGH")
    s.add_argument("--dl", type=int, default=-5, help="Defend value, or SD (-5 still, -2 moving)")
    s.add_argument("--defense", choices=["none", "evade", "block"], default="none")
    s.add_argument("--block", type=int, default=0)
    s.add_argument("--variation", choices=VARIATIONS, default="normal")
    s.add_argument("--location", choices=list(LOCATION_PENALTY), default="chest")
    s.add_argument("--mod", type=int, default=0, help="extra to-hit modifier")
    s.add_argument("--sharp", action="store_true")
    s.add_argument("--dull", action="store_true")
    s.add_argument("--gauntlets", action="store_true")
    s.add_argument("--helmet", action="store_true", help="closed helmet")
    s.set_defaults(fn=cmd_single)

    w = sub.add_parser("sweep", help="weapon x STR x armor x TGH x DL grid")
    w.add_argument("--weapons", nargs="*")
    w.add_argument("--variations", nargs="*", choices=VARIATIONS)
    w.add_argument("--strs", nargs="*", type=int)
    w.add_argument("--armors", nargs="*")
    w.add_argument("--tghs", nargs="*", type=float)
    w.add_argument("--dls", nargs="*", type=int)
    w.add_argument("--locations", nargs="*", choices=list(LOCATION_PENALTY))
    w.add_argument("--strike", type=int, default=5)
    w.add_argument("--csv", help="write results here instead of printing")
    w.set_defaults(fn=cmd_sweep)

    l = sub.add_parser("ladder", help="calibration ladder vs the five armor classes")
    l.add_argument("--str", type=int, default=10)
    l.add_argument("--strike", type=int, default=5)
    l.add_argument("--tgh", type=float, default=5)
    l.add_argument("--dl", type=int, default=0)
    l.set_defaults(fn=cmd_ladder)

    a = p.parse_args(argv)
    if a.cmd is None:
        a = p.parse_args(["ladder"])
    a.fn(a)


if __name__ == "__main__":
    main()
