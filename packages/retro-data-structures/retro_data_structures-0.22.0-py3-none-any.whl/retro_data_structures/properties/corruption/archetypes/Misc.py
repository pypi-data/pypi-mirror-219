# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.PlayerInventoryItem import PlayerInventoryItem


@dataclasses.dataclass()
class Misc(BaseProperty):
    energy: PlayerInventoryItem = dataclasses.field(default_factory=PlayerInventoryItem)
    energy_tank: PlayerInventoryItem = dataclasses.field(default_factory=PlayerInventoryItem)
    fuses: PlayerInventoryItem = dataclasses.field(default_factory=PlayerInventoryItem)
    player_inventory_item: PlayerInventoryItem = dataclasses.field(default_factory=PlayerInventoryItem)

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

        data.write(b'3k\xd4q')  # 0x336bd471
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energy.to_stream(data, default_override={'amount': 1, 'capacity': 1})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd3\x1b"\t')  # 0xd31b2209
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energy_tank.to_stream(data, default_override={'amount': 1, 'capacity': 1})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15.\xd0\xd9')  # 0x152ed0d9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fuses.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\n\x91\xae')  # 0x950a91ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.player_inventory_item.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            energy=PlayerInventoryItem.from_json(data['energy']),
            energy_tank=PlayerInventoryItem.from_json(data['energy_tank']),
            fuses=PlayerInventoryItem.from_json(data['fuses']),
            player_inventory_item=PlayerInventoryItem.from_json(data['player_inventory_item']),
        )

    def to_json(self) -> dict:
        return {
            'energy': self.energy.to_json(),
            'energy_tank': self.energy_tank.to_json(),
            'fuses': self.fuses.to_json(),
            'player_inventory_item': self.player_inventory_item.to_json(),
        }


def _decode_energy(data: typing.BinaryIO, property_size: int):
    return PlayerInventoryItem.from_stream(data, property_size, default_override={'amount': 1, 'capacity': 1})


def _decode_energy_tank(data: typing.BinaryIO, property_size: int):
    return PlayerInventoryItem.from_stream(data, property_size, default_override={'amount': 1, 'capacity': 1})


def _decode_fuses(data: typing.BinaryIO, property_size: int):
    return PlayerInventoryItem.from_stream(data, property_size)


def _decode_player_inventory_item(data: typing.BinaryIO, property_size: int):
    return PlayerInventoryItem.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x336bd471: ('energy', _decode_energy),
    0xd31b2209: ('energy_tank', _decode_energy_tank),
    0x152ed0d9: ('fuses', _decode_fuses),
    0x950a91ae: ('player_inventory_item', _decode_player_inventory_item),
}
