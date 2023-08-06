# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class SandwormStruct(BaseProperty):
    unknown_0x98106ee2: float = dataclasses.field(default=1.0)
    unknown_0x95081226: float = dataclasses.field(default=3.0)
    unknown_0xc2064265: float = dataclasses.field(default=5.0)
    move_speed_multiplier: float = dataclasses.field(default=1.0)
    unknown_0x59f14d7c: int = dataclasses.field(default=3)
    unknown_0x9606b4b0: int = dataclasses.field(default=5)
    unknown_0xfc2697dd: int = dataclasses.field(default=5)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x98\x10n\xe2')  # 0x98106ee2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x98106ee2))

        data.write(b'\x95\x08\x12&')  # 0x95081226
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95081226))

        data.write(b'\xc2\x06Be')  # 0xc2064265
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc2064265))

        data.write(b'\xfe\x913\xcd')  # 0xfe9133cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_speed_multiplier))

        data.write(b'Y\xf1M|')  # 0x59f14d7c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x59f14d7c))

        data.write(b'\x96\x06\xb4\xb0')  # 0x9606b4b0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x9606b4b0))

        data.write(b'\xfc&\x97\xdd')  # 0xfc2697dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xfc2697dd))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x98106ee2=data['unknown_0x98106ee2'],
            unknown_0x95081226=data['unknown_0x95081226'],
            unknown_0xc2064265=data['unknown_0xc2064265'],
            move_speed_multiplier=data['move_speed_multiplier'],
            unknown_0x59f14d7c=data['unknown_0x59f14d7c'],
            unknown_0x9606b4b0=data['unknown_0x9606b4b0'],
            unknown_0xfc2697dd=data['unknown_0xfc2697dd'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x98106ee2': self.unknown_0x98106ee2,
            'unknown_0x95081226': self.unknown_0x95081226,
            'unknown_0xc2064265': self.unknown_0xc2064265,
            'move_speed_multiplier': self.move_speed_multiplier,
            'unknown_0x59f14d7c': self.unknown_0x59f14d7c,
            'unknown_0x9606b4b0': self.unknown_0x9606b4b0,
            'unknown_0xfc2697dd': self.unknown_0xfc2697dd,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x98106ee2, 0x95081226, 0xc2064265, 0xfe9133cd, 0x59f14d7c, 0x9606b4b0, 0xfc2697dd)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SandwormStruct]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHlLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(70))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return SandwormStruct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_unknown_0x98106ee2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x95081226(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc2064265(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move_speed_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x59f14d7c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x9606b4b0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xfc2697dd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x98106ee2: ('unknown_0x98106ee2', _decode_unknown_0x98106ee2),
    0x95081226: ('unknown_0x95081226', _decode_unknown_0x95081226),
    0xc2064265: ('unknown_0xc2064265', _decode_unknown_0xc2064265),
    0xfe9133cd: ('move_speed_multiplier', _decode_move_speed_multiplier),
    0x59f14d7c: ('unknown_0x59f14d7c', _decode_unknown_0x59f14d7c),
    0x9606b4b0: ('unknown_0x9606b4b0', _decode_unknown_0x9606b4b0),
    0xfc2697dd: ('unknown_0xfc2697dd', _decode_unknown_0xfc2697dd),
}
