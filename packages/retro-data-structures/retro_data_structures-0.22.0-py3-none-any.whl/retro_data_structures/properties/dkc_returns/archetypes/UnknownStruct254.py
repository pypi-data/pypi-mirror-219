# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct254(BaseProperty):
    unknown_0xa35a8599: bool = dataclasses.field(default=False)
    unknown_0xf8677de6: bool = dataclasses.field(default=False)
    fully_pressed: float = dataclasses.field(default=1.0)
    unknown_0x9fb991fe: float = dataclasses.field(default=0.5)
    unknown_0xf12d036b: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xa3Z\x85\x99')  # 0xa35a8599
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa35a8599))

        data.write(b'\xf8g}\xe6')  # 0xf8677de6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf8677de6))

        data.write(b'\xf6\xb9\xa61')  # 0xf6b9a631
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fully_pressed))

        data.write(b'\x9f\xb9\x91\xfe')  # 0x9fb991fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9fb991fe))

        data.write(b'\xf1-\x03k')  # 0xf12d036b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf12d036b))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xa35a8599=data['unknown_0xa35a8599'],
            unknown_0xf8677de6=data['unknown_0xf8677de6'],
            fully_pressed=data['fully_pressed'],
            unknown_0x9fb991fe=data['unknown_0x9fb991fe'],
            unknown_0xf12d036b=data['unknown_0xf12d036b'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xa35a8599': self.unknown_0xa35a8599,
            'unknown_0xf8677de6': self.unknown_0xf8677de6,
            'fully_pressed': self.fully_pressed,
            'unknown_0x9fb991fe': self.unknown_0x9fb991fe,
            'unknown_0xf12d036b': self.unknown_0xf12d036b,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xa35a8599, 0xf8677de6, 0xf6b9a631, 0x9fb991fe, 0xf12d036b)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct254]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(44))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct254(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_unknown_0xa35a8599(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf8677de6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fully_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9fb991fe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf12d036b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa35a8599: ('unknown_0xa35a8599', _decode_unknown_0xa35a8599),
    0xf8677de6: ('unknown_0xf8677de6', _decode_unknown_0xf8677de6),
    0xf6b9a631: ('fully_pressed', _decode_fully_pressed),
    0x9fb991fe: ('unknown_0x9fb991fe', _decode_unknown_0x9fb991fe),
    0xf12d036b: ('unknown_0xf12d036b', _decode_unknown_0xf12d036b),
}
