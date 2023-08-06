# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class HUDColorsTypedef(BaseProperty):
    unknown_0xc8ddc662: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_group_active_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    threat_group_inactive_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xa6609cc5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_group_active_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_group_inactive_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xdcaab836: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_filled_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_shadow_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_bar_empty_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_tanks_filled_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    energy_tanks_empty_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    radar_widget_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    active_text_foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    inactive_text_foreground_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    text_shadow_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'\xc8\xdd\xc6b')  # 0xc8ddc662
        data.write(b'\x00\x10')  # size
        self.unknown_0xc8ddc662.to_stream(data)

        data.write(b'/<\xac\xaf')  # 0x2f3cacaf
        data.write(b'\x00\x10')  # size
        self.threat_group_active_color.to_stream(data)

        data.write(b't\xe5\xff\xa1')  # 0x74e5ffa1
        data.write(b'\x00\x10')  # size
        self.threat_group_inactive_color.to_stream(data)

        data.write(b'\xa6`\x9c\xc5')  # 0xa6609cc5
        data.write(b'\x00\x10')  # size
        self.unknown_0xa6609cc5.to_stream(data)

        data.write(b'\xcb\xb3\xfbv')  # 0xcbb3fb76
        data.write(b'\x00\x10')  # size
        self.missile_group_active_color.to_stream(data)

        data.write(b'\xd1\x10\xa1/')  # 0xd110a12f
        data.write(b'\x00\x10')  # size
        self.missile_group_inactive_color.to_stream(data)

        data.write(b'\xdc\xaa\xb86')  # 0xdcaab836
        data.write(b'\x00\x10')  # size
        self.unknown_0xdcaab836.to_stream(data)

        data.write(b'\xac\xf6-\x93')  # 0xacf62d93
        data.write(b'\x00\x10')  # size
        self.energy_bar_filled_color.to_stream(data)

        data.write(b'\xb9\xa9\xfcn')  # 0xb9a9fc6e
        data.write(b'\x00\x10')  # size
        self.energy_bar_shadow_color.to_stream(data)

        data.write(b'7\xe3\x81\xc2')  # 0x37e381c2
        data.write(b'\x00\x10')  # size
        self.energy_bar_empty_color.to_stream(data)

        data.write(b'Cw\xe6w')  # 0x4377e677
        data.write(b'\x00\x10')  # size
        self.energy_tanks_filled_color.to_stream(data)

        data.write(b'c8O\x81')  # 0x63384f81
        data.write(b'\x00\x10')  # size
        self.energy_tanks_empty_color.to_stream(data)

        data.write(b'\xa7\t\xdb@')  # 0xa709db40
        data.write(b'\x00\x10')  # size
        self.radar_widget_color.to_stream(data)

        data.write(b'\xaaJV\x04')  # 0xaa4a5604
        data.write(b'\x00\x10')  # size
        self.active_text_foreground_color.to_stream(data)

        data.write(b'l\xcc\xdf\x8f')  # 0x6cccdf8f
        data.write(b'\x00\x10')  # size
        self.inactive_text_foreground_color.to_stream(data)

        data.write(b'\r\xaa}\x80')  # 0xdaa7d80
        data.write(b'\x00\x10')  # size
        self.text_shadow_outline_color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xc8ddc662=Color.from_json(data['unknown_0xc8ddc662']),
            threat_group_active_color=Color.from_json(data['threat_group_active_color']),
            threat_group_inactive_color=Color.from_json(data['threat_group_inactive_color']),
            unknown_0xa6609cc5=Color.from_json(data['unknown_0xa6609cc5']),
            missile_group_active_color=Color.from_json(data['missile_group_active_color']),
            missile_group_inactive_color=Color.from_json(data['missile_group_inactive_color']),
            unknown_0xdcaab836=Color.from_json(data['unknown_0xdcaab836']),
            energy_bar_filled_color=Color.from_json(data['energy_bar_filled_color']),
            energy_bar_shadow_color=Color.from_json(data['energy_bar_shadow_color']),
            energy_bar_empty_color=Color.from_json(data['energy_bar_empty_color']),
            energy_tanks_filled_color=Color.from_json(data['energy_tanks_filled_color']),
            energy_tanks_empty_color=Color.from_json(data['energy_tanks_empty_color']),
            radar_widget_color=Color.from_json(data['radar_widget_color']),
            active_text_foreground_color=Color.from_json(data['active_text_foreground_color']),
            inactive_text_foreground_color=Color.from_json(data['inactive_text_foreground_color']),
            text_shadow_outline_color=Color.from_json(data['text_shadow_outline_color']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xc8ddc662': self.unknown_0xc8ddc662.to_json(),
            'threat_group_active_color': self.threat_group_active_color.to_json(),
            'threat_group_inactive_color': self.threat_group_inactive_color.to_json(),
            'unknown_0xa6609cc5': self.unknown_0xa6609cc5.to_json(),
            'missile_group_active_color': self.missile_group_active_color.to_json(),
            'missile_group_inactive_color': self.missile_group_inactive_color.to_json(),
            'unknown_0xdcaab836': self.unknown_0xdcaab836.to_json(),
            'energy_bar_filled_color': self.energy_bar_filled_color.to_json(),
            'energy_bar_shadow_color': self.energy_bar_shadow_color.to_json(),
            'energy_bar_empty_color': self.energy_bar_empty_color.to_json(),
            'energy_tanks_filled_color': self.energy_tanks_filled_color.to_json(),
            'energy_tanks_empty_color': self.energy_tanks_empty_color.to_json(),
            'radar_widget_color': self.radar_widget_color.to_json(),
            'active_text_foreground_color': self.active_text_foreground_color.to_json(),
            'inactive_text_foreground_color': self.inactive_text_foreground_color.to_json(),
            'text_shadow_outline_color': self.text_shadow_outline_color.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_unknown_0xc8ddc662(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_group_active_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_threat_group_inactive_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xa6609cc5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_group_active_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_group_inactive_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xdcaab836(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_filled_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_shadow_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_bar_empty_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_tanks_filled_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_energy_tanks_empty_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_radar_widget_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_active_text_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_inactive_text_foreground_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_shadow_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc8ddc662: ('unknown_0xc8ddc662', _decode_unknown_0xc8ddc662),
    0x2f3cacaf: ('threat_group_active_color', _decode_threat_group_active_color),
    0x74e5ffa1: ('threat_group_inactive_color', _decode_threat_group_inactive_color),
    0xa6609cc5: ('unknown_0xa6609cc5', _decode_unknown_0xa6609cc5),
    0xcbb3fb76: ('missile_group_active_color', _decode_missile_group_active_color),
    0xd110a12f: ('missile_group_inactive_color', _decode_missile_group_inactive_color),
    0xdcaab836: ('unknown_0xdcaab836', _decode_unknown_0xdcaab836),
    0xacf62d93: ('energy_bar_filled_color', _decode_energy_bar_filled_color),
    0xb9a9fc6e: ('energy_bar_shadow_color', _decode_energy_bar_shadow_color),
    0x37e381c2: ('energy_bar_empty_color', _decode_energy_bar_empty_color),
    0x4377e677: ('energy_tanks_filled_color', _decode_energy_tanks_filled_color),
    0x63384f81: ('energy_tanks_empty_color', _decode_energy_tanks_empty_color),
    0xa709db40: ('radar_widget_color', _decode_radar_widget_color),
    0xaa4a5604: ('active_text_foreground_color', _decode_active_text_foreground_color),
    0x6cccdf8f: ('inactive_text_foreground_color', _decode_inactive_text_foreground_color),
    0xdaa7d80: ('text_shadow_outline_color', _decode_text_shadow_outline_color),
}
