# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class InterpolationMethod(BaseProperty):
    interpolation_control_type: enums.InterpolationControlType = dataclasses.field(default=enums.InterpolationControlType.Unknown2)
    control_spline: Spline = dataclasses.field(default_factory=Spline)
    ease_in: float = dataclasses.field(default=0.25)
    ease_out: float = dataclasses.field(default=0.75)
    duration: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\t\xb5\x95}')  # 0x9b5957d
        data.write(b'\x00\x04')  # size
        self.interpolation_control_type.to_stream(data)

        data.write(b'\x15V\x7f\xe7')  # 0x15567fe7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\x8d27')  # 0xb08d3237
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ease_in))

        data.write(b'g\xe3\x83j')  # 0x67e3836a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ease_out))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            interpolation_control_type=enums.InterpolationControlType.from_json(data['interpolation_control_type']),
            control_spline=Spline.from_json(data['control_spline']),
            ease_in=data['ease_in'],
            ease_out=data['ease_out'],
            duration=data['duration'],
        )

    def to_json(self) -> dict:
        return {
            'interpolation_control_type': self.interpolation_control_type.to_json(),
            'control_spline': self.control_spline.to_json(),
            'ease_in': self.ease_in,
            'ease_out': self.ease_out,
            'duration': self.duration,
        }


def _decode_interpolation_control_type(data: typing.BinaryIO, property_size: int):
    return enums.InterpolationControlType.from_stream(data)


def _decode_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_ease_in(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ease_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9b5957d: ('interpolation_control_type', _decode_interpolation_control_type),
    0x15567fe7: ('control_spline', _decode_control_spline),
    0xb08d3237: ('ease_in', _decode_ease_in),
    0x67e3836a: ('ease_out', _decode_ease_out),
    0x8b51e23f: ('duration', _decode_duration),
}
