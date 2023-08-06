# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.Inventory import Inventory


@dataclasses.dataclass()
class SpawnPoint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    first_spawn: bool = dataclasses.field(default=True)
    morphed: bool = dataclasses.field(default=False)
    unknown_0xa7a88fef: bool = dataclasses.field(default=False)
    death_fall: bool = dataclasses.field(default=False)
    unknown_0xab0b9ac4: bool = dataclasses.field(default=False)
    unknown_0x4ad656da: bool = dataclasses.field(default=False)
    inventory_player: Inventory = dataclasses.field(default_factory=Inventory)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SPWN'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0\xe4R\x1b')  # 0xc0e4521b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.first_spawn))

        data.write(b'\xb9\xc4\x0f\x92')  # 0xb9c40f92
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.morphed))

        data.write(b'\xa7\xa8\x8f\xef')  # 0xa7a88fef
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa7a88fef))

        data.write(b'!\x0f&&')  # 0x210f2626
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.death_fall))

        data.write(b'\xab\x0b\x9a\xc4')  # 0xab0b9ac4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xab0b9ac4))

        data.write(b'J\xd6V\xda')  # 0x4ad656da
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x4ad656da))

        data.write(b'\xf4\xed\x95G')  # 0xf4ed9547
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.inventory_player.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            first_spawn=data['first_spawn'],
            morphed=data['morphed'],
            unknown_0xa7a88fef=data['unknown_0xa7a88fef'],
            death_fall=data['death_fall'],
            unknown_0xab0b9ac4=data['unknown_0xab0b9ac4'],
            unknown_0x4ad656da=data['unknown_0x4ad656da'],
            inventory_player=Inventory.from_json(data['inventory_player']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'first_spawn': self.first_spawn,
            'morphed': self.morphed,
            'unknown_0xa7a88fef': self.unknown_0xa7a88fef,
            'death_fall': self.death_fall,
            'unknown_0xab0b9ac4': self.unknown_0xab0b9ac4,
            'unknown_0x4ad656da': self.unknown_0x4ad656da,
            'inventory_player': self.inventory_player.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_first_spawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_morphed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa7a88fef(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_death_fall(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xab0b9ac4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4ad656da(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_inventory_player(data: typing.BinaryIO, property_size: int):
    return Inventory.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc0e4521b: ('first_spawn', _decode_first_spawn),
    0xb9c40f92: ('morphed', _decode_morphed),
    0xa7a88fef: ('unknown_0xa7a88fef', _decode_unknown_0xa7a88fef),
    0x210f2626: ('death_fall', _decode_death_fall),
    0xab0b9ac4: ('unknown_0xab0b9ac4', _decode_unknown_0xab0b9ac4),
    0x4ad656da: ('unknown_0x4ad656da', _decode_unknown_0x4ad656da),
    0xf4ed9547: ('inventory_player', _decode_inventory_player),
}
