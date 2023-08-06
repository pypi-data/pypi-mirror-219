# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct14(BaseProperty):
    view_point: float = dataclasses.field(default=0.0)
    unknown_0x81dc0c16: bool = dataclasses.field(default=False)
    unknown_0x2257ae80: float = dataclasses.field(default=0.0)

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

        data.write(b'\xae\xd4(\x87')  # 0xaed42887
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.view_point))

        data.write(b'\x81\xdc\x0c\x16')  # 0x81dc0c16
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x81dc0c16))

        data.write(b'"W\xae\x80')  # 0x2257ae80
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2257ae80))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            view_point=data['view_point'],
            unknown_0x81dc0c16=data['unknown_0x81dc0c16'],
            unknown_0x2257ae80=data['unknown_0x2257ae80'],
        )

    def to_json(self) -> dict:
        return {
            'view_point': self.view_point,
            'unknown_0x81dc0c16': self.unknown_0x81dc0c16,
            'unknown_0x2257ae80': self.unknown_0x2257ae80,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xaed42887, 0x81dc0c16, 0x2257ae80)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct14]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLH?LHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(27))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct14(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_view_point(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x81dc0c16(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x2257ae80(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xaed42887: ('view_point', _decode_view_point),
    0x81dc0c16: ('unknown_0x81dc0c16', _decode_unknown_0x81dc0c16),
    0x2257ae80: ('unknown_0x2257ae80', _decode_unknown_0x2257ae80),
}
