# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class SwingRopeData(BaseProperty):
    unknown_0x7e20a7c9: float = dataclasses.field(default=0.05000000074505806)
    rope_blend_mode: enums.RopeBlendMode = dataclasses.field(default=enums.RopeBlendMode.Unknown1)
    no_grab_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    end_cap_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    max_angle: float = dataclasses.field(default=45.0)
    minimum_swing_radius: float = dataclasses.field(default=2.0)
    unknown_0xbf43e511: float = dataclasses.field(default=0.5)
    is_rigid: bool = dataclasses.field(default=False)
    unknown_0x5b5f1a7d: bool = dataclasses.field(default=False)
    unknown_0x2c02f3ca: bool = dataclasses.field(default=False)
    unknown_0x8388e38b: float = dataclasses.field(default=0.0)
    auto_start_auto_swing: bool = dataclasses.field(default=True)
    unknown_0x77c8cc96: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x723a15a5: float = dataclasses.field(default=0.25)
    unknown_0xbecb0936: float = dataclasses.field(default=0.5)
    unknown_0x84594ed5: bool = dataclasses.field(default=False)
    unknown_0x941efaa0: bool = dataclasses.field(default=False)
    unknown_0x36f40c13: int = dataclasses.field(default=0)
    unknown_0x1acb67f5: int = dataclasses.field(default=24)
    unknown_0x087ec81b: int = dataclasses.field(default=24)
    unknown_0xb0c2af7e: int = dataclasses.field(default=24)
    unknown_0x2d1597c7: int = dataclasses.field(default=24)
    unknown_0x95a9f0a2: int = dataclasses.field(default=24)
    unknown_0x871c5f4c: int = dataclasses.field(default=24)
    unknown_0x3fa03829: int = dataclasses.field(default=24)
    unknown_0x67c3287f: int = dataclasses.field(default=24)
    unknown_0xdf7f4f1a: int = dataclasses.field(default=24)
    unknown_0x99c2d4a7: int = dataclasses.field(default=24)

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
        data.write(b'\x00\x1d')  # 29 properties

        data.write(b'~ \xa7\xc9')  # 0x7e20a7c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7e20a7c9))

        data.write(b',2G-')  # 0x2c32472d
        data.write(b'\x00\x04')  # size
        self.rope_blend_mode.to_stream(data)

        data.write(b'\xd9\xdf3\x9a')  # 0xd9df339a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no_grab_texture))

        data.write(b'\xd1\xf6Xr')  # 0xd1f65872
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.texture))

        data.write(b'<^-\x90')  # 0x3c5e2d90
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.end_cap_texture))

        data.write(b'\xd9cU\x83')  # 0xd9635583
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_angle))

        data.write(b'\x92\xac\x886')  # 0x92ac8836
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_swing_radius))

        data.write(b'\xbfC\xe5\x11')  # 0xbf43e511
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbf43e511))

        data.write(b'\xce\x9e\x91x')  # 0xce9e9178
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_rigid))

        data.write(b'[_\x1a}')  # 0x5b5f1a7d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x5b5f1a7d))

        data.write(b',\x02\xf3\xca')  # 0x2c02f3ca
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x2c02f3ca))

        data.write(b'\x83\x88\xe3\x8b')  # 0x8388e38b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8388e38b))

        data.write(b'\t\xee\x1b\x0b')  # 0x9ee1b0b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start_auto_swing))

        data.write(b'w\xc8\xcc\x96')  # 0x77c8cc96
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x77c8cc96.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'r:\x15\xa5')  # 0x723a15a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x723a15a5))

        data.write(b'\xbe\xcb\t6')  # 0xbecb0936
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbecb0936))

        data.write(b'\x84YN\xd5')  # 0x84594ed5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x84594ed5))

        data.write(b'\x94\x1e\xfa\xa0')  # 0x941efaa0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x941efaa0))

        data.write(b'6\xf4\x0c\x13')  # 0x36f40c13
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x36f40c13))

        data.write(b'\x1a\xcbg\xf5')  # 0x1acb67f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x1acb67f5))

        data.write(b'\x08~\xc8\x1b')  # 0x87ec81b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x087ec81b))

        data.write(b'\xb0\xc2\xaf~')  # 0xb0c2af7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xb0c2af7e))

        data.write(b'-\x15\x97\xc7')  # 0x2d1597c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x2d1597c7))

        data.write(b'\x95\xa9\xf0\xa2')  # 0x95a9f0a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x95a9f0a2))

        data.write(b'\x87\x1c_L')  # 0x871c5f4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x871c5f4c))

        data.write(b'?\xa08)')  # 0x3fa03829
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x3fa03829))

        data.write(b'g\xc3(\x7f')  # 0x67c3287f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x67c3287f))

        data.write(b'\xdf\x7fO\x1a')  # 0xdf7f4f1a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xdf7f4f1a))

        data.write(b'\x99\xc2\xd4\xa7')  # 0x99c2d4a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x99c2d4a7))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x7e20a7c9=data['unknown_0x7e20a7c9'],
            rope_blend_mode=enums.RopeBlendMode.from_json(data['rope_blend_mode']),
            no_grab_texture=data['no_grab_texture'],
            texture=data['texture'],
            end_cap_texture=data['end_cap_texture'],
            max_angle=data['max_angle'],
            minimum_swing_radius=data['minimum_swing_radius'],
            unknown_0xbf43e511=data['unknown_0xbf43e511'],
            is_rigid=data['is_rigid'],
            unknown_0x5b5f1a7d=data['unknown_0x5b5f1a7d'],
            unknown_0x2c02f3ca=data['unknown_0x2c02f3ca'],
            unknown_0x8388e38b=data['unknown_0x8388e38b'],
            auto_start_auto_swing=data['auto_start_auto_swing'],
            unknown_0x77c8cc96=Spline.from_json(data['unknown_0x77c8cc96']),
            unknown_0x723a15a5=data['unknown_0x723a15a5'],
            unknown_0xbecb0936=data['unknown_0xbecb0936'],
            unknown_0x84594ed5=data['unknown_0x84594ed5'],
            unknown_0x941efaa0=data['unknown_0x941efaa0'],
            unknown_0x36f40c13=data['unknown_0x36f40c13'],
            unknown_0x1acb67f5=data['unknown_0x1acb67f5'],
            unknown_0x087ec81b=data['unknown_0x087ec81b'],
            unknown_0xb0c2af7e=data['unknown_0xb0c2af7e'],
            unknown_0x2d1597c7=data['unknown_0x2d1597c7'],
            unknown_0x95a9f0a2=data['unknown_0x95a9f0a2'],
            unknown_0x871c5f4c=data['unknown_0x871c5f4c'],
            unknown_0x3fa03829=data['unknown_0x3fa03829'],
            unknown_0x67c3287f=data['unknown_0x67c3287f'],
            unknown_0xdf7f4f1a=data['unknown_0xdf7f4f1a'],
            unknown_0x99c2d4a7=data['unknown_0x99c2d4a7'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x7e20a7c9': self.unknown_0x7e20a7c9,
            'rope_blend_mode': self.rope_blend_mode.to_json(),
            'no_grab_texture': self.no_grab_texture,
            'texture': self.texture,
            'end_cap_texture': self.end_cap_texture,
            'max_angle': self.max_angle,
            'minimum_swing_radius': self.minimum_swing_radius,
            'unknown_0xbf43e511': self.unknown_0xbf43e511,
            'is_rigid': self.is_rigid,
            'unknown_0x5b5f1a7d': self.unknown_0x5b5f1a7d,
            'unknown_0x2c02f3ca': self.unknown_0x2c02f3ca,
            'unknown_0x8388e38b': self.unknown_0x8388e38b,
            'auto_start_auto_swing': self.auto_start_auto_swing,
            'unknown_0x77c8cc96': self.unknown_0x77c8cc96.to_json(),
            'unknown_0x723a15a5': self.unknown_0x723a15a5,
            'unknown_0xbecb0936': self.unknown_0xbecb0936,
            'unknown_0x84594ed5': self.unknown_0x84594ed5,
            'unknown_0x941efaa0': self.unknown_0x941efaa0,
            'unknown_0x36f40c13': self.unknown_0x36f40c13,
            'unknown_0x1acb67f5': self.unknown_0x1acb67f5,
            'unknown_0x087ec81b': self.unknown_0x087ec81b,
            'unknown_0xb0c2af7e': self.unknown_0xb0c2af7e,
            'unknown_0x2d1597c7': self.unknown_0x2d1597c7,
            'unknown_0x95a9f0a2': self.unknown_0x95a9f0a2,
            'unknown_0x871c5f4c': self.unknown_0x871c5f4c,
            'unknown_0x3fa03829': self.unknown_0x3fa03829,
            'unknown_0x67c3287f': self.unknown_0x67c3287f,
            'unknown_0xdf7f4f1a': self.unknown_0xdf7f4f1a,
            'unknown_0x99c2d4a7': self.unknown_0x99c2d4a7,
        }


def _decode_unknown_0x7e20a7c9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rope_blend_mode(data: typing.BinaryIO, property_size: int):
    return enums.RopeBlendMode.from_stream(data)


def _decode_no_grab_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_end_cap_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_max_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_swing_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbf43e511(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_rigid(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x5b5f1a7d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x2c02f3ca(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x8388e38b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_auto_start_auto_swing(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x77c8cc96(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x723a15a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbecb0936(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x84594ed5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x941efaa0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x36f40c13(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1acb67f5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x087ec81b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb0c2af7e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x2d1597c7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x95a9f0a2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x871c5f4c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x3fa03829(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x67c3287f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xdf7f4f1a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x99c2d4a7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7e20a7c9: ('unknown_0x7e20a7c9', _decode_unknown_0x7e20a7c9),
    0x2c32472d: ('rope_blend_mode', _decode_rope_blend_mode),
    0xd9df339a: ('no_grab_texture', _decode_no_grab_texture),
    0xd1f65872: ('texture', _decode_texture),
    0x3c5e2d90: ('end_cap_texture', _decode_end_cap_texture),
    0xd9635583: ('max_angle', _decode_max_angle),
    0x92ac8836: ('minimum_swing_radius', _decode_minimum_swing_radius),
    0xbf43e511: ('unknown_0xbf43e511', _decode_unknown_0xbf43e511),
    0xce9e9178: ('is_rigid', _decode_is_rigid),
    0x5b5f1a7d: ('unknown_0x5b5f1a7d', _decode_unknown_0x5b5f1a7d),
    0x2c02f3ca: ('unknown_0x2c02f3ca', _decode_unknown_0x2c02f3ca),
    0x8388e38b: ('unknown_0x8388e38b', _decode_unknown_0x8388e38b),
    0x9ee1b0b: ('auto_start_auto_swing', _decode_auto_start_auto_swing),
    0x77c8cc96: ('unknown_0x77c8cc96', _decode_unknown_0x77c8cc96),
    0x723a15a5: ('unknown_0x723a15a5', _decode_unknown_0x723a15a5),
    0xbecb0936: ('unknown_0xbecb0936', _decode_unknown_0xbecb0936),
    0x84594ed5: ('unknown_0x84594ed5', _decode_unknown_0x84594ed5),
    0x941efaa0: ('unknown_0x941efaa0', _decode_unknown_0x941efaa0),
    0x36f40c13: ('unknown_0x36f40c13', _decode_unknown_0x36f40c13),
    0x1acb67f5: ('unknown_0x1acb67f5', _decode_unknown_0x1acb67f5),
    0x87ec81b: ('unknown_0x087ec81b', _decode_unknown_0x087ec81b),
    0xb0c2af7e: ('unknown_0xb0c2af7e', _decode_unknown_0xb0c2af7e),
    0x2d1597c7: ('unknown_0x2d1597c7', _decode_unknown_0x2d1597c7),
    0x95a9f0a2: ('unknown_0x95a9f0a2', _decode_unknown_0x95a9f0a2),
    0x871c5f4c: ('unknown_0x871c5f4c', _decode_unknown_0x871c5f4c),
    0x3fa03829: ('unknown_0x3fa03829', _decode_unknown_0x3fa03829),
    0x67c3287f: ('unknown_0x67c3287f', _decode_unknown_0x67c3287f),
    0xdf7f4f1a: ('unknown_0xdf7f4f1a', _decode_unknown_0xdf7f4f1a),
    0x99c2d4a7: ('unknown_0x99c2d4a7', _decode_unknown_0x99c2d4a7),
}
