# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct7 import UnknownStruct7


@dataclasses.dataclass()
class UnknownStruct8(BaseProperty):
    num_attachments: int = dataclasses.field(default=0)
    unknown: bool = dataclasses.field(default=False)
    attachment1: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7)
    attachment2: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7)
    attachment3: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xc2\xadW5')  # 0xc2ad5735
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_attachments))

        data.write(b'cQ\xa0I')  # 0x6351a049
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\xda\xa9\xd4\xbe')  # 0xdaa9d4be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachment1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3a`L')  # 0xf361604c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachment2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\t\xf1\xdd')  # 0x5d09f1dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachment3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            num_attachments=data['num_attachments'],
            unknown=data['unknown'],
            attachment1=UnknownStruct7.from_json(data['attachment1']),
            attachment2=UnknownStruct7.from_json(data['attachment2']),
            attachment3=UnknownStruct7.from_json(data['attachment3']),
        )

    def to_json(self) -> dict:
        return {
            'num_attachments': self.num_attachments,
            'unknown': self.unknown,
            'attachment1': self.attachment1.to_json(),
            'attachment2': self.attachment2.to_json(),
            'attachment3': self.attachment3.to_json(),
        }


def _decode_num_attachments(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_attachment1(data: typing.BinaryIO, property_size: int):
    return UnknownStruct7.from_stream(data, property_size)


def _decode_attachment2(data: typing.BinaryIO, property_size: int):
    return UnknownStruct7.from_stream(data, property_size)


def _decode_attachment3(data: typing.BinaryIO, property_size: int):
    return UnknownStruct7.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc2ad5735: ('num_attachments', _decode_num_attachments),
    0x6351a049: ('unknown', _decode_unknown),
    0xdaa9d4be: ('attachment1', _decode_attachment1),
    0xf361604c: ('attachment2', _decode_attachment2),
    0x5d09f1dd: ('attachment3', _decode_attachment3),
}
