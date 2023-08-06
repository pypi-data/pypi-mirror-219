# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class DynamicLightFalloff(BaseProperty):
    falloff_type: int = dataclasses.field(default=0)
    falloff_rate: Spline = dataclasses.field(default_factory=Spline)
    falloff_rate_duration: float = dataclasses.field(default=0.0)
    falloff_rate_loops: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'Em\xf2\x0c')  # 0x456df20c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.falloff_type))

        data.write(b'/|c\xa3')  # 0x2f7c63a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.falloff_rate.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1fh\x13\xf1')  # 0x1f6813f1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.falloff_rate_duration))

        data.write(b'm2>\xa3')  # 0x6d323ea3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.falloff_rate_loops))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            falloff_type=data['falloff_type'],
            falloff_rate=Spline.from_json(data['falloff_rate']),
            falloff_rate_duration=data['falloff_rate_duration'],
            falloff_rate_loops=data['falloff_rate_loops'],
        )

    def to_json(self) -> dict:
        return {
            'falloff_type': self.falloff_type,
            'falloff_rate': self.falloff_rate.to_json(),
            'falloff_rate_duration': self.falloff_rate_duration,
            'falloff_rate_loops': self.falloff_rate_loops,
        }

    def dependencies_for(self, asset_manager):
        yield from []


def _decode_falloff_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_falloff_rate(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_falloff_rate_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_falloff_rate_loops(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x456df20c: ('falloff_type', _decode_falloff_type),
    0x2f7c63a3: ('falloff_rate', _decode_falloff_rate),
    0x1f6813f1: ('falloff_rate_duration', _decode_falloff_rate_duration),
    0x6d323ea3: ('falloff_rate_loops', _decode_falloff_rate_loops),
}
