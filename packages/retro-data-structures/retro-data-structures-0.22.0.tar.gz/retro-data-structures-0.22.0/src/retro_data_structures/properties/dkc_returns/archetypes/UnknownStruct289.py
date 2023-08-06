# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.VolcanoBossBodyPartStructA import VolcanoBossBodyPartStructA


@dataclasses.dataclass()
class UnknownStruct289(BaseProperty):
    volcano_boss_body_part_struct_a: VolcanoBossBodyPartStructA = dataclasses.field(default_factory=VolcanoBossBodyPartStructA)
    selection_chance: float = dataclasses.field(default=50.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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

        data.write(b'(\xf4\x9aS')  # 0x28f49a53
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b\x03\x04f')  # 0x1b030466
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.selection_chance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            volcano_boss_body_part_struct_a=VolcanoBossBodyPartStructA.from_json(data['volcano_boss_body_part_struct_a']),
            selection_chance=data['selection_chance'],
        )

    def to_json(self) -> dict:
        return {
            'volcano_boss_body_part_struct_a': self.volcano_boss_body_part_struct_a.to_json(),
            'selection_chance': self.selection_chance,
        }


def _decode_volcano_boss_body_part_struct_a(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructA.from_stream(data, property_size)


def _decode_selection_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x28f49a53: ('volcano_boss_body_part_struct_a', _decode_volcano_boss_body_part_struct_a),
    0x1b030466: ('selection_chance', _decode_selection_chance),
}
