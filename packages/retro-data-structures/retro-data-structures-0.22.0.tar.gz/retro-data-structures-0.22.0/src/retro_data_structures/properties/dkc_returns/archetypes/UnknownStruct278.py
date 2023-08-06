# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.JungleBossStructD import JungleBossStructD


@dataclasses.dataclass()
class UnknownStruct278(BaseProperty):
    sequence_size: int = dataclasses.field(default=0)
    jungle_boss_struct_d_0x41aca731: JungleBossStructD = dataclasses.field(default_factory=JungleBossStructD)
    jungle_boss_struct_d_0x74411162: JungleBossStructD = dataclasses.field(default_factory=JungleBossStructD)
    jungle_boss_struct_d_0xd1ca816c: JungleBossStructD = dataclasses.field(default_factory=JungleBossStructD)
    jungle_boss_struct_d_0x1f9a7dc4: JungleBossStructD = dataclasses.field(default_factory=JungleBossStructD)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\x1e9\x8c\xb1')  # 0x1e398cb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sequence_size))

        data.write(b'A\xac\xa71')  # 0x41aca731
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_d_0x41aca731.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'tA\x11b')  # 0x74411162
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_d_0x74411162.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1\xca\x81l')  # 0xd1ca816c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_d_0xd1ca816c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1f\x9a}\xc4')  # 0x1f9a7dc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_d_0x1f9a7dc4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            sequence_size=data['sequence_size'],
            jungle_boss_struct_d_0x41aca731=JungleBossStructD.from_json(data['jungle_boss_struct_d_0x41aca731']),
            jungle_boss_struct_d_0x74411162=JungleBossStructD.from_json(data['jungle_boss_struct_d_0x74411162']),
            jungle_boss_struct_d_0xd1ca816c=JungleBossStructD.from_json(data['jungle_boss_struct_d_0xd1ca816c']),
            jungle_boss_struct_d_0x1f9a7dc4=JungleBossStructD.from_json(data['jungle_boss_struct_d_0x1f9a7dc4']),
        )

    def to_json(self) -> dict:
        return {
            'sequence_size': self.sequence_size,
            'jungle_boss_struct_d_0x41aca731': self.jungle_boss_struct_d_0x41aca731.to_json(),
            'jungle_boss_struct_d_0x74411162': self.jungle_boss_struct_d_0x74411162.to_json(),
            'jungle_boss_struct_d_0xd1ca816c': self.jungle_boss_struct_d_0xd1ca816c.to_json(),
            'jungle_boss_struct_d_0x1f9a7dc4': self.jungle_boss_struct_d_0x1f9a7dc4.to_json(),
        }


def _decode_sequence_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_jungle_boss_struct_d_0x41aca731(data: typing.BinaryIO, property_size: int):
    return JungleBossStructD.from_stream(data, property_size)


def _decode_jungle_boss_struct_d_0x74411162(data: typing.BinaryIO, property_size: int):
    return JungleBossStructD.from_stream(data, property_size)


def _decode_jungle_boss_struct_d_0xd1ca816c(data: typing.BinaryIO, property_size: int):
    return JungleBossStructD.from_stream(data, property_size)


def _decode_jungle_boss_struct_d_0x1f9a7dc4(data: typing.BinaryIO, property_size: int):
    return JungleBossStructD.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1e398cb1: ('sequence_size', _decode_sequence_size),
    0x41aca731: ('jungle_boss_struct_d_0x41aca731', _decode_jungle_boss_struct_d_0x41aca731),
    0x74411162: ('jungle_boss_struct_d_0x74411162', _decode_jungle_boss_struct_d_0x74411162),
    0xd1ca816c: ('jungle_boss_struct_d_0xd1ca816c', _decode_jungle_boss_struct_d_0xd1ca816c),
    0x1f9a7dc4: ('jungle_boss_struct_d_0x1f9a7dc4', _decode_jungle_boss_struct_d_0x1f9a7dc4),
}
