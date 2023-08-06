# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class PlayerOffscreenIndicatorIconData(BaseProperty):
    indicator_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    blend_mode: enums.BlendMode = dataclasses.field(default=enums.BlendMode.Unknown1)
    override_width: int = dataclasses.field(default=0)
    override_height: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'5\xa9=\xd5')  # 0x35a93dd5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.indicator_texture))

        data.write(b'\xcd\x0bM\t')  # 0xcd0b4d09
        data.write(b'\x00\x04')  # size
        self.blend_mode.to_stream(data)

        data.write(b'\xa3\xc8\xf0m')  # 0xa3c8f06d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.override_width))

        data.write(b'\xb3\x9a\x8a6')  # 0xb39a8a36
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.override_height))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            indicator_texture=data['indicator_texture'],
            blend_mode=enums.BlendMode.from_json(data['blend_mode']),
            override_width=data['override_width'],
            override_height=data['override_height'],
        )

    def to_json(self) -> dict:
        return {
            'indicator_texture': self.indicator_texture,
            'blend_mode': self.blend_mode.to_json(),
            'override_width': self.override_width,
            'override_height': self.override_height,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x35a93dd5, 0xcd0b4d09, 0xa3c8f06d, 0xb39a8a36)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerOffscreenIndicatorIconData]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHLLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(44))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerOffscreenIndicatorIconData(
        dec[2],
        enums.BlendMode(dec[5]),
        dec[8],
        dec[11],
    )


def _decode_indicator_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_blend_mode(data: typing.BinaryIO, property_size: int):
    return enums.BlendMode.from_stream(data)


def _decode_override_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_override_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x35a93dd5: ('indicator_texture', _decode_indicator_texture),
    0xcd0b4d09: ('blend_mode', _decode_blend_mode),
    0xa3c8f06d: ('override_width', _decode_override_width),
    0xb39a8a36: ('override_height', _decode_override_height),
}
