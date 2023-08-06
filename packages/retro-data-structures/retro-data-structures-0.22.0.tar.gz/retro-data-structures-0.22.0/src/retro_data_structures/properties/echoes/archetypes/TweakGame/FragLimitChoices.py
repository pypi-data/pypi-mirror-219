# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class FragLimitChoices(BaseProperty):
    frag_limit0: int = dataclasses.field(default=0)
    frag_limit1: int = dataclasses.field(default=5)
    frag_limit2: int = dataclasses.field(default=10)
    frag_limit3: int = dataclasses.field(default=15)
    frag_limit4: int = dataclasses.field(default=20)

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

        data.write(b'\xa2\x02;\xa8')  # 0xa2023ba8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.frag_limit0))

        data.write(b'\x1a\xbe\\\xcd')  # 0x1abe5ccd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.frag_limit1))

        data.write(b'\x08\x0b\xf3#')  # 0x80bf323
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.frag_limit2))

        data.write(b'\xb0\xb7\x94F')  # 0xb0b79446
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.frag_limit3))

        data.write(b'-`\xac\xff')  # 0x2d60acff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.frag_limit4))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            frag_limit0=data['frag_limit0'],
            frag_limit1=data['frag_limit1'],
            frag_limit2=data['frag_limit2'],
            frag_limit3=data['frag_limit3'],
            frag_limit4=data['frag_limit4'],
        )

    def to_json(self) -> dict:
        return {
            'frag_limit0': self.frag_limit0,
            'frag_limit1': self.frag_limit1,
            'frag_limit2': self.frag_limit2,
            'frag_limit3': self.frag_limit3,
            'frag_limit4': self.frag_limit4,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xa2023ba8, 0x1abe5ccd, 0x80bf323, 0xb0b79446, 0x2d60acff)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[FragLimitChoices]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHlLHlLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(50))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return FragLimitChoices(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_frag_limit0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_frag_limit1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_frag_limit2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_frag_limit3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_frag_limit4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa2023ba8: ('frag_limit0', _decode_frag_limit0),
    0x1abe5ccd: ('frag_limit1', _decode_frag_limit1),
    0x80bf323: ('frag_limit2', _decode_frag_limit2),
    0xb0b79446: ('frag_limit3', _decode_frag_limit3),
    0x2d60acff: ('frag_limit4', _decode_frag_limit4),
}
