# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class PlayerMovementControls(BaseProperty):
    forward: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    backward: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    turn_left: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    turn_right: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xf86e276b: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xd0106d0d: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    strafe_left: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    strafe_right: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    jump: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    lean_left: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    lean_right: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x4058d24a: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x466568f7: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x1580c929: Spline = dataclasses.field(default_factory=Spline)
    unknown_0xff5cc926: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\x04\x12J\t')  # 0x4124a09
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forward.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xad\xe0\x10;')  # 0xade0103b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.backward.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Am\x1c\xc1')  # 0x416d1cc1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.turn_left.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6\xaa$\xc0')  # 0xe6aa24c0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.turn_right.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\xf8n'k")  # 0xf86e276b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xf86e276b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd0\x10m\r')  # 0xd0106d0d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xd0106d0d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'z\xdf\x18\xcd')  # 0x7adf18cd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.strafe_left.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\xef'\xda\xef")  # 0xef27daef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.strafe_right.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'ko\xcec')  # 0x6b6fce63
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'=\x8dhT')  # 0x3d8d6854
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lean_left.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'f\xb3\xa3\x7f')  # 0x66b3a37f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.lean_right.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@X\xd2J')  # 0x4058d24a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x4058d24a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Feh\xf7')  # 0x466568f7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x466568f7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x80\xc9)')  # 0x1580c929
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1580c929.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xff\\\xc9&')  # 0xff5cc926
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xff5cc926.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            forward=RevolutionControl.from_json(data['forward']),
            backward=RevolutionControl.from_json(data['backward']),
            turn_left=RevolutionControl.from_json(data['turn_left']),
            turn_right=RevolutionControl.from_json(data['turn_right']),
            unknown_0xf86e276b=RevolutionControl.from_json(data['unknown_0xf86e276b']),
            unknown_0xd0106d0d=RevolutionControl.from_json(data['unknown_0xd0106d0d']),
            strafe_left=RevolutionControl.from_json(data['strafe_left']),
            strafe_right=RevolutionControl.from_json(data['strafe_right']),
            jump=RevolutionControl.from_json(data['jump']),
            lean_left=RevolutionControl.from_json(data['lean_left']),
            lean_right=RevolutionControl.from_json(data['lean_right']),
            unknown_0x4058d24a=Spline.from_json(data['unknown_0x4058d24a']),
            unknown_0x466568f7=Spline.from_json(data['unknown_0x466568f7']),
            unknown_0x1580c929=Spline.from_json(data['unknown_0x1580c929']),
            unknown_0xff5cc926=Spline.from_json(data['unknown_0xff5cc926']),
        )

    def to_json(self) -> dict:
        return {
            'forward': self.forward.to_json(),
            'backward': self.backward.to_json(),
            'turn_left': self.turn_left.to_json(),
            'turn_right': self.turn_right.to_json(),
            'unknown_0xf86e276b': self.unknown_0xf86e276b.to_json(),
            'unknown_0xd0106d0d': self.unknown_0xd0106d0d.to_json(),
            'strafe_left': self.strafe_left.to_json(),
            'strafe_right': self.strafe_right.to_json(),
            'jump': self.jump.to_json(),
            'lean_left': self.lean_left.to_json(),
            'lean_right': self.lean_right.to_json(),
            'unknown_0x4058d24a': self.unknown_0x4058d24a.to_json(),
            'unknown_0x466568f7': self.unknown_0x466568f7.to_json(),
            'unknown_0x1580c929': self.unknown_0x1580c929.to_json(),
            'unknown_0xff5cc926': self.unknown_0xff5cc926.to_json(),
        }


def _decode_forward(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_backward(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_turn_left(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_turn_right(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xf86e276b(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xd0106d0d(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_strafe_left(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_strafe_right(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_jump(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_lean_left(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_lean_right(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x4058d24a(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x466568f7(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x1580c929(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0xff5cc926(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4124a09: ('forward', _decode_forward),
    0xade0103b: ('backward', _decode_backward),
    0x416d1cc1: ('turn_left', _decode_turn_left),
    0xe6aa24c0: ('turn_right', _decode_turn_right),
    0xf86e276b: ('unknown_0xf86e276b', _decode_unknown_0xf86e276b),
    0xd0106d0d: ('unknown_0xd0106d0d', _decode_unknown_0xd0106d0d),
    0x7adf18cd: ('strafe_left', _decode_strafe_left),
    0xef27daef: ('strafe_right', _decode_strafe_right),
    0x6b6fce63: ('jump', _decode_jump),
    0x3d8d6854: ('lean_left', _decode_lean_left),
    0x66b3a37f: ('lean_right', _decode_lean_right),
    0x4058d24a: ('unknown_0x4058d24a', _decode_unknown_0x4058d24a),
    0x466568f7: ('unknown_0x466568f7', _decode_unknown_0x466568f7),
    0x1580c929: ('unknown_0x1580c929', _decode_unknown_0x1580c929),
    0xff5cc926: ('unknown_0xff5cc926', _decode_unknown_0xff5cc926),
}
