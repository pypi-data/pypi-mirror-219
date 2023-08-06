# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class DoorColors(BaseProperty):
    num_door_colors: int = dataclasses.field(default=8)
    blue_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    dark_beam_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    annihilator_beam_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    light_beam_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    super_missile_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    seeker_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    power_bomb_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    grey_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    white_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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

        data.write(b'O\xce\xb9\x04')  # 0x4fceb904
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_door_colors))

        data.write(b'\xb3j\xa9\xb7')  # 0xb36aa9b7
        data.write(b'\x00\x10')  # size
        self.blue_door_color.to_stream(data)

        data.write(b'\x96 \xd4\xa0')  # 0x9620d4a0
        data.write(b'\x00\x10')  # size
        self.missile_door_color.to_stream(data)

        data.write(b'N\x1a\x9a\x8d')  # 0x4e1a9a8d
        data.write(b'\x00\x10')  # size
        self.dark_beam_door_color.to_stream(data)

        data.write(b'\xce\x98dS')  # 0xce986453
        data.write(b'\x00\x10')  # size
        self.unknown.to_stream(data)

        data.write(b'\x07\x0f6\xf9')  # 0x70f36f9
        data.write(b'\x00\x10')  # size
        self.annihilator_beam_door_color.to_stream(data)

        data.write(b'\xfa\xda\x14\xb6')  # 0xfada14b6
        data.write(b'\x00\x10')  # size
        self.light_beam_door_color.to_stream(data)

        data.write(b'\x17"A\xdc')  # 0x172241dc
        data.write(b'\x00\x10')  # size
        self.super_missile_door_color.to_stream(data)

        data.write(b'Q\x8b\xcc\xdc')  # 0x518bccdc
        data.write(b'\x00\x10')  # size
        self.seeker_door_color.to_stream(data)

        data.write(b'(S\xfa\x91')  # 0x2853fa91
        data.write(b'\x00\x10')  # size
        self.power_bomb_door_color.to_stream(data)

        data.write(b'\xe6U\xa1\x8e')  # 0xe655a18e
        data.write(b'\x00\x10')  # size
        self.grey_door_color.to_stream(data)

        data.write(b'\x0f\x08\xf3^')  # 0xf08f35e
        data.write(b'\x00\x10')  # size
        self.white_door_color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            num_door_colors=data['num_door_colors'],
            blue_door_color=Color.from_json(data['blue_door_color']),
            missile_door_color=Color.from_json(data['missile_door_color']),
            dark_beam_door_color=Color.from_json(data['dark_beam_door_color']),
            unknown=Color.from_json(data['unknown']),
            annihilator_beam_door_color=Color.from_json(data['annihilator_beam_door_color']),
            light_beam_door_color=Color.from_json(data['light_beam_door_color']),
            super_missile_door_color=Color.from_json(data['super_missile_door_color']),
            seeker_door_color=Color.from_json(data['seeker_door_color']),
            power_bomb_door_color=Color.from_json(data['power_bomb_door_color']),
            grey_door_color=Color.from_json(data['grey_door_color']),
            white_door_color=Color.from_json(data['white_door_color']),
        )

    def to_json(self) -> dict:
        return {
            'num_door_colors': self.num_door_colors,
            'blue_door_color': self.blue_door_color.to_json(),
            'missile_door_color': self.missile_door_color.to_json(),
            'dark_beam_door_color': self.dark_beam_door_color.to_json(),
            'unknown': self.unknown.to_json(),
            'annihilator_beam_door_color': self.annihilator_beam_door_color.to_json(),
            'light_beam_door_color': self.light_beam_door_color.to_json(),
            'super_missile_door_color': self.super_missile_door_color.to_json(),
            'seeker_door_color': self.seeker_door_color.to_json(),
            'power_bomb_door_color': self.power_bomb_door_color.to_json(),
            'grey_door_color': self.grey_door_color.to_json(),
            'white_door_color': self.white_door_color.to_json(),
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_num_door_colors(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_blue_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_dark_beam_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_annihilator_beam_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_light_beam_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_super_missile_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_seeker_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_power_bomb_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_grey_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_white_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4fceb904: ('num_door_colors', _decode_num_door_colors),
    0xb36aa9b7: ('blue_door_color', _decode_blue_door_color),
    0x9620d4a0: ('missile_door_color', _decode_missile_door_color),
    0x4e1a9a8d: ('dark_beam_door_color', _decode_dark_beam_door_color),
    0xce986453: ('unknown', _decode_unknown),
    0x70f36f9: ('annihilator_beam_door_color', _decode_annihilator_beam_door_color),
    0xfada14b6: ('light_beam_door_color', _decode_light_beam_door_color),
    0x172241dc: ('super_missile_door_color', _decode_super_missile_door_color),
    0x518bccdc: ('seeker_door_color', _decode_seeker_door_color),
    0x2853fa91: ('power_bomb_door_color', _decode_power_bomb_door_color),
    0xe655a18e: ('grey_door_color', _decode_grey_door_color),
    0xf08f35e: ('white_door_color', _decode_white_door_color),
}
