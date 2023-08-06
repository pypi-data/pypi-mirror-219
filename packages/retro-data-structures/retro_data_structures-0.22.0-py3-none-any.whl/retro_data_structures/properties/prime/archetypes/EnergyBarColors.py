# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.core.Color import Color


@dataclasses.dataclass()
class EnergyBarColors(BaseProperty):
    energy_bar_filled: Color = dataclasses.field(default_factory=Color)
    energy_bar_empty: Color = dataclasses.field(default_factory=Color)
    energy_bar_shadow: Color = dataclasses.field(default_factory=Color)
    energy_tank_filled: Color = dataclasses.field(default_factory=Color)
    energy_tank_empty: Color = dataclasses.field(default_factory=Color)
    energy_digits_font: Color = dataclasses.field(default_factory=Color)
    energy_digits_outline: Color = dataclasses.field(default_factory=Color)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        energy_bar_filled = Color.from_stream(data)
        energy_bar_empty = Color.from_stream(data)
        energy_bar_shadow = Color.from_stream(data)
        energy_tank_filled = Color.from_stream(data)
        energy_tank_empty = Color.from_stream(data)
        energy_digits_font = Color.from_stream(data)
        energy_digits_outline = Color.from_stream(data)
        return cls(energy_bar_filled, energy_bar_empty, energy_bar_shadow, energy_tank_filled, energy_tank_empty, energy_digits_font, energy_digits_outline)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        self.energy_bar_filled.to_stream(data)
        self.energy_bar_empty.to_stream(data)
        self.energy_bar_shadow.to_stream(data)
        self.energy_tank_filled.to_stream(data)
        self.energy_tank_empty.to_stream(data)
        self.energy_digits_font.to_stream(data)
        self.energy_digits_outline.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            energy_bar_filled=Color.from_json(data['energy_bar_filled']),
            energy_bar_empty=Color.from_json(data['energy_bar_empty']),
            energy_bar_shadow=Color.from_json(data['energy_bar_shadow']),
            energy_tank_filled=Color.from_json(data['energy_tank_filled']),
            energy_tank_empty=Color.from_json(data['energy_tank_empty']),
            energy_digits_font=Color.from_json(data['energy_digits_font']),
            energy_digits_outline=Color.from_json(data['energy_digits_outline']),
        )

    def to_json(self) -> dict:
        return {
            'energy_bar_filled': self.energy_bar_filled.to_json(),
            'energy_bar_empty': self.energy_bar_empty.to_json(),
            'energy_bar_shadow': self.energy_bar_shadow.to_json(),
            'energy_tank_filled': self.energy_tank_filled.to_json(),
            'energy_tank_empty': self.energy_tank_empty.to_json(),
            'energy_digits_font': self.energy_digits_font.to_json(),
            'energy_digits_outline': self.energy_digits_outline.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []
