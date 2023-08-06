# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct207(BaseProperty):
    distance0: float = dataclasses.field(default=6.5)
    distance1: float = dataclasses.field(default=9.0)
    distance2: float = dataclasses.field(default=13.5)
    distance3: float = dataclasses.field(default=18.0)
    distance4: float = dataclasses.field(default=20.0)
    distance5: float = dataclasses.field(default=27.0)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xc4\x8b\x03V')  # 0xc48b0356
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance0))

        data.write(b'\x0f\xd7\xd0\xf3')  # 0xfd7d0f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance1))

        data.write(b'\x89C\xa2]')  # 0x8943a25d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance2))

        data.write(b'B\x1fq\xf8')  # 0x421f71f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance3))

        data.write(b'_\x1aA@')  # 0x5f1a4140
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance4))

        data.write(b'\x94F\x92\xe5')  # 0x944692e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance5))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            distance0=data['distance0'],
            distance1=data['distance1'],
            distance2=data['distance2'],
            distance3=data['distance3'],
            distance4=data['distance4'],
            distance5=data['distance5'],
        )

    def to_json(self) -> dict:
        return {
            'distance0': self.distance0,
            'distance1': self.distance1,
            'distance2': self.distance2,
            'distance3': self.distance3,
            'distance4': self.distance4,
            'distance5': self.distance5,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xc48b0356, 0xfd7d0f3, 0x8943a25d, 0x421f71f8, 0x5f1a4140, 0x944692e5)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct207]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(60))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct207(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_distance0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_distance5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc48b0356: ('distance0', _decode_distance0),
    0xfd7d0f3: ('distance1', _decode_distance1),
    0x8943a25d: ('distance2', _decode_distance2),
    0x421f71f8: ('distance3', _decode_distance3),
    0x5f1a4140: ('distance4', _decode_distance4),
    0x944692e5: ('distance5', _decode_distance5),
}
