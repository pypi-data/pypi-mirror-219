# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class StreamedAudio(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    song_file: AssetId = dataclasses.field(metadata={'asset_types': ['STRM']}, default=default_asset_id)
    default_audio: bool = dataclasses.field(default=False)
    fade_in_time: float = dataclasses.field(default=0.25)
    fade_out_time: float = dataclasses.field(default=0.25)
    volume: float = dataclasses.field(default=1.0)
    pan: float = dataclasses.field(default=0.0)
    memory_stream: bool = dataclasses.field(default=False)
    positional: bool = dataclasses.field(default=False)
    min_audible_distance: float = dataclasses.field(default=2.0)
    max_audible_distance: float = dataclasses.field(default=25.0)
    fall_off: float = dataclasses.field(default=0.0)
    use_room_acoustics: bool = dataclasses.field(default=True)
    volume_type: enums.VolumeType = dataclasses.field(default=enums.VolumeType.Unknown3)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'STAU'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9d\x1ag\xa8')  # 0x9d1a67a8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.song_file))

        data.write(b'4\xb1R\xc4')  # 0x34b152c4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.default_audio))

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

        data.write(b'\x04+\xa4\xd5')  # 0x42ba4d5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.memory_stream))

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

        data.write(b'\x95Xq\x1e')  # 0x9558711e
        data.write(b'\x00\x04')  # size
        self.volume_type.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            song_file=data['song_file'],
            default_audio=data['default_audio'],
            fade_in_time=data['fade_in_time'],
            fade_out_time=data['fade_out_time'],
            volume=data['volume'],
            pan=data['pan'],
            memory_stream=data['memory_stream'],
            positional=data['positional'],
            min_audible_distance=data['min_audible_distance'],
            max_audible_distance=data['max_audible_distance'],
            fall_off=data['fall_off'],
            use_room_acoustics=data['use_room_acoustics'],
            volume_type=enums.VolumeType.from_json(data['volume_type']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'song_file': self.song_file,
            'default_audio': self.default_audio,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
            'volume': self.volume,
            'pan': self.pan,
            'memory_stream': self.memory_stream,
            'positional': self.positional,
            'min_audible_distance': self.min_audible_distance,
            'max_audible_distance': self.max_audible_distance,
            'fall_off': self.fall_off,
            'use_room_acoustics': self.use_room_acoustics,
            'volume_type': self.volume_type.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_song_file(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_default_audio(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pan(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_memory_stream(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


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


def _decode_volume_type(data: typing.BinaryIO, property_size: int):
    return enums.VolumeType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x9d1a67a8: ('song_file', _decode_song_file),
    0x34b152c4: ('default_audio', _decode_default_audio),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
    0xc7a7f189: ('volume', _decode_volume),
    0xdf4353a3: ('pan', _decode_pan),
    0x42ba4d5: ('memory_stream', _decode_memory_stream),
    0x6e0e81f8: ('positional', _decode_positional),
    0x25d4798a: ('min_audible_distance', _decode_min_audible_distance),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x72531867: ('fall_off', _decode_fall_off),
    0x85707354: ('use_room_acoustics', _decode_use_room_acoustics),
    0x9558711e: ('volume_type', _decode_volume_type),
}
