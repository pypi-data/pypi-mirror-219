import logging
from dataclasses import dataclass


@dataclass(frozen=True)
class DialPinout:
    counter_pin: int = 19
    dial_pin: int = 26
    handset_pin: int = 13


@dataclass(frozen=True)
class DialConfiguration:
    loglevel: int = logging.WARNING
    counter_debounce: int = 80
    dial_debounce: int = 100
    handset_debounce: int = 200

