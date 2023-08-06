# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.BouncyTireJumpHeights import BouncyTireJumpHeights
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class BouncyTireData(BaseProperty):
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    idle_animation: int = dataclasses.field(default=0)
    spring_animation: int = dataclasses.field(default=0)
    left_jiggle_animation: int = dataclasses.field(default=0)
    right_jiggle_animation: int = dataclasses.field(default=0)
    bounce_height: float = dataclasses.field(default=3.140199899673462)
    normal_jump_heights: BouncyTireJumpHeights = dataclasses.field(default_factory=BouncyTireJumpHeights)
    tar_inhibited_jump_heights: BouncyTireJumpHeights = dataclasses.field(default_factory=BouncyTireJumpHeights)
    high_jump_max_velocity_x: float = dataclasses.field(default=9.0)
    mass: float = dataclasses.field(default=80.0)
    rider_stop_speed_threshold: float = dataclasses.field(default=5.0)
    bounce_detection_angle: float = dataclasses.field(default=45.0)
    bounce_sound_effect: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    jump_sound_effect: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    collision_model: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    is_stationary: bool = dataclasses.field(default=True)
    should_cancel_players_momentum: bool = dataclasses.field(default=False)
    unknown_0x592fc47e: bool = dataclasses.field(default=False)
    should_absorb_shadows: bool = dataclasses.field(default=False)
    unknown_0x9d837da5: bool = dataclasses.field(default=True)
    air_control_disabled_duration_on_low_bounce: float = dataclasses.field(default=0.0)
    air_control_disabled_duration_on_high_bounce: float = dataclasses.field(default=0.0)
    air_control_scalar_on_high_bounce: float = dataclasses.field(default=2.0)
    air_control_scalar_on_low_bounce: float = dataclasses.field(default=2.0)

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
        data.write(b'\x00\x18')  # 24 properties

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\xa5\xb3\x8f')  # 0xa2a5b38f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.idle_animation))

        data.write(b'\rXJ\x11')  # 0xd584a11
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.spring_animation))

        data.write(b'\xcb\x191\xf5')  # 0xcb1931f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.left_jiggle_animation))

        data.write(b'db\x90z')  # 0x6462907a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.right_jiggle_animation))

        data.write(b'/RO\xd4')  # 0x2f524fd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_height))

        data.write(b'\x19(w7')  # 0x19287737
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_jump_heights.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'j:\xfc\x9e')  # 0x6a3afc9e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tar_inhibited_jump_heights.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x83\xa5):')  # 0x83a5293a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.high_jump_max_velocity_x))

        data.write(b'u\xdb\xb3u')  # 0x75dbb375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mass))

        data.write(b'OjT\x03')  # 0x4f6a5403
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rider_stop_speed_threshold))

        data.write(b'\xa8\xe4n\xa2')  # 0xa8e46ea2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_detection_angle))

        data.write(b'i\x15o\xbe')  # 0x69156fbe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_sound_effect))

        data.write(b'\xc0\t\x04\xc2')  # 0xc00904c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.jump_sound_effect))

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collision_model))

        data.write(b'\xab.V\xf4')  # 0xab2e56f4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_stationary))

        data.write(b't\x92\x0e\x0e')  # 0x74920e0e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.should_cancel_players_momentum))

        data.write(b'Y/\xc4~')  # 0x592fc47e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x592fc47e))

        data.write(b'\x82\xd1\x131')  # 0x82d11331
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.should_absorb_shadows))

        data.write(b'\x9d\x83}\xa5')  # 0x9d837da5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9d837da5))

        data.write(b'=\x04\xe5\x92')  # 0x3d04e592
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_control_disabled_duration_on_low_bounce))

        data.write(b'5\x95\xd9w')  # 0x3595d977
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_control_disabled_duration_on_high_bounce))

        data.write(b'\xd5P^\xa4')  # 0xd5505ea4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_control_scalar_on_high_bounce))

        data.write(b'-j(\x98')  # 0x2d6a2898
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_control_scalar_on_low_bounce))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            animation=AnimationParameters.from_json(data['animation']),
            idle_animation=data['idle_animation'],
            spring_animation=data['spring_animation'],
            left_jiggle_animation=data['left_jiggle_animation'],
            right_jiggle_animation=data['right_jiggle_animation'],
            bounce_height=data['bounce_height'],
            normal_jump_heights=BouncyTireJumpHeights.from_json(data['normal_jump_heights']),
            tar_inhibited_jump_heights=BouncyTireJumpHeights.from_json(data['tar_inhibited_jump_heights']),
            high_jump_max_velocity_x=data['high_jump_max_velocity_x'],
            mass=data['mass'],
            rider_stop_speed_threshold=data['rider_stop_speed_threshold'],
            bounce_detection_angle=data['bounce_detection_angle'],
            bounce_sound_effect=data['bounce_sound_effect'],
            jump_sound_effect=data['jump_sound_effect'],
            collision_model=data['collision_model'],
            is_stationary=data['is_stationary'],
            should_cancel_players_momentum=data['should_cancel_players_momentum'],
            unknown_0x592fc47e=data['unknown_0x592fc47e'],
            should_absorb_shadows=data['should_absorb_shadows'],
            unknown_0x9d837da5=data['unknown_0x9d837da5'],
            air_control_disabled_duration_on_low_bounce=data['air_control_disabled_duration_on_low_bounce'],
            air_control_disabled_duration_on_high_bounce=data['air_control_disabled_duration_on_high_bounce'],
            air_control_scalar_on_high_bounce=data['air_control_scalar_on_high_bounce'],
            air_control_scalar_on_low_bounce=data['air_control_scalar_on_low_bounce'],
        )

    def to_json(self) -> dict:
        return {
            'animation': self.animation.to_json(),
            'idle_animation': self.idle_animation,
            'spring_animation': self.spring_animation,
            'left_jiggle_animation': self.left_jiggle_animation,
            'right_jiggle_animation': self.right_jiggle_animation,
            'bounce_height': self.bounce_height,
            'normal_jump_heights': self.normal_jump_heights.to_json(),
            'tar_inhibited_jump_heights': self.tar_inhibited_jump_heights.to_json(),
            'high_jump_max_velocity_x': self.high_jump_max_velocity_x,
            'mass': self.mass,
            'rider_stop_speed_threshold': self.rider_stop_speed_threshold,
            'bounce_detection_angle': self.bounce_detection_angle,
            'bounce_sound_effect': self.bounce_sound_effect,
            'jump_sound_effect': self.jump_sound_effect,
            'collision_model': self.collision_model,
            'is_stationary': self.is_stationary,
            'should_cancel_players_momentum': self.should_cancel_players_momentum,
            'unknown_0x592fc47e': self.unknown_0x592fc47e,
            'should_absorb_shadows': self.should_absorb_shadows,
            'unknown_0x9d837da5': self.unknown_0x9d837da5,
            'air_control_disabled_duration_on_low_bounce': self.air_control_disabled_duration_on_low_bounce,
            'air_control_disabled_duration_on_high_bounce': self.air_control_disabled_duration_on_high_bounce,
            'air_control_scalar_on_high_bounce': self.air_control_scalar_on_high_bounce,
            'air_control_scalar_on_low_bounce': self.air_control_scalar_on_low_bounce,
        }


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_idle_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_spring_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_left_jiggle_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_right_jiggle_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_bounce_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_normal_jump_heights(data: typing.BinaryIO, property_size: int):
    return BouncyTireJumpHeights.from_stream(data, property_size)


def _decode_tar_inhibited_jump_heights(data: typing.BinaryIO, property_size: int):
    return BouncyTireJumpHeights.from_stream(data, property_size)


def _decode_high_jump_max_velocity_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rider_stop_speed_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_jump_sound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_is_stationary(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_should_cancel_players_momentum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x592fc47e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_should_absorb_shadows(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x9d837da5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_air_control_disabled_duration_on_low_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_air_control_disabled_duration_on_high_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_air_control_scalar_on_high_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_air_control_scalar_on_low_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa3d63f44: ('animation', _decode_animation),
    0xa2a5b38f: ('idle_animation', _decode_idle_animation),
    0xd584a11: ('spring_animation', _decode_spring_animation),
    0xcb1931f5: ('left_jiggle_animation', _decode_left_jiggle_animation),
    0x6462907a: ('right_jiggle_animation', _decode_right_jiggle_animation),
    0x2f524fd4: ('bounce_height', _decode_bounce_height),
    0x19287737: ('normal_jump_heights', _decode_normal_jump_heights),
    0x6a3afc9e: ('tar_inhibited_jump_heights', _decode_tar_inhibited_jump_heights),
    0x83a5293a: ('high_jump_max_velocity_x', _decode_high_jump_max_velocity_x),
    0x75dbb375: ('mass', _decode_mass),
    0x4f6a5403: ('rider_stop_speed_threshold', _decode_rider_stop_speed_threshold),
    0xa8e46ea2: ('bounce_detection_angle', _decode_bounce_detection_angle),
    0x69156fbe: ('bounce_sound_effect', _decode_bounce_sound_effect),
    0xc00904c2: ('jump_sound_effect', _decode_jump_sound_effect),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xab2e56f4: ('is_stationary', _decode_is_stationary),
    0x74920e0e: ('should_cancel_players_momentum', _decode_should_cancel_players_momentum),
    0x592fc47e: ('unknown_0x592fc47e', _decode_unknown_0x592fc47e),
    0x82d11331: ('should_absorb_shadows', _decode_should_absorb_shadows),
    0x9d837da5: ('unknown_0x9d837da5', _decode_unknown_0x9d837da5),
    0x3d04e592: ('air_control_disabled_duration_on_low_bounce', _decode_air_control_disabled_duration_on_low_bounce),
    0x3595d977: ('air_control_disabled_duration_on_high_bounce', _decode_air_control_disabled_duration_on_high_bounce),
    0xd5505ea4: ('air_control_scalar_on_high_bounce', _decode_air_control_scalar_on_high_bounce),
    0x2d6a2898: ('air_control_scalar_on_low_bounce', _decode_air_control_scalar_on_low_bounce),
}
