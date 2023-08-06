# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class VelocityConvergence(BaseProperty):
    max_speed: float = dataclasses.field(default=0.0)
    acceleration: float = dataclasses.field(default=0.0)
    dampening_range: float = dataclasses.field(default=1.0)

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

        data.write(b'\x82\xdb\x0c\xbe')  # 0x82db0cbe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x1a\x11\x17%')  # 0x1a111725
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dampening_range))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            max_speed=data['max_speed'],
            acceleration=data['acceleration'],
            dampening_range=data['dampening_range'],
        )

    def to_json(self) -> dict:
        return {
            'max_speed': self.max_speed,
            'acceleration': self.acceleration,
            'dampening_range': self.dampening_range,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x82db0cbe, 0x39fb7978, 0x1a111725)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[VelocityConvergence]:
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

    return VelocityConvergence(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dampening_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x82db0cbe: ('max_speed', _decode_max_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x1a111725: ('dampening_range', _decode_dampening_range),
}
