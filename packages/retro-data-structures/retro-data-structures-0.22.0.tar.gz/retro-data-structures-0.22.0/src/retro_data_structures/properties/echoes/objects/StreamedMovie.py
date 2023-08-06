# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class StreamedMovie(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    movie_file: str = dataclasses.field(default='')
    loop: bool = dataclasses.field(default=False)
    video_filter_enabled: bool = dataclasses.field(default=True)
    unknown: int = dataclasses.field(default=0)
    volume: int = dataclasses.field(default=127)
    volume_type: int = dataclasses.field(default=0)
    cache_length: float = dataclasses.field(default=0.05000000074505806)
    fade_out_time: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'MOVI'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['ScriptStreamedMovie.rel']

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X+\x84\xa8')  # 0x582b84a8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.movie_file.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xa4\x7f\xf6')  # 0xeda47ff6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop))

        data.write(b'6\x96;\xcc')  # 0x36963bcc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.video_filter_enabled))

        data.write(b'\xa7\x8a\xc0\xc0')  # 0xa78ac0c0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'\x80\xc6l7')  # 0x80c66c37
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.volume))

        data.write(b'\xe1\xffO\x04')  # 0xe1ff4f04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.volume_type))

        data.write(b'\xad\x9e\xb7\x7f')  # 0xad9eb77f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cache_length))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            movie_file=data['movie_file'],
            loop=data['loop'],
            video_filter_enabled=data['video_filter_enabled'],
            unknown=data['unknown'],
            volume=data['volume'],
            volume_type=data['volume_type'],
            cache_length=data['cache_length'],
            fade_out_time=data['fade_out_time'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'movie_file': self.movie_file,
            'loop': self.loop,
            'video_filter_enabled': self.video_filter_enabled,
            'unknown': self.unknown,
            'volume': self.volume,
            'volume_type': self.volume_type,
            'cache_length': self.cache_length,
            'fade_out_time': self.fade_out_time,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for StreamedMovie.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_movie_file(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_video_filter_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_volume_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cache_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x582b84a8: ('movie_file', _decode_movie_file),
    0xeda47ff6: ('loop', _decode_loop),
    0x36963bcc: ('video_filter_enabled', _decode_video_filter_enabled),
    0xa78ac0c0: ('unknown', _decode_unknown),
    0x80c66c37: ('volume', _decode_volume),
    0xe1ff4f04: ('volume_type', _decode_volume_type),
    0xad9eb77f: ('cache_length', _decode_cache_length),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
}
