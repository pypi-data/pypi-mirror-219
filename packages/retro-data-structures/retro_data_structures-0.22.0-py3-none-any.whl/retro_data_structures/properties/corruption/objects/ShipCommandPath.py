# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PlatformMotionProperties import PlatformMotionProperties


@dataclasses.dataclass()
class ShipCommandPath(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    motion_properties: PlatformMotionProperties = dataclasses.field(default_factory=PlatformMotionProperties)
    unknown_0x8df64d50: bool = dataclasses.field(default=False)
    stick_to_spline: bool = dataclasses.field(default=False)
    unknown_0x04c4e40b: bool = dataclasses.field(default=True)
    path_range: float = dataclasses.field(default=50.0)
    path_cone_angle: float = dataclasses.field(default=360.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SHCP'

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

        data.write(b'\n\x9d\xbf\x91')  # 0xa9dbf91
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d\xf6MP')  # 0x8df64d50
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8df64d50))

        data.write(b'\xd9R\xf5\x1a')  # 0xd952f51a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.stick_to_spline))

        data.write(b'\x04\xc4\xe4\x0b')  # 0x4c4e40b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x04c4e40b))

        data.write(b'=F\xb7\x99')  # 0x3d46b799
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.path_range))

        data.write(b'\xae\x8d \xaa')  # 0xae8d20aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.path_cone_angle))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            motion_properties=PlatformMotionProperties.from_json(data['motion_properties']),
            unknown_0x8df64d50=data['unknown_0x8df64d50'],
            stick_to_spline=data['stick_to_spline'],
            unknown_0x04c4e40b=data['unknown_0x04c4e40b'],
            path_range=data['path_range'],
            path_cone_angle=data['path_cone_angle'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'motion_properties': self.motion_properties.to_json(),
            'unknown_0x8df64d50': self.unknown_0x8df64d50,
            'stick_to_spline': self.stick_to_spline,
            'unknown_0x04c4e40b': self.unknown_0x04c4e40b,
            'path_range': self.path_range,
            'path_cone_angle': self.path_cone_angle,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_motion_properties(data: typing.BinaryIO, property_size: int):
    return PlatformMotionProperties.from_stream(data, property_size)


def _decode_unknown_0x8df64d50(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_stick_to_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x04c4e40b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_path_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_path_cone_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xa9dbf91: ('motion_properties', _decode_motion_properties),
    0x8df64d50: ('unknown_0x8df64d50', _decode_unknown_0x8df64d50),
    0xd952f51a: ('stick_to_spline', _decode_stick_to_spline),
    0x4c4e40b: ('unknown_0x04c4e40b', _decode_unknown_0x04c4e40b),
    0x3d46b799: ('path_range', _decode_path_range),
    0xae8d20aa: ('path_cone_angle', _decode_path_cone_angle),
}
