# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.FishCloudAggressionData import FishCloudAggressionData
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class FishCloud(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    fish_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    fish_count: int = dataclasses.field(default=20)
    fish_scale: float = dataclasses.field(default=0.0)
    speed: float = dataclasses.field(default=3.0)
    maximum_turn_angle: float = dataclasses.field(default=0.0)
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
    unknown_0x9939d085: int = dataclasses.field(default=3257279650)  # Choice
    material_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    can_be_killed: bool = dataclasses.field(default=False)
    collision_radius: float = dataclasses.field(default=0.0)
    respawn_wait_time: float = dataclasses.field(default=0.0)
    respawn_fade_time: float = dataclasses.field(default=0.0)
    death_effect0: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    death_effect0_count: int = dataclasses.field(default=0)
    death_effect0_scale: float = dataclasses.field(default=1.0)
    death_effect1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    death_effect1_count: int = dataclasses.field(default=0)
    death_effect1_scale: float = dataclasses.field(default=1.0)
    death_effect2: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    death_effect2_count: int = dataclasses.field(default=0)
    death_effect2_scale: float = dataclasses.field(default=1.0)
    death_effect3: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    death_effect3_count: int = dataclasses.field(default=0)
    death_effect3_scale: float = dataclasses.field(default=1.0)
    death_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    looped_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_0xd7bce5da: float = dataclasses.field(default=20.0)
    unknown_0xe8b7e32e: float = dataclasses.field(default=25.0)
    unknown_0xc320a050: bool = dataclasses.field(default=True)
    unknown_0xcd4c81a1: bool = dataclasses.field(default=True)
    aggression_data: FishCloudAggressionData = dataclasses.field(default_factory=FishCloudAggressionData)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'FISH'

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
        data.write(b'\x00/')  # 47 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\x90\xa3\xb6')  # 0x7990a3b6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fish_model))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'"d\x06.')  # 0x2264062e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.fish_count))

        data.write(b'\x97\xbe\xffO')  # 0x97beff4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fish_scale))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'\xcb\xabT\xc1')  # 0xcbab54c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_turn_angle))

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

        data.write(b'\x999\xd0\x85')  # 0x9939d085
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x9939d085))

        data.write(b'\x1f\x83\xd3P')  # 0x1f83d350
        data.write(b'\x00\x10')  # size
        self.material_color.to_stream(data)

        data.write(b'\xf60\xb8\x9f')  # 0xf630b89f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_be_killed))

        data.write(b'\x8aj\xb19')  # 0x8a6ab139
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_radius))

        data.write(b'\xfeD\xb7\xa4')  # 0xfe44b7a4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_wait_time))

        data.write(b'\x94-o*')  # 0x942d6f2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_fade_time))

        data.write(b'[\xa8bE')  # 0x5ba86245
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_effect0))

        data.write(b'\xa8#/\xb1')  # 0xa8232fb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_effect0_count))

        data.write(b'#\xd5{\xb1')  # 0x23d57bb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.death_effect0_scale))

        data.write(b'\x90\xf4\xb1\xe0')  # 0x90f4b1e0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_effect1))

        data.write(b'\xbfX;\xf2')  # 0xbf583bf2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_effect1_count))

        data.write(b'\xe2[\xa4q')  # 0xe25ba471
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.death_effect1_scale))

        data.write(b'\x16`\xc3N')  # 0x1660c34e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_effect2))

        data.write(b'\x86\xd5\x077')  # 0x86d50737
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_effect2_count))

        data.write(b'{\xb9\xc2p')  # 0x7bb9c270
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.death_effect2_scale))

        data.write(b'\xdd<\x10\xeb')  # 0xdd3c10eb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_effect3))

        data.write(b'\x91\xae\x13t')  # 0x91ae1374
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.death_effect3_count))

        data.write(b'\xba7\x1d\xb0')  # 0xba371db0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.death_effect3_scale))

        data.write(b'\xc7\xc3\xf6\x10')  # 0xc7c3f610
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.death_sound))

        data.write(b'\x05\xc7\x95`')  # 0x5c79560
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.looped_sound))

        data.write(b'\xd7\xbc\xe5\xda')  # 0xd7bce5da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd7bce5da))

        data.write(b'\xe8\xb7\xe3.')  # 0xe8b7e32e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe8b7e32e))

        data.write(b'\xc3 \xa0P')  # 0xc320a050
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc320a050))

        data.write(b'\xcdL\x81\xa1')  # 0xcd4c81a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcd4c81a1))

        data.write(b'\r\x9cg\x15')  # 0xd9c6715
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aggression_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            fish_model=data['fish_model'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            fish_count=data['fish_count'],
            fish_scale=data['fish_scale'],
            speed=data['speed'],
            maximum_turn_angle=data['maximum_turn_angle'],
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
            unknown_0x9939d085=data['unknown_0x9939d085'],
            material_color=Color.from_json(data['material_color']),
            can_be_killed=data['can_be_killed'],
            collision_radius=data['collision_radius'],
            respawn_wait_time=data['respawn_wait_time'],
            respawn_fade_time=data['respawn_fade_time'],
            death_effect0=data['death_effect0'],
            death_effect0_count=data['death_effect0_count'],
            death_effect0_scale=data['death_effect0_scale'],
            death_effect1=data['death_effect1'],
            death_effect1_count=data['death_effect1_count'],
            death_effect1_scale=data['death_effect1_scale'],
            death_effect2=data['death_effect2'],
            death_effect2_count=data['death_effect2_count'],
            death_effect2_scale=data['death_effect2_scale'],
            death_effect3=data['death_effect3'],
            death_effect3_count=data['death_effect3_count'],
            death_effect3_scale=data['death_effect3_scale'],
            death_sound=data['death_sound'],
            looped_sound=data['looped_sound'],
            unknown_0xd7bce5da=data['unknown_0xd7bce5da'],
            unknown_0xe8b7e32e=data['unknown_0xe8b7e32e'],
            unknown_0xc320a050=data['unknown_0xc320a050'],
            unknown_0xcd4c81a1=data['unknown_0xcd4c81a1'],
            aggression_data=FishCloudAggressionData.from_json(data['aggression_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'fish_model': self.fish_model,
            'character_animation_information': self.character_animation_information.to_json(),
            'fish_count': self.fish_count,
            'fish_scale': self.fish_scale,
            'speed': self.speed,
            'maximum_turn_angle': self.maximum_turn_angle,
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
            'unknown_0x9939d085': self.unknown_0x9939d085,
            'material_color': self.material_color.to_json(),
            'can_be_killed': self.can_be_killed,
            'collision_radius': self.collision_radius,
            'respawn_wait_time': self.respawn_wait_time,
            'respawn_fade_time': self.respawn_fade_time,
            'death_effect0': self.death_effect0,
            'death_effect0_count': self.death_effect0_count,
            'death_effect0_scale': self.death_effect0_scale,
            'death_effect1': self.death_effect1,
            'death_effect1_count': self.death_effect1_count,
            'death_effect1_scale': self.death_effect1_scale,
            'death_effect2': self.death_effect2,
            'death_effect2_count': self.death_effect2_count,
            'death_effect2_scale': self.death_effect2_scale,
            'death_effect3': self.death_effect3,
            'death_effect3_count': self.death_effect3_count,
            'death_effect3_scale': self.death_effect3_scale,
            'death_sound': self.death_sound,
            'looped_sound': self.looped_sound,
            'unknown_0xd7bce5da': self.unknown_0xd7bce5da,
            'unknown_0xe8b7e32e': self.unknown_0xe8b7e32e,
            'unknown_0xc320a050': self.unknown_0xc320a050,
            'unknown_0xcd4c81a1': self.unknown_0xcd4c81a1,
            'aggression_data': self.aggression_data.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_fish_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_fish_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_fish_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_turn_angle(data: typing.BinaryIO, property_size: int):
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


def _decode_unknown_0x9939d085(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_material_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_can_be_killed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_collision_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_respawn_wait_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_respawn_fade_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_effect0(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_death_effect0_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_effect0_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_effect1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_death_effect1_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_effect1_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_effect2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_death_effect2_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_effect2_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_effect3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_death_effect3_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_death_effect3_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_looped_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xd7bce5da(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe8b7e32e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc320a050(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xcd4c81a1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_aggression_data(data: typing.BinaryIO, property_size: int):
    return FishCloudAggressionData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7990a3b6: ('fish_model', _decode_fish_model),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0x2264062e: ('fish_count', _decode_fish_count),
    0x97beff4f: ('fish_scale', _decode_fish_scale),
    0x6392404e: ('speed', _decode_speed),
    0xcbab54c1: ('maximum_turn_angle', _decode_maximum_turn_angle),
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
    0x9939d085: ('unknown_0x9939d085', _decode_unknown_0x9939d085),
    0x1f83d350: ('material_color', _decode_material_color),
    0xf630b89f: ('can_be_killed', _decode_can_be_killed),
    0x8a6ab139: ('collision_radius', _decode_collision_radius),
    0xfe44b7a4: ('respawn_wait_time', _decode_respawn_wait_time),
    0x942d6f2a: ('respawn_fade_time', _decode_respawn_fade_time),
    0x5ba86245: ('death_effect0', _decode_death_effect0),
    0xa8232fb1: ('death_effect0_count', _decode_death_effect0_count),
    0x23d57bb1: ('death_effect0_scale', _decode_death_effect0_scale),
    0x90f4b1e0: ('death_effect1', _decode_death_effect1),
    0xbf583bf2: ('death_effect1_count', _decode_death_effect1_count),
    0xe25ba471: ('death_effect1_scale', _decode_death_effect1_scale),
    0x1660c34e: ('death_effect2', _decode_death_effect2),
    0x86d50737: ('death_effect2_count', _decode_death_effect2_count),
    0x7bb9c270: ('death_effect2_scale', _decode_death_effect2_scale),
    0xdd3c10eb: ('death_effect3', _decode_death_effect3),
    0x91ae1374: ('death_effect3_count', _decode_death_effect3_count),
    0xba371db0: ('death_effect3_scale', _decode_death_effect3_scale),
    0xc7c3f610: ('death_sound', _decode_death_sound),
    0x5c79560: ('looped_sound', _decode_looped_sound),
    0xd7bce5da: ('unknown_0xd7bce5da', _decode_unknown_0xd7bce5da),
    0xe8b7e32e: ('unknown_0xe8b7e32e', _decode_unknown_0xe8b7e32e),
    0xc320a050: ('unknown_0xc320a050', _decode_unknown_0xc320a050),
    0xcd4c81a1: ('unknown_0xcd4c81a1', _decode_unknown_0xcd4c81a1),
    0xd9c6715: ('aggression_data', _decode_aggression_data),
}
