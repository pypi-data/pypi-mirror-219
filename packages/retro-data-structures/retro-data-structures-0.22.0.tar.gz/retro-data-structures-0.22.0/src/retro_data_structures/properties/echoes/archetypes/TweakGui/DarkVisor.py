# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class DarkVisor(BaseProperty):
    dark_world_base_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    dark_visor_static_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    dark_visor_palette_modulate: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    dark_visor_blur_speed: float = dataclasses.field(default=0.0625)
    dark_visor_frame_top: int = dataclasses.field(default=100)
    dark_visor_frame_height: int = dataclasses.field(default=248)
    dark_visor_frame_left: int = dataclasses.field(default=50)
    dark_visor_frame_width: int = dataclasses.field(default=540)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xc5q\xa8\xc6')  # 0xc571a8c6
        data.write(b'\x00\x10')  # size
        self.dark_world_base_color.to_stream(data)

        data.write(b'\x93\xdb3R')  # 0x93db3352
        data.write(b'\x00\x10')  # size
        self.dark_visor_static_color.to_stream(data)

        data.write(b'\x92\xf8\xc6:')  # 0x92f8c63a
        data.write(b'\x00\x10')  # size
        self.dark_visor_palette_modulate.to_stream(data)

        data.write(b'\xaf\x90$\x12')  # 0xaf902412
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dark_visor_blur_speed))

        data.write(b'\xfc\x910\x90')  # 0xfc913090
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_visor_frame_top))

        data.write(b'\xd2u\xce\xee')  # 0xd275ceee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_visor_frame_height))

        data.write(b'\xaa\x80G\xa0')  # 0xaa8047a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_visor_frame_left))

        data.write(b"'s\xfb\xb3")  # 0x2773fbb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_visor_frame_width))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            dark_world_base_color=Color.from_json(data['dark_world_base_color']),
            dark_visor_static_color=Color.from_json(data['dark_visor_static_color']),
            dark_visor_palette_modulate=Color.from_json(data['dark_visor_palette_modulate']),
            dark_visor_blur_speed=data['dark_visor_blur_speed'],
            dark_visor_frame_top=data['dark_visor_frame_top'],
            dark_visor_frame_height=data['dark_visor_frame_height'],
            dark_visor_frame_left=data['dark_visor_frame_left'],
            dark_visor_frame_width=data['dark_visor_frame_width'],
        )

    def to_json(self) -> dict:
        return {
            'dark_world_base_color': self.dark_world_base_color.to_json(),
            'dark_visor_static_color': self.dark_visor_static_color.to_json(),
            'dark_visor_palette_modulate': self.dark_visor_palette_modulate.to_json(),
            'dark_visor_blur_speed': self.dark_visor_blur_speed,
            'dark_visor_frame_top': self.dark_visor_frame_top,
            'dark_visor_frame_height': self.dark_visor_frame_height,
            'dark_visor_frame_left': self.dark_visor_frame_left,
            'dark_visor_frame_width': self.dark_visor_frame_width,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_dark_world_base_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_dark_visor_static_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_dark_visor_palette_modulate(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_dark_visor_blur_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dark_visor_frame_top(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_visor_frame_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_visor_frame_left(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_visor_frame_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc571a8c6: ('dark_world_base_color', _decode_dark_world_base_color),
    0x93db3352: ('dark_visor_static_color', _decode_dark_visor_static_color),
    0x92f8c63a: ('dark_visor_palette_modulate', _decode_dark_visor_palette_modulate),
    0xaf902412: ('dark_visor_blur_speed', _decode_dark_visor_blur_speed),
    0xfc913090: ('dark_visor_frame_top', _decode_dark_visor_frame_top),
    0xd275ceee: ('dark_visor_frame_height', _decode_dark_visor_frame_height),
    0xaa8047a0: ('dark_visor_frame_left', _decode_dark_visor_frame_left),
    0x2773fbb3: ('dark_visor_frame_width', _decode_dark_visor_frame_width),
}
