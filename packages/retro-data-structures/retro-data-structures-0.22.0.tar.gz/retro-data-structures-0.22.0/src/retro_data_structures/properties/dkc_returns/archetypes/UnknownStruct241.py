# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums


@dataclasses.dataclass()
class UnknownStruct241(BaseProperty):
    part_of_music_system: bool = dataclasses.field(default=False)
    auto_buffer: bool = dataclasses.field(default=False)
    auto_buffer_when_stopped: bool = dataclasses.field(default=False)
    auto_play_when_buffered: bool = dataclasses.field(default=False)
    fade_in_time: float = dataclasses.field(default=0.05000000074505806)
    fade_out_time: float = dataclasses.field(default=0.25)
    volume: float = dataclasses.field(default=-6.0)
    save_preload_data: bool = dataclasses.field(default=False)
    start_delay: float = dataclasses.field(default=0.0)
    music_system_area_state: enums.MusicEnumB = dataclasses.field(default=enums.MusicEnumB.Unknown1)
    volume_type: enums.MusicEnumA = dataclasses.field(default=enums.MusicEnumA.Unknown2)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'.|t_')  # 0x2e7c745f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.part_of_music_system))

        data.write(b'\xc0>\xc2q')  # 0xc03ec271
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_buffer))

        data.write(b'\x0ehu\x18')  # 0xe687518
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_buffer_when_stopped))

        data.write(b'\xea\x8dT\xf4')  # 0xea8d54f4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_play_when_buffered))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        data.write(b'\xc7\xa7\xf1\x89')  # 0xc7a7f189
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume))

        data.write(b'\xd7BE\xa4')  # 0xd74245a4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.save_preload_data))

        data.write(b'\x19n\x17\xd9')  # 0x196e17d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_delay))

        data.write(b'\xfb\x8f\x0b\x1f')  # 0xfb8f0b1f
        data.write(b'\x00\x04')  # size
        self.music_system_area_state.to_stream(data)

        data.write(b'\x95Xq\x1e')  # 0x9558711e
        data.write(b'\x00\x04')  # size
        self.volume_type.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            part_of_music_system=data['part_of_music_system'],
            auto_buffer=data['auto_buffer'],
            auto_buffer_when_stopped=data['auto_buffer_when_stopped'],
            auto_play_when_buffered=data['auto_play_when_buffered'],
            fade_in_time=data['fade_in_time'],
            fade_out_time=data['fade_out_time'],
            volume=data['volume'],
            save_preload_data=data['save_preload_data'],
            start_delay=data['start_delay'],
            music_system_area_state=enums.MusicEnumB.from_json(data['music_system_area_state']),
            volume_type=enums.MusicEnumA.from_json(data['volume_type']),
        )

    def to_json(self) -> dict:
        return {
            'part_of_music_system': self.part_of_music_system,
            'auto_buffer': self.auto_buffer,
            'auto_buffer_when_stopped': self.auto_buffer_when_stopped,
            'auto_play_when_buffered': self.auto_play_when_buffered,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'volume': self.volume,
            'save_preload_data': self.save_preload_data,
            'start_delay': self.start_delay,
            'music_system_area_state': self.music_system_area_state.to_json(),
            'volume_type': self.volume_type.to_json(),
        }


_FAST_FORMAT = None
_FAST_IDS = (0x2e7c745f, 0xc03ec271, 0xe687518, 0xea8d54f4, 0x90aa341f, 0x7c269ebc, 0xc7a7f189, 0xd74245a4, 0x196e17d9, 0xfb8f0b1f, 0x9558711e)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct241]:
    if property_count != 11:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LHfLHfLHfLH?LHfLHLLHL')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(95))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct241(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        enums.MusicEnumB(dec[29]),
        enums.MusicEnumA(dec[32]),
    )


def _decode_part_of_music_system(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_buffer_when_stopped(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_play_when_buffered(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_save_preload_data(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_start_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_music_system_area_state(data: typing.BinaryIO, property_size: int):
    return enums.MusicEnumB.from_stream(data)


def _decode_volume_type(data: typing.BinaryIO, property_size: int):
    return enums.MusicEnumA.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2e7c745f: ('part_of_music_system', _decode_part_of_music_system),
    0xc03ec271: ('auto_buffer', _decode_auto_buffer),
    0xe687518: ('auto_buffer_when_stopped', _decode_auto_buffer_when_stopped),
    0xea8d54f4: ('auto_play_when_buffered', _decode_auto_play_when_buffered),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0xc7a7f189: ('volume', _decode_volume),
    0xd74245a4: ('save_preload_data', _decode_save_preload_data),
    0x196e17d9: ('start_delay', _decode_start_delay),
    0xfb8f0b1f: ('music_system_area_state', _decode_music_system_area_state),
    0x9558711e: ('volume_type', _decode_volume_type),
}
