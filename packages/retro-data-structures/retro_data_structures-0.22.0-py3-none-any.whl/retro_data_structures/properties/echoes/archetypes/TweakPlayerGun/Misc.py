# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Misc(BaseProperty):
    up_look_angle: float = dataclasses.field(default=22.0)
    down_look_angle: float = dataclasses.field(default=0.0)
    vertical_spread: float = dataclasses.field(default=7.0)
    horizontal_spread: float = dataclasses.field(default=7.0)
    high_vertical_spread: float = dataclasses.field(default=7.0)
    high_horizontal_spread: float = dataclasses.field(default=7.0)
    low_vertical_spread: float = dataclasses.field(default=7.0)
    low_horizontal_spread: float = dataclasses.field(default=7.0)
    aim_vertical_speed: float = dataclasses.field(default=4.0)
    aim_horizontal_speed: float = dataclasses.field(default=10.0)
    hologram_display_time: float = dataclasses.field(default=0.0625)
    gun_transform_time: float = dataclasses.field(default=0.25)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\xe8\xbb~<')  # 0xe8bb7e3c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.up_look_angle))

        data.write(b'^\xd7\xe0\xbd')  # 0x5ed7e0bd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.down_look_angle))

        data.write(b'\x84*\xe0\xb4')  # 0x842ae0b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_spread))

        data.write(b'\x8c)\xe9\x1c')  # 0x8c29e91c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_spread))

        data.write(b'}Zl\x93')  # 0x7d5a6c93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.high_vertical_spread))

        data.write(b'\xb2\xe2m\x02')  # 0xb2e26d02
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.high_horizontal_spread))

        data.write(b'\xd8\x1d\x14P')  # 0xd81d1450
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.low_vertical_spread))

        data.write(b'\x0c\xeb\xb5\xc6')  # 0xcebb5c6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.low_horizontal_spread))

        data.write(b'\x90L\xd4\x9d')  # 0x904cd49d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aim_vertical_speed))

        data.write(b'\xfc\xcd\xdb\x00')  # 0xfccddb00
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aim_horizontal_speed))

        data.write(b'\xf3U\xd0u')  # 0xf355d075
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hologram_display_time))

        data.write(b'\x92b\xa7"')  # 0x9262a722
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gun_transform_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            up_look_angle=data['up_look_angle'],
            down_look_angle=data['down_look_angle'],
            vertical_spread=data['vertical_spread'],
            horizontal_spread=data['horizontal_spread'],
            high_vertical_spread=data['high_vertical_spread'],
            high_horizontal_spread=data['high_horizontal_spread'],
            low_vertical_spread=data['low_vertical_spread'],
            low_horizontal_spread=data['low_horizontal_spread'],
            aim_vertical_speed=data['aim_vertical_speed'],
            aim_horizontal_speed=data['aim_horizontal_speed'],
            hologram_display_time=data['hologram_display_time'],
            gun_transform_time=data['gun_transform_time'],
        )

    def to_json(self) -> dict:
        return {
            'up_look_angle': self.up_look_angle,
            'down_look_angle': self.down_look_angle,
            'vertical_spread': self.vertical_spread,
            'horizontal_spread': self.horizontal_spread,
            'high_vertical_spread': self.high_vertical_spread,
            'high_horizontal_spread': self.high_horizontal_spread,
            'low_vertical_spread': self.low_vertical_spread,
            'low_horizontal_spread': self.low_horizontal_spread,
            'aim_vertical_speed': self.aim_vertical_speed,
            'aim_horizontal_speed': self.aim_horizontal_speed,
            'hologram_display_time': self.hologram_display_time,
            'gun_transform_time': self.gun_transform_time,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xe8bb7e3c, 0x5ed7e0bd, 0x842ae0b4, 0x8c29e91c, 0x7d5a6c93, 0xb2e26d02, 0xd81d1450, 0xcebb5c6, 0x904cd49d, 0xfccddb00, 0xf355d075, 0x9262a722)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Misc]:
    if property_count != 12:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(120))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33]) != _FAST_IDS:
        data.seek(before)
        return None

    return Misc(
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
    )


def _decode_up_look_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_down_look_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vertical_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horizontal_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_high_vertical_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_high_horizontal_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_low_vertical_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_low_horizontal_spread(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_aim_vertical_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_aim_horizontal_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hologram_display_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gun_transform_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe8bb7e3c: ('up_look_angle', _decode_up_look_angle),
    0x5ed7e0bd: ('down_look_angle', _decode_down_look_angle),
    0x842ae0b4: ('vertical_spread', _decode_vertical_spread),
    0x8c29e91c: ('horizontal_spread', _decode_horizontal_spread),
    0x7d5a6c93: ('high_vertical_spread', _decode_high_vertical_spread),
    0xb2e26d02: ('high_horizontal_spread', _decode_high_horizontal_spread),
    0xd81d1450: ('low_vertical_spread', _decode_low_vertical_spread),
    0xcebb5c6: ('low_horizontal_spread', _decode_low_horizontal_spread),
    0x904cd49d: ('aim_vertical_speed', _decode_aim_vertical_speed),
    0xfccddb00: ('aim_horizontal_speed', _decode_aim_horizontal_speed),
    0xf355d075: ('hologram_display_time', _decode_hologram_display_time),
    0x9262a722: ('gun_transform_time', _decode_gun_transform_time),
}
