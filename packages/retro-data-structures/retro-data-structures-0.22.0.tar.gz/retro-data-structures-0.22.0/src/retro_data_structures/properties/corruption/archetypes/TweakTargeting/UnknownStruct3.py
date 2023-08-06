# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.Color import Color
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct3(BaseProperty):
    unknown_0x77feeef0: float = dataclasses.field(default=0.15000000596046448)
    unknown_0x6c68981b: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    orbit_lock_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x1b905dfe: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x05ee18e2: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x337e60a9: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0x4f635051: float = dataclasses.field(default=0.25)
    unknown_0x20af6870: float = dataclasses.field(default=0.25)
    unknown_0x0a5848fb: float = dataclasses.field(default=120.0)
    unknown_0x01b64bdf: float = dataclasses.field(default=1.0)
    unknown_0xd4044569: float = dataclasses.field(default=1.0)
    unknown_0xae6c5261: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x84ac3eee: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x396d001e: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0xe8008fa5: float = dataclasses.field(default=54.0)
    unknown_0xe9c116bf: float = dataclasses.field(default=0.5)
    unknown_0x79f18548: float = dataclasses.field(default=0.25)
    unknown_0x26978c4b: float = dataclasses.field(default=0.15000000596046448)
    unknown_0x9d58f885: float = dataclasses.field(default=0.125)
    unknown_0x99c2c9af: float = dataclasses.field(default=0.4000000059604645)
    unknown_0x326905f2: float = dataclasses.field(default=1.0)
    unknown_0x3cf144d1: float = dataclasses.field(default=0.0)
    unknown_0x7975982c: float = dataclasses.field(default=0.25)
    unknown_0x460b2702: float = dataclasses.field(default=3.0)
    unknown_0x43c8a56e: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x83f19d56: float = dataclasses.field(default=0.25)
    unknown_0xa9cd091f: float = dataclasses.field(default=0.25)
    unknown_0xe589a4f9: float = dataclasses.field(default=0.4000000059604645)
    unknown_0xd7cf6cc5: float = dataclasses.field(default=0.5)
    unknown_0x85e956d3: float = dataclasses.field(default=0.8999999761581421)
    unknown_0xa6f2b827: float = dataclasses.field(default=135.0)
    unknown_0xca637bcd: float = dataclasses.field(default=0.3499999940395355)
    unknown_0xf04414b3: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00!')  # 33 properties

        data.write(b'w\xfe\xee\xf0')  # 0x77feeef0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x77feeef0))

        data.write(b'lh\x98\x1b')  # 0x6c68981b
        data.write(b'\x00\x10')  # size
        self.unknown_0x6c68981b.to_stream(data)

        data.write(b'm[\xc9\xc5')  # 0x6d5bc9c5
        data.write(b'\x00\x10')  # size
        self.orbit_lock_color.to_stream(data)

        data.write(b'\x1b\x90]\xfe')  # 0x1b905dfe
        data.write(b'\x00\x10')  # size
        self.unknown_0x1b905dfe.to_stream(data)

        data.write(b'\x05\xee\x18\xe2')  # 0x5ee18e2
        data.write(b'\x00\x10')  # size
        self.unknown_0x05ee18e2.to_stream(data)

        data.write(b'3~`\xa9')  # 0x337e60a9
        data.write(b'\x00\x0c')  # size
        self.unknown_0x337e60a9.to_stream(data)

        data.write(b'OcPQ')  # 0x4f635051
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4f635051))

        data.write(b' \xafhp')  # 0x20af6870
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x20af6870))

        data.write(b'\nXH\xfb')  # 0xa5848fb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0a5848fb))

        data.write(b'\x01\xb6K\xdf')  # 0x1b64bdf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x01b64bdf))

        data.write(b'\xd4\x04Ei')  # 0xd4044569
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd4044569))

        data.write(b'\xaelRa')  # 0xae6c5261
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xae6c5261))

        data.write(b'\x84\xac>\xee')  # 0x84ac3eee
        data.write(b'\x00\x10')  # size
        self.unknown_0x84ac3eee.to_stream(data)

        data.write(b'9m\x00\x1e')  # 0x396d001e
        data.write(b'\x00\x10')  # size
        self.unknown_0x396d001e.to_stream(data)

        data.write(b'\xe8\x00\x8f\xa5')  # 0xe8008fa5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe8008fa5))

        data.write(b'\xe9\xc1\x16\xbf')  # 0xe9c116bf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe9c116bf))

        data.write(b'y\xf1\x85H')  # 0x79f18548
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x79f18548))

        data.write(b'&\x97\x8cK')  # 0x26978c4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x26978c4b))

        data.write(b'\x9dX\xf8\x85')  # 0x9d58f885
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9d58f885))

        data.write(b'\x99\xc2\xc9\xaf')  # 0x99c2c9af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x99c2c9af))

        data.write(b'2i\x05\xf2')  # 0x326905f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x326905f2))

        data.write(b'<\xf1D\xd1')  # 0x3cf144d1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3cf144d1))

        data.write(b'yu\x98,')  # 0x7975982c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7975982c))

        data.write(b"F\x0b'\x02")  # 0x460b2702
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x460b2702))

        data.write(b'C\xc8\xa5n')  # 0x43c8a56e
        data.write(b'\x00\x10')  # size
        self.unknown_0x43c8a56e.to_stream(data)

        data.write(b'\x83\xf1\x9dV')  # 0x83f19d56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x83f19d56))

        data.write(b'\xa9\xcd\t\x1f')  # 0xa9cd091f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa9cd091f))

        data.write(b'\xe5\x89\xa4\xf9')  # 0xe589a4f9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe589a4f9))

        data.write(b'\xd7\xcfl\xc5')  # 0xd7cf6cc5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd7cf6cc5))

        data.write(b'\x85\xe9V\xd3')  # 0x85e956d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x85e956d3))

        data.write(b"\xa6\xf2\xb8'")  # 0xa6f2b827
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa6f2b827))

        data.write(b'\xcac{\xcd')  # 0xca637bcd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xca637bcd))

        data.write(b'\xf0D\x14\xb3')  # 0xf04414b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf04414b3))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x77feeef0=data['unknown_0x77feeef0'],
            unknown_0x6c68981b=Color.from_json(data['unknown_0x6c68981b']),
            orbit_lock_color=Color.from_json(data['orbit_lock_color']),
            unknown_0x1b905dfe=Color.from_json(data['unknown_0x1b905dfe']),
            unknown_0x05ee18e2=Color.from_json(data['unknown_0x05ee18e2']),
            unknown_0x337e60a9=Vector.from_json(data['unknown_0x337e60a9']),
            unknown_0x4f635051=data['unknown_0x4f635051'],
            unknown_0x20af6870=data['unknown_0x20af6870'],
            unknown_0x0a5848fb=data['unknown_0x0a5848fb'],
            unknown_0x01b64bdf=data['unknown_0x01b64bdf'],
            unknown_0xd4044569=data['unknown_0xd4044569'],
            unknown_0xae6c5261=data['unknown_0xae6c5261'],
            unknown_0x84ac3eee=Color.from_json(data['unknown_0x84ac3eee']),
            unknown_0x396d001e=Color.from_json(data['unknown_0x396d001e']),
            unknown_0xe8008fa5=data['unknown_0xe8008fa5'],
            unknown_0xe9c116bf=data['unknown_0xe9c116bf'],
            unknown_0x79f18548=data['unknown_0x79f18548'],
            unknown_0x26978c4b=data['unknown_0x26978c4b'],
            unknown_0x9d58f885=data['unknown_0x9d58f885'],
            unknown_0x99c2c9af=data['unknown_0x99c2c9af'],
            unknown_0x326905f2=data['unknown_0x326905f2'],
            unknown_0x3cf144d1=data['unknown_0x3cf144d1'],
            unknown_0x7975982c=data['unknown_0x7975982c'],
            unknown_0x460b2702=data['unknown_0x460b2702'],
            unknown_0x43c8a56e=Color.from_json(data['unknown_0x43c8a56e']),
            unknown_0x83f19d56=data['unknown_0x83f19d56'],
            unknown_0xa9cd091f=data['unknown_0xa9cd091f'],
            unknown_0xe589a4f9=data['unknown_0xe589a4f9'],
            unknown_0xd7cf6cc5=data['unknown_0xd7cf6cc5'],
            unknown_0x85e956d3=data['unknown_0x85e956d3'],
            unknown_0xa6f2b827=data['unknown_0xa6f2b827'],
            unknown_0xca637bcd=data['unknown_0xca637bcd'],
            unknown_0xf04414b3=data['unknown_0xf04414b3'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x77feeef0': self.unknown_0x77feeef0,
            'unknown_0x6c68981b': self.unknown_0x6c68981b.to_json(),
            'orbit_lock_color': self.orbit_lock_color.to_json(),
            'unknown_0x1b905dfe': self.unknown_0x1b905dfe.to_json(),
            'unknown_0x05ee18e2': self.unknown_0x05ee18e2.to_json(),
            'unknown_0x337e60a9': self.unknown_0x337e60a9.to_json(),
            'unknown_0x4f635051': self.unknown_0x4f635051,
            'unknown_0x20af6870': self.unknown_0x20af6870,
            'unknown_0x0a5848fb': self.unknown_0x0a5848fb,
            'unknown_0x01b64bdf': self.unknown_0x01b64bdf,
            'unknown_0xd4044569': self.unknown_0xd4044569,
            'unknown_0xae6c5261': self.unknown_0xae6c5261,
            'unknown_0x84ac3eee': self.unknown_0x84ac3eee.to_json(),
            'unknown_0x396d001e': self.unknown_0x396d001e.to_json(),
            'unknown_0xe8008fa5': self.unknown_0xe8008fa5,
            'unknown_0xe9c116bf': self.unknown_0xe9c116bf,
            'unknown_0x79f18548': self.unknown_0x79f18548,
            'unknown_0x26978c4b': self.unknown_0x26978c4b,
            'unknown_0x9d58f885': self.unknown_0x9d58f885,
            'unknown_0x99c2c9af': self.unknown_0x99c2c9af,
            'unknown_0x326905f2': self.unknown_0x326905f2,
            'unknown_0x3cf144d1': self.unknown_0x3cf144d1,
            'unknown_0x7975982c': self.unknown_0x7975982c,
            'unknown_0x460b2702': self.unknown_0x460b2702,
            'unknown_0x43c8a56e': self.unknown_0x43c8a56e.to_json(),
            'unknown_0x83f19d56': self.unknown_0x83f19d56,
            'unknown_0xa9cd091f': self.unknown_0xa9cd091f,
            'unknown_0xe589a4f9': self.unknown_0xe589a4f9,
            'unknown_0xd7cf6cc5': self.unknown_0xd7cf6cc5,
            'unknown_0x85e956d3': self.unknown_0x85e956d3,
            'unknown_0xa6f2b827': self.unknown_0xa6f2b827,
            'unknown_0xca637bcd': self.unknown_0xca637bcd,
            'unknown_0xf04414b3': self.unknown_0xf04414b3,
        }


def _decode_unknown_0x77feeef0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6c68981b(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_orbit_lock_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x1b905dfe(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x05ee18e2(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x337e60a9(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x4f635051(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x20af6870(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0a5848fb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x01b64bdf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd4044569(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xae6c5261(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x84ac3eee(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x396d001e(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0xe8008fa5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe9c116bf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x79f18548(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x26978c4b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9d58f885(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x99c2c9af(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x326905f2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3cf144d1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7975982c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x460b2702(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x43c8a56e(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x83f19d56(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa9cd091f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe589a4f9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd7cf6cc5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x85e956d3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa6f2b827(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xca637bcd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf04414b3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x77feeef0: ('unknown_0x77feeef0', _decode_unknown_0x77feeef0),
    0x6c68981b: ('unknown_0x6c68981b', _decode_unknown_0x6c68981b),
    0x6d5bc9c5: ('orbit_lock_color', _decode_orbit_lock_color),
    0x1b905dfe: ('unknown_0x1b905dfe', _decode_unknown_0x1b905dfe),
    0x5ee18e2: ('unknown_0x05ee18e2', _decode_unknown_0x05ee18e2),
    0x337e60a9: ('unknown_0x337e60a9', _decode_unknown_0x337e60a9),
    0x4f635051: ('unknown_0x4f635051', _decode_unknown_0x4f635051),
    0x20af6870: ('unknown_0x20af6870', _decode_unknown_0x20af6870),
    0xa5848fb: ('unknown_0x0a5848fb', _decode_unknown_0x0a5848fb),
    0x1b64bdf: ('unknown_0x01b64bdf', _decode_unknown_0x01b64bdf),
    0xd4044569: ('unknown_0xd4044569', _decode_unknown_0xd4044569),
    0xae6c5261: ('unknown_0xae6c5261', _decode_unknown_0xae6c5261),
    0x84ac3eee: ('unknown_0x84ac3eee', _decode_unknown_0x84ac3eee),
    0x396d001e: ('unknown_0x396d001e', _decode_unknown_0x396d001e),
    0xe8008fa5: ('unknown_0xe8008fa5', _decode_unknown_0xe8008fa5),
    0xe9c116bf: ('unknown_0xe9c116bf', _decode_unknown_0xe9c116bf),
    0x79f18548: ('unknown_0x79f18548', _decode_unknown_0x79f18548),
    0x26978c4b: ('unknown_0x26978c4b', _decode_unknown_0x26978c4b),
    0x9d58f885: ('unknown_0x9d58f885', _decode_unknown_0x9d58f885),
    0x99c2c9af: ('unknown_0x99c2c9af', _decode_unknown_0x99c2c9af),
    0x326905f2: ('unknown_0x326905f2', _decode_unknown_0x326905f2),
    0x3cf144d1: ('unknown_0x3cf144d1', _decode_unknown_0x3cf144d1),
    0x7975982c: ('unknown_0x7975982c', _decode_unknown_0x7975982c),
    0x460b2702: ('unknown_0x460b2702', _decode_unknown_0x460b2702),
    0x43c8a56e: ('unknown_0x43c8a56e', _decode_unknown_0x43c8a56e),
    0x83f19d56: ('unknown_0x83f19d56', _decode_unknown_0x83f19d56),
    0xa9cd091f: ('unknown_0xa9cd091f', _decode_unknown_0xa9cd091f),
    0xe589a4f9: ('unknown_0xe589a4f9', _decode_unknown_0xe589a4f9),
    0xd7cf6cc5: ('unknown_0xd7cf6cc5', _decode_unknown_0xd7cf6cc5),
    0x85e956d3: ('unknown_0x85e956d3', _decode_unknown_0x85e956d3),
    0xa6f2b827: ('unknown_0xa6f2b827', _decode_unknown_0xa6f2b827),
    0xca637bcd: ('unknown_0xca637bcd', _decode_unknown_0xca637bcd),
    0xf04414b3: ('unknown_0xf04414b3', _decode_unknown_0xf04414b3),
}
