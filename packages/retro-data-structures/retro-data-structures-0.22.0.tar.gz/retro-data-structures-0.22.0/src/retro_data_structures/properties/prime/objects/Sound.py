# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Sound(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    sound_id: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: int = dataclasses.field(default=0)
    unknown_6: int = dataclasses.field(default=0)
    unknown_7: int = dataclasses.field(default=0)
    unknown_8: int = dataclasses.field(default=0)
    unknown_9: bool = dataclasses.field(default=False)
    unknown_10: bool = dataclasses.field(default=False)
    unknown_11: bool = dataclasses.field(default=False)
    unknown_12: bool = dataclasses.field(default=False)
    unknown_13: bool = dataclasses.field(default=False)
    unknown_14: bool = dataclasses.field(default=False)
    unknown_15: bool = dataclasses.field(default=False)
    unknown_16: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x9

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        sound_id = struct.unpack('>l', data.read(4))[0]
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>l', data.read(4))[0]
        unknown_6 = struct.unpack('>l', data.read(4))[0]
        unknown_7 = struct.unpack('>l', data.read(4))[0]
        unknown_8 = struct.unpack('>l', data.read(4))[0]
        unknown_9 = struct.unpack('>?', data.read(1))[0]
        unknown_10 = struct.unpack('>?', data.read(1))[0]
        unknown_11 = struct.unpack('>?', data.read(1))[0]
        unknown_12 = struct.unpack('>?', data.read(1))[0]
        unknown_13 = struct.unpack('>?', data.read(1))[0]
        unknown_14 = struct.unpack('>?', data.read(1))[0]
        unknown_15 = struct.unpack('>?', data.read(1))[0]
        unknown_16 = struct.unpack('>l', data.read(4))[0]
        return cls(name, position, rotation, sound_id, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13, unknown_14, unknown_15, unknown_16)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x14')  # 20 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack('>l', self.sound_id))
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>l', self.unknown_5))
        data.write(struct.pack('>l', self.unknown_6))
        data.write(struct.pack('>l', self.unknown_7))
        data.write(struct.pack('>l', self.unknown_8))
        data.write(struct.pack('>?', self.unknown_9))
        data.write(struct.pack('>?', self.unknown_10))
        data.write(struct.pack('>?', self.unknown_11))
        data.write(struct.pack('>?', self.unknown_12))
        data.write(struct.pack('>?', self.unknown_13))
        data.write(struct.pack('>?', self.unknown_14))
        data.write(struct.pack('>?', self.unknown_15))
        data.write(struct.pack('>l', self.unknown_16))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            sound_id=data['sound_id'],
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=data['unknown_12'],
            unknown_13=data['unknown_13'],
            unknown_14=data['unknown_14'],
            unknown_15=data['unknown_15'],
            unknown_16=data['unknown_16'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'sound_id': self.sound_id,
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
            'unknown_14': self.unknown_14,
            'unknown_15': self.unknown_15,
            'unknown_16': self.unknown_16,
        }

    def _dependencies_for_sound_id(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_sound_id, "sound_id", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Sound.{field_name} ({field_type}): {e}"
                )
