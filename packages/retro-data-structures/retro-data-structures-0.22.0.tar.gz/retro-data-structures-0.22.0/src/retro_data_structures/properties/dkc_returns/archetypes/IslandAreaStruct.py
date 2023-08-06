# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class IslandAreaStruct(BaseProperty):
    cost: int = dataclasses.field(default=0)
    purchase_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    comment_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)

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

        data.write(b'_\xed\\\x9d')  # 0x5fed5c9d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.cost))

        data.write(b'\x0c[M\xe6')  # 0xc5b4de6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.purchase_text))

        data.write(b'\x01At5')  # 0x1417435
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.comment_text))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            cost=data['cost'],
            purchase_text=data['purchase_text'],
            comment_text=data['comment_text'],
        )

    def to_json(self) -> dict:
        return {
            'cost': self.cost,
            'purchase_text': self.purchase_text,
            'comment_text': self.comment_text,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x5fed5c9d, 0xc5b4de6, 0x1417435)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[IslandAreaStruct]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(38))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return IslandAreaStruct(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_cost(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_purchase_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_comment_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5fed5c9d: ('cost', _decode_cost),
    0xc5b4de6: ('purchase_text', _decode_purchase_text),
    0x1417435: ('comment_text', _decode_comment_text),
}
