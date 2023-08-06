# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl


@dataclasses.dataclass()
class UnknownStruct1(BaseProperty):
    unknown_0x10699c6f: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x50de5441: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xa9a26569: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0x6f71adf7: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x10i\x9co')  # 0x10699c6f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x10699c6f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\xdeTA')  # 0x50de5441
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x50de5441.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa9\xa2ei')  # 0xa9a26569
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xa9a26569.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'oq\xad\xf7')  # 0x6f71adf7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x6f71adf7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x10699c6f=RevolutionControl.from_json(data['unknown_0x10699c6f']),
            unknown_0x50de5441=RevolutionControl.from_json(data['unknown_0x50de5441']),
            unknown_0xa9a26569=RevolutionControl.from_json(data['unknown_0xa9a26569']),
            unknown_0x6f71adf7=RevolutionControl.from_json(data['unknown_0x6f71adf7']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x10699c6f': self.unknown_0x10699c6f.to_json(),
            'unknown_0x50de5441': self.unknown_0x50de5441.to_json(),
            'unknown_0xa9a26569': self.unknown_0xa9a26569.to_json(),
            'unknown_0x6f71adf7': self.unknown_0x6f71adf7.to_json(),
        }


def _decode_unknown_0x10699c6f(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x50de5441(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xa9a26569(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0x6f71adf7(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x10699c6f: ('unknown_0x10699c6f', _decode_unknown_0x10699c6f),
    0x50de5441: ('unknown_0x50de5441', _decode_unknown_0x50de5441),
    0xa9a26569: ('unknown_0xa9a26569', _decode_unknown_0xa9a26569),
    0x6f71adf7: ('unknown_0x6f71adf7', _decode_unknown_0x6f71adf7),
}
