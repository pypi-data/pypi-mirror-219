# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.GenericCreatureStructD import GenericCreatureStructD


@dataclasses.dataclass()
class Groups(BaseProperty):
    number_of_groups: int = dataclasses.field(default=0)
    group01: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD)
    group02: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD)
    group03: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD)
    group04: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD)
    group05: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD)
    group06: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD)
    group07: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD)
    group08: GenericCreatureStructD = dataclasses.field(default_factory=GenericCreatureStructD)

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

        data.write(b'\x07\xf5\xda?')  # 0x7f5da3f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_groups))

        data.write(b'iT\xc4\xa6')  # 0x6954c4a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group01.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\x03)^')  # 0x9b03295e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\x1e\x8f\xc9')  # 0x7c1e8fc9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group03.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xdd\xf4\xef')  # 0xa4ddf4ef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group04.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\xc0Rx')  # 0x43c05278
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group05.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb1\x97\xbf\x80')  # 0xb197bf80
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group06.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\x8a\x19\x17')  # 0x568a1917
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group07.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdb`O\x8d')  # 0xdb604f8d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.group08.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            number_of_groups=data['number_of_groups'],
            group01=GenericCreatureStructD.from_json(data['group01']),
            group02=GenericCreatureStructD.from_json(data['group02']),
            group03=GenericCreatureStructD.from_json(data['group03']),
            group04=GenericCreatureStructD.from_json(data['group04']),
            group05=GenericCreatureStructD.from_json(data['group05']),
            group06=GenericCreatureStructD.from_json(data['group06']),
            group07=GenericCreatureStructD.from_json(data['group07']),
            group08=GenericCreatureStructD.from_json(data['group08']),
        )

    def to_json(self) -> dict:
        return {
            'number_of_groups': self.number_of_groups,
            'group01': self.group01.to_json(),
            'group02': self.group02.to_json(),
            'group03': self.group03.to_json(),
            'group04': self.group04.to_json(),
            'group05': self.group05.to_json(),
            'group06': self.group06.to_json(),
            'group07': self.group07.to_json(),
            'group08': self.group08.to_json(),
        }


def _decode_number_of_groups(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_group01(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructD.from_stream(data, property_size)


def _decode_group02(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructD.from_stream(data, property_size)


def _decode_group03(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructD.from_stream(data, property_size)


def _decode_group04(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructD.from_stream(data, property_size)


def _decode_group05(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructD.from_stream(data, property_size)


def _decode_group06(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructD.from_stream(data, property_size)


def _decode_group07(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructD.from_stream(data, property_size)


def _decode_group08(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructD.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7f5da3f: ('number_of_groups', _decode_number_of_groups),
    0x6954c4a6: ('group01', _decode_group01),
    0x9b03295e: ('group02', _decode_group02),
    0x7c1e8fc9: ('group03', _decode_group03),
    0xa4ddf4ef: ('group04', _decode_group04),
    0x43c05278: ('group05', _decode_group05),
    0xb197bf80: ('group06', _decode_group06),
    0x568a1917: ('group07', _decode_group07),
    0xdb604f8d: ('group08', _decode_group08),
}
