# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct142 import UnknownStruct142


@dataclasses.dataclass()
class UnknownStruct143(BaseProperty):
    unknown: int = dataclasses.field(default=1138461727)  # Choice
    timer: float = dataclasses.field(default=0.0)
    unknown_struct142: UnknownStruct142 = dataclasses.field(default_factory=UnknownStruct142)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'c\xbe R')  # 0x63be2052
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown))

        data.write(b'\x87GU.')  # 0x8747552e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.timer))

        data.write(b'q\xe9\xd1\xa1')  # 0x71e9d1a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct142.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            timer=data['timer'],
            unknown_struct142=UnknownStruct142.from_json(data['unknown_struct142']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'timer': self.timer,
            'unknown_struct142': self.unknown_struct142.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct142(data: typing.BinaryIO, property_size: int):
    return UnknownStruct142.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x63be2052: ('unknown', _decode_unknown),
    0x8747552e: ('timer', _decode_timer),
    0x71e9d1a1: ('unknown_struct142', _decode_unknown_struct142),
}
