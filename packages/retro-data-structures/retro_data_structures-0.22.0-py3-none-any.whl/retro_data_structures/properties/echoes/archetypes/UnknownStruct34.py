# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct34(BaseProperty):
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    explosion: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    trail: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    mass: float = dataclasses.field(default=4.0)
    unknown_0x417f4a91: float = dataclasses.field(default=0.5)
    min_launch_speed: float = dataclasses.field(default=15.0)
    max_launch_speed: float = dataclasses.field(default=20.0)
    unknown_0xfbcdb101: int = dataclasses.field(default=5)
    sound_bounce: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_explode: int = dataclasses.field(default=0, metadata={'sound': True})
    max_turn_angle: float = dataclasses.field(default=30.0)
    unknown_0x47f99fbc: float = dataclasses.field(default=2.0)
    min_generation: int = dataclasses.field(default=0)
    max_generation: int = dataclasses.field(default=3)
    unknown_0xfbf8ea0a: float = dataclasses.field(default=40.0)
    allow_lock_on: bool = dataclasses.field(default=True)

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data, default_override={'di_weapon_type': 9, 'di_damage': 5.0, 'di_knock_back_power': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd8\xc6\xd1\\')  # 0xd8c6d15c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.explosion))

        data.write(b'\xb6\x8cm\x96')  # 0xb68c6d96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.effect))

        data.write(b'\xcb\x0b\x91\x9b')  # 0xcb0b919b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.trail))

        data.write(b'u\xdb\xb3u')  # 0x75dbb375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mass))

        data.write(b'A\x7fJ\x91')  # 0x417f4a91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x417f4a91))

        data.write(b'P\xa1\x9b\x1f')  # 0x50a19b1f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_launch_speed))

        data.write(b'\xf7\x95\x1bf')  # 0xf7951b66
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_launch_speed))

        data.write(b'\xfb\xcd\xb1\x01')  # 0xfbcdb101
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xfbcdb101))

        data.write(b'gX\xbf\x01')  # 0x6758bf01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_bounce))

        data.write(b'RJ\x80s')  # 0x524a8073
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_explode))

        data.write(b"P\xe4e'")  # 0x50e46527
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_turn_angle))

        data.write(b'G\xf9\x9f\xbc')  # 0x47f99fbc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x47f99fbc))

        data.write(b'\xdcZ\xf4\x1e')  # 0xdc5af41e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.min_generation))

        data.write(b'\x8d\xa3OC')  # 0x8da34f43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_generation))

        data.write(b'\xfb\xf8\xea\n')  # 0xfbf8ea0a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfbf8ea0a))

        data.write(b'\x98\xd2\x1b"')  # 0x98d21b22
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_lock_on))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            health=HealthInfo.from_json(data['health']),
            damage=DamageInfo.from_json(data['damage']),
            explosion=data['explosion'],
            effect=data['effect'],
            trail=data['trail'],
            mass=data['mass'],
            unknown_0x417f4a91=data['unknown_0x417f4a91'],
            min_launch_speed=data['min_launch_speed'],
            max_launch_speed=data['max_launch_speed'],
            unknown_0xfbcdb101=data['unknown_0xfbcdb101'],
            sound_bounce=data['sound_bounce'],
            sound_explode=data['sound_explode'],
            max_turn_angle=data['max_turn_angle'],
            unknown_0x47f99fbc=data['unknown_0x47f99fbc'],
            min_generation=data['min_generation'],
            max_generation=data['max_generation'],
            unknown_0xfbf8ea0a=data['unknown_0xfbf8ea0a'],
            allow_lock_on=data['allow_lock_on'],
        )

    def to_json(self) -> dict:
        return {
            'health': self.health.to_json(),
            'damage': self.damage.to_json(),
            'explosion': self.explosion,
            'effect': self.effect,
            'trail': self.trail,
            'mass': self.mass,
            'unknown_0x417f4a91': self.unknown_0x417f4a91,
            'min_launch_speed': self.min_launch_speed,
            'max_launch_speed': self.max_launch_speed,
            'unknown_0xfbcdb101': self.unknown_0xfbcdb101,
            'sound_bounce': self.sound_bounce,
            'sound_explode': self.sound_explode,
            'max_turn_angle': self.max_turn_angle,
            'unknown_0x47f99fbc': self.unknown_0x47f99fbc,
            'min_generation': self.min_generation,
            'max_generation': self.max_generation,
            'unknown_0xfbf8ea0a': self.unknown_0xfbf8ea0a,
            'allow_lock_on': self.allow_lock_on,
        }

    def _dependencies_for_health(self, asset_manager):
        yield from self.health.dependencies_for(asset_manager)

    def _dependencies_for_damage(self, asset_manager):
        yield from self.damage.dependencies_for(asset_manager)

    def _dependencies_for_explosion(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.explosion)

    def _dependencies_for_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.effect)

    def _dependencies_for_trail(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.trail)

    def _dependencies_for_sound_bounce(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_bounce)

    def _dependencies_for_sound_explode(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_explode)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_health, "health", "HealthInfo"),
            (self._dependencies_for_damage, "damage", "DamageInfo"),
            (self._dependencies_for_explosion, "explosion", "AssetId"),
            (self._dependencies_for_effect, "effect", "AssetId"),
            (self._dependencies_for_trail, "trail", "AssetId"),
            (self._dependencies_for_sound_bounce, "sound_bounce", "int"),
            (self._dependencies_for_sound_explode, "sound_explode", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct34.{field_name} ({field_type}): {e}"
                )


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 9, 'di_damage': 5.0, 'di_knock_back_power': 1.0})


def _decode_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_trail(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x417f4a91(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_launch_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_launch_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfbcdb101(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_explode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_turn_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x47f99fbc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_generation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_generation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xfbf8ea0a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_allow_lock_on(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcf90d15e: ('health', _decode_health),
    0x337f9524: ('damage', _decode_damage),
    0xd8c6d15c: ('explosion', _decode_explosion),
    0xb68c6d96: ('effect', _decode_effect),
    0xcb0b919b: ('trail', _decode_trail),
    0x75dbb375: ('mass', _decode_mass),
    0x417f4a91: ('unknown_0x417f4a91', _decode_unknown_0x417f4a91),
    0x50a19b1f: ('min_launch_speed', _decode_min_launch_speed),
    0xf7951b66: ('max_launch_speed', _decode_max_launch_speed),
    0xfbcdb101: ('unknown_0xfbcdb101', _decode_unknown_0xfbcdb101),
    0x6758bf01: ('sound_bounce', _decode_sound_bounce),
    0x524a8073: ('sound_explode', _decode_sound_explode),
    0x50e46527: ('max_turn_angle', _decode_max_turn_angle),
    0x47f99fbc: ('unknown_0x47f99fbc', _decode_unknown_0x47f99fbc),
    0xdc5af41e: ('min_generation', _decode_min_generation),
    0x8da34f43: ('max_generation', _decode_max_generation),
    0xfbf8ea0a: ('unknown_0xfbf8ea0a', _decode_unknown_0xfbf8ea0a),
    0x98d21b22: ('allow_lock_on', _decode_allow_lock_on),
}
