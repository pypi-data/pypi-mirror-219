# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.PlatformMotionProperties import PlatformMotionProperties


@dataclasses.dataclass()
class MotionPlatform(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    motion_properties: PlatformMotionProperties = dataclasses.field(default_factory=PlatformMotionProperties)
    max_velocity: float = dataclasses.field(default=1.0)
    elevation_velocity: float = dataclasses.field(default=1.0)
    radius: float = dataclasses.field(default=10.0)
    elevation: float = dataclasses.field(default=0.0)
    max_elevation: float = dataclasses.field(default=1.0)
    min_elevation: float = dataclasses.field(default=-1.0)
    direction: enums.Direction = dataclasses.field(default=enums.Direction.Unknown1)
    convergence: Convergence = dataclasses.field(default_factory=Convergence)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'MNPL'

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
        data.write(b'\x00\n')  # 10 properties

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

        data.write(b'\xe4\xf8\x9c\x8f')  # 0xe4f89c8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_velocity))

        data.write(b';;\x92\xa6')  # 0x3b3b92a6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.elevation_velocity))

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'\xc58B\x00')  # 0xc5384200
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.elevation))

        data.write(b'\xcch\x06\xa1')  # 0xcc6806a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_elevation))

        data.write(b'\xd9\xe3\xd2S')  # 0xd9e3d253
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_elevation))

        data.write(b'\nD\x1e\x0c')  # 0xa441e0c
        data.write(b'\x00\x04')  # size
        self.direction.to_stream(data)

        data.write(b'V\xf4\xbc\x93')  # 0x56f4bc93
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence.to_stream(data)
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
            motion_properties=PlatformMotionProperties.from_json(data['motion_properties']),
            max_velocity=data['max_velocity'],
            elevation_velocity=data['elevation_velocity'],
            radius=data['radius'],
            elevation=data['elevation'],
            max_elevation=data['max_elevation'],
            min_elevation=data['min_elevation'],
            direction=enums.Direction.from_json(data['direction']),
            convergence=Convergence.from_json(data['convergence']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'motion_properties': self.motion_properties.to_json(),
            'max_velocity': self.max_velocity,
            'elevation_velocity': self.elevation_velocity,
            'radius': self.radius,
            'elevation': self.elevation,
            'max_elevation': self.max_elevation,
            'min_elevation': self.min_elevation,
            'direction': self.direction.to_json(),
            'convergence': self.convergence.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_motion_properties(data: typing.BinaryIO, property_size: int):
    return PlatformMotionProperties.from_stream(data, property_size)


def _decode_max_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_elevation_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_direction(data: typing.BinaryIO, property_size: int):
    return enums.Direction.from_stream(data)


def _decode_convergence(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xa9dbf91: ('motion_properties', _decode_motion_properties),
    0xe4f89c8f: ('max_velocity', _decode_max_velocity),
    0x3b3b92a6: ('elevation_velocity', _decode_elevation_velocity),
    0x78c507eb: ('radius', _decode_radius),
    0xc5384200: ('elevation', _decode_elevation),
    0xcc6806a1: ('max_elevation', _decode_max_elevation),
    0xd9e3d253: ('min_elevation', _decode_min_elevation),
    0xa441e0c: ('direction', _decode_direction),
    0x56f4bc93: ('convergence', _decode_convergence),
}
