# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.archetypes.MetroidHopperStruct import MetroidHopperStruct
from retro_data_structures.properties.corruption.archetypes.TeamAIDebugEnum import TeamAIDebugEnum
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class MetroidHopperData(BaseProperty):
    animation_speed: float = dataclasses.field(default=1.0)
    hearing_range: float = dataclasses.field(default=100.0)
    alert_animation_chance: float = dataclasses.field(default=1.0)
    unknown_0x87c38060: bool = dataclasses.field(default=False)
    jump_apex: float = dataclasses.field(default=1.0)
    gravity_constant: float = dataclasses.field(default=30.0)
    min_melee_attack_dist: float = dataclasses.field(default=8.0)
    max_melee_attack_dist: float = dataclasses.field(default=11.0)
    unknown_0x68e4097e: float = dataclasses.field(default=0.5)
    light_melee_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    heavy_melee_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x500683fc: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x0708d3bf: float = dataclasses.field(default=20.0)
    projectile_info: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    melee_chance: float = dataclasses.field(default=0.6000000238418579)
    projectile_chance: float = dataclasses.field(default=0.30000001192092896)
    metroid_hopper_struct_0xd5a8e2da: MetroidHopperStruct = dataclasses.field(default_factory=MetroidHopperStruct)
    metroid_hopper_struct_0x184991da: MetroidHopperStruct = dataclasses.field(default_factory=MetroidHopperStruct)
    metroid_hopper_struct_0x7b07aca3: MetroidHopperStruct = dataclasses.field(default_factory=MetroidHopperStruct)
    hypermode_clear_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    hypermode_clear_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0x1da1b117: float = dataclasses.field(default=5.0)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    super_hopper_explosion_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    team_ai_debug_type: TeamAIDebugEnum = dataclasses.field(default_factory=TeamAIDebugEnum)
    debug_patrol: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x1a')  # 26 properties

        data.write(b'\xc5@wW')  # 0xc5407757
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.animation_speed))

        data.write(b'%GEP')  # 0x25474550
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hearing_range))

        data.write(b'\xe6Icv')  # 0xe6496376
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.alert_animation_chance))

        data.write(b'\x87\xc3\x80`')  # 0x87c38060
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x87c38060))

        data.write(b'\xf2x%\x01')  # 0xf2782501
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_apex))

        data.write(b'\x7f8\xdc\xcb')  # 0x7f38dccb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_constant))

        data.write(b'\x01\xb7\xd6\xb1')  # 0x1b7d6b1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_melee_attack_dist))

        data.write(b'\x05-\xe7\x9b')  # 0x52de79b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_melee_attack_dist))

        data.write(b'h\xe4\t~')  # 0x68e4097e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x68e4097e))

        data.write(b'+v\xb9\xf1')  # 0x2b76b9f1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.light_melee_damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\xf4\xa1\x01')  # 0x9ef4a101
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.heavy_melee_damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\x06\x83\xfc')  # 0x500683fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x500683fc))

        data.write(b'\x07\x08\xd3\xbf')  # 0x708d3bf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0708d3bf))

        data.write(b'\xf9\xef\x8d]')  # 0xf9ef8d5d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xae\xcf\xea-')  # 0xaecfea2d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_chance))

        data.write(b'*}\x01\x01')  # 0x2a7d0101
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_chance))

        data.write(b'\xd5\xa8\xe2\xda')  # 0xd5a8e2da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_hopper_struct_0xd5a8e2da.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18I\x91\xda')  # 0x184991da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_hopper_struct_0x184991da.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{\x07\xac\xa3')  # 0x7b07aca3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.metroid_hopper_struct_0x7b07aca3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\xde[%')  # 0x5dde5b25
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hypermode_clear_effect))

        data.write(b'\xf9] 3')  # 0xf95d2033
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hypermode_clear_sound))

        data.write(b'\x1d\xa1\xb1\x17')  # 0x1da1b117
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1da1b117))

        data.write(b'\xe0p\x00"')  # 0xe0700022
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.part))

        data.write(b'\xd1\xf6\xc5 ')  # 0xd1f6c520
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_hopper_explosion_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfbd\x881')  # 0xfb648831
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.team_ai_debug_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb8\x9a\x82')  # 0xbb389a82
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.debug_patrol))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            animation_speed=data['animation_speed'],
            hearing_range=data['hearing_range'],
            alert_animation_chance=data['alert_animation_chance'],
            unknown_0x87c38060=data['unknown_0x87c38060'],
            jump_apex=data['jump_apex'],
            gravity_constant=data['gravity_constant'],
            min_melee_attack_dist=data['min_melee_attack_dist'],
            max_melee_attack_dist=data['max_melee_attack_dist'],
            unknown_0x68e4097e=data['unknown_0x68e4097e'],
            light_melee_damage_info=DamageInfo.from_json(data['light_melee_damage_info']),
            heavy_melee_damage_info=DamageInfo.from_json(data['heavy_melee_damage_info']),
            unknown_0x500683fc=data['unknown_0x500683fc'],
            unknown_0x0708d3bf=data['unknown_0x0708d3bf'],
            projectile_info=LaunchProjectileData.from_json(data['projectile_info']),
            melee_chance=data['melee_chance'],
            projectile_chance=data['projectile_chance'],
            metroid_hopper_struct_0xd5a8e2da=MetroidHopperStruct.from_json(data['metroid_hopper_struct_0xd5a8e2da']),
            metroid_hopper_struct_0x184991da=MetroidHopperStruct.from_json(data['metroid_hopper_struct_0x184991da']),
            metroid_hopper_struct_0x7b07aca3=MetroidHopperStruct.from_json(data['metroid_hopper_struct_0x7b07aca3']),
            hypermode_clear_effect=data['hypermode_clear_effect'],
            hypermode_clear_sound=data['hypermode_clear_sound'],
            unknown_0x1da1b117=data['unknown_0x1da1b117'],
            part=data['part'],
            super_hopper_explosion_damage=DamageInfo.from_json(data['super_hopper_explosion_damage']),
            team_ai_debug_type=TeamAIDebugEnum.from_json(data['team_ai_debug_type']),
            debug_patrol=data['debug_patrol'],
        )

    def to_json(self) -> dict:
        return {
            'animation_speed': self.animation_speed,
            'hearing_range': self.hearing_range,
            'alert_animation_chance': self.alert_animation_chance,
            'unknown_0x87c38060': self.unknown_0x87c38060,
            'jump_apex': self.jump_apex,
            'gravity_constant': self.gravity_constant,
            'min_melee_attack_dist': self.min_melee_attack_dist,
            'max_melee_attack_dist': self.max_melee_attack_dist,
            'unknown_0x68e4097e': self.unknown_0x68e4097e,
            'light_melee_damage_info': self.light_melee_damage_info.to_json(),
            'heavy_melee_damage_info': self.heavy_melee_damage_info.to_json(),
            'unknown_0x500683fc': self.unknown_0x500683fc,
            'unknown_0x0708d3bf': self.unknown_0x0708d3bf,
            'projectile_info': self.projectile_info.to_json(),
            'melee_chance': self.melee_chance,
            'projectile_chance': self.projectile_chance,
            'metroid_hopper_struct_0xd5a8e2da': self.metroid_hopper_struct_0xd5a8e2da.to_json(),
            'metroid_hopper_struct_0x184991da': self.metroid_hopper_struct_0x184991da.to_json(),
            'metroid_hopper_struct_0x7b07aca3': self.metroid_hopper_struct_0x7b07aca3.to_json(),
            'hypermode_clear_effect': self.hypermode_clear_effect,
            'hypermode_clear_sound': self.hypermode_clear_sound,
            'unknown_0x1da1b117': self.unknown_0x1da1b117,
            'part': self.part,
            'super_hopper_explosion_damage': self.super_hopper_explosion_damage.to_json(),
            'team_ai_debug_type': self.team_ai_debug_type.to_json(),
            'debug_patrol': self.debug_patrol,
        }


def _decode_animation_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hearing_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alert_animation_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x87c38060(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_jump_apex(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_melee_attack_dist(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_melee_attack_dist(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x68e4097e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_light_melee_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_heavy_melee_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x500683fc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0708d3bf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile_info(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_melee_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_metroid_hopper_struct_0xd5a8e2da(data: typing.BinaryIO, property_size: int):
    return MetroidHopperStruct.from_stream(data, property_size)


def _decode_metroid_hopper_struct_0x184991da(data: typing.BinaryIO, property_size: int):
    return MetroidHopperStruct.from_stream(data, property_size)


def _decode_metroid_hopper_struct_0x7b07aca3(data: typing.BinaryIO, property_size: int):
    return MetroidHopperStruct.from_stream(data, property_size)


def _decode_hypermode_clear_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_hypermode_clear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x1da1b117(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_super_hopper_explosion_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_team_ai_debug_type(data: typing.BinaryIO, property_size: int):
    return TeamAIDebugEnum.from_stream(data, property_size)


def _decode_debug_patrol(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc5407757: ('animation_speed', _decode_animation_speed),
    0x25474550: ('hearing_range', _decode_hearing_range),
    0xe6496376: ('alert_animation_chance', _decode_alert_animation_chance),
    0x87c38060: ('unknown_0x87c38060', _decode_unknown_0x87c38060),
    0xf2782501: ('jump_apex', _decode_jump_apex),
    0x7f38dccb: ('gravity_constant', _decode_gravity_constant),
    0x1b7d6b1: ('min_melee_attack_dist', _decode_min_melee_attack_dist),
    0x52de79b: ('max_melee_attack_dist', _decode_max_melee_attack_dist),
    0x68e4097e: ('unknown_0x68e4097e', _decode_unknown_0x68e4097e),
    0x2b76b9f1: ('light_melee_damage_info', _decode_light_melee_damage_info),
    0x9ef4a101: ('heavy_melee_damage_info', _decode_heavy_melee_damage_info),
    0x500683fc: ('unknown_0x500683fc', _decode_unknown_0x500683fc),
    0x708d3bf: ('unknown_0x0708d3bf', _decode_unknown_0x0708d3bf),
    0xf9ef8d5d: ('projectile_info', _decode_projectile_info),
    0xaecfea2d: ('melee_chance', _decode_melee_chance),
    0x2a7d0101: ('projectile_chance', _decode_projectile_chance),
    0xd5a8e2da: ('metroid_hopper_struct_0xd5a8e2da', _decode_metroid_hopper_struct_0xd5a8e2da),
    0x184991da: ('metroid_hopper_struct_0x184991da', _decode_metroid_hopper_struct_0x184991da),
    0x7b07aca3: ('metroid_hopper_struct_0x7b07aca3', _decode_metroid_hopper_struct_0x7b07aca3),
    0x5dde5b25: ('hypermode_clear_effect', _decode_hypermode_clear_effect),
    0xf95d2033: ('hypermode_clear_sound', _decode_hypermode_clear_sound),
    0x1da1b117: ('unknown_0x1da1b117', _decode_unknown_0x1da1b117),
    0xe0700022: ('part', _decode_part),
    0xd1f6c520: ('super_hopper_explosion_damage', _decode_super_hopper_explosion_damage),
    0xfb648831: ('team_ai_debug_type', _decode_team_ai_debug_type),
    0xbb389a82: ('debug_patrol', _decode_debug_patrol),
}
