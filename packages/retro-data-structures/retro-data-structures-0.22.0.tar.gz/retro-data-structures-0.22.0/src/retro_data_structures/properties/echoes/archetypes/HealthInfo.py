# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class HealthInfo(BaseProperty):
    health: float = dataclasses.field(default=5.0)
    hi_knock_back_resistance: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xf0f\x89\x19')  # 0xf0668919
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.health))

        data.write(b':-\x17\xe4')  # 0x3a2d17e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hi_knock_back_resistance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            health=data['health'],
            hi_knock_back_resistance=data['hi_knock_back_resistance'],
        )

    def to_json(self) -> dict:
        return {
            'health': self.health,
            'hi_knock_back_resistance': self.hi_knock_back_resistance,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xf0668919, 0x3a2d17e4)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[HealthInfo]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return HealthInfo(
        dec[2],
        dec[5],
    )


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hi_knock_back_resistance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf0668919: ('health', _decode_health),
    0x3a2d17e4: ('hi_knock_back_resistance', _decode_hi_knock_back_resistance),
}
