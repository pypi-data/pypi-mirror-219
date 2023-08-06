# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.VolcanoBossBodyPartStructD import VolcanoBossBodyPartStructD


@dataclasses.dataclass()
class UnknownStruct293(BaseProperty):
    unknown: int = dataclasses.field(default=0)
    volcano_boss_body_part_struct_d_0x4266606e: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD)
    volcano_boss_body_part_struct_d_0x06c74576: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD)
    volcano_boss_body_part_struct_d_0x3aa7a67e: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD)
    volcano_boss_body_part_struct_d_0x8f850f46: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD)
    volcano_boss_body_part_struct_d_0xb3e5ec4e: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD)
    volcano_boss_body_part_struct_d_0xf744c956: VolcanoBossBodyPartStructD = dataclasses.field(default_factory=VolcanoBossBodyPartStructD)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x06\xef\xda\xb2')  # 0x6efdab2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'Bf`n')  # 0x4266606e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0x4266606e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x06\xc7Ev')  # 0x6c74576
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0x06c74576.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':\xa7\xa6~')  # 0x3aa7a67e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0x3aa7a67e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8f\x85\x0fF')  # 0x8f850f46
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0x8f850f46.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3\xe5\xecN')  # 0xb3e5ec4e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0xb3e5ec4e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7D\xc9V')  # 0xf744c956
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.volcano_boss_body_part_struct_d_0xf744c956.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            volcano_boss_body_part_struct_d_0x4266606e=VolcanoBossBodyPartStructD.from_json(data['volcano_boss_body_part_struct_d_0x4266606e']),
            volcano_boss_body_part_struct_d_0x06c74576=VolcanoBossBodyPartStructD.from_json(data['volcano_boss_body_part_struct_d_0x06c74576']),
            volcano_boss_body_part_struct_d_0x3aa7a67e=VolcanoBossBodyPartStructD.from_json(data['volcano_boss_body_part_struct_d_0x3aa7a67e']),
            volcano_boss_body_part_struct_d_0x8f850f46=VolcanoBossBodyPartStructD.from_json(data['volcano_boss_body_part_struct_d_0x8f850f46']),
            volcano_boss_body_part_struct_d_0xb3e5ec4e=VolcanoBossBodyPartStructD.from_json(data['volcano_boss_body_part_struct_d_0xb3e5ec4e']),
            volcano_boss_body_part_struct_d_0xf744c956=VolcanoBossBodyPartStructD.from_json(data['volcano_boss_body_part_struct_d_0xf744c956']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'volcano_boss_body_part_struct_d_0x4266606e': self.volcano_boss_body_part_struct_d_0x4266606e.to_json(),
            'volcano_boss_body_part_struct_d_0x06c74576': self.volcano_boss_body_part_struct_d_0x06c74576.to_json(),
            'volcano_boss_body_part_struct_d_0x3aa7a67e': self.volcano_boss_body_part_struct_d_0x3aa7a67e.to_json(),
            'volcano_boss_body_part_struct_d_0x8f850f46': self.volcano_boss_body_part_struct_d_0x8f850f46.to_json(),
            'volcano_boss_body_part_struct_d_0xb3e5ec4e': self.volcano_boss_body_part_struct_d_0xb3e5ec4e.to_json(),
            'volcano_boss_body_part_struct_d_0xf744c956': self.volcano_boss_body_part_struct_d_0xf744c956.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_volcano_boss_body_part_struct_d_0x4266606e(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructD.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_d_0x06c74576(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructD.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_d_0x3aa7a67e(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructD.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_d_0x8f850f46(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructD.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_d_0xb3e5ec4e(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructD.from_stream(data, property_size)


def _decode_volcano_boss_body_part_struct_d_0xf744c956(data: typing.BinaryIO, property_size: int):
    return VolcanoBossBodyPartStructD.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6efdab2: ('unknown', _decode_unknown),
    0x4266606e: ('volcano_boss_body_part_struct_d_0x4266606e', _decode_volcano_boss_body_part_struct_d_0x4266606e),
    0x6c74576: ('volcano_boss_body_part_struct_d_0x06c74576', _decode_volcano_boss_body_part_struct_d_0x06c74576),
    0x3aa7a67e: ('volcano_boss_body_part_struct_d_0x3aa7a67e', _decode_volcano_boss_body_part_struct_d_0x3aa7a67e),
    0x8f850f46: ('volcano_boss_body_part_struct_d_0x8f850f46', _decode_volcano_boss_body_part_struct_d_0x8f850f46),
    0xb3e5ec4e: ('volcano_boss_body_part_struct_d_0xb3e5ec4e', _decode_volcano_boss_body_part_struct_d_0xb3e5ec4e),
    0xf744c956: ('volcano_boss_body_part_struct_d_0xf744c956', _decode_volcano_boss_body_part_struct_d_0xf744c956),
}
