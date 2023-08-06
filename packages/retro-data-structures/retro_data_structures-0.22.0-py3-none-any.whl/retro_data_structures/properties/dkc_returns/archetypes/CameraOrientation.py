# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence
from retro_data_structures.properties.dkc_returns.archetypes.OffsetSplines import OffsetSplines
from retro_data_structures.properties.dkc_returns.archetypes.PathDetermination import PathDetermination
from retro_data_structures.properties.dkc_returns.archetypes.SpindleOrientation import SpindleOrientation
from retro_data_structures.properties.dkc_returns.archetypes.SurfaceOrientation import SurfaceOrientation
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct13 import UnknownStruct13
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct74 import UnknownStruct74
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class CameraOrientation(BaseProperty):
    orientation_type: int = dataclasses.field(default=1973921119)  # Choice
    flags_orientation: int = dataclasses.field(default=8)
    look_at_type: enums.LookAtType = dataclasses.field(default=enums.LookAtType.Unknown1)
    locator_name: str = dataclasses.field(default='')
    pitch_angle: float = dataclasses.field(default=0.0)
    target_path_determination: PathDetermination = dataclasses.field(default_factory=PathDetermination)
    distance: float = dataclasses.field(default=0.0)
    distance_direction_method: enums.DistanceDirectionMethod = dataclasses.field(default=enums.DistanceDirectionMethod.Unknown1)
    look_at_motion: Convergence = dataclasses.field(default_factory=Convergence)
    look_at_offset: OffsetSplines = dataclasses.field(default_factory=OffsetSplines)
    target_control_spline: Spline = dataclasses.field(default_factory=Spline)
    unknown_struct13: UnknownStruct13 = dataclasses.field(default_factory=UnknownStruct13)
    spindle_orientation: SpindleOrientation = dataclasses.field(default_factory=SpindleOrientation)
    surface_orientation: SurfaceOrientation = dataclasses.field(default_factory=SurfaceOrientation)
    unknown_struct74: UnknownStruct74 = dataclasses.field(default_factory=UnknownStruct74)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\\r\xa9d')  # 0x5c72a964
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.orientation_type))

        data.write(b'b\x19\x02.')  # 0x6219022e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_orientation))

        data.write(b'D\x19\x1f\xb8')  # 0x44191fb8
        data.write(b'\x00\x04')  # size
        self.look_at_type.to_stream(data)

        data.write(b'\xfb\xc6\xc1\x10')  # 0xfbc6c110
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.locator_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'o\xf79.')  # 0x6ff7392e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pitch_angle))

        data.write(b'2F\x8c\x89')  # 0x32468c89
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.target_path_determination.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3\xbfC\xbe')  # 0xc3bf43be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance))

        data.write(b'\x10\xe7\x12\x1b')  # 0x10e7121b
        data.write(b'\x00\x04')  # size
        self.distance_direction_method.to_stream(data)

        data.write(b'\xdaT\xb3\xe9')  # 0xda54b3e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_at_motion.to_stream(data, default_override={'convergence_type': enums.ConvergenceType.Unknown1})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\t\x1f)6')  # 0x91f2936
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_at_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc4\xdf\xbf\xa7')  # 0xc4dfbfa7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.target_control_spline.to_stream(data)
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

        data.write(b'\x86\xbc\x03\xd3')  # 0x86bc03d3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_orientation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\xe1\xde\xee'")  # 0xe1deee27
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.surface_orientation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\xbbD\xea')  # 0xf6bb44ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct74.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            orientation_type=data['orientation_type'],
            flags_orientation=data['flags_orientation'],
            look_at_type=enums.LookAtType.from_json(data['look_at_type']),
            locator_name=data['locator_name'],
            pitch_angle=data['pitch_angle'],
            target_path_determination=PathDetermination.from_json(data['target_path_determination']),
            distance=data['distance'],
            distance_direction_method=enums.DistanceDirectionMethod.from_json(data['distance_direction_method']),
            look_at_motion=Convergence.from_json(data['look_at_motion']),
            look_at_offset=OffsetSplines.from_json(data['look_at_offset']),
            target_control_spline=Spline.from_json(data['target_control_spline']),
            unknown_struct13=UnknownStruct13.from_json(data['unknown_struct13']),
            spindle_orientation=SpindleOrientation.from_json(data['spindle_orientation']),
            surface_orientation=SurfaceOrientation.from_json(data['surface_orientation']),
            unknown_struct74=UnknownStruct74.from_json(data['unknown_struct74']),
        )

    def to_json(self) -> dict:
        return {
            'orientation_type': self.orientation_type,
            'flags_orientation': self.flags_orientation,
            'look_at_type': self.look_at_type.to_json(),
            'locator_name': self.locator_name,
            'pitch_angle': self.pitch_angle,
            'target_path_determination': self.target_path_determination.to_json(),
            'distance': self.distance,
            'distance_direction_method': self.distance_direction_method.to_json(),
            'look_at_motion': self.look_at_motion.to_json(),
            'look_at_offset': self.look_at_offset.to_json(),
            'target_control_spline': self.target_control_spline.to_json(),
            'unknown_struct13': self.unknown_struct13.to_json(),
            'spindle_orientation': self.spindle_orientation.to_json(),
            'surface_orientation': self.surface_orientation.to_json(),
            'unknown_struct74': self.unknown_struct74.to_json(),
        }


def _decode_orientation_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_flags_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_look_at_type(data: typing.BinaryIO, property_size: int):
    return enums.LookAtType.from_stream(data)


def _decode_locator_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_pitch_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_path_determination(data: typing.BinaryIO, property_size: int):
    return PathDetermination.from_stream(data, property_size)


def _decode_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance_direction_method(data: typing.BinaryIO, property_size: int):
    return enums.DistanceDirectionMethod.from_stream(data)


def _decode_look_at_motion(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size, default_override={'convergence_type': enums.ConvergenceType.Unknown1})


def _decode_look_at_offset(data: typing.BinaryIO, property_size: int):
    return OffsetSplines.from_stream(data, property_size)


def _decode_target_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_struct13(data: typing.BinaryIO, property_size: int):
    return UnknownStruct13.from_stream(data, property_size)


def _decode_spindle_orientation(data: typing.BinaryIO, property_size: int):
    return SpindleOrientation.from_stream(data, property_size)


def _decode_surface_orientation(data: typing.BinaryIO, property_size: int):
    return SurfaceOrientation.from_stream(data, property_size)


def _decode_unknown_struct74(data: typing.BinaryIO, property_size: int):
    return UnknownStruct74.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5c72a964: ('orientation_type', _decode_orientation_type),
    0x6219022e: ('flags_orientation', _decode_flags_orientation),
    0x44191fb8: ('look_at_type', _decode_look_at_type),
    0xfbc6c110: ('locator_name', _decode_locator_name),
    0x6ff7392e: ('pitch_angle', _decode_pitch_angle),
    0x32468c89: ('target_path_determination', _decode_target_path_determination),
    0xc3bf43be: ('distance', _decode_distance),
    0x10e7121b: ('distance_direction_method', _decode_distance_direction_method),
    0xda54b3e9: ('look_at_motion', _decode_look_at_motion),
    0x91f2936: ('look_at_offset', _decode_look_at_offset),
    0xc4dfbfa7: ('target_control_spline', _decode_target_control_spline),
    0xe1f2094: ('unknown_struct13', _decode_unknown_struct13),
    0x86bc03d3: ('spindle_orientation', _decode_spindle_orientation),
    0xe1deee27: ('surface_orientation', _decode_surface_orientation),
    0xf6bb44ea: ('unknown_struct74', _decode_unknown_struct74),
}
