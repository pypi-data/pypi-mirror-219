# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerMovementParameters(BaseProperty):
    minimum_walk_speed: float = dataclasses.field(default=1.0)
    maximum_run_speed: float = dataclasses.field(default=9.0)
    acceleration: float = dataclasses.field(default=20.0)

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

        data.write(b'\x1f\xf7\x90`')  # 0x1ff79060
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_walk_speed))

        data.write(b'\x95\n{\x96')  # 0x950a7b96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_run_speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            minimum_walk_speed=data['minimum_walk_speed'],
            maximum_run_speed=data['maximum_run_speed'],
            acceleration=data['acceleration'],
        )

    def to_json(self) -> dict:
        return {
            'minimum_walk_speed': self.minimum_walk_speed,
            'maximum_run_speed': self.maximum_run_speed,
            'acceleration': self.acceleration,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x1ff79060, 0x950a7b96, 0x39fb7978)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerMovementParameters]:
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

    return PlayerMovementParameters(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_minimum_walk_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_run_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1ff79060: ('minimum_walk_speed', _decode_minimum_walk_speed),
    0x950a7b96: ('maximum_run_speed', _decode_maximum_run_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
}
