# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SpacePirateWeaponData(BaseProperty):
    unknown_0x647670ac: int = dataclasses.field(default=0)
    grenade_launcher: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unknown_0xa95a025b: int = dataclasses.field(default=3)
    unknown_0x25f822c4: float = dataclasses.field(default=15.0)
    unknown_0x765e3a20: float = dataclasses.field(default=50.0)
    grenade_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    grenade_explosion: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grenade_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grenade_trail: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grenade_mass: float = dataclasses.field(default=25.0)
    unknown_0xed086ce0: float = dataclasses.field(default=0.4000000059604645)
    unknown_0x00fc6646: float = dataclasses.field(default=20.0)
    unknown_0xa7c8e63f: float = dataclasses.field(default=50.0)
    unknown_0x454f16b1: int = dataclasses.field(default=2)
    sound_grenade_bounce: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_grenade_explode: int = dataclasses.field(default=0, metadata={'sound': True})

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'dvp\xac')  # 0x647670ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x647670ac))

        data.write(b'\xa7\x9b\xb8.')  # 0xa79bb82e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grenade_launcher))

        data.write(b'\xa9Z\x02[')  # 0xa95a025b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa95a025b))

        data.write(b'%\xf8"\xc4')  # 0x25f822c4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x25f822c4))

        data.write(b'v^: ')  # 0x765e3a20
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x765e3a20))

        data.write(b'\x14\xd1\xa3\xa8')  # 0x14d1a3a8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grenade_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 40.0, 'di_radius': 8.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x13\x19\xe0w')  # 0x1319e077
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grenade_explosion))

        data.write(b'\xd2\x07\xff\x0f')  # 0xd207ff0f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grenade_effect))

        data.write(b'+1\xc8\x82')  # 0x2b31c882
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grenade_trail))

        data.write(b'\x9ak\xb4\x7f')  # 0x9a6bb47f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grenade_mass))

        data.write(b'\xed\x08l\xe0')  # 0xed086ce0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xed086ce0))

        data.write(b'\x00\xfcfF')  # 0xfc6646
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x00fc6646))

        data.write(b'\xa7\xc8\xe6?')  # 0xa7c8e63f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa7c8e63f))

        data.write(b'EO\x16\xb1')  # 0x454f16b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x454f16b1))

        data.write(b'%\x8c>\x1b')  # 0x258c3e1b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_grenade_bounce))

        data.write(b'\xafj\xad\x88')  # 0xaf6aad88
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_grenade_explode))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x647670ac=data['unknown_0x647670ac'],
            grenade_launcher=data['grenade_launcher'],
            unknown_0xa95a025b=data['unknown_0xa95a025b'],
            unknown_0x25f822c4=data['unknown_0x25f822c4'],
            unknown_0x765e3a20=data['unknown_0x765e3a20'],
            grenade_damage=DamageInfo.from_json(data['grenade_damage']),
            grenade_explosion=data['grenade_explosion'],
            grenade_effect=data['grenade_effect'],
            grenade_trail=data['grenade_trail'],
            grenade_mass=data['grenade_mass'],
            unknown_0xed086ce0=data['unknown_0xed086ce0'],
            unknown_0x00fc6646=data['unknown_0x00fc6646'],
            unknown_0xa7c8e63f=data['unknown_0xa7c8e63f'],
            unknown_0x454f16b1=data['unknown_0x454f16b1'],
            sound_grenade_bounce=data['sound_grenade_bounce'],
            sound_grenade_explode=data['sound_grenade_explode'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x647670ac': self.unknown_0x647670ac,
            'grenade_launcher': self.grenade_launcher,
            'unknown_0xa95a025b': self.unknown_0xa95a025b,
            'unknown_0x25f822c4': self.unknown_0x25f822c4,
            'unknown_0x765e3a20': self.unknown_0x765e3a20,
            'grenade_damage': self.grenade_damage.to_json(),
            'grenade_explosion': self.grenade_explosion,
            'grenade_effect': self.grenade_effect,
            'grenade_trail': self.grenade_trail,
            'grenade_mass': self.grenade_mass,
            'unknown_0xed086ce0': self.unknown_0xed086ce0,
            'unknown_0x00fc6646': self.unknown_0x00fc6646,
            'unknown_0xa7c8e63f': self.unknown_0xa7c8e63f,
            'unknown_0x454f16b1': self.unknown_0x454f16b1,
            'sound_grenade_bounce': self.sound_grenade_bounce,
            'sound_grenade_explode': self.sound_grenade_explode,
        }

    def _dependencies_for_grenade_launcher(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grenade_launcher)

    def _dependencies_for_grenade_damage(self, asset_manager):
        yield from self.grenade_damage.dependencies_for(asset_manager)

    def _dependencies_for_grenade_explosion(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grenade_explosion)

    def _dependencies_for_grenade_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grenade_effect)

    def _dependencies_for_grenade_trail(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grenade_trail)

    def _dependencies_for_sound_grenade_bounce(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_grenade_bounce)

    def _dependencies_for_sound_grenade_explode(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_grenade_explode)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_grenade_launcher, "grenade_launcher", "AssetId"),
            (self._dependencies_for_grenade_damage, "grenade_damage", "DamageInfo"),
            (self._dependencies_for_grenade_explosion, "grenade_explosion", "AssetId"),
            (self._dependencies_for_grenade_effect, "grenade_effect", "AssetId"),
            (self._dependencies_for_grenade_trail, "grenade_trail", "AssetId"),
            (self._dependencies_for_sound_grenade_bounce, "sound_grenade_bounce", "int"),
            (self._dependencies_for_sound_grenade_explode, "sound_grenade_explode", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SpacePirateWeaponData.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0x647670ac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grenade_launcher(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0xa95a025b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x25f822c4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x765e3a20(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grenade_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 40.0, 'di_radius': 8.0, 'di_knock_back_power': 10.0})


def _decode_grenade_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grenade_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grenade_trail(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grenade_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xed086ce0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x00fc6646(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa7c8e63f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x454f16b1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_grenade_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_grenade_explode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x647670ac: ('unknown_0x647670ac', _decode_unknown_0x647670ac),
    0xa79bb82e: ('grenade_launcher', _decode_grenade_launcher),
    0xa95a025b: ('unknown_0xa95a025b', _decode_unknown_0xa95a025b),
    0x25f822c4: ('unknown_0x25f822c4', _decode_unknown_0x25f822c4),
    0x765e3a20: ('unknown_0x765e3a20', _decode_unknown_0x765e3a20),
    0x14d1a3a8: ('grenade_damage', _decode_grenade_damage),
    0x1319e077: ('grenade_explosion', _decode_grenade_explosion),
    0xd207ff0f: ('grenade_effect', _decode_grenade_effect),
    0x2b31c882: ('grenade_trail', _decode_grenade_trail),
    0x9a6bb47f: ('grenade_mass', _decode_grenade_mass),
    0xed086ce0: ('unknown_0xed086ce0', _decode_unknown_0xed086ce0),
    0xfc6646: ('unknown_0x00fc6646', _decode_unknown_0x00fc6646),
    0xa7c8e63f: ('unknown_0xa7c8e63f', _decode_unknown_0xa7c8e63f),
    0x454f16b1: ('unknown_0x454f16b1', _decode_unknown_0x454f16b1),
    0x258c3e1b: ('sound_grenade_bounce', _decode_sound_grenade_bounce),
    0xaf6aad88: ('sound_grenade_explode', _decode_sound_grenade_explode),
}
