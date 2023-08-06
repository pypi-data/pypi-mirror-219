# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.BeatUpHandlerStruct import BeatUpHandlerStruct
from retro_data_structures.properties.dkc_returns.archetypes.ControlCommands import ControlCommands
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Data(BaseProperty):
    left_command: ControlCommands = dataclasses.field(default_factory=ControlCommands)
    control_command: ControlCommands = dataclasses.field(default_factory=ControlCommands)
    swing_delay_same: float = dataclasses.field(default=1.0)
    swing_delay_different: float = dataclasses.field(default=0.10000000149011612)
    swing_delay_any: float = dataclasses.field(default=0.10000000149011612)
    randomize_hits: bool = dataclasses.field(default=False)
    skip_initial_hit: bool = dataclasses.field(default=False)
    allow_both_players_to_hit: bool = dataclasses.field(default=False)
    max_beat_up_time: float = dataclasses.field(default=0.0)
    max_multiplier: int = dataclasses.field(default=100)
    prize1: BeatUpHandlerStruct = dataclasses.field(default_factory=BeatUpHandlerStruct)
    prize2: BeatUpHandlerStruct = dataclasses.field(default_factory=BeatUpHandlerStruct)
    prize3: BeatUpHandlerStruct = dataclasses.field(default_factory=BeatUpHandlerStruct)
    hit_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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

        data.write(b'\xf6\xae]|')  # 0xf6ae5d7c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.left_command.to_stream(data, default_override={'command': enums.Command.Unknown8})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\xfdOt')  # 0xd2fd4f74
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.control_command.to_stream(data, default_override={'command': enums.Command.Unknown9})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'5\xd4\x0bg')  # 0x35d40b67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_delay_same))

        data.write(b'\x82\x94\x13\x81')  # 0x82941381
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_delay_different))

        data.write(b'\xe87v\xe6')  # 0xe83776e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_delay_any))

        data.write(b'\xf8\x04\xd4\x1c')  # 0xf804d41c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.randomize_hits))

        data.write(b'\xe3\x99\xb7Z')  # 0xe399b75a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.skip_initial_hit))

        data.write(b'\xdd1\xe5Z')  # 0xdd31e55a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_both_players_to_hit))

        data.write(b'\xb5\xbb\xe8\x8a')  # 0xb5bbe88a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_beat_up_time))

        data.write(b'\xb1.X\xb8')  # 0xb12e58b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_multiplier))

        data.write(b'B\x89\xb1[')  # 0x4289b15b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prize1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'5\x17c\xab')  # 0x351763ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prize2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xae\xb2/\xc4')  # 0xaeb22fc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prize3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'U-\xb7,')  # 0x552db72c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hit_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            left_command=ControlCommands.from_json(data['left_command']),
            control_command=ControlCommands.from_json(data['control_command']),
            swing_delay_same=data['swing_delay_same'],
            swing_delay_different=data['swing_delay_different'],
            swing_delay_any=data['swing_delay_any'],
            randomize_hits=data['randomize_hits'],
            skip_initial_hit=data['skip_initial_hit'],
            allow_both_players_to_hit=data['allow_both_players_to_hit'],
            max_beat_up_time=data['max_beat_up_time'],
            max_multiplier=data['max_multiplier'],
            prize1=BeatUpHandlerStruct.from_json(data['prize1']),
            prize2=BeatUpHandlerStruct.from_json(data['prize2']),
            prize3=BeatUpHandlerStruct.from_json(data['prize3']),
            hit_sound=data['hit_sound'],
        )

    def to_json(self) -> dict:
        return {
            'left_command': self.left_command.to_json(),
            'control_command': self.control_command.to_json(),
            'swing_delay_same': self.swing_delay_same,
            'swing_delay_different': self.swing_delay_different,
            'swing_delay_any': self.swing_delay_any,
            'randomize_hits': self.randomize_hits,
            'skip_initial_hit': self.skip_initial_hit,
            'allow_both_players_to_hit': self.allow_both_players_to_hit,
            'max_beat_up_time': self.max_beat_up_time,
            'max_multiplier': self.max_multiplier,
            'prize1': self.prize1.to_json(),
            'prize2': self.prize2.to_json(),
            'prize3': self.prize3.to_json(),
            'hit_sound': self.hit_sound,
        }


def _decode_left_command(data: typing.BinaryIO, property_size: int):
    return ControlCommands.from_stream(data, property_size, default_override={'command': enums.Command.Unknown8})


def _decode_control_command(data: typing.BinaryIO, property_size: int):
    return ControlCommands.from_stream(data, property_size, default_override={'command': enums.Command.Unknown9})


def _decode_swing_delay_same(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_delay_different(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_delay_any(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_randomize_hits(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_skip_initial_hit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_both_players_to_hit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_beat_up_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_prize1(data: typing.BinaryIO, property_size: int):
    return BeatUpHandlerStruct.from_stream(data, property_size)


def _decode_prize2(data: typing.BinaryIO, property_size: int):
    return BeatUpHandlerStruct.from_stream(data, property_size)


def _decode_prize3(data: typing.BinaryIO, property_size: int):
    return BeatUpHandlerStruct.from_stream(data, property_size)


def _decode_hit_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf6ae5d7c: ('left_command', _decode_left_command),
    0xd2fd4f74: ('control_command', _decode_control_command),
    0x35d40b67: ('swing_delay_same', _decode_swing_delay_same),
    0x82941381: ('swing_delay_different', _decode_swing_delay_different),
    0xe83776e6: ('swing_delay_any', _decode_swing_delay_any),
    0xf804d41c: ('randomize_hits', _decode_randomize_hits),
    0xe399b75a: ('skip_initial_hit', _decode_skip_initial_hit),
    0xdd31e55a: ('allow_both_players_to_hit', _decode_allow_both_players_to_hit),
    0xb5bbe88a: ('max_beat_up_time', _decode_max_beat_up_time),
    0xb12e58b8: ('max_multiplier', _decode_max_multiplier),
    0x4289b15b: ('prize1', _decode_prize1),
    0x351763ab: ('prize2', _decode_prize2),
    0xaeb22fc4: ('prize3', _decode_prize3),
    0x552db72c: ('hit_sound', _decode_hit_sound),
}
