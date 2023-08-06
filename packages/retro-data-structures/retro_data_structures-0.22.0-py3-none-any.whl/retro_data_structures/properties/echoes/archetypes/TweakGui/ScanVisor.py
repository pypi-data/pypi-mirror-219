# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class ScanVisor(BaseProperty):
    inactive_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    inactive_external_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    non_critical_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    critical_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    burn_in_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    highlight_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    critical_highlight_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe8f5018b: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xba1ae1e5: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xb39d450e: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x1042455b: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xd72435ad: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x75cdc913: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    sweep_bar_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    burn_in_time: float = dataclasses.field(default=1.0)
    fade_out_time: float = dataclasses.field(default=0.30000001192092896)

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

        data.write(b'\x97"q\xb9')  # 0x972271b9
        data.write(b'\x00\x10')  # size
        self.inactive_color.to_stream(data)

        data.write(b'\xa9\x08\xc7u')  # 0xa908c775
        data.write(b'\x00\x10')  # size
        self.inactive_external_color.to_stream(data)

        data.write(b'\xee\x1f\x1d\xf6')  # 0xee1f1df6
        data.write(b'\x00\x10')  # size
        self.non_critical_color.to_stream(data)

        data.write(b'CDZ\xe7')  # 0x43445ae7
        data.write(b'\x00\x10')  # size
        self.critical_color.to_stream(data)

        data.write(b'\xf4\x8f\xd5Y')  # 0xf48fd559
        data.write(b'\x00\x10')  # size
        self.burn_in_color.to_stream(data)

        data.write(b'zd\x12\xf6')  # 0x7a6412f6
        data.write(b'\x00\x10')  # size
        self.highlight_color.to_stream(data)

        data.write(b'\xf4_}\x17')  # 0xf45f7d17
        data.write(b'\x00\x10')  # size
        self.critical_highlight_color.to_stream(data)

        data.write(b'\xe8\xf5\x01\x8b')  # 0xe8f5018b
        data.write(b'\x00\x10')  # size
        self.unknown_0xe8f5018b.to_stream(data)

        data.write(b'\xba\x1a\xe1\xe5')  # 0xba1ae1e5
        data.write(b'\x00\x10')  # size
        self.unknown_0xba1ae1e5.to_stream(data)

        data.write(b'\xb3\x9dE\x0e')  # 0xb39d450e
        data.write(b'\x00\x10')  # size
        self.unknown_0xb39d450e.to_stream(data)

        data.write(b'\x10BE[')  # 0x1042455b
        data.write(b'\x00\x10')  # size
        self.unknown_0x1042455b.to_stream(data)

        data.write(b'\xd7$5\xad')  # 0xd72435ad
        data.write(b'\x00\x10')  # size
        self.unknown_0xd72435ad.to_stream(data)

        data.write(b'u\xcd\xc9\x13')  # 0x75cdc913
        data.write(b'\x00\x10')  # size
        self.unknown_0x75cdc913.to_stream(data)

        data.write(b'\x99~\xc3\x8d')  # 0x997ec38d
        data.write(b'\x00\x10')  # size
        self.sweep_bar_color.to_stream(data)

        data.write(b'\x00\xb8?\x02')  # 0xb83f02
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.burn_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            inactive_color=Color.from_json(data['inactive_color']),
            inactive_external_color=Color.from_json(data['inactive_external_color']),
            non_critical_color=Color.from_json(data['non_critical_color']),
            critical_color=Color.from_json(data['critical_color']),
            burn_in_color=Color.from_json(data['burn_in_color']),
            highlight_color=Color.from_json(data['highlight_color']),
            critical_highlight_color=Color.from_json(data['critical_highlight_color']),
            unknown_0xe8f5018b=Color.from_json(data['unknown_0xe8f5018b']),
            unknown_0xba1ae1e5=Color.from_json(data['unknown_0xba1ae1e5']),
            unknown_0xb39d450e=Color.from_json(data['unknown_0xb39d450e']),
            unknown_0x1042455b=Color.from_json(data['unknown_0x1042455b']),
            unknown_0xd72435ad=Color.from_json(data['unknown_0xd72435ad']),
            unknown_0x75cdc913=Color.from_json(data['unknown_0x75cdc913']),
            sweep_bar_color=Color.from_json(data['sweep_bar_color']),
            burn_in_time=data['burn_in_time'],
            fade_out_time=data['fade_out_time'],
        )

    def to_json(self) -> dict:
        return {
            'inactive_color': self.inactive_color.to_json(),
            'inactive_external_color': self.inactive_external_color.to_json(),
            'non_critical_color': self.non_critical_color.to_json(),
            'critical_color': self.critical_color.to_json(),
            'burn_in_color': self.burn_in_color.to_json(),
            'highlight_color': self.highlight_color.to_json(),
            'critical_highlight_color': self.critical_highlight_color.to_json(),
            'unknown_0xe8f5018b': self.unknown_0xe8f5018b.to_json(),
            'unknown_0xba1ae1e5': self.unknown_0xba1ae1e5.to_json(),
            'unknown_0xb39d450e': self.unknown_0xb39d450e.to_json(),
            'unknown_0x1042455b': self.unknown_0x1042455b.to_json(),
            'unknown_0xd72435ad': self.unknown_0xd72435ad.to_json(),
            'unknown_0x75cdc913': self.unknown_0x75cdc913.to_json(),
            'sweep_bar_color': self.sweep_bar_color.to_json(),
            'burn_in_time': self.burn_in_time,
            'fade_out_time': self.fade_out_time,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_inactive_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_inactive_external_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_non_critical_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_critical_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_burn_in_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_highlight_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_critical_highlight_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe8f5018b(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xba1ae1e5(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xb39d450e(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x1042455b(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xd72435ad(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x75cdc913(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_sweep_bar_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_burn_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x972271b9: ('inactive_color', _decode_inactive_color),
    0xa908c775: ('inactive_external_color', _decode_inactive_external_color),
    0xee1f1df6: ('non_critical_color', _decode_non_critical_color),
    0x43445ae7: ('critical_color', _decode_critical_color),
    0xf48fd559: ('burn_in_color', _decode_burn_in_color),
    0x7a6412f6: ('highlight_color', _decode_highlight_color),
    0xf45f7d17: ('critical_highlight_color', _decode_critical_highlight_color),
    0xe8f5018b: ('unknown_0xe8f5018b', _decode_unknown_0xe8f5018b),
    0xba1ae1e5: ('unknown_0xba1ae1e5', _decode_unknown_0xba1ae1e5),
    0xb39d450e: ('unknown_0xb39d450e', _decode_unknown_0xb39d450e),
    0x1042455b: ('unknown_0x1042455b', _decode_unknown_0x1042455b),
    0xd72435ad: ('unknown_0xd72435ad', _decode_unknown_0xd72435ad),
    0x75cdc913: ('unknown_0x75cdc913', _decode_unknown_0x75cdc913),
    0x997ec38d: ('sweep_bar_color', _decode_sweep_bar_color),
    0xb83f02: ('burn_in_time', _decode_burn_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
}
