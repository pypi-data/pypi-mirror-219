# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.dkc_returns.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.dkc_returns.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class PatternedAITypedef(BaseProperty):
    mass: float = dataclasses.field(default=150.0)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_wait_time: float = dataclasses.field(default=2.0)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    collision_radius: float = dataclasses.field(default=1.0)
    collision_height: float = dataclasses.field(default=2.0)
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    step_up_height: float = dataclasses.field(default=0.10000000149011612)
    step_down_height: float = dataclasses.field(default=0.1599999964237213)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    fsmc_0x1749405b: AssetId = dataclasses.field(metadata={'asset_types': ['FSMC']}, default=default_asset_id)
    fsmc_0x1b21eeb2: AssetId = dataclasses.field(metadata={'asset_types': ['FSMC']}, default=default_asset_id)
    path_mesh_index: int = dataclasses.field(default=0)
    unknown_0x39a6dec3: float = dataclasses.field(default=5.0)
    unknown_0x47de2455: bool = dataclasses.field(default=False)
    creature_death_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0xc88ad680: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    creature_death_particle_effect_uses_creature_orientation: bool = dataclasses.field(default=True)
    ground_pound_slap_detection_radius: float = dataclasses.field(default=5.0)
    speed: float = dataclasses.field(default=1.0)
    turn_speed: float = dataclasses.field(default=120.0)
    unknown_0x6d892893: bool = dataclasses.field(default=True)
    detection_range: float = dataclasses.field(default=100.0)
    detection_height_range: float = dataclasses.field(default=0.0)
    detection_angle: float = dataclasses.field(default=60.0)
    min_attack_range: float = dataclasses.field(default=6.0)
    max_attack_range: float = dataclasses.field(default=11.0)
    average_attack_time: float = dataclasses.field(default=2.0)
    attack_time_variation: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'u\xdb\xb3u')  # 0x75dbb375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mass))

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7VAn')  # 0xd756416e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe0\xcd\xc7\xe3')  # 0xe0cdc7e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_wait_time))

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8aj\xb19')  # 0x8a6ab139
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_radius))

        data.write(b'0\x11\xb5\xdf')  # 0x3011b5df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_height))

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'\xd95Vt')  # 0xd9355674
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.step_up_height))

        data.write(b'\x88\xea\x81\xdb')  # 0x88ea81db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.step_down_height))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17I@[')  # 0x1749405b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fsmc_0x1749405b))

        data.write(b'\x1b!\xee\xb2')  # 0x1b21eeb2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fsmc_0x1b21eeb2))

        data.write(b'\x98\x16\x964')  # 0x98169634
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.path_mesh_index))

        data.write(b'9\xa6\xde\xc3')  # 0x39a6dec3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x39a6dec3))

        data.write(b'G\xde$U')  # 0x47de2455
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x47de2455))

        data.write(b'\xdf\xe7H\x95')  # 0xdfe74895
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.creature_death_particle_effect))

        data.write(b'\xc8\x8a\xd6\x80')  # 0xc88ad680
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xc88ad680))

        data.write(b'd\xc2&g')  # 0x64c22667
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'\xfd\x8a\x96\x92')  # 0xfd8a9692
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.creature_death_particle_effect_uses_creature_orientation))

        data.write(b'\xe0dD\x02')  # 0xe0644402
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_slap_detection_radius))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'\x02\x0cx\xbb')  # 0x20c78bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed))

        data.write(b'm\x89(\x93')  # 0x6d892893
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6d892893))

        data.write(b'\x8d\xb7~\xe4')  # 0x8db77ee4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_range))

        data.write(b'Q?\x04\xb8')  # 0x513f04b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_height_range))

        data.write(b'\x83\xdf\xc4\x0f')  # 0x83dfc40f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_angle))

        data.write(b'XCI\x16')  # 0x58434916
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_range))

        data.write(b'\xffw\xc9o')  # 0xff77c96f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_range))

        data.write(b'\xb0\xcf\xe0\x15')  # 0xb0cfe015
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.average_attack_time))

        data.write(b'\xc8\x0e2\x9b')  # 0xc80e329b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_time_variation))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            mass=data['mass'],
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            contact_damage=DamageInfo.from_json(data['contact_damage']),
            damage_wait_time=data['damage_wait_time'],
            health=HealthInfo.from_json(data['health']),
            collision_radius=data['collision_radius'],
            collision_height=data['collision_height'],
            collision_offset=Vector.from_json(data['collision_offset']),
            step_up_height=data['step_up_height'],
            step_down_height=data['step_down_height'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            fsmc_0x1749405b=data['fsmc_0x1749405b'],
            fsmc_0x1b21eeb2=data['fsmc_0x1b21eeb2'],
            path_mesh_index=data['path_mesh_index'],
            unknown_0x39a6dec3=data['unknown_0x39a6dec3'],
            unknown_0x47de2455=data['unknown_0x47de2455'],
            creature_death_particle_effect=data['creature_death_particle_effect'],
            unknown_0xc88ad680=data['unknown_0xc88ad680'],
            caud=data['caud'],
            creature_death_particle_effect_uses_creature_orientation=data['creature_death_particle_effect_uses_creature_orientation'],
            ground_pound_slap_detection_radius=data['ground_pound_slap_detection_radius'],
            speed=data['speed'],
            turn_speed=data['turn_speed'],
            unknown_0x6d892893=data['unknown_0x6d892893'],
            detection_range=data['detection_range'],
            detection_height_range=data['detection_height_range'],
            detection_angle=data['detection_angle'],
            min_attack_range=data['min_attack_range'],
            max_attack_range=data['max_attack_range'],
            average_attack_time=data['average_attack_time'],
            attack_time_variation=data['attack_time_variation'],
        )

    def to_json(self) -> dict:
        return {
            'mass': self.mass,
            'vulnerability': self.vulnerability.to_json(),
            'contact_damage': self.contact_damage.to_json(),
            'damage_wait_time': self.damage_wait_time,
            'health': self.health.to_json(),
            'collision_radius': self.collision_radius,
            'collision_height': self.collision_height,
            'collision_offset': self.collision_offset.to_json(),
            'step_up_height': self.step_up_height,
            'step_down_height': self.step_down_height,
            'character_animation_information': self.character_animation_information.to_json(),
            'fsmc_0x1749405b': self.fsmc_0x1749405b,
            'fsmc_0x1b21eeb2': self.fsmc_0x1b21eeb2,
            'path_mesh_index': self.path_mesh_index,
            'unknown_0x39a6dec3': self.unknown_0x39a6dec3,
            'unknown_0x47de2455': self.unknown_0x47de2455,
            'creature_death_particle_effect': self.creature_death_particle_effect,
            'unknown_0xc88ad680': self.unknown_0xc88ad680,
            'caud': self.caud,
            'creature_death_particle_effect_uses_creature_orientation': self.creature_death_particle_effect_uses_creature_orientation,
            'ground_pound_slap_detection_radius': self.ground_pound_slap_detection_radius,
            'speed': self.speed,
            'turn_speed': self.turn_speed,
            'unknown_0x6d892893': self.unknown_0x6d892893,
            'detection_range': self.detection_range,
            'detection_height_range': self.detection_height_range,
            'detection_angle': self.detection_angle,
            'min_attack_range': self.min_attack_range,
            'max_attack_range': self.max_attack_range,
            'average_attack_time': self.average_attack_time,
            'attack_time_variation': self.attack_time_variation,
        }


def _decode_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_wait_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_collision_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_step_up_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_step_down_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_fsmc_0x1749405b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fsmc_0x1b21eeb2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_path_mesh_index(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x39a6dec3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x47de2455(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_creature_death_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xc88ad680(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_creature_death_particle_effect_uses_creature_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ground_pound_slap_detection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6d892893(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_detection_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_height_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_average_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_time_variation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x75dbb375: ('mass', _decode_mass),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0xd756416e: ('contact_damage', _decode_contact_damage),
    0xe0cdc7e3: ('damage_wait_time', _decode_damage_wait_time),
    0xcf90d15e: ('health', _decode_health),
    0x8a6ab139: ('collision_radius', _decode_collision_radius),
    0x3011b5df: ('collision_height', _decode_collision_height),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xd9355674: ('step_up_height', _decode_step_up_height),
    0x88ea81db: ('step_down_height', _decode_step_down_height),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0x1749405b: ('fsmc_0x1749405b', _decode_fsmc_0x1749405b),
    0x1b21eeb2: ('fsmc_0x1b21eeb2', _decode_fsmc_0x1b21eeb2),
    0x98169634: ('path_mesh_index', _decode_path_mesh_index),
    0x39a6dec3: ('unknown_0x39a6dec3', _decode_unknown_0x39a6dec3),
    0x47de2455: ('unknown_0x47de2455', _decode_unknown_0x47de2455),
    0xdfe74895: ('creature_death_particle_effect', _decode_creature_death_particle_effect),
    0xc88ad680: ('unknown_0xc88ad680', _decode_unknown_0xc88ad680),
    0x64c22667: ('caud', _decode_caud),
    0xfd8a9692: ('creature_death_particle_effect_uses_creature_orientation', _decode_creature_death_particle_effect_uses_creature_orientation),
    0xe0644402: ('ground_pound_slap_detection_radius', _decode_ground_pound_slap_detection_radius),
    0x6392404e: ('speed', _decode_speed),
    0x20c78bb: ('turn_speed', _decode_turn_speed),
    0x6d892893: ('unknown_0x6d892893', _decode_unknown_0x6d892893),
    0x8db77ee4: ('detection_range', _decode_detection_range),
    0x513f04b8: ('detection_height_range', _decode_detection_height_range),
    0x83dfc40f: ('detection_angle', _decode_detection_angle),
    0x58434916: ('min_attack_range', _decode_min_attack_range),
    0xff77c96f: ('max_attack_range', _decode_max_attack_range),
    0xb0cfe015: ('average_attack_time', _decode_average_attack_time),
    0xc80e329b: ('attack_time_variation', _decode_attack_time_variation),
}
