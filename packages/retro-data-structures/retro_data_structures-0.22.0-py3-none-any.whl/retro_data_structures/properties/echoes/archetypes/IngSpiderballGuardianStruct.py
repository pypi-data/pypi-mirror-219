# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class IngSpiderballGuardianStruct(BaseProperty):
    min_patrol_speed: float = dataclasses.field(default=5.0)
    max_patrol_speed: float = dataclasses.field(default=10.0)
    linear_acceleration: float = dataclasses.field(default=7.0)
    angular_speed: float = dataclasses.field(default=720.0)
    unknown: float = dataclasses.field(default=40.0)
    stunned_speed: float = dataclasses.field(default=2.0)
    stunned_time: float = dataclasses.field(default=25.0)
    max_charge_time: float = dataclasses.field(default=15.0)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x17\xc5\xb6\x1d')  # 0x17c5b61d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_patrol_speed))

        data.write(b'\xb0\xf16d')  # 0xb0f13664
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_patrol_speed))

        data.write(b'\xaf\x9b\x05\xf4')  # 0xaf9b05f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.linear_acceleration))

        data.write(b'\xbc\xd73?')  # 0xbcd7333f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.angular_speed))

        data.write(b'\xd1\xd9\xd8\xbd')  # 0xd1d9d8bd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\x8dY\x17\xd4')  # 0x8d5917d4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stunned_speed))

        data.write(b'\x81\x05\xec\xfd')  # 0x8105ecfd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stunned_time))

        data.write(b'\xe5\x06^\xa8')  # 0xe5065ea8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_charge_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            min_patrol_speed=data['min_patrol_speed'],
            max_patrol_speed=data['max_patrol_speed'],
            linear_acceleration=data['linear_acceleration'],
            angular_speed=data['angular_speed'],
            unknown=data['unknown'],
            stunned_speed=data['stunned_speed'],
            stunned_time=data['stunned_time'],
            max_charge_time=data['max_charge_time'],
        )

    def to_json(self) -> dict:
        return {
            'min_patrol_speed': self.min_patrol_speed,
            'max_patrol_speed': self.max_patrol_speed,
            'linear_acceleration': self.linear_acceleration,
            'angular_speed': self.angular_speed,
            'unknown': self.unknown,
            'stunned_speed': self.stunned_speed,
            'stunned_time': self.stunned_time,
            'max_charge_time': self.max_charge_time,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x17c5b61d, 0xb0f13664, 0xaf9b05f4, 0xbcd7333f, 0xd1d9d8bd, 0x8d5917d4, 0x8105ecfd, 0xe5065ea8)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[IngSpiderballGuardianStruct]:
    if property_count != 8:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(80))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) != _FAST_IDS:
        data.seek(before)
        return None

    return IngSpiderballGuardianStruct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
    )


def _decode_min_patrol_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_patrol_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_linear_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_angular_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stunned_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stunned_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_charge_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x17c5b61d: ('min_patrol_speed', _decode_min_patrol_speed),
    0xb0f13664: ('max_patrol_speed', _decode_max_patrol_speed),
    0xaf9b05f4: ('linear_acceleration', _decode_linear_acceleration),
    0xbcd7333f: ('angular_speed', _decode_angular_speed),
    0xd1d9d8bd: ('unknown', _decode_unknown),
    0x8d5917d4: ('stunned_speed', _decode_stunned_speed),
    0x8105ecfd: ('stunned_time', _decode_stunned_time),
    0xe5065ea8: ('max_charge_time', _decode_max_charge_time),
}
