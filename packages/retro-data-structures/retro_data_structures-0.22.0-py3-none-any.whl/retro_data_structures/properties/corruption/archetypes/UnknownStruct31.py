# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct31(BaseProperty):
    initial_morph_time: float = dataclasses.field(default=15.0)
    unknown_0xc8cfc063: float = dataclasses.field(default=15.0)
    unknown_0x80c0d235: float = dataclasses.field(default=85.0)
    unknown_0x26fa79a3: float = dataclasses.field(default=20.0)
    unknown_0xc77f29dc: float = dataclasses.field(default=0.0)
    gandrayda_to_berserker: float = dataclasses.field(default=20.0)
    unknown_0xcbbd9a4e: float = dataclasses.field(default=40.0)
    gandrayda_to_swarm: float = dataclasses.field(default=40.0)
    unknown_0xa2675081: float = dataclasses.field(default=20.0)
    unknown_0x413aee5b: float = dataclasses.field(default=30.0)
    unknown_0x931ea2ea: float = dataclasses.field(default=10.0)
    unknown_0x144f7ed6: float = dataclasses.field(default=45.0)
    unknown_0x659d7d56: float = dataclasses.field(default=45.0)
    unknown_0x7a11bb7b: float = dataclasses.field(default=60.0)
    unknown_0xb4089be1: float = dataclasses.field(default=0.0)
    swarm_to_gandrayda: float = dataclasses.field(default=90.0)
    swarm_to_berserker: float = dataclasses.field(default=10.0)
    unknown_0x73ac8586: float = dataclasses.field(default=60.0)
    unknown_0x704c4fc6: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'E\x16\x11\t')  # 0x45161109
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_morph_time))

        data.write(b'\xc8\xcf\xc0c')  # 0xc8cfc063
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc8cfc063))

        data.write(b'\x80\xc0\xd25')  # 0x80c0d235
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x80c0d235))

        data.write(b'&\xfay\xa3')  # 0x26fa79a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x26fa79a3))

        data.write(b'\xc7\x7f)\xdc')  # 0xc77f29dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc77f29dc))

        data.write(b'\x14\x14s\xb5')  # 0x141473b5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gandrayda_to_berserker))

        data.write(b'\xcb\xbd\x9aN')  # 0xcbbd9a4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcbbd9a4e))

        data.write(b'\x8d|a\x03')  # 0x8d7c6103
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gandrayda_to_swarm))

        data.write(b'\xa2gP\x81')  # 0xa2675081
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa2675081))

        data.write(b'A:\xee[')  # 0x413aee5b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x413aee5b))

        data.write(b'\x93\x1e\xa2\xea')  # 0x931ea2ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x931ea2ea))

        data.write(b'\x14O~\xd6')  # 0x144f7ed6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x144f7ed6))

        data.write(b'e\x9d}V')  # 0x659d7d56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x659d7d56))

        data.write(b'z\x11\xbb{')  # 0x7a11bb7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7a11bb7b))

        data.write(b'\xb4\x08\x9b\xe1')  # 0xb4089be1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb4089be1))

        data.write(b' #Z1')  # 0x20235a31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swarm_to_gandrayda))

        data.write(b'\xa7r\x86\r')  # 0xa772860d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swarm_to_berserker))

        data.write(b's\xac\x85\x86')  # 0x73ac8586
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x73ac8586))

        data.write(b'pLO\xc6')  # 0x704c4fc6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x704c4fc6))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            initial_morph_time=data['initial_morph_time'],
            unknown_0xc8cfc063=data['unknown_0xc8cfc063'],
            unknown_0x80c0d235=data['unknown_0x80c0d235'],
            unknown_0x26fa79a3=data['unknown_0x26fa79a3'],
            unknown_0xc77f29dc=data['unknown_0xc77f29dc'],
            gandrayda_to_berserker=data['gandrayda_to_berserker'],
            unknown_0xcbbd9a4e=data['unknown_0xcbbd9a4e'],
            gandrayda_to_swarm=data['gandrayda_to_swarm'],
            unknown_0xa2675081=data['unknown_0xa2675081'],
            unknown_0x413aee5b=data['unknown_0x413aee5b'],
            unknown_0x931ea2ea=data['unknown_0x931ea2ea'],
            unknown_0x144f7ed6=data['unknown_0x144f7ed6'],
            unknown_0x659d7d56=data['unknown_0x659d7d56'],
            unknown_0x7a11bb7b=data['unknown_0x7a11bb7b'],
            unknown_0xb4089be1=data['unknown_0xb4089be1'],
            swarm_to_gandrayda=data['swarm_to_gandrayda'],
            swarm_to_berserker=data['swarm_to_berserker'],
            unknown_0x73ac8586=data['unknown_0x73ac8586'],
            unknown_0x704c4fc6=data['unknown_0x704c4fc6'],
        )

    def to_json(self) -> dict:
        return {
            'initial_morph_time': self.initial_morph_time,
            'unknown_0xc8cfc063': self.unknown_0xc8cfc063,
            'unknown_0x80c0d235': self.unknown_0x80c0d235,
            'unknown_0x26fa79a3': self.unknown_0x26fa79a3,
            'unknown_0xc77f29dc': self.unknown_0xc77f29dc,
            'gandrayda_to_berserker': self.gandrayda_to_berserker,
            'unknown_0xcbbd9a4e': self.unknown_0xcbbd9a4e,
            'gandrayda_to_swarm': self.gandrayda_to_swarm,
            'unknown_0xa2675081': self.unknown_0xa2675081,
            'unknown_0x413aee5b': self.unknown_0x413aee5b,
            'unknown_0x931ea2ea': self.unknown_0x931ea2ea,
            'unknown_0x144f7ed6': self.unknown_0x144f7ed6,
            'unknown_0x659d7d56': self.unknown_0x659d7d56,
            'unknown_0x7a11bb7b': self.unknown_0x7a11bb7b,
            'unknown_0xb4089be1': self.unknown_0xb4089be1,
            'swarm_to_gandrayda': self.swarm_to_gandrayda,
            'swarm_to_berserker': self.swarm_to_berserker,
            'unknown_0x73ac8586': self.unknown_0x73ac8586,
            'unknown_0x704c4fc6': self.unknown_0x704c4fc6,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x45161109, 0xc8cfc063, 0x80c0d235, 0x26fa79a3, 0xc77f29dc, 0x141473b5, 0xcbbd9a4e, 0x8d7c6103, 0xa2675081, 0x413aee5b, 0x931ea2ea, 0x144f7ed6, 0x659d7d56, 0x7a11bb7b, 0xb4089be1, 0x20235a31, 0xa772860d, 0x73ac8586, 0x704c4fc6)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct31]:
    if property_count != 19:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(190))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct31(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
        dec[35],
        dec[38],
        dec[41],
        dec[44],
        dec[47],
        dec[50],
        dec[53],
        dec[56],
    )


def _decode_initial_morph_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc8cfc063(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x80c0d235(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x26fa79a3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc77f29dc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gandrayda_to_berserker(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcbbd9a4e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gandrayda_to_swarm(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa2675081(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x413aee5b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x931ea2ea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x144f7ed6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x659d7d56(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7a11bb7b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb4089be1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swarm_to_gandrayda(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swarm_to_berserker(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x73ac8586(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x704c4fc6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x45161109: ('initial_morph_time', _decode_initial_morph_time),
    0xc8cfc063: ('unknown_0xc8cfc063', _decode_unknown_0xc8cfc063),
    0x80c0d235: ('unknown_0x80c0d235', _decode_unknown_0x80c0d235),
    0x26fa79a3: ('unknown_0x26fa79a3', _decode_unknown_0x26fa79a3),
    0xc77f29dc: ('unknown_0xc77f29dc', _decode_unknown_0xc77f29dc),
    0x141473b5: ('gandrayda_to_berserker', _decode_gandrayda_to_berserker),
    0xcbbd9a4e: ('unknown_0xcbbd9a4e', _decode_unknown_0xcbbd9a4e),
    0x8d7c6103: ('gandrayda_to_swarm', _decode_gandrayda_to_swarm),
    0xa2675081: ('unknown_0xa2675081', _decode_unknown_0xa2675081),
    0x413aee5b: ('unknown_0x413aee5b', _decode_unknown_0x413aee5b),
    0x931ea2ea: ('unknown_0x931ea2ea', _decode_unknown_0x931ea2ea),
    0x144f7ed6: ('unknown_0x144f7ed6', _decode_unknown_0x144f7ed6),
    0x659d7d56: ('unknown_0x659d7d56', _decode_unknown_0x659d7d56),
    0x7a11bb7b: ('unknown_0x7a11bb7b', _decode_unknown_0x7a11bb7b),
    0xb4089be1: ('unknown_0xb4089be1', _decode_unknown_0xb4089be1),
    0x20235a31: ('swarm_to_gandrayda', _decode_swarm_to_gandrayda),
    0xa772860d: ('swarm_to_berserker', _decode_swarm_to_berserker),
    0x73ac8586: ('unknown_0x73ac8586', _decode_unknown_0x73ac8586),
    0x704c4fc6: ('unknown_0x704c4fc6', _decode_unknown_0x704c4fc6),
}
