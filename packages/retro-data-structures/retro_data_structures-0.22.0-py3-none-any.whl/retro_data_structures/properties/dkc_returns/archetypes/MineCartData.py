# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.MineCartMaterialSounds import MineCartMaterialSounds
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class MineCartData(BaseProperty):
    collision_height_with_driver: float = dataclasses.field(default=2.0)
    wheel_diameter: float = dataclasses.field(default=0.699999988079071)
    airbourne_wheel_friction: float = dataclasses.field(default=1.2000000476837158)
    acceleration: float = dataclasses.field(default=20.0)
    deceleration: float = dataclasses.field(default=30.0)
    deceleration_to_minimum_speed: float = dataclasses.field(default=30.0)
    gravity_acceleration_multiplier: float = dataclasses.field(default=0.5)
    initial_speed: float = dataclasses.field(default=0.0)
    minimum_speed: float = dataclasses.field(default=14.0)
    maximum_speed: float = dataclasses.field(default=40.0)
    roll_forwards: bool = dataclasses.field(default=True)
    travel_at_minimum_speed: bool = dataclasses.field(default=False)
    maximum_speed_limit_enabled: bool = dataclasses.field(default=True)
    can_jump: bool = dataclasses.field(default=True)
    allow_platform_advancement: bool = dataclasses.field(default=True)
    allow_player_collision: bool = dataclasses.field(default=False)
    wait_for_all_players: bool = dataclasses.field(default=True)
    eligible_for_render_sorting: bool = dataclasses.field(default=True)
    jump_up_pitch: float = dataclasses.field(default=35.0)
    jump_down_pitch: float = dataclasses.field(default=35.0)
    minimum_jump_angle_up_slope: float = dataclasses.field(default=35.0)
    start_rolling: bool = dataclasses.field(default=False)
    initial_disable_controls_time: float = dataclasses.field(default=0.20000000298023224)
    pitch_acceleration_air: float = dataclasses.field(default=3.0)
    pitch_acceleration_ground: float = dataclasses.field(default=15.0)
    sound_enabled: bool = dataclasses.field(default=True)
    rolling_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    rolling_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound_pitch: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound_volume: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound2: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    rolling_sound2_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound2_pitch: Spline = dataclasses.field(default_factory=Spline)
    rolling_sound2_volume: Spline = dataclasses.field(default_factory=Spline)
    jump_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    land_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    num_material_sounds: int = dataclasses.field(default=0)
    material_sounds1: MineCartMaterialSounds = dataclasses.field(default_factory=MineCartMaterialSounds)
    material_sounds2: MineCartMaterialSounds = dataclasses.field(default_factory=MineCartMaterialSounds)
    material_sounds3: MineCartMaterialSounds = dataclasses.field(default_factory=MineCartMaterialSounds)
    material_sounds4: MineCartMaterialSounds = dataclasses.field(default_factory=MineCartMaterialSounds)
    material_sounds5: MineCartMaterialSounds = dataclasses.field(default_factory=MineCartMaterialSounds)
    material_sounds6: MineCartMaterialSounds = dataclasses.field(default_factory=MineCartMaterialSounds)
    maximum_land_sound_volume_speed: float = dataclasses.field(default=30.0)
    lean_back_vertical_speed_threshold: float = dataclasses.field(default=6.0)
    lean_forward_vertical_speed_threshold: float = dataclasses.field(default=-6.0)
    crash_velocity_damping: float = dataclasses.field(default=0.6600000262260437)
    vertical_crash_velocity: float = dataclasses.field(default=20.0)
    eol_speed: float = dataclasses.field(default=16.5)
    eol_hurl_distance: Vector = dataclasses.field(default_factory=lambda: Vector(x=15.0, y=0.0, z=6.0))
    sync_catch_time1: float = dataclasses.field(default=0.0)

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
        data.write(b'\x003')  # 51 properties

        data.write(b'[\xc9%\x1c')  # 0x5bc9251c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.collision_height_with_driver))

        data.write(b'?\x19\xed\xde')  # 0x3f19edde
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.wheel_diameter))

        data.write(b'\xfe\xe1W\xd3')  # 0xfee157d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.airbourne_wheel_friction))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'\x0cZ\x9c\xca')  # 0xc5a9cca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration_to_minimum_speed))

        data.write(b'fj\xbe\x89')  # 0x666abe89
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_acceleration_multiplier))

        data.write(b'\xcb\x14\xd9|')  # 0xcb14d97c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_speed))

        data.write(b'\x01\x85&>')  # 0x185263e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_speed))

        data.write(b'\x14\x0e\xf2\xcc')  # 0x140ef2cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed))

        data.write(b'<\x02v\xdf')  # 0x3c0276df
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.roll_forwards))

        data.write(b'\x7fc\x98\x8a')  # 0x7f63988a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.travel_at_minimum_speed))

        data.write(b'Y\xe0]~')  # 0x59e05d7e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.maximum_speed_limit_enabled))

        data.write(b'N&0\xe9')  # 0x4e2630e9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_jump))

        data.write(b'\xe5w\xb6\x1b')  # 0xe577b61b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_platform_advancement))

        data.write(b'\xdf\xdaS\x00')  # 0xdfda5300
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_player_collision))

        data.write(b'\xcd`\xf1\x8d')  # 0xcd60f18d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.wait_for_all_players))

        data.write(b'\x91\xff\xef\xed')  # 0x91ffefed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.eligible_for_render_sorting))

        data.write(b'\x17\xcb<X')  # 0x17cb3c58
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_up_pitch))

        data.write(b'\x85\xf7L\x0e')  # 0x85f74c0e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_down_pitch))

        data.write(b'-dI:')  # 0x2d64493a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_jump_angle_up_slope))

        data.write(b'\xdc\xe9\xb3{')  # 0xdce9b37b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_rolling))

        data.write(b'\xae\xf4i\xe8')  # 0xaef469e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_disable_controls_time))

        data.write(b'jJ~F')  # 0x6a4a7e46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pitch_acceleration_air))

        data.write(b'y2\x0f\x08')  # 0x79320f08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pitch_acceleration_ground))

        data.write(b'\xe8Q!\xc7')  # 0xe85121c7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.sound_enabled))

        data.write(b'6\xb1\xad\xd6')  # 0x36b1add6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rolling_sound))

        data.write(b'\xef\xe4y\x8f')  # 0xefe4798f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x96\xd4\xf7\x8b')  # 0x96d4f78b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x00\x1e\r')  # 0x15001e0d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\xa61\x00')  # 0xe3a63100
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rolling_sound2))

        data.write(b';\x01l\xfa')  # 0x3b016cfa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00\xc9ZU')  # 0xc95a55
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b't\xfd\xfcs')  # 0x74fdfc73
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rolling_sound2_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb\xe6`\xaf')  # 0xebe660af
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.jump_sound))

        data.write(b'\x0e+\x82\xec')  # 0xe2b82ec
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.land_sound))

        data.write(b'\xd7\xc1\x91A')  # 0xd7c19141
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_material_sounds))

        data.write(b'\x8e\x1a\x08\xaf')  # 0x8e1a08af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sounds1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\xff1\x92')  # 0xf8ff3192
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sounds2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'c\x8c\xdbF')  # 0x638cdb46
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sounds3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x155C\xe8')  # 0x153543e8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sounds4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8eF\xa9<')  # 0x8e46a93c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sounds5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\xa3\x90\x01')  # 0xf8a39001
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_sounds6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'm\xbc\x05!')  # 0x6dbc0521
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_land_sound_volume_speed))

        data.write(b'c\xc4\x1bt')  # 0x63c41b74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lean_back_vertical_speed_threshold))

        data.write(b'\xfb\xce_\xea')  # 0xfbce5fea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lean_forward_vertical_speed_threshold))

        data.write(b'6\x84E\x0b')  # 0x3684450b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.crash_velocity_damping))

        data.write(b'4\xf4\x13\xe7')  # 0x34f413e7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_crash_velocity))

        data.write(b'\xb1k\xef\xab')  # 0xb16befab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.eol_speed))

        data.write(b'\rf\x9d\xb3')  # 0xd669db3
        data.write(b'\x00\x0c')  # size
        self.eol_hurl_distance.to_stream(data)

        data.write(b'\xdc\xf4g\xfa')  # 0xdcf467fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.sync_catch_time1))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            collision_height_with_driver=data['collision_height_with_driver'],
            wheel_diameter=data['wheel_diameter'],
            airbourne_wheel_friction=data['airbourne_wheel_friction'],
            acceleration=data['acceleration'],
            deceleration=data['deceleration'],
            deceleration_to_minimum_speed=data['deceleration_to_minimum_speed'],
            gravity_acceleration_multiplier=data['gravity_acceleration_multiplier'],
            initial_speed=data['initial_speed'],
            minimum_speed=data['minimum_speed'],
            maximum_speed=data['maximum_speed'],
            roll_forwards=data['roll_forwards'],
            travel_at_minimum_speed=data['travel_at_minimum_speed'],
            maximum_speed_limit_enabled=data['maximum_speed_limit_enabled'],
            can_jump=data['can_jump'],
            allow_platform_advancement=data['allow_platform_advancement'],
            allow_player_collision=data['allow_player_collision'],
            wait_for_all_players=data['wait_for_all_players'],
            eligible_for_render_sorting=data['eligible_for_render_sorting'],
            jump_up_pitch=data['jump_up_pitch'],
            jump_down_pitch=data['jump_down_pitch'],
            minimum_jump_angle_up_slope=data['minimum_jump_angle_up_slope'],
            start_rolling=data['start_rolling'],
            initial_disable_controls_time=data['initial_disable_controls_time'],
            pitch_acceleration_air=data['pitch_acceleration_air'],
            pitch_acceleration_ground=data['pitch_acceleration_ground'],
            sound_enabled=data['sound_enabled'],
            rolling_sound=data['rolling_sound'],
            rolling_sound_low_pass_filter=Spline.from_json(data['rolling_sound_low_pass_filter']),
            rolling_sound_pitch=Spline.from_json(data['rolling_sound_pitch']),
            rolling_sound_volume=Spline.from_json(data['rolling_sound_volume']),
            rolling_sound2=data['rolling_sound2'],
            rolling_sound2_low_pass_filter=Spline.from_json(data['rolling_sound2_low_pass_filter']),
            rolling_sound2_pitch=Spline.from_json(data['rolling_sound2_pitch']),
            rolling_sound2_volume=Spline.from_json(data['rolling_sound2_volume']),
            jump_sound=data['jump_sound'],
            land_sound=data['land_sound'],
            num_material_sounds=data['num_material_sounds'],
            material_sounds1=MineCartMaterialSounds.from_json(data['material_sounds1']),
            material_sounds2=MineCartMaterialSounds.from_json(data['material_sounds2']),
            material_sounds3=MineCartMaterialSounds.from_json(data['material_sounds3']),
            material_sounds4=MineCartMaterialSounds.from_json(data['material_sounds4']),
            material_sounds5=MineCartMaterialSounds.from_json(data['material_sounds5']),
            material_sounds6=MineCartMaterialSounds.from_json(data['material_sounds6']),
            maximum_land_sound_volume_speed=data['maximum_land_sound_volume_speed'],
            lean_back_vertical_speed_threshold=data['lean_back_vertical_speed_threshold'],
            lean_forward_vertical_speed_threshold=data['lean_forward_vertical_speed_threshold'],
            crash_velocity_damping=data['crash_velocity_damping'],
            vertical_crash_velocity=data['vertical_crash_velocity'],
            eol_speed=data['eol_speed'],
            eol_hurl_distance=Vector.from_json(data['eol_hurl_distance']),
            sync_catch_time1=data['sync_catch_time1'],
        )

    def to_json(self) -> dict:
        return {
            'collision_height_with_driver': self.collision_height_with_driver,
            'wheel_diameter': self.wheel_diameter,
            'airbourne_wheel_friction': self.airbourne_wheel_friction,
            'acceleration': self.acceleration,
            'deceleration': self.deceleration,
            'deceleration_to_minimum_speed': self.deceleration_to_minimum_speed,
            'gravity_acceleration_multiplier': self.gravity_acceleration_multiplier,
            'initial_speed': self.initial_speed,
            'minimum_speed': self.minimum_speed,
            'maximum_speed': self.maximum_speed,
            'roll_forwards': self.roll_forwards,
            'travel_at_minimum_speed': self.travel_at_minimum_speed,
            'maximum_speed_limit_enabled': self.maximum_speed_limit_enabled,
            'can_jump': self.can_jump,
            'allow_platform_advancement': self.allow_platform_advancement,
            'allow_player_collision': self.allow_player_collision,
            'wait_for_all_players': self.wait_for_all_players,
            'eligible_for_render_sorting': self.eligible_for_render_sorting,
            'jump_up_pitch': self.jump_up_pitch,
            'jump_down_pitch': self.jump_down_pitch,
            'minimum_jump_angle_up_slope': self.minimum_jump_angle_up_slope,
            'start_rolling': self.start_rolling,
            'initial_disable_controls_time': self.initial_disable_controls_time,
            'pitch_acceleration_air': self.pitch_acceleration_air,
            'pitch_acceleration_ground': self.pitch_acceleration_ground,
            'sound_enabled': self.sound_enabled,
            'rolling_sound': self.rolling_sound,
            'rolling_sound_low_pass_filter': self.rolling_sound_low_pass_filter.to_json(),
            'rolling_sound_pitch': self.rolling_sound_pitch.to_json(),
            'rolling_sound_volume': self.rolling_sound_volume.to_json(),
            'rolling_sound2': self.rolling_sound2,
            'rolling_sound2_low_pass_filter': self.rolling_sound2_low_pass_filter.to_json(),
            'rolling_sound2_pitch': self.rolling_sound2_pitch.to_json(),
            'rolling_sound2_volume': self.rolling_sound2_volume.to_json(),
            'jump_sound': self.jump_sound,
            'land_sound': self.land_sound,
            'num_material_sounds': self.num_material_sounds,
            'material_sounds1': self.material_sounds1.to_json(),
            'material_sounds2': self.material_sounds2.to_json(),
            'material_sounds3': self.material_sounds3.to_json(),
            'material_sounds4': self.material_sounds4.to_json(),
            'material_sounds5': self.material_sounds5.to_json(),
            'material_sounds6': self.material_sounds6.to_json(),
            'maximum_land_sound_volume_speed': self.maximum_land_sound_volume_speed,
            'lean_back_vertical_speed_threshold': self.lean_back_vertical_speed_threshold,
            'lean_forward_vertical_speed_threshold': self.lean_forward_vertical_speed_threshold,
            'crash_velocity_damping': self.crash_velocity_damping,
            'vertical_crash_velocity': self.vertical_crash_velocity,
            'eol_speed': self.eol_speed,
            'eol_hurl_distance': self.eol_hurl_distance.to_json(),
            'sync_catch_time1': self.sync_catch_time1,
        }


def _decode_collision_height_with_driver(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wheel_diameter(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_airbourne_wheel_friction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration_to_minimum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity_acceleration_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_forwards(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_travel_at_minimum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_maximum_speed_limit_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_jump(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_platform_advancement(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_player_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_wait_for_all_players(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_eligible_for_render_sorting(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_jump_up_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_down_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_jump_angle_up_slope(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_rolling(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_initial_disable_controls_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pitch_acceleration_air(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pitch_acceleration_ground(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rolling_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rolling_sound_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rolling_sound2_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound2_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_rolling_sound2_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_jump_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_land_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_num_material_sounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_material_sounds1(data: typing.BinaryIO, property_size: int):
    return MineCartMaterialSounds.from_stream(data, property_size)


def _decode_material_sounds2(data: typing.BinaryIO, property_size: int):
    return MineCartMaterialSounds.from_stream(data, property_size)


def _decode_material_sounds3(data: typing.BinaryIO, property_size: int):
    return MineCartMaterialSounds.from_stream(data, property_size)


def _decode_material_sounds4(data: typing.BinaryIO, property_size: int):
    return MineCartMaterialSounds.from_stream(data, property_size)


def _decode_material_sounds5(data: typing.BinaryIO, property_size: int):
    return MineCartMaterialSounds.from_stream(data, property_size)


def _decode_material_sounds6(data: typing.BinaryIO, property_size: int):
    return MineCartMaterialSounds.from_stream(data, property_size)


def _decode_maximum_land_sound_volume_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lean_back_vertical_speed_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lean_forward_vertical_speed_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_crash_velocity_damping(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vertical_crash_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_eol_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_eol_hurl_distance(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_sync_catch_time1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5bc9251c: ('collision_height_with_driver', _decode_collision_height_with_driver),
    0x3f19edde: ('wheel_diameter', _decode_wheel_diameter),
    0xfee157d3: ('airbourne_wheel_friction', _decode_airbourne_wheel_friction),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0xc5a9cca: ('deceleration_to_minimum_speed', _decode_deceleration_to_minimum_speed),
    0x666abe89: ('gravity_acceleration_multiplier', _decode_gravity_acceleration_multiplier),
    0xcb14d97c: ('initial_speed', _decode_initial_speed),
    0x185263e: ('minimum_speed', _decode_minimum_speed),
    0x140ef2cc: ('maximum_speed', _decode_maximum_speed),
    0x3c0276df: ('roll_forwards', _decode_roll_forwards),
    0x7f63988a: ('travel_at_minimum_speed', _decode_travel_at_minimum_speed),
    0x59e05d7e: ('maximum_speed_limit_enabled', _decode_maximum_speed_limit_enabled),
    0x4e2630e9: ('can_jump', _decode_can_jump),
    0xe577b61b: ('allow_platform_advancement', _decode_allow_platform_advancement),
    0xdfda5300: ('allow_player_collision', _decode_allow_player_collision),
    0xcd60f18d: ('wait_for_all_players', _decode_wait_for_all_players),
    0x91ffefed: ('eligible_for_render_sorting', _decode_eligible_for_render_sorting),
    0x17cb3c58: ('jump_up_pitch', _decode_jump_up_pitch),
    0x85f74c0e: ('jump_down_pitch', _decode_jump_down_pitch),
    0x2d64493a: ('minimum_jump_angle_up_slope', _decode_minimum_jump_angle_up_slope),
    0xdce9b37b: ('start_rolling', _decode_start_rolling),
    0xaef469e8: ('initial_disable_controls_time', _decode_initial_disable_controls_time),
    0x6a4a7e46: ('pitch_acceleration_air', _decode_pitch_acceleration_air),
    0x79320f08: ('pitch_acceleration_ground', _decode_pitch_acceleration_ground),
    0xe85121c7: ('sound_enabled', _decode_sound_enabled),
    0x36b1add6: ('rolling_sound', _decode_rolling_sound),
    0xefe4798f: ('rolling_sound_low_pass_filter', _decode_rolling_sound_low_pass_filter),
    0x96d4f78b: ('rolling_sound_pitch', _decode_rolling_sound_pitch),
    0x15001e0d: ('rolling_sound_volume', _decode_rolling_sound_volume),
    0xe3a63100: ('rolling_sound2', _decode_rolling_sound2),
    0x3b016cfa: ('rolling_sound2_low_pass_filter', _decode_rolling_sound2_low_pass_filter),
    0xc95a55: ('rolling_sound2_pitch', _decode_rolling_sound2_pitch),
    0x74fdfc73: ('rolling_sound2_volume', _decode_rolling_sound2_volume),
    0xebe660af: ('jump_sound', _decode_jump_sound),
    0xe2b82ec: ('land_sound', _decode_land_sound),
    0xd7c19141: ('num_material_sounds', _decode_num_material_sounds),
    0x8e1a08af: ('material_sounds1', _decode_material_sounds1),
    0xf8ff3192: ('material_sounds2', _decode_material_sounds2),
    0x638cdb46: ('material_sounds3', _decode_material_sounds3),
    0x153543e8: ('material_sounds4', _decode_material_sounds4),
    0x8e46a93c: ('material_sounds5', _decode_material_sounds5),
    0xf8a39001: ('material_sounds6', _decode_material_sounds6),
    0x6dbc0521: ('maximum_land_sound_volume_speed', _decode_maximum_land_sound_volume_speed),
    0x63c41b74: ('lean_back_vertical_speed_threshold', _decode_lean_back_vertical_speed_threshold),
    0xfbce5fea: ('lean_forward_vertical_speed_threshold', _decode_lean_forward_vertical_speed_threshold),
    0x3684450b: ('crash_velocity_damping', _decode_crash_velocity_damping),
    0x34f413e7: ('vertical_crash_velocity', _decode_vertical_crash_velocity),
    0xb16befab: ('eol_speed', _decode_eol_speed),
    0xd669db3: ('eol_hurl_distance', _decode_eol_hurl_distance),
    0xdcf467fa: ('sync_catch_time1', _decode_sync_catch_time1),
}
