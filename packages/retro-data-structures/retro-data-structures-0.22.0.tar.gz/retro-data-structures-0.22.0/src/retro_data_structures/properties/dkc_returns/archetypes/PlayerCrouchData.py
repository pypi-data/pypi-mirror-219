# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerCrouchData(BaseProperty):
    push_down_threshold: float = dataclasses.field(default=0.800000011920929)
    angle_threshold: float = dataclasses.field(default=30.0)
    deceleration: float = dataclasses.field(default=9.0)
    backflip_spin_jump_height: float = dataclasses.field(default=6.5)
    blow_message_interval: float = dataclasses.field(default=0.25)
    blow_forward_range: float = dataclasses.field(default=3.0)
    blow_vertical_range: float = dataclasses.field(default=1.125)
    min_blow_time: float = dataclasses.field(default=0.20000000298023224)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'\xba\x08\x9b\xb4')  # 0xba089bb4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.push_down_threshold))

        data.write(b']\t\x0b\x9a')  # 0x5d090b9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.angle_threshold))

        data.write(b'\x9e\xc4\xfc\x10')  # 0x9ec4fc10
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deceleration))

        data.write(b'\xc6A\xa9k')  # 0xc641a96b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.backflip_spin_jump_height))

        data.write(b'\x94!\xe3F')  # 0x9421e346
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.blow_message_interval))

        data.write(b'\xef6\xae2')  # 0xef36ae32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.blow_forward_range))

        data.write(b'\x1d\xc2\xbfG')  # 0x1dc2bf47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.blow_vertical_range))

        data.write(b'=\x8f\xc0\xf4')  # 0x3d8fc0f4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_blow_time))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            push_down_threshold=data['push_down_threshold'],
            angle_threshold=data['angle_threshold'],
            deceleration=data['deceleration'],
            backflip_spin_jump_height=data['backflip_spin_jump_height'],
            blow_message_interval=data['blow_message_interval'],
            blow_forward_range=data['blow_forward_range'],
            blow_vertical_range=data['blow_vertical_range'],
            min_blow_time=data['min_blow_time'],
        )

    def to_json(self) -> dict:
        return {
            'push_down_threshold': self.push_down_threshold,
            'angle_threshold': self.angle_threshold,
            'deceleration': self.deceleration,
            'backflip_spin_jump_height': self.backflip_spin_jump_height,
            'blow_message_interval': self.blow_message_interval,
            'blow_forward_range': self.blow_forward_range,
            'blow_vertical_range': self.blow_vertical_range,
            'min_blow_time': self.min_blow_time,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xba089bb4, 0x5d090b9a, 0x9ec4fc10, 0xc641a96b, 0x9421e346, 0xef36ae32, 0x1dc2bf47, 0x3d8fc0f4)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[PlayerCrouchData]:
    if property_count != 8:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(80))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21]) != _FAST_IDS:
        data.seek(before)
        return None

    return PlayerCrouchData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
    )


def _decode_push_down_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_angle_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_backflip_spin_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_blow_message_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_blow_forward_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_blow_vertical_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_blow_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xba089bb4: ('push_down_threshold', _decode_push_down_threshold),
    0x5d090b9a: ('angle_threshold', _decode_angle_threshold),
    0x9ec4fc10: ('deceleration', _decode_deceleration),
    0xc641a96b: ('backflip_spin_jump_height', _decode_backflip_spin_jump_height),
    0x9421e346: ('blow_message_interval', _decode_blow_message_interval),
    0xef36ae32: ('blow_forward_range', _decode_blow_forward_range),
    0x1dc2bf47: ('blow_vertical_range', _decode_blow_vertical_range),
    0x3d8fc0f4: ('min_blow_time', _decode_min_blow_time),
}
