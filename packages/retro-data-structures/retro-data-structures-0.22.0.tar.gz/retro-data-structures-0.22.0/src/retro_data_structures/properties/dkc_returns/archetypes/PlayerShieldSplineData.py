# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class PlayerShieldSplineData(BaseProperty):
    health_equal_or_greater_than: int = dataclasses.field(default=10)
    shield_visual_spline: Spline = dataclasses.field(default_factory=Spline)

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

        data.write(b'9\xe3`L')  # 0x39e3604c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.health_equal_or_greater_than))

        data.write(b'\xfe\x8f\x08\x86')  # 0xfe8f0886
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shield_visual_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            health_equal_or_greater_than=data['health_equal_or_greater_than'],
            shield_visual_spline=Spline.from_json(data['shield_visual_spline']),
        )

    def to_json(self) -> dict:
        return {
            'health_equal_or_greater_than': self.health_equal_or_greater_than,
            'shield_visual_spline': self.shield_visual_spline.to_json(),
        }


def _decode_health_equal_or_greater_than(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_shield_visual_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x39e3604c: ('health_equal_or_greater_than', _decode_health_equal_or_greater_than),
    0xfe8f0886: ('shield_visual_spline', _decode_shield_visual_spline),
}
