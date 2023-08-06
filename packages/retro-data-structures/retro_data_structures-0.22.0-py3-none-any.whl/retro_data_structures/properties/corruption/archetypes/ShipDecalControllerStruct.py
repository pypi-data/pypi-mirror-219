# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ShipDecalControllerStruct(BaseProperty):
    save_game: enums.SaveGame = dataclasses.field(default=enums.SaveGame.Unknown1)
    texture_asset: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

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

        data.write(b'w\xed\xd0\xf1')  # 0x77edd0f1
        data.write(b'\x00\x04')  # size
        self.save_game.to_stream(data)

        data.write(b'/\x11\xc1O')  # 0x2f11c14f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.texture_asset))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            save_game=enums.SaveGame.from_json(data['save_game']),
            texture_asset=data['texture_asset'],
        )

    def to_json(self) -> dict:
        return {
            'save_game': self.save_game.to_json(),
            'texture_asset': self.texture_asset,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x77edd0f1, 0x2f11c14f)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ShipDecalControllerStruct]:
    if property_count != 2:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(24))
    if (dec[0], dec[3]) != _FAST_IDS:
        data.seek(before)
        return None

    return ShipDecalControllerStruct(
        enums.SaveGame(dec[2]),
        dec[5],
    )


def _decode_save_game(data: typing.BinaryIO, property_size: int):
    return enums.SaveGame.from_stream(data)


def _decode_texture_asset(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x77edd0f1: ('save_game', _decode_save_game),
    0x2f11c14f: ('texture_asset', _decode_texture_asset),
}
