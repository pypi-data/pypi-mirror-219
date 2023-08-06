# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class ProportionalConvergence(BaseProperty):
    velocity: float = dataclasses.field(default=0.0)
    dampening_control: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\x02\xf0\x16\x83')  # 0x2f01683
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.velocity))

        data.write(b'\xf7\xfb\xa2\xbf')  # 0xf7fba2bf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dampening_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            velocity=data['velocity'],
            dampening_control=Spline.from_json(data['dampening_control']),
        )

    def to_json(self) -> dict:
        return {
            'velocity': self.velocity,
            'dampening_control': self.dampening_control.to_json(),
        }


def _decode_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dampening_control(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2f01683: ('velocity', _decode_velocity),
    0xf7fba2bf: ('dampening_control', _decode_dampening_control),
}
