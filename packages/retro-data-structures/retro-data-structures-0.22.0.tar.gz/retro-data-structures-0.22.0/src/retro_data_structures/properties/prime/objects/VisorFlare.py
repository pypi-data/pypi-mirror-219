# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.FlareDef import FlareDef
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class VisorFlare(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: bool = dataclasses.field(default=False)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: int = dataclasses.field(default=0)
    flare_def_1: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare_def_2: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare_def_3: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare_def_4: FlareDef = dataclasses.field(default_factory=FlareDef)
    flare_def_5: FlareDef = dataclasses.field(default_factory=FlareDef)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x51

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>?', data.read(1))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>l', data.read(4))[0]
        flare_def_1 = FlareDef.from_stream(data, property_size)
        flare_def_2 = FlareDef.from_stream(data, property_size)
        flare_def_3 = FlareDef.from_stream(data, property_size)
        flare_def_4 = FlareDef.from_stream(data, property_size)
        flare_def_5 = FlareDef.from_stream(data, property_size)
        return cls(name, position, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, flare_def_1, flare_def_2, flare_def_3, flare_def_4, flare_def_5)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0e')  # 14 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>?', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>l', self.unknown_7))
        self.flare_def_1.to_stream(data)
        self.flare_def_2.to_stream(data)
        self.flare_def_3.to_stream(data)
        self.flare_def_4.to_stream(data)
        self.flare_def_5.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            flare_def_1=FlareDef.from_json(data['flare_def_1']),
            flare_def_2=FlareDef.from_json(data['flare_def_2']),
            flare_def_3=FlareDef.from_json(data['flare_def_3']),
            flare_def_4=FlareDef.from_json(data['flare_def_4']),
            flare_def_5=FlareDef.from_json(data['flare_def_5']),
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'flare_def_1': self.flare_def_1.to_json(),
            'flare_def_2': self.flare_def_2.to_json(),
            'flare_def_3': self.flare_def_3.to_json(),
            'flare_def_4': self.flare_def_4.to_json(),
            'flare_def_5': self.flare_def_5.to_json(),
        }

    def _dependencies_for_flare_def_1(self, asset_manager):
        yield from self.flare_def_1.dependencies_for(asset_manager)

    def _dependencies_for_flare_def_2(self, asset_manager):
        yield from self.flare_def_2.dependencies_for(asset_manager)

    def _dependencies_for_flare_def_3(self, asset_manager):
        yield from self.flare_def_3.dependencies_for(asset_manager)

    def _dependencies_for_flare_def_4(self, asset_manager):
        yield from self.flare_def_4.dependencies_for(asset_manager)

    def _dependencies_for_flare_def_5(self, asset_manager):
        yield from self.flare_def_5.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_flare_def_1, "flare_def_1", "FlareDef"),
            (self._dependencies_for_flare_def_2, "flare_def_2", "FlareDef"),
            (self._dependencies_for_flare_def_3, "flare_def_3", "FlareDef"),
            (self._dependencies_for_flare_def_4, "flare_def_4", "FlareDef"),
            (self._dependencies_for_flare_def_5, "flare_def_5", "FlareDef"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for VisorFlare.{field_name} ({field_type}): {e}"
                )
