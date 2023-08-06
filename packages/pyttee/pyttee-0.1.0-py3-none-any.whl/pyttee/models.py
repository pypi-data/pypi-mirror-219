
from dataclasses import dataclass


@dataclass
class Tag:
    props: dict[str, str]
    children: list
    name: str

    @classmethod
    def default_factory(cls):
        return cls(props={}, children=[], name="")
