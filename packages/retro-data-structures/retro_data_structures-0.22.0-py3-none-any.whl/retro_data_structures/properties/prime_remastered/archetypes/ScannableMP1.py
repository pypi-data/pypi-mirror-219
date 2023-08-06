# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime_remastered.core.AssetId import AssetId, default_asset_id
import uuid


@dataclasses.dataclass()
class ScannableMP1(BaseProperty):
    scan_file: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    unk_bool: bool = dataclasses.field(default=False)

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
        data.write(b'\x01\x00')  # 1 properties
        num_properties_written = 1

        data.write(b'\xb4\xe2s\x1a')  # 0x1a73e2b4
        data.write(b'\x10\x00')  # size
        data.write(self.scan_file.bytes_le)

        if self.unk_bool != default_override.get('unk_bool', False):
            num_properties_written += 1
            data.write(b'9@&\x05')  # 0x5264039
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unk_bool))

        if num_properties_written != 1:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack("<H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scan_file=uuid.UUID(data['scan_file']),
            unk_bool=data['unk_bool'],
        )

    def to_json(self) -> dict:
        return {
            'scan_file': str(self.scan_file),
            'unk_bool': self.unk_bool,
        }


def _decode_scan_file(data: typing.BinaryIO, property_size: int):
    return uuid.UUID(bytes_le=data.read(16))


def _decode_unk_bool(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1a73e2b4: ('scan_file', _decode_scan_file),
    0x5264039: ('unk_bool', _decode_unk_bool),
}
