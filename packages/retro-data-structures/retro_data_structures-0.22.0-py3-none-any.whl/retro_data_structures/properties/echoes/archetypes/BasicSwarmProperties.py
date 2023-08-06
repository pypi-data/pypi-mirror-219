# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class BasicSwarmProperties(BaseProperty):
    contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_wait_time: float = dataclasses.field(default=1.0)
    collision_radius: float = dataclasses.field(default=0.30000001192092896)
    touch_radius: float = dataclasses.field(default=0.699999988079071)
    damage_radius: float = dataclasses.field(default=0.0)
    speed: float = dataclasses.field(default=3.0)
    count: int = dataclasses.field(default=50)
    max_count: int = dataclasses.field(default=0)
    influence_radius: float = dataclasses.field(default=2.5)
    unknown_0x61959f0d: float = dataclasses.field(default=1.0)
    alignment_priority: float = dataclasses.field(default=0.699999988079071)
    separation_priority: float = dataclasses.field(default=0.4000000059604645)
    path_following_priority: float = dataclasses.field(default=0.699999988079071)
    player_attract_priority: float = dataclasses.field(default=0.699999988079071)
    player_attract_distance: float = dataclasses.field(default=10.0)
    spawn_speed: float = dataclasses.field(default=6.0)
    attacker_count: int = dataclasses.field(default=5)
    attack_proximity: float = dataclasses.field(default=0.0)
    attack_timer: float = dataclasses.field(default=0.0)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    damage_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    death_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0x84f81f55: int = dataclasses.field(default=5)
    unknown_0xe1bd61d8: float = dataclasses.field(default=1.0)
    turn_rate: float = dataclasses.field(default=90.0)
    unknown_0xc2208b0f: bool = dataclasses.field(default=False)
    unknown_0x7eb5d9e8: bool = dataclasses.field(default=False)
    is_orbitable: bool = dataclasses.field(default=True)
    unknown_0xbc01a28e: bool = dataclasses.field(default=False)
    locomotion_looped_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    attack_looped_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0xd2986c43: float = dataclasses.field(default=0.0)
    max_audible_distance: float = dataclasses.field(default=100.0)
    min_volume: int = dataclasses.field(default=20)
    max_volume: int = dataclasses.field(default=127)
    freeze_duration: float = dataclasses.field(default=5.0)
    life_time: float = dataclasses.field(default=100.0)

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
        data.write(b'\x00%')  # 37 properties

        data.write(b'\xd7VAn')  # 0xd756416e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_radius': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe0\xcd\xc7\xe3')  # 0xe0cdc7e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_wait_time))

        data.write(b'\x8aj\xb19')  # 0x8a6ab139
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_radius))

        data.write(b'\x06\x8c\x8e\x81')  # 0x68c8e81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.touch_radius))

        data.write(b'\x0fY\x879')  # 0xf598739
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_radius))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'2\x91\xb8\xa2')  # 0x3291b8a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.count))

        data.write(b'T\xb6\x8cL')  # 0x54b68c4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_count))

        data.write(b'\xb1`E\x0e')  # 0xb160450e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.influence_radius))

        data.write(b'a\x95\x9f\r')  # 0x61959f0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61959f0d))

        data.write(b'HA\xf1\xde')  # 0x4841f1de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.alignment_priority))

        data.write(b'\xd2\x93\xeb\xc4')  # 0xd293ebc4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.separation_priority))

        data.write(b'\xae\x11\xf9u')  # 0xae11f975
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.path_following_priority))

        data.write(b'\x87\xed\xbc\xf1')  # 0x87edbcf1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_attract_priority))

        data.write(b'T+\xc8\x12')  # 0x542bc812
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_attract_distance))

        data.write(b'\xa3U\xc0O')  # 0xa355c04f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spawn_speed))

        data.write(b'R:@\\')  # 0x523a405c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.attacker_count))

        data.write(b'\x1c\xa0\xe7`')  # 0x1ca0e760
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_proximity))

        data.write(b'\x88\xdf>\xa8')  # 0x88df3ea8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_timer))

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data, default_override={'health': 2.0, 'hi_knock_back_resistance': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'8.@n')  # 0x382e406e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}F)0')  # 0x7d462930
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death_particle_effect))

        data.write(b'\x84\xf8\x1fU')  # 0x84f81f55
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x84f81f55))

        data.write(b'\xe1\xbda\xd8')  # 0xe1bd61d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe1bd61d8))

        data.write(b'\xe3M\xc7\x03')  # 0xe34dc703
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_rate))

        data.write(b'\xc2 \x8b\x0f')  # 0xc2208b0f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc2208b0f))

        data.write(b'~\xb5\xd9\xe8')  # 0x7eb5d9e8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7eb5d9e8))

        data.write(b'\x82k\xec\x80')  # 0x826bec80
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_orbitable))

        data.write(b'\xbc\x01\xa2\x8e')  # 0xbc01a28e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xbc01a28e))

        data.write(b'\x97\x07\x0f\x80')  # 0x97070f80
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.locomotion_looped_sound))

        data.write(b'\xaaE3W')  # 0xaa453357
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.attack_looped_sound))

        data.write(b'\xd2\x98lC')  # 0xd2986c43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd2986c43))

        data.write(b'!NH\xa0')  # 0x214e48a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_audible_distance))

        data.write(b'Wa\x94\x96')  # 0x57619496
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.min_volume))

        data.write(b'\xc7\x12\x84|')  # 0xc712847c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_volume))

        data.write(b'\xef;\xd8\xcf')  # 0xef3bd8cf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.freeze_duration))

        data.write(b'\xb0-\xe5U')  # 0xb02de555
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.life_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            contact_damage=DamageInfo.from_json(data['contact_damage']),
            damage_wait_time=data['damage_wait_time'],
            collision_radius=data['collision_radius'],
            touch_radius=data['touch_radius'],
            damage_radius=data['damage_radius'],
            speed=data['speed'],
            count=data['count'],
            max_count=data['max_count'],
            influence_radius=data['influence_radius'],
            unknown_0x61959f0d=data['unknown_0x61959f0d'],
            alignment_priority=data['alignment_priority'],
            separation_priority=data['separation_priority'],
            path_following_priority=data['path_following_priority'],
            player_attract_priority=data['player_attract_priority'],
            player_attract_distance=data['player_attract_distance'],
            spawn_speed=data['spawn_speed'],
            attacker_count=data['attacker_count'],
            attack_proximity=data['attack_proximity'],
            attack_timer=data['attack_timer'],
            health=HealthInfo.from_json(data['health']),
            damage_vulnerability=DamageVulnerability.from_json(data['damage_vulnerability']),
            death_particle_effect=data['death_particle_effect'],
            unknown_0x84f81f55=data['unknown_0x84f81f55'],
            unknown_0xe1bd61d8=data['unknown_0xe1bd61d8'],
            turn_rate=data['turn_rate'],
            unknown_0xc2208b0f=data['unknown_0xc2208b0f'],
            unknown_0x7eb5d9e8=data['unknown_0x7eb5d9e8'],
            is_orbitable=data['is_orbitable'],
            unknown_0xbc01a28e=data['unknown_0xbc01a28e'],
            locomotion_looped_sound=data['locomotion_looped_sound'],
            attack_looped_sound=data['attack_looped_sound'],
            unknown_0xd2986c43=data['unknown_0xd2986c43'],
            max_audible_distance=data['max_audible_distance'],
            min_volume=data['min_volume'],
            max_volume=data['max_volume'],
            freeze_duration=data['freeze_duration'],
            life_time=data['life_time'],
        )

    def to_json(self) -> dict:
        return {
            'contact_damage': self.contact_damage.to_json(),
            'damage_wait_time': self.damage_wait_time,
            'collision_radius': self.collision_radius,
            'touch_radius': self.touch_radius,
            'damage_radius': self.damage_radius,
            'speed': self.speed,
            'count': self.count,
            'max_count': self.max_count,
            'influence_radius': self.influence_radius,
            'unknown_0x61959f0d': self.unknown_0x61959f0d,
            'alignment_priority': self.alignment_priority,
            'separation_priority': self.separation_priority,
            'path_following_priority': self.path_following_priority,
            'player_attract_priority': self.player_attract_priority,
            'player_attract_distance': self.player_attract_distance,
            'spawn_speed': self.spawn_speed,
            'attacker_count': self.attacker_count,
            'attack_proximity': self.attack_proximity,
            'attack_timer': self.attack_timer,
            'health': self.health.to_json(),
            'damage_vulnerability': self.damage_vulnerability.to_json(),
            'death_particle_effect': self.death_particle_effect,
            'unknown_0x84f81f55': self.unknown_0x84f81f55,
            'unknown_0xe1bd61d8': self.unknown_0xe1bd61d8,
            'turn_rate': self.turn_rate,
            'unknown_0xc2208b0f': self.unknown_0xc2208b0f,
            'unknown_0x7eb5d9e8': self.unknown_0x7eb5d9e8,
            'is_orbitable': self.is_orbitable,
            'unknown_0xbc01a28e': self.unknown_0xbc01a28e,
            'locomotion_looped_sound': self.locomotion_looped_sound,
            'attack_looped_sound': self.attack_looped_sound,
            'unknown_0xd2986c43': self.unknown_0xd2986c43,
            'max_audible_distance': self.max_audible_distance,
            'min_volume': self.min_volume,
            'max_volume': self.max_volume,
            'freeze_duration': self.freeze_duration,
            'life_time': self.life_time,
        }

    def _dependencies_for_contact_damage(self, asset_manager):
        yield from self.contact_damage.dependencies_for(asset_manager)

    def _dependencies_for_health(self, asset_manager):
        yield from self.health.dependencies_for(asset_manager)

    def _dependencies_for_damage_vulnerability(self, asset_manager):
        yield from self.damage_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_death_particle_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.death_particle_effect)

    def _dependencies_for_locomotion_looped_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.locomotion_looped_sound)

    def _dependencies_for_attack_looped_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.attack_looped_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_contact_damage, "contact_damage", "DamageInfo"),
            (self._dependencies_for_health, "health", "HealthInfo"),
            (self._dependencies_for_damage_vulnerability, "damage_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_death_particle_effect, "death_particle_effect", "AssetId"),
            (self._dependencies_for_locomotion_looped_sound, "locomotion_looped_sound", "int"),
            (self._dependencies_for_attack_looped_sound, "attack_looped_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for BasicSwarmProperties.{field_name} ({field_type}): {e}"
                )


def _decode_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_radius': 5.0})


def _decode_damage_wait_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_touch_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_influence_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61959f0d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alignment_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_separation_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_path_following_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_attract_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_attract_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spawn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attacker_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_attack_proximity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size, default_override={'health': 2.0, 'hi_knock_back_resistance': 2.0})


def _decode_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_death_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x84f81f55(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xe1bd61d8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc2208b0f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7eb5d9e8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_orbitable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xbc01a28e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_locomotion_looped_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_attack_looped_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd2986c43(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_freeze_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd756416e: ('contact_damage', _decode_contact_damage),
    0xe0cdc7e3: ('damage_wait_time', _decode_damage_wait_time),
    0x8a6ab139: ('collision_radius', _decode_collision_radius),
    0x68c8e81: ('touch_radius', _decode_touch_radius),
    0xf598739: ('damage_radius', _decode_damage_radius),
    0x6392404e: ('speed', _decode_speed),
    0x3291b8a2: ('count', _decode_count),
    0x54b68c4c: ('max_count', _decode_max_count),
    0xb160450e: ('influence_radius', _decode_influence_radius),
    0x61959f0d: ('unknown_0x61959f0d', _decode_unknown_0x61959f0d),
    0x4841f1de: ('alignment_priority', _decode_alignment_priority),
    0xd293ebc4: ('separation_priority', _decode_separation_priority),
    0xae11f975: ('path_following_priority', _decode_path_following_priority),
    0x87edbcf1: ('player_attract_priority', _decode_player_attract_priority),
    0x542bc812: ('player_attract_distance', _decode_player_attract_distance),
    0xa355c04f: ('spawn_speed', _decode_spawn_speed),
    0x523a405c: ('attacker_count', _decode_attacker_count),
    0x1ca0e760: ('attack_proximity', _decode_attack_proximity),
    0x88df3ea8: ('attack_timer', _decode_attack_timer),
    0xcf90d15e: ('health', _decode_health),
    0x382e406e: ('damage_vulnerability', _decode_damage_vulnerability),
    0x7d462930: ('death_particle_effect', _decode_death_particle_effect),
    0x84f81f55: ('unknown_0x84f81f55', _decode_unknown_0x84f81f55),
    0xe1bd61d8: ('unknown_0xe1bd61d8', _decode_unknown_0xe1bd61d8),
    0xe34dc703: ('turn_rate', _decode_turn_rate),
    0xc2208b0f: ('unknown_0xc2208b0f', _decode_unknown_0xc2208b0f),
    0x7eb5d9e8: ('unknown_0x7eb5d9e8', _decode_unknown_0x7eb5d9e8),
    0x826bec80: ('is_orbitable', _decode_is_orbitable),
    0xbc01a28e: ('unknown_0xbc01a28e', _decode_unknown_0xbc01a28e),
    0x97070f80: ('locomotion_looped_sound', _decode_locomotion_looped_sound),
    0xaa453357: ('attack_looped_sound', _decode_attack_looped_sound),
    0xd2986c43: ('unknown_0xd2986c43', _decode_unknown_0xd2986c43),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x57619496: ('min_volume', _decode_min_volume),
    0xc712847c: ('max_volume', _decode_max_volume),
    0xef3bd8cf: ('freeze_duration', _decode_freeze_duration),
    0xb02de555: ('life_time', _decode_life_time),
}
