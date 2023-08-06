# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct30(BaseProperty):
    weapon_system: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART', 'ELSC']}, default=default_asset_id)
    visor_impact_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x2f79b3d0: float = dataclasses.field(default=20.0)
    unknown_0x11cc7b58: float = dataclasses.field(default=60.0)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'E\x9a\xe4\xa8')  # 0x459ae4a8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.weapon_system))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9\xc8\xe2\xbd')  # 0xe9c8e2bd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_effect))

        data.write(b'\x86\xff\xb3\xf6')  # 0x86ffb3f6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.visor_impact_sound))

        data.write(b'/y\xb3\xd0')  # 0x2f79b3d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2f79b3d0))

        data.write(b'\x11\xcc{X')  # 0x11cc7b58
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x11cc7b58))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            weapon_system=data['weapon_system'],
            damage=DamageInfo.from_json(data['damage']),
            visor_effect=data['visor_effect'],
            visor_impact_sound=data['visor_impact_sound'],
            unknown_0x2f79b3d0=data['unknown_0x2f79b3d0'],
            unknown_0x11cc7b58=data['unknown_0x11cc7b58'],
        )

    def to_json(self) -> dict:
        return {
            'weapon_system': self.weapon_system,
            'damage': self.damage.to_json(),
            'visor_effect': self.visor_effect,
            'visor_impact_sound': self.visor_impact_sound,
            'unknown_0x2f79b3d0': self.unknown_0x2f79b3d0,
            'unknown_0x11cc7b58': self.unknown_0x11cc7b58,
        }


def _decode_weapon_system(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_visor_impact_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x2f79b3d0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x11cc7b58(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x459ae4a8: ('weapon_system', _decode_weapon_system),
    0x337f9524: ('damage', _decode_damage),
    0xe9c8e2bd: ('visor_effect', _decode_visor_effect),
    0x86ffb3f6: ('visor_impact_sound', _decode_visor_impact_sound),
    0x2f79b3d0: ('unknown_0x2f79b3d0', _decode_unknown_0x2f79b3d0),
    0x11cc7b58: ('unknown_0x11cc7b58', _decode_unknown_0x11cc7b58),
}
