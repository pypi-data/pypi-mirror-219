from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING
if TYPE_CHECKING:
    from .keyboard_event import KeyboardEvent
    from .mouse_event import MouseEvent


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    trigger_condition: Callable[[KeyboardEvent | MouseEvent], bool] | None = None

    def __post_init__(self) -> None:
        if self.trigger_condition is None:
            object.__setattr__(self, "trigger_condition", lambda event: event.name == self.name)
