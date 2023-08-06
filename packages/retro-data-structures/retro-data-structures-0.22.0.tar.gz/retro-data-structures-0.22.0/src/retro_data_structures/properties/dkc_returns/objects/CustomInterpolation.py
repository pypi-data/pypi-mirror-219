# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.FOVInterpolationMethod import FOVInterpolationMethod
from retro_data_structures.properties.dkc_returns.archetypes.MotionInterpolationMethod import MotionInterpolationMethod
from retro_data_structures.properties.dkc_returns.archetypes.OrientationInterpolationMethod import OrientationInterpolationMethod


@dataclasses.dataclass()
class CustomInterpolation(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flags_camera_interpolation: int = dataclasses.field(default=3)
    distance: float = dataclasses.field(default=100.0)
    angle: float = dataclasses.field(default=135.0)
    motion_interpolation: MotionInterpolationMethod = dataclasses.field(default_factory=MotionInterpolationMethod)
    orientation_interpolation: OrientationInterpolationMethod = dataclasses.field(default_factory=OrientationInterpolationMethod)
    fov_interpolation_method: FOVInterpolationMethod = dataclasses.field(default_factory=FOVInterpolationMethod)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CSTI'

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

        data.write(b'g\xa9\x84\xcb')  # 0x67a984cb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_camera_interpolation))

        data.write(b'\xc3\xbfC\xbe')  # 0xc3bf43be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance))

        data.write(b'8*\x19s')  # 0x382a1973
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.angle))

        data.write(b'\x843^q')  # 0x84335e71
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_interpolation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d\xf8\xd3\x19')  # 0x1df8d319
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_interpolation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1\xfa\xf0$')  # 0x31faf024
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fov_interpolation_method.to_stream(data)
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
            flags_camera_interpolation=data['flags_camera_interpolation'],
            distance=data['distance'],
            angle=data['angle'],
            motion_interpolation=MotionInterpolationMethod.from_json(data['motion_interpolation']),
            orientation_interpolation=OrientationInterpolationMethod.from_json(data['orientation_interpolation']),
            fov_interpolation_method=FOVInterpolationMethod.from_json(data['fov_interpolation_method']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flags_camera_interpolation': self.flags_camera_interpolation,
            'distance': self.distance,
            'angle': self.angle,
            'motion_interpolation': self.motion_interpolation.to_json(),
            'orientation_interpolation': self.orientation_interpolation.to_json(),
            'fov_interpolation_method': self.fov_interpolation_method.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flags_camera_interpolation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_motion_interpolation(data: typing.BinaryIO, property_size: int):
    return MotionInterpolationMethod.from_stream(data, property_size)


def _decode_orientation_interpolation(data: typing.BinaryIO, property_size: int):
    return OrientationInterpolationMethod.from_stream(data, property_size)


def _decode_fov_interpolation_method(data: typing.BinaryIO, property_size: int):
    return FOVInterpolationMethod.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x67a984cb: ('flags_camera_interpolation', _decode_flags_camera_interpolation),
    0xc3bf43be: ('distance', _decode_distance),
    0x382a1973: ('angle', _decode_angle),
    0x84335e71: ('motion_interpolation', _decode_motion_interpolation),
    0x1df8d319: ('orientation_interpolation', _decode_orientation_interpolation),
    0x31faf024: ('fov_interpolation_method', _decode_fov_interpolation_method),
}
