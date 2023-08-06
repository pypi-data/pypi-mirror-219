# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.GhorStructC import GhorStructC
from retro_data_structures.properties.corruption.archetypes.ShockWaveInfo import ShockWaveInfo
from retro_data_structures.properties.corruption.archetypes.UnknownStruct35 import UnknownStruct35
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct36(BaseProperty):
    is_gandrayda: bool = dataclasses.field(default=False)
    slip_time: float = dataclasses.field(default=4.0)
    collision_set: str = dataclasses.field(default='')
    unknown_0xfaf186b6: str = dataclasses.field(default='')
    snap_locator: str = dataclasses.field(default='')
    unknown_struct35: UnknownStruct35 = dataclasses.field(default_factory=UnknownStruct35)
    ghor_struct_c: GhorStructC = dataclasses.field(default_factory=GhorStructC)
    ball_target_extend: Spline = dataclasses.field(default_factory=Spline)
    ball_target_retract: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x13d02889: str = dataclasses.field(default='')
    unknown_0x4a744859: Spline = dataclasses.field(default_factory=Spline)
    jump_distance: float = dataclasses.field(default=25.0)
    jump_height: float = dataclasses.field(default=14.0)
    jump_shockwave: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    move_min_range: float = dataclasses.field(default=15.0)
    move_max_range: float = dataclasses.field(default=50.0)
    move_desired_range: float = dataclasses.field(default=40.0)
    move_min_distance: float = dataclasses.field(default=15.0)
    move_desired_distance: float = dataclasses.field(default=20.0)
    unknown_0xa31d0055: float = dataclasses.field(default=20.0)
    unknown_0x9ae279da: float = dataclasses.field(default=1.0)
    unknown_0xb39c84c2: float = dataclasses.field(default=3.0)
    unknown_0x2a35593b: float = dataclasses.field(default=8.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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

        data.write(b'S\x1a\x8c\x85')  # 0x531a8c85
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_gandrayda))

        data.write(b'\xe9\x86_\xc0')  # 0xe9865fc0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slip_time))

        data.write(b'\x9c\xe3\x1f\xfa')  # 0x9ce31ffa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.collision_set.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xf1\x86\xb6')  # 0xfaf186b6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0xfaf186b6.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\x19I\xb5')  # 0x5d1949b5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.snap_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xae\xc7Tn')  # 0xaec7546e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct35.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\x0e\xc4\x9a')  # 0x810ec49a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\x98\xf8\xce')  # 0x9b98f8ce
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_target_extend.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'=\x14\xfb\x8e')  # 0x3d14fb8e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_target_retract.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x13\xd0(\x89')  # 0x13d02889
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x13d02889.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'JtHY')  # 0x4a744859
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x4a744859.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b.\xa4\x89')  # 0x9b2ea489
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_distance))

        data.write(b'\xd0GQ\x91')  # 0xd0475191
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_height))

        data.write(b'V\xc1\x92\xf3')  # 0x56c192f3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_shockwave.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5Z\x15H')  # 0xf55a1548
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85T\xe3`')  # 0x8554e360
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_min_range))

        data.write(b'\xc5\x1b\x9b\x16')  # 0xc51b9b16
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_max_range))

        data.write(b'\xaf\xec\xab\x12')  # 0xafecab12
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_desired_range))

        data.write(b'|\xc5\x9b1')  # 0x7cc59b31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_min_distance))

        data.write(b'\xd6\xaa\xd9\x96')  # 0xd6aad996
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.move_desired_distance))

        data.write(b'\xa3\x1d\x00U')  # 0xa31d0055
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa31d0055))

        data.write(b'\x9a\xe2y\xda')  # 0x9ae279da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9ae279da))

        data.write(b'\xb3\x9c\x84\xc2')  # 0xb39c84c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb39c84c2))

        data.write(b'*5Y;')  # 0x2a35593b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2a35593b))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            is_gandrayda=data['is_gandrayda'],
            slip_time=data['slip_time'],
            collision_set=data['collision_set'],
            unknown_0xfaf186b6=data['unknown_0xfaf186b6'],
            snap_locator=data['snap_locator'],
            unknown_struct35=UnknownStruct35.from_json(data['unknown_struct35']),
            ghor_struct_c=GhorStructC.from_json(data['ghor_struct_c']),
            ball_target_extend=Spline.from_json(data['ball_target_extend']),
            ball_target_retract=Spline.from_json(data['ball_target_retract']),
            unknown_0x13d02889=data['unknown_0x13d02889'],
            unknown_0x4a744859=Spline.from_json(data['unknown_0x4a744859']),
            jump_distance=data['jump_distance'],
            jump_height=data['jump_height'],
            jump_shockwave=ShockWaveInfo.from_json(data['jump_shockwave']),
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
            move_min_range=data['move_min_range'],
            move_max_range=data['move_max_range'],
            move_desired_range=data['move_desired_range'],
            move_min_distance=data['move_min_distance'],
            move_desired_distance=data['move_desired_distance'],
            unknown_0xa31d0055=data['unknown_0xa31d0055'],
            unknown_0x9ae279da=data['unknown_0x9ae279da'],
            unknown_0xb39c84c2=data['unknown_0xb39c84c2'],
            unknown_0x2a35593b=data['unknown_0x2a35593b'],
        )

    def to_json(self) -> dict:
        return {
            'is_gandrayda': self.is_gandrayda,
            'slip_time': self.slip_time,
            'collision_set': self.collision_set,
            'unknown_0xfaf186b6': self.unknown_0xfaf186b6,
            'snap_locator': self.snap_locator,
            'unknown_struct35': self.unknown_struct35.to_json(),
            'ghor_struct_c': self.ghor_struct_c.to_json(),
            'ball_target_extend': self.ball_target_extend.to_json(),
            'ball_target_retract': self.ball_target_retract.to_json(),
            'unknown_0x13d02889': self.unknown_0x13d02889,
            'unknown_0x4a744859': self.unknown_0x4a744859.to_json(),
            'jump_distance': self.jump_distance,
            'jump_height': self.jump_height,
            'jump_shockwave': self.jump_shockwave.to_json(),
            'shock_wave_info': self.shock_wave_info.to_json(),
            'move_min_range': self.move_min_range,
            'move_max_range': self.move_max_range,
            'move_desired_range': self.move_desired_range,
            'move_min_distance': self.move_min_distance,
            'move_desired_distance': self.move_desired_distance,
            'unknown_0xa31d0055': self.unknown_0xa31d0055,
            'unknown_0x9ae279da': self.unknown_0x9ae279da,
            'unknown_0xb39c84c2': self.unknown_0xb39c84c2,
            'unknown_0x2a35593b': self.unknown_0x2a35593b,
        }


def _decode_is_gandrayda(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_slip_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_collision_set(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0xfaf186b6(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_snap_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_struct35(data: typing.BinaryIO, property_size: int):
    return UnknownStruct35.from_stream(data, property_size)


def _decode_ghor_struct_c(data: typing.BinaryIO, property_size: int):
    return GhorStructC.from_stream(data, property_size)


def _decode_ball_target_extend(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_ball_target_retract(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x13d02889(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x4a744859(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_jump_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_shockwave(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_move_min_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move_max_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move_desired_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move_min_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_move_desired_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa31d0055(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9ae279da(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb39c84c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2a35593b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x531a8c85: ('is_gandrayda', _decode_is_gandrayda),
    0xe9865fc0: ('slip_time', _decode_slip_time),
    0x9ce31ffa: ('collision_set', _decode_collision_set),
    0xfaf186b6: ('unknown_0xfaf186b6', _decode_unknown_0xfaf186b6),
    0x5d1949b5: ('snap_locator', _decode_snap_locator),
    0xaec7546e: ('unknown_struct35', _decode_unknown_struct35),
    0x810ec49a: ('ghor_struct_c', _decode_ghor_struct_c),
    0x9b98f8ce: ('ball_target_extend', _decode_ball_target_extend),
    0x3d14fb8e: ('ball_target_retract', _decode_ball_target_retract),
    0x13d02889: ('unknown_0x13d02889', _decode_unknown_0x13d02889),
    0x4a744859: ('unknown_0x4a744859', _decode_unknown_0x4a744859),
    0x9b2ea489: ('jump_distance', _decode_jump_distance),
    0xd0475191: ('jump_height', _decode_jump_height),
    0x56c192f3: ('jump_shockwave', _decode_jump_shockwave),
    0xf55a1548: ('shock_wave_info', _decode_shock_wave_info),
    0x8554e360: ('move_min_range', _decode_move_min_range),
    0xc51b9b16: ('move_max_range', _decode_move_max_range),
    0xafecab12: ('move_desired_range', _decode_move_desired_range),
    0x7cc59b31: ('move_min_distance', _decode_move_min_distance),
    0xd6aad996: ('move_desired_distance', _decode_move_desired_distance),
    0xa31d0055: ('unknown_0xa31d0055', _decode_unknown_0xa31d0055),
    0x9ae279da: ('unknown_0x9ae279da', _decode_unknown_0x9ae279da),
    0xb39c84c2: ('unknown_0xb39c84c2', _decode_unknown_0xb39c84c2),
    0x2a35593b: ('unknown_0x2a35593b', _decode_unknown_0x2a35593b),
}
