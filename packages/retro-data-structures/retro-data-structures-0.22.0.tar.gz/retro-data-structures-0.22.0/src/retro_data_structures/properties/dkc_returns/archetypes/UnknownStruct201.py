# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class UnknownStruct201(BaseProperty):
    unknown: int = dataclasses.field(default=1694551927)  # Choice
    turn_rate: float = dataclasses.field(default=90.0)
    velocity: Spline = dataclasses.field(default_factory=Spline)

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

        data.write(b'|q\xcb\xad')  # 0x7c71cbad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown))

        data.write(b'\xe3M\xc7\x03')  # 0xe34dc703
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_rate))

        data.write(b'\x13\xebZ}')  # 0x13eb5a7d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.velocity.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            turn_rate=data['turn_rate'],
            velocity=Spline.from_json(data['velocity']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'turn_rate': self.turn_rate,
            'velocity': self.velocity.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_turn_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_velocity(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7c71cbad: ('unknown', _decode_unknown),
    0xe34dc703: ('turn_rate', _decode_turn_rate),
    0x13eb5a7d: ('velocity', _decode_velocity),
}
