# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class KorbaSnatcherData(BaseProperty):
    player_attach_distance: float = dataclasses.field(default=0.800000011920929)
    unknown_0xa2efcada: int = dataclasses.field(default=5)
    unknown_0x37e9d29b: int = dataclasses.field(default=8)
    unknown_0xb827744f: float = dataclasses.field(default=1.0)
    unknown_0x010f2e81: float = dataclasses.field(default=2.5)
    unknown_0xf7e350db: float = dataclasses.field(default=2000.0)
    morphball_roll_speed_multiplier: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x05a571a0: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x8abb2662: float = dataclasses.field(default=1.0)
    unknown_0x04d6c440: float = dataclasses.field(default=30.0)
    korba_death_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xa3P\xf1Z')  # 0xa350f15a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_attach_distance))

        data.write(b'\xa2\xef\xca\xda')  # 0xa2efcada
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa2efcada))

        data.write(b'7\xe9\xd2\x9b')  # 0x37e9d29b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x37e9d29b))

        data.write(b"\xb8'tO")  # 0xb827744f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb827744f))

        data.write(b'\x01\x0f.\x81')  # 0x10f2e81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x010f2e81))

        data.write(b'\xf7\xe3P\xdb')  # 0xf7e350db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf7e350db))

        data.write(b'\xc7\xec={')  # 0xc7ec3d7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.morphball_roll_speed_multiplier))

        data.write(b'\x05\xa5q\xa0')  # 0x5a571a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x05a571a0))

        data.write(b'\x8a\xbb&b')  # 0x8abb2662
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8abb2662))

        data.write(b'\x04\xd6\xc4@')  # 0x4d6c440
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x04d6c440))

        data.write(b'\x97;\xf0\xca')  # 0x973bf0ca
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.korba_death_particle_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            player_attach_distance=data['player_attach_distance'],
            unknown_0xa2efcada=data['unknown_0xa2efcada'],
            unknown_0x37e9d29b=data['unknown_0x37e9d29b'],
            unknown_0xb827744f=data['unknown_0xb827744f'],
            unknown_0x010f2e81=data['unknown_0x010f2e81'],
            unknown_0xf7e350db=data['unknown_0xf7e350db'],
            morphball_roll_speed_multiplier=data['morphball_roll_speed_multiplier'],
            unknown_0x05a571a0=data['unknown_0x05a571a0'],
            unknown_0x8abb2662=data['unknown_0x8abb2662'],
            unknown_0x04d6c440=data['unknown_0x04d6c440'],
            korba_death_particle_effect=data['korba_death_particle_effect'],
        )

    def to_json(self) -> dict:
        return {
            'player_attach_distance': self.player_attach_distance,
            'unknown_0xa2efcada': self.unknown_0xa2efcada,
            'unknown_0x37e9d29b': self.unknown_0x37e9d29b,
            'unknown_0xb827744f': self.unknown_0xb827744f,
            'unknown_0x010f2e81': self.unknown_0x010f2e81,
            'unknown_0xf7e350db': self.unknown_0xf7e350db,
            'morphball_roll_speed_multiplier': self.morphball_roll_speed_multiplier,
            'unknown_0x05a571a0': self.unknown_0x05a571a0,
            'unknown_0x8abb2662': self.unknown_0x8abb2662,
            'unknown_0x04d6c440': self.unknown_0x04d6c440,
            'korba_death_particle_effect': self.korba_death_particle_effect,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xa350f15a, 0xa2efcada, 0x37e9d29b, 0xb827744f, 0x10f2e81, 0xf7e350db, 0xc7ec3d7b, 0x5a571a0, 0x8abb2662, 0x4d6c440, 0x973bf0ca)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[KorbaSnatcherData]:
    if property_count != 11:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHlLHlLHfLHfLHfLHfLHfLHfLHfLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(114))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) != _FAST_IDS:
        data.seek(before)
        return None

    return KorbaSnatcherData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
    )


def _decode_player_attach_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa2efcada(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x37e9d29b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb827744f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x010f2e81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf7e350db(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_morphball_roll_speed_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x05a571a0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8abb2662(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x04d6c440(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_korba_death_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa350f15a: ('player_attach_distance', _decode_player_attach_distance),
    0xa2efcada: ('unknown_0xa2efcada', _decode_unknown_0xa2efcada),
    0x37e9d29b: ('unknown_0x37e9d29b', _decode_unknown_0x37e9d29b),
    0xb827744f: ('unknown_0xb827744f', _decode_unknown_0xb827744f),
    0x10f2e81: ('unknown_0x010f2e81', _decode_unknown_0x010f2e81),
    0xf7e350db: ('unknown_0xf7e350db', _decode_unknown_0xf7e350db),
    0xc7ec3d7b: ('morphball_roll_speed_multiplier', _decode_morphball_roll_speed_multiplier),
    0x5a571a0: ('unknown_0x05a571a0', _decode_unknown_0x05a571a0),
    0x8abb2662: ('unknown_0x8abb2662', _decode_unknown_0x8abb2662),
    0x4d6c440: ('unknown_0x04d6c440', _decode_unknown_0x04d6c440),
    0x973bf0ca: ('korba_death_particle_effect', _decode_korba_death_particle_effect),
}
