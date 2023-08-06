# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.DamageEffectData import DamageEffectData
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct187(BaseProperty):
    unknown: int = dataclasses.field(default=1)
    impact_stun_radius: float = dataclasses.field(default=5.0)
    impact_stun_velocity: float = dataclasses.field(default=8.0)
    impact_stun_duration: float = dataclasses.field(default=1.0)
    shock_wave_ring_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage_effect_data: DamageEffectData = dataclasses.field(default_factory=DamageEffectData)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\xd4:\xac"')  # 0xd43aac22
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.impact_stun_radius))

        data.write(b'Y\xcc\xac\x1b')  # 0x59ccac1b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.impact_stun_velocity))

        data.write(b'\xd0mX\xa7')  # 0xd06d58a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.impact_stun_duration))

        data.write(b'\xd3\xc19\x0e')  # 0xd3c1390e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shock_wave_ring_effect))

        data.write(b'\xae4/\x0f')  # 0xae342f0f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_effect_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            impact_stun_radius=data['impact_stun_radius'],
            impact_stun_velocity=data['impact_stun_velocity'],
            impact_stun_duration=data['impact_stun_duration'],
            shock_wave_ring_effect=data['shock_wave_ring_effect'],
            damage_effect_data=DamageEffectData.from_json(data['damage_effect_data']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'impact_stun_radius': self.impact_stun_radius,
            'impact_stun_velocity': self.impact_stun_velocity,
            'impact_stun_duration': self.impact_stun_duration,
            'shock_wave_ring_effect': self.shock_wave_ring_effect,
            'damage_effect_data': self.damage_effect_data.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_impact_stun_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_impact_stun_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_impact_stun_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shock_wave_ring_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage_effect_data(data: typing.BinaryIO, property_size: int):
    return DamageEffectData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8a58a7f8: ('unknown', _decode_unknown),
    0xd43aac22: ('impact_stun_radius', _decode_impact_stun_radius),
    0x59ccac1b: ('impact_stun_velocity', _decode_impact_stun_velocity),
    0xd06d58a7: ('impact_stun_duration', _decode_impact_stun_duration),
    0xd3c1390e: ('shock_wave_ring_effect', _decode_shock_wave_ring_effect),
    0xae342f0f: ('damage_effect_data', _decode_damage_effect_data),
}
