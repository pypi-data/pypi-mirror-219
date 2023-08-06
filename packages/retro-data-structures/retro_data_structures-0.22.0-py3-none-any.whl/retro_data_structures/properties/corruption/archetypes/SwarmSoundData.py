# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SwarmSoundData(BaseProperty):
    sound_asset: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    max_count: int = dataclasses.field(default=5)
    min_delay: float = dataclasses.field(default=2.0)
    max_delay: float = dataclasses.field(default=4.0)

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xfc\rX\x9e')  # 0xfc0d589e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_asset))

        data.write(b'T\xb6\x8cL')  # 0x54b68c4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_count))

        data.write(b'\xb5\xf9\xc7\x1a')  # 0xb5f9c71a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_delay))

        data.write(b'\xf5\xb6\xbfl')  # 0xf5b6bf6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_delay))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            sound_asset=data['sound_asset'],
            max_count=data['max_count'],
            min_delay=data['min_delay'],
            max_delay=data['max_delay'],
        )

    def to_json(self) -> dict:
        return {
            'sound_asset': self.sound_asset,
            'max_count': self.max_count,
            'min_delay': self.min_delay,
            'max_delay': self.max_delay,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xfc0d589e, 0x54b68c4c, 0xb5f9c71a, 0xf5b6bf6c)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[SwarmSoundData]:
    if property_count != 4:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHlLHfLHf')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(44))
    if (dec[0], dec[3], dec[6], dec[9]) != _FAST_IDS:
        data.seek(before)
        return None

    return SwarmSoundData(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
    )


def _decode_sound_asset(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_max_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_min_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfc0d589e: ('sound_asset', _decode_sound_asset),
    0x54b68c4c: ('max_count', _decode_max_count),
    0xb5f9c71a: ('min_delay', _decode_min_delay),
    0xf5b6bf6c: ('max_delay', _decode_max_delay),
}
