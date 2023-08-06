# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerPeriodicAdditiveAnimationData(BaseProperty):
    random_delay_minimum: float = dataclasses.field(default=3.0)
    random_delay_maximum: float = dataclasses.field(default=6.0)
    animation: int = dataclasses.field(default=0)
    visibility_key: str = dataclasses.field(default='')

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'n22\x95')  # 0x6e323295
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_delay_minimum))

        data.write(b'\xfeA"\x7f')  # 0xfe41227f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_delay_maximum))

        data.write(b'\xaa\xcd\xb1\x1c')  # 0xaacdb11c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation))

        data.write(b'\x15\xdb\xa7A')  # 0x15dba741
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.visibility_key.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            random_delay_minimum=data['random_delay_minimum'],
            random_delay_maximum=data['random_delay_maximum'],
            animation=data['animation'],
            visibility_key=data['visibility_key'],
        )

    def to_json(self) -> dict:
        return {
            'random_delay_minimum': self.random_delay_minimum,
            'random_delay_maximum': self.random_delay_maximum,
            'animation': self.animation,
            'visibility_key': self.visibility_key,
        }


def _decode_random_delay_minimum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_delay_maximum(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_visibility_key(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6e323295: ('random_delay_minimum', _decode_random_delay_minimum),
    0xfe41227f: ('random_delay_maximum', _decode_random_delay_maximum),
    0xaacdb11c: ('animation', _decode_animation),
    0x15dba741: ('visibility_key', _decode_visibility_key),
}
