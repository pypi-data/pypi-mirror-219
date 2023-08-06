# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Kralee(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flavor: int = dataclasses.field(default=0)  # Choice
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    waypoint_approach_distance: float = dataclasses.field(default=2.5)
    visible_distance: float = dataclasses.field(default=2.5)
    wall_turn_speed: float = dataclasses.field(default=360.0)
    floor_turn_speed: float = dataclasses.field(default=180.0)
    down_turn_speed: float = dataclasses.field(default=120.0)
    unknown_0xd5c25506: float = dataclasses.field(default=0.4000000059604645)
    projectile_bounds_multiplier: float = dataclasses.field(default=1.0)
    collision_look_ahead: float = dataclasses.field(default=0.019999999552965164)
    warp_in_time: float = dataclasses.field(default=1.0)
    warp_out_time: float = dataclasses.field(default=1.0)
    visible_time: float = dataclasses.field(default=0.0)
    unknown_0x7bba36ff: float = dataclasses.field(default=0.0)
    invisible_time: float = dataclasses.field(default=0.0)
    unknown_0x4e4ae0e4: float = dataclasses.field(default=0.0)
    warp_attack_radius: float = dataclasses.field(default=2.5)
    warp_attack_knockback: float = dataclasses.field(default=10.0)
    warp_attack_damage: float = dataclasses.field(default=10.0)
    anim_speed_scalar: float = dataclasses.field(default=1.0)
    max_audible_distance: float = dataclasses.field(default=50.0)
    warp_in_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    warp_out_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    warp_in_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    warp_out_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    initially_paused: bool = dataclasses.field(default=False)
    initially_invisible: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'KRAL'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['WallCrawler.rel', 'Kralee.rel']

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x1d')  # 29 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbesrJ')  # 0xbe73724a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flavor))

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'mass': 25.0, 'speed': 3.0, 'turn_speed': 720.0, 'detection_range': 5.0, 'detection_height_range': 5.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'max_attack_range': 20.0, 'damage_wait_time': 3.0, 'collision_radius': 0.20000000298023224, 'collision_height': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's;\xd2|')  # 0x733bd27c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.waypoint_approach_distance))

        data.write(b'\xa7%0\xe8')  # 0xa72530e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visible_distance))

        data.write(b'\xacG\xc6(')  # 0xac47c628
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wall_turn_speed))

        data.write(b'\x8eO{)')  # 0x8e4f7b29
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_turn_speed))

        data.write(b'=<\x1bv')  # 0x3d3c1b76
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.down_turn_speed))

        data.write(b'\xd5\xc2U\x06')  # 0xd5c25506
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd5c25506))

        data.write(b't.\xab ')  # 0x742eab20
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_bounds_multiplier))

        data.write(b'\x80\xa8\x19\t')  # 0x80a81909
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_look_ahead))

        data.write(b'\xedj\x93S')  # 0xed6a9353
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.warp_in_time))

        data.write(b'\x031S\xa0')  # 0x33153a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.warp_out_time))

        data.write(b'W\x04\x89|')  # 0x5704897c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visible_time))

        data.write(b'{\xba6\xff')  # 0x7bba36ff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7bba36ff))

        data.write(b'\xbb\xd4\xb1\x0c')  # 0xbbd4b10c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.invisible_time))

        data.write(b'NJ\xe0\xe4')  # 0x4e4ae0e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4e4ae0e4))

        data.write(b'\xadi\xac2')  # 0xad69ac32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.warp_attack_radius))

        data.write(b'\xc7\xd2\xed\xe8')  # 0xc7d2ede8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.warp_attack_knockback))

        data.write(b'\xb1\xa2c5')  # 0xb1a26335
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.warp_attack_damage))

        data.write(b'\x85\x90H;')  # 0x8590483b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anim_speed_scalar))

        data.write(b'!NH\xa0')  # 0x214e48a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_audible_distance))

        data.write(b'5\x1d\xbcs')  # 0x351dbc73
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.warp_in_particle_effect))

        data.write(b'-r\xba{')  # 0x2d72ba7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.warp_out_particle_effect))

        data.write(b'\x80\xb5\x83$')  # 0x80b58324
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.warp_in_sound))

        data.write(b'\xa4\xef{B')  # 0xa4ef7b42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.warp_out_sound))

        data.write(b'\xc3\xccC\x7f')  # 0xc3cc437f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.initially_paused))

        data.write(b's\x8d\x1c\x80')  # 0x738d1c80
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.initially_invisible))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            flavor=data['flavor'],
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            waypoint_approach_distance=data['waypoint_approach_distance'],
            visible_distance=data['visible_distance'],
            wall_turn_speed=data['wall_turn_speed'],
            floor_turn_speed=data['floor_turn_speed'],
            down_turn_speed=data['down_turn_speed'],
            unknown_0xd5c25506=data['unknown_0xd5c25506'],
            projectile_bounds_multiplier=data['projectile_bounds_multiplier'],
            collision_look_ahead=data['collision_look_ahead'],
            warp_in_time=data['warp_in_time'],
            warp_out_time=data['warp_out_time'],
            visible_time=data['visible_time'],
            unknown_0x7bba36ff=data['unknown_0x7bba36ff'],
            invisible_time=data['invisible_time'],
            unknown_0x4e4ae0e4=data['unknown_0x4e4ae0e4'],
            warp_attack_radius=data['warp_attack_radius'],
            warp_attack_knockback=data['warp_attack_knockback'],
            warp_attack_damage=data['warp_attack_damage'],
            anim_speed_scalar=data['anim_speed_scalar'],
            max_audible_distance=data['max_audible_distance'],
            warp_in_particle_effect=data['warp_in_particle_effect'],
            warp_out_particle_effect=data['warp_out_particle_effect'],
            warp_in_sound=data['warp_in_sound'],
            warp_out_sound=data['warp_out_sound'],
            initially_paused=data['initially_paused'],
            initially_invisible=data['initially_invisible'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flavor': self.flavor,
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'waypoint_approach_distance': self.waypoint_approach_distance,
            'visible_distance': self.visible_distance,
            'wall_turn_speed': self.wall_turn_speed,
            'floor_turn_speed': self.floor_turn_speed,
            'down_turn_speed': self.down_turn_speed,
            'unknown_0xd5c25506': self.unknown_0xd5c25506,
            'projectile_bounds_multiplier': self.projectile_bounds_multiplier,
            'collision_look_ahead': self.collision_look_ahead,
            'warp_in_time': self.warp_in_time,
            'warp_out_time': self.warp_out_time,
            'visible_time': self.visible_time,
            'unknown_0x7bba36ff': self.unknown_0x7bba36ff,
            'invisible_time': self.invisible_time,
            'unknown_0x4e4ae0e4': self.unknown_0x4e4ae0e4,
            'warp_attack_radius': self.warp_attack_radius,
            'warp_attack_knockback': self.warp_attack_knockback,
            'warp_attack_damage': self.warp_attack_damage,
            'anim_speed_scalar': self.anim_speed_scalar,
            'max_audible_distance': self.max_audible_distance,
            'warp_in_particle_effect': self.warp_in_particle_effect,
            'warp_out_particle_effect': self.warp_out_particle_effect,
            'warp_in_sound': self.warp_in_sound,
            'warp_out_sound': self.warp_out_sound,
            'initially_paused': self.initially_paused,
            'initially_invisible': self.initially_invisible,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_warp_in_particle_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.warp_in_particle_effect)

    def _dependencies_for_warp_out_particle_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.warp_out_particle_effect)

    def _dependencies_for_warp_in_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.warp_in_sound)

    def _dependencies_for_warp_out_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.warp_out_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_warp_in_particle_effect, "warp_in_particle_effect", "AssetId"),
            (self._dependencies_for_warp_out_particle_effect, "warp_out_particle_effect", "AssetId"),
            (self._dependencies_for_warp_in_sound, "warp_in_sound", "int"),
            (self._dependencies_for_warp_out_sound, "warp_out_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Kralee.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flavor(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'mass': 25.0, 'speed': 3.0, 'turn_speed': 720.0, 'detection_range': 5.0, 'detection_height_range': 5.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'max_attack_range': 20.0, 'damage_wait_time': 3.0, 'collision_radius': 0.20000000298023224, 'collision_height': 5.0})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_waypoint_approach_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wall_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_down_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd5c25506(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile_bounds_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_look_ahead(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_warp_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_warp_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visible_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7bba36ff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_invisible_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4e4ae0e4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_warp_attack_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_warp_attack_knockback(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_warp_attack_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_anim_speed_scalar(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_warp_in_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_warp_out_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_warp_in_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_warp_out_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_initially_paused(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_initially_invisible(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xbe73724a: ('flavor', _decode_flavor),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x733bd27c: ('waypoint_approach_distance', _decode_waypoint_approach_distance),
    0xa72530e8: ('visible_distance', _decode_visible_distance),
    0xac47c628: ('wall_turn_speed', _decode_wall_turn_speed),
    0x8e4f7b29: ('floor_turn_speed', _decode_floor_turn_speed),
    0x3d3c1b76: ('down_turn_speed', _decode_down_turn_speed),
    0xd5c25506: ('unknown_0xd5c25506', _decode_unknown_0xd5c25506),
    0x742eab20: ('projectile_bounds_multiplier', _decode_projectile_bounds_multiplier),
    0x80a81909: ('collision_look_ahead', _decode_collision_look_ahead),
    0xed6a9353: ('warp_in_time', _decode_warp_in_time),
    0x33153a0: ('warp_out_time', _decode_warp_out_time),
    0x5704897c: ('visible_time', _decode_visible_time),
    0x7bba36ff: ('unknown_0x7bba36ff', _decode_unknown_0x7bba36ff),
    0xbbd4b10c: ('invisible_time', _decode_invisible_time),
    0x4e4ae0e4: ('unknown_0x4e4ae0e4', _decode_unknown_0x4e4ae0e4),
    0xad69ac32: ('warp_attack_radius', _decode_warp_attack_radius),
    0xc7d2ede8: ('warp_attack_knockback', _decode_warp_attack_knockback),
    0xb1a26335: ('warp_attack_damage', _decode_warp_attack_damage),
    0x8590483b: ('anim_speed_scalar', _decode_anim_speed_scalar),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x351dbc73: ('warp_in_particle_effect', _decode_warp_in_particle_effect),
    0x2d72ba7b: ('warp_out_particle_effect', _decode_warp_out_particle_effect),
    0x80b58324: ('warp_in_sound', _decode_warp_in_sound),
    0xa4ef7b42: ('warp_out_sound', _decode_warp_out_sound),
    0xc3cc437f: ('initially_paused', _decode_initially_paused),
    0x738d1c80: ('initially_invisible', _decode_initially_invisible),
}
