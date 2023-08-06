# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class PathControl(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    path_flags: int = dataclasses.field(default=0)  # Flagset
    path_curve_type: enums.PathCurveType = dataclasses.field(default=enums.PathCurveType.Unknown1)
    radius_control: Spline = dataclasses.field(default_factory=Spline)
    height_control: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PCTL'

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xb9\x7f\x9f')  # 0xb0b97f9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.path_flags))

        data.write(b'\xf2_\xfd\xff')  # 0xf25ffdff
        data.write(b'\x00\x04')  # size
        self.path_curve_type.to_stream(data)

        data.write(b'\xf8\xaf\x85\x8c')  # 0xf8af858c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.radius_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'r\xcd`\xce')  # 0x72cd60ce
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.height_control.to_stream(data)
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
            path_flags=data['path_flags'],
            path_curve_type=enums.PathCurveType.from_json(data['path_curve_type']),
            radius_control=Spline.from_json(data['radius_control']),
            height_control=Spline.from_json(data['height_control']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'path_flags': self.path_flags,
            'path_curve_type': self.path_curve_type.to_json(),
            'radius_control': self.radius_control.to_json(),
            'height_control': self.height_control.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_path_flags(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_path_curve_type(data: typing.BinaryIO, property_size: int):
    return enums.PathCurveType.from_stream(data)


def _decode_radius_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_height_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb0b97f9f: ('path_flags', _decode_path_flags),
    0xf25ffdff: ('path_curve_type', _decode_path_curve_type),
    0xf8af858c: ('radius_control', _decode_radius_control),
    0x72cd60ce: ('height_control', _decode_height_control),
}
