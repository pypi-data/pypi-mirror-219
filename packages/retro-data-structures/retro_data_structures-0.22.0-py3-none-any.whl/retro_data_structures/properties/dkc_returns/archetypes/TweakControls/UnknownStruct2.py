# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.RevolutionControl import RevolutionControl


@dataclasses.dataclass()
class UnknownStruct2(BaseProperty):
    unknown_0x1d9b5cc1: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x56aaa727: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xdccb2caa: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x3c573a20: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    jump: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xc66160e6: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xc6bc4b19: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x79810b2b: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xd6787ebe: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x532087d5: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x3ed13a6a: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x7aa0b07c: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x1c204629: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x1996475f: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)

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

        data.write(b'\x1d\x9b\\\xc1')  # 0x1d9b5cc1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1d9b5cc1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"V\xaa\xa7'")  # 0x56aaa727
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x56aaa727.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdc\xcb,\xaa')  # 0xdccb2caa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xdccb2caa.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<W: ')  # 0x3c573a20
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x3c573a20.to_stream(data)
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

        data.write(b'\xc6a`\xe6')  # 0xc66160e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xc66160e6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xbcK\x19')  # 0xc6bc4b19
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xc6bc4b19.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\x81\x0b+')  # 0x79810b2b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x79810b2b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd6x~\xbe')  # 0xd6787ebe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xd6787ebe.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S \x87\xd5')  # 0x532087d5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x532087d5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>\xd1:j')  # 0x3ed13a6a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x3ed13a6a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'z\xa0\xb0|')  # 0x7aa0b07c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7aa0b07c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c F)')  # 0x1c204629
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1c204629.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\x96G_')  # 0x1996475f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1996475f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x1d9b5cc1=RevolutionControl.from_json(data['unknown_0x1d9b5cc1']),
            unknown_0x56aaa727=RevolutionControl.from_json(data['unknown_0x56aaa727']),
            unknown_0xdccb2caa=RevolutionControl.from_json(data['unknown_0xdccb2caa']),
            unknown_0x3c573a20=RevolutionControl.from_json(data['unknown_0x3c573a20']),
            jump=RevolutionControl.from_json(data['jump']),
            unknown_0xc66160e6=RevolutionControl.from_json(data['unknown_0xc66160e6']),
            unknown_0xc6bc4b19=RevolutionControl.from_json(data['unknown_0xc6bc4b19']),
            unknown_0x79810b2b=RevolutionControl.from_json(data['unknown_0x79810b2b']),
            unknown_0xd6787ebe=RevolutionControl.from_json(data['unknown_0xd6787ebe']),
            unknown_0x532087d5=RevolutionControl.from_json(data['unknown_0x532087d5']),
            unknown_0x3ed13a6a=RevolutionControl.from_json(data['unknown_0x3ed13a6a']),
            unknown_0x7aa0b07c=RevolutionControl.from_json(data['unknown_0x7aa0b07c']),
            unknown_0x1c204629=RevolutionControl.from_json(data['unknown_0x1c204629']),
            unknown_0x1996475f=RevolutionControl.from_json(data['unknown_0x1996475f']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x1d9b5cc1': self.unknown_0x1d9b5cc1.to_json(),
            'unknown_0x56aaa727': self.unknown_0x56aaa727.to_json(),
            'unknown_0xdccb2caa': self.unknown_0xdccb2caa.to_json(),
            'unknown_0x3c573a20': self.unknown_0x3c573a20.to_json(),
            'jump': self.jump.to_json(),
            'unknown_0xc66160e6': self.unknown_0xc66160e6.to_json(),
            'unknown_0xc6bc4b19': self.unknown_0xc6bc4b19.to_json(),
            'unknown_0x79810b2b': self.unknown_0x79810b2b.to_json(),
            'unknown_0xd6787ebe': self.unknown_0xd6787ebe.to_json(),
            'unknown_0x532087d5': self.unknown_0x532087d5.to_json(),
            'unknown_0x3ed13a6a': self.unknown_0x3ed13a6a.to_json(),
            'unknown_0x7aa0b07c': self.unknown_0x7aa0b07c.to_json(),
            'unknown_0x1c204629': self.unknown_0x1c204629.to_json(),
            'unknown_0x1996475f': self.unknown_0x1996475f.to_json(),
        }


def _decode_unknown_0x1d9b5cc1(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x56aaa727(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xdccb2caa(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x3c573a20(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_jump(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xc66160e6(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xc6bc4b19(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x79810b2b(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xd6787ebe(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x532087d5(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x3ed13a6a(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x7aa0b07c(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x1c204629(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x1996475f(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1d9b5cc1: ('unknown_0x1d9b5cc1', _decode_unknown_0x1d9b5cc1),
    0x56aaa727: ('unknown_0x56aaa727', _decode_unknown_0x56aaa727),
    0xdccb2caa: ('unknown_0xdccb2caa', _decode_unknown_0xdccb2caa),
    0x3c573a20: ('unknown_0x3c573a20', _decode_unknown_0x3c573a20),
    0x6b6fce63: ('jump', _decode_jump),
    0xc66160e6: ('unknown_0xc66160e6', _decode_unknown_0xc66160e6),
    0xc6bc4b19: ('unknown_0xc6bc4b19', _decode_unknown_0xc6bc4b19),
    0x79810b2b: ('unknown_0x79810b2b', _decode_unknown_0x79810b2b),
    0xd6787ebe: ('unknown_0xd6787ebe', _decode_unknown_0xd6787ebe),
    0x532087d5: ('unknown_0x532087d5', _decode_unknown_0x532087d5),
    0x3ed13a6a: ('unknown_0x3ed13a6a', _decode_unknown_0x3ed13a6a),
    0x7aa0b07c: ('unknown_0x7aa0b07c', _decode_unknown_0x7aa0b07c),
    0x1c204629: ('unknown_0x1c204629', _decode_unknown_0x1c204629),
    0x1996475f: ('unknown_0x1996475f', _decode_unknown_0x1996475f),
}
