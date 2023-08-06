# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Color import Color
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class VisorGoo(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    elsc: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: Color = dataclasses.field(default_factory=Color)
    sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_7: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x53

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        particle = struct.unpack(">L", data.read(4))[0]
        elsc = struct.unpack(">L", data.read(4))[0]
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = Color.from_stream(data)
        sound = struct.unpack('>l', data.read(4))[0]
        unknown_7 = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, particle, elsc, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, sound, unknown_7)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0b')  # 11 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        data.write(struct.pack(">L", self.particle))
        data.write(struct.pack(">L", self.elsc))
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        self.unknown_5.to_stream(data)
        data.write(struct.pack('>l', self.sound))
        data.write(struct.pack('>?', self.unknown_7))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            particle=data['particle'],
            elsc=data['elsc'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=Color.from_json(data['unknown_5']),
            sound=data['sound'],
            unknown_7=data['unknown_7'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'particle': self.particle,
            'elsc': self.elsc,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5.to_json(),
            'sound': self.sound,
            'unknown_7': self.unknown_7,
        }

    def _dependencies_for_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle)

    def _dependencies_for_elsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.elsc)

    def _dependencies_for_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_particle, "particle", "AssetId"),
            (self._dependencies_for_elsc, "elsc", "AssetId"),
            (self._dependencies_for_sound, "sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for VisorGoo.{field_name} ({field_type}): {e}"
                )
