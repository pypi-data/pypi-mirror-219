# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class Camera(BaseProperty):
    ball_camera_angle_per_second: float = dataclasses.field(default=1200.0)
    ball_camera_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    ball_camera_min_speed_distance: float = dataclasses.field(default=6.0)
    ball_camera_max_speed_distance: float = dataclasses.field(default=5.0)
    ball_camera_backwards_distance: float = dataclasses.field(default=10.0)
    ball_camera_elevation: float = dataclasses.field(default=30.0)
    ball_camera_spring_constant: float = dataclasses.field(default=10.0)
    ball_camera_spring_max: float = dataclasses.field(default=0.009999999776482582)
    ball_camera_spring_tardis: float = dataclasses.field(default=1.0)
    ball_camera_centroid_spring_constant: float = dataclasses.field(default=80.0)
    ball_camera_centroid_spring_max: float = dataclasses.field(default=4.0)
    ball_camera_centroid_spring_tardis: float = dataclasses.field(default=1.0)
    ball_camera_centroid_distance_spring_constant: float = dataclasses.field(default=30.0)
    ball_camera_centroid_distance_spring_max: float = dataclasses.field(default=8.0)
    ball_camera_centroid_distance_spring_tardis: float = dataclasses.field(default=2.5)
    ball_camera_look_at_spring_constant: float = dataclasses.field(default=20.0)
    ball_camera_look_at_spring_max: float = dataclasses.field(default=10.0)
    ball_camera_look_at_spring_tardis: float = dataclasses.field(default=1.5)
    ball_camera_transition_time: float = dataclasses.field(default=0.75)
    ball_camera_free_look_speed: float = dataclasses.field(default=80.0)
    ball_camera_free_look_zoom_speed: float = dataclasses.field(default=10.0)
    ball_camera_free_look_min_distance: float = dataclasses.field(default=5.0)
    ball_camera_free_look_max_distance: float = dataclasses.field(default=6.0)
    ball_camera_free_look_max_vert_angle: float = dataclasses.field(default=89.0)
    unknown_0x144db504: float = dataclasses.field(default=3.0)
    unknown_0xee5bea64: float = dataclasses.field(default=25.0)
    ball_camera_chase_distance: float = dataclasses.field(default=4.0)
    ball_camera_chase_elevation: float = dataclasses.field(default=10.0)
    ball_camera_chase_yaw_speed: float = dataclasses.field(default=60.0)
    ball_camera_chase_dampen_angle: float = dataclasses.field(default=90.0)
    ball_camera_chase_angle_per_second: float = dataclasses.field(default=1200.0)
    ball_camera_chase_look_at_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    ball_camera_chase_spring_constant: float = dataclasses.field(default=20.0)
    ball_camera_chase_spring_max: float = dataclasses.field(default=5.0)
    ball_camera_chase_spring_tardis: float = dataclasses.field(default=5.5)
    ball_camera_boost_distance: float = dataclasses.field(default=4.0)
    ball_camera_boost_elevation: float = dataclasses.field(default=10.0)
    ball_camera_boost_yaw_speed: float = dataclasses.field(default=80.0)
    ball_camera_boost_dampen_angle: float = dataclasses.field(default=90.0)
    ball_camera_boost_angle_per_second: float = dataclasses.field(default=2400.0)
    ball_camera_boost_look_at_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    ball_camera_boost_spring_constant: float = dataclasses.field(default=20.0)
    ball_camera_boost_spring_max: float = dataclasses.field(default=5.0)
    ball_camera_boost_spring_tardis: float = dataclasses.field(default=5.5)
    ball_camera_control_distance: float = dataclasses.field(default=3.0)
    ball_camera_look_at_min_height: float = dataclasses.field(default=4.0)
    unknown_0x50f77df0: float = dataclasses.field(default=0.4000000059604645)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00/')  # 47 properties

        data.write(b'\x8a\xe4\t\xfc')  # 0x8ae409fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_angle_per_second))

        data.write(b'\xc7\xbf0|')  # 0xc7bf307c
        data.write(b'\x00\x0c')  # size
        self.ball_camera_offset.to_stream(data)

        data.write(b'\xf8\x82\x97\xb3')  # 0xf88297b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_min_speed_distance))

        data.write(b'\xeb\xc7q\x18')  # 0xebc77118
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_max_speed_distance))

        data.write(b'\x0fR\x07L')  # 0xf52074c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_backwards_distance))

        data.write(b'1\xff\x1a1')  # 0x31ff1a31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_elevation))

        data.write(b'\xc5J*d')  # 0xc54a2a64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_spring_constant))

        data.write(b'Xv\x95\xfa')  # 0x587695fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_spring_max))

        data.write(b'f\x17\x06\\')  # 0x6617065c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_spring_tardis))

        data.write(b'\xda0\x10\xaf')  # 0xda3010af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_centroid_spring_constant))

        data.write(b'\xd2\xe2g\xa2')  # 0xd2e267a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_centroid_spring_max))

        data.write(b'\xd5P\xad\xbc')  # 0xd550adbc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_centroid_spring_tardis))

        data.write(b'\xfaJ\xe4\x12')  # 0xfa4ae412
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_centroid_distance_spring_constant))

        data.write(b'\xd0\xef\xed\xbf')  # 0xd0efedbf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_centroid_distance_spring_max))

        data.write(b'~s\x91\xe1')  # 0x7e7391e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_centroid_distance_spring_tardis))

        data.write(b'j\xb0\x1e\x0b')  # 0x6ab01e0b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_look_at_spring_constant))

        data.write(b'\xf9\xfd\x14\xb7')  # 0xf9fd14b7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_look_at_spring_max))

        data.write(b'F\xa7\xeb\xcc')  # 0x46a7ebcc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_look_at_spring_tardis))

        data.write(b'n\xfa\x81Y')  # 0x6efa8159
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_transition_time))

        data.write(b'\xaet\xc2/')  # 0xae74c22f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_free_look_speed))

        data.write(b'\xc0@\xd2;')  # 0xc040d23b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_free_look_zoom_speed))

        data.write(b'\x16\xa3V\x15')  # 0x16a35615
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_free_look_min_distance))

        data.write(b'GZ\xedH')  # 0x475aed48
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_free_look_max_distance))

        data.write(b'\x14\xdem9')  # 0x14de6d39
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_free_look_max_vert_angle))

        data.write(b'\x14M\xb5\x04')  # 0x144db504
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x144db504))

        data.write(b'\xee[\xead')  # 0xee5bea64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xee5bea64))

        data.write(b'\xf2\x0b\xa5$')  # 0xf20ba524
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_chase_distance))

        data.write(b'\xd5\xd3\x8c\xbc')  # 0xd5d38cbc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_chase_elevation))

        data.write(b'T)\xd2\xae')  # 0x5429d2ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_chase_yaw_speed))

        data.write(b'1\xbd%\x1e')  # 0x31bd251e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_chase_dampen_angle))

        data.write(b'P\xfcJ\xcb')  # 0x50fc4acb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_chase_angle_per_second))

        data.write(b'\xa8\xa8m\xe9')  # 0xa8a86de9
        data.write(b'\x00\x0c')  # size
        self.ball_camera_chase_look_at_offset.to_stream(data)

        data.write(b'\x1fRiS')  # 0x1f526953
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_chase_spring_constant))

        data.write(b'\xbcZ\x03w')  # 0xbc5a0377
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_chase_spring_max))

        data.write(b'\x9a9\xcf\x14')  # 0x9a39cf14
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_chase_spring_tardis))

        data.write(b'\xe6\xf4D?')  # 0xe6f4443f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_boost_distance))

        data.write(b'_\xa2\xba\xb1')  # 0x5fa2bab1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_boost_elevation))

        data.write(b'@\xd63\xb5')  # 0x40d633b5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_boost_yaw_speed))

        data.write(b'K\xa9D\xbb')  # 0x4ba944bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_boost_dampen_angle))

        data.write(b'\xe9s[\xa1')  # 0xe9735ba1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_boost_angle_per_second))

        data.write(b'Am\x0e\x9f')  # 0x416d0e9f
        data.write(b'\x00\x0c')  # size
        self.ball_camera_boost_look_at_offset.to_stream(data)

        data.write(b'\xa6\xddx9')  # 0xa6dd7839
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_boost_spring_constant))

        data.write(b'6+5z')  # 0x362b357a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_boost_spring_max))

        data.write(b'<\xff\x8c\x12')  # 0x3cff8c12
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_boost_spring_tardis))

        data.write(b'\xeeL\x1fK')  # 0xee4c1f4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_control_distance))

        data.write(b'\x93\x88\xfaP')  # 0x9388fa50
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_camera_look_at_min_height))

        data.write(b'P\xf7}\xf0')  # 0x50f77df0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x50f77df0))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ball_camera_angle_per_second=data['ball_camera_angle_per_second'],
            ball_camera_offset=Vector.from_json(data['ball_camera_offset']),
            ball_camera_min_speed_distance=data['ball_camera_min_speed_distance'],
            ball_camera_max_speed_distance=data['ball_camera_max_speed_distance'],
            ball_camera_backwards_distance=data['ball_camera_backwards_distance'],
            ball_camera_elevation=data['ball_camera_elevation'],
            ball_camera_spring_constant=data['ball_camera_spring_constant'],
            ball_camera_spring_max=data['ball_camera_spring_max'],
            ball_camera_spring_tardis=data['ball_camera_spring_tardis'],
            ball_camera_centroid_spring_constant=data['ball_camera_centroid_spring_constant'],
            ball_camera_centroid_spring_max=data['ball_camera_centroid_spring_max'],
            ball_camera_centroid_spring_tardis=data['ball_camera_centroid_spring_tardis'],
            ball_camera_centroid_distance_spring_constant=data['ball_camera_centroid_distance_spring_constant'],
            ball_camera_centroid_distance_spring_max=data['ball_camera_centroid_distance_spring_max'],
            ball_camera_centroid_distance_spring_tardis=data['ball_camera_centroid_distance_spring_tardis'],
            ball_camera_look_at_spring_constant=data['ball_camera_look_at_spring_constant'],
            ball_camera_look_at_spring_max=data['ball_camera_look_at_spring_max'],
            ball_camera_look_at_spring_tardis=data['ball_camera_look_at_spring_tardis'],
            ball_camera_transition_time=data['ball_camera_transition_time'],
            ball_camera_free_look_speed=data['ball_camera_free_look_speed'],
            ball_camera_free_look_zoom_speed=data['ball_camera_free_look_zoom_speed'],
            ball_camera_free_look_min_distance=data['ball_camera_free_look_min_distance'],
            ball_camera_free_look_max_distance=data['ball_camera_free_look_max_distance'],
            ball_camera_free_look_max_vert_angle=data['ball_camera_free_look_max_vert_angle'],
            unknown_0x144db504=data['unknown_0x144db504'],
            unknown_0xee5bea64=data['unknown_0xee5bea64'],
            ball_camera_chase_distance=data['ball_camera_chase_distance'],
            ball_camera_chase_elevation=data['ball_camera_chase_elevation'],
            ball_camera_chase_yaw_speed=data['ball_camera_chase_yaw_speed'],
            ball_camera_chase_dampen_angle=data['ball_camera_chase_dampen_angle'],
            ball_camera_chase_angle_per_second=data['ball_camera_chase_angle_per_second'],
            ball_camera_chase_look_at_offset=Vector.from_json(data['ball_camera_chase_look_at_offset']),
            ball_camera_chase_spring_constant=data['ball_camera_chase_spring_constant'],
            ball_camera_chase_spring_max=data['ball_camera_chase_spring_max'],
            ball_camera_chase_spring_tardis=data['ball_camera_chase_spring_tardis'],
            ball_camera_boost_distance=data['ball_camera_boost_distance'],
            ball_camera_boost_elevation=data['ball_camera_boost_elevation'],
            ball_camera_boost_yaw_speed=data['ball_camera_boost_yaw_speed'],
            ball_camera_boost_dampen_angle=data['ball_camera_boost_dampen_angle'],
            ball_camera_boost_angle_per_second=data['ball_camera_boost_angle_per_second'],
            ball_camera_boost_look_at_offset=Vector.from_json(data['ball_camera_boost_look_at_offset']),
            ball_camera_boost_spring_constant=data['ball_camera_boost_spring_constant'],
            ball_camera_boost_spring_max=data['ball_camera_boost_spring_max'],
            ball_camera_boost_spring_tardis=data['ball_camera_boost_spring_tardis'],
            ball_camera_control_distance=data['ball_camera_control_distance'],
            ball_camera_look_at_min_height=data['ball_camera_look_at_min_height'],
            unknown_0x50f77df0=data['unknown_0x50f77df0'],
        )

    def to_json(self) -> dict:
        return {
            'ball_camera_angle_per_second': self.ball_camera_angle_per_second,
            'ball_camera_offset': self.ball_camera_offset.to_json(),
            'ball_camera_min_speed_distance': self.ball_camera_min_speed_distance,
            'ball_camera_max_speed_distance': self.ball_camera_max_speed_distance,
            'ball_camera_backwards_distance': self.ball_camera_backwards_distance,
            'ball_camera_elevation': self.ball_camera_elevation,
            'ball_camera_spring_constant': self.ball_camera_spring_constant,
            'ball_camera_spring_max': self.ball_camera_spring_max,
            'ball_camera_spring_tardis': self.ball_camera_spring_tardis,
            'ball_camera_centroid_spring_constant': self.ball_camera_centroid_spring_constant,
            'ball_camera_centroid_spring_max': self.ball_camera_centroid_spring_max,
            'ball_camera_centroid_spring_tardis': self.ball_camera_centroid_spring_tardis,
            'ball_camera_centroid_distance_spring_constant': self.ball_camera_centroid_distance_spring_constant,
            'ball_camera_centroid_distance_spring_max': self.ball_camera_centroid_distance_spring_max,
            'ball_camera_centroid_distance_spring_tardis': self.ball_camera_centroid_distance_spring_tardis,
            'ball_camera_look_at_spring_constant': self.ball_camera_look_at_spring_constant,
            'ball_camera_look_at_spring_max': self.ball_camera_look_at_spring_max,
            'ball_camera_look_at_spring_tardis': self.ball_camera_look_at_spring_tardis,
            'ball_camera_transition_time': self.ball_camera_transition_time,
            'ball_camera_free_look_speed': self.ball_camera_free_look_speed,
            'ball_camera_free_look_zoom_speed': self.ball_camera_free_look_zoom_speed,
            'ball_camera_free_look_min_distance': self.ball_camera_free_look_min_distance,
            'ball_camera_free_look_max_distance': self.ball_camera_free_look_max_distance,
            'ball_camera_free_look_max_vert_angle': self.ball_camera_free_look_max_vert_angle,
            'unknown_0x144db504': self.unknown_0x144db504,
            'unknown_0xee5bea64': self.unknown_0xee5bea64,
            'ball_camera_chase_distance': self.ball_camera_chase_distance,
            'ball_camera_chase_elevation': self.ball_camera_chase_elevation,
            'ball_camera_chase_yaw_speed': self.ball_camera_chase_yaw_speed,
            'ball_camera_chase_dampen_angle': self.ball_camera_chase_dampen_angle,
            'ball_camera_chase_angle_per_second': self.ball_camera_chase_angle_per_second,
            'ball_camera_chase_look_at_offset': self.ball_camera_chase_look_at_offset.to_json(),
            'ball_camera_chase_spring_constant': self.ball_camera_chase_spring_constant,
            'ball_camera_chase_spring_max': self.ball_camera_chase_spring_max,
            'ball_camera_chase_spring_tardis': self.ball_camera_chase_spring_tardis,
            'ball_camera_boost_distance': self.ball_camera_boost_distance,
            'ball_camera_boost_elevation': self.ball_camera_boost_elevation,
            'ball_camera_boost_yaw_speed': self.ball_camera_boost_yaw_speed,
            'ball_camera_boost_dampen_angle': self.ball_camera_boost_dampen_angle,
            'ball_camera_boost_angle_per_second': self.ball_camera_boost_angle_per_second,
            'ball_camera_boost_look_at_offset': self.ball_camera_boost_look_at_offset.to_json(),
            'ball_camera_boost_spring_constant': self.ball_camera_boost_spring_constant,
            'ball_camera_boost_spring_max': self.ball_camera_boost_spring_max,
            'ball_camera_boost_spring_tardis': self.ball_camera_boost_spring_tardis,
            'ball_camera_control_distance': self.ball_camera_control_distance,
            'ball_camera_look_at_min_height': self.ball_camera_look_at_min_height,
            'unknown_0x50f77df0': self.unknown_0x50f77df0,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_ball_camera_angle_per_second(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_ball_camera_min_speed_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_max_speed_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_backwards_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_spring_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_spring_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_spring_tardis(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_centroid_spring_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_centroid_spring_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_centroid_spring_tardis(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_centroid_distance_spring_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_centroid_distance_spring_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_centroid_distance_spring_tardis(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_look_at_spring_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_look_at_spring_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_look_at_spring_tardis(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_transition_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_free_look_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_free_look_zoom_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_free_look_min_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_free_look_max_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_free_look_max_vert_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x144db504(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xee5bea64(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_chase_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_chase_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_chase_yaw_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_chase_dampen_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_chase_angle_per_second(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_chase_look_at_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_ball_camera_chase_spring_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_chase_spring_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_chase_spring_tardis(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_boost_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_boost_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_boost_yaw_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_boost_dampen_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_boost_angle_per_second(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_boost_look_at_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_ball_camera_boost_spring_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_boost_spring_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_boost_spring_tardis(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_control_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_camera_look_at_min_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x50f77df0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8ae409fc: ('ball_camera_angle_per_second', _decode_ball_camera_angle_per_second),
    0xc7bf307c: ('ball_camera_offset', _decode_ball_camera_offset),
    0xf88297b3: ('ball_camera_min_speed_distance', _decode_ball_camera_min_speed_distance),
    0xebc77118: ('ball_camera_max_speed_distance', _decode_ball_camera_max_speed_distance),
    0xf52074c: ('ball_camera_backwards_distance', _decode_ball_camera_backwards_distance),
    0x31ff1a31: ('ball_camera_elevation', _decode_ball_camera_elevation),
    0xc54a2a64: ('ball_camera_spring_constant', _decode_ball_camera_spring_constant),
    0x587695fa: ('ball_camera_spring_max', _decode_ball_camera_spring_max),
    0x6617065c: ('ball_camera_spring_tardis', _decode_ball_camera_spring_tardis),
    0xda3010af: ('ball_camera_centroid_spring_constant', _decode_ball_camera_centroid_spring_constant),
    0xd2e267a2: ('ball_camera_centroid_spring_max', _decode_ball_camera_centroid_spring_max),
    0xd550adbc: ('ball_camera_centroid_spring_tardis', _decode_ball_camera_centroid_spring_tardis),
    0xfa4ae412: ('ball_camera_centroid_distance_spring_constant', _decode_ball_camera_centroid_distance_spring_constant),
    0xd0efedbf: ('ball_camera_centroid_distance_spring_max', _decode_ball_camera_centroid_distance_spring_max),
    0x7e7391e1: ('ball_camera_centroid_distance_spring_tardis', _decode_ball_camera_centroid_distance_spring_tardis),
    0x6ab01e0b: ('ball_camera_look_at_spring_constant', _decode_ball_camera_look_at_spring_constant),
    0xf9fd14b7: ('ball_camera_look_at_spring_max', _decode_ball_camera_look_at_spring_max),
    0x46a7ebcc: ('ball_camera_look_at_spring_tardis', _decode_ball_camera_look_at_spring_tardis),
    0x6efa8159: ('ball_camera_transition_time', _decode_ball_camera_transition_time),
    0xae74c22f: ('ball_camera_free_look_speed', _decode_ball_camera_free_look_speed),
    0xc040d23b: ('ball_camera_free_look_zoom_speed', _decode_ball_camera_free_look_zoom_speed),
    0x16a35615: ('ball_camera_free_look_min_distance', _decode_ball_camera_free_look_min_distance),
    0x475aed48: ('ball_camera_free_look_max_distance', _decode_ball_camera_free_look_max_distance),
    0x14de6d39: ('ball_camera_free_look_max_vert_angle', _decode_ball_camera_free_look_max_vert_angle),
    0x144db504: ('unknown_0x144db504', _decode_unknown_0x144db504),
    0xee5bea64: ('unknown_0xee5bea64', _decode_unknown_0xee5bea64),
    0xf20ba524: ('ball_camera_chase_distance', _decode_ball_camera_chase_distance),
    0xd5d38cbc: ('ball_camera_chase_elevation', _decode_ball_camera_chase_elevation),
    0x5429d2ae: ('ball_camera_chase_yaw_speed', _decode_ball_camera_chase_yaw_speed),
    0x31bd251e: ('ball_camera_chase_dampen_angle', _decode_ball_camera_chase_dampen_angle),
    0x50fc4acb: ('ball_camera_chase_angle_per_second', _decode_ball_camera_chase_angle_per_second),
    0xa8a86de9: ('ball_camera_chase_look_at_offset', _decode_ball_camera_chase_look_at_offset),
    0x1f526953: ('ball_camera_chase_spring_constant', _decode_ball_camera_chase_spring_constant),
    0xbc5a0377: ('ball_camera_chase_spring_max', _decode_ball_camera_chase_spring_max),
    0x9a39cf14: ('ball_camera_chase_spring_tardis', _decode_ball_camera_chase_spring_tardis),
    0xe6f4443f: ('ball_camera_boost_distance', _decode_ball_camera_boost_distance),
    0x5fa2bab1: ('ball_camera_boost_elevation', _decode_ball_camera_boost_elevation),
    0x40d633b5: ('ball_camera_boost_yaw_speed', _decode_ball_camera_boost_yaw_speed),
    0x4ba944bb: ('ball_camera_boost_dampen_angle', _decode_ball_camera_boost_dampen_angle),
    0xe9735ba1: ('ball_camera_boost_angle_per_second', _decode_ball_camera_boost_angle_per_second),
    0x416d0e9f: ('ball_camera_boost_look_at_offset', _decode_ball_camera_boost_look_at_offset),
    0xa6dd7839: ('ball_camera_boost_spring_constant', _decode_ball_camera_boost_spring_constant),
    0x362b357a: ('ball_camera_boost_spring_max', _decode_ball_camera_boost_spring_max),
    0x3cff8c12: ('ball_camera_boost_spring_tardis', _decode_ball_camera_boost_spring_tardis),
    0xee4c1f4b: ('ball_camera_control_distance', _decode_ball_camera_control_distance),
    0x9388fa50: ('ball_camera_look_at_min_height', _decode_ball_camera_look_at_min_height),
    0x50f77df0: ('unknown_0x50f77df0', _decode_unknown_0x50f77df0),
}
