# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class BehaveChance(BaseProperty):
    lurk: float = dataclasses.field(default=-0.0)
    unknown: float = dataclasses.field(default=0.0)
    attack: float = dataclasses.field(default=0.0)
    move: float = dataclasses.field(default=0.0)
    lurk_time: float = dataclasses.field(default=0.0)
    charge_attack: float = dataclasses.field(default=0.0)
    num_bolts: int = dataclasses.field(default=0)

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

        data.write(b'\xd3\xa3\x13\xa5')  # 0xd3a313a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lurk))

        data.write(b'<\xfai\xf1')  # 0x3cfa69f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\x1a\xf8\x9fK')  # 0x1af89f4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack))

        data.write(b'\xe7\xe6of')  # 0xe7e66f66
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move))

        data.write(b'\xb9\xd9\xc2\xd2')  # 0xb9d9c2d2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lurk_time))

        data.write(b'\xcf\xab\xdd_')  # 0xcfabdd5f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_attack))

        data.write(b'Z\xb2(\xb6')  # 0x5ab228b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_bolts))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            lurk=data['lurk'],
            unknown=data['unknown'],
            attack=data['attack'],
            move=data['move'],
            lurk_time=data['lurk_time'],
            charge_attack=data['charge_attack'],
            num_bolts=data['num_bolts'],
        )

    def to_json(self) -> dict:
        return {
            'lurk': self.lurk,
            'unknown': self.unknown,
            'attack': self.attack,
            'move': self.move,
            'lurk_time': self.lurk_time,
            'charge_attack': self.charge_attack,
            'num_bolts': self.num_bolts,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xd3a313a5, 0x3cfa69f1, 0x1af89f4b, 0xe7e66f66, 0xb9d9c2d2, 0xcfabdd5f, 0x5ab228b6)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[BehaveChance]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(70))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return BehaveChance(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_lurk(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lurk_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_num_bolts(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd3a313a5: ('lurk', _decode_lurk),
    0x3cfa69f1: ('unknown', _decode_unknown),
    0x1af89f4b: ('attack', _decode_attack),
    0xe7e66f66: ('move', _decode_move),
    0xb9d9c2d2: ('lurk_time', _decode_lurk_time),
    0xcfabdd5f: ('charge_attack', _decode_charge_attack),
    0x5ab228b6: ('num_bolts', _decode_num_bolts),
}
