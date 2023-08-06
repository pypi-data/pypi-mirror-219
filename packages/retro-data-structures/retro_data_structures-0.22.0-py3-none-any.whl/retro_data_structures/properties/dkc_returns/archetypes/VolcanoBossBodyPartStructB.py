# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct285 import UnknownStruct285
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct286 import UnknownStruct286


@dataclasses.dataclass()
class VolcanoBossBodyPartStructB(BaseProperty):
    unknown_struct285: UnknownStruct285 = dataclasses.field(default_factory=UnknownStruct285)
    unknown_struct286: UnknownStruct286 = dataclasses.field(default_factory=UnknownStruct286)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xcd\x85\xb2\x9d')  # 0xcd85b29d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct285.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\x18kj')  # 0x50186b6a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct286.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct285=UnknownStruct285.from_json(data['unknown_struct285']),
            unknown_struct286=UnknownStruct286.from_json(data['unknown_struct286']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct285': self.unknown_struct285.to_json(),
            'unknown_struct286': self.unknown_struct286.to_json(),
        }


def _decode_unknown_struct285(data: typing.BinaryIO, property_size: int):
    return UnknownStruct285.from_stream(data, property_size)


def _decode_unknown_struct286(data: typing.BinaryIO, property_size: int):
    return UnknownStruct286.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcd85b29d: ('unknown_struct285', _decode_unknown_struct285),
    0x50186b6a: ('unknown_struct286', _decode_unknown_struct286),
}
