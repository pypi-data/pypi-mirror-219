# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class Misc(BaseProperty):
    unknown_0x13cfde23: float = dataclasses.field(default=0.699999988079071)
    unknown_0xf3499713: float = dataclasses.field(default=1.0)
    unknown_0x895a47fb: float = dataclasses.field(default=200.0)

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

        data.write(b'\x13\xcf\xde#')  # 0x13cfde23
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x13cfde23))

        data.write(b'\xf3I\x97\x13')  # 0xf3499713
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf3499713))

        data.write(b'\x89ZG\xfb')  # 0x895a47fb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x895a47fb))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x13cfde23=data['unknown_0x13cfde23'],
            unknown_0xf3499713=data['unknown_0xf3499713'],
            unknown_0x895a47fb=data['unknown_0x895a47fb'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x13cfde23': self.unknown_0x13cfde23,
            'unknown_0xf3499713': self.unknown_0xf3499713,
            'unknown_0x895a47fb': self.unknown_0x895a47fb,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x13cfde23, 0xf3499713, 0x895a47fb)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[Misc]:
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

    return Misc(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_unknown_0x13cfde23(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf3499713(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x895a47fb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x13cfde23: ('unknown_0x13cfde23', _decode_unknown_0x13cfde23),
    0xf3499713: ('unknown_0xf3499713', _decode_unknown_0xf3499713),
    0x895a47fb: ('unknown_0x895a47fb', _decode_unknown_0x895a47fb),
}
