# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class CameraPitch(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    forwards_pitch: Spline = dataclasses.field(default_factory=Spline)
    backwards_pitch: Spline = dataclasses.field(default_factory=Spline)
    use_player_radius: bool = dataclasses.field(default=False)
    max_radius: float = dataclasses.field(default=20.0)
    ease_in: Spline = dataclasses.field(default_factory=Spline)
    ease_out: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CAMP'

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

        data.write(b'\x81\xd0\x93\xb3')  # 0x81d093b3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forwards_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xad\x9f\x8e>')  # 0xad9f8e3e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.backwards_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'9"\xd9\xdc')  # 0x3922d9dc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_player_radius))

        data.write(b'\xc5\x99\xbc\xbb')  # 0xc599bcbb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_radius))

        data.write(b'\xdfUP\xcc')  # 0xdf5550cc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ease_in.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcaX\x134')  # 0xca581334
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ease_out.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            forwards_pitch=Spline.from_json(data['forwards_pitch']),
            backwards_pitch=Spline.from_json(data['backwards_pitch']),
            use_player_radius=data['use_player_radius'],
            max_radius=data['max_radius'],
            ease_in=Spline.from_json(data['ease_in']),
            ease_out=Spline.from_json(data['ease_out']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'forwards_pitch': self.forwards_pitch.to_json(),
            'backwards_pitch': self.backwards_pitch.to_json(),
            'use_player_radius': self.use_player_radius,
            'max_radius': self.max_radius,
            'ease_in': self.ease_in.to_json(),
            'ease_out': self.ease_out.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_forwards_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_backwards_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_use_player_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ease_in(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_ease_out(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x81d093b3: ('forwards_pitch', _decode_forwards_pitch),
    0xad9f8e3e: ('backwards_pitch', _decode_backwards_pitch),
    0x3922d9dc: ('use_player_radius', _decode_use_player_radius),
    0xc599bcbb: ('max_radius', _decode_max_radius),
    0xdf5550cc: ('ease_in', _decode_ease_in),
    0xca581334: ('ease_out', _decode_ease_out),
}
