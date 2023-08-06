# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class FishCloud(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    active: bool = dataclasses.field(default=True)
    fish_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    fish_count: float = dataclasses.field(default=20.0)
    speed: float = dataclasses.field(default=3.0)
    influence_distance: float = dataclasses.field(default=2.0)
    unknown_0x61959f0d: float = dataclasses.field(default=0.4000000059604645)
    alignment_priority: float = dataclasses.field(default=0.8999999761581421)
    separation_priority: float = dataclasses.field(default=1.0)
    projectile_priority: float = dataclasses.field(default=1.0)
    player_priority: float = dataclasses.field(default=0.4000000059604645)
    containment_priority: float = dataclasses.field(default=0.20000000298023224)
    wander_priority: float = dataclasses.field(default=0.0)
    wander_amount: float = dataclasses.field(default=0.0)
    player_ball_priority: float = dataclasses.field(default=0.0)
    player_ball_distance: float = dataclasses.field(default=30.0)
    projectile_decay_rate: float = dataclasses.field(default=0.10000000149011612)
    player_decay_rate: float = dataclasses.field(default=0.10000000149011612)
    look_ahead_time: float = dataclasses.field(default=0.5)
    update_frame: int = dataclasses.field(default=3)
    material_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    can_be_killed: bool = dataclasses.field(default=False)
    collision_radius: float = dataclasses.field(default=0.0)
    death_effect0: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    death_effect0_count: int = dataclasses.field(default=0)
    death_effect1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    death_effect1_count: int = dataclasses.field(default=0)
    death_effect2: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    death_effect2_count: int = dataclasses.field(default=0)
    death_effect3: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    death_effect3_count: int = dataclasses.field(default=0)
    death_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0xc320a050: bool = dataclasses.field(default=True)
    unknown_0xcd4c81a1: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'FISH'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['FishCloud.rel']

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
        data.write(b'\x00#')  # 35 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xbb/E')  # 0xc6bb2f45
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.active))

        data.write(b'y\x90\xa3\xb6')  # 0x7990a3b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.fish_model))

        data.write(b'\xe2_\xb0\x8c')  # 0xe25fb08c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1\xc0ru')  # 0xf1c07275
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fish_count))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'xd\xad\x0e')  # 0x7864ad0e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.influence_distance))

        data.write(b'a\x95\x9f\r')  # 0x61959f0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61959f0d))

        data.write(b'HA\xf1\xde')  # 0x4841f1de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.alignment_priority))

        data.write(b'\xd2\x93\xeb\xc4')  # 0xd293ebc4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.separation_priority))

        data.write(b'_6*\x14')  # 0x5f362a14
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_priority))

        data.write(b'\xec\x9bs\xc2')  # 0xec9b73c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_priority))

        data.write(b'\x7f\xf1F\x9e')  # 0x7ff1469e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.containment_priority))

        data.write(b'|\xe1xp')  # 0x7ce17870
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wander_priority))

        data.write(b':%\xf0\x9d')  # 0x3a25f09d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wander_amount))

        data.write(b'#\xa1`\xf3')  # 0x23a160f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_ball_priority))

        data.write(b'\xf0g\x14\x10')  # 0xf0671410
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_ball_distance))

        data.write(b'\xa1trh')  # 0xa1747268
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_decay_rate))

        data.write(b'\xcew\xa8\xd0')  # 0xce77a8d0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_decay_rate))

        data.write(b'\x8c\xb2\x0cS')  # 0x8cb20c53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.look_ahead_time))

        data.write(b'!\xb3\xd0|')  # 0x21b3d07c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.update_frame))

        data.write(b'\x1f\x83\xd3P')  # 0x1f83d350
        data.write(b'\x00\x10')  # size
        self.material_color.to_stream(data)

        data.write(b'\xf60\xb8\x9f')  # 0xf630b89f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_be_killed))

        data.write(b'\x8aj\xb19')  # 0x8a6ab139
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_radius))

        data.write(b'[\xa8bE')  # 0x5ba86245
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death_effect0))

        data.write(b'\xa8#/\xb1')  # 0xa8232fb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_effect0_count))

        data.write(b'\x90\xf4\xb1\xe0')  # 0x90f4b1e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death_effect1))

        data.write(b'\xbfX;\xf2')  # 0xbf583bf2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_effect1_count))

        data.write(b'\x16`\xc3N')  # 0x1660c34e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death_effect2))

        data.write(b'\x86\xd5\x077')  # 0x86d50737
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_effect2_count))

        data.write(b'\xdd<\x10\xeb')  # 0xdd3c10eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.death_effect3))

        data.write(b'\x91\xae\x13t')  # 0x91ae1374
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_effect3_count))

        data.write(b'=\xe2o\xc8')  # 0x3de26fc8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_sound))

        data.write(b'\xc3 \xa0P')  # 0xc320a050
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc320a050))

        data.write(b'\xcdL\x81\xa1')  # 0xcd4c81a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcd4c81a1))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            active=data['active'],
            fish_model=data['fish_model'],
            animation_information=AnimationParameters.from_json(data['animation_information']),
            fish_count=data['fish_count'],
            speed=data['speed'],
            influence_distance=data['influence_distance'],
            unknown_0x61959f0d=data['unknown_0x61959f0d'],
            alignment_priority=data['alignment_priority'],
            separation_priority=data['separation_priority'],
            projectile_priority=data['projectile_priority'],
            player_priority=data['player_priority'],
            containment_priority=data['containment_priority'],
            wander_priority=data['wander_priority'],
            wander_amount=data['wander_amount'],
            player_ball_priority=data['player_ball_priority'],
            player_ball_distance=data['player_ball_distance'],
            projectile_decay_rate=data['projectile_decay_rate'],
            player_decay_rate=data['player_decay_rate'],
            look_ahead_time=data['look_ahead_time'],
            update_frame=data['update_frame'],
            material_color=Color.from_json(data['material_color']),
            can_be_killed=data['can_be_killed'],
            collision_radius=data['collision_radius'],
            death_effect0=data['death_effect0'],
            death_effect0_count=data['death_effect0_count'],
            death_effect1=data['death_effect1'],
            death_effect1_count=data['death_effect1_count'],
            death_effect2=data['death_effect2'],
            death_effect2_count=data['death_effect2_count'],
            death_effect3=data['death_effect3'],
            death_effect3_count=data['death_effect3_count'],
            death_sound=data['death_sound'],
            unknown_0xc320a050=data['unknown_0xc320a050'],
            unknown_0xcd4c81a1=data['unknown_0xcd4c81a1'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'active': self.active,
            'fish_model': self.fish_model,
            'animation_information': self.animation_information.to_json(),
            'fish_count': self.fish_count,
            'speed': self.speed,
            'influence_distance': self.influence_distance,
            'unknown_0x61959f0d': self.unknown_0x61959f0d,
            'alignment_priority': self.alignment_priority,
            'separation_priority': self.separation_priority,
            'projectile_priority': self.projectile_priority,
            'player_priority': self.player_priority,
            'containment_priority': self.containment_priority,
            'wander_priority': self.wander_priority,
            'wander_amount': self.wander_amount,
            'player_ball_priority': self.player_ball_priority,
            'player_ball_distance': self.player_ball_distance,
            'projectile_decay_rate': self.projectile_decay_rate,
            'player_decay_rate': self.player_decay_rate,
            'look_ahead_time': self.look_ahead_time,
            'update_frame': self.update_frame,
            'material_color': self.material_color.to_json(),
            'can_be_killed': self.can_be_killed,
            'collision_radius': self.collision_radius,
            'death_effect0': self.death_effect0,
            'death_effect0_count': self.death_effect0_count,
            'death_effect1': self.death_effect1,
            'death_effect1_count': self.death_effect1_count,
            'death_effect2': self.death_effect2,
            'death_effect2_count': self.death_effect2_count,
            'death_effect3': self.death_effect3,
            'death_effect3_count': self.death_effect3_count,
            'death_sound': self.death_sound,
            'unknown_0xc320a050': self.unknown_0xc320a050,
            'unknown_0xcd4c81a1': self.unknown_0xcd4c81a1,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_fish_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.fish_model)

    def _dependencies_for_animation_information(self, asset_manager):
        yield from self.animation_information.dependencies_for(asset_manager)

    def _dependencies_for_death_effect0(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.death_effect0)

    def _dependencies_for_death_effect1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.death_effect1)

    def _dependencies_for_death_effect2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.death_effect2)

    def _dependencies_for_death_effect3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.death_effect3)

    def _dependencies_for_death_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.death_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_fish_model, "fish_model", "AssetId"),
            (self._dependencies_for_animation_information, "animation_information", "AnimationParameters"),
            (self._dependencies_for_death_effect0, "death_effect0", "AssetId"),
            (self._dependencies_for_death_effect1, "death_effect1", "AssetId"),
            (self._dependencies_for_death_effect2, "death_effect2", "AssetId"),
            (self._dependencies_for_death_effect3, "death_effect3", "AssetId"),
            (self._dependencies_for_death_sound, "death_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for FishCloud.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_active(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fish_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_fish_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_influence_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61959f0d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_alignment_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_separation_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_containment_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wander_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wander_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_ball_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_ball_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile_decay_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_player_decay_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_look_ahead_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_update_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_material_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_can_be_killed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_collision_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_effect0(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_death_effect0_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_effect1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_death_effect1_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_effect2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_death_effect2_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_effect3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_death_effect3_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc320a050(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xcd4c81a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc6bb2f45: ('active', _decode_active),
    0x7990a3b6: ('fish_model', _decode_fish_model),
    0xe25fb08c: ('animation_information', _decode_animation_information),
    0xf1c07275: ('fish_count', _decode_fish_count),
    0x6392404e: ('speed', _decode_speed),
    0x7864ad0e: ('influence_distance', _decode_influence_distance),
    0x61959f0d: ('unknown_0x61959f0d', _decode_unknown_0x61959f0d),
    0x4841f1de: ('alignment_priority', _decode_alignment_priority),
    0xd293ebc4: ('separation_priority', _decode_separation_priority),
    0x5f362a14: ('projectile_priority', _decode_projectile_priority),
    0xec9b73c2: ('player_priority', _decode_player_priority),
    0x7ff1469e: ('containment_priority', _decode_containment_priority),
    0x7ce17870: ('wander_priority', _decode_wander_priority),
    0x3a25f09d: ('wander_amount', _decode_wander_amount),
    0x23a160f3: ('player_ball_priority', _decode_player_ball_priority),
    0xf0671410: ('player_ball_distance', _decode_player_ball_distance),
    0xa1747268: ('projectile_decay_rate', _decode_projectile_decay_rate),
    0xce77a8d0: ('player_decay_rate', _decode_player_decay_rate),
    0x8cb20c53: ('look_ahead_time', _decode_look_ahead_time),
    0x21b3d07c: ('update_frame', _decode_update_frame),
    0x1f83d350: ('material_color', _decode_material_color),
    0xf630b89f: ('can_be_killed', _decode_can_be_killed),
    0x8a6ab139: ('collision_radius', _decode_collision_radius),
    0x5ba86245: ('death_effect0', _decode_death_effect0),
    0xa8232fb1: ('death_effect0_count', _decode_death_effect0_count),
    0x90f4b1e0: ('death_effect1', _decode_death_effect1),
    0xbf583bf2: ('death_effect1_count', _decode_death_effect1_count),
    0x1660c34e: ('death_effect2', _decode_death_effect2),
    0x86d50737: ('death_effect2_count', _decode_death_effect2_count),
    0xdd3c10eb: ('death_effect3', _decode_death_effect3),
    0x91ae1374: ('death_effect3_count', _decode_death_effect3_count),
    0x3de26fc8: ('death_sound', _decode_death_sound),
    0xc320a050: ('unknown_0xc320a050', _decode_unknown_0xc320a050),
    0xcd4c81a1: ('unknown_0xcd4c81a1', _decode_unknown_0xcd4c81a1),
}
