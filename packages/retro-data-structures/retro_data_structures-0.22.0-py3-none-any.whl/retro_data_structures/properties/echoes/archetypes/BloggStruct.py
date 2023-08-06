# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class BloggStruct(BaseProperty):
    unknown_0x3e505ddb: int = dataclasses.field(default=0)
    unknown_0x118f1e46: int = dataclasses.field(default=0)
    unknown_0x6e603df2: float = dataclasses.field(default=0.0)
    unknown_0x1e74f1ec: float = dataclasses.field(default=0.0)
    unknown_0xecba9fb2: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'>P]\xdb')  # 0x3e505ddb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x3e505ddb))

        data.write(b'\x11\x8f\x1eF')  # 0x118f1e46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x118f1e46))

        data.write(b'n`=\xf2')  # 0x6e603df2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6e603df2))

        data.write(b'\x1et\xf1\xec')  # 0x1e74f1ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1e74f1ec))

        data.write(b'\xec\xba\x9f\xb2')  # 0xecba9fb2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xecba9fb2))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x3e505ddb=data['unknown_0x3e505ddb'],
            unknown_0x118f1e46=data['unknown_0x118f1e46'],
            unknown_0x6e603df2=data['unknown_0x6e603df2'],
            unknown_0x1e74f1ec=data['unknown_0x1e74f1ec'],
            unknown_0xecba9fb2=data['unknown_0xecba9fb2'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x3e505ddb': self.unknown_0x3e505ddb,
            'unknown_0x118f1e46': self.unknown_0x118f1e46,
            'unknown_0x6e603df2': self.unknown_0x6e603df2,
            'unknown_0x1e74f1ec': self.unknown_0x1e74f1ec,
            'unknown_0xecba9fb2': self.unknown_0xecba9fb2,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x3e505ddb, 0x118f1e46, 0x6e603df2, 0x1e74f1ec, 0xecba9fb2)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[BloggStruct]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHlLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return BloggStruct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_unknown_0x3e505ddb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x118f1e46(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6e603df2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1e74f1ec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xecba9fb2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x3e505ddb: ('unknown_0x3e505ddb', _decode_unknown_0x3e505ddb),
    0x118f1e46: ('unknown_0x118f1e46', _decode_unknown_0x118f1e46),
    0x6e603df2: ('unknown_0x6e603df2', _decode_unknown_0x6e603df2),
    0x1e74f1ec: ('unknown_0x1e74f1ec', _decode_unknown_0x1e74f1ec),
    0xecba9fb2: ('unknown_0xecba9fb2', _decode_unknown_0xecba9fb2),
}
