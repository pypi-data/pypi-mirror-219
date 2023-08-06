# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class GhorStructA(BaseProperty):
    undamaged: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    damaged: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    locator: str = dataclasses.field(default='')
    damage_effect: str = dataclasses.field(default='')

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xf8\xbe\xdbc')  # 0xf8bedb63
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.undamaged))

        data.write(b'\x1d\\\xcc-')  # 0x1d5ccc2d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.damaged))

        data.write(b'\x8af\x0f\xe5')  # 0x8a660fe5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_\x13z\xc5')  # 0x5f137ac5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.damage_effect.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            undamaged=data['undamaged'],
            damaged=data['damaged'],
            locator=data['locator'],
            damage_effect=data['damage_effect'],
        )

    def to_json(self) -> dict:
        return {
            'undamaged': self.undamaged,
            'damaged': self.damaged,
            'locator': self.locator,
            'damage_effect': self.damage_effect,
        }


def _decode_undamaged(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damaged(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_locator(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_damage_effect(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf8bedb63: ('undamaged', _decode_undamaged),
    0x1d5ccc2d: ('damaged', _decode_damaged),
    0x8a660fe5: ('locator', _decode_locator),
    0x5f137ac5: ('damage_effect', _decode_damage_effect),
}
