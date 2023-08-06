# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class MoleTrainManagerStructA(BaseProperty):
    unknown_0xee447d6b: bool = dataclasses.field(default=True)
    unknown_0x4d765168: float = dataclasses.field(default=46.0)
    unknown_0x4f01c9e2: float = dataclasses.field(default=36.0)
    chase_offset: float = dataclasses.field(default=25.0)
    chase_speed: float = dataclasses.field(default=11.0)
    unknown_0xd33f6240: float = dataclasses.field(default=12.0)
    chase_delay: float = dataclasses.field(default=5.0)

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\xeeD}k')  # 0xee447d6b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xee447d6b))

        data.write(b'MvQh')  # 0x4d765168
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4d765168))

        data.write(b'O\x01\xc9\xe2')  # 0x4f01c9e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4f01c9e2))

        data.write(b'\xed\rh\x95')  # 0xed0d6895
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chase_offset))

        data.write(b'\x92\xfb\xc1a')  # 0x92fbc161
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chase_speed))

        data.write(b'\xd3?b@')  # 0xd33f6240
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd33f6240))

        data.write(b'\xe5\x96r\xb3')  # 0xe59672b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chase_delay))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xee447d6b=data['unknown_0xee447d6b'],
            unknown_0x4d765168=data['unknown_0x4d765168'],
            unknown_0x4f01c9e2=data['unknown_0x4f01c9e2'],
            chase_offset=data['chase_offset'],
            chase_speed=data['chase_speed'],
            unknown_0xd33f6240=data['unknown_0xd33f6240'],
            chase_delay=data['chase_delay'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xee447d6b': self.unknown_0xee447d6b,
            'unknown_0x4d765168': self.unknown_0x4d765168,
            'unknown_0x4f01c9e2': self.unknown_0x4f01c9e2,
            'chase_offset': self.chase_offset,
            'chase_speed': self.chase_speed,
            'unknown_0xd33f6240': self.unknown_0xd33f6240,
            'chase_delay': self.chase_delay,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xee447d6b, 0x4d765168, 0x4f01c9e2, 0xed0d6895, 0x92fbc161, 0xd33f6240, 0xe59672b3)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[MoleTrainManagerStructA]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(67))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return MoleTrainManagerStructA(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_unknown_0xee447d6b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x4d765168(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4f01c9e2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chase_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chase_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd33f6240(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chase_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xee447d6b: ('unknown_0xee447d6b', _decode_unknown_0xee447d6b),
    0x4d765168: ('unknown_0x4d765168', _decode_unknown_0x4d765168),
    0x4f01c9e2: ('unknown_0x4f01c9e2', _decode_unknown_0x4f01c9e2),
    0xed0d6895: ('chase_offset', _decode_chase_offset),
    0x92fbc161: ('chase_speed', _decode_chase_speed),
    0xd33f6240: ('unknown_0xd33f6240', _decode_unknown_0xd33f6240),
    0xe59672b3: ('chase_delay', _decode_chase_delay),
}
