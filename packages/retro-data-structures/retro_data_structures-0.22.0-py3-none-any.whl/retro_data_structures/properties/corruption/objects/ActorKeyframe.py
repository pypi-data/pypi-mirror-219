# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class ActorKeyframe(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    animation_index: int = dataclasses.field(default=0)
    unknown_0xc215a24f: int = dataclasses.field(default=0)
    loop: bool = dataclasses.field(default=False)
    loop_duration: float = dataclasses.field(default=0.0)
    unknown_0x6d62ef74: int = dataclasses.field(default=0)
    playback_rate: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ACKF'

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
        data.write(b'\x00\x06')  # 6 properties
        num_properties_written = 6

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        if self.animation_index != default_override.get('animation_index', 0):
            num_properties_written += 1
            data.write(b'\x1c\xcd\x05\x86')  # 0x1ccd0586
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>l', self.animation_index))

        data.write(b'\xc2\x15\xa2O')  # 0xc215a24f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc215a24f))

        data.write(b'\xed\xa4\x7f\xf6')  # 0xeda47ff6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.loop))

        data.write(b'\xce\xe6\x87#')  # 0xcee68723
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.loop_duration))

        data.write(b'mb\xeft')  # 0x6d62ef74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6d62ef74))

        data.write(b'o\x8d4\xca')  # 0x6f8d34ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.playback_rate))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.write(struct.pack(">H", num_properties_written))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            animation_index=data['animation_index'],
            unknown_0xc215a24f=data['unknown_0xc215a24f'],
            loop=data['loop'],
            loop_duration=data['loop_duration'],
            unknown_0x6d62ef74=data['unknown_0x6d62ef74'],
            playback_rate=data['playback_rate'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'animation_index': self.animation_index,
            'unknown_0xc215a24f': self.unknown_0xc215a24f,
            'loop': self.loop,
            'loop_duration': self.loop_duration,
            'unknown_0x6d62ef74': self.unknown_0x6d62ef74,
            'playback_rate': self.playback_rate,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_animation_index(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc215a24f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6d62ef74(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_playback_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x1ccd0586: ('animation_index', _decode_animation_index),
    0xc215a24f: ('unknown_0xc215a24f', _decode_unknown_0xc215a24f),
    0xeda47ff6: ('loop', _decode_loop),
    0xcee68723: ('loop_duration', _decode_loop_duration),
    0x6d62ef74: ('unknown_0x6d62ef74', _decode_unknown_0x6d62ef74),
    0x6f8d34ca: ('playback_rate', _decode_playback_rate),
}
