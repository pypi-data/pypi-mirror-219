# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct270(BaseProperty):
    allow_ground_pound: bool = dataclasses.field(default=False)
    allow_peanut_gun: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xbdERd')  # 0xbd455264
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_ground_pound))

        data.write(b'\xd1\x14\xb7]')  # 0xd114b75d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_peanut_gun))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            allow_ground_pound=data['allow_ground_pound'],
            allow_peanut_gun=data['allow_peanut_gun'],
        )

    def to_json(self) -> dict:
        return {
            'allow_ground_pound': self.allow_ground_pound,
            'allow_peanut_gun': self.allow_peanut_gun,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xbd455264, 0xd114b75d)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct270]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(14))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct270(
        dec[2],
        dec[5],
    )


def _decode_allow_ground_pound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_peanut_gun(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbd455264: ('allow_ground_pound', _decode_allow_ground_pound),
    0xd114b75d: ('allow_peanut_gun', _decode_allow_peanut_gun),
}
