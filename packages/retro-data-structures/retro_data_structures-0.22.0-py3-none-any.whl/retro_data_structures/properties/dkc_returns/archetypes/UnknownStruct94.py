# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.ForestBossStructC import ForestBossStructC


@dataclasses.dataclass()
class UnknownStruct94(BaseProperty):
    forest_boss_struct_c_0x63f77b98: ForestBossStructC = dataclasses.field(default_factory=ForestBossStructC)
    forest_boss_struct_c_0x8561e02d: ForestBossStructC = dataclasses.field(default_factory=ForestBossStructC)

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

        data.write(b'c\xf7{\x98')  # 0x63f77b98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_c_0x63f77b98.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85a\xe0-')  # 0x8561e02d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.forest_boss_struct_c_0x8561e02d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            forest_boss_struct_c_0x63f77b98=ForestBossStructC.from_json(data['forest_boss_struct_c_0x63f77b98']),
            forest_boss_struct_c_0x8561e02d=ForestBossStructC.from_json(data['forest_boss_struct_c_0x8561e02d']),
        )

    def to_json(self) -> dict:
        return {
            'forest_boss_struct_c_0x63f77b98': self.forest_boss_struct_c_0x63f77b98.to_json(),
            'forest_boss_struct_c_0x8561e02d': self.forest_boss_struct_c_0x8561e02d.to_json(),
        }


def _decode_forest_boss_struct_c_0x63f77b98(data: typing.BinaryIO, property_size: int):
    return ForestBossStructC.from_stream(data, property_size)


def _decode_forest_boss_struct_c_0x8561e02d(data: typing.BinaryIO, property_size: int):
    return ForestBossStructC.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x63f77b98: ('forest_boss_struct_c_0x63f77b98', _decode_forest_boss_struct_c_0x63f77b98),
    0x8561e02d: ('forest_boss_struct_c_0x8561e02d', _decode_forest_boss_struct_c_0x8561e02d),
}
