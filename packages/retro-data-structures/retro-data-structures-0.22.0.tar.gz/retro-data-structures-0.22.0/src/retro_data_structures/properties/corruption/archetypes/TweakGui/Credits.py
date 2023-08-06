# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class Credits(BaseProperty):
    unknown_0x81fc78c2: str = dataclasses.field(default='')
    unknown_0x2bcd300d: str = dataclasses.field(default='')
    alternate_font: str = dataclasses.field(default='')
    font_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    font_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    total_time: float = dataclasses.field(default=191.0)
    text_fade_time: float = dataclasses.field(default=2.0)
    movie_fade_time: float = dataclasses.field(default=2.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\x81\xfcx\xc2')  # 0x81fc78c2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x81fc78c2.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+\xcd0\r')  # 0x2bcd300d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x2bcd300d.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xce\xf9\x0c\x00')  # 0xcef90c00
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.alternate_font.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1a\x96\xecg')  # 0x1a96ec67
        data.write(b'\x00\x10')  # size
        self.font_color.to_stream(data)

        data.write(b'\x84J\xb6\xb0')  # 0x844ab6b0
        data.write(b'\x00\x10')  # size
        self.font_outline_color.to_stream(data)

        data.write(b'\x19hk\xf6')  # 0x19686bf6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.total_time))

        data.write(b'R\x98Z\xd1')  # 0x52985ad1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_fade_time))

        data.write(b'\xf0\xf9w\xe6')  # 0xf0f977e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movie_fade_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x81fc78c2=data['unknown_0x81fc78c2'],
            unknown_0x2bcd300d=data['unknown_0x2bcd300d'],
            alternate_font=data['alternate_font'],
            font_color=Color.from_json(data['font_color']),
            font_outline_color=Color.from_json(data['font_outline_color']),
            total_time=data['total_time'],
            text_fade_time=data['text_fade_time'],
            movie_fade_time=data['movie_fade_time'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x81fc78c2': self.unknown_0x81fc78c2,
            'unknown_0x2bcd300d': self.unknown_0x2bcd300d,
            'alternate_font': self.alternate_font,
            'font_color': self.font_color.to_json(),
            'font_outline_color': self.font_outline_color.to_json(),
            'total_time': self.total_time,
            'text_fade_time': self.text_fade_time,
            'movie_fade_time': self.movie_fade_time,
        }


def _decode_unknown_0x81fc78c2(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x2bcd300d(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_alternate_font(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_font_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_font_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_total_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_text_fade_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movie_fade_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x81fc78c2: ('unknown_0x81fc78c2', _decode_unknown_0x81fc78c2),
    0x2bcd300d: ('unknown_0x2bcd300d', _decode_unknown_0x2bcd300d),
    0xcef90c00: ('alternate_font', _decode_alternate_font),
    0x1a96ec67: ('font_color', _decode_font_color),
    0x844ab6b0: ('font_outline_color', _decode_font_outline_color),
    0x19686bf6: ('total_time', _decode_total_time),
    0x52985ad1: ('text_fade_time', _decode_text_fade_time),
    0xf0f977e6: ('movie_fade_time', _decode_movie_fade_time),
}
