# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.GenericCreatureStructE import GenericCreatureStructE


@dataclasses.dataclass()
class Animations(BaseProperty):
    number_of_animations: int = dataclasses.field(default=0)
    animation01: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation02: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation03: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation04: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation05: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation06: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation07: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation08: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation09: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation10: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation11: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation12: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation13: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation14: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation15: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)
    animation16: GenericCreatureStructE = dataclasses.field(default_factory=GenericCreatureStructE)

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'h*\xa3\xc9')  # 0x682aa3c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_animations))

        data.write(b'\x12J2\xa3')  # 0x124a32a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation01.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\xeb\x17\xbb')  # 0x56eb17bb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'j\x8b\xf4\xb3')  # 0x6a8bf4b3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation03.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\xa9]\x8b')  # 0xdfa95d8b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation04.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe3\xc9\xbe\x83')  # 0xe3c9be83
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation05.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa7h\x9b\x9b')  # 0xa7689b9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation06.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\x08x\x93')  # 0x9b087893
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation07.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16\\\xcf\xaa')  # 0x165ccfaa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation08.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*<,\xa2')  # 0x2a3c2ca2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation09.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \xcd9z')  # 0x20cd397a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation10.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c\xad\xdar')  # 0x1cadda72
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation11.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\x0c\xffj')  # 0x580cff6a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation12.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'dl\x1cb')  # 0x646c1c62
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation13.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1N\xb5Z')  # 0xd14eb55a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation14.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed.VR')  # 0xed2e5652
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation15.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa9\x8fsJ')  # 0xa98f734a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation16.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            number_of_animations=data['number_of_animations'],
            animation01=GenericCreatureStructE.from_json(data['animation01']),
            animation02=GenericCreatureStructE.from_json(data['animation02']),
            animation03=GenericCreatureStructE.from_json(data['animation03']),
            animation04=GenericCreatureStructE.from_json(data['animation04']),
            animation05=GenericCreatureStructE.from_json(data['animation05']),
            animation06=GenericCreatureStructE.from_json(data['animation06']),
            animation07=GenericCreatureStructE.from_json(data['animation07']),
            animation08=GenericCreatureStructE.from_json(data['animation08']),
            animation09=GenericCreatureStructE.from_json(data['animation09']),
            animation10=GenericCreatureStructE.from_json(data['animation10']),
            animation11=GenericCreatureStructE.from_json(data['animation11']),
            animation12=GenericCreatureStructE.from_json(data['animation12']),
            animation13=GenericCreatureStructE.from_json(data['animation13']),
            animation14=GenericCreatureStructE.from_json(data['animation14']),
            animation15=GenericCreatureStructE.from_json(data['animation15']),
            animation16=GenericCreatureStructE.from_json(data['animation16']),
        )

    def to_json(self) -> dict:
        return {
            'number_of_animations': self.number_of_animations,
            'animation01': self.animation01.to_json(),
            'animation02': self.animation02.to_json(),
            'animation03': self.animation03.to_json(),
            'animation04': self.animation04.to_json(),
            'animation05': self.animation05.to_json(),
            'animation06': self.animation06.to_json(),
            'animation07': self.animation07.to_json(),
            'animation08': self.animation08.to_json(),
            'animation09': self.animation09.to_json(),
            'animation10': self.animation10.to_json(),
            'animation11': self.animation11.to_json(),
            'animation12': self.animation12.to_json(),
            'animation13': self.animation13.to_json(),
            'animation14': self.animation14.to_json(),
            'animation15': self.animation15.to_json(),
            'animation16': self.animation16.to_json(),
        }


def _decode_number_of_animations(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_animation01(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation02(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation03(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation04(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation05(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation06(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation07(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation08(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation09(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation10(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation11(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation12(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation13(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation14(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation15(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


def _decode_animation16(data: typing.BinaryIO, property_size: int):
    return GenericCreatureStructE.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x682aa3c9: ('number_of_animations', _decode_number_of_animations),
    0x124a32a3: ('animation01', _decode_animation01),
    0x56eb17bb: ('animation02', _decode_animation02),
    0x6a8bf4b3: ('animation03', _decode_animation03),
    0xdfa95d8b: ('animation04', _decode_animation04),
    0xe3c9be83: ('animation05', _decode_animation05),
    0xa7689b9b: ('animation06', _decode_animation06),
    0x9b087893: ('animation07', _decode_animation07),
    0x165ccfaa: ('animation08', _decode_animation08),
    0x2a3c2ca2: ('animation09', _decode_animation09),
    0x20cd397a: ('animation10', _decode_animation10),
    0x1cadda72: ('animation11', _decode_animation11),
    0x580cff6a: ('animation12', _decode_animation12),
    0x646c1c62: ('animation13', _decode_animation13),
    0xd14eb55a: ('animation14', _decode_animation14),
    0xed2e5652: ('animation15', _decode_animation15),
    0xa98f734a: ('animation16', _decode_animation16),
}
