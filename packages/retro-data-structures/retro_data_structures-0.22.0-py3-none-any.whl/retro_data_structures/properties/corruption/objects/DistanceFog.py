# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.Vector2f import Vector2f
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class DistanceFog(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_0x88e8d530: int = dataclasses.field(default=3630416747)  # Choice
    mode: int = dataclasses.field(default=0)
    color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=1.0, b=0.0, a=0.0))
    near_far_plane: Vector2f = dataclasses.field(default_factory=Vector2f)
    color_rate: float = dataclasses.field(default=0.0)
    distance_rate: Vector2f = dataclasses.field(default_factory=Vector2f)
    force_settings: bool = dataclasses.field(default=False)
    is_two_sided: bool = dataclasses.field(default=False)
    unknown_0xb7246843: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=1.0, b=0.0, a=0.0))
    vector2f_0x520d1dd5: Vector2f = dataclasses.field(default_factory=Vector2f)
    unknown_0xbc86052a: float = dataclasses.field(default=0.0)
    vector2f_0xfba31a97: Vector2f = dataclasses.field(default_factory=Vector2f)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DFOG'

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data, default_override={'active': False})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88\xe8\xd50')  # 0x88e8d530
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x88e8d530))

        data.write(b'\t\xadc\xde')  # 0x9ad63de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.mode))

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

        data.write(b'e \x08\xda')  # 0x652008da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.near_far_plane.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b")\xabG'")  # 0x29ab4727
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.color_rate))

        data.write(b'\xcc\x8e\x0f\x98')  # 0xcc8e0f98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.distance_rate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5\x93[g')  # 0xc5935b67
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_settings))

        data.write(b'\xb5\xd1\xef\x02')  # 0xb5d1ef02
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_two_sided))

        data.write(b'\xb7$hC')  # 0xb7246843
        data.write(b'\x00\x10')  # size
        self.unknown_0xb7246843.to_stream(data)

        data.write(b'R\r\x1d\xd5')  # 0x520d1dd5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vector2f_0x520d1dd5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc\x86\x05*')  # 0xbc86052a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbc86052a))

        data.write(b'\xfb\xa3\x1a\x97')  # 0xfba31a97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vector2f_0xfba31a97.to_stream(data)
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
            unknown_0x88e8d530=data['unknown_0x88e8d530'],
            mode=data['mode'],
            color=Color.from_json(data['color']),
            near_far_plane=Vector2f.from_json(data['near_far_plane']),
            color_rate=data['color_rate'],
            distance_rate=Vector2f.from_json(data['distance_rate']),
            force_settings=data['force_settings'],
            is_two_sided=data['is_two_sided'],
            unknown_0xb7246843=Color.from_json(data['unknown_0xb7246843']),
            vector2f_0x520d1dd5=Vector2f.from_json(data['vector2f_0x520d1dd5']),
            unknown_0xbc86052a=data['unknown_0xbc86052a'],
            vector2f_0xfba31a97=Vector2f.from_json(data['vector2f_0xfba31a97']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_0x88e8d530': self.unknown_0x88e8d530,
            'mode': self.mode,
            'color': self.color.to_json(),
            'near_far_plane': self.near_far_plane.to_json(),
            'color_rate': self.color_rate,
            'distance_rate': self.distance_rate.to_json(),
            'force_settings': self.force_settings,
            'is_two_sided': self.is_two_sided,
            'unknown_0xb7246843': self.unknown_0xb7246843.to_json(),
            'vector2f_0x520d1dd5': self.vector2f_0x520d1dd5.to_json(),
            'unknown_0xbc86052a': self.unknown_0xbc86052a,
            'vector2f_0xfba31a97': self.vector2f_0xfba31a97.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size, default_override={'active': False})


def _decode_unknown_0x88e8d530(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_near_far_plane(data: typing.BinaryIO, property_size: int):
    return Vector2f.from_stream(data, property_size)


def _decode_color_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance_rate(data: typing.BinaryIO, property_size: int):
    return Vector2f.from_stream(data, property_size)


def _decode_force_settings(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_two_sided(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb7246843(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_vector2f_0x520d1dd5(data: typing.BinaryIO, property_size: int):
    return Vector2f.from_stream(data, property_size)


def _decode_unknown_0xbc86052a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vector2f_0xfba31a97(data: typing.BinaryIO, property_size: int):
    return Vector2f.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x88e8d530: ('unknown_0x88e8d530', _decode_unknown_0x88e8d530),
    0x9ad63de: ('mode', _decode_mode),
    0x37c7d09d: ('color', _decode_color),
    0x652008da: ('near_far_plane', _decode_near_far_plane),
    0x29ab4727: ('color_rate', _decode_color_rate),
    0xcc8e0f98: ('distance_rate', _decode_distance_rate),
    0xc5935b67: ('force_settings', _decode_force_settings),
    0xb5d1ef02: ('is_two_sided', _decode_is_two_sided),
    0xb7246843: ('unknown_0xb7246843', _decode_unknown_0xb7246843),
    0x520d1dd5: ('vector2f_0x520d1dd5', _decode_vector2f_0x520d1dd5),
    0xbc86052a: ('unknown_0xbc86052a', _decode_unknown_0xbc86052a),
    0xfba31a97: ('vector2f_0xfba31a97', _decode_vector2f_0xfba31a97),
}
