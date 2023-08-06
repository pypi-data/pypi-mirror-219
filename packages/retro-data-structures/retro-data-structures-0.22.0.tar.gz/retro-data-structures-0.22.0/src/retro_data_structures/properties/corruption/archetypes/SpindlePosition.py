# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.SpindlePositionInterpolant import SpindlePositionInterpolant


@dataclasses.dataclass()
class SpindlePosition(BaseProperty):
    flags_spindle_position: int = dataclasses.field(default=320)  # Flagset
    angular_speed: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    linear_speed: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    motion_radius: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    radial_offset: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    desired_angular_offset: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    min_angular_offset: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    max_angular_offset: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    z_offset: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    angular_constraint: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    angular_dampening: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    desired_angular_speed: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)
    constraint_flip_angle: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\xb8\xa6A:')  # 0xb8a6413a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_spindle_position))

        data.write(b'\xa0\xfb\x99\x86')  # 0xa0fb9986
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.angular_speed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\x07\x95\x83')  # 0x58079583
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.linear_speed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4L\x10\x03')  # 0xe44c1003
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_radius.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'9\x93i6')  # 0x39936936
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.radial_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-\x8c8\xb0')  # 0x2d8c38b0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.desired_angular_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d*a\x88')  # 0x1d2a6188
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.min_angular_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91\xcc\x9fj')  # 0x91cc9f6a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.max_angular_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x90R\x89\xac')  # 0x905289ac
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.z_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5\xf6\x84\x9d')  # 0xf5f6849d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.angular_constraint.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{f\xa7\xb4')  # 0x7b66a7b4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.angular_dampening.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\x92l\xcd')  # 0x68926ccd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.desired_angular_speed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1X\xfd;')  # 0x3158fd3b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.constraint_flip_angle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flags_spindle_position=data['flags_spindle_position'],
            angular_speed=SpindlePositionInterpolant.from_json(data['angular_speed']),
            linear_speed=SpindlePositionInterpolant.from_json(data['linear_speed']),
            motion_radius=SpindlePositionInterpolant.from_json(data['motion_radius']),
            radial_offset=SpindlePositionInterpolant.from_json(data['radial_offset']),
            desired_angular_offset=SpindlePositionInterpolant.from_json(data['desired_angular_offset']),
            min_angular_offset=SpindlePositionInterpolant.from_json(data['min_angular_offset']),
            max_angular_offset=SpindlePositionInterpolant.from_json(data['max_angular_offset']),
            z_offset=SpindlePositionInterpolant.from_json(data['z_offset']),
            angular_constraint=SpindlePositionInterpolant.from_json(data['angular_constraint']),
            angular_dampening=SpindlePositionInterpolant.from_json(data['angular_dampening']),
            desired_angular_speed=SpindlePositionInterpolant.from_json(data['desired_angular_speed']),
            constraint_flip_angle=SpindlePositionInterpolant.from_json(data['constraint_flip_angle']),
        )

    def to_json(self) -> dict:
        return {
            'flags_spindle_position': self.flags_spindle_position,
            'angular_speed': self.angular_speed.to_json(),
            'linear_speed': self.linear_speed.to_json(),
            'motion_radius': self.motion_radius.to_json(),
            'radial_offset': self.radial_offset.to_json(),
            'desired_angular_offset': self.desired_angular_offset.to_json(),
            'min_angular_offset': self.min_angular_offset.to_json(),
            'max_angular_offset': self.max_angular_offset.to_json(),
            'z_offset': self.z_offset.to_json(),
            'angular_constraint': self.angular_constraint.to_json(),
            'angular_dampening': self.angular_dampening.to_json(),
            'desired_angular_speed': self.desired_angular_speed.to_json(),
            'constraint_flip_angle': self.constraint_flip_angle.to_json(),
        }


def _decode_flags_spindle_position(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_angular_speed(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_linear_speed(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_motion_radius(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_radial_offset(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_desired_angular_offset(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_min_angular_offset(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_max_angular_offset(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_z_offset(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_angular_constraint(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_angular_dampening(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_desired_angular_speed(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


def _decode_constraint_flip_angle(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb8a6413a: ('flags_spindle_position', _decode_flags_spindle_position),
    0xa0fb9986: ('angular_speed', _decode_angular_speed),
    0x58079583: ('linear_speed', _decode_linear_speed),
    0xe44c1003: ('motion_radius', _decode_motion_radius),
    0x39936936: ('radial_offset', _decode_radial_offset),
    0x2d8c38b0: ('desired_angular_offset', _decode_desired_angular_offset),
    0x1d2a6188: ('min_angular_offset', _decode_min_angular_offset),
    0x91cc9f6a: ('max_angular_offset', _decode_max_angular_offset),
    0x905289ac: ('z_offset', _decode_z_offset),
    0xf5f6849d: ('angular_constraint', _decode_angular_constraint),
    0x7b66a7b4: ('angular_dampening', _decode_angular_dampening),
    0x68926ccd: ('desired_angular_speed', _decode_desired_angular_speed),
    0x3158fd3b: ('constraint_flip_angle', _decode_constraint_flip_angle),
}
