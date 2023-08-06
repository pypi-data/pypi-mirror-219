# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class FixedDelayRules(BaseProperty):
    number_of_fixed_delays: int = dataclasses.field(default=0)
    fixed_delay1: float = dataclasses.field(default=0.0)
    fixed_delay2: float = dataclasses.field(default=0.0)
    fixed_delay3: float = dataclasses.field(default=0.0)
    fixed_delay4: float = dataclasses.field(default=0.0)
    fixed_delay5: float = dataclasses.field(default=0.0)

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

        data.write(b'\x1f\x07\xfcI')  # 0x1f07fc49
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.number_of_fixed_delays))

        data.write(b'\xf5Au\xc5')  # 0xf54175c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_delay1))

        data.write(b's\xd5\x07k')  # 0x73d5076b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_delay2))

        data.write(b'\xb8\x89\xd4\xce')  # 0xb889d4ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_delay3))

        data.write(b'\xa5\x8c\xe4v')  # 0xa58ce476
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_delay4))

        data.write(b'n\xd07\xd3')  # 0x6ed037d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_delay5))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            number_of_fixed_delays=data['number_of_fixed_delays'],
            fixed_delay1=data['fixed_delay1'],
            fixed_delay2=data['fixed_delay2'],
            fixed_delay3=data['fixed_delay3'],
            fixed_delay4=data['fixed_delay4'],
            fixed_delay5=data['fixed_delay5'],
        )

    def to_json(self) -> dict:
        return {
            'number_of_fixed_delays': self.number_of_fixed_delays,
            'fixed_delay1': self.fixed_delay1,
            'fixed_delay2': self.fixed_delay2,
            'fixed_delay3': self.fixed_delay3,
            'fixed_delay4': self.fixed_delay4,
            'fixed_delay5': self.fixed_delay5,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x1f07fc49, 0xf54175c5, 0x73d5076b, 0xb889d4ce, 0xa58ce476, 0x6ed037d3)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[FixedDelayRules]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(60))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return FixedDelayRules(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_number_of_fixed_delays(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_fixed_delay1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fixed_delay2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fixed_delay3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fixed_delay4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fixed_delay5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1f07fc49: ('number_of_fixed_delays', _decode_number_of_fixed_delays),
    0xf54175c5: ('fixed_delay1', _decode_fixed_delay1),
    0x73d5076b: ('fixed_delay2', _decode_fixed_delay2),
    0xb889d4ce: ('fixed_delay3', _decode_fixed_delay3),
    0xa58ce476: ('fixed_delay4', _decode_fixed_delay4),
    0x6ed037d3: ('fixed_delay5', _decode_fixed_delay5),
}
