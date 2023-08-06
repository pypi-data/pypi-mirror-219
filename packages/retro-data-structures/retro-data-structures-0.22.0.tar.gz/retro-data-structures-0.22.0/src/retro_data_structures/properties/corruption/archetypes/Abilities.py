# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Abilities(BaseProperty):
    double_jump: bool = dataclasses.field(default=False)
    suit_type: int = dataclasses.field(default=0)
    screw_attack: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\t\xdc<\xdd')  # 0x9dc3cdd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.double_jump))

        data.write(b'\xc0\xbd\x8a^')  # 0xc0bd8a5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.suit_type))

        data.write(b'Z\x06n,')  # 0x5a066e2c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.screw_attack))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            double_jump=data['double_jump'],
            suit_type=data['suit_type'],
            screw_attack=data['screw_attack'],
        )

    def to_json(self) -> dict:
        return {
            'double_jump': self.double_jump,
            'suit_type': self.suit_type,
            'screw_attack': self.screw_attack,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x9dc3cdd, 0xc0bd8a5e, 0x5a066e2c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Abilities]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(27))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return Abilities(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_double_jump(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_suit_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_screw_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9dc3cdd: ('double_jump', _decode_double_jump),
    0xc0bd8a5e: ('suit_type', _decode_suit_type),
    0x5a066e2c: ('screw_attack', _decode_screw_attack),
}
