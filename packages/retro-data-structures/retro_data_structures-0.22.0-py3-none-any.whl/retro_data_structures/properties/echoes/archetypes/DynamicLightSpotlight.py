# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class DynamicLightSpotlight(BaseProperty):
    spotlight_angle: Spline = dataclasses.field(default_factory=Spline)
    spotlight_angle_duration: float = dataclasses.field(default=0.0)
    spotlight_angle_loops: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xfe\xec\xa0\xd6')  # 0xfeeca0d6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spotlight_angle.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'y\xaay\x8b')  # 0x79aa798b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spotlight_angle_duration))

        data.write(b'/\xd0\x83\x00')  # 0x2fd08300
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.spotlight_angle_loops))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            spotlight_angle=Spline.from_json(data['spotlight_angle']),
            spotlight_angle_duration=data['spotlight_angle_duration'],
            spotlight_angle_loops=data['spotlight_angle_loops'],
        )

    def to_json(self) -> dict:
        return {
            'spotlight_angle': self.spotlight_angle.to_json(),
            'spotlight_angle_duration': self.spotlight_angle_duration,
            'spotlight_angle_loops': self.spotlight_angle_loops,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_spotlight_angle(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_spotlight_angle_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spotlight_angle_loops(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfeeca0d6: ('spotlight_angle', _decode_spotlight_angle),
    0x79aa798b: ('spotlight_angle_duration', _decode_spotlight_angle_duration),
    0x2fd08300: ('spotlight_angle_loops', _decode_spotlight_angle_loops),
}
