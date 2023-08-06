# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct151(BaseProperty):
    hud_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    text_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    confirm_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    cancel_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)

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

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b'\xe6\xf6\xe2p')  # 0xe6f6e270
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_string))

        data.write(b'O\xab\xac\t')  # 0x4fabac09
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.confirm_string))

        data.write(b'\xcbj\xf8\x9b')  # 0xcb6af89b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cancel_string))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hud_frame=data['hud_frame'],
            text_string=data['text_string'],
            confirm_string=data['confirm_string'],
            cancel_string=data['cancel_string'],
        )

    def to_json(self) -> dict:
        return {
            'hud_frame': self.hud_frame,
            'text_string': self.text_string,
            'confirm_string': self.confirm_string,
            'cancel_string': self.cancel_string,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf2299ed6, 0xe6f6e270, 0x4fabac09, 0xcb6af89b)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct151]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(56))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct151(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_confirm_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cancel_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0xe6f6e270: ('text_string', _decode_text_string),
    0x4fabac09: ('confirm_string', _decode_confirm_string),
    0xcb6af89b: ('cancel_string', _decode_cancel_string),
}
