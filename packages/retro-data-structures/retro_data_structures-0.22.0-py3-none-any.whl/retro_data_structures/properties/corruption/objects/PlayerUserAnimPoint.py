# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class PlayerUserAnimPoint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    attach_dist: float = dataclasses.field(default=0.75)
    unknown_0xad2d4f53: float = dataclasses.field(default=1.0)
    unknown_0x285b4540: float = dataclasses.field(default=0.0)
    unknown_0x6806d0b3: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x1ce620a7: int = dataclasses.field(default=5)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PUAP'

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"d='i")  # 0x643d2769
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attach_dist))

        data.write(b'\xad-OS')  # 0xad2d4f53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xad2d4f53))

        data.write(b'([E@')  # 0x285b4540
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x285b4540))

        data.write(b'h\x06\xd0\xb3')  # 0x6806d0b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6806d0b3))

        data.write(b'\x1c\xe6 \xa7')  # 0x1ce620a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x1ce620a7))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            animation=AnimationParameters.from_json(data['animation']),
            attach_dist=data['attach_dist'],
            unknown_0xad2d4f53=data['unknown_0xad2d4f53'],
            unknown_0x285b4540=data['unknown_0x285b4540'],
            unknown_0x6806d0b3=data['unknown_0x6806d0b3'],
            unknown_0x1ce620a7=data['unknown_0x1ce620a7'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'animation': self.animation.to_json(),
            'attach_dist': self.attach_dist,
            'unknown_0xad2d4f53': self.unknown_0xad2d4f53,
            'unknown_0x285b4540': self.unknown_0x285b4540,
            'unknown_0x6806d0b3': self.unknown_0x6806d0b3,
            'unknown_0x1ce620a7': self.unknown_0x1ce620a7,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_attach_dist(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xad2d4f53(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x285b4540(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6806d0b3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1ce620a7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xa3d63f44: ('animation', _decode_animation),
    0x643d2769: ('attach_dist', _decode_attach_dist),
    0xad2d4f53: ('unknown_0xad2d4f53', _decode_unknown_0xad2d4f53),
    0x285b4540: ('unknown_0x285b4540', _decode_unknown_0x285b4540),
    0x6806d0b3: ('unknown_0x6806d0b3', _decode_unknown_0x6806d0b3),
    0x1ce620a7: ('unknown_0x1ce620a7', _decode_unknown_0x1ce620a7),
}
