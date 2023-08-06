# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Color import Color


@dataclasses.dataclass()
class PlayerOffscreenIndicatorTextData(BaseProperty):
    text_render_mode: enums.UnknownEnum3 = dataclasses.field(default=enums.UnknownEnum3.Unknown1)
    default_font: AssetId = dataclasses.field(metadata={'asset_types': ['FONT']}, default=default_asset_id)
    foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    geometry_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    gradient_start: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    gradient_end: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x9f\x1b\xd4m')  # 0x9f1bd46d
        data.write(b'\x00\x04')  # size
        self.text_render_mode.to_stream(data)

        data.write(b'\r\xb9\xf8\xb6')  # 0xdb9f8b6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.default_font))

        data.write(b'?9\xe65')  # 0x3f39e635
        data.write(b'\x00\x10')  # size
        self.foreground_color.to_stream(data)

        data.write(b'`\xd7\x85i')  # 0x60d78569
        data.write(b'\x00\x10')  # size
        self.outline_color.to_stream(data)

        data.write(b'Y\x08\xef9')  # 0x5908ef39
        data.write(b'\x00\x10')  # size
        self.geometry_color.to_stream(data)

        data.write(b'\xfb\xb7\xbeE')  # 0xfbb7be45
        data.write(b'\x00\x10')  # size
        self.gradient_start.to_stream(data)

        data.write(b'\x0f\xbc\xe3\xfb')  # 0xfbce3fb
        data.write(b'\x00\x10')  # size
        self.gradient_end.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            text_render_mode=enums.UnknownEnum3.from_json(data['text_render_mode']),
            default_font=data['default_font'],
            foreground_color=Color.from_json(data['foreground_color']),
            outline_color=Color.from_json(data['outline_color']),
            geometry_color=Color.from_json(data['geometry_color']),
            gradient_start=Color.from_json(data['gradient_start']),
            gradient_end=Color.from_json(data['gradient_end']),
        )

    def to_json(self) -> dict:
        return {
            'text_render_mode': self.text_render_mode.to_json(),
            'default_font': self.default_font,
            'foreground_color': self.foreground_color.to_json(),
            'outline_color': self.outline_color.to_json(),
            'geometry_color': self.geometry_color.to_json(),
            'gradient_start': self.gradient_start.to_json(),
            'gradient_end': self.gradient_end.to_json(),
        }


def _decode_text_render_mode(data: typing.BinaryIO, property_size: int):
    return enums.UnknownEnum3.from_stream(data)


def _decode_default_font(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_geometry_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_gradient_start(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_gradient_end(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9f1bd46d: ('text_render_mode', _decode_text_render_mode),
    0xdb9f8b6: ('default_font', _decode_default_font),
    0x3f39e635: ('foreground_color', _decode_foreground_color),
    0x60d78569: ('outline_color', _decode_outline_color),
    0x5908ef39: ('geometry_color', _decode_geometry_color),
    0xfbb7be45: ('gradient_start', _decode_gradient_start),
    0xfbce3fb: ('gradient_end', _decode_gradient_end),
}
