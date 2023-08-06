# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class Multiplayer(BaseProperty):
    score_text_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa09caefe: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    timer_text_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    timer_text_blink_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xec4197e3: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x823e2fb3: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x95cc4ed8: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdb2ca6ff: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    lockon_indicator_on_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    lockon_indicator_off_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'#\xca\xc7D')  # 0x23cac744
        data.write(b'\x00\x10')  # size
        self.score_text_color.to_stream(data)

        data.write(b'\xa0\x9c\xae\xfe')  # 0xa09caefe
        data.write(b'\x00\x10')  # size
        self.unknown_0xa09caefe.to_stream(data)

        data.write(b'k\xf0O\xf9')  # 0x6bf04ff9
        data.write(b'\x00\x10')  # size
        self.timer_text_color.to_stream(data)

        data.write(b'B\x80\xd0\n')  # 0x4280d00a
        data.write(b'\x00\x10')  # size
        self.timer_text_blink_color.to_stream(data)

        data.write(b'\xecA\x97\xe3')  # 0xec4197e3
        data.write(b'\x00\x10')  # size
        self.unknown_0xec4197e3.to_stream(data)

        data.write(b'\x82>/\xb3')  # 0x823e2fb3
        data.write(b'\x00\x10')  # size
        self.unknown_0x823e2fb3.to_stream(data)

        data.write(b'\x95\xccN\xd8')  # 0x95cc4ed8
        data.write(b'\x00\x10')  # size
        self.unknown_0x95cc4ed8.to_stream(data)

        data.write(b'\xdb,\xa6\xff')  # 0xdb2ca6ff
        data.write(b'\x00\x10')  # size
        self.unknown_0xdb2ca6ff.to_stream(data)

        data.write(b'\x03\xd2\x7f\xfd')  # 0x3d27ffd
        data.write(b'\x00\x10')  # size
        self.lockon_indicator_on_color.to_stream(data)

        data.write(b'L!Wu')  # 0x4c215775
        data.write(b'\x00\x10')  # size
        self.lockon_indicator_off_color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            score_text_color=Color.from_json(data['score_text_color']),
            unknown_0xa09caefe=Color.from_json(data['unknown_0xa09caefe']),
            timer_text_color=Color.from_json(data['timer_text_color']),
            timer_text_blink_color=Color.from_json(data['timer_text_blink_color']),
            unknown_0xec4197e3=Color.from_json(data['unknown_0xec4197e3']),
            unknown_0x823e2fb3=Color.from_json(data['unknown_0x823e2fb3']),
            unknown_0x95cc4ed8=Color.from_json(data['unknown_0x95cc4ed8']),
            unknown_0xdb2ca6ff=Color.from_json(data['unknown_0xdb2ca6ff']),
            lockon_indicator_on_color=Color.from_json(data['lockon_indicator_on_color']),
            lockon_indicator_off_color=Color.from_json(data['lockon_indicator_off_color']),
        )

    def to_json(self) -> dict:
        return {
            'score_text_color': self.score_text_color.to_json(),
            'unknown_0xa09caefe': self.unknown_0xa09caefe.to_json(),
            'timer_text_color': self.timer_text_color.to_json(),
            'timer_text_blink_color': self.timer_text_blink_color.to_json(),
            'unknown_0xec4197e3': self.unknown_0xec4197e3.to_json(),
            'unknown_0x823e2fb3': self.unknown_0x823e2fb3.to_json(),
            'unknown_0x95cc4ed8': self.unknown_0x95cc4ed8.to_json(),
            'unknown_0xdb2ca6ff': self.unknown_0xdb2ca6ff.to_json(),
            'lockon_indicator_on_color': self.lockon_indicator_on_color.to_json(),
            'lockon_indicator_off_color': self.lockon_indicator_off_color.to_json(),
        }


def _decode_score_text_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa09caefe(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_timer_text_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_timer_text_blink_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xec4197e3(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x823e2fb3(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x95cc4ed8(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdb2ca6ff(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_lockon_indicator_on_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_lockon_indicator_off_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x23cac744: ('score_text_color', _decode_score_text_color),
    0xa09caefe: ('unknown_0xa09caefe', _decode_unknown_0xa09caefe),
    0x6bf04ff9: ('timer_text_color', _decode_timer_text_color),
    0x4280d00a: ('timer_text_blink_color', _decode_timer_text_blink_color),
    0xec4197e3: ('unknown_0xec4197e3', _decode_unknown_0xec4197e3),
    0x823e2fb3: ('unknown_0x823e2fb3', _decode_unknown_0x823e2fb3),
    0x95cc4ed8: ('unknown_0x95cc4ed8', _decode_unknown_0x95cc4ed8),
    0xdb2ca6ff: ('unknown_0xdb2ca6ff', _decode_unknown_0xdb2ca6ff),
    0x3d27ffd: ('lockon_indicator_on_color', _decode_lockon_indicator_on_color),
    0x4c215775: ('lockon_indicator_off_color', _decode_lockon_indicator_off_color),
}
