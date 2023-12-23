from dataclasses import dataclass


@dataclass
class Skin:
    id: int
    description: str
    price: int
    sex: bool
    dl_id: int
