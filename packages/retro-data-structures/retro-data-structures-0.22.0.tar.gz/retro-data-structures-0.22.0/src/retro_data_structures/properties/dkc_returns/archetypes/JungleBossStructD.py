# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.VolcanoBossBodyPartStructA import VolcanoBossBodyPartStructA


@dataclasses.dataclass()
class JungleBossStructD(BaseProperty):
    volcano_boss_body_part_struct_a_0x12d98dc2: VolcanoBossBodyPartStructA = dataclasses.field(default_factory=VolcanoBossBodyPartStructA)
    volcano_boss_body_part_struct_a_0xc0f12817: VolcanoBossBodyPartStructA = dataclasses.field(default_factory=VolcanoBossBodyPartStructA)
    volcano_boss_body_part_struct_a_0xf8019f49: VolcanoBossBodyPartStructA = dataclasses.field(default_factory=VolcanoBossBodyPartStructA)
    unknown: float = dataclasses.field(default=50.0)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\x12\xd9\x8d\xc2')  # 0x12d98dc2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_a_0x12d98dc2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0\xf1(\x17')  # 0xc0f12817
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_a_0xc0f12817.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\x01\x9fI')  # 0xf8019f49
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_a_0xf8019f49.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J\xf1\xe5z')  # 0x4af1e57a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            volcano_boss_body_part_struct_a_0x12d98dc2=VolcanoBossBodyPartStructA.from_json(data['volcano_boss_body_part_struct_a_0x12d98dc2']),
            volcano_boss_body_part_struct_a_0xc0f12817=VolcanoBossBodyPartStructA.from_json(data['volcano_boss_body_part_struct_a_0xc0f12817']),
            volcano_boss_body_part_struct_a_0xf8019f49=VolcanoBossBodyPartStructA.from_json(data['volcano_boss_body_part_struct_a_0xf8019f49']),
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'volcano_boss_body_part_struct_a_0x12d98dc2': self.volcano_boss_body_part_struct_a_0x12d98dc2.to_json(),
            'volcano_boss_body_part_struct_a_0xc0f12817': self.volcano_boss_body_part_struct_a_0xc0f12817.to_json(),
            'volcano_boss_body_part_struct_a_0xf8019f49': self.volcano_boss_body_part_struct_a_0xf8019f49.to_json(),
            'unknown': self.unknown,
        }


def _decode_volcano_boss_body_part_struct_a_0x12d98dc2(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructA.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_a_0xc0f12817(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructA.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_a_0xf8019f49(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructA.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x12d98dc2: ('volcano_boss_body_part_struct_a_0x12d98dc2', _decode_volcano_boss_body_part_struct_a_0x12d98dc2),
    0xc0f12817: ('volcano_boss_body_part_struct_a_0xc0f12817', _decode_volcano_boss_body_part_struct_a_0xc0f12817),
    0xf8019f49: ('volcano_boss_body_part_struct_a_0xf8019f49', _decode_volcano_boss_body_part_struct_a_0xf8019f49),
    0x4af1e57a: ('unknown', _decode_unknown),
}
