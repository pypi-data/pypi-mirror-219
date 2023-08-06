# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class CattleProd(BaseProperty):
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    hyper_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    max_attack_dist: float = dataclasses.field(default=5.0)
    visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART', 'ELSC']}, default=default_asset_id)
    stun_time: float = dataclasses.field(default=1.0)
    unknown: float = dataclasses.field(default=25.0)
    player_impact_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\xda\xbf\x84')  # 0xb3dabf84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'.\xd2_P')  # 0x2ed25f50
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_dist))

        data.write(b'\xe9\xc8\xe2\xbd')  # 0xe9c8e2bd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_effect))

        data.write(b'~\x19#\x95')  # 0x7e192395
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_time))

        data.write(b']\x16R\xe2')  # 0x5d1652e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xe3:\x99m')  # 0xe33a996d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.player_impact_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            damage=DamageInfo.from_json(data['damage']),
            hyper_damage=DamageInfo.from_json(data['hyper_damage']),
            max_attack_dist=data['max_attack_dist'],
            visor_effect=data['visor_effect'],
            stun_time=data['stun_time'],
            unknown=data['unknown'],
            player_impact_sound=data['player_impact_sound'],
        )

    def to_json(self) -> dict:
        return {
            'damage': self.damage.to_json(),
            'hyper_damage': self.hyper_damage.to_json(),
            'max_attack_dist': self.max_attack_dist,
            'visor_effect': self.visor_effect,
            'stun_time': self.stun_time,
            'unknown': self.unknown,
            'player_impact_sound': self.player_impact_sound,
        }


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_hyper_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_max_attack_dist(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stun_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_impact_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x337f9524: ('damage', _decode_damage),
    0xb3dabf84: ('hyper_damage', _decode_hyper_damage),
    0x2ed25f50: ('max_attack_dist', _decode_max_attack_dist),
    0xe9c8e2bd: ('visor_effect', _decode_visor_effect),
    0x7e192395: ('stun_time', _decode_stun_time),
    0x5d1652e2: ('unknown', _decode_unknown),
    0xe33a996d: ('player_impact_sound', _decode_player_impact_sound),
}
