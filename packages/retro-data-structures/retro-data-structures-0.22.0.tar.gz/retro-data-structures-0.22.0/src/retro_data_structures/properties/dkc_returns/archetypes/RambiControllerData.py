# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class RambiControllerData(BaseProperty):
    flee_speed_percentage: float = dataclasses.field(default=50.0)
    maintain_direction_time: float = dataclasses.field(default=2.0)
    off_screen_turn_around_distance: float = dataclasses.field(default=3.0)
    despawn_timer: float = dataclasses.field(default=10.0)
    despawn_distance: float = dataclasses.field(default=15.0)
    far_despawn_distance: float = dataclasses.field(default=25.0)

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

        data.write(b'\x04\x9b\xfc\x1b')  # 0x49bfc1b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flee_speed_percentage))

        data.write(b'Df\x01n')  # 0x4466016e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maintain_direction_time))

        data.write(b'\x7f\xf6\xb0\x94')  # 0x7ff6b094
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.off_screen_turn_around_distance))

        data.write(b'\xbc/\x0bA')  # 0xbc2f0b41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.despawn_timer))

        data.write(b'\xe7eV(')  # 0xe7655628
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.despawn_distance))

        data.write(b'\xeb\xe0,\xd7')  # 0xebe02cd7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.far_despawn_distance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flee_speed_percentage=data['flee_speed_percentage'],
            maintain_direction_time=data['maintain_direction_time'],
            off_screen_turn_around_distance=data['off_screen_turn_around_distance'],
            despawn_timer=data['despawn_timer'],
            despawn_distance=data['despawn_distance'],
            far_despawn_distance=data['far_despawn_distance'],
        )

    def to_json(self) -> dict:
        return {
            'flee_speed_percentage': self.flee_speed_percentage,
            'maintain_direction_time': self.maintain_direction_time,
            'off_screen_turn_around_distance': self.off_screen_turn_around_distance,
            'despawn_timer': self.despawn_timer,
            'despawn_distance': self.despawn_distance,
            'far_despawn_distance': self.far_despawn_distance,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x49bfc1b, 0x4466016e, 0x7ff6b094, 0xbc2f0b41, 0xe7655628, 0xebe02cd7)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[RambiControllerData]:
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

    return RambiControllerData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_flee_speed_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maintain_direction_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_off_screen_turn_around_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_despawn_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_despawn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_far_despawn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x49bfc1b: ('flee_speed_percentage', _decode_flee_speed_percentage),
    0x4466016e: ('maintain_direction_time', _decode_maintain_direction_time),
    0x7ff6b094: ('off_screen_turn_around_distance', _decode_off_screen_turn_around_distance),
    0xbc2f0b41: ('despawn_timer', _decode_despawn_timer),
    0xe7655628: ('despawn_distance', _decode_despawn_distance),
    0xebe02cd7: ('far_despawn_distance', _decode_far_despawn_distance),
}
