# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.InventoryControls import InventoryControls
from retro_data_structures.properties.corruption.archetypes.MapControls import MapControls
from retro_data_structures.properties.corruption.archetypes.MiscControls.UnknownStruct1 import UnknownStruct1
from retro_data_structures.properties.corruption.archetypes.MiscControls.UnknownStruct2 import UnknownStruct2
from retro_data_structures.properties.corruption.archetypes.RevolutionControl import RevolutionControl


@dataclasses.dataclass()
class MiscControls(BaseProperty):
    map: MapControls = dataclasses.field(default_factory=MapControls)
    inventory: InventoryControls = dataclasses.field(default_factory=InventoryControls)
    options_screen: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)
    unknown_0xc6232204: UnknownStruct1 = dataclasses.field(default_factory=UnknownStruct1)
    unknown_0x5126ffe7: UnknownStruct2 = dataclasses.field(default_factory=UnknownStruct2)
    unknown_0x439f3678: RevolutionControl = dataclasses.field(default_factory=RevolutionControl)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\x9a\xcbJ\xce')  # 0x9acb4ace
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.map.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed4\x82\xb7')  # 0xed3482b7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.inventory.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xe5/\x14')  # 0x36e52f14
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.options_screen.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6#"\x04')  # 0xc6232204
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xc6232204.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q&\xff\xe7')  # 0x5126ffe7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x5126ffe7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\x9f6x')  # 0x439f3678
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x439f3678.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            map=MapControls.from_json(data['map']),
            inventory=InventoryControls.from_json(data['inventory']),
            options_screen=RevolutionControl.from_json(data['options_screen']),
            unknown_0xc6232204=UnknownStruct1.from_json(data['unknown_0xc6232204']),
            unknown_0x5126ffe7=UnknownStruct2.from_json(data['unknown_0x5126ffe7']),
            unknown_0x439f3678=RevolutionControl.from_json(data['unknown_0x439f3678']),
        )

    def to_json(self) -> dict:
        return {
            'map': self.map.to_json(),
            'inventory': self.inventory.to_json(),
            'options_screen': self.options_screen.to_json(),
            'unknown_0xc6232204': self.unknown_0xc6232204.to_json(),
            'unknown_0x5126ffe7': self.unknown_0x5126ffe7.to_json(),
            'unknown_0x439f3678': self.unknown_0x439f3678.to_json(),
        }


def _decode_map(data: typing.BinaryIO, property_size: int):
    return MapControls.from_stream(data, property_size)


def _decode_inventory(data: typing.BinaryIO, property_size: int):
    return InventoryControls.from_stream(data, property_size)


def _decode_options_screen(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


def _decode_unknown_0xc6232204(data: typing.BinaryIO, property_size: int):
    return UnknownStruct1.from_stream(data, property_size)


def _decode_unknown_0x5126ffe7(data: typing.BinaryIO, property_size: int):
    return UnknownStruct2.from_stream(data, property_size)


def _decode_unknown_0x439f3678(data: typing.BinaryIO, property_size: int):
    return RevolutionControl.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9acb4ace: ('map', _decode_map),
    0xed3482b7: ('inventory', _decode_inventory),
    0x36e52f14: ('options_screen', _decode_options_screen),
    0xc6232204: ('unknown_0xc6232204', _decode_unknown_0xc6232204),
    0x5126ffe7: ('unknown_0x5126ffe7', _decode_unknown_0x5126ffe7),
    0x439f3678: ('unknown_0x439f3678', _decode_unknown_0x439f3678),
}
