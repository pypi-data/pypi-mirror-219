# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.prime.core.Color import Color


@dataclasses.dataclass()
class PrimeStruct6(BaseProperty):
    unnamed: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_1: Color = dataclasses.field(default_factory=Color)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unnamed = DamageVulnerability.from_stream(data, property_size)
        unknown_1 = Color.from_stream(data)
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>l', data.read(4))[0]
        return cls(unnamed, unknown_1, unknown_2, unknown_3)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        self.unnamed.to_stream(data)
        self.unknown_1.to_stream(data)
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>l', self.unknown_3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unnamed=DamageVulnerability.from_json(data['unnamed']),
            unknown_1=Color.from_json(data['unknown_1']),
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
        )

    def to_json(self) -> dict:
        return {
            'unnamed': self.unnamed.to_json(),
            'unknown_1': self.unknown_1.to_json(),
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
        }

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed, "unnamed", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PrimeStruct6.{field_name} ({field_type}): {e}"
                )
