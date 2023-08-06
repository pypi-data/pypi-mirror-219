# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence


@dataclasses.dataclass()
class UnknownStruct77(BaseProperty):
    convergence_0xaeb294fd: Convergence = dataclasses.field(default_factory=Convergence)
    convergence_0x4a4b9b59: Convergence = dataclasses.field(default_factory=Convergence)
    convergence_0xecdaca25: Convergence = dataclasses.field(default_factory=Convergence)
    unknown_0x7e69a860: bool = dataclasses.field(default=True)
    convergence_0x26bcff37: Convergence = dataclasses.field(default_factory=Convergence)
    unknown_0x6c1626b9: float = dataclasses.field(default=4.0)
    unknown_0x7a323dda: float = dataclasses.field(default=9.0)
    unknown_0x33e6589f: float = dataclasses.field(default=1.0)
    unknown_0x1a98a587: float = dataclasses.field(default=4.25)
    unknown_0x021f6d9b: float = dataclasses.field(default=12.0)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\xae\xb2\x94\xfd')  # 0xaeb294fd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence_0xaeb294fd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'JK\x9bY')  # 0x4a4b9b59
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence_0x4a4b9b59.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xec\xda\xca%')  # 0xecdaca25
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence_0xecdaca25.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~i\xa8`')  # 0x7e69a860
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7e69a860))

        data.write(b'&\xbc\xff7')  # 0x26bcff37
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence_0x26bcff37.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'l\x16&\xb9')  # 0x6c1626b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6c1626b9))

        data.write(b'z2=\xda')  # 0x7a323dda
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7a323dda))

        data.write(b'3\xe6X\x9f')  # 0x33e6589f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x33e6589f))

        data.write(b'\x1a\x98\xa5\x87')  # 0x1a98a587
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1a98a587))

        data.write(b'\x02\x1fm\x9b')  # 0x21f6d9b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x021f6d9b))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            convergence_0xaeb294fd=Convergence.from_json(data['convergence_0xaeb294fd']),
            convergence_0x4a4b9b59=Convergence.from_json(data['convergence_0x4a4b9b59']),
            convergence_0xecdaca25=Convergence.from_json(data['convergence_0xecdaca25']),
            unknown_0x7e69a860=data['unknown_0x7e69a860'],
            convergence_0x26bcff37=Convergence.from_json(data['convergence_0x26bcff37']),
            unknown_0x6c1626b9=data['unknown_0x6c1626b9'],
            unknown_0x7a323dda=data['unknown_0x7a323dda'],
            unknown_0x33e6589f=data['unknown_0x33e6589f'],
            unknown_0x1a98a587=data['unknown_0x1a98a587'],
            unknown_0x021f6d9b=data['unknown_0x021f6d9b'],
        )

    def to_json(self) -> dict:
        return {
            'convergence_0xaeb294fd': self.convergence_0xaeb294fd.to_json(),
            'convergence_0x4a4b9b59': self.convergence_0x4a4b9b59.to_json(),
            'convergence_0xecdaca25': self.convergence_0xecdaca25.to_json(),
            'unknown_0x7e69a860': self.unknown_0x7e69a860,
            'convergence_0x26bcff37': self.convergence_0x26bcff37.to_json(),
            'unknown_0x6c1626b9': self.unknown_0x6c1626b9,
            'unknown_0x7a323dda': self.unknown_0x7a323dda,
            'unknown_0x33e6589f': self.unknown_0x33e6589f,
            'unknown_0x1a98a587': self.unknown_0x1a98a587,
            'unknown_0x021f6d9b': self.unknown_0x021f6d9b,
        }


def _decode_convergence_0xaeb294fd(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_convergence_0x4a4b9b59(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_convergence_0xecdaca25(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_unknown_0x7e69a860(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_convergence_0x26bcff37(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_unknown_0x6c1626b9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7a323dda(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x33e6589f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1a98a587(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x021f6d9b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xaeb294fd: ('convergence_0xaeb294fd', _decode_convergence_0xaeb294fd),
    0x4a4b9b59: ('convergence_0x4a4b9b59', _decode_convergence_0x4a4b9b59),
    0xecdaca25: ('convergence_0xecdaca25', _decode_convergence_0xecdaca25),
    0x7e69a860: ('unknown_0x7e69a860', _decode_unknown_0x7e69a860),
    0x26bcff37: ('convergence_0x26bcff37', _decode_convergence_0x26bcff37),
    0x6c1626b9: ('unknown_0x6c1626b9', _decode_unknown_0x6c1626b9),
    0x7a323dda: ('unknown_0x7a323dda', _decode_unknown_0x7a323dda),
    0x33e6589f: ('unknown_0x33e6589f', _decode_unknown_0x33e6589f),
    0x1a98a587: ('unknown_0x1a98a587', _decode_unknown_0x1a98a587),
    0x21f6d9b: ('unknown_0x021f6d9b', _decode_unknown_0x021f6d9b),
}
