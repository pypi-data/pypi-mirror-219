# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct158(BaseProperty):
    caud_0x31bd7c5d: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x2a3fc965: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'1\xbd|]')  # 0x31bd7c5d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x31bd7c5d))

        data.write(b'*?\xc9e')  # 0x2a3fc965
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x2a3fc965))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            caud_0x31bd7c5d=data['caud_0x31bd7c5d'],
            caud_0x2a3fc965=data['caud_0x2a3fc965'],
        )

    def to_json(self) -> dict:
        return {
            'caud_0x31bd7c5d': self.caud_0x31bd7c5d,
            'caud_0x2a3fc965': self.caud_0x2a3fc965,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x31bd7c5d, 0x2a3fc965)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct158]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(28))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct158(
        dec[2],
        dec[5],
    )


def _decode_caud_0x31bd7c5d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x2a3fc965(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x31bd7c5d: ('caud_0x31bd7c5d', _decode_caud_0x31bd7c5d),
    0x2a3fc965: ('caud_0x2a3fc965', _decode_caud_0x2a3fc965),
}
