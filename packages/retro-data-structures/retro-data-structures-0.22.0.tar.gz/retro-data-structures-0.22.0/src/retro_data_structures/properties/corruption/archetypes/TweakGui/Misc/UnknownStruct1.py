# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct1(BaseProperty):
    unknown_0xe7c4becd: float = dataclasses.field(default=0.5)
    unknown_0xbaa1b7c1: float = dataclasses.field(default=0.5)
    unknown_0x3b8d9a8e: float = dataclasses.field(default=2.0)
    unknown_0xbd735f69: float = dataclasses.field(default=4.0)
    unknown_0x5ad522c2: float = dataclasses.field(default=0.25)
    unknown_0x4358b0f1: float = dataclasses.field(default=2.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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

        data.write(b'\xe7\xc4\xbe\xcd')  # 0xe7c4becd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe7c4becd))

        data.write(b'\xba\xa1\xb7\xc1')  # 0xbaa1b7c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbaa1b7c1))

        data.write(b';\x8d\x9a\x8e')  # 0x3b8d9a8e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3b8d9a8e))

        data.write(b'\xbds_i')  # 0xbd735f69
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbd735f69))

        data.write(b'Z\xd5"\xc2')  # 0x5ad522c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5ad522c2))

        data.write(b'CX\xb0\xf1')  # 0x4358b0f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4358b0f1))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xe7c4becd=data['unknown_0xe7c4becd'],
            unknown_0xbaa1b7c1=data['unknown_0xbaa1b7c1'],
            unknown_0x3b8d9a8e=data['unknown_0x3b8d9a8e'],
            unknown_0xbd735f69=data['unknown_0xbd735f69'],
            unknown_0x5ad522c2=data['unknown_0x5ad522c2'],
            unknown_0x4358b0f1=data['unknown_0x4358b0f1'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xe7c4becd': self.unknown_0xe7c4becd,
            'unknown_0xbaa1b7c1': self.unknown_0xbaa1b7c1,
            'unknown_0x3b8d9a8e': self.unknown_0x3b8d9a8e,
            'unknown_0xbd735f69': self.unknown_0xbd735f69,
            'unknown_0x5ad522c2': self.unknown_0x5ad522c2,
            'unknown_0x4358b0f1': self.unknown_0x4358b0f1,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xe7c4becd, 0xbaa1b7c1, 0x3b8d9a8e, 0xbd735f69, 0x5ad522c2, 0x4358b0f1)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct1]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(60))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct1(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_unknown_0xe7c4becd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbaa1b7c1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3b8d9a8e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbd735f69(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5ad522c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4358b0f1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe7c4becd: ('unknown_0xe7c4becd', _decode_unknown_0xe7c4becd),
    0xbaa1b7c1: ('unknown_0xbaa1b7c1', _decode_unknown_0xbaa1b7c1),
    0x3b8d9a8e: ('unknown_0x3b8d9a8e', _decode_unknown_0x3b8d9a8e),
    0xbd735f69: ('unknown_0xbd735f69', _decode_unknown_0xbd735f69),
    0x5ad522c2: ('unknown_0x5ad522c2', _decode_unknown_0x5ad522c2),
    0x4358b0f1: ('unknown_0x4358b0f1', _decode_unknown_0x4358b0f1),
}
