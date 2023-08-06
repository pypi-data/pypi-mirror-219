# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class TextProperties(BaseProperty):
    text_bounding_width: int = dataclasses.field(default=1)
    text_bounding_height: int = dataclasses.field(default=1)
    line_spacing: float = dataclasses.field(default=100.0)
    line_extra_space: int = dataclasses.field(default=0)
    character_extra_space: int = dataclasses.field(default=0)
    foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    geometry_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    default_font: AssetId = dataclasses.field(metadata={'asset_types': ['FONT']}, default=default_asset_id)
    unknown_0x18dd95cd: int = dataclasses.field(default=0)
    unknown_0x42091548: int = dataclasses.field(default=0)
    wrap_text: bool = dataclasses.field(default=True)

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

        data.write(b'\xeeR\x1d\xc6')  # 0xee521dc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.text_bounding_width))

        data.write(b'\xf2\xd3j\xbb')  # 0xf2d36abb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.text_bounding_height))

        data.write(b'\x1a\x99b\x92')  # 0x1a996292
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.line_spacing))

        data.write(b'\x05\xef\xf9\x13')  # 0x5eff913
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.line_extra_space))

        data.write(b'E\x83\t\x01')  # 0x45830901
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.character_extra_space))

        data.write(b'?9\xe65')  # 0x3f39e635
        data.write(b'\x00\x10')  # size
        self.foreground_color.to_stream(data)

        data.write(b'`\xd7\x85i')  # 0x60d78569
        data.write(b'\x00\x10')  # size
        self.outline_color.to_stream(data)

        data.write(b'Y\x08\xef9')  # 0x5908ef39
        data.write(b'\x00\x10')  # size
        self.geometry_color.to_stream(data)

        data.write(b'\r\xb9\xf8\xb6')  # 0xdb9f8b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.default_font))

        data.write(b'\x18\xdd\x95\xcd')  # 0x18dd95cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x18dd95cd))

        data.write(b'B\t\x15H')  # 0x42091548
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x42091548))

        data.write(b'3\x05s\xe9')  # 0x330573e9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.wrap_text))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            text_bounding_width=data['text_bounding_width'],
            text_bounding_height=data['text_bounding_height'],
            line_spacing=data['line_spacing'],
            line_extra_space=data['line_extra_space'],
            character_extra_space=data['character_extra_space'],
            foreground_color=Color.from_json(data['foreground_color']),
            outline_color=Color.from_json(data['outline_color']),
            geometry_color=Color.from_json(data['geometry_color']),
            default_font=data['default_font'],
            unknown_0x18dd95cd=data['unknown_0x18dd95cd'],
            unknown_0x42091548=data['unknown_0x42091548'],
            wrap_text=data['wrap_text'],
        )

    def to_json(self) -> dict:
        return {
            'text_bounding_width': self.text_bounding_width,
            'text_bounding_height': self.text_bounding_height,
            'line_spacing': self.line_spacing,
            'line_extra_space': self.line_extra_space,
            'character_extra_space': self.character_extra_space,
            'foreground_color': self.foreground_color.to_json(),
            'outline_color': self.outline_color.to_json(),
            'geometry_color': self.geometry_color.to_json(),
            'default_font': self.default_font,
            'unknown_0x18dd95cd': self.unknown_0x18dd95cd,
            'unknown_0x42091548': self.unknown_0x42091548,
            'wrap_text': self.wrap_text,
        }

    def _dependencies_for_default_font(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.default_font)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_default_font, "default_font", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for TextProperties.{field_name} ({field_type}): {e}"
                )


def _decode_text_bounding_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_text_bounding_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_line_spacing(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_line_extra_space(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_character_extra_space(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_geometry_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_default_font(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x18dd95cd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x42091548(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_wrap_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xee521dc6: ('text_bounding_width', _decode_text_bounding_width),
    0xf2d36abb: ('text_bounding_height', _decode_text_bounding_height),
    0x1a996292: ('line_spacing', _decode_line_spacing),
    0x5eff913: ('line_extra_space', _decode_line_extra_space),
    0x45830901: ('character_extra_space', _decode_character_extra_space),
    0x3f39e635: ('foreground_color', _decode_foreground_color),
    0x60d78569: ('outline_color', _decode_outline_color),
    0x5908ef39: ('geometry_color', _decode_geometry_color),
    0xdb9f8b6: ('default_font', _decode_default_font),
    0x18dd95cd: ('unknown_0x18dd95cd', _decode_unknown_0x18dd95cd),
    0x42091548: ('unknown_0x42091548', _decode_unknown_0x42091548),
    0x330573e9: ('wrap_text', _decode_wrap_text),
}
