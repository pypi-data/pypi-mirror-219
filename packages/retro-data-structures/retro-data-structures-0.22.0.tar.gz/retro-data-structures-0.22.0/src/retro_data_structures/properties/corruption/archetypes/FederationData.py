# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.UnknownStruct29 import UnknownStruct29


@dataclasses.dataclass()
class FederationData(BaseProperty):
    can_blink: bool = dataclasses.field(default=True)
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29)
    unknown: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\\tw\x10')  # 0x5c747710
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_blink))

        data.write(b'nX\xd7\x14')  # 0x6e58d714
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0f1\xfd\xae')  # 0xf31fdae
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            can_blink=data['can_blink'],
            unknown_struct29=UnknownStruct29.from_json(data['unknown_struct29']),
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'can_blink': self.can_blink,
            'unknown_struct29': self.unknown_struct29.to_json(),
            'unknown': self.unknown,
        }


def _decode_can_blink(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct29(data: typing.BinaryIO, property_size: int):
    return UnknownStruct29.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5c747710: ('can_blink', _decode_can_blink),
    0x6e58d714: ('unknown_struct29', _decode_unknown_struct29),
    0xf31fdae: ('unknown', _decode_unknown),
}
