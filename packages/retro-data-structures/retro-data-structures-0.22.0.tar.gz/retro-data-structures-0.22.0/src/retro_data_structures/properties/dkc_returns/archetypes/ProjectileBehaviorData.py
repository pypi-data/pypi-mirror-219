# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.DamageEffectData import DamageEffectData


@dataclasses.dataclass()
class ProjectileBehaviorData(BaseProperty):
    disable_collision_time_after_creation: float = dataclasses.field(default=0.5)
    mode: int = dataclasses.field(default=547879193)  # Choice
    launch_up_speed: float = dataclasses.field(default=0.0)
    target_speed_multiplier: float = dataclasses.field(default=1.0)
    extra_distance_past_target_point: float = dataclasses.field(default=0.0)
    max_spline_distance_from_starting_point: float = dataclasses.field(default=0.0)
    reverse_direction_when_target_is_thrown: bool = dataclasses.field(default=False)
    max_life_time: float = dataclasses.field(default=5.0)
    max_life_time_safe_guard: float = dataclasses.field(default=30.0)
    number_of_damage_effects: int = dataclasses.field(default=0)
    align_damage_effects_to_surface_on_creation: bool = dataclasses.field(default=False)
    allow_damage_effects_to_slave_to_platforms: bool = dataclasses.field(default=False)
    damage_effect: DamageEffectData = dataclasses.field(default_factory=DamageEffectData)
    damage_effect2: DamageEffectData = dataclasses.field(default_factory=DamageEffectData)
    damage_effect3: DamageEffectData = dataclasses.field(default_factory=DamageEffectData)
    apply_contact_rules: bool = dataclasses.field(default=False)
    ignore_all_but_player: bool = dataclasses.field(default=False)
    disable_behavior_after_applying_velocity: bool = dataclasses.field(default=False)
    disable_max_life_time: bool = dataclasses.field(default=False)
    limit_speed: bool = dataclasses.field(default=False)
    maximum_speed: float = dataclasses.field(default=100.0)

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
        data.write(b'\x00\x15')  # 21 properties

        data.write(b'\xbe\xc9\x90\x05')  # 0xbec99005
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_collision_time_after_creation))

        data.write(b'\xb8\xf6\x0f\x9a')  # 0xb8f60f9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.mode))

        data.write(b'A\xf0\x9d\xe5')  # 0x41f09de5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_up_speed))

        data.write(b'>\x88\x17\xaa')  # 0x3e8817aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_speed_multiplier))

        data.write(b'.\x94\xd9\x8e')  # 0x2e94d98e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.extra_distance_past_target_point))

        data.write(b'\xe2\x96\xb2\x9f')  # 0xe296b29f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_spline_distance_from_starting_point))

        data.write(b'\x82\xdb\xfc\xf1')  # 0x82dbfcf1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.reverse_direction_when_target_is_thrown))

        data.write(b'V%oY')  # 0x56256f59
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_life_time))

        data.write(b'\x17\xe5\x81\x1d')  # 0x17e5811d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_life_time_safe_guard))

        data.write(b'>Hm\xc0')  # 0x3e486dc0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_damage_effects))

        data.write(b"*\xcb\xfb'")  # 0x2acbfb27
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.align_damage_effects_to_surface_on_creation))

        data.write(b'\xe3\xf9j\x88')  # 0xe3f96a88
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_damage_effects_to_slave_to_platforms))

        data.write(b'>\x01!\xc3')  # 0x3e0121c3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_effect.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f12\x85')  # 0x7f313285
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_effect2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\x97\xf9\xc6')  # 0xf897f9c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_effect3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S\x185}')  # 0x5318357d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_contact_rules))

        data.write(b'\xab\x0fQX')  # 0xab0f5158
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_all_but_player))

        data.write(b'\xb9\xe1I\xe6')  # 0xb9e149e6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_behavior_after_applying_velocity))

        data.write(b'\xce\xd5\x0fx')  # 0xced50f78
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_max_life_time))

        data.write(b'\xd0\xe7\xf9`')  # 0xd0e7f960
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.limit_speed))

        data.write(b'\x14\x0e\xf2\xcc')  # 0x140ef2cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            disable_collision_time_after_creation=data['disable_collision_time_after_creation'],
            mode=data['mode'],
            launch_up_speed=data['launch_up_speed'],
            target_speed_multiplier=data['target_speed_multiplier'],
            extra_distance_past_target_point=data['extra_distance_past_target_point'],
            max_spline_distance_from_starting_point=data['max_spline_distance_from_starting_point'],
            reverse_direction_when_target_is_thrown=data['reverse_direction_when_target_is_thrown'],
            max_life_time=data['max_life_time'],
            max_life_time_safe_guard=data['max_life_time_safe_guard'],
            number_of_damage_effects=data['number_of_damage_effects'],
            align_damage_effects_to_surface_on_creation=data['align_damage_effects_to_surface_on_creation'],
            allow_damage_effects_to_slave_to_platforms=data['allow_damage_effects_to_slave_to_platforms'],
            damage_effect=DamageEffectData.from_json(data['damage_effect']),
            damage_effect2=DamageEffectData.from_json(data['damage_effect2']),
            damage_effect3=DamageEffectData.from_json(data['damage_effect3']),
            apply_contact_rules=data['apply_contact_rules'],
            ignore_all_but_player=data['ignore_all_but_player'],
            disable_behavior_after_applying_velocity=data['disable_behavior_after_applying_velocity'],
            disable_max_life_time=data['disable_max_life_time'],
            limit_speed=data['limit_speed'],
            maximum_speed=data['maximum_speed'],
        )

    def to_json(self) -> dict:
        return {
            'disable_collision_time_after_creation': self.disable_collision_time_after_creation,
            'mode': self.mode,
            'launch_up_speed': self.launch_up_speed,
            'target_speed_multiplier': self.target_speed_multiplier,
            'extra_distance_past_target_point': self.extra_distance_past_target_point,
            'max_spline_distance_from_starting_point': self.max_spline_distance_from_starting_point,
            'reverse_direction_when_target_is_thrown': self.reverse_direction_when_target_is_thrown,
            'max_life_time': self.max_life_time,
            'max_life_time_safe_guard': self.max_life_time_safe_guard,
            'number_of_damage_effects': self.number_of_damage_effects,
            'align_damage_effects_to_surface_on_creation': self.align_damage_effects_to_surface_on_creation,
            'allow_damage_effects_to_slave_to_platforms': self.allow_damage_effects_to_slave_to_platforms,
            'damage_effect': self.damage_effect.to_json(),
            'damage_effect2': self.damage_effect2.to_json(),
            'damage_effect3': self.damage_effect3.to_json(),
            'apply_contact_rules': self.apply_contact_rules,
            'ignore_all_but_player': self.ignore_all_but_player,
            'disable_behavior_after_applying_velocity': self.disable_behavior_after_applying_velocity,
            'disable_max_life_time': self.disable_max_life_time,
            'limit_speed': self.limit_speed,
            'maximum_speed': self.maximum_speed,
        }


def _decode_disable_collision_time_after_creation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_launch_up_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_speed_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_extra_distance_past_target_point(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_spline_distance_from_starting_point(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverse_direction_when_target_is_thrown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_life_time_safe_guard(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_number_of_damage_effects(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_align_damage_effects_to_surface_on_creation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_damage_effects_to_slave_to_platforms(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_damage_effect(data: typing.BinaryIO, property_size: int):
    return DamageEffectData.from_stream(data, property_size)


def _decode_damage_effect2(data: typing.BinaryIO, property_size: int):
    return DamageEffectData.from_stream(data, property_size)


def _decode_damage_effect3(data: typing.BinaryIO, property_size: int):
    return DamageEffectData.from_stream(data, property_size)


def _decode_apply_contact_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_all_but_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_behavior_after_applying_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_max_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_limit_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_maximum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbec99005: ('disable_collision_time_after_creation', _decode_disable_collision_time_after_creation),
    0xb8f60f9a: ('mode', _decode_mode),
    0x41f09de5: ('launch_up_speed', _decode_launch_up_speed),
    0x3e8817aa: ('target_speed_multiplier', _decode_target_speed_multiplier),
    0x2e94d98e: ('extra_distance_past_target_point', _decode_extra_distance_past_target_point),
    0xe296b29f: ('max_spline_distance_from_starting_point', _decode_max_spline_distance_from_starting_point),
    0x82dbfcf1: ('reverse_direction_when_target_is_thrown', _decode_reverse_direction_when_target_is_thrown),
    0x56256f59: ('max_life_time', _decode_max_life_time),
    0x17e5811d: ('max_life_time_safe_guard', _decode_max_life_time_safe_guard),
    0x3e486dc0: ('number_of_damage_effects', _decode_number_of_damage_effects),
    0x2acbfb27: ('align_damage_effects_to_surface_on_creation', _decode_align_damage_effects_to_surface_on_creation),
    0xe3f96a88: ('allow_damage_effects_to_slave_to_platforms', _decode_allow_damage_effects_to_slave_to_platforms),
    0x3e0121c3: ('damage_effect', _decode_damage_effect),
    0x7f313285: ('damage_effect2', _decode_damage_effect2),
    0xf897f9c6: ('damage_effect3', _decode_damage_effect3),
    0x5318357d: ('apply_contact_rules', _decode_apply_contact_rules),
    0xab0f5158: ('ignore_all_but_player', _decode_ignore_all_but_player),
    0xb9e149e6: ('disable_behavior_after_applying_velocity', _decode_disable_behavior_after_applying_velocity),
    0xced50f78: ('disable_max_life_time', _decode_disable_max_life_time),
    0xd0e7f960: ('limit_speed', _decode_limit_speed),
    0x140ef2cc: ('maximum_speed', _decode_maximum_speed),
}
