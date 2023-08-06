# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ScannableParameters(BaseProperty):
    scannable_info0: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    max_scannable_distance: float = dataclasses.field(default=0.0)
    priority: int = dataclasses.field(default=0)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xb9N\x9b\xe7')  # 0xb94e9be7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.scannable_info0))

        data.write(b'\xffJ\xe2\xec')  # 0xff4ae2ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_scannable_distance))

        data.write(b'B\x08vP')  # 0x42087650
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.priority))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scannable_info0=data['scannable_info0'],
            max_scannable_distance=data['max_scannable_distance'],
            priority=data['priority'],
        )

    def to_json(self) -> dict:
        return {
            'scannable_info0': self.scannable_info0,
            'max_scannable_distance': self.max_scannable_distance,
            'priority': self.priority,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xb94e9be7, 0xff4ae2ec, 0x42087650)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[ScannableParameters]:
    if property_count != 3:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHfLHl')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(34))
    if (dec[0], dec[3], dec[6]) != _FAST_IDS:
        data.seek(before)
        return None

    return ScannableParameters(
        dec[2],
        dec[5],
        dec[8],
    )


def _decode_scannable_info0(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_max_scannable_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb94e9be7: ('scannable_info0', _decode_scannable_info0),
    0xff4ae2ec: ('max_scannable_distance', _decode_max_scannable_distance),
    0x42087650: ('priority', _decode_priority),
}
