# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Color import Color
from retro_data_structures.properties.dkc_returns.core.Spline import Spline
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class GrabbedBehaviorData(BaseProperty):
    is_barrel: bool = dataclasses.field(default=False)
    grabbable_at_creation: bool = dataclasses.field(default=False)
    grabbable_when_settled: bool = dataclasses.field(default=True)
    mark_grabbable_immediately_on_settle: bool = dataclasses.field(default=False)
    set_as_thrown_at_creation: bool = dataclasses.field(default=False)
    spawn_other_player_on_explosion: bool = dataclasses.field(default=False)
    explode_on_impact_with_floor: bool = dataclasses.field(default=False)
    explode_on_impact_with_wall: bool = dataclasses.field(default=True)
    explode_on_impact_with_actor: bool = dataclasses.field(default=False)
    explode_on_impact_with_bouncy: bool = dataclasses.field(default=False)
    explode_on_impact_with_character: bool = dataclasses.field(default=False)
    disable_character_material_when_grabbed: bool = dataclasses.field(default=False)
    apply_damage_on_impact_with_character: bool = dataclasses.field(default=True)
    apply_damage_on_impact_with_held_character: bool = dataclasses.field(default=True)
    apply_damage_on_impact_with_thrown_character: bool = dataclasses.field(default=True)
    bounce_on_impact_with_held_character: bool = dataclasses.field(default=False)
    force_drop_on_impact_with_held_character: bool = dataclasses.field(default=False)
    explode_on_impact_with_held_character: bool = dataclasses.field(default=False)
    explode_on_impact_with_thrown_character: bool = dataclasses.field(default=False)
    explode_on_impact_with_player: bool = dataclasses.field(default=False)
    explode_on_impact_when_dropped: bool = dataclasses.field(default=False)
    explode_on_impact_with_actor_when_held: bool = dataclasses.field(default=False)
    explode_on_impact_with_character_when_held: bool = dataclasses.field(default=False)
    apply_damage_on_impact_with_player: bool = dataclasses.field(default=True)
    disable_collision_actors_on_throw: bool = dataclasses.field(default=False)
    delay_explode_on_stopped_moving: float = dataclasses.field(default=0.0)
    delay_explode_on_impact_with_player: float = dataclasses.field(default=0.0)
    explode_time_after_throw: float = dataclasses.field(default=0.0)
    flash_on_explode_timer: bool = dataclasses.field(default=False)
    start_flash_on_enter_force_trigger: bool = dataclasses.field(default=False)
    start_flashing_time: float = dataclasses.field(default=0.0)
    flash_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=0.0, b=0.0, a=0.0))
    flash_incandescence: bool = dataclasses.field(default=False)
    initial_flash_period: float = dataclasses.field(default=1.0)
    final_flash_period: float = dataclasses.field(default=1.0)
    accelerate_flash_duration: float = dataclasses.field(default=0.0)
    is_indestructible: bool = dataclasses.field(default=False)
    is_immovable: bool = dataclasses.field(default=True)
    lock_to_player_path_when_thrown: bool = dataclasses.field(default=True)
    allow_player_walkthrough: bool = dataclasses.field(default=False)
    allow_ai_walkthrough: bool = dataclasses.field(default=False)
    distance_from_spline: float = dataclasses.field(default=0.0)
    can_explode_off_screen: bool = dataclasses.field(default=True)
    start_timer_when_partially_offscreen: bool = dataclasses.field(default=False)
    max_time_off_screen: float = dataclasses.field(default=0.5)
    ground_impact_damp: float = dataclasses.field(default=1.0)
    wall_impact_damp: float = dataclasses.field(default=1.0)
    carried_object_impact_damp: float = dataclasses.field(default=1.0)
    ground_friction: float = dataclasses.field(default=0.0)
    min_downward_velocity_to_bounce: float = dataclasses.field(default=6.0)
    bounce_factor: float = dataclasses.field(default=0.5)
    max_vertical_bounce_speed: float = dataclasses.field(default=10.0)
    heal_players_on_explosion: bool = dataclasses.field(default=False)
    flying_effect_speed: float = dataclasses.field(default=3.0)
    flying_effect_target_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    flying_health_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    explosion_health_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    health_sound_effect: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    roll_through_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    roll_through_sound_effect: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    hit_by_thrown_object_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    flash_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    flash_sound_pitch: Spline = dataclasses.field(default_factory=Spline)
    flash_sound_volume: Spline = dataclasses.field(default_factory=Spline)
    dk_optional_throw_velocity: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    diddy_optional_throw_velocity: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))

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
        data.write(b'\x00B')  # 66 properties

        data.write(b'z\xcbx\xbd')  # 0x7acb78bd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_barrel))

        data.write(b'\xdb\x0eZQ')  # 0xdb0e5a51
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grabbable_at_creation))

        data.write(b'KG\x01\xdd')  # 0x4b4701dd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grabbable_when_settled))

        data.write(b'\xf8|c\xc6')  # 0xf87c63c6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.mark_grabbable_immediately_on_settle))

        data.write(b'\xd3B\xbci')  # 0xd342bc69
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.set_as_thrown_at_creation))

        data.write(b'\xd3-\x9f\xe3')  # 0xd32d9fe3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.spawn_other_player_on_explosion))

        data.write(b'\xd1B\xe3\xf1')  # 0xd142e3f1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_floor))

        data.write(b'(\xbe\xcd\xb5')  # 0x28becdb5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_wall))

        data.write(b'\t\xdaT\xa0')  # 0x9da54a0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_actor))

        data.write(b'\xf3\xf8\xebA')  # 0xf3f8eb41
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_bouncy))

        data.write(b'\x0eZ,\xd9')  # 0xe5a2cd9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_character))

        data.write(b"'k\xa3\xe0")  # 0x276ba3e0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_character_material_when_grabbed))

        data.write(b'\x9d\xc8\xe8\xd6')  # 0x9dc8e8d6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_damage_on_impact_with_character))

        data.write(b'y>{\xca')  # 0x793e7bca
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_damage_on_impact_with_held_character))

        data.write(b')\xe4\xba\xf8')  # 0x29e4baf8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_damage_on_impact_with_thrown_character))

        data.write(b'A\xee{\xa8')  # 0x41ee7ba8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.bounce_on_impact_with_held_character))

        data.write(b'\xaau%\x11')  # 0xaa752511
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_drop_on_impact_with_held_character))

        data.write(b'\x9d\x8a\x7ff')  # 0x9d8a7f66
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_held_character))

        data.write(b',;i\xb0')  # 0x2c3b69b0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_thrown_character))

        data.write(b'\x12/\xc9\xcc')  # 0x122fc9cc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_player))

        data.write(b'@\x90\x8e\xb7')  # 0x40908eb7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_when_dropped))

        data.write(b'\x1b\xb0\xd6\xf0')  # 0x1bb0d6f0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_actor_when_held))

        data.write(b'\xdb\xb8\n\xcf')  # 0xdbb80acf
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.explode_on_impact_with_character_when_held))

        data.write(b'G\x9a\x01\xf5')  # 0x479a01f5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.apply_damage_on_impact_with_player))

        data.write(b'\xceN8C')  # 0xce4e3843
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_collision_actors_on_throw))

        data.write(b'\xc4\xd3\xdc\xac')  # 0xc4d3dcac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_explode_on_stopped_moving))

        data.write(b'\xb6\xcb\xab1')  # 0xb6cbab31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_explode_on_impact_with_player))

        data.write(b'Q\xca\t<')  # 0x51ca093c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.explode_time_after_throw))

        data.write(b'\x89\xae\xc3N')  # 0x89aec34e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.flash_on_explode_timer))

        data.write(b'cQ#\xe5')  # 0x635123e5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_flash_on_enter_force_trigger))

        data.write(b'7w\x13`')  # 0x37771360
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_flashing_time))

        data.write(b"'\x11-%")  # 0x27112d25
        data.write(b'\x00\x10')  # size
        self.flash_color.to_stream(data)

        data.write(b'\xd3/\xce\xdd')  # 0xd32fcedd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.flash_incandescence))

        data.write(b'd\xb2?\xb3')  # 0x64b23fb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_flash_period))

        data.write(b'\x87\x01/\x0f')  # 0x87012f0f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.final_flash_period))

        data.write(b'V\x01\xc4\xfd')  # 0x5601c4fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.accelerate_flash_duration))

        data.write(b'\xbf\x04\x87@')  # 0xbf048740
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_indestructible))

        data.write(b'\xec\x12\xed\xd7')  # 0xec12edd7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_immovable))

        data.write(b'\x1ap\xd4\xa5')  # 0x1a70d4a5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.lock_to_player_path_when_thrown))

        data.write(b'\xc6\xbf\x0f\xc0')  # 0xc6bf0fc0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_player_walkthrough))

        data.write(b'\xef\xa0bN')  # 0xefa0624e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_ai_walkthrough))

        data.write(b'\x05\xcf\t\x93')  # 0x5cf0993
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance_from_spline))

        data.write(b'\xc3K\x1c\xfc')  # 0xc34b1cfc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_explode_off_screen))

        data.write(b'B\n\xa8\xb1')  # 0x420aa8b1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_timer_when_partially_offscreen))

        data.write(b'\x12\xd1\xf8s')  # 0x12d1f873
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_time_off_screen))

        data.write(b'5\x03*\xb6')  # 0x35032ab6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_impact_damp))

        data.write(b'\x88F\x14B')  # 0x88461442
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wall_impact_damp))

        data.write(b'\xf4\xa3\xe2\x1e')  # 0xf4a3e21e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.carried_object_impact_damp))

        data.write(b'"%m|')  # 0x22256d7c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_friction))

        data.write(b'L\\\x17\xec')  # 0x4c5c17ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_downward_velocity_to_bounce))

        data.write(b'\x00+\xa5m')  # 0x2ba56d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_factor))

        data.write(b'\x06\xb38T')  # 0x6b33854
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_vertical_bounce_speed))

        data.write(b'.4\xd4\xa6')  # 0x2e34d4a6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.heal_players_on_explosion))

        data.write(b'\xa9\x9bMl')  # 0xa99b4d6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flying_effect_speed))

        data.write(b'x~\xa8\xb1')  # 0x787ea8b1
        data.write(b'\x00\x0c')  # size
        self.flying_effect_target_scale.to_stream(data)

        data.write(b'\xada\xc2:')  # 0xad61c23a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flying_health_effect))

        data.write(b'\x99e\xb4\x81')  # 0x9965b481
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.explosion_health_effect))

        data.write(b'8\x9c;\xd6')  # 0x389c3bd6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.health_sound_effect))

        data.write(b'\x17\x91\x85\x04')  # 0x17918504
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.roll_through_effect))

        data.write(b'l\xf5\x91Z')  # 0x6cf5915a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.roll_through_sound_effect))

        data.write(b'W\x18N\xe6')  # 0x57184ee6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hit_by_thrown_object_sound))

        data.write(b'\xb5\x8bQN')  # 0xb58b514e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flash_sound))

        data.write(b'\x96\xc0c\xe5')  # 0x96c063e5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flash_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\nF\xc6')  # 0xbf0a46c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flash_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\x88\xa0B')  # 0xf688a042
        data.write(b'\x00\x0c')  # size
        self.dk_optional_throw_velocity.to_stream(data)

        data.write(b'a\x84\x8d\xd1')  # 0x61848dd1
        data.write(b'\x00\x0c')  # size
        self.diddy_optional_throw_velocity.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            is_barrel=data['is_barrel'],
            grabbable_at_creation=data['grabbable_at_creation'],
            grabbable_when_settled=data['grabbable_when_settled'],
            mark_grabbable_immediately_on_settle=data['mark_grabbable_immediately_on_settle'],
            set_as_thrown_at_creation=data['set_as_thrown_at_creation'],
            spawn_other_player_on_explosion=data['spawn_other_player_on_explosion'],
            explode_on_impact_with_floor=data['explode_on_impact_with_floor'],
            explode_on_impact_with_wall=data['explode_on_impact_with_wall'],
            explode_on_impact_with_actor=data['explode_on_impact_with_actor'],
            explode_on_impact_with_bouncy=data['explode_on_impact_with_bouncy'],
            explode_on_impact_with_character=data['explode_on_impact_with_character'],
            disable_character_material_when_grabbed=data['disable_character_material_when_grabbed'],
            apply_damage_on_impact_with_character=data['apply_damage_on_impact_with_character'],
            apply_damage_on_impact_with_held_character=data['apply_damage_on_impact_with_held_character'],
            apply_damage_on_impact_with_thrown_character=data['apply_damage_on_impact_with_thrown_character'],
            bounce_on_impact_with_held_character=data['bounce_on_impact_with_held_character'],
            force_drop_on_impact_with_held_character=data['force_drop_on_impact_with_held_character'],
            explode_on_impact_with_held_character=data['explode_on_impact_with_held_character'],
            explode_on_impact_with_thrown_character=data['explode_on_impact_with_thrown_character'],
            explode_on_impact_with_player=data['explode_on_impact_with_player'],
            explode_on_impact_when_dropped=data['explode_on_impact_when_dropped'],
            explode_on_impact_with_actor_when_held=data['explode_on_impact_with_actor_when_held'],
            explode_on_impact_with_character_when_held=data['explode_on_impact_with_character_when_held'],
            apply_damage_on_impact_with_player=data['apply_damage_on_impact_with_player'],
            disable_collision_actors_on_throw=data['disable_collision_actors_on_throw'],
            delay_explode_on_stopped_moving=data['delay_explode_on_stopped_moving'],
            delay_explode_on_impact_with_player=data['delay_explode_on_impact_with_player'],
            explode_time_after_throw=data['explode_time_after_throw'],
            flash_on_explode_timer=data['flash_on_explode_timer'],
            start_flash_on_enter_force_trigger=data['start_flash_on_enter_force_trigger'],
            start_flashing_time=data['start_flashing_time'],
            flash_color=Color.from_json(data['flash_color']),
            flash_incandescence=data['flash_incandescence'],
            initial_flash_period=data['initial_flash_period'],
            final_flash_period=data['final_flash_period'],
            accelerate_flash_duration=data['accelerate_flash_duration'],
            is_indestructible=data['is_indestructible'],
            is_immovable=data['is_immovable'],
            lock_to_player_path_when_thrown=data['lock_to_player_path_when_thrown'],
            allow_player_walkthrough=data['allow_player_walkthrough'],
            allow_ai_walkthrough=data['allow_ai_walkthrough'],
            distance_from_spline=data['distance_from_spline'],
            can_explode_off_screen=data['can_explode_off_screen'],
            start_timer_when_partially_offscreen=data['start_timer_when_partially_offscreen'],
            max_time_off_screen=data['max_time_off_screen'],
            ground_impact_damp=data['ground_impact_damp'],
            wall_impact_damp=data['wall_impact_damp'],
            carried_object_impact_damp=data['carried_object_impact_damp'],
            ground_friction=data['ground_friction'],
            min_downward_velocity_to_bounce=data['min_downward_velocity_to_bounce'],
            bounce_factor=data['bounce_factor'],
            max_vertical_bounce_speed=data['max_vertical_bounce_speed'],
            heal_players_on_explosion=data['heal_players_on_explosion'],
            flying_effect_speed=data['flying_effect_speed'],
            flying_effect_target_scale=Vector.from_json(data['flying_effect_target_scale']),
            flying_health_effect=data['flying_health_effect'],
            explosion_health_effect=data['explosion_health_effect'],
            health_sound_effect=data['health_sound_effect'],
            roll_through_effect=data['roll_through_effect'],
            roll_through_sound_effect=data['roll_through_sound_effect'],
            hit_by_thrown_object_sound=data['hit_by_thrown_object_sound'],
            flash_sound=data['flash_sound'],
            flash_sound_pitch=Spline.from_json(data['flash_sound_pitch']),
            flash_sound_volume=Spline.from_json(data['flash_sound_volume']),
            dk_optional_throw_velocity=Vector.from_json(data['dk_optional_throw_velocity']),
            diddy_optional_throw_velocity=Vector.from_json(data['diddy_optional_throw_velocity']),
        )

    def to_json(self) -> dict:
        return {
            'is_barrel': self.is_barrel,
            'grabbable_at_creation': self.grabbable_at_creation,
            'grabbable_when_settled': self.grabbable_when_settled,
            'mark_grabbable_immediately_on_settle': self.mark_grabbable_immediately_on_settle,
            'set_as_thrown_at_creation': self.set_as_thrown_at_creation,
            'spawn_other_player_on_explosion': self.spawn_other_player_on_explosion,
            'explode_on_impact_with_floor': self.explode_on_impact_with_floor,
            'explode_on_impact_with_wall': self.explode_on_impact_with_wall,
            'explode_on_impact_with_actor': self.explode_on_impact_with_actor,
            'explode_on_impact_with_bouncy': self.explode_on_impact_with_bouncy,
            'explode_on_impact_with_character': self.explode_on_impact_with_character,
            'disable_character_material_when_grabbed': self.disable_character_material_when_grabbed,
            'apply_damage_on_impact_with_character': self.apply_damage_on_impact_with_character,
            'apply_damage_on_impact_with_held_character': self.apply_damage_on_impact_with_held_character,
            'apply_damage_on_impact_with_thrown_character': self.apply_damage_on_impact_with_thrown_character,
            'bounce_on_impact_with_held_character': self.bounce_on_impact_with_held_character,
            'force_drop_on_impact_with_held_character': self.force_drop_on_impact_with_held_character,
            'explode_on_impact_with_held_character': self.explode_on_impact_with_held_character,
            'explode_on_impact_with_thrown_character': self.explode_on_impact_with_thrown_character,
            'explode_on_impact_with_player': self.explode_on_impact_with_player,
            'explode_on_impact_when_dropped': self.explode_on_impact_when_dropped,
            'explode_on_impact_with_actor_when_held': self.explode_on_impact_with_actor_when_held,
            'explode_on_impact_with_character_when_held': self.explode_on_impact_with_character_when_held,
            'apply_damage_on_impact_with_player': self.apply_damage_on_impact_with_player,
            'disable_collision_actors_on_throw': self.disable_collision_actors_on_throw,
            'delay_explode_on_stopped_moving': self.delay_explode_on_stopped_moving,
            'delay_explode_on_impact_with_player': self.delay_explode_on_impact_with_player,
            'explode_time_after_throw': self.explode_time_after_throw,
            'flash_on_explode_timer': self.flash_on_explode_timer,
            'start_flash_on_enter_force_trigger': self.start_flash_on_enter_force_trigger,
            'start_flashing_time': self.start_flashing_time,
            'flash_color': self.flash_color.to_json(),
            'flash_incandescence': self.flash_incandescence,
            'initial_flash_period': self.initial_flash_period,
            'final_flash_period': self.final_flash_period,
            'accelerate_flash_duration': self.accelerate_flash_duration,
            'is_indestructible': self.is_indestructible,
            'is_immovable': self.is_immovable,
            'lock_to_player_path_when_thrown': self.lock_to_player_path_when_thrown,
            'allow_player_walkthrough': self.allow_player_walkthrough,
            'allow_ai_walkthrough': self.allow_ai_walkthrough,
            'distance_from_spline': self.distance_from_spline,
            'can_explode_off_screen': self.can_explode_off_screen,
            'start_timer_when_partially_offscreen': self.start_timer_when_partially_offscreen,
            'max_time_off_screen': self.max_time_off_screen,
            'ground_impact_damp': self.ground_impact_damp,
            'wall_impact_damp': self.wall_impact_damp,
            'carried_object_impact_damp': self.carried_object_impact_damp,
            'ground_friction': self.ground_friction,
            'min_downward_velocity_to_bounce': self.min_downward_velocity_to_bounce,
            'bounce_factor': self.bounce_factor,
            'max_vertical_bounce_speed': self.max_vertical_bounce_speed,
            'heal_players_on_explosion': self.heal_players_on_explosion,
            'flying_effect_speed': self.flying_effect_speed,
            'flying_effect_target_scale': self.flying_effect_target_scale.to_json(),
            'flying_health_effect': self.flying_health_effect,
            'explosion_health_effect': self.explosion_health_effect,
            'health_sound_effect': self.health_sound_effect,
            'roll_through_effect': self.roll_through_effect,
            'roll_through_sound_effect': self.roll_through_sound_effect,
            'hit_by_thrown_object_sound': self.hit_by_thrown_object_sound,
            'flash_sound': self.flash_sound,
            'flash_sound_pitch': self.flash_sound_pitch.to_json(),
            'flash_sound_volume': self.flash_sound_volume.to_json(),
            'dk_optional_throw_velocity': self.dk_optional_throw_velocity.to_json(),
            'diddy_optional_throw_velocity': self.diddy_optional_throw_velocity.to_json(),
        }


def _decode_is_barrel(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grabbable_at_creation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grabbable_when_settled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_mark_grabbable_immediately_on_settle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_set_as_thrown_at_creation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_spawn_other_player_on_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_floor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_wall(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_actor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_bouncy(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_character(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_character_material_when_grabbed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_apply_damage_on_impact_with_character(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_apply_damage_on_impact_with_held_character(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_apply_damage_on_impact_with_thrown_character(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_bounce_on_impact_with_held_character(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_force_drop_on_impact_with_held_character(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_held_character(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_thrown_character(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_when_dropped(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_actor_when_held(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_explode_on_impact_with_character_when_held(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_apply_damage_on_impact_with_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_collision_actors_on_throw(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_delay_explode_on_stopped_moving(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_explode_on_impact_with_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_explode_time_after_throw(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_on_explode_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_flash_on_enter_force_trigger(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_flashing_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flash_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_flash_incandescence(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_initial_flash_period(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_final_flash_period(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_accelerate_flash_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_indestructible(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_immovable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_lock_to_player_path_when_thrown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_player_walkthrough(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_ai_walkthrough(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_distance_from_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_can_explode_off_screen(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_timer_when_partially_offscreen(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_time_off_screen(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_impact_damp(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wall_impact_damp(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_carried_object_impact_damp(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_friction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_downward_velocity_to_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_factor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_vertical_bounce_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_heal_players_on_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_flying_effect_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flying_effect_target_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_flying_health_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_explosion_health_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_health_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_roll_through_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_roll_through_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_hit_by_thrown_object_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flash_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flash_sound_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_flash_sound_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_dk_optional_throw_velocity(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_diddy_optional_throw_velocity(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7acb78bd: ('is_barrel', _decode_is_barrel),
    0xdb0e5a51: ('grabbable_at_creation', _decode_grabbable_at_creation),
    0x4b4701dd: ('grabbable_when_settled', _decode_grabbable_when_settled),
    0xf87c63c6: ('mark_grabbable_immediately_on_settle', _decode_mark_grabbable_immediately_on_settle),
    0xd342bc69: ('set_as_thrown_at_creation', _decode_set_as_thrown_at_creation),
    0xd32d9fe3: ('spawn_other_player_on_explosion', _decode_spawn_other_player_on_explosion),
    0xd142e3f1: ('explode_on_impact_with_floor', _decode_explode_on_impact_with_floor),
    0x28becdb5: ('explode_on_impact_with_wall', _decode_explode_on_impact_with_wall),
    0x9da54a0: ('explode_on_impact_with_actor', _decode_explode_on_impact_with_actor),
    0xf3f8eb41: ('explode_on_impact_with_bouncy', _decode_explode_on_impact_with_bouncy),
    0xe5a2cd9: ('explode_on_impact_with_character', _decode_explode_on_impact_with_character),
    0x276ba3e0: ('disable_character_material_when_grabbed', _decode_disable_character_material_when_grabbed),
    0x9dc8e8d6: ('apply_damage_on_impact_with_character', _decode_apply_damage_on_impact_with_character),
    0x793e7bca: ('apply_damage_on_impact_with_held_character', _decode_apply_damage_on_impact_with_held_character),
    0x29e4baf8: ('apply_damage_on_impact_with_thrown_character', _decode_apply_damage_on_impact_with_thrown_character),
    0x41ee7ba8: ('bounce_on_impact_with_held_character', _decode_bounce_on_impact_with_held_character),
    0xaa752511: ('force_drop_on_impact_with_held_character', _decode_force_drop_on_impact_with_held_character),
    0x9d8a7f66: ('explode_on_impact_with_held_character', _decode_explode_on_impact_with_held_character),
    0x2c3b69b0: ('explode_on_impact_with_thrown_character', _decode_explode_on_impact_with_thrown_character),
    0x122fc9cc: ('explode_on_impact_with_player', _decode_explode_on_impact_with_player),
    0x40908eb7: ('explode_on_impact_when_dropped', _decode_explode_on_impact_when_dropped),
    0x1bb0d6f0: ('explode_on_impact_with_actor_when_held', _decode_explode_on_impact_with_actor_when_held),
    0xdbb80acf: ('explode_on_impact_with_character_when_held', _decode_explode_on_impact_with_character_when_held),
    0x479a01f5: ('apply_damage_on_impact_with_player', _decode_apply_damage_on_impact_with_player),
    0xce4e3843: ('disable_collision_actors_on_throw', _decode_disable_collision_actors_on_throw),
    0xc4d3dcac: ('delay_explode_on_stopped_moving', _decode_delay_explode_on_stopped_moving),
    0xb6cbab31: ('delay_explode_on_impact_with_player', _decode_delay_explode_on_impact_with_player),
    0x51ca093c: ('explode_time_after_throw', _decode_explode_time_after_throw),
    0x89aec34e: ('flash_on_explode_timer', _decode_flash_on_explode_timer),
    0x635123e5: ('start_flash_on_enter_force_trigger', _decode_start_flash_on_enter_force_trigger),
    0x37771360: ('start_flashing_time', _decode_start_flashing_time),
    0x27112d25: ('flash_color', _decode_flash_color),
    0xd32fcedd: ('flash_incandescence', _decode_flash_incandescence),
    0x64b23fb3: ('initial_flash_period', _decode_initial_flash_period),
    0x87012f0f: ('final_flash_period', _decode_final_flash_period),
    0x5601c4fd: ('accelerate_flash_duration', _decode_accelerate_flash_duration),
    0xbf048740: ('is_indestructible', _decode_is_indestructible),
    0xec12edd7: ('is_immovable', _decode_is_immovable),
    0x1a70d4a5: ('lock_to_player_path_when_thrown', _decode_lock_to_player_path_when_thrown),
    0xc6bf0fc0: ('allow_player_walkthrough', _decode_allow_player_walkthrough),
    0xefa0624e: ('allow_ai_walkthrough', _decode_allow_ai_walkthrough),
    0x5cf0993: ('distance_from_spline', _decode_distance_from_spline),
    0xc34b1cfc: ('can_explode_off_screen', _decode_can_explode_off_screen),
    0x420aa8b1: ('start_timer_when_partially_offscreen', _decode_start_timer_when_partially_offscreen),
    0x12d1f873: ('max_time_off_screen', _decode_max_time_off_screen),
    0x35032ab6: ('ground_impact_damp', _decode_ground_impact_damp),
    0x88461442: ('wall_impact_damp', _decode_wall_impact_damp),
    0xf4a3e21e: ('carried_object_impact_damp', _decode_carried_object_impact_damp),
    0x22256d7c: ('ground_friction', _decode_ground_friction),
    0x4c5c17ec: ('min_downward_velocity_to_bounce', _decode_min_downward_velocity_to_bounce),
    0x2ba56d: ('bounce_factor', _decode_bounce_factor),
    0x6b33854: ('max_vertical_bounce_speed', _decode_max_vertical_bounce_speed),
    0x2e34d4a6: ('heal_players_on_explosion', _decode_heal_players_on_explosion),
    0xa99b4d6c: ('flying_effect_speed', _decode_flying_effect_speed),
    0x787ea8b1: ('flying_effect_target_scale', _decode_flying_effect_target_scale),
    0xad61c23a: ('flying_health_effect', _decode_flying_health_effect),
    0x9965b481: ('explosion_health_effect', _decode_explosion_health_effect),
    0x389c3bd6: ('health_sound_effect', _decode_health_sound_effect),
    0x17918504: ('roll_through_effect', _decode_roll_through_effect),
    0x6cf5915a: ('roll_through_sound_effect', _decode_roll_through_sound_effect),
    0x57184ee6: ('hit_by_thrown_object_sound', _decode_hit_by_thrown_object_sound),
    0xb58b514e: ('flash_sound', _decode_flash_sound),
    0x96c063e5: ('flash_sound_pitch', _decode_flash_sound_pitch),
    0xbf0a46c6: ('flash_sound_volume', _decode_flash_sound_volume),
    0xf688a042: ('dk_optional_throw_velocity', _decode_dk_optional_throw_velocity),
    0x61848dd1: ('diddy_optional_throw_velocity', _decode_diddy_optional_throw_velocity),
}
