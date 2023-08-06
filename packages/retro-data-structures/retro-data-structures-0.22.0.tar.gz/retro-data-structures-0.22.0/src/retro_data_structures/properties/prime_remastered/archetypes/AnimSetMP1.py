# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime_remastered.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime_remastered.core.PooledString import PooledString
import uuid


@dataclasses.dataclass()
class AnimSetMP1(BaseProperty):
    id: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    str1: PooledString = dataclasses.field(default_factory=PooledString)
    str2: PooledString = dataclasses.field(default_factory=PooledString)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack("<H", data.read(2))[0]
        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack("<LH", data.read(6))
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
        num_properties_offset = data.tell()
        data.write(b'\x00\x00')  # 0 properties
        num_properties_written = 0

        if self.id != default_override.get('id', default_asset_id):
            num_properties_written += 1
            data.write(b'\x85\xd8\x89\xa5')  # 0xa589d885
            data.write(b'\x10\x00')  # size
            data.write(self.id.bytes_le)

        if self.str1 != default_override.get('str1', PooledString()):
            num_properties_written += 1
            data.write(b'\xf0\xc0\xf0\xd6')  # 0xd6f0c0f0
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.str1.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack("<H", after - before - 2))
            data.seek(after)

        if self.str2 != default_override.get('str2', PooledString()):
            num_properties_written += 1
            data.write(b'\x01:\xc0\x87')  # 0x87c03a01
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.str2.to_stream(data)
            after = data.tell()
            data.seek(before)
            data.write(struct.pack("<H", after - before - 2))
            data.seek(after)

        if num_properties_written != 0:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack("<H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            id=uuid.UUID(data['id']),
            str1=PooledString.from_json(data['str1']),
            str2=PooledString.from_json(data['str2']),
        )

    def to_json(self) -> dict:
        return {
            'id': str(self.id),
            'str1': self.str1.to_json(),
            'str2': self.str2.to_json(),
        }


def _decode_id(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_str1(data: typing.BinaryIO, property_size: int):
    return PooledString.from_stream(data, property_size)


def _decode_str2(data: typing.BinaryIO, property_size: int):
    return PooledString.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa589d885: ('id', _decode_id),
    0xd6f0c0f0: ('str1', _decode_str1),
    0x87c03a01: ('str2', _decode_str2),
}
