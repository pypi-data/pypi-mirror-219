# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class KongSwingData(BaseProperty):
    rope_grab_distance: float = dataclasses.field(default=10.0)
    minimum_swing_time: float = dataclasses.field(default=0.10000000149011612)
    swing_max_speed: float = dataclasses.field(default=30.0)
    minimum_jump_height: float = dataclasses.field(default=1.0)
    maximum_jump_height: float = dataclasses.field(default=3.0)
    jump_tap_time: float = dataclasses.field(default=0.10000000149011612)
    swing_acceleration: float = dataclasses.field(default=7.0)
    swing_acceleration_multiplier_based_on_rope_radius: float = dataclasses.field(default=3.0)
    vertical_release_factor: float = dataclasses.field(default=0.5)
    angle_dampen_factor: float = dataclasses.field(default=3.0)
    gravity: float = dataclasses.field(default=10.0)
    gravity_dampen_factor: float = dataclasses.field(default=1.100000023841858)
    climb_up_max_speed: float = dataclasses.field(default=4.0)
    climb_up_acceleration: float = dataclasses.field(default=20.0)
    climb_down_max_speed: float = dataclasses.field(default=4.0)
    climb_down_acceleration: float = dataclasses.field(default=20.0)
    climb_dampen_factor: float = dataclasses.field(default=4.0)
    climb_analog_degrees_from_vertical: float = dataclasses.field(default=0.0)
    grab_boost: float = dataclasses.field(default=2.0)
    time_between_grabs: float = dataclasses.field(default=0.20000000298023224)
    time_to_disable_on_scripted_release: float = dataclasses.field(default=1.0)
    stall_angle_threshold: float = dataclasses.field(default=5.0)
    auto_swing_release_velocity_x: float = dataclasses.field(default=6.0)
    auto_swing_jump_velocity_x: float = dataclasses.field(default=9.0)
    auto_swing_jump_vertical_velocity: float = dataclasses.field(default=6.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x19')  # 25 properties

        data.write(b'M\x0eL ')  # 0x4d0e4c20
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rope_grab_distance))

        data.write(b'\xeaT\xc4N')  # 0xea54c44e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_swing_time))

        data.write(b'r]=u')  # 0x725d3d75
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_max_speed))

        data.write(b'yz\xa5Q')  # 0x797aa551
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_jump_height))

        data.write(b'8m\x9a\xd7')  # 0x386d9ad7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_jump_height))

        data.write(b'x*\x03\x10')  # 0x782a0310
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_tap_time))

        data.write(b'mzR\t')  # 0x6d7a5209
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_acceleration))

        data.write(b'\xce\xfb\xfee')  # 0xcefbfe65
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_acceleration_multiplier_based_on_rope_radius))

        data.write(b'?I\xe9\x87')  # 0x3f49e987
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_release_factor))

        data.write(b':Z\xb3\x98')  # 0x3a5ab398
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.angle_dampen_factor))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\x1au\x844')  # 0x1a758434
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_dampen_factor))

        data.write(b'\x04m\xd3\x8f')  # 0x46dd38f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_up_max_speed))

        data.write(b'A\xfd\xbb\x9a')  # 0x41fdbb9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_up_acceleration))

        data.write(b'\xa8l\x03\x1f')  # 0xa86c031f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_down_max_speed))

        data.write(b'\xb7O\xb1\x8c')  # 0xb74fb18c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_down_acceleration))

        data.write(b'\xdf\xfa\xba>')  # 0xdffaba3e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_dampen_factor))

        data.write(b'\xda]g\xb1')  # 0xda5d67b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_analog_degrees_from_vertical))

        data.write(b'9=\x1aN')  # 0x393d1a4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_boost))

        data.write(b'\xd3,\xcf\x88')  # 0xd32ccf88
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_between_grabs))

        data.write(b'"\xc5\x7fd')  # 0x22c57f64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_to_disable_on_scripted_release))

        data.write(b'\xde\x81k\xd4')  # 0xde816bd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stall_angle_threshold))

        data.write(b'4\xbcsk')  # 0x34bc736b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.auto_swing_release_velocity_x))

        data.write(b'\xfc\xa1\xb4\xfa')  # 0xfca1b4fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.auto_swing_jump_velocity_x))

        data.write(b'\xb8?\xec\x12')  # 0xb83fec12
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.auto_swing_jump_vertical_velocity))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            rope_grab_distance=data['rope_grab_distance'],
            minimum_swing_time=data['minimum_swing_time'],
            swing_max_speed=data['swing_max_speed'],
            minimum_jump_height=data['minimum_jump_height'],
            maximum_jump_height=data['maximum_jump_height'],
            jump_tap_time=data['jump_tap_time'],
            swing_acceleration=data['swing_acceleration'],
            swing_acceleration_multiplier_based_on_rope_radius=data['swing_acceleration_multiplier_based_on_rope_radius'],
            vertical_release_factor=data['vertical_release_factor'],
            angle_dampen_factor=data['angle_dampen_factor'],
            gravity=data['gravity'],
            gravity_dampen_factor=data['gravity_dampen_factor'],
            climb_up_max_speed=data['climb_up_max_speed'],
            climb_up_acceleration=data['climb_up_acceleration'],
            climb_down_max_speed=data['climb_down_max_speed'],
            climb_down_acceleration=data['climb_down_acceleration'],
            climb_dampen_factor=data['climb_dampen_factor'],
            climb_analog_degrees_from_vertical=data['climb_analog_degrees_from_vertical'],
            grab_boost=data['grab_boost'],
            time_between_grabs=data['time_between_grabs'],
            time_to_disable_on_scripted_release=data['time_to_disable_on_scripted_release'],
            stall_angle_threshold=data['stall_angle_threshold'],
            auto_swing_release_velocity_x=data['auto_swing_release_velocity_x'],
            auto_swing_jump_velocity_x=data['auto_swing_jump_velocity_x'],
            auto_swing_jump_vertical_velocity=data['auto_swing_jump_vertical_velocity'],
        )

    def to_json(self) -> dict:
        return {
            'rope_grab_distance': self.rope_grab_distance,
            'minimum_swing_time': self.minimum_swing_time,
            'swing_max_speed': self.swing_max_speed,
            'minimum_jump_height': self.minimum_jump_height,
            'maximum_jump_height': self.maximum_jump_height,
            'jump_tap_time': self.jump_tap_time,
            'swing_acceleration': self.swing_acceleration,
            'swing_acceleration_multiplier_based_on_rope_radius': self.swing_acceleration_multiplier_based_on_rope_radius,
            'vertical_release_factor': self.vertical_release_factor,
            'angle_dampen_factor': self.angle_dampen_factor,
            'gravity': self.gravity,
            'gravity_dampen_factor': self.gravity_dampen_factor,
            'climb_up_max_speed': self.climb_up_max_speed,
            'climb_up_acceleration': self.climb_up_acceleration,
            'climb_down_max_speed': self.climb_down_max_speed,
            'climb_down_acceleration': self.climb_down_acceleration,
            'climb_dampen_factor': self.climb_dampen_factor,
            'climb_analog_degrees_from_vertical': self.climb_analog_degrees_from_vertical,
            'grab_boost': self.grab_boost,
            'time_between_grabs': self.time_between_grabs,
            'time_to_disable_on_scripted_release': self.time_to_disable_on_scripted_release,
            'stall_angle_threshold': self.stall_angle_threshold,
            'auto_swing_release_velocity_x': self.auto_swing_release_velocity_x,
            'auto_swing_jump_velocity_x': self.auto_swing_jump_velocity_x,
            'auto_swing_jump_vertical_velocity': self.auto_swing_jump_vertical_velocity,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x4d0e4c20, 0xea54c44e, 0x725d3d75, 0x797aa551, 0x386d9ad7, 0x782a0310, 0x6d7a5209, 0xcefbfe65, 0x3f49e987, 0x3a5ab398, 0x2f2ae3e5, 0x1a758434, 0x46dd38f, 0x41fdbb9a, 0xa86c031f, 0xb74fb18c, 0xdffaba3e, 0xda5d67b1, 0x393d1a4e, 0xd32ccf88, 0x22c57f64, 0xde816bd4, 0x34bc736b, 0xfca1b4fa, 0xb83fec12)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[KongSwingData]:
    if property_count != 25:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(250))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54], dec[57], dec[60], dec[63], dec[66], dec[69], dec[72]) != _FAST_IDS:
        data.seek(before)
        return None

    return KongSwingData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
        dec[35],
        dec[38],
        dec[41],
        dec[44],
        dec[47],
        dec[50],
        dec[53],
        dec[56],
        dec[59],
        dec[62],
        dec[65],
        dec[68],
        dec[71],
        dec[74],
    )


def _decode_rope_grab_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_swing_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_tap_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_acceleration_multiplier_based_on_rope_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vertical_release_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_angle_dampen_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity_dampen_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_up_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_up_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_down_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_down_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_dampen_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_analog_degrees_from_vertical(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grab_boost(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_between_grabs(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_to_disable_on_scripted_release(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stall_angle_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_auto_swing_release_velocity_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_auto_swing_jump_velocity_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_auto_swing_jump_vertical_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4d0e4c20: ('rope_grab_distance', _decode_rope_grab_distance),
    0xea54c44e: ('minimum_swing_time', _decode_minimum_swing_time),
    0x725d3d75: ('swing_max_speed', _decode_swing_max_speed),
    0x797aa551: ('minimum_jump_height', _decode_minimum_jump_height),
    0x386d9ad7: ('maximum_jump_height', _decode_maximum_jump_height),
    0x782a0310: ('jump_tap_time', _decode_jump_tap_time),
    0x6d7a5209: ('swing_acceleration', _decode_swing_acceleration),
    0xcefbfe65: ('swing_acceleration_multiplier_based_on_rope_radius', _decode_swing_acceleration_multiplier_based_on_rope_radius),
    0x3f49e987: ('vertical_release_factor', _decode_vertical_release_factor),
    0x3a5ab398: ('angle_dampen_factor', _decode_angle_dampen_factor),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x1a758434: ('gravity_dampen_factor', _decode_gravity_dampen_factor),
    0x46dd38f: ('climb_up_max_speed', _decode_climb_up_max_speed),
    0x41fdbb9a: ('climb_up_acceleration', _decode_climb_up_acceleration),
    0xa86c031f: ('climb_down_max_speed', _decode_climb_down_max_speed),
    0xb74fb18c: ('climb_down_acceleration', _decode_climb_down_acceleration),
    0xdffaba3e: ('climb_dampen_factor', _decode_climb_dampen_factor),
    0xda5d67b1: ('climb_analog_degrees_from_vertical', _decode_climb_analog_degrees_from_vertical),
    0x393d1a4e: ('grab_boost', _decode_grab_boost),
    0xd32ccf88: ('time_between_grabs', _decode_time_between_grabs),
    0x22c57f64: ('time_to_disable_on_scripted_release', _decode_time_to_disable_on_scripted_release),
    0xde816bd4: ('stall_angle_threshold', _decode_stall_angle_threshold),
    0x34bc736b: ('auto_swing_release_velocity_x', _decode_auto_swing_release_velocity_x),
    0xfca1b4fa: ('auto_swing_jump_velocity_x', _decode_auto_swing_jump_velocity_x),
    0xb83fec12: ('auto_swing_jump_vertical_velocity', _decode_auto_swing_jump_vertical_velocity),
}
