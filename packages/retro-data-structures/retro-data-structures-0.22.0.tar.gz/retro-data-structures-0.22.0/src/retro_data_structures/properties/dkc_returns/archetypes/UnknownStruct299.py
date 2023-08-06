# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct299(BaseProperty):
    enabled: bool = dataclasses.field(default=False)
    color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))

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

        data.write(b")\xc7}'")  # 0x29c77d27
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enabled))

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            enabled=data['enabled'],
            color=Color.from_json(data['color']),
        )

    def to_json(self) -> dict:
        return {
            'enabled': self.enabled,
            'color': self.color.to_json(),
        }


def _decode_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x29c77d27: ('enabled', _decode_enabled),
    0x37c7d09d: ('color', _decode_color),
}
