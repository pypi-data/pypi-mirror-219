# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct232(BaseProperty):
    unknown_0x4cd75db8: float = dataclasses.field(default=3.0)
    unknown_0xefee802b: float = dataclasses.field(default=2.0)
    unknown_0x50ad6480: str = dataclasses.field(default='')

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

        data.write(b'L\xd7]\xb8')  # 0x4cd75db8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4cd75db8))

        data.write(b'\xef\xee\x80+')  # 0xefee802b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xefee802b))

        data.write(b'P\xadd\x80')  # 0x50ad6480
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x50ad6480.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x4cd75db8=data['unknown_0x4cd75db8'],
            unknown_0xefee802b=data['unknown_0xefee802b'],
            unknown_0x50ad6480=data['unknown_0x50ad6480'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x4cd75db8': self.unknown_0x4cd75db8,
            'unknown_0xefee802b': self.unknown_0xefee802b,
            'unknown_0x50ad6480': self.unknown_0x50ad6480,
        }


def _decode_unknown_0x4cd75db8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xefee802b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x50ad6480(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4cd75db8: ('unknown_0x4cd75db8', _decode_unknown_0x4cd75db8),
    0xefee802b: ('unknown_0xefee802b', _decode_unknown_0xefee802b),
    0x50ad6480: ('unknown_0x50ad6480', _decode_unknown_0x50ad6480),
}
