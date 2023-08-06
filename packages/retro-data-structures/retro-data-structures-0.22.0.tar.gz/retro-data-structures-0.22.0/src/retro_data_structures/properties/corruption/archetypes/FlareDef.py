# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class FlareDef(BaseProperty):
    texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    position: float = dataclasses.field(default=0.0)
    scale: float = dataclasses.field(default=1.0)
    color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xd1\xf6Xr')  # 0xd1f65872
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.texture))

        data.write(b'\xcb\x99\xb4\xda')  # 0xcb99b4da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.position))

        data.write(b',Q\xa6v')  # 0x2c51a676
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scale))

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            texture=data['texture'],
            position=data['position'],
            scale=data['scale'],
            color=Color.from_json(data['color']),
        )

    def to_json(self) -> dict:
        return {
            'texture': self.texture,
            'position': self.position,
            'scale': self.scale,
            'color': self.color.to_json(),
        }


def _decode_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_position(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd1f65872: ('texture', _decode_texture),
    0xcb99b4da: ('position', _decode_position),
    0x2c51a676: ('scale', _decode_scale),
    0x37c7d09d: ('color', _decode_color),
}
