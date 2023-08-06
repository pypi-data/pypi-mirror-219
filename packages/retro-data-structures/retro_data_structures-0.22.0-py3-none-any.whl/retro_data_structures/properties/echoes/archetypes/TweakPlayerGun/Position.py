# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Position(BaseProperty):
    unknown: float = dataclasses.field(default=0.30000001192092896)
    x: float = dataclasses.field(default=0.25)
    y: float = dataclasses.field(default=0.30000001192092896)
    z: float = dataclasses.field(default=-0.3499999940395355)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x15G\xd7{')  # 0x1547d77b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xa1g}N')  # 0xa1677d4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.x))

        data.write(b'j;\xae\xeb')  # 0x6a3baeeb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.y))

        data.write(b'\xec\xaf\xdcE')  # 0xecafdc45
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.z))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            x=data['x'],
            y=data['y'],
            z=data['z'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x1547d77b, 0xa1677d4e, 0x6a3baeeb, 0xecafdc45)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Position]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return Position(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_z(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1547d77b: ('unknown', _decode_unknown),
    0xa1677d4e: ('x', _decode_x),
    0x6a3baeeb: ('y', _decode_y),
    0xecafdc45: ('z', _decode_z),
}
