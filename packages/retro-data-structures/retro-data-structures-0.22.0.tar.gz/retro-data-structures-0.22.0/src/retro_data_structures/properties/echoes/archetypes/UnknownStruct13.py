# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct13(BaseProperty):
    unknown: float = dataclasses.field(default=2.0)
    min_attack_range: float = dataclasses.field(default=10.0)
    max_attack_range: float = dataclasses.field(default=35.0)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    mold_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    mold_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_mold: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xd2X\xec\t')  # 0xd258ec09
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'XCI\x16')  # 0x58434916
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_range))

        data.write(b'\xffw\xc9o')  # 0xff77c96f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_range))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 40.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile))

        data.write(b'Yy\xd9\xe1')  # 0x5979d9e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.mold_effect))

        data.write(b'\x80t..')  # 0x80742e2e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mold_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 0.08332999795675278})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5\xcf\xb8\xaf')  # 0xf5cfb8af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_mold.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            min_attack_range=data['min_attack_range'],
            max_attack_range=data['max_attack_range'],
            damage=DamageInfo.from_json(data['damage']),
            projectile=data['projectile'],
            mold_effect=data['mold_effect'],
            mold_damage=DamageInfo.from_json(data['mold_damage']),
            sound_mold=AudioPlaybackParms.from_json(data['sound_mold']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'min_attack_range': self.min_attack_range,
            'max_attack_range': self.max_attack_range,
            'damage': self.damage.to_json(),
            'projectile': self.projectile,
            'mold_effect': self.mold_effect,
            'mold_damage': self.mold_damage.to_json(),
            'sound_mold': self.sound_mold.to_json(),
        }

    def _dependencies_for_damage(self, asset_manager):
        yield from self.damage.dependencies_for(asset_manager)

    def _dependencies_for_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile)

    def _dependencies_for_mold_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.mold_effect)

    def _dependencies_for_mold_damage(self, asset_manager):
        yield from self.mold_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_mold(self, asset_manager):
        yield from self.sound_mold.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_damage, "damage", "DamageInfo"),
            (self._dependencies_for_projectile, "projectile", "AssetId"),
            (self._dependencies_for_mold_effect, "mold_effect", "AssetId"),
            (self._dependencies_for_mold_damage, "mold_damage", "DamageInfo"),
            (self._dependencies_for_sound_mold, "sound_mold", "AudioPlaybackParms"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct13.{field_name} ({field_type}): {e}"
                )


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 40.0, 'di_knock_back_power': 10.0})


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_mold_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_mold_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 0.08332999795675278})


def _decode_sound_mold(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd258ec09: ('unknown', _decode_unknown),
    0x58434916: ('min_attack_range', _decode_min_attack_range),
    0xff77c96f: ('max_attack_range', _decode_max_attack_range),
    0x337f9524: ('damage', _decode_damage),
    0xef485db9: ('projectile', _decode_projectile),
    0x5979d9e1: ('mold_effect', _decode_mold_effect),
    0x80742e2e: ('mold_damage', _decode_mold_damage),
    0xf5cfb8af: ('sound_mold', _decode_sound_mold),
}
