# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.DamageEffectData import DamageEffectData
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct291(BaseProperty):
    unknown_0x0063bdc5: float = dataclasses.field(default=3.4000000953674316)
    unknown_0xfa8948cc: float = dataclasses.field(default=0.5)
    unknown_0xce1bcfd8: float = dataclasses.field(default=1.0)
    unknown_0x96ecf959: float = dataclasses.field(default=0.5)
    shock_wave_ring_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage_effect_data_0xae342f0f: DamageEffectData = dataclasses.field(default_factory=DamageEffectData)
    damage_effect_data_0x46d65682: DamageEffectData = dataclasses.field(default_factory=DamageEffectData)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x00c\xbd\xc5')  # 0x63bdc5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0063bdc5))

        data.write(b'\xfa\x89H\xcc')  # 0xfa8948cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfa8948cc))

        data.write(b'\xce\x1b\xcf\xd8')  # 0xce1bcfd8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xce1bcfd8))

        data.write(b'\x96\xec\xf9Y')  # 0x96ecf959
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x96ecf959))

        data.write(b'\xd3\xc19\x0e')  # 0xd3c1390e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shock_wave_ring_effect))

        data.write(b'\xae4/\x0f')  # 0xae342f0f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_effect_data_0xae342f0f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\xd6V\x82')  # 0x46d65682
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_effect_data_0x46d65682.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x0063bdc5=data['unknown_0x0063bdc5'],
            unknown_0xfa8948cc=data['unknown_0xfa8948cc'],
            unknown_0xce1bcfd8=data['unknown_0xce1bcfd8'],
            unknown_0x96ecf959=data['unknown_0x96ecf959'],
            shock_wave_ring_effect=data['shock_wave_ring_effect'],
            damage_effect_data_0xae342f0f=DamageEffectData.from_json(data['damage_effect_data_0xae342f0f']),
            damage_effect_data_0x46d65682=DamageEffectData.from_json(data['damage_effect_data_0x46d65682']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x0063bdc5': self.unknown_0x0063bdc5,
            'unknown_0xfa8948cc': self.unknown_0xfa8948cc,
            'unknown_0xce1bcfd8': self.unknown_0xce1bcfd8,
            'unknown_0x96ecf959': self.unknown_0x96ecf959,
            'shock_wave_ring_effect': self.shock_wave_ring_effect,
            'damage_effect_data_0xae342f0f': self.damage_effect_data_0xae342f0f.to_json(),
            'damage_effect_data_0x46d65682': self.damage_effect_data_0x46d65682.to_json(),
        }


def _decode_unknown_0x0063bdc5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfa8948cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xce1bcfd8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x96ecf959(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shock_wave_ring_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage_effect_data_0xae342f0f(data: typing.BinaryIO, property_size: int):
    return DamageEffectData.from_stream(data, property_size)


def _decode_damage_effect_data_0x46d65682(data: typing.BinaryIO, property_size: int):
    return DamageEffectData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x63bdc5: ('unknown_0x0063bdc5', _decode_unknown_0x0063bdc5),
    0xfa8948cc: ('unknown_0xfa8948cc', _decode_unknown_0xfa8948cc),
    0xce1bcfd8: ('unknown_0xce1bcfd8', _decode_unknown_0xce1bcfd8),
    0x96ecf959: ('unknown_0x96ecf959', _decode_unknown_0x96ecf959),
    0xd3c1390e: ('shock_wave_ring_effect', _decode_shock_wave_ring_effect),
    0xae342f0f: ('damage_effect_data_0xae342f0f', _decode_damage_effect_data_0xae342f0f),
    0x46d65682: ('damage_effect_data_0x46d65682', _decode_damage_effect_data_0x46d65682),
}
