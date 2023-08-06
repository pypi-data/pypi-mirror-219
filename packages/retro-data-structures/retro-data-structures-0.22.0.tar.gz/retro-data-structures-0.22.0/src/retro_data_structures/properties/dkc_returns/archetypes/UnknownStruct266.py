# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct266(BaseProperty):
    max_impulse_speed: float = dataclasses.field(default=0.0)
    acceleration: float = dataclasses.field(default=0.0)
    duration: float = dataclasses.field(default=0.0)
    cool_down_deceleration: float = dataclasses.field(default=0.0)
    passive_deceleration: float = dataclasses.field(default=0.0)
    max_passive_speed: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xecF\x16\x86')  # 0xec461686
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_impulse_speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'\xa4\xb2\xd2x')  # 0xa4b2d278
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cool_down_deceleration))

        data.write(b'\x81\x17\r!')  # 0x81170d21
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.passive_deceleration))

        data.write(b'Q\xb0="')  # 0x51b03d22
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_passive_speed))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            max_impulse_speed=data['max_impulse_speed'],
            acceleration=data['acceleration'],
            duration=data['duration'],
            cool_down_deceleration=data['cool_down_deceleration'],
            passive_deceleration=data['passive_deceleration'],
            max_passive_speed=data['max_passive_speed'],
        )

    def to_json(self) -> dict:
        return {
            'max_impulse_speed': self.max_impulse_speed,
            'acceleration': self.acceleration,
            'duration': self.duration,
            'cool_down_deceleration': self.cool_down_deceleration,
            'passive_deceleration': self.passive_deceleration,
            'max_passive_speed': self.max_passive_speed,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xec461686, 0x39fb7978, 0x8b51e23f, 0xa4b2d278, 0x81170d21, 0x51b03d22)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct266]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(60))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct266(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_max_impulse_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cool_down_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_passive_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_passive_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xec461686: ('max_impulse_speed', _decode_max_impulse_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x8b51e23f: ('duration', _decode_duration),
    0xa4b2d278: ('cool_down_deceleration', _decode_cool_down_deceleration),
    0x81170d21: ('passive_deceleration', _decode_passive_deceleration),
    0x51b03d22: ('max_passive_speed', _decode_max_passive_speed),
}
