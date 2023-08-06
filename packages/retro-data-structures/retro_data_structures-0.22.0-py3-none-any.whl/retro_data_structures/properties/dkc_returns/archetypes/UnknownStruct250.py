# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct250(BaseProperty):
    horizontal_acceleration: float = dataclasses.field(default=40.0)
    unknown_0xd8109ad6: float = dataclasses.field(default=16.0)
    initial_vertical_speed: float = dataclasses.field(default=14.0)
    initial_disable_controls_time: float = dataclasses.field(default=0.75)
    unknown_0xbc609c25: float = dataclasses.field(default=-25.0)
    unknown_0xa5fea1f2: float = dataclasses.field(default=50.0)
    unknown_0x7ae84b42: float = dataclasses.field(default=20.0)
    unknown_0xf9670ac1: float = dataclasses.field(default=5.0)
    unknown_0x76683dd3: float = dataclasses.field(default=16.0)
    unknown_0x21666d90: float = dataclasses.field(default=0.0)
    bounce_k: float = dataclasses.field(default=0.30000001192092896)
    unknown_0x0ef5b050: float = dataclasses.field(default=0.20000000298023224)
    neutral_pitch: float = dataclasses.field(default=-70.0)
    pitch_acceleration: float = dataclasses.field(default=5.0)
    pitch_limit: float = dataclasses.field(default=50.0)
    unknown_0xce155a8d: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x1952baf3: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x0fb70190: float = dataclasses.field(default=-16.0)
    engine_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    engine_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    engine_sound_pitch: Spline = dataclasses.field(default_factory=Spline)
    engine_sound_volume: Spline = dataclasses.field(default_factory=Spline)
    engine_sound2: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    engine_sound2_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    engine_sound2_pitch: Spline = dataclasses.field(default_factory=Spline)
    engine_sound2_volume: Spline = dataclasses.field(default_factory=Spline)
    crash_velocity_damping: float = dataclasses.field(default=0.6600000262260437)
    vertical_crash_velocity: float = dataclasses.field(default=20.0)
    unknown_0x6763516a: float = dataclasses.field(default=5.0)
    unknown_0x0755ff5c: float = dataclasses.field(default=1.0)
    unknown_0xaeaf14ad: float = dataclasses.field(default=18.0)
    unknown_0xfecde575: float = dataclasses.field(default=-90.0)
    exhaust_effect_scalar: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00!')  # 33 properties

        data.write(b'\x07Vz\x08')  # 0x7567a08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horizontal_acceleration))

        data.write(b'\xd8\x10\x9a\xd6')  # 0xd8109ad6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd8109ad6))

        data.write(b'cqC\xa3')  # 0x637143a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_vertical_speed))

        data.write(b'\xae\xf4i\xe8')  # 0xaef469e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_disable_controls_time))

        data.write(b'\xbc`\x9c%')  # 0xbc609c25
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbc609c25))

        data.write(b'\xa5\xfe\xa1\xf2')  # 0xa5fea1f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa5fea1f2))

        data.write(b'z\xe8KB')  # 0x7ae84b42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7ae84b42))

        data.write(b'\xf9g\n\xc1')  # 0xf9670ac1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf9670ac1))

        data.write(b'vh=\xd3')  # 0x76683dd3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76683dd3))

        data.write(b'!fm\x90')  # 0x21666d90
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x21666d90))

        data.write(b'\xf2m\xf1\xd6')  # 0xf26df1d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bounce_k))

        data.write(b'\x0e\xf5\xb0P')  # 0xef5b050
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0ef5b050))

        data.write(b'\xacS*\x85')  # 0xac532a85
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.neutral_pitch))

        data.write(b'[\xeax\xca')  # 0x5bea78ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pitch_acceleration))

        data.write(b'\xf5\x1a=\x06')  # 0xf51a3d06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pitch_limit))

        data.write(b'\xce\x15Z\x8d')  # 0xce155a8d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xce155a8d))

        data.write(b'\x19R\xba\xf3')  # 0x1952baf3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1952baf3))

        data.write(b'\x0f\xb7\x01\x90')  # 0xfb70190
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0fb70190))

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

        data.write(b'6\x84E\x0b')  # 0x3684450b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.crash_velocity_damping))

        data.write(b'4\xf4\x13\xe7')  # 0x34f413e7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vertical_crash_velocity))

        data.write(b'gcQj')  # 0x6763516a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6763516a))

        data.write(b'\x07U\xff\\')  # 0x755ff5c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0755ff5c))

        data.write(b'\xae\xaf\x14\xad')  # 0xaeaf14ad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xaeaf14ad))

        data.write(b'\xfe\xcd\xe5u')  # 0xfecde575
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfecde575))

        data.write(b'"\xdf\x00\x96')  # 0x22df0096
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.exhaust_effect_scalar))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            horizontal_acceleration=data['horizontal_acceleration'],
            unknown_0xd8109ad6=data['unknown_0xd8109ad6'],
            initial_vertical_speed=data['initial_vertical_speed'],
            initial_disable_controls_time=data['initial_disable_controls_time'],
            unknown_0xbc609c25=data['unknown_0xbc609c25'],
            unknown_0xa5fea1f2=data['unknown_0xa5fea1f2'],
            unknown_0x7ae84b42=data['unknown_0x7ae84b42'],
            unknown_0xf9670ac1=data['unknown_0xf9670ac1'],
            unknown_0x76683dd3=data['unknown_0x76683dd3'],
            unknown_0x21666d90=data['unknown_0x21666d90'],
            bounce_k=data['bounce_k'],
            unknown_0x0ef5b050=data['unknown_0x0ef5b050'],
            neutral_pitch=data['neutral_pitch'],
            pitch_acceleration=data['pitch_acceleration'],
            pitch_limit=data['pitch_limit'],
            unknown_0xce155a8d=data['unknown_0xce155a8d'],
            unknown_0x1952baf3=data['unknown_0x1952baf3'],
            unknown_0x0fb70190=data['unknown_0x0fb70190'],
            engine_sound=data['engine_sound'],
            engine_sound_low_pass_filter=Spline.from_json(data['engine_sound_low_pass_filter']),
            engine_sound_pitch=Spline.from_json(data['engine_sound_pitch']),
            engine_sound_volume=Spline.from_json(data['engine_sound_volume']),
            engine_sound2=data['engine_sound2'],
            engine_sound2_low_pass_filter=Spline.from_json(data['engine_sound2_low_pass_filter']),
            engine_sound2_pitch=Spline.from_json(data['engine_sound2_pitch']),
            engine_sound2_volume=Spline.from_json(data['engine_sound2_volume']),
            crash_velocity_damping=data['crash_velocity_damping'],
            vertical_crash_velocity=data['vertical_crash_velocity'],
            unknown_0x6763516a=data['unknown_0x6763516a'],
            unknown_0x0755ff5c=data['unknown_0x0755ff5c'],
            unknown_0xaeaf14ad=data['unknown_0xaeaf14ad'],
            unknown_0xfecde575=data['unknown_0xfecde575'],
            exhaust_effect_scalar=data['exhaust_effect_scalar'],
        )

    def to_json(self) -> dict:
        return {
            'horizontal_acceleration': self.horizontal_acceleration,
            'unknown_0xd8109ad6': self.unknown_0xd8109ad6,
            'initial_vertical_speed': self.initial_vertical_speed,
            'initial_disable_controls_time': self.initial_disable_controls_time,
            'unknown_0xbc609c25': self.unknown_0xbc609c25,
            'unknown_0xa5fea1f2': self.unknown_0xa5fea1f2,
            'unknown_0x7ae84b42': self.unknown_0x7ae84b42,
            'unknown_0xf9670ac1': self.unknown_0xf9670ac1,
            'unknown_0x76683dd3': self.unknown_0x76683dd3,
            'unknown_0x21666d90': self.unknown_0x21666d90,
            'bounce_k': self.bounce_k,
            'unknown_0x0ef5b050': self.unknown_0x0ef5b050,
            'neutral_pitch': self.neutral_pitch,
            'pitch_acceleration': self.pitch_acceleration,
            'pitch_limit': self.pitch_limit,
            'unknown_0xce155a8d': self.unknown_0xce155a8d,
            'unknown_0x1952baf3': self.unknown_0x1952baf3,
            'unknown_0x0fb70190': self.unknown_0x0fb70190,
            'engine_sound': self.engine_sound,
            'engine_sound_low_pass_filter': self.engine_sound_low_pass_filter.to_json(),
            'engine_sound_pitch': self.engine_sound_pitch.to_json(),
            'engine_sound_volume': self.engine_sound_volume.to_json(),
            'engine_sound2': self.engine_sound2,
            'engine_sound2_low_pass_filter': self.engine_sound2_low_pass_filter.to_json(),
            'engine_sound2_pitch': self.engine_sound2_pitch.to_json(),
            'engine_sound2_volume': self.engine_sound2_volume.to_json(),
            'crash_velocity_damping': self.crash_velocity_damping,
            'vertical_crash_velocity': self.vertical_crash_velocity,
            'unknown_0x6763516a': self.unknown_0x6763516a,
            'unknown_0x0755ff5c': self.unknown_0x0755ff5c,
            'unknown_0xaeaf14ad': self.unknown_0xaeaf14ad,
            'unknown_0xfecde575': self.unknown_0xfecde575,
            'exhaust_effect_scalar': self.exhaust_effect_scalar,
        }


def _decode_horizontal_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd8109ad6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_vertical_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_disable_controls_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbc609c25(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa5fea1f2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7ae84b42(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf9670ac1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76683dd3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x21666d90(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bounce_k(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0ef5b050(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_neutral_pitch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pitch_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pitch_limit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xce155a8d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1952baf3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0fb70190(data: typing.BinaryIO, property_size: int):
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


def _decode_crash_velocity_damping(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vertical_crash_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6763516a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0755ff5c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xaeaf14ad(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfecde575(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_exhaust_effect_scalar(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7567a08: ('horizontal_acceleration', _decode_horizontal_acceleration),
    0xd8109ad6: ('unknown_0xd8109ad6', _decode_unknown_0xd8109ad6),
    0x637143a3: ('initial_vertical_speed', _decode_initial_vertical_speed),
    0xaef469e8: ('initial_disable_controls_time', _decode_initial_disable_controls_time),
    0xbc609c25: ('unknown_0xbc609c25', _decode_unknown_0xbc609c25),
    0xa5fea1f2: ('unknown_0xa5fea1f2', _decode_unknown_0xa5fea1f2),
    0x7ae84b42: ('unknown_0x7ae84b42', _decode_unknown_0x7ae84b42),
    0xf9670ac1: ('unknown_0xf9670ac1', _decode_unknown_0xf9670ac1),
    0x76683dd3: ('unknown_0x76683dd3', _decode_unknown_0x76683dd3),
    0x21666d90: ('unknown_0x21666d90', _decode_unknown_0x21666d90),
    0xf26df1d6: ('bounce_k', _decode_bounce_k),
    0xef5b050: ('unknown_0x0ef5b050', _decode_unknown_0x0ef5b050),
    0xac532a85: ('neutral_pitch', _decode_neutral_pitch),
    0x5bea78ca: ('pitch_acceleration', _decode_pitch_acceleration),
    0xf51a3d06: ('pitch_limit', _decode_pitch_limit),
    0xce155a8d: ('unknown_0xce155a8d', _decode_unknown_0xce155a8d),
    0x1952baf3: ('unknown_0x1952baf3', _decode_unknown_0x1952baf3),
    0xfb70190: ('unknown_0x0fb70190', _decode_unknown_0x0fb70190),
    0xd190899c: ('engine_sound', _decode_engine_sound),
    0x82375435: ('engine_sound_low_pass_filter', _decode_engine_sound_low_pass_filter),
    0xb875593b: ('engine_sound_pitch', _decode_engine_sound_pitch),
    0xde4f0c2f: ('engine_sound_volume', _decode_engine_sound_volume),
    0x7548b8aa: ('engine_sound2', _decode_engine_sound2),
    0x10d8e545: ('engine_sound2_low_pass_filter', _decode_engine_sound2_low_pass_filter),
    0xcb864877: ('engine_sound2_pitch', _decode_engine_sound2_pitch),
    0xa156f285: ('engine_sound2_volume', _decode_engine_sound2_volume),
    0x3684450b: ('crash_velocity_damping', _decode_crash_velocity_damping),
    0x34f413e7: ('vertical_crash_velocity', _decode_vertical_crash_velocity),
    0x6763516a: ('unknown_0x6763516a', _decode_unknown_0x6763516a),
    0x755ff5c: ('unknown_0x0755ff5c', _decode_unknown_0x0755ff5c),
    0xaeaf14ad: ('unknown_0xaeaf14ad', _decode_unknown_0xaeaf14ad),
    0xfecde575: ('unknown_0xfecde575', _decode_unknown_0xfecde575),
    0x22df0096: ('exhaust_effect_scalar', _decode_exhaust_effect_scalar),
}
