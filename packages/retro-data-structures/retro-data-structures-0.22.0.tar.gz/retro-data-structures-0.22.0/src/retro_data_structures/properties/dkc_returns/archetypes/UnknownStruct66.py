# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct66(BaseProperty):
    unknown: bool = dataclasses.field(default=False)
    debug_name: str = dataclasses.field(default='')
    max_value: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x18\xc79j')  # 0x18c7396a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\xbd\x0b~\xde')  # 0xbd0b7ede
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.debug_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'l\x84\xc5\x88')  # 0x6c84c588
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_value))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            debug_name=data['debug_name'],
            max_value=data['max_value'],
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'debug_name': self.debug_name,
            'max_value': self.max_value,
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_debug_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_max_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x18c7396a: ('unknown', _decode_unknown),
    0xbd0b7ede: ('debug_name', _decode_debug_name),
    0x6c84c588: ('max_value', _decode_max_value),
}
