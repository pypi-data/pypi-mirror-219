# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType


@dataclasses.dataclass()
class TweakCameraBob(BaseObjectType):
    instance_name: str = dataclasses.field(default='')
    camera_bob_extent_x: float = dataclasses.field(default=0.07000000029802322)
    camera_bob_extent_y: float = dataclasses.field(default=0.14000000059604645)
    camera_bob_period: float = dataclasses.field(default=0.38999998569488525)
    unknown_0xa27bb5a7: float = dataclasses.field(default=0.7699999809265137)
    unknown_0xe3580b2b: float = dataclasses.field(default=0.800000011920929)
    slow_speed_period_scale: float = dataclasses.field(default=0.30000001192092896)
    target_magnitude_tracking_rate: float = dataclasses.field(default=0.10000000149011612)
    landing_bob_spring_constant: float = dataclasses.field(default=150.0)
    view_wander_radius: float = dataclasses.field(default=0.10000000149011612)
    view_wander_speed_min: float = dataclasses.field(default=0.10000000149011612)
    view_wander_speed_max: float = dataclasses.field(default=0.4000000059604645)
    view_wander_roll_variation: float = dataclasses.field(default=0.30000001192092896)
    gun_bob_magnitude: float = dataclasses.field(default=0.2199999988079071)
    helmet_bob_magnitude: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return None

    def set_name(self, name: str) -> None:
        raise RuntimeError(f"{self.__class__.__name__} does not have name")

    @classmethod
    def object_type(cls) -> str:
        return 'TWCB'

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\x7f\xda\x14f')  # 0x7fda1466
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.instance_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2\xa0\xb6\xf1')  # 0xe2a0b6f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_bob_extent_x))

        data.write(b')\xfceT')  # 0x29fc6554
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_bob_extent_y))

        data.write(b'\x14\x9ds9')  # 0x149d7339
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_bob_period))

        data.write(b'\xa2{\xb5\xa7')  # 0xa27bb5a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa27bb5a7))

        data.write(b'\xe3X\x0b+')  # 0xe3580b2b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe3580b2b))

        data.write(b'\xb0]\xad\xe7')  # 0xb05dade7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slow_speed_period_scale))

        data.write(b'm\xc5\xd4@')  # 0x6dc5d440
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.target_magnitude_tracking_rate))

        data.write(b'\xd1e9\xa7')  # 0xd16539a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.landing_bob_spring_constant))

        data.write(b'\xad\xbb\nB')  # 0xadbb0a42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.view_wander_radius))

        data.write(b'\xe7\xf8\xf1\x1b')  # 0xe7f8f11b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.view_wander_speed_min))

        data.write(b'\x01\x98^\xfa')  # 0x1985efa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.view_wander_speed_max))

        data.write(b'\xef\x19\xba3')  # 0xef19ba33
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.view_wander_roll_variation))

        data.write(b'\x7fY\xbe\x96')  # 0x7f59be96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gun_bob_magnitude))

        data.write(b'8\xa8*\xc1')  # 0x38a82ac1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.helmet_bob_magnitude))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            instance_name=data['instance_name'],
            camera_bob_extent_x=data['camera_bob_extent_x'],
            camera_bob_extent_y=data['camera_bob_extent_y'],
            camera_bob_period=data['camera_bob_period'],
            unknown_0xa27bb5a7=data['unknown_0xa27bb5a7'],
            unknown_0xe3580b2b=data['unknown_0xe3580b2b'],
            slow_speed_period_scale=data['slow_speed_period_scale'],
            target_magnitude_tracking_rate=data['target_magnitude_tracking_rate'],
            landing_bob_spring_constant=data['landing_bob_spring_constant'],
            view_wander_radius=data['view_wander_radius'],
            view_wander_speed_min=data['view_wander_speed_min'],
            view_wander_speed_max=data['view_wander_speed_max'],
            view_wander_roll_variation=data['view_wander_roll_variation'],
            gun_bob_magnitude=data['gun_bob_magnitude'],
            helmet_bob_magnitude=data['helmet_bob_magnitude'],
        )

    def to_json(self) -> dict:
        return {
            'instance_name': self.instance_name,
            'camera_bob_extent_x': self.camera_bob_extent_x,
            'camera_bob_extent_y': self.camera_bob_extent_y,
            'camera_bob_period': self.camera_bob_period,
            'unknown_0xa27bb5a7': self.unknown_0xa27bb5a7,
            'unknown_0xe3580b2b': self.unknown_0xe3580b2b,
            'slow_speed_period_scale': self.slow_speed_period_scale,
            'target_magnitude_tracking_rate': self.target_magnitude_tracking_rate,
            'landing_bob_spring_constant': self.landing_bob_spring_constant,
            'view_wander_radius': self.view_wander_radius,
            'view_wander_speed_min': self.view_wander_speed_min,
            'view_wander_speed_max': self.view_wander_speed_max,
            'view_wander_roll_variation': self.view_wander_roll_variation,
            'gun_bob_magnitude': self.gun_bob_magnitude,
            'helmet_bob_magnitude': self.helmet_bob_magnitude,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_instance_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_camera_bob_extent_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_bob_extent_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_bob_period(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa27bb5a7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe3580b2b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slow_speed_period_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_target_magnitude_tracking_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_landing_bob_spring_constant(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_view_wander_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_view_wander_speed_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_view_wander_speed_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_view_wander_roll_variation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gun_bob_magnitude(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_helmet_bob_magnitude(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7fda1466: ('instance_name', _decode_instance_name),
    0xe2a0b6f1: ('camera_bob_extent_x', _decode_camera_bob_extent_x),
    0x29fc6554: ('camera_bob_extent_y', _decode_camera_bob_extent_y),
    0x149d7339: ('camera_bob_period', _decode_camera_bob_period),
    0xa27bb5a7: ('unknown_0xa27bb5a7', _decode_unknown_0xa27bb5a7),
    0xe3580b2b: ('unknown_0xe3580b2b', _decode_unknown_0xe3580b2b),
    0xb05dade7: ('slow_speed_period_scale', _decode_slow_speed_period_scale),
    0x6dc5d440: ('target_magnitude_tracking_rate', _decode_target_magnitude_tracking_rate),
    0xd16539a7: ('landing_bob_spring_constant', _decode_landing_bob_spring_constant),
    0xadbb0a42: ('view_wander_radius', _decode_view_wander_radius),
    0xe7f8f11b: ('view_wander_speed_min', _decode_view_wander_speed_min),
    0x1985efa: ('view_wander_speed_max', _decode_view_wander_speed_max),
    0xef19ba33: ('view_wander_roll_variation', _decode_view_wander_roll_variation),
    0x7f59be96: ('gun_bob_magnitude', _decode_gun_bob_magnitude),
    0x38a82ac1: ('helmet_bob_magnitude', _decode_helmet_bob_magnitude),
}
