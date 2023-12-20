import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cached_property
from math import lcm
from pathlib import Path


@dataclass
class SignalCount:
    low: int = 0
    high: int = 0


DEBUG = False


class ModuleRegistry:
    def __init__(self):
        self.registry = {}
        self.signal_queue = deque()
        self.signal_count = SignalCount()

    def register(self, key: str, module: "Module"):
        module.registry = self
        self.registry[key] = module

    def sync_senders(self):
        for module in list(self.registry.values()):
            for receiver in module.receivers:
                try:
                    self.registry[receiver].senders.add(module.key)
                except KeyError:
                    self.register(
                        receiver,
                        NullModule(key=receiver, receivers=[], senders={module.key}),
                    )

    def queue_signal(self, sender: str, dest: str, signal: bool):
        if signal:
            self.signal_count.high += 1
        else:
            self.signal_count.low += 1
        self.signal_queue.append((sender, dest, signal))

    def send_signal(self):
        sender, dest, signal = self.signal_queue.popleft()
        if DEBUG:
            print(f"{sender} -{'high' if signal else 'low'}-> {dest}")
        self.registry[dest].signal(signal, sender=sender)

    @property
    def id(self):
        return "".join(module.id for module in self.registry.values())


@dataclass
class Module:
    key: str
    receivers: list[str]
    senders: set[str] = field(default_factory=set)
    registry: ModuleRegistry = None

    def send(self, signal: bool):
        for receiver in self.receivers:
            self.registry.queue_signal(self.key, receiver, signal)

    def reset(self):
        pass

    @property
    def id(self):
        return "0"


@dataclass
class FlipFlopModule(Module):
    state: bool = False  # on or off

    def signal(self, high: bool, sender: str) -> None:
        if not high:
            self.state = not self.state
            self.send(self.state)

    def reset(self):
        self.state = False

    @property
    def id(self):
        return "1" if self.state else "0"


@dataclass
class ConjunctionModule(Module):
    state: dict = field(default_factory=lambda: defaultdict(bool))  # on or off
    on_count = 0

    @cached_property
    def senders_count(self):
        return len(self.senders)

    def signal(self, high: bool, sender: str) -> None:
        value = self.state[sender]
        if value and not high:
            self.on_count -= 1
        if not value and high:
            self.on_count += 1
        self.state[sender] = high

        self.send(not self.complete)

    @property
    def complete(self):
        return self.on_count == self.senders_count

    def reset(self):
        self.state = defaultdict(bool)


@dataclass
class BroadcasterModule(Module):
    def signal(self, high: bool, sender: str) -> None:
        self.send(high)


@dataclass
class NullModule(Module):
    def signal(self, high: bool, sender: str) -> None:
        pass


def parse_input(path: str):
    p = Path(path)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    module_registry = ModuleRegistry()
    module_registry.register("button", Module("button", ["broadcaster"]))
    for raw_module in content.split("\n"):
        from_, raw_receivers = raw_module.split(" -> ")
        receivers = raw_receivers.split(", ")
        match from_[0]:
            case "b":
                module_registry.register(
                    "broadcaster",
                    BroadcasterModule(key="broadcaster", receivers=receivers),
                )
            case "%":
                module_registry.register(
                    from_[1:], FlipFlopModule(from_[1:], receivers=receivers)
                )
            case "&":
                module_registry.register(
                    from_[1:], ConjunctionModule(from_[1:], receivers=receivers)
                )
    module_registry.sync_senders()

    return module_registry


def tick(module_registry: ModuleRegistry):
    module_registry.queue_signal("button", "broadcaster", False)
    while module_registry.signal_queue:
        module_registry.send_signal()


def main1(module_registry: ModuleRegistry):
    for _ in range(1000):
        tick(module_registry)

    print("module_registry.signal_count", module_registry.signal_count)
    return module_registry.signal_count.high * module_registry.signal_count.low


def main2(module_registry):
    cases = module_registry.registry["broadcaster"].receivers

    cycles = []
    for j, case in enumerate(cases):
        for module in module_registry.registry.values():
            module.reset()
        module_registry.registry["broadcaster"].receivers = [case]

        i = 1
        known_states = {module_registry.id: 0}
        tick(module_registry)
        while True:
            if (start := known_states.get(state := module_registry.id)) is not None:
                cycles.append((i - start, start))
                break
            else:
                known_states[state] = i
            tick(module_registry)
            i += 1

        print(f"cycle for module {case} is {i} with {start=}")
    assert all(start == 0 for _, start in cycles)
    return cycles[0][1] + lcm(*(cycle for cycle, _ in cycles))


if __name__ == "__main__":
    input_filepath = sys.argv[1]
    second_part = len(sys.argv) > 2 and sys.argv[2] == "--two"
    input_ = parse_input(input_filepath)
    if second_part:
        print(f"result: {main2(input_)}", file=sys.stdout)
    else:
        print(f"result: {main1(input_)}", file=sys.stdout)
