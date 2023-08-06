# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class AIWaypoint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    speed: float = dataclasses.field(default=1.0)
    pause: float = dataclasses.field(default=0.0)
    unknown_0xc6705a00: int = dataclasses.field(default=0)
    locator_index: int = dataclasses.field(default=0)
    unknown_0x166979d4: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'AIWP'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'\x80\xf7\xe6\x05')  # 0x80f7e605
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pause))

        data.write(b'\xc6pZ\x00')  # 0xc6705a00
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc6705a00))

        data.write(b'\xa7\x90\xc6\xa9')  # 0xa790c6a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.locator_index))

        data.write(b'\x16iy\xd4')  # 0x166979d4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x166979d4))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            speed=data['speed'],
            pause=data['pause'],
            unknown_0xc6705a00=data['unknown_0xc6705a00'],
            locator_index=data['locator_index'],
            unknown_0x166979d4=data['unknown_0x166979d4'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'speed': self.speed,
            'pause': self.pause,
            'unknown_0xc6705a00': self.unknown_0xc6705a00,
            'locator_index': self.locator_index,
            'unknown_0x166979d4': self.unknown_0x166979d4,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pause(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc6705a00(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_locator_index(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x166979d4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x6392404e: ('speed', _decode_speed),
    0x80f7e605: ('pause', _decode_pause),
    0xc6705a00: ('unknown_0xc6705a00', _decode_unknown_0xc6705a00),
    0xa790c6a9: ('locator_index', _decode_locator_index),
    0x166979d4: ('unknown_0x166979d4', _decode_unknown_0x166979d4),
}
