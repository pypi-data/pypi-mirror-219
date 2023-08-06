# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class FlyerSwarmData(BaseProperty):
    unknown_0x4a85a2da: float = dataclasses.field(default=1.0)
    unknown_0x10cccd3c: float = dataclasses.field(default=1.0)
    unknown_0x1e8e90a4: float = dataclasses.field(default=0.0)
    unknown_0x262e586d: float = dataclasses.field(default=0.0)
    roll_upright_speed: float = dataclasses.field(default=0.0)
    roll_upright_min_angle: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'J\x85\xa2\xda')  # 0x4a85a2da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4a85a2da))

        data.write(b'\x10\xcc\xcd<')  # 0x10cccd3c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x10cccd3c))

        data.write(b'\x1e\x8e\x90\xa4')  # 0x1e8e90a4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1e8e90a4))

        data.write(b'&.Xm')  # 0x262e586d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x262e586d))

        data.write(b"G\x9aW'")  # 0x479a5727
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.roll_upright_speed))

        data.write(b'\xd5r\xd1\xda')  # 0xd572d1da
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.roll_upright_min_angle))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x4a85a2da=data['unknown_0x4a85a2da'],
            unknown_0x10cccd3c=data['unknown_0x10cccd3c'],
            unknown_0x1e8e90a4=data['unknown_0x1e8e90a4'],
            unknown_0x262e586d=data['unknown_0x262e586d'],
            roll_upright_speed=data['roll_upright_speed'],
            roll_upright_min_angle=data['roll_upright_min_angle'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x4a85a2da': self.unknown_0x4a85a2da,
            'unknown_0x10cccd3c': self.unknown_0x10cccd3c,
            'unknown_0x1e8e90a4': self.unknown_0x1e8e90a4,
            'unknown_0x262e586d': self.unknown_0x262e586d,
            'roll_upright_speed': self.roll_upright_speed,
            'roll_upright_min_angle': self.roll_upright_min_angle,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x4a85a2da, 0x10cccd3c, 0x1e8e90a4, 0x262e586d, 0x479a5727, 0xd572d1da)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[FlyerSwarmData]:
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

    return FlyerSwarmData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_unknown_0x4a85a2da(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x10cccd3c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1e8e90a4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x262e586d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_upright_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_upright_min_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4a85a2da: ('unknown_0x4a85a2da', _decode_unknown_0x4a85a2da),
    0x10cccd3c: ('unknown_0x10cccd3c', _decode_unknown_0x10cccd3c),
    0x1e8e90a4: ('unknown_0x1e8e90a4', _decode_unknown_0x1e8e90a4),
    0x262e586d: ('unknown_0x262e586d', _decode_unknown_0x262e586d),
    0x479a5727: ('roll_upright_speed', _decode_roll_upright_speed),
    0xd572d1da: ('roll_upright_min_angle', _decode_roll_upright_min_angle),
}
