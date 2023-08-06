# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class HurlHeightRules(BaseProperty):
    number_of_hurl_heights: int = dataclasses.field(default=0)
    hurl_height1: float = dataclasses.field(default=1.0)
    hurl_height2: float = dataclasses.field(default=2.0)
    hurl_height3: float = dataclasses.field(default=3.0)
    hurl_height4: float = dataclasses.field(default=4.0)
    hurl_height5: float = dataclasses.field(default=5.0)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'!\x87\xc1~')  # 0x2187c17e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_hurl_heights))

        data.write(b'=.\xa7`')  # 0x3d2ea760
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height1))

        data.write(b'\xbb\xba\xd5\xce')  # 0xbbbad5ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height2))

        data.write(b'p\xe6\x06k')  # 0x70e6066b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height3))

        data.write(b'm\xe36\xd3')  # 0x6de336d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height4))

        data.write(b'\xa6\xbf\xe5v')  # 0xa6bfe576
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hurl_height5))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            number_of_hurl_heights=data['number_of_hurl_heights'],
            hurl_height1=data['hurl_height1'],
            hurl_height2=data['hurl_height2'],
            hurl_height3=data['hurl_height3'],
            hurl_height4=data['hurl_height4'],
            hurl_height5=data['hurl_height5'],
        )

    def to_json(self) -> dict:
        return {
            'number_of_hurl_heights': self.number_of_hurl_heights,
            'hurl_height1': self.hurl_height1,
            'hurl_height2': self.hurl_height2,
            'hurl_height3': self.hurl_height3,
            'hurl_height4': self.hurl_height4,
            'hurl_height5': self.hurl_height5,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x2187c17e, 0x3d2ea760, 0xbbbad5ce, 0x70e6066b, 0x6de336d3, 0xa6bfe576)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[HurlHeightRules]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(60))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return HurlHeightRules(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_number_of_hurl_heights(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_hurl_height1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hurl_height5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2187c17e: ('number_of_hurl_heights', _decode_number_of_hurl_heights),
    0x3d2ea760: ('hurl_height1', _decode_hurl_height1),
    0xbbbad5ce: ('hurl_height2', _decode_hurl_height2),
    0x70e6066b: ('hurl_height3', _decode_hurl_height3),
    0x6de336d3: ('hurl_height4', _decode_hurl_height4),
    0xa6bfe576: ('hurl_height5', _decode_hurl_height5),
}
