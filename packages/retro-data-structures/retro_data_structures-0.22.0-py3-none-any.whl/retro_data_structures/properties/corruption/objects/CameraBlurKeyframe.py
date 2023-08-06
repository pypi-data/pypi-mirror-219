# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class CameraBlurKeyframe(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    blur_type: int = dataclasses.field(default=0)
    blur_radius: float = dataclasses.field(default=0.0)
    which_filter_group: int = dataclasses.field(default=0)
    interpolate_in_time: float = dataclasses.field(default=0.0)
    interpolate_out_time: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'BLUR'

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

        data.write(b'\xe95\x91H')  # 0xe9359148
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.blur_type))

        data.write(b'on\xb1\xf4')  # 0x6f6eb1f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.blur_radius))

        data.write(b'?\xdcK.')  # 0x3fdc4b2e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.which_filter_group))

        data.write(b'\xab\xd4\x1a6')  # 0xabd41a36
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.interpolate_in_time))

        data.write(b'>\xafx\xfe')  # 0x3eaf78fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.interpolate_out_time))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            blur_type=data['blur_type'],
            blur_radius=data['blur_radius'],
            which_filter_group=data['which_filter_group'],
            interpolate_in_time=data['interpolate_in_time'],
            interpolate_out_time=data['interpolate_out_time'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'blur_type': self.blur_type,
            'blur_radius': self.blur_radius,
            'which_filter_group': self.which_filter_group,
            'interpolate_in_time': self.interpolate_in_time,
            'interpolate_out_time': self.interpolate_out_time,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_blur_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_blur_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_which_filter_group(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_interpolate_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_interpolate_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xe9359148: ('blur_type', _decode_blur_type),
    0x6f6eb1f4: ('blur_radius', _decode_blur_radius),
    0x3fdc4b2e: ('which_filter_group', _decode_which_filter_group),
    0xabd41a36: ('interpolate_in_time', _decode_interpolate_in_time),
    0x3eaf78fe: ('interpolate_out_time', _decode_interpolate_out_time),
}
