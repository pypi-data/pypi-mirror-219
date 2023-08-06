from dataclasses import dataclass
from typing import Literal


@dataclass
class License:
    status: Literal['ACTIVE', 'DEACTIVATED']
