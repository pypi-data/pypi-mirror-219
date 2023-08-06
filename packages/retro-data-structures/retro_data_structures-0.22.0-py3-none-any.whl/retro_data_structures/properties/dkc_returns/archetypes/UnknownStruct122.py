# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct122(BaseProperty):
    unknown_0x9aebebc8: int = dataclasses.field(default=2036438260)  # Choice
    unknown_0x9af3fd16: bool = dataclasses.field(default=False)
    unknown_0x314c7ce4: float = dataclasses.field(default=1.0)
    unknown_0x74367d95: int = dataclasses.field(default=1)
    mechanoid_delta_rate: float = dataclasses.field(default=2.0)

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

        data.write(b'\x9a\xeb\xeb\xc8')  # 0x9aebebc8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x9aebebc8))

        data.write(b'\x9a\xf3\xfd\x16')  # 0x9af3fd16
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9af3fd16))

        data.write(b'1L|\xe4')  # 0x314c7ce4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x314c7ce4))

        data.write(b't6}\x95')  # 0x74367d95
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x74367d95))

        data.write(b'r\x173i')  # 0x72173369
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mechanoid_delta_rate))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x9aebebc8=data['unknown_0x9aebebc8'],
            unknown_0x9af3fd16=data['unknown_0x9af3fd16'],
            unknown_0x314c7ce4=data['unknown_0x314c7ce4'],
            unknown_0x74367d95=data['unknown_0x74367d95'],
            mechanoid_delta_rate=data['mechanoid_delta_rate'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x9aebebc8': self.unknown_0x9aebebc8,
            'unknown_0x9af3fd16': self.unknown_0x9af3fd16,
            'unknown_0x314c7ce4': self.unknown_0x314c7ce4,
            'unknown_0x74367d95': self.unknown_0x74367d95,
            'mechanoid_delta_rate': self.mechanoid_delta_rate,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x9aebebc8, 0x9af3fd16, 0x314c7ce4, 0x74367d95, 0x72173369)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct122]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLH?LHfLHlLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(47))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct122(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_unknown_0x9aebebc8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x9af3fd16(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x314c7ce4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x74367d95(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mechanoid_delta_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9aebebc8: ('unknown_0x9aebebc8', _decode_unknown_0x9aebebc8),
    0x9af3fd16: ('unknown_0x9af3fd16', _decode_unknown_0x9af3fd16),
    0x314c7ce4: ('unknown_0x314c7ce4', _decode_unknown_0x314c7ce4),
    0x74367d95: ('unknown_0x74367d95', _decode_unknown_0x74367d95),
    0x72173369: ('mechanoid_delta_rate', _decode_mechanoid_delta_rate),
}
