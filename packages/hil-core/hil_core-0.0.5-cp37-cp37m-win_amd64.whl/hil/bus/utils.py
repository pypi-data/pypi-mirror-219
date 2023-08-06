import can
import yaml


def load_bus(fn: str) -> can.interface.Bus:
    with open(fn, "r", encoding="utf-8") as f:
        o = yaml.safe_load(f)
        return can.Bus(**o)
