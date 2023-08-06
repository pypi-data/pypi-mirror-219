# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.ChasePosition import ChasePosition
from retro_data_structures.properties.corruption.archetypes.ColliderPosition import ColliderPosition
from retro_data_structures.properties.corruption.archetypes.OffsetPosition import OffsetPosition
from retro_data_structures.properties.corruption.archetypes.PathPosition import PathPosition
from retro_data_structures.properties.corruption.archetypes.SpindlePosition import SpindlePosition
from retro_data_structures.properties.corruption.archetypes.SurfacePosition import SurfacePosition


@dataclasses.dataclass()
class CameraPosition(BaseProperty):
    position_type: enums.PositionType = dataclasses.field(default=enums.PositionType.Unknown1)
    flags_camera_position: int = dataclasses.field(default=2)  # Flagset
    colliders: ColliderPosition = dataclasses.field(default_factory=ColliderPosition)
    chase: ChasePosition = dataclasses.field(default_factory=ChasePosition)
    path: PathPosition = dataclasses.field(default_factory=PathPosition)
    spindle: SpindlePosition = dataclasses.field(default_factory=SpindlePosition)
    surface: SurfacePosition = dataclasses.field(default_factory=SurfacePosition)
    offset: OffsetPosition = dataclasses.field(default_factory=OffsetPosition)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xb7\xcdG\x10')  # 0xb7cd4710
        data.write(b'\x00\x04')  # size
        self.position_type.to_stream(data)

        data.write(b'\xb1\xb6\xcf3')  # 0xb1b6cf33
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_camera_position))

        data.write(b'P\x1e\xd3\xa3')  # 0x501ed3a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.colliders.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xdd\xc5v')  # 0xbbddc576
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.chase.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe8\xab\x9b\xc8')  # 0xe8ab9bc8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\xc1\xdf\x0c')  # 0x9ec1df0c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xb2\xd1\xe6')  # 0xbbb2d1e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.surface.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x07\xd1\x94\xaf')  # 0x7d194af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            position_type=enums.PositionType.from_json(data['position_type']),
            flags_camera_position=data['flags_camera_position'],
            colliders=ColliderPosition.from_json(data['colliders']),
            chase=ChasePosition.from_json(data['chase']),
            path=PathPosition.from_json(data['path']),
            spindle=SpindlePosition.from_json(data['spindle']),
            surface=SurfacePosition.from_json(data['surface']),
            offset=OffsetPosition.from_json(data['offset']),
        )

    def to_json(self) -> dict:
        return {
            'position_type': self.position_type.to_json(),
            'flags_camera_position': self.flags_camera_position,
            'colliders': self.colliders.to_json(),
            'chase': self.chase.to_json(),
            'path': self.path.to_json(),
            'spindle': self.spindle.to_json(),
            'surface': self.surface.to_json(),
            'offset': self.offset.to_json(),
        }


def _decode_position_type(data: typing.BinaryIO, property_size: int):
    return enums.PositionType.from_stream(data)


def _decode_flags_camera_position(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_colliders(data: typing.BinaryIO, property_size: int):
    return ColliderPosition.from_stream(data, property_size)


def _decode_chase(data: typing.BinaryIO, property_size: int):
    return ChasePosition.from_stream(data, property_size)


def _decode_path(data: typing.BinaryIO, property_size: int):
    return PathPosition.from_stream(data, property_size)


def _decode_spindle(data: typing.BinaryIO, property_size: int):
    return SpindlePosition.from_stream(data, property_size)


def _decode_surface(data: typing.BinaryIO, property_size: int):
    return SurfacePosition.from_stream(data, property_size)


def _decode_offset(data: typing.BinaryIO, property_size: int):
    return OffsetPosition.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb7cd4710: ('position_type', _decode_position_type),
    0xb1b6cf33: ('flags_camera_position', _decode_flags_camera_position),
    0x501ed3a3: ('colliders', _decode_colliders),
    0xbbddc576: ('chase', _decode_chase),
    0xe8ab9bc8: ('path', _decode_path),
    0x9ec1df0c: ('spindle', _decode_spindle),
    0xbbb2d1e6: ('surface', _decode_surface),
    0x7d194af: ('offset', _decode_offset),
}
