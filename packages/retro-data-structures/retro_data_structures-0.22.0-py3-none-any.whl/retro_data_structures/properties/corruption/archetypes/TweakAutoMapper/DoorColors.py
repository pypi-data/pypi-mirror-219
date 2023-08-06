# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class DoorColors(BaseProperty):
    power_beam_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    nova_beam_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    plasma_beam_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    missile_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    ice_missile_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    seeker_missile_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    grapple_voltage_door_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xe9\xd55\x9d')  # 0xe9d5359d
        data.write(b'\x00\x10')  # size
        self.power_beam_door_color.to_stream(data)

        data.write(b'9>\x89\x90')  # 0x393e8990
        data.write(b'\x00\x10')  # size
        self.nova_beam_door_color.to_stream(data)

        data.write(b'\x96\xf5%:')  # 0x96f5253a
        data.write(b'\x00\x10')  # size
        self.plasma_beam_door_color.to_stream(data)

        data.write(b'\x96 \xd4\xa0')  # 0x9620d4a0
        data.write(b'\x00\x10')  # size
        self.missile_door_color.to_stream(data)

        data.write(b'y\x83\x12v')  # 0x79831276
        data.write(b'\x00\x10')  # size
        self.ice_missile_door_color.to_stream(data)

        data.write(b'Z\xc1{c')  # 0x5ac17b63
        data.write(b'\x00\x10')  # size
        self.seeker_missile_door_color.to_stream(data)

        data.write(b'i\xe2<\xf3')  # 0x69e23cf3
        data.write(b'\x00\x10')  # size
        self.grapple_voltage_door_color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            power_beam_door_color=Color.from_json(data['power_beam_door_color']),
            nova_beam_door_color=Color.from_json(data['nova_beam_door_color']),
            plasma_beam_door_color=Color.from_json(data['plasma_beam_door_color']),
            missile_door_color=Color.from_json(data['missile_door_color']),
            ice_missile_door_color=Color.from_json(data['ice_missile_door_color']),
            seeker_missile_door_color=Color.from_json(data['seeker_missile_door_color']),
            grapple_voltage_door_color=Color.from_json(data['grapple_voltage_door_color']),
        )

    def to_json(self) -> dict:
        return {
            'power_beam_door_color': self.power_beam_door_color.to_json(),
            'nova_beam_door_color': self.nova_beam_door_color.to_json(),
            'plasma_beam_door_color': self.plasma_beam_door_color.to_json(),
            'missile_door_color': self.missile_door_color.to_json(),
            'ice_missile_door_color': self.ice_missile_door_color.to_json(),
            'seeker_missile_door_color': self.seeker_missile_door_color.to_json(),
            'grapple_voltage_door_color': self.grapple_voltage_door_color.to_json(),
        }


def _decode_power_beam_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_nova_beam_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_plasma_beam_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_missile_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_ice_missile_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_seeker_missile_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_grapple_voltage_door_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe9d5359d: ('power_beam_door_color', _decode_power_beam_door_color),
    0x393e8990: ('nova_beam_door_color', _decode_nova_beam_door_color),
    0x96f5253a: ('plasma_beam_door_color', _decode_plasma_beam_door_color),
    0x9620d4a0: ('missile_door_color', _decode_missile_door_color),
    0x79831276: ('ice_missile_door_color', _decode_ice_missile_door_color),
    0x5ac17b63: ('seeker_missile_door_color', _decode_seeker_missile_door_color),
    0x69e23cf3: ('grapple_voltage_door_color', _decode_grapple_voltage_door_color),
}
