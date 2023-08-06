# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class TrackObjectModuleData(BaseProperty):
    maximum_track_distance: float = dataclasses.field(default=15.0)
    full_left_distance: float = dataclasses.field(default=10.0)
    full_right_distance: float = dataclasses.field(default=5.0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x04\xf3\xde:')  # 0x4f3de3a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_track_distance))

        data.write(b'\x03m\xc8\xdd')  # 0x36dc8dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.full_left_distance))

        data.write(b'7\xa1#6')  # 0x37a12336
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.full_right_distance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            maximum_track_distance=data['maximum_track_distance'],
            full_left_distance=data['full_left_distance'],
            full_right_distance=data['full_right_distance'],
        )

    def to_json(self) -> dict:
        return {
            'maximum_track_distance': self.maximum_track_distance,
            'full_left_distance': self.full_left_distance,
            'full_right_distance': self.full_right_distance,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x4f3de3a, 0x36dc8dd, 0x37a12336)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[TrackObjectModuleData]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(30))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return TrackObjectModuleData(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_maximum_track_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_full_left_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_full_right_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4f3de3a: ('maximum_track_distance', _decode_maximum_track_distance),
    0x36dc8dd: ('full_left_distance', _decode_full_left_distance),
    0x37a12336: ('full_right_distance', _decode_full_right_distance),
}
