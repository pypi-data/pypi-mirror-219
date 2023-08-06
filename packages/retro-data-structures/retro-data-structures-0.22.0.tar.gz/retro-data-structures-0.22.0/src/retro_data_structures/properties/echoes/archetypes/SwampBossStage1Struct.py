# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class SwampBossStage1Struct(BaseProperty):
    unknown_0x98106ee2: float = dataclasses.field(default=50.0)
    unknown_0x95e7a2c2: float = dataclasses.field(default=1.0)
    unknown_0x76ba1c18: float = dataclasses.field(default=3.0)
    unknown_0xbb0ffdd6: int = dataclasses.field(default=3)
    unknown_0x60b0ae31: int = dataclasses.field(default=3)
    first_attack: int = dataclasses.field(default=0)
    second_attack: int = dataclasses.field(default=0)
    third_attack: int = dataclasses.field(default=0)
    fourth_attack: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x98\x10n\xe2')  # 0x98106ee2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x98106ee2))

        data.write(b'\x95\xe7\xa2\xc2')  # 0x95e7a2c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95e7a2c2))

        data.write(b'v\xba\x1c\x18')  # 0x76ba1c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76ba1c18))

        data.write(b'\xbb\x0f\xfd\xd6')  # 0xbb0ffdd6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xbb0ffdd6))

        data.write(b'`\xb0\xae1')  # 0x60b0ae31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x60b0ae31))

        data.write(b'\x9c\xfa\x9a\xcb')  # 0x9cfa9acb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.first_attack))

        data.write(b'\x18\x0f\x81\xdd')  # 0x180f81dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.second_attack))

        data.write(b'Ba|\xfd')  # 0x42617cfd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.third_attack))

        data.write(b'\xc3\x9f\x86N')  # 0xc39f864e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.fourth_attack))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x98106ee2=data['unknown_0x98106ee2'],
            unknown_0x95e7a2c2=data['unknown_0x95e7a2c2'],
            unknown_0x76ba1c18=data['unknown_0x76ba1c18'],
            unknown_0xbb0ffdd6=data['unknown_0xbb0ffdd6'],
            unknown_0x60b0ae31=data['unknown_0x60b0ae31'],
            first_attack=data['first_attack'],
            second_attack=data['second_attack'],
            third_attack=data['third_attack'],
            fourth_attack=data['fourth_attack'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x98106ee2': self.unknown_0x98106ee2,
            'unknown_0x95e7a2c2': self.unknown_0x95e7a2c2,
            'unknown_0x76ba1c18': self.unknown_0x76ba1c18,
            'unknown_0xbb0ffdd6': self.unknown_0xbb0ffdd6,
            'unknown_0x60b0ae31': self.unknown_0x60b0ae31,
            'first_attack': self.first_attack,
            'second_attack': self.second_attack,
            'third_attack': self.third_attack,
            'fourth_attack': self.fourth_attack,
        }

    def dependencies_for(self, asset_manager):
        yield from []


_FAST_FORMAT = None
_FAST_IDS = (0x98106ee2, 0x95e7a2c2, 0x76ba1c18, 0xbb0ffdd6, 0x60b0ae31, 0x9cfa9acb, 0x180f81dd, 0x42617cfd, 0xc39f864e)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SwampBossStage1Struct]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHlLHlLHlLHlLHlLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(90))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return SwampBossStage1Struct(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
    )


def _decode_unknown_0x98106ee2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x95e7a2c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ba1c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbb0ffdd6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x60b0ae31(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_first_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_second_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_third_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_fourth_attack(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x98106ee2: ('unknown_0x98106ee2', _decode_unknown_0x98106ee2),
    0x95e7a2c2: ('unknown_0x95e7a2c2', _decode_unknown_0x95e7a2c2),
    0x76ba1c18: ('unknown_0x76ba1c18', _decode_unknown_0x76ba1c18),
    0xbb0ffdd6: ('unknown_0xbb0ffdd6', _decode_unknown_0xbb0ffdd6),
    0x60b0ae31: ('unknown_0x60b0ae31', _decode_unknown_0x60b0ae31),
    0x9cfa9acb: ('first_attack', _decode_first_attack),
    0x180f81dd: ('second_attack', _decode_second_attack),
    0x42617cfd: ('third_attack', _decode_third_attack),
    0xc39f864e: ('fourth_attack', _decode_fourth_attack),
}
