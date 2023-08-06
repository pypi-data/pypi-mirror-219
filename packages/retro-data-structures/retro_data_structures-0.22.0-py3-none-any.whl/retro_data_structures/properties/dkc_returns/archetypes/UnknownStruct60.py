# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class UnknownStruct60(BaseProperty):
    swoop_direction: enums.SwoopDirection = dataclasses.field(default=enums.SwoopDirection.Unknown1)
    type: enums.UnknownEnum4 = dataclasses.field(default=enums.UnknownEnum4.Unknown1)

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

        data.write(b'\x13\xd7\x0bg')  # 0x13d70b67
        data.write(b'\x00\x04')  # size
        self.swoop_direction.to_stream(data)

        data.write(b'GK\xcc\xe3')  # 0x474bcce3
        data.write(b'\x00\x04')  # size
        self.type.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            swoop_direction=enums.SwoopDirection.from_json(data['swoop_direction']),
            type=enums.UnknownEnum4.from_json(data['type']),
        )

    def to_json(self) -> dict:
        return {
            'swoop_direction': self.swoop_direction.to_json(),
            'type': self.type.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x13d70b67, 0x474bcce3)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct60]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct60(
        enums.SwoopDirection(dec[2]),
        enums.UnknownEnum4(dec[5]),
    )


def _decode_swoop_direction(data: typing.BinaryIO, property_size: int):
    return enums.SwoopDirection.from_stream(data)


def _decode_type(data: typing.BinaryIO, property_size: int):
    return enums.UnknownEnum4.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x13d70b67: ('swoop_direction', _decode_swoop_direction),
    0x474bcce3: ('type', _decode_type),
}
