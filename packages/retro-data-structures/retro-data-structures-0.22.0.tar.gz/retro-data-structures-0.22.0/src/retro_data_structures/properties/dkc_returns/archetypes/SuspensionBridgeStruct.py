# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class SuspensionBridgeStruct(BaseProperty):
    player: bool = dataclasses.field(default=True)
    ai: bool = dataclasses.field(default=False)
    creature: bool = dataclasses.field(default=False)
    damage_effect: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xd5i\x92d')  # 0xd5699264
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player))

        data.write(b'\xab\x1fT#')  # 0xab1f5423
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ai))

        data.write(b'\xec\xf80\xee')  # 0xecf830ee
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.creature))

        data.write(b'\xe9\xd2\xffI')  # 0xe9d2ff49
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.damage_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            player=data['player'],
            ai=data['ai'],
            creature=data['creature'],
            damage_effect=data['damage_effect'],
        )

    def to_json(self) -> dict:
        return {
            'player': self.player,
            'ai': self.ai,
            'creature': self.creature,
            'damage_effect': self.damage_effect,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xd5699264, 0xab1f5423, 0xecf830ee, 0xe9d2ff49)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SuspensionBridgeStruct]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(28))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return SuspensionBridgeStruct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ai(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_creature(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_damage_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd5699264: ('player', _decode_player),
    0xab1f5423: ('ai', _decode_ai),
    0xecf830ee: ('creature', _decode_creature),
    0xe9d2ff49: ('damage_effect', _decode_damage_effect),
}
