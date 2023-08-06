# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class UnknownStruct249(BaseProperty):
    music_fade: bool = dataclasses.field(default=True)
    music_fade_out_time: float = dataclasses.field(default=0.5)
    play_jingle: bool = dataclasses.field(default=True)
    camera_fade: bool = dataclasses.field(default=True)
    camera_fade_out_delay_time: float = dataclasses.field(default=1.0)
    camera_fade_out_time: float = dataclasses.field(default=1.5)
    interface_delay_time: float = dataclasses.field(default=0.5)
    volume_fade_out_time: float = dataclasses.field(default=0.75)
    unknown: str = dataclasses.field(default='')

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xed^\xc8\xa1')  # 0xed5ec8a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.music_fade))

        data.write(b'\x8d\xce\xa3O')  # 0x8dcea34f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.music_fade_out_time))

        data.write(b'\x03\x97\xdc\xf7')  # 0x397dcf7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.play_jingle))

        data.write(b'\x9ab\x10\xd3')  # 0x9a6210d3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.camera_fade))

        data.write(b'tf\xf0H')  # 0x7466f048
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_fade_out_delay_time))

        data.write(b'\xc3\xdd\x83\x89')  # 0xc3dd8389
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.camera_fade_out_time))

        data.write(b'tj\x13\xe9')  # 0x746a13e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.interface_delay_time))

        data.write(b'/\x9d\xedK')  # 0x2f9ded4b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.volume_fade_out_time))

        data.write(b'+\xd2\xae2')  # 0x2bd2ae32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.unknown.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            music_fade=data['music_fade'],
            music_fade_out_time=data['music_fade_out_time'],
            play_jingle=data['play_jingle'],
            camera_fade=data['camera_fade'],
            camera_fade_out_delay_time=data['camera_fade_out_delay_time'],
            camera_fade_out_time=data['camera_fade_out_time'],
            interface_delay_time=data['interface_delay_time'],
            volume_fade_out_time=data['volume_fade_out_time'],
            unknown=data['unknown'],
        )

    def to_json(self) -> dict:
        return {
            'music_fade': self.music_fade,
            'music_fade_out_time': self.music_fade_out_time,
            'play_jingle': self.play_jingle,
            'camera_fade': self.camera_fade,
            'camera_fade_out_delay_time': self.camera_fade_out_delay_time,
            'camera_fade_out_time': self.camera_fade_out_time,
            'interface_delay_time': self.interface_delay_time,
            'volume_fade_out_time': self.volume_fade_out_time,
            'unknown': self.unknown,
        }


def _decode_music_fade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_music_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_play_jingle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_camera_fade(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_camera_fade_out_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_interface_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xed5ec8a1: ('music_fade', _decode_music_fade),
    0x8dcea34f: ('music_fade_out_time', _decode_music_fade_out_time),
    0x397dcf7: ('play_jingle', _decode_play_jingle),
    0x9a6210d3: ('camera_fade', _decode_camera_fade),
    0x7466f048: ('camera_fade_out_delay_time', _decode_camera_fade_out_delay_time),
    0xc3dd8389: ('camera_fade_out_time', _decode_camera_fade_out_time),
    0x746a13e9: ('interface_delay_time', _decode_interface_delay_time),
    0x2f9ded4b: ('volume_fade_out_time', _decode_volume_fade_out_time),
    0x2bd2ae32: ('unknown', _decode_unknown),
}
