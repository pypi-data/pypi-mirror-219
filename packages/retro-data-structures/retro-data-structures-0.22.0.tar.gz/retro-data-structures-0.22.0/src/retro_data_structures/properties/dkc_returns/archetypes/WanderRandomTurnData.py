# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class WanderRandomTurnData(BaseProperty):
    min_time_till_turn: float = dataclasses.field(default=2.0)
    max_time_till_turn: float = dataclasses.field(default=5.0)
    time_to_disable_turn_after_collision: float = dataclasses.field(default=4.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'3\x9c\xf3\x14')  # 0x339cf314
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_time_till_turn))

        data.write(b'\x1a\xe2\x0e\x0c')  # 0x1ae20e0c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_time_till_turn))

        data.write(b'T\xd6\\\xdc')  # 0x54d65cdc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_to_disable_turn_after_collision))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            min_time_till_turn=data['min_time_till_turn'],
            max_time_till_turn=data['max_time_till_turn'],
            time_to_disable_turn_after_collision=data['time_to_disable_turn_after_collision'],
        )

    def to_json(self) -> dict:
        return {
            'min_time_till_turn': self.min_time_till_turn,
            'max_time_till_turn': self.max_time_till_turn,
            'time_to_disable_turn_after_collision': self.time_to_disable_turn_after_collision,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x339cf314, 0x1ae20e0c, 0x54d65cdc)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[WanderRandomTurnData]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return WanderRandomTurnData(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_min_time_till_turn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_time_till_turn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_to_disable_turn_after_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x339cf314: ('min_time_till_turn', _decode_min_time_till_turn),
    0x1ae20e0c: ('max_time_till_turn', _decode_max_time_till_turn),
    0x54d65cdc: ('time_to_disable_turn_after_collision', _decode_time_to_disable_turn_after_collision),
}
