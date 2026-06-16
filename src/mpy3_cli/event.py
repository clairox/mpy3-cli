from collections.abc import Callable
from typing import Any, Literal


class Event:
    def __init__(self, value: Any) -> None:
        self.value = value


class PlayerTimeChangedEvent(Event):
    def __init__(self, value: int) -> None:
        super().__init__(value)


EventName = Literal["player_time_changed"]


EventCallback = Callable[[Event], None]
Listener = dict[str, list[EventCallback]]


class EventManager:
    def __init__(self) -> None:
        self.listeners: Listener = {}

    def attach(self, name: EventName, callback: EventCallback) -> None:
        if name in self.listeners:
            self.listeners[name].append(callback)
        else:
            self.listeners.setdefault(name, [callback])

    def detach(self, name: EventName, callback: EventCallback) -> None:
        if name in self.listeners:
            self.listeners[name].remove(callback)

    def dispatch(self, name: EventName, value: Any) -> None:
        if name in self.listeners:
            for callback in self.listeners[name]:
                event = None
                if name == "player_time_changed":
                    event = PlayerTimeChangedEvent(value)
                else:
                    event = Event(value)

                callback(event)


event_manager = EventManager()
