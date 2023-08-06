# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct297(BaseProperty):
    lift_velocity: float = dataclasses.field(default=15.0)
    horizontal_acceleration: float = dataclasses.field(default=35.0)
    horizontal_deceleration: float = dataclasses.field(default=3.0)
    max_horizontal_velocity: float = dataclasses.field(default=12.5)
    boost_acceleration: float = dataclasses.field(default=20.0)
    max_boost_speed: float = dataclasses.field(default=15.0)
    boost_deceleration: float = dataclasses.field(default=20.0)
    max_boost_deceleration_speed: float = dataclasses.field(default=-9.0)
    initial_disable_controls_time: float = dataclasses.field(default=0.800000011920929)
    bounce_disable_controls_time: float = dataclasses.field(default=0.800000011920929)
    horizontal_padding: float = dataclasses.field(default=0.20000000298023224)
    bounce_k: float = dataclasses.field(default=0.800000011920929)
    screen_top_percentage: float = dataclasses.field(default=10.0)
    screen_top_kill_constant: float = dataclasses.field(default=0.949999988079071)
    maximum_lean_delta: float = dataclasses.field(default=360.0)
    maximum_lean_degrees: float = dataclasses.field(default=30.0)
    max_barrel_rotation: float = dataclasses.field(default=35.0)
    anim_input_rate: float = dataclasses.field(default=4.0)
    boost_anim_threshold: float = dataclasses.field(default=10.0)
    boost_into_acceleration: float = dataclasses.field(default=4.0)
    boost_out_of_acceleration: float = dataclasses.field(default=4.0)
    exhaust_effect_scalar: float = dataclasses.field(default=1.0)
    engine_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    engine_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    engine_sound_pitch: Spline = dataclasses.field(default_factory=Spline)
    engine_sound_volume: Spline = dataclasses.field(default_factory=Spline)
    engine_sound2: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    engine_sound2_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    engine_sound2_pitch: Spline = dataclasses.field(default_factory=Spline)
    engine_sound2_volume: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x1e')  # 30 properties

        data.write(b'{\x08\x82\x0f')  # 0x7b08820f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lift_velocity))

        data.write(b'\x07Vz\x08')  # 0x7567a08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_acceleration))

        data.write(b'\xa0i\xff`')  # 0xa069ff60
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_deceleration))

        data.write(b'\xd5k\x05\xf2')  # 0xd56b05f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_horizontal_velocity))

        data.write(b'\xd9\xdc\xd0\x88')  # 0xd9dcd088
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_acceleration))

        data.write(b'z\x8bd\xc8')  # 0x7a8b64c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_boost_speed))

        data.write(b'~\xe3U\xe0')  # 0x7ee355e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_deceleration))

        data.write(b'\x1a\xa3\xa4\x19')  # 0x1aa3a419
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_boost_deceleration_speed))

        data.write(b'\xae\xf4i\xe8')  # 0xaef469e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_disable_controls_time))

        data.write(b'G\xdf\xa4\x87')  # 0x47dfa487
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_disable_controls_time))

        data.write(b'\xbf/\x07\x9b')  # 0xbf2f079b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_padding))

        data.write(b'\xf2m\xf1\xd6')  # 0xf26df1d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_k))

        data.write(b'LVc9')  # 0x4c566339
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screen_top_percentage))

        data.write(b'\xce\x95.\x91')  # 0xce952e91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screen_top_kill_constant))

        data.write(b'\xa7w6=')  # 0xa777363d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_lean_delta))

        data.write(b'\xad\rE\xfa')  # 0xad0d45fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_lean_degrees))

        data.write(b'\xae\xe0\x8et')  # 0xaee08e74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_barrel_rotation))

        data.write(b'\xe5\xebci')  # 0xe5eb6369
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.anim_input_rate))

        data.write(b'\xb8\xf2=i')  # 0xb8f23d69
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_anim_threshold))

        data.write(b'c7\xd1\x94')  # 0x6337d194
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_into_acceleration))

        data.write(b'\x96#\xe4K')  # 0x9623e44b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_out_of_acceleration))

        data.write(b'"\xdf\x00\x96')  # 0x22df0096
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.exhaust_effect_scalar))

        data.write(b'\xd1\x90\x89\x9c')  # 0xd190899c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.engine_sound))

        data.write(b'\x827T5')  # 0x82375435
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.engine_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8uY;')  # 0xb875593b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.engine_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdeO\x0c/')  # 0xde4f0c2f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.engine_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'uH\xb8\xaa')  # 0x7548b8aa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.engine_sound2))

        data.write(b'\x10\xd8\xe5E')  # 0x10d8e545
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.engine_sound2_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcb\x86Hw')  # 0xcb864877
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.engine_sound2_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1V\xf2\x85')  # 0xa156f285
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.engine_sound2_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            lift_velocity=data['lift_velocity'],
            horizontal_acceleration=data['horizontal_acceleration'],
            horizontal_deceleration=data['horizontal_deceleration'],
            max_horizontal_velocity=data['max_horizontal_velocity'],
            boost_acceleration=data['boost_acceleration'],
            max_boost_speed=data['max_boost_speed'],
            boost_deceleration=data['boost_deceleration'],
            max_boost_deceleration_speed=data['max_boost_deceleration_speed'],
            initial_disable_controls_time=data['initial_disable_controls_time'],
            bounce_disable_controls_time=data['bounce_disable_controls_time'],
            horizontal_padding=data['horizontal_padding'],
            bounce_k=data['bounce_k'],
            screen_top_percentage=data['screen_top_percentage'],
            screen_top_kill_constant=data['screen_top_kill_constant'],
            maximum_lean_delta=data['maximum_lean_delta'],
            maximum_lean_degrees=data['maximum_lean_degrees'],
            max_barrel_rotation=data['max_barrel_rotation'],
            anim_input_rate=data['anim_input_rate'],
            boost_anim_threshold=data['boost_anim_threshold'],
            boost_into_acceleration=data['boost_into_acceleration'],
            boost_out_of_acceleration=data['boost_out_of_acceleration'],
            exhaust_effect_scalar=data['exhaust_effect_scalar'],
            engine_sound=data['engine_sound'],
            engine_sound_low_pass_filter=Spline.from_json(data['engine_sound_low_pass_filter']),
            engine_sound_pitch=Spline.from_json(data['engine_sound_pitch']),
            engine_sound_volume=Spline.from_json(data['engine_sound_volume']),
            engine_sound2=data['engine_sound2'],
            engine_sound2_low_pass_filter=Spline.from_json(data['engine_sound2_low_pass_filter']),
            engine_sound2_pitch=Spline.from_json(data['engine_sound2_pitch']),
            engine_sound2_volume=Spline.from_json(data['engine_sound2_volume']),
        )

    def to_json(self) -> dict:
        return {
            'lift_velocity': self.lift_velocity,
            'horizontal_acceleration': self.horizontal_acceleration,
            'horizontal_deceleration': self.horizontal_deceleration,
            'max_horizontal_velocity': self.max_horizontal_velocity,
            'boost_acceleration': self.boost_acceleration,
            'max_boost_speed': self.max_boost_speed,
            'boost_deceleration': self.boost_deceleration,
            'max_boost_deceleration_speed': self.max_boost_deceleration_speed,
            'initial_disable_controls_time': self.initial_disable_controls_time,
            'bounce_disable_controls_time': self.bounce_disable_controls_time,
            'horizontal_padding': self.horizontal_padding,
            'bounce_k': self.bounce_k,
            'screen_top_percentage': self.screen_top_percentage,
            'screen_top_kill_constant': self.screen_top_kill_constant,
            'maximum_lean_delta': self.maximum_lean_delta,
            'maximum_lean_degrees': self.maximum_lean_degrees,
            'max_barrel_rotation': self.max_barrel_rotation,
            'anim_input_rate': self.anim_input_rate,
            'boost_anim_threshold': self.boost_anim_threshold,
            'boost_into_acceleration': self.boost_into_acceleration,
            'boost_out_of_acceleration': self.boost_out_of_acceleration,
            'exhaust_effect_scalar': self.exhaust_effect_scalar,
            'engine_sound': self.engine_sound,
            'engine_sound_low_pass_filter': self.engine_sound_low_pass_filter.to_json(),
            'engine_sound_pitch': self.engine_sound_pitch.to_json(),
            'engine_sound_volume': self.engine_sound_volume.to_json(),
            'engine_sound2': self.engine_sound2,
            'engine_sound2_low_pass_filter': self.engine_sound2_low_pass_filter.to_json(),
            'engine_sound2_pitch': self.engine_sound2_pitch.to_json(),
            'engine_sound2_volume': self.engine_sound2_volume.to_json(),
        }


def _decode_lift_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horizontal_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horizontal_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_horizontal_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_boost_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_boost_deceleration_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_disable_controls_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_disable_controls_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horizontal_padding(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_k(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screen_top_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screen_top_kill_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_lean_delta(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_lean_degrees(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_barrel_rotation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_anim_input_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_anim_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_into_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_out_of_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_exhaust_effect_scalar(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_engine_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_engine_sound_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_engine_sound_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_engine_sound_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_engine_sound2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_engine_sound2_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_engine_sound2_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_engine_sound2_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7b08820f: ('lift_velocity', _decode_lift_velocity),
    0x7567a08: ('horizontal_acceleration', _decode_horizontal_acceleration),
    0xa069ff60: ('horizontal_deceleration', _decode_horizontal_deceleration),
    0xd56b05f2: ('max_horizontal_velocity', _decode_max_horizontal_velocity),
    0xd9dcd088: ('boost_acceleration', _decode_boost_acceleration),
    0x7a8b64c8: ('max_boost_speed', _decode_max_boost_speed),
    0x7ee355e0: ('boost_deceleration', _decode_boost_deceleration),
    0x1aa3a419: ('max_boost_deceleration_speed', _decode_max_boost_deceleration_speed),
    0xaef469e8: ('initial_disable_controls_time', _decode_initial_disable_controls_time),
    0x47dfa487: ('bounce_disable_controls_time', _decode_bounce_disable_controls_time),
    0xbf2f079b: ('horizontal_padding', _decode_horizontal_padding),
    0xf26df1d6: ('bounce_k', _decode_bounce_k),
    0x4c566339: ('screen_top_percentage', _decode_screen_top_percentage),
    0xce952e91: ('screen_top_kill_constant', _decode_screen_top_kill_constant),
    0xa777363d: ('maximum_lean_delta', _decode_maximum_lean_delta),
    0xad0d45fa: ('maximum_lean_degrees', _decode_maximum_lean_degrees),
    0xaee08e74: ('max_barrel_rotation', _decode_max_barrel_rotation),
    0xe5eb6369: ('anim_input_rate', _decode_anim_input_rate),
    0xb8f23d69: ('boost_anim_threshold', _decode_boost_anim_threshold),
    0x6337d194: ('boost_into_acceleration', _decode_boost_into_acceleration),
    0x9623e44b: ('boost_out_of_acceleration', _decode_boost_out_of_acceleration),
    0x22df0096: ('exhaust_effect_scalar', _decode_exhaust_effect_scalar),
    0xd190899c: ('engine_sound', _decode_engine_sound),
    0x82375435: ('engine_sound_low_pass_filter', _decode_engine_sound_low_pass_filter),
    0xb875593b: ('engine_sound_pitch', _decode_engine_sound_pitch),
    0xde4f0c2f: ('engine_sound_volume', _decode_engine_sound_volume),
    0x7548b8aa: ('engine_sound2', _decode_engine_sound2),
    0x10d8e545: ('engine_sound2_low_pass_filter', _decode_engine_sound2_low_pass_filter),
    0xcb864877: ('engine_sound2_pitch', _decode_engine_sound2_pitch),
    0xa156f285: ('engine_sound2_volume', _decode_engine_sound2_volume),
}
