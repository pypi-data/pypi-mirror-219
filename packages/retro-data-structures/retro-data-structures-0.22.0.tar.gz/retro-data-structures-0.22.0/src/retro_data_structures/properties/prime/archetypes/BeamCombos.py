# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime as enums


@dataclasses.dataclass()
class BeamCombos(BaseProperty):
    super_missile: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)
    ice_spreader: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)
    wavebuster: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)
    flamethrower: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)
    phazon_combo: enums.VulnerabilityType = dataclasses.field(default=enums.VulnerabilityType.DoubleDamage)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        super_missile = enums.VulnerabilityType.from_stream(data)
        ice_spreader = enums.VulnerabilityType.from_stream(data)
        wavebuster = enums.VulnerabilityType.from_stream(data)
        flamethrower = enums.VulnerabilityType.from_stream(data)
        phazon_combo = enums.VulnerabilityType.from_stream(data)
        return cls(super_missile, ice_spreader, wavebuster, flamethrower, phazon_combo)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        self.super_missile.to_stream(data)
        self.ice_spreader.to_stream(data)
        self.wavebuster.to_stream(data)
        self.flamethrower.to_stream(data)
        self.phazon_combo.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            super_missile=enums.VulnerabilityType.from_json(data['super_missile']),
            ice_spreader=enums.VulnerabilityType.from_json(data['ice_spreader']),
            wavebuster=enums.VulnerabilityType.from_json(data['wavebuster']),
            flamethrower=enums.VulnerabilityType.from_json(data['flamethrower']),
            phazon_combo=enums.VulnerabilityType.from_json(data['phazon_combo']),
        )

    def to_json(self) -> dict:
        return {
            'super_missile': self.super_missile.to_json(),
            'ice_spreader': self.ice_spreader.to_json(),
            'wavebuster': self.wavebuster.to_json(),
            'flamethrower': self.flamethrower.to_json(),
            'phazon_combo': self.phazon_combo.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []
