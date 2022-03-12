from itertools import chain, combinations
import sys
from dataclasses import dataclass, field
from typing import List


@dataclass
class Item:
    name: str
    cost: int
    damage: int
    armor: int


SHOP = dict(
    weapons=[
        Item(name="Dagger", cost=8, damage=4, armor=0),
        Item(name="Shortsword", cost=10, damage=5, armor=0),
        Item(name="Warhammer", cost=25, damage=6, armor=0),
        Item(name="Longsword", cost=40, damage=7, armor=0),
        Item(name="Greataxe", cost=74, damage=8, armor=0),
    ],
    armor=[
        Item(name="Leather", cost=13, damage=0, armor=1),
        Item(name="Chainmail", cost=31, damage=0, armor=2),
        Item(name="Splintmail", cost=53, damage=0, armor=3),
        Item(name="Bandedmail", cost=75, damage=0, armor=4),
        Item(name="Platemail", cost=102, damage=0, armor=5),
    ],
    rings=[
        Item(name="Damage +1", cost=25, damage=1, armor=0),
        Item(name="Damage +2", cost=50, damage=2, armor=0),
        Item(name="Damage +3", cost=100, damage=3, armor=0),
        Item(name="Defense +1", cost=20, damage=0, armor=1),
        Item(name="Defense +2", cost=40, damage=0, armor=2),
        Item(name="Defense +3", cost=80, damage=0, armor=3),
    ],
)


@dataclass
class Character:
    hit_points: int
    damage: int
    armor: int


@dataclass
class Scenario:
    cost: int
    player: Character
    items: List[Item] = field(default_factory=list)


def is_victor1(player: Character, boss: Character):
    # count how many turns the player survives
    player_dmg_per_turn = boss.damage - player.armor
    turns_to_kill_player = (player.hit_points + player_dmg_per_turn - 1) // player_dmg_per_turn
    # count how many turns the boss survives
    boss_dmg_per_turn = player.damage - boss.armor
    turns_to_kill_boss = (boss.hit_points + boss_dmg_per_turn - 1) // boss_dmg_per_turn
    return turns_to_kill_boss <= turns_to_kill_player


def is_boss_victor2(player: Character, boss: Character):
    # count how many turns the player survives
    player_dmg_per_turn = max(0, boss.damage - player.armor)
    if player_dmg_per_turn == 0:
        return False
    turns_to_kill_player = (player.hit_points + player_dmg_per_turn - 1) // player_dmg_per_turn
    # count how many turns the boss survives
    boss_dmg_per_turn = max(0, player.damage - boss.armor)
    if boss_dmg_per_turn == 0:
        return True
    turns_to_kill_boss = (boss.hit_points + boss_dmg_per_turn - 1) // boss_dmg_per_turn
    return turns_to_kill_boss > turns_to_kill_player


def parse_input(input):
    values = {}
    for line in input:
        key, value = line.rstrip().split(": ")
        values[key] = int(value)
    return Character(
        hit_points=values["Hit Points"], damage=values["Damage"], armor=values["Armor"]
    )


def compute_scenario():
    for weapon in SHOP["weapons"]:
        for armor in chain((None,), SHOP["armor"]):
            for ring1, ring2 in chain(
                ((None, None),),
                combinations(SHOP["rings"], 2),
                [(r[0], None) for r in combinations(SHOP["rings"], 1)],
            ):
                scenario = Scenario(cost=0, player=Character(hit_points=100, damage=0, armor=0))
                scenario.cost += weapon.cost
                scenario.player.damage += weapon.damage
                scenario.items.append(weapon)
                if armor:
                    scenario.cost += armor.cost
                    scenario.player.armor += armor.armor
                    scenario.items.append(armor)
                if ring1:
                    scenario.cost += ring1.cost
                    scenario.player.damage += ring1.damage
                    scenario.player.armor += ring1.armor
                    scenario.items.append(ring1)
                if ring2:
                    scenario.cost += ring2.cost
                    scenario.player.damage += ring2.damage
                    scenario.player.armor += ring2.armor
                    scenario.items.append(ring2)
                yield scenario


def main1(input):
    boss = parse_input(input)
    min_cost = 1e9
    best_scenario = None
    for scenario in compute_scenario():
        if scenario.cost > min_cost:
            continue
        if is_victor1(scenario.player, boss) and scenario.cost < min_cost:
            min_cost = scenario.cost
            best_scenario = scenario
    return min_cost, best_scenario


def main2(input):
    boss = parse_input(input)
    max_cost = 0
    worst_scenario = None
    for scenario in compute_scenario():
        if scenario.cost < max_cost:
            continue
        if is_boss_victor2(scenario.player, boss) and scenario.cost > max_cost:
            max_cost = scenario.cost
            worst_scenario = scenario
    return max_cost, worst_scenario


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
