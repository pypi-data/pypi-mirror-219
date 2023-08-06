# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.RevolutionControl.UnknownStruct2 import UnknownStruct2
from retro_data_structures.properties.corruption.archetypes.RevolutionControl.UnknownStruct3 import UnknownStruct3
from retro_data_structures.properties.corruption.archetypes.RevolutionControl.UnknownStruct4 import UnknownStruct4


@dataclasses.dataclass()
class UnknownStruct1(BaseProperty):
    unknown_0xe1c76bfb: enums.RevolutionControl_UnknownEnum2 = dataclasses.field(default=enums.RevolutionControl_UnknownEnum2.Unknown1)
    unknown_0x3d8010c2: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_0x9e8e5bf9: UnknownStruct3 = dataclasses.field(default_factory=UnknownStruct3)
    unknown_0x6d33ae8f: UnknownStruct4 = dataclasses.field(default_factory=UnknownStruct4)

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

        data.write(b'\xe1\xc7k\xfb')  # 0xe1c76bfb
        data.write(b'\x00\x04')  # size
        self.unknown_0xe1c76bfb.to_stream(data)

        data.write(b'=\x80\x10\xc2')  # 0x3d8010c2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x3d8010c2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\x8e[\xf9')  # 0x9e8e5bf9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x9e8e5bf9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'm3\xae\x8f')  # 0x6d33ae8f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x6d33ae8f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xe1c76bfb=enums.RevolutionControl_UnknownEnum2.from_json(data['unknown_0xe1c76bfb']),
            unknown_0x3d8010c2=UnknownStruct2.from_json(data['unknown_0x3d8010c2']),
            unknown_0x9e8e5bf9=UnknownStruct3.from_json(data['unknown_0x9e8e5bf9']),
            unknown_0x6d33ae8f=UnknownStruct4.from_json(data['unknown_0x6d33ae8f']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xe1c76bfb': self.unknown_0xe1c76bfb.to_json(),
            'unknown_0x3d8010c2': self.unknown_0x3d8010c2.to_json(),
            'unknown_0x9e8e5bf9': self.unknown_0x9e8e5bf9.to_json(),
            'unknown_0x6d33ae8f': self.unknown_0x6d33ae8f.to_json(),
        }


def _decode_unknown_0xe1c76bfb(data: typing.BinaryIO, property_size: int):
    return enums.RevolutionControl_UnknownEnum2.from_stream(data)


def _decode_unknown_0x3d8010c2(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_0x9e8e5bf9(data: typing.BinaryIO, property_size: int):
    return UnknownStruct3.from_stream(data, property_size)


def _decode_unknown_0x6d33ae8f(data: typing.BinaryIO, property_size: int):
    return UnknownStruct4.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe1c76bfb: ('unknown_0xe1c76bfb', _decode_unknown_0xe1c76bfb),
    0x3d8010c2: ('unknown_0x3d8010c2', _decode_unknown_0x3d8010c2),
    0x9e8e5bf9: ('unknown_0x9e8e5bf9', _decode_unknown_0x9e8e5bf9),
    0x6d33ae8f: ('unknown_0x6d33ae8f', _decode_unknown_0x6d33ae8f),
}
