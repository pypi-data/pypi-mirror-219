# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class TurretHudTypedef(BaseProperty):
    frame_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    font_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    font_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_fill_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_shadow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_empty_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xa4\x857,')  # 0xa485372c
        data.write(b'\x00\x10')  # size
        self.frame_color.to_stream(data)

        data.write(b'\x1a\x96\xecg')  # 0x1a96ec67
        data.write(b'\x00\x10')  # size
        self.font_color.to_stream(data)

        data.write(b'\x84J\xb6\xb0')  # 0x844ab6b0
        data.write(b'\x00\x10')  # size
        self.font_outline_color.to_stream(data)

        data.write(b'\xbd\xb6\x97\xa9')  # 0xbdb697a9
        data.write(b'\x00\x10')  # size
        self.energy_bar_fill_color.to_stream(data)

        data.write(b'\xb9\xa9\xfcn')  # 0xb9a9fc6e
        data.write(b'\x00\x10')  # size
        self.energy_bar_shadow_color.to_stream(data)

        data.write(b'7\xe3\x81\xc2')  # 0x37e381c2
        data.write(b'\x00\x10')  # size
        self.energy_bar_empty_color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            frame_color=Color.from_json(data['frame_color']),
            font_color=Color.from_json(data['font_color']),
            font_outline_color=Color.from_json(data['font_outline_color']),
            energy_bar_fill_color=Color.from_json(data['energy_bar_fill_color']),
            energy_bar_shadow_color=Color.from_json(data['energy_bar_shadow_color']),
            energy_bar_empty_color=Color.from_json(data['energy_bar_empty_color']),
        )

    def to_json(self) -> dict:
        return {
            'frame_color': self.frame_color.to_json(),
            'font_color': self.font_color.to_json(),
            'font_outline_color': self.font_outline_color.to_json(),
            'energy_bar_fill_color': self.energy_bar_fill_color.to_json(),
            'energy_bar_shadow_color': self.energy_bar_shadow_color.to_json(),
            'energy_bar_empty_color': self.energy_bar_empty_color.to_json(),
        }


def _decode_frame_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_font_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_font_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_fill_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_shadow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_empty_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa485372c: ('frame_color', _decode_frame_color),
    0x1a96ec67: ('font_color', _decode_font_color),
    0x844ab6b0: ('font_outline_color', _decode_font_outline_color),
    0xbdb697a9: ('energy_bar_fill_color', _decode_energy_bar_fill_color),
    0xb9a9fc6e: ('energy_bar_shadow_color', _decode_energy_bar_shadow_color),
    0x37e381c2: ('energy_bar_empty_color', _decode_energy_bar_empty_color),
}
