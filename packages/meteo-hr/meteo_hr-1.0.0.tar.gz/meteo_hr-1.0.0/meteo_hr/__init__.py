from typing import NamedTuple, Union


class Place3D(NamedTuple):
    name: str
    slug: str
    region: str


class Place7D(NamedTuple):
    name: str
    code: str


Place = Union[Place3D, Place7D]
