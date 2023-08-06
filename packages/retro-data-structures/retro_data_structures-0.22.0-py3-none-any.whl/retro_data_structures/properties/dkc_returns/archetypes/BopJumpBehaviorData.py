# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.BopJumpData import BopJumpData


@dataclasses.dataclass()
class BopJumpBehaviorData(BaseProperty):
    bop_jump_type: enums.BopJumpType = dataclasses.field(default=enums.BopJumpType.Unknown1)
    number_of_jumps: int = dataclasses.field(default=2)
    jump1: BopJumpData = dataclasses.field(default_factory=BopJumpData)
    jump2: BopJumpData = dataclasses.field(default_factory=BopJumpData)
    jump3: BopJumpData = dataclasses.field(default_factory=BopJumpData)
    jump4: BopJumpData = dataclasses.field(default_factory=BopJumpData)
    jump5: BopJumpData = dataclasses.field(default_factory=BopJumpData)
    jump_delay_time: float = dataclasses.field(default=1.0)
    no_actor_collision: bool = dataclasses.field(default=False)
    turn_at_bounds: bool = dataclasses.field(default=True)
    direction_control: enums.DirectionControl = dataclasses.field(default=enums.DirectionControl.Unknown1)
    jump_when_player_jumps: bool = dataclasses.field(default=False)
    jump_when_bumping_wall: bool = dataclasses.field(default=False)
    ignore_tar_inhibited_players: bool = dataclasses.field(default=True)
    minimum_seek_direction_time: float = dataclasses.field(default=3.0)
    pursuit_distance: float = dataclasses.field(default=0.0)
    reverse_base_chance: float = dataclasses.field(default=10.0)
    reverse_additional_chance: float = dataclasses.field(default=5.0)

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'v\xe1p\xef')  # 0x76e170ef
        data.write(b'\x00\x04')  # size
        self.bop_jump_type.to_stream(data)

        data.write(b'\xf2\xb3\xc5\xa1')  # 0xf2b3c5a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_jumps))

        data.write(b'\xcbV\x07c')  # 0xcb560763
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc\xc8\xd5\x93')  # 0xbcc8d593
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump2.to_stream(data, default_override={'height': 2.0, 'distance': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"'m\x99\xfc")  # 0x276d99fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S\xf5ps')  # 0x53f57073
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc8P<\x1c')  # 0xc8503c1c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xf3\xd4\xfa')  # 0x36f3d4fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_delay_time))

        data.write(b';\xb9\x9cx')  # 0x3bb99c78
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.no_actor_collision))

        data.write(b'_\xa0 \xff')  # 0x5fa020ff
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.turn_at_bounds))

        data.write(b'\x01UX\xf8')  # 0x15558f8
        data.write(b'\x00\x04')  # size
        self.direction_control.to_stream(data)

        data.write(b'\xae\xb9qW')  # 0xaeb97157
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.jump_when_player_jumps))

        data.write(b'#\xcbDv')  # 0x23cb4476
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.jump_when_bumping_wall))

        data.write(b'W\x18U\xa7')  # 0x571855a7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_tar_inhibited_players))

        data.write(b'\xe9\xe0\xbe\xb6')  # 0xe9e0beb6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_seek_direction_time))

        data.write(b'\xc9F\xd3\xef')  # 0xc946d3ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pursuit_distance))

        data.write(b'x;8/')  # 0x783b382f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverse_base_chance))

        data.write(b'\xb2\xf9\x97Y')  # 0xb2f99759
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reverse_additional_chance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            bop_jump_type=enums.BopJumpType.from_json(data['bop_jump_type']),
            number_of_jumps=data['number_of_jumps'],
            jump1=BopJumpData.from_json(data['jump1']),
            jump2=BopJumpData.from_json(data['jump2']),
            jump3=BopJumpData.from_json(data['jump3']),
            jump4=BopJumpData.from_json(data['jump4']),
            jump5=BopJumpData.from_json(data['jump5']),
            jump_delay_time=data['jump_delay_time'],
            no_actor_collision=data['no_actor_collision'],
            turn_at_bounds=data['turn_at_bounds'],
            direction_control=enums.DirectionControl.from_json(data['direction_control']),
            jump_when_player_jumps=data['jump_when_player_jumps'],
            jump_when_bumping_wall=data['jump_when_bumping_wall'],
            ignore_tar_inhibited_players=data['ignore_tar_inhibited_players'],
            minimum_seek_direction_time=data['minimum_seek_direction_time'],
            pursuit_distance=data['pursuit_distance'],
            reverse_base_chance=data['reverse_base_chance'],
            reverse_additional_chance=data['reverse_additional_chance'],
        )

    def to_json(self) -> dict:
        return {
            'bop_jump_type': self.bop_jump_type.to_json(),
            'number_of_jumps': self.number_of_jumps,
            'jump1': self.jump1.to_json(),
            'jump2': self.jump2.to_json(),
            'jump3': self.jump3.to_json(),
            'jump4': self.jump4.to_json(),
            'jump5': self.jump5.to_json(),
            'jump_delay_time': self.jump_delay_time,
            'no_actor_collision': self.no_actor_collision,
            'turn_at_bounds': self.turn_at_bounds,
            'direction_control': self.direction_control.to_json(),
            'jump_when_player_jumps': self.jump_when_player_jumps,
            'jump_when_bumping_wall': self.jump_when_bumping_wall,
            'ignore_tar_inhibited_players': self.ignore_tar_inhibited_players,
            'minimum_seek_direction_time': self.minimum_seek_direction_time,
            'pursuit_distance': self.pursuit_distance,
            'reverse_base_chance': self.reverse_base_chance,
            'reverse_additional_chance': self.reverse_additional_chance,
        }


def _decode_bop_jump_type(data: typing.BinaryIO, property_size: int):
    return enums.BopJumpType.from_stream(data)


def _decode_number_of_jumps(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_jump1(data: typing.BinaryIO, property_size: int):
    return BopJumpData.from_stream(data, property_size)


def _decode_jump2(data: typing.BinaryIO, property_size: int):
    return BopJumpData.from_stream(data, property_size, default_override={'height': 2.0, 'distance': 1.0})


def _decode_jump3(data: typing.BinaryIO, property_size: int):
    return BopJumpData.from_stream(data, property_size)


def _decode_jump4(data: typing.BinaryIO, property_size: int):
    return BopJumpData.from_stream(data, property_size)


def _decode_jump5(data: typing.BinaryIO, property_size: int):
    return BopJumpData.from_stream(data, property_size)


def _decode_jump_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_no_actor_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_turn_at_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_direction_control(data: typing.BinaryIO, property_size: int):
    return enums.DirectionControl.from_stream(data)


def _decode_jump_when_player_jumps(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_jump_when_bumping_wall(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_tar_inhibited_players(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minimum_seek_direction_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pursuit_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverse_base_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reverse_additional_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x76e170ef: ('bop_jump_type', _decode_bop_jump_type),
    0xf2b3c5a1: ('number_of_jumps', _decode_number_of_jumps),
    0xcb560763: ('jump1', _decode_jump1),
    0xbcc8d593: ('jump2', _decode_jump2),
    0x276d99fc: ('jump3', _decode_jump3),
    0x53f57073: ('jump4', _decode_jump4),
    0xc8503c1c: ('jump5', _decode_jump5),
    0x36f3d4fa: ('jump_delay_time', _decode_jump_delay_time),
    0x3bb99c78: ('no_actor_collision', _decode_no_actor_collision),
    0x5fa020ff: ('turn_at_bounds', _decode_turn_at_bounds),
    0x15558f8: ('direction_control', _decode_direction_control),
    0xaeb97157: ('jump_when_player_jumps', _decode_jump_when_player_jumps),
    0x23cb4476: ('jump_when_bumping_wall', _decode_jump_when_bumping_wall),
    0x571855a7: ('ignore_tar_inhibited_players', _decode_ignore_tar_inhibited_players),
    0xe9e0beb6: ('minimum_seek_direction_time', _decode_minimum_seek_direction_time),
    0xc946d3ef: ('pursuit_distance', _decode_pursuit_distance),
    0x783b382f: ('reverse_base_chance', _decode_reverse_base_chance),
    0xb2f99759: ('reverse_additional_chance', _decode_reverse_additional_chance),
}
