# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class IdleBehaviorData(BaseProperty):
    idle_type: enums.IdleType = dataclasses.field(default=enums.IdleType.Unknown1)
    delay_before_first_idle: float = dataclasses.field(default=0.0)
    first_idle_time: float = dataclasses.field(default=0.0)
    delay_between_idles: float = dataclasses.field(default=0.0)
    idle_time: float = dataclasses.field(default=0.0)
    idle_at_start: bool = dataclasses.field(default=True)

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

        data.write(b'\xc9T\x9d+')  # 0xc9549d2b
        data.write(b'\x00\x04')  # size
        self.idle_type.to_stream(data)

        data.write(b'$\xf6\xd9V')  # 0x24f6d956
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_before_first_idle))

        data.write(b'\xa3\xeb\x83$')  # 0xa3eb8324
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.first_idle_time))

        data.write(b'\x89\xb0z\xf3')  # 0x89b07af3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_between_idles))

        data.write(b'\xd1\x02\x0f,')  # 0xd1020f2c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.idle_time))

        data.write(b'\xbdq\xad\x8b')  # 0xbd71ad8b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.idle_at_start))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            idle_type=enums.IdleType.from_json(data['idle_type']),
            delay_before_first_idle=data['delay_before_first_idle'],
            first_idle_time=data['first_idle_time'],
            delay_between_idles=data['delay_between_idles'],
            idle_time=data['idle_time'],
            idle_at_start=data['idle_at_start'],
        )

    def to_json(self) -> dict:
        return {
            'idle_type': self.idle_type.to_json(),
            'delay_before_first_idle': self.delay_before_first_idle,
            'first_idle_time': self.first_idle_time,
            'delay_between_idles': self.delay_between_idles,
            'idle_time': self.idle_time,
            'idle_at_start': self.idle_at_start,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xc9549d2b, 0x24f6d956, 0xa3eb8324, 0x89b07af3, 0xd1020f2c, 0xbd71ad8b)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[IdleBehaviorData]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHLLHfLHfLHfLHfLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(57))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return IdleBehaviorData(
        enums.IdleType(dec[2]),
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_idle_type(data: typing.BinaryIO, property_size: int):
    return enums.IdleType.from_stream(data)


def _decode_delay_before_first_idle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_first_idle_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_between_idles(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_idle_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_idle_at_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc9549d2b: ('idle_type', _decode_idle_type),
    0x24f6d956: ('delay_before_first_idle', _decode_delay_before_first_idle),
    0xa3eb8324: ('first_idle_time', _decode_first_idle_time),
    0x89b07af3: ('delay_between_idles', _decode_delay_between_idles),
    0xd1020f2c: ('idle_time', _decode_idle_time),
    0xbd71ad8b: ('idle_at_start', _decode_idle_at_start),
}
