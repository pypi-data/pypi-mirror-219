# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.FOVInterpolationMethod import FOVInterpolationMethod
from retro_data_structures.properties.corruption.archetypes.MotionInterpolationMethod import MotionInterpolationMethod
from retro_data_structures.properties.corruption.archetypes.OrientationInterpolationMethod import OrientationInterpolationMethod


@dataclasses.dataclass()
class CameraInterpolation(BaseProperty):
    on_flags: int = dataclasses.field(default=3)  # Flagset
    on_distance: float = dataclasses.field(default=100.0)
    on_angle: float = dataclasses.field(default=135.0)
    motion_interpolation_on: MotionInterpolationMethod = dataclasses.field(default_factory=MotionInterpolationMethod)
    orientation_interpolation_on: OrientationInterpolationMethod = dataclasses.field(default_factory=OrientationInterpolationMethod)
    fov_interpolation_on: FOVInterpolationMethod = dataclasses.field(default_factory=FOVInterpolationMethod)
    off_flags: int = dataclasses.field(default=3)  # Flagset
    off_distance: float = dataclasses.field(default=100.0)
    off_angle: float = dataclasses.field(default=135.0)
    motion_interpolation_off: MotionInterpolationMethod = dataclasses.field(default_factory=MotionInterpolationMethod)
    orientation_interpolation_off: OrientationInterpolationMethod = dataclasses.field(default_factory=OrientationInterpolationMethod)
    fov_interpolation_off: FOVInterpolationMethod = dataclasses.field(default_factory=FOVInterpolationMethod)
    custom_flags: int = dataclasses.field(default=3)  # Flagset
    custom_distance: float = dataclasses.field(default=100.0)
    custom_angle: float = dataclasses.field(default=135.0)
    motion_interpolation_custom: MotionInterpolationMethod = dataclasses.field(default_factory=MotionInterpolationMethod)
    orientation_interpolation_custom: OrientationInterpolationMethod = dataclasses.field(default_factory=OrientationInterpolationMethod)
    fov_interpolation_method: FOVInterpolationMethod = dataclasses.field(default_factory=FOVInterpolationMethod)

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\x1dI\xd3\\')  # 0x1d49d35c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.on_flags))

        data.write(b'\xc2-d\x92')  # 0xc22d6492
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.on_distance))

        data.write(b'\xe0 "\xd5')  # 0xe02022d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.on_angle))

        data.write(b'\xa78y\n')  # 0xa738790a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_interpolation_on.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7h\xa1\x8e')  # 0xa768a18e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_interpolation_on.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b';\x8c|\xb4')  # 0x3b8c7cb4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fov_interpolation_on.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05\x8c\x1b\x1d')  # 0x58c1b1d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.off_flags))

        data.write(b"\x94?\x8a'")  # 0x943f8a27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.off_distance))

        data.write(b"1'\xe6\x8a")  # 0x3127e68a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.off_angle))

        data.write(b'\x7f\xacs*')  # 0x7fac732a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_interpolation_off.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\xabs\xb6')  # 0xdfab73b6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_interpolation_off.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\x91\xed\xbc')  # 0xf391edbc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fov_interpolation_off.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x07\xa6\xc2,')  # 0x7a6c22c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.custom_flags))

        data.write(b'\xc4\xe7@\x18')  # 0xc4e74018
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_distance))

        data.write(b'(\xb3\xb4\xb5')  # 0x28b3b4b5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.custom_angle))

        data.write(b'\xbcr<\xac')  # 0xbc723cac
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_interpolation_custom.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbe\t6v')  # 0xbe093676
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_interpolation_custom.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'puN\x15')  # 0x70754e15
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fov_interpolation_method.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            on_flags=data['on_flags'],
            on_distance=data['on_distance'],
            on_angle=data['on_angle'],
            motion_interpolation_on=MotionInterpolationMethod.from_json(data['motion_interpolation_on']),
            orientation_interpolation_on=OrientationInterpolationMethod.from_json(data['orientation_interpolation_on']),
            fov_interpolation_on=FOVInterpolationMethod.from_json(data['fov_interpolation_on']),
            off_flags=data['off_flags'],
            off_distance=data['off_distance'],
            off_angle=data['off_angle'],
            motion_interpolation_off=MotionInterpolationMethod.from_json(data['motion_interpolation_off']),
            orientation_interpolation_off=OrientationInterpolationMethod.from_json(data['orientation_interpolation_off']),
            fov_interpolation_off=FOVInterpolationMethod.from_json(data['fov_interpolation_off']),
            custom_flags=data['custom_flags'],
            custom_distance=data['custom_distance'],
            custom_angle=data['custom_angle'],
            motion_interpolation_custom=MotionInterpolationMethod.from_json(data['motion_interpolation_custom']),
            orientation_interpolation_custom=OrientationInterpolationMethod.from_json(data['orientation_interpolation_custom']),
            fov_interpolation_method=FOVInterpolationMethod.from_json(data['fov_interpolation_method']),
        )

    def to_json(self) -> dict:
        return {
            'on_flags': self.on_flags,
            'on_distance': self.on_distance,
            'on_angle': self.on_angle,
            'motion_interpolation_on': self.motion_interpolation_on.to_json(),
            'orientation_interpolation_on': self.orientation_interpolation_on.to_json(),
            'fov_interpolation_on': self.fov_interpolation_on.to_json(),
            'off_flags': self.off_flags,
            'off_distance': self.off_distance,
            'off_angle': self.off_angle,
            'motion_interpolation_off': self.motion_interpolation_off.to_json(),
            'orientation_interpolation_off': self.orientation_interpolation_off.to_json(),
            'fov_interpolation_off': self.fov_interpolation_off.to_json(),
            'custom_flags': self.custom_flags,
            'custom_distance': self.custom_distance,
            'custom_angle': self.custom_angle,
            'motion_interpolation_custom': self.motion_interpolation_custom.to_json(),
            'orientation_interpolation_custom': self.orientation_interpolation_custom.to_json(),
            'fov_interpolation_method': self.fov_interpolation_method.to_json(),
        }


def _decode_on_flags(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_on_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_on_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_motion_interpolation_on(data: typing.BinaryIO, property_size: int):
    return MotionInterpolationMethod.from_stream(data, property_size)


def _decode_orientation_interpolation_on(data: typing.BinaryIO, property_size: int):
    return OrientationInterpolationMethod.from_stream(data, property_size)


def _decode_fov_interpolation_on(data: typing.BinaryIO, property_size: int):
    return FOVInterpolationMethod.from_stream(data, property_size)


def _decode_off_flags(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_off_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_off_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_motion_interpolation_off(data: typing.BinaryIO, property_size: int):
    return MotionInterpolationMethod.from_stream(data, property_size)


def _decode_orientation_interpolation_off(data: typing.BinaryIO, property_size: int):
    return OrientationInterpolationMethod.from_stream(data, property_size)


def _decode_fov_interpolation_off(data: typing.BinaryIO, property_size: int):
    return FOVInterpolationMethod.from_stream(data, property_size)


def _decode_custom_flags(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_custom_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_custom_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_motion_interpolation_custom(data: typing.BinaryIO, property_size: int):
    return MotionInterpolationMethod.from_stream(data, property_size)


def _decode_orientation_interpolation_custom(data: typing.BinaryIO, property_size: int):
    return OrientationInterpolationMethod.from_stream(data, property_size)


def _decode_fov_interpolation_method(data: typing.BinaryIO, property_size: int):
    return FOVInterpolationMethod.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1d49d35c: ('on_flags', _decode_on_flags),
    0xc22d6492: ('on_distance', _decode_on_distance),
    0xe02022d5: ('on_angle', _decode_on_angle),
    0xa738790a: ('motion_interpolation_on', _decode_motion_interpolation_on),
    0xa768a18e: ('orientation_interpolation_on', _decode_orientation_interpolation_on),
    0x3b8c7cb4: ('fov_interpolation_on', _decode_fov_interpolation_on),
    0x58c1b1d: ('off_flags', _decode_off_flags),
    0x943f8a27: ('off_distance', _decode_off_distance),
    0x3127e68a: ('off_angle', _decode_off_angle),
    0x7fac732a: ('motion_interpolation_off', _decode_motion_interpolation_off),
    0xdfab73b6: ('orientation_interpolation_off', _decode_orientation_interpolation_off),
    0xf391edbc: ('fov_interpolation_off', _decode_fov_interpolation_off),
    0x7a6c22c: ('custom_flags', _decode_custom_flags),
    0xc4e74018: ('custom_distance', _decode_custom_distance),
    0x28b3b4b5: ('custom_angle', _decode_custom_angle),
    0xbc723cac: ('motion_interpolation_custom', _decode_motion_interpolation_custom),
    0xbe093676: ('orientation_interpolation_custom', _decode_orientation_interpolation_custom),
    0x70754e15: ('fov_interpolation_method', _decode_fov_interpolation_method),
}
