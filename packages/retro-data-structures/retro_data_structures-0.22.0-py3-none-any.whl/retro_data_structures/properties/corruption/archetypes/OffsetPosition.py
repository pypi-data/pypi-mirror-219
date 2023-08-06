# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.OffsetInterpolant import OffsetInterpolant


@dataclasses.dataclass()
class OffsetPosition(BaseProperty):
    offset_type: enums.OffsetType = dataclasses.field(default=enums.OffsetType.Unknown1)
    offset: OffsetInterpolant = dataclasses.field(default_factory=OffsetInterpolant)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'p\xc7\x8c>')  # 0x70c78c3e
        data.write(b'\x00\x04')  # size
        self.offset_type.to_stream(data)

        data.write(b'7i\xa2\t')  # 0x3769a209
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            offset_type=enums.OffsetType.from_json(data['offset_type']),
            offset=OffsetInterpolant.from_json(data['offset']),
        )

    def to_json(self) -> dict:
        return {
            'offset_type': self.offset_type.to_json(),
            'offset': self.offset.to_json(),
        }


def _decode_offset_type(data: typing.BinaryIO, property_size: int):
    return enums.OffsetType.from_stream(data)


def _decode_offset(data: typing.BinaryIO, property_size: int):
    return OffsetInterpolant.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x70c78c3e: ('offset_type', _decode_offset_type),
    0x3769a209: ('offset', _decode_offset),
}
