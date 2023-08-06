# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.RevolutionControl import RevolutionControl


@dataclasses.dataclass()
class MiscControls(BaseProperty):
    unknown_0x439f3678: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xbf8653ed: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x9ca552b4: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x88b5fd4d: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xb63c1d0b: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x1d88ee3e: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    skip_cinematic: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xd9cf3e97: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xb7346005: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x76299df7: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x2c2b2b0e: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'C\x9f6x')  # 0x439f3678
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x439f3678.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\x86S\xed')  # 0xbf8653ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xbf8653ed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9c\xa5R\xb4')  # 0x9ca552b4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x9ca552b4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88\xb5\xfdM')  # 0x88b5fd4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x88b5fd4d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6<\x1d\x0b')  # 0xb63c1d0b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb63c1d0b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d\x88\xee>')  # 0x1d88ee3e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x1d88ee3e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\xa3\xe0}')  # 0x19a3e07d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.skip_cinematic.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd9\xcf>\x97')  # 0xd9cf3e97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xd9cf3e97.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb74`\x05')  # 0xb7346005
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb7346005.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v)\x9d\xf7')  # 0x76299df7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x76299df7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',++\x0e')  # 0x2c2b2b0e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x2c2b2b0e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x439f3678=RevolutionControl.from_json(data['unknown_0x439f3678']),
            unknown_0xbf8653ed=RevolutionControl.from_json(data['unknown_0xbf8653ed']),
            unknown_0x9ca552b4=RevolutionControl.from_json(data['unknown_0x9ca552b4']),
            unknown_0x88b5fd4d=RevolutionControl.from_json(data['unknown_0x88b5fd4d']),
            unknown_0xb63c1d0b=RevolutionControl.from_json(data['unknown_0xb63c1d0b']),
            unknown_0x1d88ee3e=RevolutionControl.from_json(data['unknown_0x1d88ee3e']),
            skip_cinematic=RevolutionControl.from_json(data['skip_cinematic']),
            unknown_0xd9cf3e97=RevolutionControl.from_json(data['unknown_0xd9cf3e97']),
            unknown_0xb7346005=RevolutionControl.from_json(data['unknown_0xb7346005']),
            unknown_0x76299df7=RevolutionControl.from_json(data['unknown_0x76299df7']),
            unknown_0x2c2b2b0e=RevolutionControl.from_json(data['unknown_0x2c2b2b0e']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x439f3678': self.unknown_0x439f3678.to_json(),
            'unknown_0xbf8653ed': self.unknown_0xbf8653ed.to_json(),
            'unknown_0x9ca552b4': self.unknown_0x9ca552b4.to_json(),
            'unknown_0x88b5fd4d': self.unknown_0x88b5fd4d.to_json(),
            'unknown_0xb63c1d0b': self.unknown_0xb63c1d0b.to_json(),
            'unknown_0x1d88ee3e': self.unknown_0x1d88ee3e.to_json(),
            'skip_cinematic': self.skip_cinematic.to_json(),
            'unknown_0xd9cf3e97': self.unknown_0xd9cf3e97.to_json(),
            'unknown_0xb7346005': self.unknown_0xb7346005.to_json(),
            'unknown_0x76299df7': self.unknown_0x76299df7.to_json(),
            'unknown_0x2c2b2b0e': self.unknown_0x2c2b2b0e.to_json(),
        }


def _decode_unknown_0x439f3678(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xbf8653ed(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x9ca552b4(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x88b5fd4d(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xb63c1d0b(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x1d88ee3e(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_skip_cinematic(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xd9cf3e97(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xb7346005(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x76299df7(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x2c2b2b0e(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x439f3678: ('unknown_0x439f3678', _decode_unknown_0x439f3678),
    0xbf8653ed: ('unknown_0xbf8653ed', _decode_unknown_0xbf8653ed),
    0x9ca552b4: ('unknown_0x9ca552b4', _decode_unknown_0x9ca552b4),
    0x88b5fd4d: ('unknown_0x88b5fd4d', _decode_unknown_0x88b5fd4d),
    0xb63c1d0b: ('unknown_0xb63c1d0b', _decode_unknown_0xb63c1d0b),
    0x1d88ee3e: ('unknown_0x1d88ee3e', _decode_unknown_0x1d88ee3e),
    0x19a3e07d: ('skip_cinematic', _decode_skip_cinematic),
    0xd9cf3e97: ('unknown_0xd9cf3e97', _decode_unknown_0xd9cf3e97),
    0xb7346005: ('unknown_0xb7346005', _decode_unknown_0xb7346005),
    0x76299df7: ('unknown_0x76299df7', _decode_unknown_0x76299df7),
    0x2c2b2b0e: ('unknown_0x2c2b2b0e', _decode_unknown_0x2c2b2b0e),
}
