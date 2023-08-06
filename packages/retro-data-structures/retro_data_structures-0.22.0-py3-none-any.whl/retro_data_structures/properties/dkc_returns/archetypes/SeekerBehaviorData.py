# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class SeekerBehaviorData(BaseProperty):
    mode: int = dataclasses.field(default=3821732504)  # Choice
    seek_when_behavior_inactive: bool = dataclasses.field(default=False)
    attack_range_squared: float = dataclasses.field(default=0.0)
    speed: float = dataclasses.field(default=5.0)
    acceleration: float = dataclasses.field(default=1.0)
    deceleration: float = dataclasses.field(default=1.0)
    turn_speed_radians: float = dataclasses.field(default=0.0)
    hover_speed_threshold: float = dataclasses.field(default=0.30000001192092896)
    ignore_all_but_player: bool = dataclasses.field(default=True)
    ignore_all_during_death: bool = dataclasses.field(default=True)
    suicide_on_player_touch: bool = dataclasses.field(default=True)
    disable_collision_time_after_creation: float = dataclasses.field(default=0.0)
    life_time: float = dataclasses.field(default=120.0)
    max_distance_from_origin_squared: float = dataclasses.field(default=0.0)
    targeting_time: float = dataclasses.field(default=0.5)
    telegraph_time: float = dataclasses.field(default=0.25)
    pause_time: float = dataclasses.field(default=1.0)
    stop_distance_squared: float = dataclasses.field(default=0.0)
    stop_speed: float = dataclasses.field(default=0.0)
    flight_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    flight_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline)
    flight_sound_pitch: Spline = dataclasses.field(default_factory=Spline)
    flight_sound_volume: Spline = dataclasses.field(default_factory=Spline)
    maximum_speed_for_audio_inverse: float = dataclasses.field(default=0.0)
    flight_sound_deceleration_k: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x19')  # 25 properties

        data.write(b'\xb8\xf6\x0f\x9a')  # 0xb8f60f9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.mode))

        data.write(b'tZ\x8f\x03')  # 0x745a8f03
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.seek_when_behavior_inactive))

        data.write(b'\xde[\xfca')  # 0xde5bfc61
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_range_squared))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'X\x9av\xff')  # 0x589a76ff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed_radians))

        data.write(b'3+U\x18')  # 0x332b5518
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_speed_threshold))

        data.write(b'\xab\x0fQX')  # 0xab0f5158
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_all_but_player))

        data.write(b'\x88Is\xd2')  # 0x884973d2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_all_during_death))

        data.write(b'\xba\xc8\x0e\x1f')  # 0xbac80e1f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.suicide_on_player_touch))

        data.write(b'\xbe\xc9\x90\x05')  # 0xbec99005
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disable_collision_time_after_creation))

        data.write(b'\xb0-\xe5U')  # 0xb02de555
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.life_time))

        data.write(b'\t(X\x0f')  # 0x928580f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_distance_from_origin_squared))

        data.write(b'\xd9L9T')  # 0xd94c3954
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.targeting_time))

        data.write(b'\x8ek\xbe\xf1')  # 0x8e6bbef1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.telegraph_time))

        data.write(b'k\x08\xf2\xf2')  # 0x6b08f2f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pause_time))

        data.write(b'H\xb4Y\x11')  # 0x48b45911
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stop_distance_squared))

        data.write(b'\xd4`\x08!')  # 0xd4600821
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stop_speed))

        data.write(b'\xe1\xe6k$')  # 0xe1e66b24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flight_sound))

        data.write(b'\xb4\x13\xc4_')  # 0xb413c45f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xc7FL')  # 0x76c7464c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10\xe0Z\xaf')  # 0x10e05aaf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd\xa0\xb3\xf2')  # 0xbda0b3f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed_for_audio_inverse))

        data.write(b'z}\xf6\xe3')  # 0x7a7df6e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_sound_deceleration_k))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            mode=data['mode'],
            seek_when_behavior_inactive=data['seek_when_behavior_inactive'],
            attack_range_squared=data['attack_range_squared'],
            speed=data['speed'],
            acceleration=data['acceleration'],
            deceleration=data['deceleration'],
            turn_speed_radians=data['turn_speed_radians'],
            hover_speed_threshold=data['hover_speed_threshold'],
            ignore_all_but_player=data['ignore_all_but_player'],
            ignore_all_during_death=data['ignore_all_during_death'],
            suicide_on_player_touch=data['suicide_on_player_touch'],
            disable_collision_time_after_creation=data['disable_collision_time_after_creation'],
            life_time=data['life_time'],
            max_distance_from_origin_squared=data['max_distance_from_origin_squared'],
            targeting_time=data['targeting_time'],
            telegraph_time=data['telegraph_time'],
            pause_time=data['pause_time'],
            stop_distance_squared=data['stop_distance_squared'],
            stop_speed=data['stop_speed'],
            flight_sound=data['flight_sound'],
            flight_sound_low_pass_filter=Spline.from_json(data['flight_sound_low_pass_filter']),
            flight_sound_pitch=Spline.from_json(data['flight_sound_pitch']),
            flight_sound_volume=Spline.from_json(data['flight_sound_volume']),
            maximum_speed_for_audio_inverse=data['maximum_speed_for_audio_inverse'],
            flight_sound_deceleration_k=data['flight_sound_deceleration_k'],
        )

    def to_json(self) -> dict:
        return {
            'mode': self.mode,
            'seek_when_behavior_inactive': self.seek_when_behavior_inactive,
            'attack_range_squared': self.attack_range_squared,
            'speed': self.speed,
            'acceleration': self.acceleration,
            'deceleration': self.deceleration,
            'turn_speed_radians': self.turn_speed_radians,
            'hover_speed_threshold': self.hover_speed_threshold,
            'ignore_all_but_player': self.ignore_all_but_player,
            'ignore_all_during_death': self.ignore_all_during_death,
            'suicide_on_player_touch': self.suicide_on_player_touch,
            'disable_collision_time_after_creation': self.disable_collision_time_after_creation,
            'life_time': self.life_time,
            'max_distance_from_origin_squared': self.max_distance_from_origin_squared,
            'targeting_time': self.targeting_time,
            'telegraph_time': self.telegraph_time,
            'pause_time': self.pause_time,
            'stop_distance_squared': self.stop_distance_squared,
            'stop_speed': self.stop_speed,
            'flight_sound': self.flight_sound,
            'flight_sound_low_pass_filter': self.flight_sound_low_pass_filter.to_json(),
            'flight_sound_pitch': self.flight_sound_pitch.to_json(),
            'flight_sound_volume': self.flight_sound_volume.to_json(),
            'maximum_speed_for_audio_inverse': self.maximum_speed_for_audio_inverse,
            'flight_sound_deceleration_k': self.flight_sound_deceleration_k,
        }


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_seek_when_behavior_inactive(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_attack_range_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_turn_speed_radians(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hover_speed_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_all_but_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_all_during_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_suicide_on_player_touch(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_collision_time_after_creation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_life_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_distance_from_origin_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_targeting_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_telegraph_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pause_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stop_distance_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stop_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_flight_sound_low_pass_filter(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_flight_sound_pitch(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_flight_sound_volume(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_maximum_speed_for_audio_inverse(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_sound_deceleration_k(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb8f60f9a: ('mode', _decode_mode),
    0x745a8f03: ('seek_when_behavior_inactive', _decode_seek_when_behavior_inactive),
    0xde5bfc61: ('attack_range_squared', _decode_attack_range_squared),
    0x6392404e: ('speed', _decode_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0x589a76ff: ('turn_speed_radians', _decode_turn_speed_radians),
    0x332b5518: ('hover_speed_threshold', _decode_hover_speed_threshold),
    0xab0f5158: ('ignore_all_but_player', _decode_ignore_all_but_player),
    0x884973d2: ('ignore_all_during_death', _decode_ignore_all_during_death),
    0xbac80e1f: ('suicide_on_player_touch', _decode_suicide_on_player_touch),
    0xbec99005: ('disable_collision_time_after_creation', _decode_disable_collision_time_after_creation),
    0xb02de555: ('life_time', _decode_life_time),
    0x928580f: ('max_distance_from_origin_squared', _decode_max_distance_from_origin_squared),
    0xd94c3954: ('targeting_time', _decode_targeting_time),
    0x8e6bbef1: ('telegraph_time', _decode_telegraph_time),
    0x6b08f2f2: ('pause_time', _decode_pause_time),
    0x48b45911: ('stop_distance_squared', _decode_stop_distance_squared),
    0xd4600821: ('stop_speed', _decode_stop_speed),
    0xe1e66b24: ('flight_sound', _decode_flight_sound),
    0xb413c45f: ('flight_sound_low_pass_filter', _decode_flight_sound_low_pass_filter),
    0x76c7464c: ('flight_sound_pitch', _decode_flight_sound_pitch),
    0x10e05aaf: ('flight_sound_volume', _decode_flight_sound_volume),
    0xbda0b3f2: ('maximum_speed_for_audio_inverse', _decode_maximum_speed_for_audio_inverse),
    0x7a7df6e3: ('flight_sound_deceleration_k', _decode_flight_sound_deceleration_k),
}
