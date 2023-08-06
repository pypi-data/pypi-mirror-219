# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.LocomotionContextEnum import LocomotionContextEnum
from retro_data_structures.properties.dkc_returns.archetypes.WanderRandomTurnData import WanderRandomTurnData


@dataclasses.dataclass()
class WanderBehaviorData(BaseProperty):
    move_toward_nearest_player_on_init: bool = dataclasses.field(default=False)
    seek_player: bool = dataclasses.field(default=False)
    use_seek_activation_range: bool = dataclasses.field(default=False)
    seek_activation_range_squared: float = dataclasses.field(default=0.0)
    maintain_distance: bool = dataclasses.field(default=False)
    desired_distance: float = dataclasses.field(default=7.0)
    min_time_between_direction_changes: float = dataclasses.field(default=1.0)
    ignore_tar_inhibited_players: bool = dataclasses.field(default=False)
    minimum_seek_direction_time: float = dataclasses.field(default=3.0)
    use_seeking_tarred_player_locomotion_context: bool = dataclasses.field(default=False)
    use_platform_edge_as_bounds: bool = dataclasses.field(default=False)
    seeking_tarred_player_locomotion_context: LocomotionContextEnum = dataclasses.field(default_factory=LocomotionContextEnum)
    enable_random_turn: bool = dataclasses.field(default=False)
    random_turn: WanderRandomTurnData = dataclasses.field(default_factory=WanderRandomTurnData)

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
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'A\x83$Y')  # 0x41832459
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.move_toward_nearest_player_on_init))

        data.write(b'l\xea\x0e\xba')  # 0x6cea0eba
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.seek_player))

        data.write(b"\x14\xd0'\xb0")  # 0x14d027b0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_seek_activation_range))

        data.write(b'\x9b\x8b\xec\x06')  # 0x9b8bec06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.seek_activation_range_squared))

        data.write(b'\x00\x9a\x130')  # 0x9a1330
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.maintain_distance))

        data.write(b'`\xbe5\xa1')  # 0x60be35a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.desired_distance))

        data.write(b'\x8f^wy')  # 0x8f5e7779
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_time_between_direction_changes))

        data.write(b'W\x18U\xa7')  # 0x571855a7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_tar_inhibited_players))

        data.write(b'\xe9\xe0\xbe\xb6')  # 0xe9e0beb6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_seek_direction_time))

        data.write(b'\x9a\xeb\x03\xd9')  # 0x9aeb03d9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_seeking_tarred_player_locomotion_context))

        data.write(b'\x9a\x12\x87\xd4')  # 0x9a1287d4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_platform_edge_as_bounds))

        data.write(b'\x12\x96\xe3\x16')  # 0x1296e316
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seeking_tarred_player_locomotion_context.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93\x8ce\x1f')  # 0x938c651f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_random_turn))

        data.write(b'f3\x87|')  # 0x6633877c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.random_turn.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            move_toward_nearest_player_on_init=data['move_toward_nearest_player_on_init'],
            seek_player=data['seek_player'],
            use_seek_activation_range=data['use_seek_activation_range'],
            seek_activation_range_squared=data['seek_activation_range_squared'],
            maintain_distance=data['maintain_distance'],
            desired_distance=data['desired_distance'],
            min_time_between_direction_changes=data['min_time_between_direction_changes'],
            ignore_tar_inhibited_players=data['ignore_tar_inhibited_players'],
            minimum_seek_direction_time=data['minimum_seek_direction_time'],
            use_seeking_tarred_player_locomotion_context=data['use_seeking_tarred_player_locomotion_context'],
            use_platform_edge_as_bounds=data['use_platform_edge_as_bounds'],
            seeking_tarred_player_locomotion_context=LocomotionContextEnum.from_json(data['seeking_tarred_player_locomotion_context']),
            enable_random_turn=data['enable_random_turn'],
            random_turn=WanderRandomTurnData.from_json(data['random_turn']),
        )

    def to_json(self) -> dict:
        return {
            'move_toward_nearest_player_on_init': self.move_toward_nearest_player_on_init,
            'seek_player': self.seek_player,
            'use_seek_activation_range': self.use_seek_activation_range,
            'seek_activation_range_squared': self.seek_activation_range_squared,
            'maintain_distance': self.maintain_distance,
            'desired_distance': self.desired_distance,
            'min_time_between_direction_changes': self.min_time_between_direction_changes,
            'ignore_tar_inhibited_players': self.ignore_tar_inhibited_players,
            'minimum_seek_direction_time': self.minimum_seek_direction_time,
            'use_seeking_tarred_player_locomotion_context': self.use_seeking_tarred_player_locomotion_context,
            'use_platform_edge_as_bounds': self.use_platform_edge_as_bounds,
            'seeking_tarred_player_locomotion_context': self.seeking_tarred_player_locomotion_context.to_json(),
            'enable_random_turn': self.enable_random_turn,
            'random_turn': self.random_turn.to_json(),
        }


def _decode_move_toward_nearest_player_on_init(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_seek_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_seek_activation_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_seek_activation_range_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maintain_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_desired_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_time_between_direction_changes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_tar_inhibited_players(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minimum_seek_direction_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_seeking_tarred_player_locomotion_context(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_platform_edge_as_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_seeking_tarred_player_locomotion_context(data: typing.BinaryIO, property_size: int):
    return LocomotionContextEnum.from_stream(data, property_size)


def _decode_enable_random_turn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_random_turn(data: typing.BinaryIO, property_size: int):
    return WanderRandomTurnData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x41832459: ('move_toward_nearest_player_on_init', _decode_move_toward_nearest_player_on_init),
    0x6cea0eba: ('seek_player', _decode_seek_player),
    0x14d027b0: ('use_seek_activation_range', _decode_use_seek_activation_range),
    0x9b8bec06: ('seek_activation_range_squared', _decode_seek_activation_range_squared),
    0x9a1330: ('maintain_distance', _decode_maintain_distance),
    0x60be35a1: ('desired_distance', _decode_desired_distance),
    0x8f5e7779: ('min_time_between_direction_changes', _decode_min_time_between_direction_changes),
    0x571855a7: ('ignore_tar_inhibited_players', _decode_ignore_tar_inhibited_players),
    0xe9e0beb6: ('minimum_seek_direction_time', _decode_minimum_seek_direction_time),
    0x9aeb03d9: ('use_seeking_tarred_player_locomotion_context', _decode_use_seeking_tarred_player_locomotion_context),
    0x9a1287d4: ('use_platform_edge_as_bounds', _decode_use_platform_edge_as_bounds),
    0x1296e316: ('seeking_tarred_player_locomotion_context', _decode_seeking_tarred_player_locomotion_context),
    0x938c651f: ('enable_random_turn', _decode_enable_random_turn),
    0x6633877c: ('random_turn', _decode_random_turn),
}
