# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class SlideBehaviorData(BaseProperty):
    slope_detection_angle: float = dataclasses.field(default=20.0)
    slide_detection_angle: float = dataclasses.field(default=54.0)
    slide_friction: float = dataclasses.field(default=1.0)
    slow_friction: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'N}\xef~')  # 0x4e7def7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slope_detection_angle))

        data.write(b'e\x91\xa3\xa9')  # 0x6591a3a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_detection_angle))

        data.write(b'\xc2\x8b(^')  # 0xc28b285e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_friction))

        data.write(b'\xce\xd6\xfc\xcf')  # 0xced6fccf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slow_friction))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            slope_detection_angle=data['slope_detection_angle'],
            slide_detection_angle=data['slide_detection_angle'],
            slide_friction=data['slide_friction'],
            slow_friction=data['slow_friction'],
        )

    def to_json(self) -> dict:
        return {
            'slope_detection_angle': self.slope_detection_angle,
            'slide_detection_angle': self.slide_detection_angle,
            'slide_friction': self.slide_friction,
            'slow_friction': self.slow_friction,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x4e7def7e, 0x6591a3a9, 0xc28b285e, 0xced6fccf)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SlideBehaviorData]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(40))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return SlideBehaviorData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_slope_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_detection_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_friction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slow_friction(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4e7def7e: ('slope_detection_angle', _decode_slope_detection_angle),
    0x6591a3a9: ('slide_detection_angle', _decode_slide_detection_angle),
    0xc28b285e: ('slide_friction', _decode_slide_friction),
    0xced6fccf: ('slow_friction', _decode_slow_friction),
}
