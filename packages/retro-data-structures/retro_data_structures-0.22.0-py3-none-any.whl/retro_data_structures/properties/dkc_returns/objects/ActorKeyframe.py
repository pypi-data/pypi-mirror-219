# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class ActorKeyframe(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_0xc215a24f: int = dataclasses.field(default=0)
    mirrored: bool = dataclasses.field(default=False)
    force_secondary: bool = dataclasses.field(default=False)
    loop: bool = dataclasses.field(default=False)
    loop_duration: float = dataclasses.field(default=0.0)
    unknown_0x6d62ef74: int = dataclasses.field(default=8)
    playback_rate: float = dataclasses.field(default=1.0)
    playback_blend_mode: enums.AnimEnum = dataclasses.field(default=enums.AnimEnum.Unknown1)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2\x15\xa2O')  # 0xc215a24f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc215a24f))

        data.write(b'\x1f\xe4L:')  # 0x1fe44c3a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.mirrored))

        data.write(b'\\\xce[\x97')  # 0x5cce5b97
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.force_secondary))

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

        data.write(b'\xed\x1f\x8a\xab')  # 0xed1f8aab
        data.write(b'\x00\x04')  # size
        self.playback_blend_mode.to_stream(data)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown_0xc215a24f=data['unknown_0xc215a24f'],
            mirrored=data['mirrored'],
            force_secondary=data['force_secondary'],
            loop=data['loop'],
            loop_duration=data['loop_duration'],
            unknown_0x6d62ef74=data['unknown_0x6d62ef74'],
            playback_rate=data['playback_rate'],
            playback_blend_mode=enums.AnimEnum.from_json(data['playback_blend_mode']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_0xc215a24f': self.unknown_0xc215a24f,
            'mirrored': self.mirrored,
            'force_secondary': self.force_secondary,
            'loop': self.loop,
            'loop_duration': self.loop_duration,
            'unknown_0x6d62ef74': self.unknown_0x6d62ef74,
            'playback_rate': self.playback_rate,
            'playback_blend_mode': self.playback_blend_mode.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_0xc215a24f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mirrored(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_force_secondary(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_loop_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6d62ef74(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_playback_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_playback_blend_mode(data: typing.BinaryIO, property_size: int):
    return enums.AnimEnum.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc215a24f: ('unknown_0xc215a24f', _decode_unknown_0xc215a24f),
    0x1fe44c3a: ('mirrored', _decode_mirrored),
    0x5cce5b97: ('force_secondary', _decode_force_secondary),
    0xeda47ff6: ('loop', _decode_loop),
    0xcee68723: ('loop_duration', _decode_loop_duration),
    0x6d62ef74: ('unknown_0x6d62ef74', _decode_unknown_0x6d62ef74),
    0x6f8d34ca: ('playback_rate', _decode_playback_rate),
    0xed1f8aab: ('playback_blend_mode', _decode_playback_blend_mode),
}
