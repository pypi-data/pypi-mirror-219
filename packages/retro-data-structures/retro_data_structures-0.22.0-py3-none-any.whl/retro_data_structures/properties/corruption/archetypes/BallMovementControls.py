# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl


@dataclasses.dataclass()
class BallMovementControls(BaseProperty):
    roll_forward: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    roll_backward: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    roll_left: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    roll_right: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    boost_ball: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    spider_ball: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    screw_attack: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    spring_ball: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xb4\xf2\x96@')  # 0xb4f29640
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.roll_forward.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2P\t\xd3')  # 0xa25009d3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.roll_backward.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9c\xba\x81{')  # 0x9cba817b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.roll_left.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcd\xc3\xa9\xcf')  # 0xcdc3a9cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.roll_right.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/\x0e\x02v')  # 0x2f0e0276
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.boost_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9a\x974T')  # 0x9a973454
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spider_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\x9f`\xa3')  # 0x8b9f60a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.screw_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'uj6\x82')  # 0x756a3682
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spring_ball.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            roll_forward=RevolutionControl.from_json(data['roll_forward']),
            roll_backward=RevolutionControl.from_json(data['roll_backward']),
            roll_left=RevolutionControl.from_json(data['roll_left']),
            roll_right=RevolutionControl.from_json(data['roll_right']),
            boost_ball=RevolutionControl.from_json(data['boost_ball']),
            spider_ball=RevolutionControl.from_json(data['spider_ball']),
            screw_attack=RevolutionControl.from_json(data['screw_attack']),
            spring_ball=RevolutionControl.from_json(data['spring_ball']),
        )

    def to_json(self) -> dict:
        return {
            'roll_forward': self.roll_forward.to_json(),
            'roll_backward': self.roll_backward.to_json(),
            'roll_left': self.roll_left.to_json(),
            'roll_right': self.roll_right.to_json(),
            'boost_ball': self.boost_ball.to_json(),
            'spider_ball': self.spider_ball.to_json(),
            'screw_attack': self.screw_attack.to_json(),
            'spring_ball': self.spring_ball.to_json(),
        }


def _decode_roll_forward(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_roll_backward(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_roll_left(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_roll_right(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_boost_ball(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_spider_ball(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_screw_attack(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_spring_ball(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb4f29640: ('roll_forward', _decode_roll_forward),
    0xa25009d3: ('roll_backward', _decode_roll_backward),
    0x9cba817b: ('roll_left', _decode_roll_left),
    0xcdc3a9cf: ('roll_right', _decode_roll_right),
    0x2f0e0276: ('boost_ball', _decode_boost_ball),
    0x9a973454: ('spider_ball', _decode_spider_ball),
    0x8b9f60a3: ('screw_attack', _decode_screw_attack),
    0x756a3682: ('spring_ball', _decode_spring_ball),
}
