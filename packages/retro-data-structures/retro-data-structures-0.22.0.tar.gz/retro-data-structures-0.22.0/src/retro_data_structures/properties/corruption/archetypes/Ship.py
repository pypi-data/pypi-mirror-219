# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.PlayerInventoryItem import PlayerInventoryItem


@dataclasses.dataclass()
class Ship(BaseProperty):
    ship_missile: PlayerInventoryItem = dataclasses.field(default_factory=PlayerInventoryItem)
    ship_grapple: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'9\x8a6\x08')  # 0x398a3608
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ship_missile.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xae\xe1\t')  # 0xf9aee109
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ship_grapple))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ship_missile=PlayerInventoryItem.from_json(data['ship_missile']),
            ship_grapple=data['ship_grapple'],
        )

    def to_json(self) -> dict:
        return {
            'ship_missile': self.ship_missile.to_json(),
            'ship_grapple': self.ship_grapple,
        }


def _decode_ship_missile(data: typing.BinaryIO, property_size: int):
    return PlayerInventoryItem.from_stream(data, property_size)


def _decode_ship_grapple(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x398a3608: ('ship_missile', _decode_ship_missile),
    0xf9aee109: ('ship_grapple', _decode_ship_grapple),
}
