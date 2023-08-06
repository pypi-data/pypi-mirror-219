# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class Completion(BaseProperty):
    unknown_0x81fc78c2: str = dataclasses.field(default='')
    main_font: str = dataclasses.field(default='')
    secondary_font: str = dataclasses.field(default='')
    main_font_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    main_font_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    stats_font_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    stats_font_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unlock_font_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unlock_font_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xb6fe7398: float = dataclasses.field(default=0.25)
    unknown_0x6af2871b: float = dataclasses.field(default=0.30000001192092896)
    text_start_delay: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\x81\xfcx\xc2')  # 0x81fc78c2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x81fc78c2.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'^\x7f\x85\xc7')  # 0x5e7f85c7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.main_font.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\n\ri\xd0')  # 0xa0d69d0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.secondary_font.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Z$\xa7\xe4')  # 0x5a24a7e4
        data.write(b'\x00\x10')  # size
        self.main_font_color.to_stream(data)

        data.write(b'\xa98\xbf9')  # 0xa938bf39
        data.write(b'\x00\x10')  # size
        self.main_font_outline_color.to_stream(data)

        data.write(b'\xc6\xcc\x9d\x0c')  # 0xc6cc9d0c
        data.write(b'\x00\x10')  # size
        self.stats_font_color.to_stream(data)

        data.write(b'\xd3\xa4\xa1\x80')  # 0xd3a4a180
        data.write(b'\x00\x10')  # size
        self.stats_font_outline_color.to_stream(data)

        data.write(b'\x07\xabVB')  # 0x7ab5642
        data.write(b'\x00\x10')  # size
        self.unlock_font_color.to_stream(data)

        data.write(b'Y\\c\xed')  # 0x595c63ed
        data.write(b'\x00\x10')  # size
        self.unlock_font_outline_color.to_stream(data)

        data.write(b'\xb6\xfes\x98')  # 0xb6fe7398
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb6fe7398))

        data.write(b'j\xf2\x87\x1b')  # 0x6af2871b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6af2871b))

        data.write(b')U\xd0U')  # 0x2955d055
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.text_start_delay))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x81fc78c2=data['unknown_0x81fc78c2'],
            main_font=data['main_font'],
            secondary_font=data['secondary_font'],
            main_font_color=Color.from_json(data['main_font_color']),
            main_font_outline_color=Color.from_json(data['main_font_outline_color']),
            stats_font_color=Color.from_json(data['stats_font_color']),
            stats_font_outline_color=Color.from_json(data['stats_font_outline_color']),
            unlock_font_color=Color.from_json(data['unlock_font_color']),
            unlock_font_outline_color=Color.from_json(data['unlock_font_outline_color']),
            unknown_0xb6fe7398=data['unknown_0xb6fe7398'],
            unknown_0x6af2871b=data['unknown_0x6af2871b'],
            text_start_delay=data['text_start_delay'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x81fc78c2': self.unknown_0x81fc78c2,
            'main_font': self.main_font,
            'secondary_font': self.secondary_font,
            'main_font_color': self.main_font_color.to_json(),
            'main_font_outline_color': self.main_font_outline_color.to_json(),
            'stats_font_color': self.stats_font_color.to_json(),
            'stats_font_outline_color': self.stats_font_outline_color.to_json(),
            'unlock_font_color': self.unlock_font_color.to_json(),
            'unlock_font_outline_color': self.unlock_font_outline_color.to_json(),
            'unknown_0xb6fe7398': self.unknown_0xb6fe7398,
            'unknown_0x6af2871b': self.unknown_0x6af2871b,
            'text_start_delay': self.text_start_delay,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_unknown_0x81fc78c2(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_main_font(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_secondary_font(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_main_font_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_main_font_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_stats_font_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_stats_font_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unlock_font_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unlock_font_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xb6fe7398(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6af2871b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_text_start_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x81fc78c2: ('unknown_0x81fc78c2', _decode_unknown_0x81fc78c2),
    0x5e7f85c7: ('main_font', _decode_main_font),
    0xa0d69d0: ('secondary_font', _decode_secondary_font),
    0x5a24a7e4: ('main_font_color', _decode_main_font_color),
    0xa938bf39: ('main_font_outline_color', _decode_main_font_outline_color),
    0xc6cc9d0c: ('stats_font_color', _decode_stats_font_color),
    0xd3a4a180: ('stats_font_outline_color', _decode_stats_font_outline_color),
    0x7ab5642: ('unlock_font_color', _decode_unlock_font_color),
    0x595c63ed: ('unlock_font_outline_color', _decode_unlock_font_outline_color),
    0xb6fe7398: ('unknown_0xb6fe7398', _decode_unknown_0xb6fe7398),
    0x6af2871b: ('unknown_0x6af2871b', _decode_unknown_0x6af2871b),
    0x2955d055: ('text_start_delay', _decode_text_start_delay),
}
