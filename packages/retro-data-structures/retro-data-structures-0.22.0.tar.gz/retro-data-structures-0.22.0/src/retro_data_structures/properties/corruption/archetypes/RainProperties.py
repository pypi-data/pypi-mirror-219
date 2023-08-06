# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.LayerInfo import LayerInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class RainProperties(BaseProperty):
    color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.1490200012922287))
    velocity: float = dataclasses.field(default=-40.0)
    min_length: float = dataclasses.field(default=1.0)
    max_length: float = dataclasses.field(default=3.0)
    near_width: float = dataclasses.field(default=6.0)
    far_width: float = dataclasses.field(default=6.0)
    unknown: float = dataclasses.field(default=50.0)
    sheet_texture: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    sheet_motion: LayerInfo = dataclasses.field(default_factory=LayerInfo)
    enable_sheet: bool = dataclasses.field(default=True)
    rain_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    density_volume_spline: Spline = dataclasses.field(default_factory=Spline)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'7\xc7\xd0\x9d')  # 0x37c7d09d
        data.write(b'\x00\x10')  # size
        self.color.to_stream(data)

        data.write(b'\x02\xf0\x16\x83')  # 0x2f01683
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.velocity))

        data.write(b'\xc6\x16\t=')  # 0xc616093d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_length))

        data.write(b'\x7f0\x92L')  # 0x7f30924c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_length))

        data.write(b'\xae\xadRY')  # 0xaead5259
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.near_width))

        data.write(b'\xf4\xf4\xe8V')  # 0xf4f4e856
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.far_width))

        data.write(b'p\x8d\xfe\x03')  # 0x708dfe03
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'3\x99\xd6[')  # 0x3399d65b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sheet_texture))

        data.write(b'\x84v\xc5|')  # 0x8476c57c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sheet_motion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\xebMW')  # 0x5deb4d57
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_sheet))

        data.write(b'55Z\x0b')  # 0x35355a0b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rain_sound))

        data.write(b'\x1aY\xb7\x81')  # 0x1a59b781
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.density_volume_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            color=Color.from_json(data['color']),
            velocity=data['velocity'],
            min_length=data['min_length'],
            max_length=data['max_length'],
            near_width=data['near_width'],
            far_width=data['far_width'],
            unknown=data['unknown'],
            sheet_texture=data['sheet_texture'],
            sheet_motion=LayerInfo.from_json(data['sheet_motion']),
            enable_sheet=data['enable_sheet'],
            rain_sound=data['rain_sound'],
            density_volume_spline=Spline.from_json(data['density_volume_spline']),
        )

    def to_json(self) -> dict:
        return {
            'color': self.color.to_json(),
            'velocity': self.velocity,
            'min_length': self.min_length,
            'max_length': self.max_length,
            'near_width': self.near_width,
            'far_width': self.far_width,
            'unknown': self.unknown,
            'sheet_texture': self.sheet_texture,
            'sheet_motion': self.sheet_motion.to_json(),
            'enable_sheet': self.enable_sheet,
            'rain_sound': self.rain_sound,
            'density_volume_spline': self.density_volume_spline.to_json(),
        }


def _decode_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_near_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_far_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sheet_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sheet_motion(data: typing.BinaryIO, property_size: int):
    return LayerInfo.from_stream(data, property_size)


def _decode_enable_sheet(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rain_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_density_volume_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x37c7d09d: ('color', _decode_color),
    0x2f01683: ('velocity', _decode_velocity),
    0xc616093d: ('min_length', _decode_min_length),
    0x7f30924c: ('max_length', _decode_max_length),
    0xaead5259: ('near_width', _decode_near_width),
    0xf4f4e856: ('far_width', _decode_far_width),
    0x708dfe03: ('unknown', _decode_unknown),
    0x3399d65b: ('sheet_texture', _decode_sheet_texture),
    0x8476c57c: ('sheet_motion', _decode_sheet_motion),
    0x5deb4d57: ('enable_sheet', _decode_enable_sheet),
    0x35355a0b: ('rain_sound', _decode_rain_sound),
    0x1a59b781: ('density_volume_spline', _decode_density_volume_spline),
}
