# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.GhorStructC import GhorStructC


@dataclasses.dataclass()
class UnknownStruct38(BaseProperty):
    force_disable: bool = dataclasses.field(default=False)
    ghor_struct_c: GhorStructC = dataclasses.field(default_factory=GhorStructC)
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xa8\xd0\xee\x16')  # 0xa8d0ee16
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_disable))

        data.write(b'\xa8+]\xaa')  # 0xa82b5daa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9p\x13\xd0')  # 0xc97013d0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            force_disable=data['force_disable'],
            ghor_struct_c=GhorStructC.from_json(data['ghor_struct_c']),
            damage_info=DamageInfo.from_json(data['damage_info']),
        )

    def to_json(self) -> dict:
        return {
            'force_disable': self.force_disable,
            'ghor_struct_c': self.ghor_struct_c.to_json(),
            'damage_info': self.damage_info.to_json(),
        }


def _decode_force_disable(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ghor_struct_c(data: typing.BinaryIO, property_size: int):
    return GhorStructC.from_stream(data, property_size)


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa8d0ee16: ('force_disable', _decode_force_disable),
    0xa82b5daa: ('ghor_struct_c', _decode_ghor_struct_c),
    0xc97013d0: ('damage_info', _decode_damage_info),
}
