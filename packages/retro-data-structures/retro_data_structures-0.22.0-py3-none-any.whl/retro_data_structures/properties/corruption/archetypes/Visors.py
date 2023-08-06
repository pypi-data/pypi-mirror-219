# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Visors(BaseProperty):
    scan_visor: bool = dataclasses.field(default=False)
    command_visor: bool = dataclasses.field(default=False)
    x_ray_visor: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'Xj\x8fu')  # 0x586a8f75
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.scan_visor))

        data.write(b'\x04\xfc\xa2\xa9')  # 0x4fca2a9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.command_visor))

        data.write(b'\xf5]\xd0,')  # 0xf55dd02c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.x_ray_visor))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scan_visor=data['scan_visor'],
            command_visor=data['command_visor'],
            x_ray_visor=data['x_ray_visor'],
        )

    def to_json(self) -> dict:
        return {
            'scan_visor': self.scan_visor,
            'command_visor': self.command_visor,
            'x_ray_visor': self.x_ray_visor,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x586a8f75, 0x4fca2a9, 0xf55dd02c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Visors]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(21))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return Visors(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_scan_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_command_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_x_ray_visor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x586a8f75: ('scan_visor', _decode_scan_visor),
    0x4fca2a9: ('command_visor', _decode_command_visor),
    0xf55dd02c: ('x_ray_visor', _decode_x_ray_visor),
}
