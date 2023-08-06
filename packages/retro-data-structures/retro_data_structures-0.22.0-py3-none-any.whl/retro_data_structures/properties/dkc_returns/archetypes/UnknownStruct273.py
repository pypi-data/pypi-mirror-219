# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct273(BaseProperty):
    unknown_0x0eafc768: int = dataclasses.field(default=1)
    unknown_0x03223140: int = dataclasses.field(default=1)

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

        data.write(b'\x0e\xaf\xc7h')  # 0xeafc768
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x0eafc768))

        data.write(b'\x03"1@')  # 0x3223140
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x03223140))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x0eafc768=data['unknown_0x0eafc768'],
            unknown_0x03223140=data['unknown_0x03223140'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x0eafc768': self.unknown_0x0eafc768,
            'unknown_0x03223140': self.unknown_0x03223140,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xeafc768, 0x3223140)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct273]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(20))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct273(
        dec[2],
        dec[5],
    )


def _decode_unknown_0x0eafc768(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x03223140(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xeafc768: ('unknown_0x0eafc768', _decode_unknown_0x0eafc768),
    0x3223140: ('unknown_0x03223140', _decode_unknown_0x03223140),
}
