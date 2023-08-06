# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct55 import UnknownStruct55


@dataclasses.dataclass()
class UnknownStruct192(BaseProperty):
    unknown: bool = dataclasses.field(default=False)
    unknown_struct55_0x6ed124ef: UnknownStruct55 = dataclasses.field(default_factory=UnknownStruct55)
    unknown_struct55_0x5b3c92bc: UnknownStruct55 = dataclasses.field(default_factory=UnknownStruct55)
    unknown_struct55_0xfeb702b2: UnknownStruct55 = dataclasses.field(default_factory=UnknownStruct55)
    unknown_struct55_0x30e7fe1a: UnknownStruct55 = dataclasses.field(default_factory=UnknownStruct55)
    unknown_struct55_0x956c6e14: UnknownStruct55 = dataclasses.field(default_factory=UnknownStruct55)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xa6\xde\xd8t')  # 0xa6ded874
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'n\xd1$\xef')  # 0x6ed124ef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct55_0x6ed124ef.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'[<\x92\xbc')  # 0x5b3c92bc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct55_0x5b3c92bc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfe\xb7\x02\xb2')  # 0xfeb702b2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct55_0xfeb702b2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\xe7\xfe\x1a')  # 0x30e7fe1a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct55_0x30e7fe1a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95ln\x14')  # 0x956c6e14
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct55_0x956c6e14.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown=data['unknown'],
            unknown_struct55_0x6ed124ef=UnknownStruct55.from_json(data['unknown_struct55_0x6ed124ef']),
            unknown_struct55_0x5b3c92bc=UnknownStruct55.from_json(data['unknown_struct55_0x5b3c92bc']),
            unknown_struct55_0xfeb702b2=UnknownStruct55.from_json(data['unknown_struct55_0xfeb702b2']),
            unknown_struct55_0x30e7fe1a=UnknownStruct55.from_json(data['unknown_struct55_0x30e7fe1a']),
            unknown_struct55_0x956c6e14=UnknownStruct55.from_json(data['unknown_struct55_0x956c6e14']),
        )

    def to_json(self) -> dict:
        return {
            'unknown': self.unknown,
            'unknown_struct55_0x6ed124ef': self.unknown_struct55_0x6ed124ef.to_json(),
            'unknown_struct55_0x5b3c92bc': self.unknown_struct55_0x5b3c92bc.to_json(),
            'unknown_struct55_0xfeb702b2': self.unknown_struct55_0xfeb702b2.to_json(),
            'unknown_struct55_0x30e7fe1a': self.unknown_struct55_0x30e7fe1a.to_json(),
            'unknown_struct55_0x956c6e14': self.unknown_struct55_0x956c6e14.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct55_0x6ed124ef(data: typing.BinaryIO, property_size: int):
    return UnknownStruct55.from_stream(data, property_size)


def _decode_unknown_struct55_0x5b3c92bc(data: typing.BinaryIO, property_size: int):
    return UnknownStruct55.from_stream(data, property_size)


def _decode_unknown_struct55_0xfeb702b2(data: typing.BinaryIO, property_size: int):
    return UnknownStruct55.from_stream(data, property_size)


def _decode_unknown_struct55_0x30e7fe1a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct55.from_stream(data, property_size)


def _decode_unknown_struct55_0x956c6e14(data: typing.BinaryIO, property_size: int):
    return UnknownStruct55.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa6ded874: ('unknown', _decode_unknown),
    0x6ed124ef: ('unknown_struct55_0x6ed124ef', _decode_unknown_struct55_0x6ed124ef),
    0x5b3c92bc: ('unknown_struct55_0x5b3c92bc', _decode_unknown_struct55_0x5b3c92bc),
    0xfeb702b2: ('unknown_struct55_0xfeb702b2', _decode_unknown_struct55_0xfeb702b2),
    0x30e7fe1a: ('unknown_struct55_0x30e7fe1a', _decode_unknown_struct55_0x30e7fe1a),
    0x956c6e14: ('unknown_struct55_0x956c6e14', _decode_unknown_struct55_0x956c6e14),
}
