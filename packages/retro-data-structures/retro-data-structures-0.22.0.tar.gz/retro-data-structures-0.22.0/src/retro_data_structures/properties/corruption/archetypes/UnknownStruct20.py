# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.archetypes.ShockWaveInfo import ShockWaveInfo


@dataclasses.dataclass()
class UnknownStruct20(BaseProperty):
    health: float = dataclasses.field(default=750.0)
    animation_speed: float = dataclasses.field(default=1.100000023841858)
    heart_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    body_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    mouth_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    stun_threshold: float = dataclasses.field(default=80.0)
    stun_decay: float = dataclasses.field(default=0.0)
    unknown_0x7d185e91: float = dataclasses.field(default=7.5)
    unknown_0x9b78f170: float = dataclasses.field(default=11.25)
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x93b08ac8: float = dataclasses.field(default=0.4000000059604645)
    dash_delay_maximum: float = dataclasses.field(default=15.0)
    dash_delay_minimum: float = dataclasses.field(default=15.0)
    dash_delay_variance: float = dataclasses.field(default=5.0)
    wander_distance: float = dataclasses.field(default=30.0)
    too_far_distance: float = dataclasses.field(default=20.0)
    berserk_distance: float = dataclasses.field(default=44.0)
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    bomb: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    unknown_0x54cfed2a: float = dataclasses.field(default=0.5)
    unknown_0x94a19a8b: float = dataclasses.field(default=30.0)
    unknown_0x72c1356a: float = dataclasses.field(default=60.0)
    unknown_0xe291a671: int = dataclasses.field(default=4)
    unknown_0xa793e5f3: int = dataclasses.field(default=4)
    unknown_0x19774dec: int = dataclasses.field(default=1)
    circle_chance: float = dataclasses.field(default=100.0)
    circle_right_chance: float = dataclasses.field(default=100.0)
    circle_left_chance: float = dataclasses.field(default=100.0)
    circle_north_chance: float = dataclasses.field(default=100.0)
    circle_south_chance: float = dataclasses.field(default=100.0)
    circle_pause_chance: float = dataclasses.field(default=200.0)
    bomb_chance: float = dataclasses.field(default=0.800000011920929)
    fade_out_target_alpha: float = dataclasses.field(default=0.0)
    fade_out_delta: float = dataclasses.field(default=-0.02500000037252903)
    fade_in_target_alpha: float = dataclasses.field(default=1.0)
    fade_in_delta: float = dataclasses.field(default=0.02500000037252903)
    unknown_0x20dc1c96: float = dataclasses.field(default=0.5)

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
        data.write(b'\x00%')  # 37 properties

        data.write(b'\xf0f\x89\x19')  # 0xf0668919
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.health))

        data.write(b'\xc5@wW')  # 0xc5407757
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.animation_speed))

        data.write(b'\xf0d\xb3\xbc')  # 0xf064b3bc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.heart_vulnerability.to_stream(data)
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

        data.write(b'\xed~\xdc\xa3')  # 0xed7edca3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mouth_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'[\xdd\x1eL')  # 0x5bdd1e4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_threshold))

        data.write(b'`\x82C\x0f')  # 0x6082430f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stun_decay))

        data.write(b'}\x18^\x91')  # 0x7d185e91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7d185e91))

        data.write(b'\x9bx\xf1p')  # 0x9b78f170
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9b78f170))

        data.write(b'$\xb93\xd3')  # 0x24b933d3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data, default_override={'di_damage': 3.0, 'di_radius': 1.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93\xb0\x8a\xc8')  # 0x93b08ac8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x93b08ac8))

        data.write(b'\x1b7\xed\xa7')  # 0x1b37eda7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dash_delay_maximum))

        data.write(b'\x8bD\xfdM')  # 0x8b44fd4d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dash_delay_minimum))

        data.write(b'\xda\xc0^\xb5')  # 0xdac05eb5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dash_delay_variance))

        data.write(b"\xaf'\x0c\x93")  # 0xaf270c93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wander_distance))

        data.write(b'\x88\x19h\x8d')  # 0x8819688d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.too_far_distance))

        data.write(b'\xbc\x9b\xba\xf9')  # 0xbc9bbaf9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.berserk_distance))

        data.write(b'\x9c2\xd0\xa0')  # 0x9c32d0a0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data, default_override={'duration': 5.0, 'height': 2.0, 'radial_velocity': 45.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'N\xa6\xc6\xa9')  # 0x4ea6c6a9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bomb.to_stream(data, default_override={'delay': 0.20000000298023224, 'delay_variance': 0.10000000149011612, 'stop_homing_range': 30.0, 'generate_pickup_chance': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'T\xcf\xed*')  # 0x54cfed2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x54cfed2a))

        data.write(b'\x94\xa1\x9a\x8b')  # 0x94a19a8b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x94a19a8b))

        data.write(b'r\xc15j')  # 0x72c1356a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x72c1356a))

        data.write(b'\xe2\x91\xa6q')  # 0xe291a671
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xe291a671))

        data.write(b'\xa7\x93\xe5\xf3')  # 0xa793e5f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa793e5f3))

        data.write(b'\x19wM\xec')  # 0x19774dec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x19774dec))

        data.write(b'H+w\x04')  # 0x482b7704
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.circle_chance))

        data.write(b'\xc3TMg')  # 0xc3544d67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.circle_right_chance))

        data.write(b'\xa2G\xc4|')  # 0xa247c47c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.circle_left_chance))

        data.write(b'e\x15\x99\x9e')  # 0x6515999e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.circle_north_chance))

        data.write(b'\xef\xb5O\x99')  # 0xefb54f99
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.circle_south_chance))

        data.write(b'\xc8\xd2\xe4\xa8')  # 0xc8d2e4a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.circle_pause_chance))

        data.write(b'\xf3\xad8\x81')  # 0xf3ad3881
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bomb_chance))

        data.write(b'\x03n<t')  # 0x36e3c74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_target_alpha))

        data.write(b'!q\xc5\xed')  # 0x2171c5ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_delta))

        data.write(b'%\x15d\x1c')  # 0x2515641c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_target_alpha))

        data.write(b'nB\xbb\x15')  # 0x6e42bb15
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_delta))

        data.write(b' \xdc\x1c\x96')  # 0x20dc1c96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x20dc1c96))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            health=data['health'],
            animation_speed=data['animation_speed'],
            heart_vulnerability=DamageVulnerability.from_json(data['heart_vulnerability']),
            body_vulnerability=DamageVulnerability.from_json(data['body_vulnerability']),
            mouth_vulnerability=DamageVulnerability.from_json(data['mouth_vulnerability']),
            stun_threshold=data['stun_threshold'],
            stun_decay=data['stun_decay'],
            unknown_0x7d185e91=data['unknown_0x7d185e91'],
            unknown_0x9b78f170=data['unknown_0x9b78f170'],
            damage_info=DamageInfo.from_json(data['damage_info']),
            unknown_0x93b08ac8=data['unknown_0x93b08ac8'],
            dash_delay_maximum=data['dash_delay_maximum'],
            dash_delay_minimum=data['dash_delay_minimum'],
            dash_delay_variance=data['dash_delay_variance'],
            wander_distance=data['wander_distance'],
            too_far_distance=data['too_far_distance'],
            berserk_distance=data['berserk_distance'],
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
            bomb=LaunchProjectileData.from_json(data['bomb']),
            unknown_0x54cfed2a=data['unknown_0x54cfed2a'],
            unknown_0x94a19a8b=data['unknown_0x94a19a8b'],
            unknown_0x72c1356a=data['unknown_0x72c1356a'],
            unknown_0xe291a671=data['unknown_0xe291a671'],
            unknown_0xa793e5f3=data['unknown_0xa793e5f3'],
            unknown_0x19774dec=data['unknown_0x19774dec'],
            circle_chance=data['circle_chance'],
            circle_right_chance=data['circle_right_chance'],
            circle_left_chance=data['circle_left_chance'],
            circle_north_chance=data['circle_north_chance'],
            circle_south_chance=data['circle_south_chance'],
            circle_pause_chance=data['circle_pause_chance'],
            bomb_chance=data['bomb_chance'],
            fade_out_target_alpha=data['fade_out_target_alpha'],
            fade_out_delta=data['fade_out_delta'],
            fade_in_target_alpha=data['fade_in_target_alpha'],
            fade_in_delta=data['fade_in_delta'],
            unknown_0x20dc1c96=data['unknown_0x20dc1c96'],
        )

    def to_json(self) -> dict:
        return {
            'health': self.health,
            'animation_speed': self.animation_speed,
            'heart_vulnerability': self.heart_vulnerability.to_json(),
            'body_vulnerability': self.body_vulnerability.to_json(),
            'mouth_vulnerability': self.mouth_vulnerability.to_json(),
            'stun_threshold': self.stun_threshold,
            'stun_decay': self.stun_decay,
            'unknown_0x7d185e91': self.unknown_0x7d185e91,
            'unknown_0x9b78f170': self.unknown_0x9b78f170,
            'damage_info': self.damage_info.to_json(),
            'unknown_0x93b08ac8': self.unknown_0x93b08ac8,
            'dash_delay_maximum': self.dash_delay_maximum,
            'dash_delay_minimum': self.dash_delay_minimum,
            'dash_delay_variance': self.dash_delay_variance,
            'wander_distance': self.wander_distance,
            'too_far_distance': self.too_far_distance,
            'berserk_distance': self.berserk_distance,
            'shock_wave_info': self.shock_wave_info.to_json(),
            'bomb': self.bomb.to_json(),
            'unknown_0x54cfed2a': self.unknown_0x54cfed2a,
            'unknown_0x94a19a8b': self.unknown_0x94a19a8b,
            'unknown_0x72c1356a': self.unknown_0x72c1356a,
            'unknown_0xe291a671': self.unknown_0xe291a671,
            'unknown_0xa793e5f3': self.unknown_0xa793e5f3,
            'unknown_0x19774dec': self.unknown_0x19774dec,
            'circle_chance': self.circle_chance,
            'circle_right_chance': self.circle_right_chance,
            'circle_left_chance': self.circle_left_chance,
            'circle_north_chance': self.circle_north_chance,
            'circle_south_chance': self.circle_south_chance,
            'circle_pause_chance': self.circle_pause_chance,
            'bomb_chance': self.bomb_chance,
            'fade_out_target_alpha': self.fade_out_target_alpha,
            'fade_out_delta': self.fade_out_delta,
            'fade_in_target_alpha': self.fade_in_target_alpha,
            'fade_in_delta': self.fade_in_delta,
            'unknown_0x20dc1c96': self.unknown_0x20dc1c96,
        }


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_animation_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_heart_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_body_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_mouth_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_stun_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stun_decay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7d185e91(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9b78f170(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_damage': 3.0, 'di_radius': 1.0, 'di_knock_back_power': 10.0})


def _decode_unknown_0x93b08ac8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dash_delay_maximum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dash_delay_minimum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dash_delay_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wander_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_too_far_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_berserk_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size, default_override={'duration': 5.0, 'height': 2.0, 'radial_velocity': 45.0})


def _decode_bomb(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size, default_override={'delay': 0.20000000298023224, 'delay_variance': 0.10000000149011612, 'stop_homing_range': 30.0, 'generate_pickup_chance': 1.0})


def _decode_unknown_0x54cfed2a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x94a19a8b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x72c1356a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe291a671(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xa793e5f3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x19774dec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_circle_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_circle_right_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_circle_left_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_circle_north_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_circle_south_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_circle_pause_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bomb_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_target_alpha(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_delta(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_in_target_alpha(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_in_delta(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x20dc1c96(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf0668919: ('health', _decode_health),
    0xc5407757: ('animation_speed', _decode_animation_speed),
    0xf064b3bc: ('heart_vulnerability', _decode_heart_vulnerability),
    0xd9230d1: ('body_vulnerability', _decode_body_vulnerability),
    0xed7edca3: ('mouth_vulnerability', _decode_mouth_vulnerability),
    0x5bdd1e4c: ('stun_threshold', _decode_stun_threshold),
    0x6082430f: ('stun_decay', _decode_stun_decay),
    0x7d185e91: ('unknown_0x7d185e91', _decode_unknown_0x7d185e91),
    0x9b78f170: ('unknown_0x9b78f170', _decode_unknown_0x9b78f170),
    0x24b933d3: ('damage_info', _decode_damage_info),
    0x93b08ac8: ('unknown_0x93b08ac8', _decode_unknown_0x93b08ac8),
    0x1b37eda7: ('dash_delay_maximum', _decode_dash_delay_maximum),
    0x8b44fd4d: ('dash_delay_minimum', _decode_dash_delay_minimum),
    0xdac05eb5: ('dash_delay_variance', _decode_dash_delay_variance),
    0xaf270c93: ('wander_distance', _decode_wander_distance),
    0x8819688d: ('too_far_distance', _decode_too_far_distance),
    0xbc9bbaf9: ('berserk_distance', _decode_berserk_distance),
    0x9c32d0a0: ('shock_wave_info', _decode_shock_wave_info),
    0x4ea6c6a9: ('bomb', _decode_bomb),
    0x54cfed2a: ('unknown_0x54cfed2a', _decode_unknown_0x54cfed2a),
    0x94a19a8b: ('unknown_0x94a19a8b', _decode_unknown_0x94a19a8b),
    0x72c1356a: ('unknown_0x72c1356a', _decode_unknown_0x72c1356a),
    0xe291a671: ('unknown_0xe291a671', _decode_unknown_0xe291a671),
    0xa793e5f3: ('unknown_0xa793e5f3', _decode_unknown_0xa793e5f3),
    0x19774dec: ('unknown_0x19774dec', _decode_unknown_0x19774dec),
    0x482b7704: ('circle_chance', _decode_circle_chance),
    0xc3544d67: ('circle_right_chance', _decode_circle_right_chance),
    0xa247c47c: ('circle_left_chance', _decode_circle_left_chance),
    0x6515999e: ('circle_north_chance', _decode_circle_north_chance),
    0xefb54f99: ('circle_south_chance', _decode_circle_south_chance),
    0xc8d2e4a8: ('circle_pause_chance', _decode_circle_pause_chance),
    0xf3ad3881: ('bomb_chance', _decode_bomb_chance),
    0x36e3c74: ('fade_out_target_alpha', _decode_fade_out_target_alpha),
    0x2171c5ed: ('fade_out_delta', _decode_fade_out_delta),
    0x2515641c: ('fade_in_target_alpha', _decode_fade_in_target_alpha),
    0x6e42bb15: ('fade_in_delta', _decode_fade_in_delta),
    0x20dc1c96: ('unknown_0x20dc1c96', _decode_unknown_0x20dc1c96),
}
