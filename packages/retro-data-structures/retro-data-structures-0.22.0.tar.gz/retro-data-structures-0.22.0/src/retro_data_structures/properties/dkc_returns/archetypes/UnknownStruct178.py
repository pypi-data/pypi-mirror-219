# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct178(BaseProperty):
    gui_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    unknown_0x1dd553a2: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_0x765f0301: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\x1d\xd5S\xa2')  # 0x1dd553a2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x1dd553a2))

        data.write(b'v_\x03\x01')  # 0x765f0301
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x765f0301))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gui_frame=data['gui_frame'],
            unknown_0x1dd553a2=data['unknown_0x1dd553a2'],
            unknown_0x765f0301=data['unknown_0x765f0301'],
        )

    def to_json(self) -> dict:
        return {
            'gui_frame': self.gui_frame,
            'unknown_0x1dd553a2': self.unknown_0x1dd553a2,
            'unknown_0x765f0301': self.unknown_0x765f0301,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x806052cb, 0x1dd553a2, 0x765f0301)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct178]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(42))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct178(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x1dd553a2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x765f0301(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x1dd553a2: ('unknown_0x1dd553a2', _decode_unknown_0x1dd553a2),
    0x765f0301: ('unknown_0x765f0301', _decode_unknown_0x765f0301),
}
