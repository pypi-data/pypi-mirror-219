# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.prime.archetypes.MassivePrimeStruct import MassivePrimeStruct
from retro_data_structures.properties.prime.archetypes.PrimeStruct1 import PrimeStruct1
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class MetroidPrimeStage1(BaseObjectType):
    unknown_1: int = dataclasses.field(default=0)
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unknown_2: bool = dataclasses.field(default=False)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: int = dataclasses.field(default=0)
    unknown_7: bool = dataclasses.field(default=False)
    unknown_8: int = dataclasses.field(default=0)
    health_info_1: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    health_info_2: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    unknown_9: int = dataclasses.field(default=0)
    prime_struct1_1: PrimeStruct1 = dataclasses.field(default_factory=PrimeStruct1)
    prime_struct1_2: PrimeStruct1 = dataclasses.field(default_factory=PrimeStruct1)
    prime_struct1_3: PrimeStruct1 = dataclasses.field(default_factory=PrimeStruct1)
    prime_struct1_4: PrimeStruct1 = dataclasses.field(default_factory=PrimeStruct1)
    unknown_10: int = dataclasses.field(default=0)
    unknown_11: int = dataclasses.field(default=0)
    unnamed: MassivePrimeStruct = dataclasses.field(default_factory=MassivePrimeStruct)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x84

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        unknown_1 = struct.unpack('>l', data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unknown_2 = struct.unpack('>?', data.read(1))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>l', data.read(4))[0]
        unknown_7 = struct.unpack('>?', data.read(1))[0]
        unknown_8 = struct.unpack('>l', data.read(4))[0]
        health_info_1 = HealthInfo.from_stream(data, property_size)
        health_info_2 = HealthInfo.from_stream(data, property_size)
        unknown_9 = struct.unpack('>l', data.read(4))[0]
        prime_struct1_1 = PrimeStruct1.from_stream(data, property_size)
        prime_struct1_2 = PrimeStruct1.from_stream(data, property_size)
        prime_struct1_3 = PrimeStruct1.from_stream(data, property_size)
        prime_struct1_4 = PrimeStruct1.from_stream(data, property_size)
        unknown_10 = struct.unpack('>l', data.read(4))[0]
        unknown_11 = struct.unpack('>l', data.read(4))[0]
        unnamed = MassivePrimeStruct.from_stream(data, property_size)
        return cls(unknown_1, name, position, rotation, scale, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, health_info_1, health_info_2, unknown_9, prime_struct1_1, prime_struct1_2, prime_struct1_3, prime_struct1_4, unknown_10, unknown_11, unnamed)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x16')  # 22 properties
        data.write(struct.pack('>l', self.unknown_1))
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        data.write(struct.pack('>?', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>l', self.unknown_6))
        data.write(struct.pack('>?', self.unknown_7))
        data.write(struct.pack('>l', self.unknown_8))
        self.health_info_1.to_stream(data)
        self.health_info_2.to_stream(data)
        data.write(struct.pack('>l', self.unknown_9))
        self.prime_struct1_1.to_stream(data)
        self.prime_struct1_2.to_stream(data)
        self.prime_struct1_3.to_stream(data)
        self.prime_struct1_4.to_stream(data)
        data.write(struct.pack('>l', self.unknown_10))
        data.write(struct.pack('>l', self.unknown_11))
        self.unnamed.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            health_info_1=HealthInfo.from_json(data['health_info_1']),
            health_info_2=HealthInfo.from_json(data['health_info_2']),
            unknown_9=data['unknown_9'],
            prime_struct1_1=PrimeStruct1.from_json(data['prime_struct1_1']),
            prime_struct1_2=PrimeStruct1.from_json(data['prime_struct1_2']),
            prime_struct1_3=PrimeStruct1.from_json(data['prime_struct1_3']),
            prime_struct1_4=PrimeStruct1.from_json(data['prime_struct1_4']),
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unnamed=MassivePrimeStruct.from_json(data['unnamed']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'health_info_1': self.health_info_1.to_json(),
            'health_info_2': self.health_info_2.to_json(),
            'unknown_9': self.unknown_9,
            'prime_struct1_1': self.prime_struct1_1.to_json(),
            'prime_struct1_2': self.prime_struct1_2.to_json(),
            'prime_struct1_3': self.prime_struct1_3.to_json(),
            'prime_struct1_4': self.prime_struct1_4.to_json(),
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unnamed': self.unnamed.to_json(),
        }

    def _dependencies_for_health_info_1(self, asset_manager):
        yield from self.health_info_1.dependencies_for(asset_manager)

    def _dependencies_for_health_info_2(self, asset_manager):
        yield from self.health_info_2.dependencies_for(asset_manager)

    def _dependencies_for_prime_struct1_1(self, asset_manager):
        yield from self.prime_struct1_1.dependencies_for(asset_manager)

    def _dependencies_for_prime_struct1_2(self, asset_manager):
        yield from self.prime_struct1_2.dependencies_for(asset_manager)

    def _dependencies_for_prime_struct1_3(self, asset_manager):
        yield from self.prime_struct1_3.dependencies_for(asset_manager)

    def _dependencies_for_prime_struct1_4(self, asset_manager):
        yield from self.prime_struct1_4.dependencies_for(asset_manager)

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_health_info_1, "health_info_1", "HealthInfo"),
            (self._dependencies_for_health_info_2, "health_info_2", "HealthInfo"),
            (self._dependencies_for_prime_struct1_1, "prime_struct1_1", "PrimeStruct1"),
            (self._dependencies_for_prime_struct1_2, "prime_struct1_2", "PrimeStruct1"),
            (self._dependencies_for_prime_struct1_3, "prime_struct1_3", "PrimeStruct1"),
            (self._dependencies_for_prime_struct1_4, "prime_struct1_4", "PrimeStruct1"),
            (self._dependencies_for_unnamed, "unnamed", "MassivePrimeStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for MetroidPrimeStage1.{field_name} ({field_type}): {e}"
                )
