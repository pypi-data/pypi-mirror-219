# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct242(BaseProperty):
    song_file: AssetId = dataclasses.field(metadata={'asset_types': ['STRM']}, default=default_asset_id)
    dvd_file: str = dataclasses.field(default='')
    start_faded_out: bool = dataclasses.field(default=False)
    fade_in_time: float = dataclasses.field(default=0.05000000074505806)
    fade_out_time: float = dataclasses.field(default=0.25)
    volume: float = dataclasses.field(default=-6.0)
    pan: float = dataclasses.field(default=0.0)
    positional: bool = dataclasses.field(default=False)
    min_audible_distance: float = dataclasses.field(default=2.0)
    max_audible_distance: float = dataclasses.field(default=75.0)
    fall_off: float = dataclasses.field(default=0.0)
    use_room_acoustics: bool = dataclasses.field(default=True)
    start_sample: int = dataclasses.field(default=0)
    is_default_retronome_music: bool = dataclasses.field(default=False)
    sound_group_names: str = dataclasses.field(default='')

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\x9d\x1ag\xa8')  # 0x9d1a67a8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.song_file))

        data.write(b'\xb4\x17\x06J')  # 0xb417064a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.dvd_file.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeb%\n\x0b')  # 0xeb250a0b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_faded_out))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'\xc7\xa7\xf1\x89')  # 0xc7a7f189
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume))

        data.write(b'\xdfCS\xa3')  # 0xdf4353a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pan))

        data.write(b'n\x0e\x81\xf8')  # 0x6e0e81f8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.positional))

        data.write(b'%\xd4y\x8a')  # 0x25d4798a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_audible_distance))

        data.write(b'!NH\xa0')  # 0x214e48a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_audible_distance))

        data.write(b'rS\x18g')  # 0x72531867
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fall_off))

        data.write(b'\x85psT')  # 0x85707354
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_room_acoustics))

        data.write(b'\xe8\x8f\xf3w')  # 0xe88ff377
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.start_sample))

        data.write(b'\x07\x94\xc3\xeb')  # 0x794c3eb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_default_retronome_music))

        data.write(b'\xc8q\xbd\x1b')  # 0xc871bd1b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.sound_group_names.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            song_file=data['song_file'],
            dvd_file=data['dvd_file'],
            start_faded_out=data['start_faded_out'],
            fade_in_time=data['fade_in_time'],
            fade_out_time=data['fade_out_time'],
            volume=data['volume'],
            pan=data['pan'],
            positional=data['positional'],
            min_audible_distance=data['min_audible_distance'],
            max_audible_distance=data['max_audible_distance'],
            fall_off=data['fall_off'],
            use_room_acoustics=data['use_room_acoustics'],
            start_sample=data['start_sample'],
            is_default_retronome_music=data['is_default_retronome_music'],
            sound_group_names=data['sound_group_names'],
        )

    def to_json(self) -> dict:
        return {
            'song_file': self.song_file,
            'dvd_file': self.dvd_file,
            'start_faded_out': self.start_faded_out,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'volume': self.volume,
            'pan': self.pan,
            'positional': self.positional,
            'min_audible_distance': self.min_audible_distance,
            'max_audible_distance': self.max_audible_distance,
            'fall_off': self.fall_off,
            'use_room_acoustics': self.use_room_acoustics,
            'start_sample': self.start_sample,
            'is_default_retronome_music': self.is_default_retronome_music,
            'sound_group_names': self.sound_group_names,
        }


def _decode_song_file(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dvd_file(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_start_faded_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pan(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_positional(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_min_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fall_off(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_room_acoustics(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_sample(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_is_default_retronome_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_sound_group_names(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9d1a67a8: ('song_file', _decode_song_file),
    0xb417064a: ('dvd_file', _decode_dvd_file),
    0xeb250a0b: ('start_faded_out', _decode_start_faded_out),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0xc7a7f189: ('volume', _decode_volume),
    0xdf4353a3: ('pan', _decode_pan),
    0x6e0e81f8: ('positional', _decode_positional),
    0x25d4798a: ('min_audible_distance', _decode_min_audible_distance),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x72531867: ('fall_off', _decode_fall_off),
    0x85707354: ('use_room_acoustics', _decode_use_room_acoustics),
    0xe88ff377: ('start_sample', _decode_start_sample),
    0x794c3eb: ('is_default_retronome_music', _decode_is_default_retronome_music),
    0xc871bd1b: ('sound_group_names', _decode_sound_group_names),
}
