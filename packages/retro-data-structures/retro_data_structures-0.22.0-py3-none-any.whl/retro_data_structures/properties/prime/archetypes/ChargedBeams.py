# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime as enums


@dataclasses.dataclass()
class ChargedBeams(BaseProperty):
    power: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)
    ice: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)
    wave: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)
    plasma: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)
    phazon: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        power = enums.VulnerabilityType.from_stream(data)
        ice = enums.VulnerabilityType.from_stream(data)
        wave = enums.VulnerabilityType.from_stream(data)
        plasma = enums.VulnerabilityType.from_stream(data)
        phazon = enums.VulnerabilityType.from_stream(data)
        return cls(power, ice, wave, plasma, phazon)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        self.power.to_stream(data)
        self.ice.to_stream(data)
        self.wave.to_stream(data)
        self.plasma.to_stream(data)
        self.phazon.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            power=enums.VulnerabilityType.from_json(data['power']),
            ice=enums.VulnerabilityType.from_json(data['ice']),
            wave=enums.VulnerabilityType.from_json(data['wave']),
            plasma=enums.VulnerabilityType.from_json(data['plasma']),
            phazon=enums.VulnerabilityType.from_json(data['phazon']),
        )

    def to_json(self) -> dict:
        return {
            'power': self.power.to_json(),
            'ice': self.ice.to_json(),
            'wave': self.wave.to_json(),
            'plasma': self.plasma.to_json(),
            'phazon': self.phazon.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []
