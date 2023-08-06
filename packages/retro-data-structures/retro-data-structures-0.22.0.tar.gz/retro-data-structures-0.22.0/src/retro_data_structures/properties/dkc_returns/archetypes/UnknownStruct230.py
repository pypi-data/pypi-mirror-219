# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct230(BaseProperty):
    unknown_0x43bc661c: bool = dataclasses.field(default=False)
    allow_swipe: bool = dataclasses.field(default=False)
    unknown_0xe10e94ec: float = dataclasses.field(default=1.0)
    unknown_0x84b3080b: str = dataclasses.field(default='')
    unknown_0x69170884: str = dataclasses.field(default='')

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'C\xbcf\x1c')  # 0x43bc661c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x43bc661c))

        data.write(b'A\x0b\xde\xf2')  # 0x410bdef2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.allow_swipe))

        data.write(b'\xe1\x0e\x94\xec')  # 0xe10e94ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe10e94ec))

        data.write(b'\x84\xb3\x08\x0b')  # 0x84b3080b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x84b3080b.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i\x17\x08\x84')  # 0x69170884
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x69170884.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x43bc661c=data['unknown_0x43bc661c'],
            allow_swipe=data['allow_swipe'],
            unknown_0xe10e94ec=data['unknown_0xe10e94ec'],
            unknown_0x84b3080b=data['unknown_0x84b3080b'],
            unknown_0x69170884=data['unknown_0x69170884'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x43bc661c': self.unknown_0x43bc661c,
            'allow_swipe': self.allow_swipe,
            'unknown_0xe10e94ec': self.unknown_0xe10e94ec,
            'unknown_0x84b3080b': self.unknown_0x84b3080b,
            'unknown_0x69170884': self.unknown_0x69170884,
        }


def _decode_unknown_0x43bc661c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_allow_swipe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xe10e94ec(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x84b3080b(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x69170884(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x43bc661c: ('unknown_0x43bc661c', _decode_unknown_0x43bc661c),
    0x410bdef2: ('allow_swipe', _decode_allow_swipe),
    0xe10e94ec: ('unknown_0xe10e94ec', _decode_unknown_0xe10e94ec),
    0x84b3080b: ('unknown_0x84b3080b', _decode_unknown_0x84b3080b),
    0x69170884: ('unknown_0x69170884', _decode_unknown_0x69170884),
}
