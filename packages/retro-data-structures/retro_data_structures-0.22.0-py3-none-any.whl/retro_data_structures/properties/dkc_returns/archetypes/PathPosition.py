# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence
from retro_data_structures.properties.dkc_returns.archetypes.PathDetermination import PathDetermination
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct13 import UnknownStruct13
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class PathPosition(BaseProperty):
    flags_path_position: int = dataclasses.field(default=0)
    initial_position: enums.InitialPosition = dataclasses.field(default=enums.InitialPosition.Unknown1)
    path_determination: PathDetermination = dataclasses.field(default_factory=PathDetermination)
    distance: float = dataclasses.field(default=4.0)
    dampen_distance: float = dataclasses.field(default=3.0)
    convergence: Convergence = dataclasses.field(default_factory=Convergence)
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    unknown: Spline = dataclasses.field(default_factory=Spline)
    unknown_struct13: UnknownStruct13 = dataclasses.field(default_factory=UnknownStruct13)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'%\x9d2y')  # 0x259d3279
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_path_position))

        data.write(b'4\x0eL\xa3')  # 0x340e4ca3
        data.write(b'\x00\x04')  # size
        self.initial_position.to_stream(data)

        data.write(b'\n\xed\\}')  # 0xaed5c7d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path_determination.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3\xbfC\xbe')  # 0xc3bf43be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance))

        data.write(b'2\xf85\xec')  # 0x32f835ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dampen_distance))

        data.write(b'\x95\x91\x08\xa5')  # 0x959108a5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"'\xe5\xf8t")  # 0x27e5f874
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12\x86\x1f}')  # 0x12861f7d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0e\x1f \x94')  # 0xe1f2094
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct13.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flags_path_position=data['flags_path_position'],
            initial_position=enums.InitialPosition.from_json(data['initial_position']),
            path_determination=PathDetermination.from_json(data['path_determination']),
            distance=data['distance'],
            dampen_distance=data['dampen_distance'],
            convergence=Convergence.from_json(data['convergence']),
            motion_control_spline=Spline.from_json(data['motion_control_spline']),
            unknown=Spline.from_json(data['unknown']),
            unknown_struct13=UnknownStruct13.from_json(data['unknown_struct13']),
        )

    def to_json(self) -> dict:
        return {
            'flags_path_position': self.flags_path_position,
            'initial_position': self.initial_position.to_json(),
            'path_determination': self.path_determination.to_json(),
            'distance': self.distance,
            'dampen_distance': self.dampen_distance,
            'convergence': self.convergence.to_json(),
            'motion_control_spline': self.motion_control_spline.to_json(),
            'unknown': self.unknown.to_json(),
            'unknown_struct13': self.unknown_struct13.to_json(),
        }


def _decode_flags_path_position(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_initial_position(data: typing.BinaryIO, property_size: int):
    return enums.InitialPosition.from_stream(data)


def _decode_path_determination(data: typing.BinaryIO, property_size: int):
    return PathDetermination.from_stream(data, property_size)


def _decode_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dampen_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_convergence(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_motion_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_struct13(data: typing.BinaryIO, property_size: int):
    return UnknownStruct13.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x259d3279: ('flags_path_position', _decode_flags_path_position),
    0x340e4ca3: ('initial_position', _decode_initial_position),
    0xaed5c7d: ('path_determination', _decode_path_determination),
    0xc3bf43be: ('distance', _decode_distance),
    0x32f835ec: ('dampen_distance', _decode_dampen_distance),
    0x959108a5: ('convergence', _decode_convergence),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0x12861f7d: ('unknown', _decode_unknown),
    0xe1f2094: ('unknown_struct13', _decode_unknown_struct13),
}
