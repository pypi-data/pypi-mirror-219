# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.echoes as enums


@dataclasses.dataclass()
class VisorParameters(BaseProperty):
    scan_through: bool = dataclasses.field(default=False)
    visor_flags: enums.VisorFlags = dataclasses.field(default=enums.VisorFlags(15))

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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

        data.write(b'\xfe\x9d\xc2f')  # 0xfe9dc266
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scan_through))

        data.write(b'\xca\x19\xe8\xc6')  # 0xca19e8c6
        data.write(b'\x00\x04')  # size
        self.visor_flags.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scan_through=data['scan_through'],
            visor_flags=enums.VisorFlags.from_json(data['visor_flags']),
        )

    def to_json(self) -> dict:
        return {
            'scan_through': self.scan_through,
            'visor_flags': self.visor_flags.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0xfe9dc266, 0xca19e8c6)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[VisorParameters]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(17))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return VisorParameters(
        dec[2],
        enums.VisorFlags(dec[5]),
    )


def _decode_scan_through(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_visor_flags(data: typing.BinaryIO, property_size: int):
    return enums.VisorFlags.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfe9dc266: ('scan_through', _decode_scan_through),
    0xca19e8c6: ('visor_flags', _decode_visor_flags),
}
