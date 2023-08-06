# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime_remastered as enums
from retro_data_structures.properties.prime_remastered.core.AssetId import AssetId, default_asset_id
import uuid


@dataclasses.dataclass()
class HUDMemoMP1(BaseProperty):
    unk_int_1: int = dataclasses.field(default=1077936128)
    memo_type: enums.MemoType = dataclasses.field(default=enums.MemoType.StatusMessage)
    guid_1: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    unk_bool_1: bool = dataclasses.field(default=True)
    unk_int_3: int = dataclasses.field(default=0)

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

        if self.unk_int_1 != default_override.get('unk_int_1', 1077936128):
            num_properties_written += 1
            data.write(b'\xd0\xb4)\xf4')  # 0xf429b4d0
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<l', self.unk_int_1))

        if self.memo_type != default_override.get('memo_type', enums.MemoType.StatusMessage):
            num_properties_written += 1
            data.write(b'\xfd=\x1f\x1e')  # 0x1e1f3dfd
            data.write(b'\x04\x00')  # size
            self.memo_type.to_stream(data)

        if self.guid_1 != default_override.get('guid_1', default_asset_id):
            num_properties_written += 1
            data.write(b'\x18\xd1\x86\xd7')  # 0xd786d118
            data.write(b'\x10\x00')  # size
            data.write(self.guid_1.bytes_le)

        if self.unk_bool_1 != default_override.get('unk_bool_1', True):
            num_properties_written += 1
            data.write(b'\xcf\xc9<\xe7')  # 0xe73cc9cf
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unk_bool_1))

        if self.unk_int_3 != default_override.get('unk_int_3', 0):
            num_properties_written += 1
            data.write(b'\x95s\xe1V')  # 0x56e17395
            data.write(b'\x04\x00')  # size
            data.write(struct.pack('<l', self.unk_int_3))

        if num_properties_written != 0:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack("<H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unk_int_1=data['unk_int_1'],
            memo_type=enums.MemoType.from_json(data['memo_type']),
            guid_1=uuid.UUID(data['guid_1']),
            unk_bool_1=data['unk_bool_1'],
            unk_int_3=data['unk_int_3'],
        )

    def to_json(self) -> dict:
        return {
            'unk_int_1': self.unk_int_1,
            'memo_type': self.memo_type.to_json(),
            'guid_1': str(self.guid_1),
            'unk_bool_1': self.unk_bool_1,
            'unk_int_3': self.unk_int_3,
        }


def _decode_unk_int_1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<l', data.read(4))[0]


def _decode_memo_type(data: typing.BinaryIO, property_size: int):
    return enums.MemoType.from_stream(data)


def _decode_guid_1(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_unk_bool_1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_unk_int_3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf429b4d0: ('unk_int_1', _decode_unk_int_1),
    0x1e1f3dfd: ('memo_type', _decode_memo_type),
    0xd786d118: ('guid_1', _decode_guid_1),
    0xe73cc9cf: ('unk_bool_1', _decode_unk_bool_1),
    0x56e17395: ('unk_int_3', _decode_unk_int_3),
}
