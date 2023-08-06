# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class RSPL(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    splash_scale: float = dataclasses.field(default=1.0)
    max_splashes: int = dataclasses.field(default=20)
    generation_rate: int = dataclasses.field(default=2)
    start_height: float = dataclasses.field(default=1.0)
    alpha_factor: float = dataclasses.field(default=0.125)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'RSPL'

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

        data.write(b'\x08#\x1a\xc9')  # 0x8231ac9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.splash_scale))

        data.write(b'bH\xaa\x06')  # 0x6248aa06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_splashes))

        data.write(b'\x7fZ\x86\xdd')  # 0x7f5a86dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.generation_rate))

        data.write(b"\xc4\x05'\xf6")  # 0xc40527f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_height))

        data.write(b'\xe0N\x02p')  # 0xe04e0270
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.alpha_factor))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            splash_scale=data['splash_scale'],
            max_splashes=data['max_splashes'],
            generation_rate=data['generation_rate'],
            start_height=data['start_height'],
            alpha_factor=data['alpha_factor'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'splash_scale': self.splash_scale,
            'max_splashes': self.max_splashes,
            'generation_rate': self.generation_rate,
            'start_height': self.start_height,
            'alpha_factor': self.alpha_factor,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_splash_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_splashes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_generation_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_start_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alpha_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x8231ac9: ('splash_scale', _decode_splash_scale),
    0x6248aa06: ('max_splashes', _decode_max_splashes),
    0x7f5a86dd: ('generation_rate', _decode_generation_rate),
    0xc40527f6: ('start_height', _decode_start_height),
    0xe04e0270: ('alpha_factor', _decode_alpha_factor),
}
