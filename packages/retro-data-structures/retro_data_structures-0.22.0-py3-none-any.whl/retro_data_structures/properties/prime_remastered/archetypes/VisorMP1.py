# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.prime_remastered as enums


@dataclasses.dataclass()
class VisorMP1(BaseProperty):
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: bool = dataclasses.field(default=False)
    unknown_3: bool = dataclasses.field(default=False)
    visor_flags: enums.VisorFlags = dataclasses.field(default=enums.VisorFlags(0))

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME_REMASTER

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack("<H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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

        if self.unknown_1 != default_override.get('unknown_1', False):
            num_properties_written += 1
            data.write(b'\x15P\xf7\x82')  # 0x82f75015
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unknown_1))

        if self.unknown_2 != default_override.get('unknown_2', False):
            num_properties_written += 1
            data.write(b'\x12\xfcIQ')  # 0x5149fc12
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unknown_2))

        if self.unknown_3 != default_override.get('unknown_3', False):
            num_properties_written += 1
            data.write(b'P\xca\x82\x13')  # 0x1382ca50
            data.write(b'\x01\x00')  # size
            data.write(struct.pack('<?', self.unknown_3))

        if self.visor_flags != default_override.get('visor_flags', enums.VisorFlags(0)):
            num_properties_written += 1
            data.write(b'\xa5V\x8aR')  # 0x528a56a5
            data.write(b'\x04\x00')  # size
            self.visor_flags.to_stream(data)

        if num_properties_written != 0:
            struct_end_offset = data.tell()
            data.seek(num_properties_offset)
            data.write(struct.pack("<H", num_properties_written))
            data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            visor_flags=enums.VisorFlags.from_json(data['visor_flags']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'visor_flags': self.visor_flags.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x82f75015, 0x5149fc12, 0x1382ca50, 0x528a56a5)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[VisorMP1]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('<LH?LH?LH?LHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(31))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return VisorMP1(
        dec[2],
        dec[5],
        dec[8],
        enums.VisorFlags(dec[11]),
    )


def _decode_unknown_1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_unknown_2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_unknown_3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('<?', data.read(1))[0]


def _decode_visor_flags(data: typing.BinaryIO, property_size: int):
    return enums.VisorFlags.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x82f75015: ('unknown_1', _decode_unknown_1),
    0x5149fc12: ('unknown_2', _decode_unknown_2),
    0x1382ca50: ('unknown_3', _decode_unknown_3),
    0x528a56a5: ('visor_flags', _decode_visor_flags),
}
