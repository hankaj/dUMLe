from dataclasses import dataclass
from typing import List


@dataclass
class ErrorMessage:
    errors: List[str]
