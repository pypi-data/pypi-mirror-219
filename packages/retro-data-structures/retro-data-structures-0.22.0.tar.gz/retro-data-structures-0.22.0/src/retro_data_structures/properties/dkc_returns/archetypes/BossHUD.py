# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class BossHUD(BaseProperty):
    boss_hud_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)

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
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'\x8bL\x10,')  # 0x8b4c102c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.boss_hud_frame))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            boss_hud_frame=data['boss_hud_frame'],
        )

    def to_json(self) -> dict:
        return {
            'boss_hud_frame': self.boss_hud_frame,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x8b4c102c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[BossHUD]:
    if property_count != 1:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(14))
    if (dec[0]) != _FAST_IDS:
        data.seek(before)
        return None

    return BossHUD(
        dec[2],
    )


def _decode_boss_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8b4c102c: ('boss_hud_frame', _decode_boss_hud_frame),
}
