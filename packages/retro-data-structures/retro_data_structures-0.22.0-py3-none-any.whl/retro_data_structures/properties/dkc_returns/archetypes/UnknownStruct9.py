# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct9(BaseProperty):
    unknown_0x5d28cce5: float = dataclasses.field(default=0.0)
    unknown_0x1fe2e0b4: float = dataclasses.field(default=1.0)
    lerp_duration: float = dataclasses.field(default=1.0)
    unknown_0x9adf7732: bool = dataclasses.field(default=False)
    unknown_0x7fbfe9fd: bool = dataclasses.field(default=True)
    unknown_0x6a54d863: bool = dataclasses.field(default=False)
    unknown_0x17d5302a: float = dataclasses.field(default=7.0)
    unknown_0xfa271b70: bool = dataclasses.field(default=False)
    unknown_0x5c927fb2: float = dataclasses.field(default=5.0)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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

        data.write(b'](\xcc\xe5')  # 0x5d28cce5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5d28cce5))

        data.write(b'\x1f\xe2\xe0\xb4')  # 0x1fe2e0b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1fe2e0b4))

        data.write(b'\x829\xd0L')  # 0x8239d04c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lerp_duration))

        data.write(b'\x9a\xdfw2')  # 0x9adf7732
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9adf7732))

        data.write(b'\x7f\xbf\xe9\xfd')  # 0x7fbfe9fd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x7fbfe9fd))

        data.write(b'jT\xd8c')  # 0x6a54d863
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6a54d863))

        data.write(b'\x17\xd50*')  # 0x17d5302a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x17d5302a))

        data.write(b"\xfa'\x1bp")  # 0xfa271b70
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xfa271b70))

        data.write(b'\\\x92\x7f\xb2')  # 0x5c927fb2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5c927fb2))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x5d28cce5=data['unknown_0x5d28cce5'],
            unknown_0x1fe2e0b4=data['unknown_0x1fe2e0b4'],
            lerp_duration=data['lerp_duration'],
            unknown_0x9adf7732=data['unknown_0x9adf7732'],
            unknown_0x7fbfe9fd=data['unknown_0x7fbfe9fd'],
            unknown_0x6a54d863=data['unknown_0x6a54d863'],
            unknown_0x17d5302a=data['unknown_0x17d5302a'],
            unknown_0xfa271b70=data['unknown_0xfa271b70'],
            unknown_0x5c927fb2=data['unknown_0x5c927fb2'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x5d28cce5': self.unknown_0x5d28cce5,
            'unknown_0x1fe2e0b4': self.unknown_0x1fe2e0b4,
            'lerp_duration': self.lerp_duration,
            'unknown_0x9adf7732': self.unknown_0x9adf7732,
            'unknown_0x7fbfe9fd': self.unknown_0x7fbfe9fd,
            'unknown_0x6a54d863': self.unknown_0x6a54d863,
            'unknown_0x17d5302a': self.unknown_0x17d5302a,
            'unknown_0xfa271b70': self.unknown_0xfa271b70,
            'unknown_0x5c927fb2': self.unknown_0x5c927fb2,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x5d28cce5, 0x1fe2e0b4, 0x8239d04c, 0x9adf7732, 0x7fbfe9fd, 0x6a54d863, 0x17d5302a, 0xfa271b70, 0x5c927fb2)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct9]:
    if property_count != 9:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLH?LH?LH?LHfLH?LHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(78))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct9(
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


def _decode_unknown_0x5d28cce5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1fe2e0b4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lerp_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9adf7732(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x7fbfe9fd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x6a54d863(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x17d5302a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfa271b70(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x5c927fb2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5d28cce5: ('unknown_0x5d28cce5', _decode_unknown_0x5d28cce5),
    0x1fe2e0b4: ('unknown_0x1fe2e0b4', _decode_unknown_0x1fe2e0b4),
    0x8239d04c: ('lerp_duration', _decode_lerp_duration),
    0x9adf7732: ('unknown_0x9adf7732', _decode_unknown_0x9adf7732),
    0x7fbfe9fd: ('unknown_0x7fbfe9fd', _decode_unknown_0x7fbfe9fd),
    0x6a54d863: ('unknown_0x6a54d863', _decode_unknown_0x6a54d863),
    0x17d5302a: ('unknown_0x17d5302a', _decode_unknown_0x17d5302a),
    0xfa271b70: ('unknown_0xfa271b70', _decode_unknown_0xfa271b70),
    0x5c927fb2: ('unknown_0x5c927fb2', _decode_unknown_0x5c927fb2),
}
