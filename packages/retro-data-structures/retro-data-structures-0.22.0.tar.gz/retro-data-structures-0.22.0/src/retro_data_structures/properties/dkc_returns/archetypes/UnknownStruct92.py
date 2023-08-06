# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct92(BaseProperty):
    unknown: bool = dataclasses.field(default=True)
    auto_start_light: bool = dataclasses.field(default=True)

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

        data.write(b'](\x96\x13')  # 0x5d289613
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\xae\xdf\xa0\x91')  # 0xaedfa091
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start_light))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            auto_start_light=data['auto_start_light'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'auto_start_light': self.auto_start_light,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x5d289613, 0xaedfa091)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct92]:
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

    return UnknownStruct92(
        dec[2],
        dec[5],
    )


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start_light(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5d289613: ('unknown', _decode_unknown),
    0xaedfa091: ('auto_start_light', _decode_auto_start_light),
}
