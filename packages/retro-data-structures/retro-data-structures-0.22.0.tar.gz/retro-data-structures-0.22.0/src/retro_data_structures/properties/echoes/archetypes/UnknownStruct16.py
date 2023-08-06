# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct16(BaseProperty):
    unknown_0x7ee77018: float = dataclasses.field(default=50.0)
    unknown_0xbfb7ca5c: float = dataclasses.field(default=100.0)
    unknown_0x1e2debc6: float = dataclasses.field(default=100.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'~\xe7p\x18')  # 0x7ee77018
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7ee77018))

        data.write(b'\xbf\xb7\xca\\')  # 0xbfb7ca5c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbfb7ca5c))

        data.write(b'\x1e-\xeb\xc6')  # 0x1e2debc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1e2debc6))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x7ee77018=data['unknown_0x7ee77018'],
            unknown_0xbfb7ca5c=data['unknown_0xbfb7ca5c'],
            unknown_0x1e2debc6=data['unknown_0x1e2debc6'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x7ee77018': self.unknown_0x7ee77018,
            'unknown_0xbfb7ca5c': self.unknown_0xbfb7ca5c,
            'unknown_0x1e2debc6': self.unknown_0x1e2debc6,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x7ee77018, 0xbfb7ca5c, 0x1e2debc6)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct16]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct16(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_unknown_0x7ee77018(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbfb7ca5c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1e2debc6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7ee77018: ('unknown_0x7ee77018', _decode_unknown_0x7ee77018),
    0xbfb7ca5c: ('unknown_0xbfb7ca5c', _decode_unknown_0xbfb7ca5c),
    0x1e2debc6: ('unknown_0x1e2debc6', _decode_unknown_0x1e2debc6),
}
