# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.JungleBossStructB import JungleBossStructB


@dataclasses.dataclass()
class UnknownStruct202(BaseProperty):
    unknown_0x28ca1360: bool = dataclasses.field(default=False)
    unknown_0x775a0160: str = dataclasses.field(default='')
    unknown_0x06efdab2: int = dataclasses.field(default=0)
    jungle_boss_struct_b_0xd4292680: JungleBossStructB = dataclasses.field(default_factory=JungleBossStructB)
    jungle_boss_struct_b_0x90880398: JungleBossStructB = dataclasses.field(default_factory=JungleBossStructB)
    jungle_boss_struct_b_0xace8e090: JungleBossStructB = dataclasses.field(default_factory=JungleBossStructB)
    jungle_boss_struct_b_0x19ca49a8: JungleBossStructB = dataclasses.field(default_factory=JungleBossStructB)
    jungle_boss_struct_b_0x25aaaaa0: JungleBossStructB = dataclasses.field(default_factory=JungleBossStructB)
    jungle_boss_struct_b_0x610b8fb8: JungleBossStructB = dataclasses.field(default_factory=JungleBossStructB)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'(\xca\x13`')  # 0x28ca1360
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x28ca1360))

        data.write(b'wZ\x01`')  # 0x775a0160
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown_0x775a0160.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x06\xef\xda\xb2')  # 0x6efdab2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x06efdab2))

        data.write(b'\xd4)&\x80')  # 0xd4292680
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_b_0xd4292680.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x90\x88\x03\x98')  # 0x90880398
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_b_0x90880398.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xac\xe8\xe0\x90')  # 0xace8e090
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_b_0xace8e090.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\xcaI\xa8')  # 0x19ca49a8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_b_0x19ca49a8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'%\xaa\xaa\xa0')  # 0x25aaaaa0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_b_0x25aaaaa0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'a\x0b\x8f\xb8')  # 0x610b8fb8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jungle_boss_struct_b_0x610b8fb8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x28ca1360=data['unknown_0x28ca1360'],
            unknown_0x775a0160=data['unknown_0x775a0160'],
            unknown_0x06efdab2=data['unknown_0x06efdab2'],
            jungle_boss_struct_b_0xd4292680=JungleBossStructB.from_json(data['jungle_boss_struct_b_0xd4292680']),
            jungle_boss_struct_b_0x90880398=JungleBossStructB.from_json(data['jungle_boss_struct_b_0x90880398']),
            jungle_boss_struct_b_0xace8e090=JungleBossStructB.from_json(data['jungle_boss_struct_b_0xace8e090']),
            jungle_boss_struct_b_0x19ca49a8=JungleBossStructB.from_json(data['jungle_boss_struct_b_0x19ca49a8']),
            jungle_boss_struct_b_0x25aaaaa0=JungleBossStructB.from_json(data['jungle_boss_struct_b_0x25aaaaa0']),
            jungle_boss_struct_b_0x610b8fb8=JungleBossStructB.from_json(data['jungle_boss_struct_b_0x610b8fb8']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x28ca1360': self.unknown_0x28ca1360,
            'unknown_0x775a0160': self.unknown_0x775a0160,
            'unknown_0x06efdab2': self.unknown_0x06efdab2,
            'jungle_boss_struct_b_0xd4292680': self.jungle_boss_struct_b_0xd4292680.to_json(),
            'jungle_boss_struct_b_0x90880398': self.jungle_boss_struct_b_0x90880398.to_json(),
            'jungle_boss_struct_b_0xace8e090': self.jungle_boss_struct_b_0xace8e090.to_json(),
            'jungle_boss_struct_b_0x19ca49a8': self.jungle_boss_struct_b_0x19ca49a8.to_json(),
            'jungle_boss_struct_b_0x25aaaaa0': self.jungle_boss_struct_b_0x25aaaaa0.to_json(),
            'jungle_boss_struct_b_0x610b8fb8': self.jungle_boss_struct_b_0x610b8fb8.to_json(),
        }


def _decode_unknown_0x28ca1360(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x775a0160(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x06efdab2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_jungle_boss_struct_b_0xd4292680(data: typing.BinaryIO, property_size: int):
    return JungleBossStructB.from_stream(data, property_size)


def _decode_jungle_boss_struct_b_0x90880398(data: typing.BinaryIO, property_size: int):
    return JungleBossStructB.from_stream(data, property_size)


def _decode_jungle_boss_struct_b_0xace8e090(data: typing.BinaryIO, property_size: int):
    return JungleBossStructB.from_stream(data, property_size)


def _decode_jungle_boss_struct_b_0x19ca49a8(data: typing.BinaryIO, property_size: int):
    return JungleBossStructB.from_stream(data, property_size)


def _decode_jungle_boss_struct_b_0x25aaaaa0(data: typing.BinaryIO, property_size: int):
    return JungleBossStructB.from_stream(data, property_size)


def _decode_jungle_boss_struct_b_0x610b8fb8(data: typing.BinaryIO, property_size: int):
    return JungleBossStructB.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x28ca1360: ('unknown_0x28ca1360', _decode_unknown_0x28ca1360),
    0x775a0160: ('unknown_0x775a0160', _decode_unknown_0x775a0160),
    0x6efdab2: ('unknown_0x06efdab2', _decode_unknown_0x06efdab2),
    0xd4292680: ('jungle_boss_struct_b_0xd4292680', _decode_jungle_boss_struct_b_0xd4292680),
    0x90880398: ('jungle_boss_struct_b_0x90880398', _decode_jungle_boss_struct_b_0x90880398),
    0xace8e090: ('jungle_boss_struct_b_0xace8e090', _decode_jungle_boss_struct_b_0xace8e090),
    0x19ca49a8: ('jungle_boss_struct_b_0x19ca49a8', _decode_jungle_boss_struct_b_0x19ca49a8),
    0x25aaaaa0: ('jungle_boss_struct_b_0x25aaaaa0', _decode_jungle_boss_struct_b_0x25aaaaa0),
    0x610b8fb8: ('jungle_boss_struct_b_0x610b8fb8', _decode_jungle_boss_struct_b_0x610b8fb8),
}
