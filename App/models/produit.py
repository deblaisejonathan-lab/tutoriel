from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Produit:
    titre: str
    prix: Optional[str]=None
    note: Optional[str] = None
    image: Optional[str]=None
def conv_dict(self)-> dict:
    return asdict(self)