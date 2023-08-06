# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.AnimGridModifierData import AnimGridModifierData
from retro_data_structures.properties.dkc_returns.archetypes.RobotChickenFlyerStructA import RobotChickenFlyerStructA
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct260 import UnknownStruct260
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct261 import UnknownStruct261


@dataclasses.dataclass()
class UnknownStruct262(BaseProperty):
    snap_to_spline: bool = dataclasses.field(default=True)
    floor_height: float = dataclasses.field(default=0.0)
    gravity: float = dataclasses.field(default=55.0)
    acceleration: float = dataclasses.field(default=20.0)
    deceleration: float = dataclasses.field(default=12.0)
    maximum_speed: float = dataclasses.field(default=12.0)
    unknown_0xe46e8d01: float = dataclasses.field(default=10.0)
    use_player_crush: bool = dataclasses.field(default=False)
    max_children: int = dataclasses.field(default=6)
    child_spawn_time: float = dataclasses.field(default=2.0)
    unknown_0xd2d92d71: int = dataclasses.field(default=9)
    unknown_0x1cc6b88d: float = dataclasses.field(default=0.8700000047683716)
    unknown_0x9605aad3: int = dataclasses.field(default=20)
    unknown_0x806dc773: float = dataclasses.field(default=0.0)
    unknown_0x101ed799: float = dataclasses.field(default=9.0)
    unknown_0xbbd7c692: float = dataclasses.field(default=13.0)
    robot_chicken_flyer_struct_a_0xe84aa51c: RobotChickenFlyerStructA = dataclasses.field(default_factory=RobotChickenFlyerStructA)
    robot_chicken_flyer_struct_a_0xa152f46f: RobotChickenFlyerStructA = dataclasses.field(default_factory=RobotChickenFlyerStructA)
    robot_chicken_flyer_struct_a_0x1f59e2c1: RobotChickenFlyerStructA = dataclasses.field(default_factory=RobotChickenFlyerStructA)
    robot_chicken_flyer_struct_a_0xc4d0e557: RobotChickenFlyerStructA = dataclasses.field(default_factory=RobotChickenFlyerStructA)
    unknown_struct260: UnknownStruct260 = dataclasses.field(default_factory=UnknownStruct260)
    anim_grid: AnimGridModifierData = dataclasses.field(default_factory=AnimGridModifierData)
    unknown_struct261: UnknownStruct261 = dataclasses.field(default_factory=UnknownStruct261)

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
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'&\xec\xb99')  # 0x26ecb939
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_to_spline))

        data.write(b'\x04\x1d\xa1r')  # 0x41da172
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_height))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'\x14\x0e\xf2\xcc')  # 0x140ef2cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_speed))

        data.write(b'\xe4n\x8d\x01')  # 0xe46e8d01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe46e8d01))

        data.write(b'\xea\x05i\xd2')  # 0xea0569d2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_player_crush))

        data.write(b'\x8b\x12\xf3\xb0')  # 0x8b12f3b0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_children))

        data.write(b'h\xda\xe7\xe9')  # 0x68dae7e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.child_spawn_time))

        data.write(b'\xd2\xd9-q')  # 0xd2d92d71
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd2d92d71))

        data.write(b'\x1c\xc6\xb8\x8d')  # 0x1cc6b88d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1cc6b88d))

        data.write(b'\x96\x05\xaa\xd3')  # 0x9605aad3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x9605aad3))

        data.write(b'\x80m\xc7s')  # 0x806dc773
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x806dc773))

        data.write(b'\x10\x1e\xd7\x99')  # 0x101ed799
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x101ed799))

        data.write(b'\xbb\xd7\xc6\x92')  # 0xbbd7c692
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbbd7c692))

        data.write(b'\xe8J\xa5\x1c')  # 0xe84aa51c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_a_0xe84aa51c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1R\xf4o')  # 0xa152f46f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_a_0xa152f46f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1fY\xe2\xc1')  # 0x1f59e2c1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_a_0x1f59e2c1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc4\xd0\xe5W')  # 0xc4d0e557
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_a_0xc4d0e557.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\x01\x1e\xc5')  # 0xf8011ec5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct260.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\xfdI\xae')  # 0x68fd49ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.anim_grid.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\x01Q\xf6')  # 0x420151f6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct261.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            snap_to_spline=data['snap_to_spline'],
            floor_height=data['floor_height'],
            gravity=data['gravity'],
            acceleration=data['acceleration'],
            deceleration=data['deceleration'],
            maximum_speed=data['maximum_speed'],
            unknown_0xe46e8d01=data['unknown_0xe46e8d01'],
            use_player_crush=data['use_player_crush'],
            max_children=data['max_children'],
            child_spawn_time=data['child_spawn_time'],
            unknown_0xd2d92d71=data['unknown_0xd2d92d71'],
            unknown_0x1cc6b88d=data['unknown_0x1cc6b88d'],
            unknown_0x9605aad3=data['unknown_0x9605aad3'],
            unknown_0x806dc773=data['unknown_0x806dc773'],
            unknown_0x101ed799=data['unknown_0x101ed799'],
            unknown_0xbbd7c692=data['unknown_0xbbd7c692'],
            robot_chicken_flyer_struct_a_0xe84aa51c=RobotChickenFlyerStructA.from_json(data['robot_chicken_flyer_struct_a_0xe84aa51c']),
            robot_chicken_flyer_struct_a_0xa152f46f=RobotChickenFlyerStructA.from_json(data['robot_chicken_flyer_struct_a_0xa152f46f']),
            robot_chicken_flyer_struct_a_0x1f59e2c1=RobotChickenFlyerStructA.from_json(data['robot_chicken_flyer_struct_a_0x1f59e2c1']),
            robot_chicken_flyer_struct_a_0xc4d0e557=RobotChickenFlyerStructA.from_json(data['robot_chicken_flyer_struct_a_0xc4d0e557']),
            unknown_struct260=UnknownStruct260.from_json(data['unknown_struct260']),
            anim_grid=AnimGridModifierData.from_json(data['anim_grid']),
            unknown_struct261=UnknownStruct261.from_json(data['unknown_struct261']),
        )

    def to_json(self) -> dict:
        return {
            'snap_to_spline': self.snap_to_spline,
            'floor_height': self.floor_height,
            'gravity': self.gravity,
            'acceleration': self.acceleration,
            'deceleration': self.deceleration,
            'maximum_speed': self.maximum_speed,
            'unknown_0xe46e8d01': self.unknown_0xe46e8d01,
            'use_player_crush': self.use_player_crush,
            'max_children': self.max_children,
            'child_spawn_time': self.child_spawn_time,
            'unknown_0xd2d92d71': self.unknown_0xd2d92d71,
            'unknown_0x1cc6b88d': self.unknown_0x1cc6b88d,
            'unknown_0x9605aad3': self.unknown_0x9605aad3,
            'unknown_0x806dc773': self.unknown_0x806dc773,
            'unknown_0x101ed799': self.unknown_0x101ed799,
            'unknown_0xbbd7c692': self.unknown_0xbbd7c692,
            'robot_chicken_flyer_struct_a_0xe84aa51c': self.robot_chicken_flyer_struct_a_0xe84aa51c.to_json(),
            'robot_chicken_flyer_struct_a_0xa152f46f': self.robot_chicken_flyer_struct_a_0xa152f46f.to_json(),
            'robot_chicken_flyer_struct_a_0x1f59e2c1': self.robot_chicken_flyer_struct_a_0x1f59e2c1.to_json(),
            'robot_chicken_flyer_struct_a_0xc4d0e557': self.robot_chicken_flyer_struct_a_0xc4d0e557.to_json(),
            'unknown_struct260': self.unknown_struct260.to_json(),
            'anim_grid': self.anim_grid.to_json(),
            'unknown_struct261': self.unknown_struct261.to_json(),
        }


def _decode_snap_to_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_floor_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe46e8d01(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_player_crush(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_children(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_child_spawn_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd2d92d71(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1cc6b88d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9605aad3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x806dc773(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x101ed799(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbbd7c692(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_robot_chicken_flyer_struct_a_0xe84aa51c(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructA.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_a_0xa152f46f(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructA.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_a_0x1f59e2c1(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructA.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_a_0xc4d0e557(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructA.from_stream(data, property_size)


def _decode_unknown_struct260(data: typing.BinaryIO, property_size: int):
    return UnknownStruct260.from_stream(data, property_size)


def _decode_anim_grid(data: typing.BinaryIO, property_size: int):
    return AnimGridModifierData.from_stream(data, property_size)


def _decode_unknown_struct261(data: typing.BinaryIO, property_size: int):
    return UnknownStruct261.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x26ecb939: ('snap_to_spline', _decode_snap_to_spline),
    0x41da172: ('floor_height', _decode_floor_height),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0x140ef2cc: ('maximum_speed', _decode_maximum_speed),
    0xe46e8d01: ('unknown_0xe46e8d01', _decode_unknown_0xe46e8d01),
    0xea0569d2: ('use_player_crush', _decode_use_player_crush),
    0x8b12f3b0: ('max_children', _decode_max_children),
    0x68dae7e9: ('child_spawn_time', _decode_child_spawn_time),
    0xd2d92d71: ('unknown_0xd2d92d71', _decode_unknown_0xd2d92d71),
    0x1cc6b88d: ('unknown_0x1cc6b88d', _decode_unknown_0x1cc6b88d),
    0x9605aad3: ('unknown_0x9605aad3', _decode_unknown_0x9605aad3),
    0x806dc773: ('unknown_0x806dc773', _decode_unknown_0x806dc773),
    0x101ed799: ('unknown_0x101ed799', _decode_unknown_0x101ed799),
    0xbbd7c692: ('unknown_0xbbd7c692', _decode_unknown_0xbbd7c692),
    0xe84aa51c: ('robot_chicken_flyer_struct_a_0xe84aa51c', _decode_robot_chicken_flyer_struct_a_0xe84aa51c),
    0xa152f46f: ('robot_chicken_flyer_struct_a_0xa152f46f', _decode_robot_chicken_flyer_struct_a_0xa152f46f),
    0x1f59e2c1: ('robot_chicken_flyer_struct_a_0x1f59e2c1', _decode_robot_chicken_flyer_struct_a_0x1f59e2c1),
    0xc4d0e557: ('robot_chicken_flyer_struct_a_0xc4d0e557', _decode_robot_chicken_flyer_struct_a_0xc4d0e557),
    0xf8011ec5: ('unknown_struct260', _decode_unknown_struct260),
    0x68fd49ae: ('anim_grid', _decode_anim_grid),
    0x420151f6: ('unknown_struct261', _decode_unknown_struct261),
}
