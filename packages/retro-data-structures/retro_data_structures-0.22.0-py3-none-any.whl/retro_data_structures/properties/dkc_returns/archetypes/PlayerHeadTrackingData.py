# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerHeadTrackingData(BaseProperty):
    animation: int = dataclasses.field(default=0)
    unknown_0x7f96d93c: int = dataclasses.field(default=0)
    unknown_0xd0ed78b3: int = dataclasses.field(default=0)
    head_aim_locator: str = dataclasses.field(default='')
    head_locator: str = dataclasses.field(default='')
    upper_lip_locator: str = dataclasses.field(default='')

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xaa\xcd\xb1\x1c')  # 0xaacdb11c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation))

        data.write(b'\x7f\x96\xd9<')  # 0x7f96d93c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x7f96d93c))

        data.write(b'\xd0\xedx\xb3')  # 0xd0ed78b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd0ed78b3))

        data.write(b'\xf0\xebw-')  # 0xf0eb772d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.head_aim_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xda\x07\\\x18')  # 0xda075c18
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.head_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5\xfa\x9d"')  # 0xa5fa9d22
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.upper_lip_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            animation=data['animation'],
            unknown_0x7f96d93c=data['unknown_0x7f96d93c'],
            unknown_0xd0ed78b3=data['unknown_0xd0ed78b3'],
            head_aim_locator=data['head_aim_locator'],
            head_locator=data['head_locator'],
            upper_lip_locator=data['upper_lip_locator'],
        )

    def to_json(self) -> dict:
        return {
            'animation': self.animation,
            'unknown_0x7f96d93c': self.unknown_0x7f96d93c,
            'unknown_0xd0ed78b3': self.unknown_0xd0ed78b3,
            'head_aim_locator': self.head_aim_locator,
            'head_locator': self.head_locator,
            'upper_lip_locator': self.upper_lip_locator,
        }


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x7f96d93c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xd0ed78b3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_head_aim_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_head_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_upper_lip_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xaacdb11c: ('animation', _decode_animation),
    0x7f96d93c: ('unknown_0x7f96d93c', _decode_unknown_0x7f96d93c),
    0xd0ed78b3: ('unknown_0xd0ed78b3', _decode_unknown_0xd0ed78b3),
    0xf0eb772d: ('head_aim_locator', _decode_head_aim_locator),
    0xda075c18: ('head_locator', _decode_head_locator),
    0xa5fa9d22: ('upper_lip_locator', _decode_upper_lip_locator),
}
