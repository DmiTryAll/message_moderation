from dataclasses import dataclass
from pathlib import Path

from domain.utils.progress_counter_storage import ProgressCounterStorage


@dataclass
class ProgressCounterFileStorage(ProgressCounterStorage):
    path: Path

    async def get(self) -> int:
        try:
            result = self.path.read_text()
        except FileNotFoundError:
            result = 0
        return int(result)

    async def set(self, value: int) -> None:
        with open(self.path, "w") as f:
            f.write(str(value))