# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.SplineType import SplineType
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class PlatformMotionProperties(BaseProperty):
    motion_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    motion_spline_duration: float = dataclasses.field(default=10.0)
    initial_time: float = dataclasses.field(default=0.0)
    unknown: int = dataclasses.field(default=288)
    roll_control_spline: Spline = dataclasses.field(default_factory=Spline)
    yaw_control_spline: Spline = dataclasses.field(default_factory=Spline)
    pitch_control_spline: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'I=j-')  # 0x493d6a2d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_spline_type.to_stream(data)
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

        data.write(b'\xfd\x1e/V')  # 0xfd1e2f56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.motion_spline_duration))

        data.write(b'\xa5u=R')  # 0xa5753d52
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_time))

        data.write(b'\xae\x80b\x8f')  # 0xae80628f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'b\x8b\xdf\x0f')  # 0x628bdf0f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.roll_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\xd0:2')  # 0x78d03a32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.yaw_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4\xa2\xe1Z')  # 0xb4a2e15a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pitch_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_spline_type=SplineType.from_json(data['motion_spline_type']),
            motion_control_spline=Spline.from_json(data['motion_control_spline']),
            motion_spline_duration=data['motion_spline_duration'],
            initial_time=data['initial_time'],
            unknown=data['unknown'],
            roll_control_spline=Spline.from_json(data['roll_control_spline']),
            yaw_control_spline=Spline.from_json(data['yaw_control_spline']),
            pitch_control_spline=Spline.from_json(data['pitch_control_spline']),
        )

    def to_json(self) -> dict:
        return {
            'motion_spline_type': self.motion_spline_type.to_json(),
            'motion_control_spline': self.motion_control_spline.to_json(),
            'motion_spline_duration': self.motion_spline_duration,
            'initial_time': self.initial_time,
            'unknown': self.unknown,
            'roll_control_spline': self.roll_control_spline.to_json(),
            'yaw_control_spline': self.yaw_control_spline.to_json(),
            'pitch_control_spline': self.pitch_control_spline.to_json(),
        }

    def _dependencies_for_motion_spline_type(self, asset_manager):
        yield from self.motion_spline_type.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_motion_spline_type, "motion_spline_type", "SplineType"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PlatformMotionProperties.{field_name} ({field_type}): {e}"
                )


def _decode_motion_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_motion_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_motion_spline_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_roll_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_yaw_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_pitch_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x493d6a2d: ('motion_spline_type', _decode_motion_spline_type),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0xfd1e2f56: ('motion_spline_duration', _decode_motion_spline_duration),
    0xa5753d52: ('initial_time', _decode_initial_time),
    0xae80628f: ('unknown', _decode_unknown),
    0x628bdf0f: ('roll_control_spline', _decode_roll_control_spline),
    0x78d03a32: ('yaw_control_spline', _decode_yaw_control_spline),
    0xb4a2e15a: ('pitch_control_spline', _decode_pitch_control_spline),
}
