# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ShadowData(BaseProperty):
    unknown_0xcecb77dd: bool = dataclasses.field(default=False)
    shadow_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    edge_adjust: enums.EdgeAdjust = dataclasses.field(default=enums.EdgeAdjust.Unknown1)
    minimum_opacity: float = dataclasses.field(default=0.25)
    maximum_opacity: float = dataclasses.field(default=0.75)
    unknown_0x1524c118: float = dataclasses.field(default=0.25)
    unknown_0xc7c4c8a9: float = dataclasses.field(default=1.0)
    unknown_0x565c73a2: float = dataclasses.field(default=20.0)
    floor_offset: float = dataclasses.field(default=0.05000000074505806)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xce\xcbw\xdd')  # 0xcecb77dd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xcecb77dd))

        data.write(b'd\xc0\xc5O')  # 0x64c0c54f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shadow_texture))

        data.write(b'y\xcf\xa7u')  # 0x79cfa775
        data.write(b'\x00\x04')  # size
        self.edge_adjust.to_stream(data)

        data.write(b'\x1c\xf3\xf4h')  # 0x1cf3f468
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_opacity))

        data.write(b'\xbb\xc7t\x11')  # 0xbbc77411
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_opacity))

        data.write(b'\x15$\xc1\x18')  # 0x1524c118
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1524c118))

        data.write(b'\xc7\xc4\xc8\xa9')  # 0xc7c4c8a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc7c4c8a9))

        data.write(b'V\\s\xa2')  # 0x565c73a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x565c73a2))

        data.write(b'\x80\x8e\x9e2')  # 0x808e9e32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.floor_offset))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xcecb77dd=data['unknown_0xcecb77dd'],
            shadow_texture=data['shadow_texture'],
            edge_adjust=enums.EdgeAdjust.from_json(data['edge_adjust']),
            minimum_opacity=data['minimum_opacity'],
            maximum_opacity=data['maximum_opacity'],
            unknown_0x1524c118=data['unknown_0x1524c118'],
            unknown_0xc7c4c8a9=data['unknown_0xc7c4c8a9'],
            unknown_0x565c73a2=data['unknown_0x565c73a2'],
            floor_offset=data['floor_offset'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xcecb77dd': self.unknown_0xcecb77dd,
            'shadow_texture': self.shadow_texture,
            'edge_adjust': self.edge_adjust.to_json(),
            'minimum_opacity': self.minimum_opacity,
            'maximum_opacity': self.maximum_opacity,
            'unknown_0x1524c118': self.unknown_0x1524c118,
            'unknown_0xc7c4c8a9': self.unknown_0xc7c4c8a9,
            'unknown_0x565c73a2': self.unknown_0x565c73a2,
            'floor_offset': self.floor_offset,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xcecb77dd, 0x64c0c54f, 0x79cfa775, 0x1cf3f468, 0xbbc77411, 0x1524c118, 0xc7c4c8a9, 0x565c73a2, 0x808e9e32)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ShadowData]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHQLHLLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(91))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return ShadowData(
        dec[2],
        dec[5],
        enums.EdgeAdjust(dec[8]),
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
    )


def _decode_unknown_0xcecb77dd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shadow_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_edge_adjust(data: typing.BinaryIO, property_size: int):
    return enums.EdgeAdjust.from_stream(data)


def _decode_minimum_opacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_opacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1524c118(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc7c4c8a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x565c73a2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_floor_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcecb77dd: ('unknown_0xcecb77dd', _decode_unknown_0xcecb77dd),
    0x64c0c54f: ('shadow_texture', _decode_shadow_texture),
    0x79cfa775: ('edge_adjust', _decode_edge_adjust),
    0x1cf3f468: ('minimum_opacity', _decode_minimum_opacity),
    0xbbc77411: ('maximum_opacity', _decode_maximum_opacity),
    0x1524c118: ('unknown_0x1524c118', _decode_unknown_0x1524c118),
    0xc7c4c8a9: ('unknown_0xc7c4c8a9', _decode_unknown_0xc7c4c8a9),
    0x565c73a2: ('unknown_0x565c73a2', _decode_unknown_0x565c73a2),
    0x808e9e32: ('floor_offset', _decode_floor_offset),
}
