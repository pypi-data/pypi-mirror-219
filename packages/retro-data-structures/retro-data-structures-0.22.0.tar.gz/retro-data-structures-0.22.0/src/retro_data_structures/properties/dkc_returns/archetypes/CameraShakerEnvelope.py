# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class CameraShakerEnvelope(BaseProperty):
    shake_shape: enums.ShakeShape = dataclasses.field(default=enums.ShakeShape.Unknown1)
    amplitude: Spline = dataclasses.field(default_factory=Spline)
    period: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xc6\x08\x9a?')  # 0xc6089a3f
        data.write(b'\x00\x04')  # size
        self.shake_shape.to_stream(data)

        data.write(b'\x90\xb3\xcc~')  # 0x90b3cc7e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.amplitude.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i\xa8\x15\x17')  # 0x69a81517
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.period.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            shake_shape=enums.ShakeShape.from_json(data['shake_shape']),
            amplitude=Spline.from_json(data['amplitude']),
            period=Spline.from_json(data['period']),
        )

    def to_json(self) -> dict:
        return {
            'shake_shape': self.shake_shape.to_json(),
            'amplitude': self.amplitude.to_json(),
            'period': self.period.to_json(),
        }


def _decode_shake_shape(data: typing.BinaryIO, property_size: int):
    return enums.ShakeShape.from_stream(data)


def _decode_amplitude(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_period(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc6089a3f: ('shake_shape', _decode_shake_shape),
    0x90b3cc7e: ('amplitude', _decode_amplitude),
    0x69a81517: ('period', _decode_period),
}
