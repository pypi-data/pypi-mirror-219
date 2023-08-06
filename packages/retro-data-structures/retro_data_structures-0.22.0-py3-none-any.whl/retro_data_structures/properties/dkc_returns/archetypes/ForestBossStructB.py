# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct49 import UnknownStruct49


@dataclasses.dataclass()
class ForestBossStructB(BaseProperty):
    unknown_0xc8844cea: float = dataclasses.field(default=10.0)
    unknown_0x9f8a1ca9: float = dataclasses.field(default=30.0)
    unknown_0x72fc2ebd: float = dataclasses.field(default=10.0)
    tired_duration: float = dataclasses.field(default=8.0)
    unknown_0x66b5bc1e: float = dataclasses.field(default=7.0)
    unknown_0xe021ceb0: float = dataclasses.field(default=6.0)
    unknown_0x2b7d1d15: float = dataclasses.field(default=5.0)
    unknown_0xc4a217ad: float = dataclasses.field(default=0.10000000149011612)
    unknown_struct49_0x84df6106: UnknownStruct49 = dataclasses.field(default_factory=UnknownStruct49)
    unknown_struct49_0x9f91359a: UnknownStruct49 = dataclasses.field(default_factory=UnknownStruct49)
    unknown_struct49_0x294bbca0: UnknownStruct49 = dataclasses.field(default_factory=UnknownStruct49)
    flee_duration: float = dataclasses.field(default=20.0)
    unknown_struct49_0x11c70370: UnknownStruct49 = dataclasses.field(default_factory=UnknownStruct49)

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\xc8\x84L\xea')  # 0xc8844cea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc8844cea))

        data.write(b'\x9f\x8a\x1c\xa9')  # 0x9f8a1ca9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9f8a1ca9))

        data.write(b'r\xfc.\xbd')  # 0x72fc2ebd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x72fc2ebd))

        data.write(b'\xd2\xe5.}')  # 0xd2e52e7d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.tired_duration))

        data.write(b'f\xb5\xbc\x1e')  # 0x66b5bc1e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x66b5bc1e))

        data.write(b'\xe0!\xce\xb0')  # 0xe021ceb0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe021ceb0))

        data.write(b'+}\x1d\x15')  # 0x2b7d1d15
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2b7d1d15))

        data.write(b'\xc4\xa2\x17\xad')  # 0xc4a217ad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc4a217ad))

        data.write(b'\x84\xdfa\x06')  # 0x84df6106
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct49_0x84df6106.to_stream(data, default_override={'speed': 6.0, 'acceleration': 10.0, 'deceleration': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9f\x915\x9a')  # 0x9f91359a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct49_0x9f91359a.to_stream(data, default_override={'acceleration': 10.0, 'deceleration': 10.0, 'roll_speed': 480.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b')K\xbc\xa0')  # 0x294bbca0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct49_0x294bbca0.to_stream(data, default_override={'speed': 12.0, 'acceleration': 10.0, 'deceleration': 10.0, 'roll_speed': 180.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\x1c\xc3\x9f')  # 0x501cc39f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flee_duration))

        data.write(b'\x11\xc7\x03p')  # 0x11c70370
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct49_0x11c70370.to_stream(data, default_override={'speed': 20.0, 'deceleration': 20.0, 'roll_speed': 180.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xc8844cea=data['unknown_0xc8844cea'],
            unknown_0x9f8a1ca9=data['unknown_0x9f8a1ca9'],
            unknown_0x72fc2ebd=data['unknown_0x72fc2ebd'],
            tired_duration=data['tired_duration'],
            unknown_0x66b5bc1e=data['unknown_0x66b5bc1e'],
            unknown_0xe021ceb0=data['unknown_0xe021ceb0'],
            unknown_0x2b7d1d15=data['unknown_0x2b7d1d15'],
            unknown_0xc4a217ad=data['unknown_0xc4a217ad'],
            unknown_struct49_0x84df6106=UnknownStruct49.from_json(data['unknown_struct49_0x84df6106']),
            unknown_struct49_0x9f91359a=UnknownStruct49.from_json(data['unknown_struct49_0x9f91359a']),
            unknown_struct49_0x294bbca0=UnknownStruct49.from_json(data['unknown_struct49_0x294bbca0']),
            flee_duration=data['flee_duration'],
            unknown_struct49_0x11c70370=UnknownStruct49.from_json(data['unknown_struct49_0x11c70370']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xc8844cea': self.unknown_0xc8844cea,
            'unknown_0x9f8a1ca9': self.unknown_0x9f8a1ca9,
            'unknown_0x72fc2ebd': self.unknown_0x72fc2ebd,
            'tired_duration': self.tired_duration,
            'unknown_0x66b5bc1e': self.unknown_0x66b5bc1e,
            'unknown_0xe021ceb0': self.unknown_0xe021ceb0,
            'unknown_0x2b7d1d15': self.unknown_0x2b7d1d15,
            'unknown_0xc4a217ad': self.unknown_0xc4a217ad,
            'unknown_struct49_0x84df6106': self.unknown_struct49_0x84df6106.to_json(),
            'unknown_struct49_0x9f91359a': self.unknown_struct49_0x9f91359a.to_json(),
            'unknown_struct49_0x294bbca0': self.unknown_struct49_0x294bbca0.to_json(),
            'flee_duration': self.flee_duration,
            'unknown_struct49_0x11c70370': self.unknown_struct49_0x11c70370.to_json(),
        }


def _decode_unknown_0xc8844cea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9f8a1ca9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x72fc2ebd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tired_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x66b5bc1e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe021ceb0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2b7d1d15(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc4a217ad(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct49_0x84df6106(data: typing.BinaryIO, property_size: int):
    return UnknownStruct49.from_stream(data, property_size, default_override={'speed': 6.0, 'acceleration': 10.0, 'deceleration': 10.0})


def _decode_unknown_struct49_0x9f91359a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct49.from_stream(data, property_size, default_override={'acceleration': 10.0, 'deceleration': 10.0, 'roll_speed': 480.0})


def _decode_unknown_struct49_0x294bbca0(data: typing.BinaryIO, property_size: int):
    return UnknownStruct49.from_stream(data, property_size, default_override={'speed': 12.0, 'acceleration': 10.0, 'deceleration': 10.0, 'roll_speed': 180.0})


def _decode_flee_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct49_0x11c70370(data: typing.BinaryIO, property_size: int):
    return UnknownStruct49.from_stream(data, property_size, default_override={'speed': 20.0, 'deceleration': 20.0, 'roll_speed': 180.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc8844cea: ('unknown_0xc8844cea', _decode_unknown_0xc8844cea),
    0x9f8a1ca9: ('unknown_0x9f8a1ca9', _decode_unknown_0x9f8a1ca9),
    0x72fc2ebd: ('unknown_0x72fc2ebd', _decode_unknown_0x72fc2ebd),
    0xd2e52e7d: ('tired_duration', _decode_tired_duration),
    0x66b5bc1e: ('unknown_0x66b5bc1e', _decode_unknown_0x66b5bc1e),
    0xe021ceb0: ('unknown_0xe021ceb0', _decode_unknown_0xe021ceb0),
    0x2b7d1d15: ('unknown_0x2b7d1d15', _decode_unknown_0x2b7d1d15),
    0xc4a217ad: ('unknown_0xc4a217ad', _decode_unknown_0xc4a217ad),
    0x84df6106: ('unknown_struct49_0x84df6106', _decode_unknown_struct49_0x84df6106),
    0x9f91359a: ('unknown_struct49_0x9f91359a', _decode_unknown_struct49_0x9f91359a),
    0x294bbca0: ('unknown_struct49_0x294bbca0', _decode_unknown_struct49_0x294bbca0),
    0x501cc39f: ('flee_duration', _decode_flee_duration),
    0x11c70370: ('unknown_struct49_0x11c70370', _decode_unknown_struct49_0x11c70370),
}
