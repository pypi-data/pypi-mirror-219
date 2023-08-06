# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.GhorStructA import GhorStructA


@dataclasses.dataclass()
class CircleLineMode(BaseProperty):
    ghor_struct_a_0x17386c2c: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    ghor_struct_a_0xd171838c: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    ghor_struct_a_0x017549cb: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    ghor_struct_a_0x08f6bdc5: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    ghor_struct_a_0x7b589dd6: GhorStructA = dataclasses.field(default_factory=GhorStructA)
    collision_set: str = dataclasses.field(default='')
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x178l,')  # 0x17386c2c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0x17386c2c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1q\x83\x8c')  # 0xd171838c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0xd171838c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01uI\xcb')  # 0x17549cb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0x017549cb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x08\xf6\xbd\xc5')  # 0x8f6bdc5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0x08f6bdc5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{X\x9d\xd6')  # 0x7b589dd6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghor_struct_a_0x7b589dd6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9c\xe3\x1f\xfa')  # 0x9ce31ffa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.collision_set.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            ghor_struct_a_0x17386c2c=GhorStructA.from_json(data['ghor_struct_a_0x17386c2c']),
            ghor_struct_a_0xd171838c=GhorStructA.from_json(data['ghor_struct_a_0xd171838c']),
            ghor_struct_a_0x017549cb=GhorStructA.from_json(data['ghor_struct_a_0x017549cb']),
            ghor_struct_a_0x08f6bdc5=GhorStructA.from_json(data['ghor_struct_a_0x08f6bdc5']),
            ghor_struct_a_0x7b589dd6=GhorStructA.from_json(data['ghor_struct_a_0x7b589dd6']),
            collision_set=data['collision_set'],
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'ghor_struct_a_0x17386c2c': self.ghor_struct_a_0x17386c2c.to_json(),
            'ghor_struct_a_0xd171838c': self.ghor_struct_a_0xd171838c.to_json(),
            'ghor_struct_a_0x017549cb': self.ghor_struct_a_0x017549cb.to_json(),
            'ghor_struct_a_0x08f6bdc5': self.ghor_struct_a_0x08f6bdc5.to_json(),
            'ghor_struct_a_0x7b589dd6': self.ghor_struct_a_0x7b589dd6.to_json(),
            'collision_set': self.collision_set,
            'vulnerability': self.vulnerability.to_json(),
        }


def _decode_ghor_struct_a_0x17386c2c(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_ghor_struct_a_0xd171838c(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_ghor_struct_a_0x017549cb(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_ghor_struct_a_0x08f6bdc5(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_ghor_struct_a_0x7b589dd6(data: typing.BinaryIO, property_size: int):
    return GhorStructA.from_stream(data, property_size)


def _decode_collision_set(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x17386c2c: ('ghor_struct_a_0x17386c2c', _decode_ghor_struct_a_0x17386c2c),
    0xd171838c: ('ghor_struct_a_0xd171838c', _decode_ghor_struct_a_0xd171838c),
    0x17549cb: ('ghor_struct_a_0x017549cb', _decode_ghor_struct_a_0x017549cb),
    0x8f6bdc5: ('ghor_struct_a_0x08f6bdc5', _decode_ghor_struct_a_0x08f6bdc5),
    0x7b589dd6: ('ghor_struct_a_0x7b589dd6', _decode_ghor_struct_a_0x7b589dd6),
    0x9ce31ffa: ('collision_set', _decode_collision_set),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
}
