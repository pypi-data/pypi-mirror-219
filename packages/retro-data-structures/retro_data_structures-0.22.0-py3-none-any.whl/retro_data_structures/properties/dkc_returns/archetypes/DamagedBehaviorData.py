# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class DamagedBehaviorData(BaseProperty):
    death_type: enums.DeathType = dataclasses.field(default=enums.DeathType.Unknown1)
    flee_on_damaged: bool = dataclasses.field(default=False)
    blink_when_damaged: bool = dataclasses.field(default=True)
    flinch_from_ground_pound: bool = dataclasses.field(default=False)
    allow_top_flinch: bool = dataclasses.field(default=False)
    flinch_requires_perfect_match: bool = dataclasses.field(default=True)
    stop_on_knockback: bool = dataclasses.field(default=False)
    hurl_from_thrown_damage: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'i\x9b\xfa\x8b')  # 0x699bfa8b
        data.write(b'\x00\x04')  # size
        self.death_type.to_stream(data)

        data.write(b'\x97\xdet!')  # 0x97de7421
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.flee_on_damaged))

        data.write(b'U\xefZ\xb4')  # 0x55ef5ab4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.blink_when_damaged))

        data.write(b'y\xd2\x17\xbf')  # 0x79d217bf
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.flinch_from_ground_pound))

        data.write(b'/_\xd5<')  # 0x2f5fd53c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_top_flinch))

        data.write(b'\xd6\xffg\xbf')  # 0xd6ff67bf
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.flinch_requires_perfect_match))

        data.write(b'\xbe\xba\xf0\x85')  # 0xbebaf085
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.stop_on_knockback))

        data.write(b'\x02*0`')  # 0x22a3060
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.hurl_from_thrown_damage))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            death_type=enums.DeathType.from_json(data['death_type']),
            flee_on_damaged=data['flee_on_damaged'],
            blink_when_damaged=data['blink_when_damaged'],
            flinch_from_ground_pound=data['flinch_from_ground_pound'],
            allow_top_flinch=data['allow_top_flinch'],
            flinch_requires_perfect_match=data['flinch_requires_perfect_match'],
            stop_on_knockback=data['stop_on_knockback'],
            hurl_from_thrown_damage=data['hurl_from_thrown_damage'],
        )

    def to_json(self) -> dict:
        return {
            'death_type': self.death_type.to_json(),
            'flee_on_damaged': self.flee_on_damaged,
            'blink_when_damaged': self.blink_when_damaged,
            'flinch_from_ground_pound': self.flinch_from_ground_pound,
            'allow_top_flinch': self.allow_top_flinch,
            'flinch_requires_perfect_match': self.flinch_requires_perfect_match,
            'stop_on_knockback': self.stop_on_knockback,
            'hurl_from_thrown_damage': self.hurl_from_thrown_damage,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x699bfa8b, 0x97de7421, 0x55ef5ab4, 0x79d217bf, 0x2f5fd53c, 0xd6ff67bf, 0xbebaf085, 0x22a3060)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[DamagedBehaviorData]:
    if property_count != 8:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLH?LH?LH?LH?LH?LH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(59))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) != _FAST_IDS:
        data.seek(before)
        return None

    return DamagedBehaviorData(
        enums.DeathType(dec[2]),
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
    )


def _decode_death_type(data: typing.BinaryIO, property_size: int):
    return enums.DeathType.from_stream(data)


def _decode_flee_on_damaged(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_blink_when_damaged(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_flinch_from_ground_pound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_top_flinch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_flinch_requires_perfect_match(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_stop_on_knockback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_hurl_from_thrown_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x699bfa8b: ('death_type', _decode_death_type),
    0x97de7421: ('flee_on_damaged', _decode_flee_on_damaged),
    0x55ef5ab4: ('blink_when_damaged', _decode_blink_when_damaged),
    0x79d217bf: ('flinch_from_ground_pound', _decode_flinch_from_ground_pound),
    0x2f5fd53c: ('allow_top_flinch', _decode_allow_top_flinch),
    0xd6ff67bf: ('flinch_requires_perfect_match', _decode_flinch_requires_perfect_match),
    0xbebaf085: ('stop_on_knockback', _decode_stop_on_knockback),
    0x22a3060: ('hurl_from_thrown_damage', _decode_hurl_from_thrown_damage),
}
