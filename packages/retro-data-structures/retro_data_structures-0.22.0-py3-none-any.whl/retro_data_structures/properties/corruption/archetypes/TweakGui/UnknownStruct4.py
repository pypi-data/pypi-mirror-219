# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct4(BaseProperty):
    outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    stripe_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    stripe_scale: float = dataclasses.field(default=1.0)
    min_random_stripe_wipe_speed: float = dataclasses.field(default=0.5)
    max_random_stripe_wipe_speed: float = dataclasses.field(default=1.0)
    unknown_0x8c9a8472: float = dataclasses.field(default=0.5)
    unknown_0x3ca59e4e: float = dataclasses.field(default=1.0)

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

        data.write(b'`\xd7\x85i')  # 0x60d78569
        data.write(b'\x00\x10')  # size
        self.outline_color.to_stream(data)

        data.write(b'\xd2\xe9,7')  # 0xd2e92c37
        data.write(b'\x00\x10')  # size
        self.stripe_color.to_stream(data)

        data.write(b'\xc9\x7fZ\xdc')  # 0xc97f5adc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stripe_scale))

        data.write(b'8\xdb\rc')  # 0x38db0d63
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_random_stripe_wipe_speed))

        data.write(b'\xd7Y\x13\x19')  # 0xd7591319
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_random_stripe_wipe_speed))

        data.write(b'\x8c\x9a\x84r')  # 0x8c9a8472
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8c9a8472))

        data.write(b'<\xa5\x9eN')  # 0x3ca59e4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3ca59e4e))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            outline_color=Color.from_json(data['outline_color']),
            stripe_color=Color.from_json(data['stripe_color']),
            stripe_scale=data['stripe_scale'],
            min_random_stripe_wipe_speed=data['min_random_stripe_wipe_speed'],
            max_random_stripe_wipe_speed=data['max_random_stripe_wipe_speed'],
            unknown_0x8c9a8472=data['unknown_0x8c9a8472'],
            unknown_0x3ca59e4e=data['unknown_0x3ca59e4e'],
        )

    def to_json(self) -> dict:
        return {
            'outline_color': self.outline_color.to_json(),
            'stripe_color': self.stripe_color.to_json(),
            'stripe_scale': self.stripe_scale,
            'min_random_stripe_wipe_speed': self.min_random_stripe_wipe_speed,
            'max_random_stripe_wipe_speed': self.max_random_stripe_wipe_speed,
            'unknown_0x8c9a8472': self.unknown_0x8c9a8472,
            'unknown_0x3ca59e4e': self.unknown_0x3ca59e4e,
        }


def _decode_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_stripe_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_stripe_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_random_stripe_wipe_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_random_stripe_wipe_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8c9a8472(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3ca59e4e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x60d78569: ('outline_color', _decode_outline_color),
    0xd2e92c37: ('stripe_color', _decode_stripe_color),
    0xc97f5adc: ('stripe_scale', _decode_stripe_scale),
    0x38db0d63: ('min_random_stripe_wipe_speed', _decode_min_random_stripe_wipe_speed),
    0xd7591319: ('max_random_stripe_wipe_speed', _decode_max_random_stripe_wipe_speed),
    0x8c9a8472: ('unknown_0x8c9a8472', _decode_unknown_0x8c9a8472),
    0x3ca59e4e: ('unknown_0x3ca59e4e', _decode_unknown_0x3ca59e4e),
}
