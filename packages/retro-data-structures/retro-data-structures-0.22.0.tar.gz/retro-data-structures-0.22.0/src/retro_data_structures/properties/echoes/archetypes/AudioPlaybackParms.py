# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class AudioPlaybackParms(BaseProperty):
    maximum_distance: float = dataclasses.field(default=100.0)
    fall_off: float = dataclasses.field(default=0.10000000149011612)
    sound_id: int = dataclasses.field(default=0, metadata={'sound': True})
    max_volume: int = dataclasses.field(default=127)
    min_volume: int = dataclasses.field(default=0)
    use_room_acoustics: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'\x0eD\x9fr')  # 0xe449f72
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_distance))

        data.write(b'rS\x18g')  # 0x72531867
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fall_off))

        data.write(b'\xaf\x85\xa3t')  # 0xaf85a374
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_id))

        data.write(b'\xc7\x12\x84|')  # 0xc712847c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.max_volume))

        data.write(b'Wa\x94\x96')  # 0x57619496
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.min_volume))

        data.write(b'\x85psT')  # 0x85707354
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_room_acoustics))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            maximum_distance=data['maximum_distance'],
            fall_off=data['fall_off'],
            sound_id=data['sound_id'],
            max_volume=data['max_volume'],
            min_volume=data['min_volume'],
            use_room_acoustics=data['use_room_acoustics'],
        )

    def to_json(self) -> dict:
        return {
            'maximum_distance': self.maximum_distance,
            'fall_off': self.fall_off,
            'sound_id': self.sound_id,
            'max_volume': self.max_volume,
            'min_volume': self.min_volume,
            'use_room_acoustics': self.use_room_acoustics,
        }

    def _dependencies_for_sound_id(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_id)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_sound_id, "sound_id", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for AudioPlaybackParms.{field_name} ({field_type}): {e}"
                )


_FAST_FORMAT = None
_FAST_IDS = (0xe449f72, 0x72531867, 0xaf85a374, 0xc712847c, 0x57619496, 0x85707354)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[AudioPlaybackParms]:
    if property_count != 6:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHfLHfLHlLHlLHlLH?')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(57))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) != _FAST_IDS:
        data.seek(before)
        return None

    return AudioPlaybackParms(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
    )


def _decode_maximum_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fall_off(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_id(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_min_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_use_room_acoustics(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe449f72: ('maximum_distance', _decode_maximum_distance),
    0x72531867: ('fall_off', _decode_fall_off),
    0xaf85a374: ('sound_id', _decode_sound_id),
    0xc712847c: ('max_volume', _decode_max_volume),
    0x57619496: ('min_volume', _decode_min_volume),
    0x85707354: ('use_room_acoustics', _decode_use_room_acoustics),
}
