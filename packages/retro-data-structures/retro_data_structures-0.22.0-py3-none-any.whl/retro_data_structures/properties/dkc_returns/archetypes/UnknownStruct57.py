# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct278 import UnknownStruct278


@dataclasses.dataclass()
class UnknownStruct57(BaseProperty):
    unknown_struct278: UnknownStruct278 = dataclasses.field(default_factory=UnknownStruct278)

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
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\x18X\xcb\xdb')  # 0x1858cbdb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct278.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct278=UnknownStruct278.from_json(data['unknown_struct278']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct278': self.unknown_struct278.to_json(),
        }


def _decode_unknown_struct278(data: typing.BinaryIO, property_size: int):
    return UnknownStruct278.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1858cbdb: ('unknown_struct278', _decode_unknown_struct278),
}
