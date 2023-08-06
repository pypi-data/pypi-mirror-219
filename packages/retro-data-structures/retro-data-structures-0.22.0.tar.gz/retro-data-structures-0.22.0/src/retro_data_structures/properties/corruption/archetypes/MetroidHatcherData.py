# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.FlyerMovementMode import FlyerMovementMode
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class MetroidHatcherData(BaseProperty):
    hearing_range: float = dataclasses.field(default=25.0)
    lose_interest_range: float = dataclasses.field(default=50.0)
    lose_interest_time: float = dataclasses.field(default=10.0)
    unknown_0xfe4588a1: float = dataclasses.field(default=50.0)
    unknown_0xc2688b41: float = dataclasses.field(default=0.5)
    unknown_0x7b0cc30d: float = dataclasses.field(default=60.0)
    damage_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    body_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    brain_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    brain_x_ray_radius: float = dataclasses.field(default=1.0)
    brain_radius: float = dataclasses.field(default=0.10000000149011612)
    leg_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0xb9e0c90d: float = dataclasses.field(default=20.0)
    unknown_0x81d39802: float = dataclasses.field(default=0.10000000149011612)
    tentacle_regrow_time: float = dataclasses.field(default=0.33329999446868896)
    unknown_0xf79a10b0: float = dataclasses.field(default=0.5)
    unknown_0xc550a481: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x95e7a2c2: float = dataclasses.field(default=10.0)
    unknown_0x76ba1c18: float = dataclasses.field(default=15.0)
    unknown_0xe08106ed: float = dataclasses.field(default=5.0)
    unknown_0x88d7c540: float = dataclasses.field(default=5.0)
    unknown_0xace62367: float = dataclasses.field(default=5.0)
    unknown_0x620b1b3d: float = dataclasses.field(default=5.0)
    max_attack_height: float = dataclasses.field(default=10.0)
    min_attack_height: float = dataclasses.field(default=9.0)
    max_attack_forward: float = dataclasses.field(default=16.0)
    min_attack_forward: float = dataclasses.field(default=14.0)
    unknown_0x0978b98a: float = dataclasses.field(default=10.0)
    unknown_0xcfcd32bb: float = dataclasses.field(default=-1.5)
    unknown_0x17d71349: float = dataclasses.field(default=8.0)
    recheck_path_time: float = dataclasses.field(default=1.0)
    recheck_path_distance: float = dataclasses.field(default=5.0)
    max_num_metroids: int = dataclasses.field(default=3)
    auto_spawn: bool = dataclasses.field(default=False)
    max_spawn_delay: float = dataclasses.field(default=30.0)
    min_spawn_delay: float = dataclasses.field(default=20.0)
    unknown_0x6089191d: int = dataclasses.field(default=10)
    unknown_0x258b5a9f: int = dataclasses.field(default=5)
    unknown_0x2ae610e5: float = dataclasses.field(default=20.0)
    hatch_chance: float = dataclasses.field(default=0.699999988079071)
    maya_double: float = dataclasses.field(default=0.5)
    unknown_0x3fee1ba4: float = dataclasses.field(default=0.5)
    spin_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    max_spin_attack_delay: float = dataclasses.field(default=20.0)
    min_spin_attack_delay: float = dataclasses.field(default=10.0)
    unknown_0xbeaf2105: float = dataclasses.field(default=15.0)
    unknown_0x54ff4d38: float = dataclasses.field(default=3.0)
    unknown_0xb29fe2d9: float = dataclasses.field(default=2.0)
    dodge_chance: float = dataclasses.field(default=0.0010000000474974513)
    unknown_0x42647ad7: float = dataclasses.field(default=100.0)
    unknown_0xa404d536: float = dataclasses.field(default=15.0)
    unknown_0x248d3599: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xbfd77e62: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xcdaa2c74: float = dataclasses.field(default=30.0)
    unknown_0x2bca8395: float = dataclasses.field(default=10.0)
    patrol: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    attack_path: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    combat: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    stab_attack: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0x6ca56014: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0xe20e51c3: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0x25a68a0e: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0xd9b5d506: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0x8bb1c3a2: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    stunned: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0xfb2ddfad: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    dash: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    flyer_movement_mode_0x5fe13a7b: FlyerMovementMode = dataclasses.field(default_factory=FlyerMovementMode)
    claw: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    char_0x4d7dbeab: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    char_0xa17c09bb: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    char_0x11dc2dab: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    char_0xfddd9abb: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0xc99cee00: float = dataclasses.field(default=0.6000000238418579)
    unknown_0x2ffc41e1: float = dataclasses.field(default=0.4000000059604645)
    unknown_0x7f5d9ab7: float = dataclasses.field(default=0.800000011920929)
    unknown_0x993d3556: float = dataclasses.field(default=0.5)
    unknown_0x08efeb79: float = dataclasses.field(default=0.0)
    unknown_0xee8f4498: float = dataclasses.field(default=0.0)
    unknown_0xc24d8fbd: float = dataclasses.field(default=20.0)
    unknown_0x242d205c: float = dataclasses.field(default=15.0)
    stun_threshold: float = dataclasses.field(default=30.0)
    electric_ball_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    sound_ball_effect: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    electric_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    sound_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    leg_hit_splash: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

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
        data.write(b'\x00W')  # 87 properties

        data.write(b'%GEP')  # 0x25474550
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hearing_range))

        data.write(b'GO\xa5\x89')  # 0x474fa589
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lose_interest_range))

        data.write(b'\xf8\xb0\xc2\xbb')  # 0xf8b0c2bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lose_interest_time))

        data.write(b'\xfeE\x88\xa1')  # 0xfe4588a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfe4588a1))

        data.write(b'\xc2h\x8bA')  # 0xc2688b41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc2688b41))

        data.write(b'{\x0c\xc3\r')  # 0x7b0cc30d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7b0cc30d))

        data.write(b't+36')  # 0x742b3336
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\r\x920\xd1')  # 0xd9230d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.body_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$:\xb1\r')  # 0x243ab10d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.brain_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01!\x15\xa2')  # 0x12115a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.brain_x_ray_radius))

        data.write(b'\xa1*D\t')  # 0xa12a4409
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.brain_radius))

        data.write(b'\x9f\x0f\xf8R')  # 0x9f0ff852
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.leg_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9\xe0\xc9\r')  # 0xb9e0c90d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb9e0c90d))

        data.write(b'\x81\xd3\x98\x02')  # 0x81d39802
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x81d39802))

        data.write(b'\xba\x00-\xcb')  # 0xba002dcb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tentacle_regrow_time))

        data.write(b'\xf7\x9a\x10\xb0')  # 0xf79a10b0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf79a10b0))

        data.write(b'\xc5P\xa4\x81')  # 0xc550a481
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc550a481))

        data.write(b'\x95\xe7\xa2\xc2')  # 0x95e7a2c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95e7a2c2))

        data.write(b'v\xba\x1c\x18')  # 0x76ba1c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76ba1c18))

        data.write(b'\xe0\x81\x06\xed')  # 0xe08106ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe08106ed))

        data.write(b'\x88\xd7\xc5@')  # 0x88d7c540
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x88d7c540))

        data.write(b'\xac\xe6#g')  # 0xace62367
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xace62367))

        data.write(b'b\x0b\x1b=')  # 0x620b1b3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x620b1b3d))

        data.write(b'\xe1\xaeQ\xd8')  # 0xe1ae51d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_height))

        data.write(b'\xc8\xd0\xac\xc0')  # 0xc8d0acc0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_height))

        data.write(b'\xf3\xe8\x01-')  # 0xf3e8012d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_forward))

        data.write(b'\xe0\xad\xe7\x86')  # 0xe0ade786
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_forward))

        data.write(b'\tx\xb9\x8a')  # 0x978b98a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0978b98a))

        data.write(b'\xcf\xcd2\xbb')  # 0xcfcd32bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcfcd32bb))

        data.write(b'\x17\xd7\x13I')  # 0x17d71349
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x17d71349))

        data.write(b'\x9a\xa9\x0bk')  # 0x9aa90b6b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recheck_path_time))

        data.write(b'v&\xec\x89')  # 0x7626ec89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.recheck_path_distance))

        data.write(b'y\x15\xe2\xb3')  # 0x7915e2b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_num_metroids))

        data.write(b'\xcc\xc0\xcf\x92')  # 0xccc0cf92
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_spawn))

        data.write(b'u\xe0\xb0\xa7')  # 0x75e0b0a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_spawn_delay))

        data.write(b'&F\xa8C')  # 0x2646a843
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_spawn_delay))

        data.write(b'`\x89\x19\x1d')  # 0x6089191d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6089191d))

        data.write(b'%\x8bZ\x9f')  # 0x258b5a9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x258b5a9f))

        data.write(b'*\xe6\x10\xe5')  # 0x2ae610e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2ae610e5))

        data.write(b'5K\xae1')  # 0x354bae31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hatch_chance))

        data.write(b'\xf4\xb2\xc8\x01')  # 0xf4b2c801
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maya_double))

        data.write(b'?\xee\x1b\xa4')  # 0x3fee1ba4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3fee1ba4))

        data.write(b'\xcf\xac\xffS')  # 0xcfacff53
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spin_attack_damage.to_stream(data, default_override={'di_damage': 30.0, 'di_knock_back_power': 20.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'l\xb6\xd8\xc7')  # 0x6cb6d8c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_spin_attack_delay))

        data.write(b'h,\xe9\xed')  # 0x682ce9ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_spin_attack_delay))

        data.write(b'\xbe\xaf!\x05')  # 0xbeaf2105
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbeaf2105))

        data.write(b'T\xffM8')  # 0x54ff4d38
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x54ff4d38))

        data.write(b'\xb2\x9f\xe2\xd9')  # 0xb29fe2d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb29fe2d9))

        data.write(b'G\xbe2\x98')  # 0x47be3298
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_chance))

        data.write(b'Bdz\xd7')  # 0x42647ad7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x42647ad7))

        data.write(b'\xa4\x04\xd56')  # 0xa404d536
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa404d536))

        data.write(b'$\x8d5\x99')  # 0x248d3599
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x248d3599))

        data.write(b'\xbf\xd7~b')  # 0xbfd77e62
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbfd77e62))

        data.write(b'\xcd\xaa,t')  # 0xcdaa2c74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcdaa2c74))

        data.write(b'+\xca\x83\x95')  # 0x2bca8395
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2bca8395))

        data.write(b'\xcc\xdd:\xca')  # 0xccdd3aca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patrol.to_stream(data, default_override={'speed': 3.0, 'acceleration': 1.0, 'facing_turn_rate': 30.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc8E\xd3\xc0')  # 0xc845d3c0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_path.to_stream(data, default_override={'speed': 3.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcc}.\x98')  # 0xcc7d2e98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.combat.to_stream(data, default_override={'speed': 3.0, 'acceleration': 10.0, 'turn_threshold': 181.0, 'floor_buffer': 11.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9\xc3\xdb\x94')  # 0xb9c3db94
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stab_attack.to_stream(data, default_override={'speed': 0.10000000149011612, 'acceleration': 10.0, 'turn_rate': 10800.0, 'facing_turn_rate': 120.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_max': 0.0, 'floor_buffer': 8.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'l\xa5`\x14')  # 0x6ca56014
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0x6ca56014.to_stream(data, default_override={'speed': 30.0, 'acceleration': 50.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_max': 0.0, 'floor_buffer': 3.5, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2\x0eQ\xc3')  # 0xe20e51c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0xe20e51c3.to_stream(data, default_override={'speed': 30.0, 'acceleration': 10.0, 'facing_turn_rate': 1.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_max': 1.0, 'floor_buffer': 5.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'%\xa6\x8a\x0e')  # 0x25a68a0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0x25a68a0e.to_stream(data, default_override={'speed': 1.0, 'acceleration': 10.0, 'turn_threshold': 181.0, 'height_variation_max': 0.0, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd9\xb5\xd5\x06')  # 0xd9b5d506
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0xd9b5d506.to_stream(data, default_override={'speed': 30.0, 'acceleration': 20.0, 'facing_turn_rate': 1.0, 'turn_threshold': 181.0, 'height_variation_max': 1.0, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\xb1\xc3\xa2')  # 0x8bb1c3a2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0x8bb1c3a2.to_stream(data, default_override={'speed': 1.0, 'acceleration': 10.0, 'turn_threshold': 181.0, 'height_variation_max': 1.0, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'8\x9c\xb5\x15')  # 0x389cb515
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stunned.to_stream(data, default_override={'speed': 5.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_max': 1.0, 'floor_buffer': 5.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfb-\xdf\xad')  # 0xfb2ddfad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0xfb2ddfad.to_stream(data, default_override={'speed': 5.0, 'acceleration': 10.0, 'facing_turn_rate': 15.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_min': 1.0, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc5X\xbc\r')  # 0xc558bc0d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dash.to_stream(data, default_override={'speed': 40.0, 'acceleration': 100.0, 'turn_rate': 360.0, 'turn_threshold': 181.0, 'avoidance_range': 1.0, 'height_variation_max': 0.5, 'floor_buffer': 13.0, 'ceiling_buffer': 8.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_\xe1:{')  # 0x5fe13a7b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flyer_movement_mode_0x5fe13a7b.to_stream(data, default_override={'acceleration': 20.0, 'turn_threshold': 181.0, 'floor_buffer': 12.0, 'ceiling_buffer': 12.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd8\xa1\x06')  # 0xfd38a106
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.claw.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'M}\xbe\xab')  # 0x4d7dbeab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.char_0x4d7dbeab.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1|\t\xbb')  # 0xa17c09bb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.char_0xa17c09bb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x11\xdc-\xab')  # 0x11dc2dab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.char_0x11dc2dab.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd\xdd\x9a\xbb')  # 0xfddd9abb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.char_0xfddd9abb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9\x9c\xee\x00')  # 0xc99cee00
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc99cee00))

        data.write(b'/\xfcA\xe1')  # 0x2ffc41e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2ffc41e1))

        data.write(b'\x7f]\x9a\xb7')  # 0x7f5d9ab7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7f5d9ab7))

        data.write(b'\x99=5V')  # 0x993d3556
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x993d3556))

        data.write(b'\x08\xef\xeby')  # 0x8efeb79
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x08efeb79))

        data.write(b'\xee\x8fD\x98')  # 0xee8f4498
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xee8f4498))

        data.write(b'\xc2M\x8f\xbd')  # 0xc24d8fbd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc24d8fbd))

        data.write(b'$- \\')  # 0x242d205c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x242d205c))

        data.write(b'[\xdd\x1eL')  # 0x5bdd1e4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_threshold))

        data.write(b'm\xa4\xa3\xb0')  # 0x6da4a3b0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.electric_ball_effect))

        data.write(b'?\xcd\x8bf')  # 0x3fcd8b66
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_ball_effect))

        data.write(b'\xcc\n\xf2\x87')  # 0xcc0af287
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.electric_visor_effect))

        data.write(b'\xa3\xe8\xecN')  # 0xa3e8ec4e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_visor_effect))

        data.write(b'\xf4\n\x9c\x9d')  # 0xf40a9c9d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.leg_hit_splash))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hearing_range=data['hearing_range'],
            lose_interest_range=data['lose_interest_range'],
            lose_interest_time=data['lose_interest_time'],
            unknown_0xfe4588a1=data['unknown_0xfe4588a1'],
            unknown_0xc2688b41=data['unknown_0xc2688b41'],
            unknown_0x7b0cc30d=data['unknown_0x7b0cc30d'],
            damage_vulnerability=DamageVulnerability.from_json(data['damage_vulnerability']),
            body_vulnerability=DamageVulnerability.from_json(data['body_vulnerability']),
            brain_vulnerability=DamageVulnerability.from_json(data['brain_vulnerability']),
            brain_x_ray_radius=data['brain_x_ray_radius'],
            brain_radius=data['brain_radius'],
            leg_vulnerability=DamageVulnerability.from_json(data['leg_vulnerability']),
            unknown_0xb9e0c90d=data['unknown_0xb9e0c90d'],
            unknown_0x81d39802=data['unknown_0x81d39802'],
            tentacle_regrow_time=data['tentacle_regrow_time'],
            unknown_0xf79a10b0=data['unknown_0xf79a10b0'],
            unknown_0xc550a481=data['unknown_0xc550a481'],
            unknown_0x95e7a2c2=data['unknown_0x95e7a2c2'],
            unknown_0x76ba1c18=data['unknown_0x76ba1c18'],
            unknown_0xe08106ed=data['unknown_0xe08106ed'],
            unknown_0x88d7c540=data['unknown_0x88d7c540'],
            unknown_0xace62367=data['unknown_0xace62367'],
            unknown_0x620b1b3d=data['unknown_0x620b1b3d'],
            max_attack_height=data['max_attack_height'],
            min_attack_height=data['min_attack_height'],
            max_attack_forward=data['max_attack_forward'],
            min_attack_forward=data['min_attack_forward'],
            unknown_0x0978b98a=data['unknown_0x0978b98a'],
            unknown_0xcfcd32bb=data['unknown_0xcfcd32bb'],
            unknown_0x17d71349=data['unknown_0x17d71349'],
            recheck_path_time=data['recheck_path_time'],
            recheck_path_distance=data['recheck_path_distance'],
            max_num_metroids=data['max_num_metroids'],
            auto_spawn=data['auto_spawn'],
            max_spawn_delay=data['max_spawn_delay'],
            min_spawn_delay=data['min_spawn_delay'],
            unknown_0x6089191d=data['unknown_0x6089191d'],
            unknown_0x258b5a9f=data['unknown_0x258b5a9f'],
            unknown_0x2ae610e5=data['unknown_0x2ae610e5'],
            hatch_chance=data['hatch_chance'],
            maya_double=data['maya_double'],
            unknown_0x3fee1ba4=data['unknown_0x3fee1ba4'],
            spin_attack_damage=DamageInfo.from_json(data['spin_attack_damage']),
            max_spin_attack_delay=data['max_spin_attack_delay'],
            min_spin_attack_delay=data['min_spin_attack_delay'],
            unknown_0xbeaf2105=data['unknown_0xbeaf2105'],
            unknown_0x54ff4d38=data['unknown_0x54ff4d38'],
            unknown_0xb29fe2d9=data['unknown_0xb29fe2d9'],
            dodge_chance=data['dodge_chance'],
            unknown_0x42647ad7=data['unknown_0x42647ad7'],
            unknown_0xa404d536=data['unknown_0xa404d536'],
            unknown_0x248d3599=data['unknown_0x248d3599'],
            unknown_0xbfd77e62=data['unknown_0xbfd77e62'],
            unknown_0xcdaa2c74=data['unknown_0xcdaa2c74'],
            unknown_0x2bca8395=data['unknown_0x2bca8395'],
            patrol=FlyerMovementMode.from_json(data['patrol']),
            attack_path=FlyerMovementMode.from_json(data['attack_path']),
            combat=FlyerMovementMode.from_json(data['combat']),
            stab_attack=FlyerMovementMode.from_json(data['stab_attack']),
            flyer_movement_mode_0x6ca56014=FlyerMovementMode.from_json(data['flyer_movement_mode_0x6ca56014']),
            flyer_movement_mode_0xe20e51c3=FlyerMovementMode.from_json(data['flyer_movement_mode_0xe20e51c3']),
            flyer_movement_mode_0x25a68a0e=FlyerMovementMode.from_json(data['flyer_movement_mode_0x25a68a0e']),
            flyer_movement_mode_0xd9b5d506=FlyerMovementMode.from_json(data['flyer_movement_mode_0xd9b5d506']),
            flyer_movement_mode_0x8bb1c3a2=FlyerMovementMode.from_json(data['flyer_movement_mode_0x8bb1c3a2']),
            stunned=FlyerMovementMode.from_json(data['stunned']),
            flyer_movement_mode_0xfb2ddfad=FlyerMovementMode.from_json(data['flyer_movement_mode_0xfb2ddfad']),
            dash=FlyerMovementMode.from_json(data['dash']),
            flyer_movement_mode_0x5fe13a7b=FlyerMovementMode.from_json(data['flyer_movement_mode_0x5fe13a7b']),
            claw=AnimationParameters.from_json(data['claw']),
            char_0x4d7dbeab=AnimationParameters.from_json(data['char_0x4d7dbeab']),
            char_0xa17c09bb=AnimationParameters.from_json(data['char_0xa17c09bb']),
            char_0x11dc2dab=AnimationParameters.from_json(data['char_0x11dc2dab']),
            char_0xfddd9abb=AnimationParameters.from_json(data['char_0xfddd9abb']),
            unknown_0xc99cee00=data['unknown_0xc99cee00'],
            unknown_0x2ffc41e1=data['unknown_0x2ffc41e1'],
            unknown_0x7f5d9ab7=data['unknown_0x7f5d9ab7'],
            unknown_0x993d3556=data['unknown_0x993d3556'],
            unknown_0x08efeb79=data['unknown_0x08efeb79'],
            unknown_0xee8f4498=data['unknown_0xee8f4498'],
            unknown_0xc24d8fbd=data['unknown_0xc24d8fbd'],
            unknown_0x242d205c=data['unknown_0x242d205c'],
            stun_threshold=data['stun_threshold'],
            electric_ball_effect=data['electric_ball_effect'],
            sound_ball_effect=data['sound_ball_effect'],
            electric_visor_effect=data['electric_visor_effect'],
            sound_visor_effect=data['sound_visor_effect'],
            leg_hit_splash=data['leg_hit_splash'],
        )

    def to_json(self) -> dict:
        return {
            'hearing_range': self.hearing_range,
            'lose_interest_range': self.lose_interest_range,
            'lose_interest_time': self.lose_interest_time,
            'unknown_0xfe4588a1': self.unknown_0xfe4588a1,
            'unknown_0xc2688b41': self.unknown_0xc2688b41,
            'unknown_0x7b0cc30d': self.unknown_0x7b0cc30d,
            'damage_vulnerability': self.damage_vulnerability.to_json(),
            'body_vulnerability': self.body_vulnerability.to_json(),
            'brain_vulnerability': self.brain_vulnerability.to_json(),
            'brain_x_ray_radius': self.brain_x_ray_radius,
            'brain_radius': self.brain_radius,
            'leg_vulnerability': self.leg_vulnerability.to_json(),
            'unknown_0xb9e0c90d': self.unknown_0xb9e0c90d,
            'unknown_0x81d39802': self.unknown_0x81d39802,
            'tentacle_regrow_time': self.tentacle_regrow_time,
            'unknown_0xf79a10b0': self.unknown_0xf79a10b0,
            'unknown_0xc550a481': self.unknown_0xc550a481,
            'unknown_0x95e7a2c2': self.unknown_0x95e7a2c2,
            'unknown_0x76ba1c18': self.unknown_0x76ba1c18,
            'unknown_0xe08106ed': self.unknown_0xe08106ed,
            'unknown_0x88d7c540': self.unknown_0x88d7c540,
            'unknown_0xace62367': self.unknown_0xace62367,
            'unknown_0x620b1b3d': self.unknown_0x620b1b3d,
            'max_attack_height': self.max_attack_height,
            'min_attack_height': self.min_attack_height,
            'max_attack_forward': self.max_attack_forward,
            'min_attack_forward': self.min_attack_forward,
            'unknown_0x0978b98a': self.unknown_0x0978b98a,
            'unknown_0xcfcd32bb': self.unknown_0xcfcd32bb,
            'unknown_0x17d71349': self.unknown_0x17d71349,
            'recheck_path_time': self.recheck_path_time,
            'recheck_path_distance': self.recheck_path_distance,
            'max_num_metroids': self.max_num_metroids,
            'auto_spawn': self.auto_spawn,
            'max_spawn_delay': self.max_spawn_delay,
            'min_spawn_delay': self.min_spawn_delay,
            'unknown_0x6089191d': self.unknown_0x6089191d,
            'unknown_0x258b5a9f': self.unknown_0x258b5a9f,
            'unknown_0x2ae610e5': self.unknown_0x2ae610e5,
            'hatch_chance': self.hatch_chance,
            'maya_double': self.maya_double,
            'unknown_0x3fee1ba4': self.unknown_0x3fee1ba4,
            'spin_attack_damage': self.spin_attack_damage.to_json(),
            'max_spin_attack_delay': self.max_spin_attack_delay,
            'min_spin_attack_delay': self.min_spin_attack_delay,
            'unknown_0xbeaf2105': self.unknown_0xbeaf2105,
            'unknown_0x54ff4d38': self.unknown_0x54ff4d38,
            'unknown_0xb29fe2d9': self.unknown_0xb29fe2d9,
            'dodge_chance': self.dodge_chance,
            'unknown_0x42647ad7': self.unknown_0x42647ad7,
            'unknown_0xa404d536': self.unknown_0xa404d536,
            'unknown_0x248d3599': self.unknown_0x248d3599,
            'unknown_0xbfd77e62': self.unknown_0xbfd77e62,
            'unknown_0xcdaa2c74': self.unknown_0xcdaa2c74,
            'unknown_0x2bca8395': self.unknown_0x2bca8395,
            'patrol': self.patrol.to_json(),
            'attack_path': self.attack_path.to_json(),
            'combat': self.combat.to_json(),
            'stab_attack': self.stab_attack.to_json(),
            'flyer_movement_mode_0x6ca56014': self.flyer_movement_mode_0x6ca56014.to_json(),
            'flyer_movement_mode_0xe20e51c3': self.flyer_movement_mode_0xe20e51c3.to_json(),
            'flyer_movement_mode_0x25a68a0e': self.flyer_movement_mode_0x25a68a0e.to_json(),
            'flyer_movement_mode_0xd9b5d506': self.flyer_movement_mode_0xd9b5d506.to_json(),
            'flyer_movement_mode_0x8bb1c3a2': self.flyer_movement_mode_0x8bb1c3a2.to_json(),
            'stunned': self.stunned.to_json(),
            'flyer_movement_mode_0xfb2ddfad': self.flyer_movement_mode_0xfb2ddfad.to_json(),
            'dash': self.dash.to_json(),
            'flyer_movement_mode_0x5fe13a7b': self.flyer_movement_mode_0x5fe13a7b.to_json(),
            'claw': self.claw.to_json(),
            'char_0x4d7dbeab': self.char_0x4d7dbeab.to_json(),
            'char_0xa17c09bb': self.char_0xa17c09bb.to_json(),
            'char_0x11dc2dab': self.char_0x11dc2dab.to_json(),
            'char_0xfddd9abb': self.char_0xfddd9abb.to_json(),
            'unknown_0xc99cee00': self.unknown_0xc99cee00,
            'unknown_0x2ffc41e1': self.unknown_0x2ffc41e1,
            'unknown_0x7f5d9ab7': self.unknown_0x7f5d9ab7,
            'unknown_0x993d3556': self.unknown_0x993d3556,
            'unknown_0x08efeb79': self.unknown_0x08efeb79,
            'unknown_0xee8f4498': self.unknown_0xee8f4498,
            'unknown_0xc24d8fbd': self.unknown_0xc24d8fbd,
            'unknown_0x242d205c': self.unknown_0x242d205c,
            'stun_threshold': self.stun_threshold,
            'electric_ball_effect': self.electric_ball_effect,
            'sound_ball_effect': self.sound_ball_effect,
            'electric_visor_effect': self.electric_visor_effect,
            'sound_visor_effect': self.sound_visor_effect,
            'leg_hit_splash': self.leg_hit_splash,
        }


def _decode_hearing_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lose_interest_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lose_interest_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfe4588a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc2688b41(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7b0cc30d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_body_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_brain_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_brain_x_ray_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_brain_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_leg_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0xb9e0c90d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x81d39802(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tentacle_regrow_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf79a10b0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc550a481(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x95e7a2c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ba1c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe08106ed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x88d7c540(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xace62367(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x620b1b3d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_forward(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_attack_forward(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0978b98a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcfcd32bb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x17d71349(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recheck_path_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_recheck_path_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_num_metroids(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_auto_spawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_spawn_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_spawn_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6089191d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x258b5a9f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x2ae610e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hatch_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maya_double(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3fee1ba4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spin_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_damage': 30.0, 'di_knock_back_power': 20.0})


def _decode_max_spin_attack_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_spin_attack_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbeaf2105(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x54ff4d38(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb29fe2d9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x42647ad7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa404d536(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x248d3599(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbfd77e62(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcdaa2c74(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2bca8395(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_patrol(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 3.0, 'acceleration': 1.0, 'facing_turn_rate': 30.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})


def _decode_attack_path(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 3.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})


def _decode_combat(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 3.0, 'acceleration': 10.0, 'turn_threshold': 181.0, 'floor_buffer': 11.0, 'ceiling_buffer': 8.0})


def _decode_stab_attack(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 0.10000000149011612, 'acceleration': 10.0, 'turn_rate': 10800.0, 'facing_turn_rate': 120.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_max': 0.0, 'floor_buffer': 8.0, 'ceiling_buffer': 8.0})


def _decode_flyer_movement_mode_0x6ca56014(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 30.0, 'acceleration': 50.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_max': 0.0, 'floor_buffer': 3.5, 'ceiling_buffer': 8.0})


def _decode_flyer_movement_mode_0xe20e51c3(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 30.0, 'acceleration': 10.0, 'facing_turn_rate': 1.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_max': 1.0, 'floor_buffer': 5.0, 'ceiling_buffer': 8.0})


def _decode_flyer_movement_mode_0x25a68a0e(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 1.0, 'acceleration': 10.0, 'turn_threshold': 181.0, 'height_variation_max': 0.0, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})


def _decode_flyer_movement_mode_0xd9b5d506(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 30.0, 'acceleration': 20.0, 'facing_turn_rate': 1.0, 'turn_threshold': 181.0, 'height_variation_max': 1.0, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})


def _decode_flyer_movement_mode_0x8bb1c3a2(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 1.0, 'acceleration': 10.0, 'turn_threshold': 181.0, 'height_variation_max': 1.0, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})


def _decode_stunned(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 5.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_max': 1.0, 'floor_buffer': 5.0, 'ceiling_buffer': 8.0})


def _decode_flyer_movement_mode_0xfb2ddfad(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 5.0, 'acceleration': 10.0, 'facing_turn_rate': 15.0, 'turn_threshold': 181.0, 'use_avoidance': False, 'height_variation_min': 1.0, 'floor_buffer': 10.0, 'ceiling_buffer': 8.0})


def _decode_dash(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'speed': 40.0, 'acceleration': 100.0, 'turn_rate': 360.0, 'turn_threshold': 181.0, 'avoidance_range': 1.0, 'height_variation_max': 0.5, 'floor_buffer': 13.0, 'ceiling_buffer': 8.0})


def _decode_flyer_movement_mode_0x5fe13a7b(data: typing.BinaryIO, property_size: int):
    return FlyerMovementMode.from_stream(data, property_size, default_override={'acceleration': 20.0, 'turn_threshold': 181.0, 'floor_buffer': 12.0, 'ceiling_buffer': 12.0})


def _decode_claw(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_char_0x4d7dbeab(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_char_0xa17c09bb(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_char_0x11dc2dab(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_char_0xfddd9abb(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0xc99cee00(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2ffc41e1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7f5d9ab7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x993d3556(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x08efeb79(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xee8f4498(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc24d8fbd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x242d205c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stun_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_electric_ball_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_ball_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_electric_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_leg_hit_splash(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x25474550: ('hearing_range', _decode_hearing_range),
    0x474fa589: ('lose_interest_range', _decode_lose_interest_range),
    0xf8b0c2bb: ('lose_interest_time', _decode_lose_interest_time),
    0xfe4588a1: ('unknown_0xfe4588a1', _decode_unknown_0xfe4588a1),
    0xc2688b41: ('unknown_0xc2688b41', _decode_unknown_0xc2688b41),
    0x7b0cc30d: ('unknown_0x7b0cc30d', _decode_unknown_0x7b0cc30d),
    0x742b3336: ('damage_vulnerability', _decode_damage_vulnerability),
    0xd9230d1: ('body_vulnerability', _decode_body_vulnerability),
    0x243ab10d: ('brain_vulnerability', _decode_brain_vulnerability),
    0x12115a2: ('brain_x_ray_radius', _decode_brain_x_ray_radius),
    0xa12a4409: ('brain_radius', _decode_brain_radius),
    0x9f0ff852: ('leg_vulnerability', _decode_leg_vulnerability),
    0xb9e0c90d: ('unknown_0xb9e0c90d', _decode_unknown_0xb9e0c90d),
    0x81d39802: ('unknown_0x81d39802', _decode_unknown_0x81d39802),
    0xba002dcb: ('tentacle_regrow_time', _decode_tentacle_regrow_time),
    0xf79a10b0: ('unknown_0xf79a10b0', _decode_unknown_0xf79a10b0),
    0xc550a481: ('unknown_0xc550a481', _decode_unknown_0xc550a481),
    0x95e7a2c2: ('unknown_0x95e7a2c2', _decode_unknown_0x95e7a2c2),
    0x76ba1c18: ('unknown_0x76ba1c18', _decode_unknown_0x76ba1c18),
    0xe08106ed: ('unknown_0xe08106ed', _decode_unknown_0xe08106ed),
    0x88d7c540: ('unknown_0x88d7c540', _decode_unknown_0x88d7c540),
    0xace62367: ('unknown_0xace62367', _decode_unknown_0xace62367),
    0x620b1b3d: ('unknown_0x620b1b3d', _decode_unknown_0x620b1b3d),
    0xe1ae51d8: ('max_attack_height', _decode_max_attack_height),
    0xc8d0acc0: ('min_attack_height', _decode_min_attack_height),
    0xf3e8012d: ('max_attack_forward', _decode_max_attack_forward),
    0xe0ade786: ('min_attack_forward', _decode_min_attack_forward),
    0x978b98a: ('unknown_0x0978b98a', _decode_unknown_0x0978b98a),
    0xcfcd32bb: ('unknown_0xcfcd32bb', _decode_unknown_0xcfcd32bb),
    0x17d71349: ('unknown_0x17d71349', _decode_unknown_0x17d71349),
    0x9aa90b6b: ('recheck_path_time', _decode_recheck_path_time),
    0x7626ec89: ('recheck_path_distance', _decode_recheck_path_distance),
    0x7915e2b3: ('max_num_metroids', _decode_max_num_metroids),
    0xccc0cf92: ('auto_spawn', _decode_auto_spawn),
    0x75e0b0a7: ('max_spawn_delay', _decode_max_spawn_delay),
    0x2646a843: ('min_spawn_delay', _decode_min_spawn_delay),
    0x6089191d: ('unknown_0x6089191d', _decode_unknown_0x6089191d),
    0x258b5a9f: ('unknown_0x258b5a9f', _decode_unknown_0x258b5a9f),
    0x2ae610e5: ('unknown_0x2ae610e5', _decode_unknown_0x2ae610e5),
    0x354bae31: ('hatch_chance', _decode_hatch_chance),
    0xf4b2c801: ('maya_double', _decode_maya_double),
    0x3fee1ba4: ('unknown_0x3fee1ba4', _decode_unknown_0x3fee1ba4),
    0xcfacff53: ('spin_attack_damage', _decode_spin_attack_damage),
    0x6cb6d8c7: ('max_spin_attack_delay', _decode_max_spin_attack_delay),
    0x682ce9ed: ('min_spin_attack_delay', _decode_min_spin_attack_delay),
    0xbeaf2105: ('unknown_0xbeaf2105', _decode_unknown_0xbeaf2105),
    0x54ff4d38: ('unknown_0x54ff4d38', _decode_unknown_0x54ff4d38),
    0xb29fe2d9: ('unknown_0xb29fe2d9', _decode_unknown_0xb29fe2d9),
    0x47be3298: ('dodge_chance', _decode_dodge_chance),
    0x42647ad7: ('unknown_0x42647ad7', _decode_unknown_0x42647ad7),
    0xa404d536: ('unknown_0xa404d536', _decode_unknown_0xa404d536),
    0x248d3599: ('unknown_0x248d3599', _decode_unknown_0x248d3599),
    0xbfd77e62: ('unknown_0xbfd77e62', _decode_unknown_0xbfd77e62),
    0xcdaa2c74: ('unknown_0xcdaa2c74', _decode_unknown_0xcdaa2c74),
    0x2bca8395: ('unknown_0x2bca8395', _decode_unknown_0x2bca8395),
    0xccdd3aca: ('patrol', _decode_patrol),
    0xc845d3c0: ('attack_path', _decode_attack_path),
    0xcc7d2e98: ('combat', _decode_combat),
    0xb9c3db94: ('stab_attack', _decode_stab_attack),
    0x6ca56014: ('flyer_movement_mode_0x6ca56014', _decode_flyer_movement_mode_0x6ca56014),
    0xe20e51c3: ('flyer_movement_mode_0xe20e51c3', _decode_flyer_movement_mode_0xe20e51c3),
    0x25a68a0e: ('flyer_movement_mode_0x25a68a0e', _decode_flyer_movement_mode_0x25a68a0e),
    0xd9b5d506: ('flyer_movement_mode_0xd9b5d506', _decode_flyer_movement_mode_0xd9b5d506),
    0x8bb1c3a2: ('flyer_movement_mode_0x8bb1c3a2', _decode_flyer_movement_mode_0x8bb1c3a2),
    0x389cb515: ('stunned', _decode_stunned),
    0xfb2ddfad: ('flyer_movement_mode_0xfb2ddfad', _decode_flyer_movement_mode_0xfb2ddfad),
    0xc558bc0d: ('dash', _decode_dash),
    0x5fe13a7b: ('flyer_movement_mode_0x5fe13a7b', _decode_flyer_movement_mode_0x5fe13a7b),
    0xfd38a106: ('claw', _decode_claw),
    0x4d7dbeab: ('char_0x4d7dbeab', _decode_char_0x4d7dbeab),
    0xa17c09bb: ('char_0xa17c09bb', _decode_char_0xa17c09bb),
    0x11dc2dab: ('char_0x11dc2dab', _decode_char_0x11dc2dab),
    0xfddd9abb: ('char_0xfddd9abb', _decode_char_0xfddd9abb),
    0xc99cee00: ('unknown_0xc99cee00', _decode_unknown_0xc99cee00),
    0x2ffc41e1: ('unknown_0x2ffc41e1', _decode_unknown_0x2ffc41e1),
    0x7f5d9ab7: ('unknown_0x7f5d9ab7', _decode_unknown_0x7f5d9ab7),
    0x993d3556: ('unknown_0x993d3556', _decode_unknown_0x993d3556),
    0x8efeb79: ('unknown_0x08efeb79', _decode_unknown_0x08efeb79),
    0xee8f4498: ('unknown_0xee8f4498', _decode_unknown_0xee8f4498),
    0xc24d8fbd: ('unknown_0xc24d8fbd', _decode_unknown_0xc24d8fbd),
    0x242d205c: ('unknown_0x242d205c', _decode_unknown_0x242d205c),
    0x5bdd1e4c: ('stun_threshold', _decode_stun_threshold),
    0x6da4a3b0: ('electric_ball_effect', _decode_electric_ball_effect),
    0x3fcd8b66: ('sound_ball_effect', _decode_sound_ball_effect),
    0xcc0af287: ('electric_visor_effect', _decode_electric_visor_effect),
    0xa3e8ec4e: ('sound_visor_effect', _decode_sound_visor_effect),
    0xf40a9c9d: ('leg_hit_splash', _decode_leg_hit_splash),
}
