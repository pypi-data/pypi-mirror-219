# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.archetypes.PrimeStruct3 import PrimeStruct3


@dataclasses.dataclass()
class PrimeStruct2(BaseProperty):
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    prime_struct3_1: PrimeStruct3 = dataclasses.field(default_factory=PrimeStruct3)
    prime_struct3_2: PrimeStruct3 = dataclasses.field(default_factory=PrimeStruct3)
    prime_struct3_3: PrimeStruct3 = dataclasses.field(default_factory=PrimeStruct3)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        prime_struct3_1 = PrimeStruct3.from_stream(data, property_size)
        prime_struct3_2 = PrimeStruct3.from_stream(data, property_size)
        prime_struct3_3 = PrimeStruct3.from_stream(data, property_size)
        return cls(unknown_1, unknown_2, unknown_3, prime_struct3_1, prime_struct3_2, prime_struct3_3)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        self.prime_struct3_1.to_stream(data)
        self.prime_struct3_2.to_stream(data)
        self.prime_struct3_3.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            prime_struct3_1=PrimeStruct3.from_json(data['prime_struct3_1']),
            prime_struct3_2=PrimeStruct3.from_json(data['prime_struct3_2']),
            prime_struct3_3=PrimeStruct3.from_json(data['prime_struct3_3']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'prime_struct3_1': self.prime_struct3_1.to_json(),
            'prime_struct3_2': self.prime_struct3_2.to_json(),
            'prime_struct3_3': self.prime_struct3_3.to_json(),
        }

    def _dependencies_for_prime_struct3_1(self, asset_manager):
        yield from self.prime_struct3_1.dependencies_for(asset_manager)

    def _dependencies_for_prime_struct3_2(self, asset_manager):
        yield from self.prime_struct3_2.dependencies_for(asset_manager)

    def _dependencies_for_prime_struct3_3(self, asset_manager):
        yield from self.prime_struct3_3.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_prime_struct3_1, "prime_struct3_1", "PrimeStruct3"),
            (self._dependencies_for_prime_struct3_2, "prime_struct3_2", "PrimeStruct3"),
            (self._dependencies_for_prime_struct3_3, "prime_struct3_3", "PrimeStruct3"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PrimeStruct2.{field_name} ({field_type}): {e}"
                )
