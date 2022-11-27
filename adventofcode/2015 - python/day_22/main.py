from collections import defaultdict
import sys
from dataclasses import dataclass, field, replace
from typing import List


@dataclass(frozen=True, slots=True)
class Spell:
    name: str
    cost: int
    damage: int = 0
    healing: int = 0
    armor: int = 0
    mana: int = 0
    effect_duration: int = 1


@dataclass(frozen=True, slots=True)
class Effect:
    remaining_turns: int
    spell: Spell


SPELLS = [
    Spell(name="Magic Missile", cost=53, damage=4),
    Spell(name="Drain", cost=73, damage=2, healing=2),
    Spell(name="Shield", cost=113, armor=7, effect_duration=6),
    Spell(name="Poison", cost=173, damage=3, effect_duration=6),
    Spell(name="Recharge", cost=229, effect_duration=5, mana=101),
]

CHEAPEST_SPELL_COST = min(spell.cost for spell in SPELLS)


@dataclass(frozen=True, slots=True)
class Character:
    hit_points: int
    damage: int
    armor: int = 0
    mana: int = 0


@dataclass(slots=True)
class Scenario:
    cost: int
    player: Character
    boss: Character
    spells: List[Spell] = field(default_factory=list)
    effects: List[Effect] = field(default_factory=list)

    @property
    def player_is_dead(self):
        return self.player.hit_points <= 0

    @property
    def is_won(self):
        return self.boss.hit_points <= 0

    def summary(self):
        return (
            f"cost: {self.cost}, boss: {self.boss.hit_points},"
            f" player: {self.player.hit_points} (armor={self.player.armor},"
            f"mana={self.player.mana}). Spells: {', '.join(s.name for s in self.spells)}"
        )

    @staticmethod
    def apply_effect(scenario, effect):
        spell = effect.spell
        if spell.damage:
            scenario.boss = replace(
                scenario.boss, hit_points=scenario.boss.hit_points - spell.damage
            )
        if spell.healing:
            scenario.player = replace(
                scenario.player, hit_points=scenario.player.hit_points + spell.healing
            )
        if spell.mana:
            scenario.player = replace(scenario.player, mana=scenario.player.mana + spell.mana)
        if spell.armor and scenario.player.armor != spell.armor:
            scenario.player = replace(scenario.player, armor=spell.armor)
        if effect.remaining_turns <= 1:
            return None
        return replace(effect, remaining_turns=effect.remaining_turns - 1)

    def apply_effects(self):
        remaining_effects = []
        new_scenario = replace(self, effects=remaining_effects)
        armor = 0
        for effect in self.effects:
            if effect.spell.armor and effect.remaining_turns > 0:
                armor = effect.spell.armor
            new_effect = Scenario.apply_effect(new_scenario, effect)
            if new_effect:
                remaining_effects.append(new_effect)
        new_scenario.player = replace(new_scenario.player, armor=armor)
        return new_scenario

    def cast(self, spell):
        assert self.player.mana >= spell.cost
        return replace(
            self,
            player=replace(self.player, mana=self.player.mana - spell.cost),
            effects=[*self.effects, Effect(spell=spell, remaining_turns=spell.effect_duration)],
            spells=[*self.spells, spell],
            cost=self.cost + spell.cost,
        )

    def runnable_spells(self):
        spells = []
        for spell in SPELLS:
            if spell.cost <= self.player.mana and not any(
                effect.spell == spell and effect.remaining_turns > 0 for effect in self.effects
            ):
                spells.append(spell)
        return spells


def parse_input(input):
    values = {}
    for line in input:
        key, value = line.rstrip().split(": ")
        values[key] = int(value)
    return Character(hit_points=values["Hit Points"], damage=values["Damage"])


class Simulation:
    def __init__(self, hard=False, min_mana=1e9):
        self.min_mana = min_mana  # hypothesis to speed up computation
        self.best_scenario = None
        self.hard = hard

    def run(self, player, boss):
        scenarios = [Scenario(cost=0, player=player, boss=boss)]

        i = 1
        lost = defaultdict(int)
        won = 0
        while scenarios:
            print(f"turn {i} - {len(scenarios)} scenarios - {sum(lost.values())} lost - {won} won")
            i += 1
            # player turn
            remaining_scenarios = []
            for scenario in scenarios:
                scenario = scenario.apply_effects()
                if self.hard:
                    scenario.player = replace(
                        scenario.player, hit_points=scenario.player.hit_points - 1
                    )
                if scenario.player_is_dead:
                    lost["dead"] += 1
                    continue
                elif scenario.cost > self.min_mana:
                    lost["cost"] += 1
                    continue
                elif scenario.is_won and scenario.cost < self.min_mana:
                    won += 1
                    self.min_mana = scenario.cost
                    self.best_scenario = scenario
                    print(f"WIN: {scenario.summary()}")
                    continue

                runnable_spells = scenario.runnable_spells()
                if not runnable_spells:
                    lost["out_of_mana"] += 1
                    continue
                for spell in runnable_spells:
                    new_scenario = scenario.cast(spell)
                    if new_scenario.player_is_dead:
                        lost["dead"] += 1
                        continue
                    elif new_scenario.cost > self.min_mana:
                        lost["cost"] += 1
                        continue
                    elif new_scenario.is_won and new_scenario.cost < self.min_mana:
                        self.min_mana = new_scenario.cost
                        self.best_scenario = new_scenario
                    else:
                        remaining_scenarios.append(new_scenario)
            scenarios = remaining_scenarios

            # boss turn
            remaining_scenarios = []
            for scenario in scenarios:
                scenario = scenario.apply_effects()
                if scenario.player_is_dead:
                    lost["dead"] += 1
                    continue
                elif scenario.is_won and scenario.cost < self.min_mana:
                    won += 1
                    self.min_mana = scenario.cost
                    self.best_scenario = scenario
                    print(f"WIN: {scenario.summary()}")
                else:
                    remaining_scenarios.append(scenario)

                # boss attack
                scenario.player = replace(
                    scenario.player,
                    hit_points=scenario.player.hit_points
                    - max(1, scenario.boss.damage - scenario.player.armor),
                )
                scenarios = remaining_scenarios


def main1(input):
    boss = parse_input(input)
    player = Character(hit_points=50, damage=0, mana=500, armor=0)

    simulation = Simulation(min_mana=2000)
    simulation.run(player=player, boss=boss)
    return simulation.min_mana


def main2(input):
    boss = parse_input(input)
    player = Character(hit_points=50, damage=0, mana=500, armor=0)

    simulation = Simulation(min_mana=5000, hard=True)
    simulation.run(player=player, boss=boss)
    return simulation.min_mana


if __name__ == "__main__":
    input = sys.stdin
    main = main2 if "--two" in sys.argv else main1
    print(main(input), file=sys.stdout)
