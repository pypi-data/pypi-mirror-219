# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct204(BaseProperty):
    unknown_0xdfd9aa56: int = dataclasses.field(default=1)
    unknown_0xda21386f: float = dataclasses.field(default=2.0)
    unknown_0x5cb54ac1: float = dataclasses.field(default=2.0)
    unknown_0x97e99964: float = dataclasses.field(default=2.0)
    unknown_0x63bdd01f: int = dataclasses.field(default=0)
    unknown_0x71087ff1: int = dataclasses.field(default=3)
    unknown_0xc9b41894: int = dataclasses.field(default=6)
    unknown_0x004297b4: bool = dataclasses.field(default=False)
    unknown_0xa055a56f: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xdf\xd9\xaaV')  # 0xdfd9aa56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xdfd9aa56))

        data.write(b'\xda!8o')  # 0xda21386f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xda21386f))

        data.write(b'\\\xb5J\xc1')  # 0x5cb54ac1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5cb54ac1))

        data.write(b'\x97\xe9\x99d')  # 0x97e99964
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x97e99964))

        data.write(b'c\xbd\xd0\x1f')  # 0x63bdd01f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x63bdd01f))

        data.write(b'q\x08\x7f\xf1')  # 0x71087ff1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x71087ff1))

        data.write(b'\xc9\xb4\x18\x94')  # 0xc9b41894
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc9b41894))

        data.write(b'\x00B\x97\xb4')  # 0x4297b4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x004297b4))

        data.write(b'\xa0U\xa5o')  # 0xa055a56f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa055a56f))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xdfd9aa56=data['unknown_0xdfd9aa56'],
            unknown_0xda21386f=data['unknown_0xda21386f'],
            unknown_0x5cb54ac1=data['unknown_0x5cb54ac1'],
            unknown_0x97e99964=data['unknown_0x97e99964'],
            unknown_0x63bdd01f=data['unknown_0x63bdd01f'],
            unknown_0x71087ff1=data['unknown_0x71087ff1'],
            unknown_0xc9b41894=data['unknown_0xc9b41894'],
            unknown_0x004297b4=data['unknown_0x004297b4'],
            unknown_0xa055a56f=data['unknown_0xa055a56f'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xdfd9aa56': self.unknown_0xdfd9aa56,
            'unknown_0xda21386f': self.unknown_0xda21386f,
            'unknown_0x5cb54ac1': self.unknown_0x5cb54ac1,
            'unknown_0x97e99964': self.unknown_0x97e99964,
            'unknown_0x63bdd01f': self.unknown_0x63bdd01f,
            'unknown_0x71087ff1': self.unknown_0x71087ff1,
            'unknown_0xc9b41894': self.unknown_0xc9b41894,
            'unknown_0x004297b4': self.unknown_0x004297b4,
            'unknown_0xa055a56f': self.unknown_0xa055a56f,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xdfd9aa56, 0xda21386f, 0x5cb54ac1, 0x97e99964, 0x63bdd01f, 0x71087ff1, 0xc9b41894, 0x4297b4, 0xa055a56f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct204]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHlLHlLHlLH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(84))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct204(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
    )


def _decode_unknown_0xdfd9aa56(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xda21386f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5cb54ac1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x97e99964(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x63bdd01f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x71087ff1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc9b41894(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x004297b4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa055a56f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdfd9aa56: ('unknown_0xdfd9aa56', _decode_unknown_0xdfd9aa56),
    0xda21386f: ('unknown_0xda21386f', _decode_unknown_0xda21386f),
    0x5cb54ac1: ('unknown_0x5cb54ac1', _decode_unknown_0x5cb54ac1),
    0x97e99964: ('unknown_0x97e99964', _decode_unknown_0x97e99964),
    0x63bdd01f: ('unknown_0x63bdd01f', _decode_unknown_0x63bdd01f),
    0x71087ff1: ('unknown_0x71087ff1', _decode_unknown_0x71087ff1),
    0xc9b41894: ('unknown_0xc9b41894', _decode_unknown_0xc9b41894),
    0x4297b4: ('unknown_0x004297b4', _decode_unknown_0x004297b4),
    0xa055a56f: ('unknown_0xa055a56f', _decode_unknown_0xa055a56f),
}
