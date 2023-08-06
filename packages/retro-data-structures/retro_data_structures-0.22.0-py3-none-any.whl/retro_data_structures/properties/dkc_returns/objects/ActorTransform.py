# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.RotationSplines import RotationSplines
from retro_data_structures.properties.dkc_returns.archetypes.ScaleSplines import ScaleSplines
from retro_data_structures.properties.dkc_returns.archetypes.TranslationSplines import TranslationSplines
from retro_data_structures.properties.dkc_returns.core.Spline import Spline


@dataclasses.dataclass()
class ActorTransform(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flags_actor_transform: int = dataclasses.field(default=20)
    duration: float = dataclasses.field(default=10.0)
    initial_time: float = dataclasses.field(default=0.0)
    rotation_controls: RotationSplines = dataclasses.field(default_factory=RotationSplines)
    scale_controls: ScaleSplines = dataclasses.field(default_factory=ScaleSplines)
    translation_control: TranslationSplines = dataclasses.field(default_factory=TranslationSplines)
    path_position: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ATRN'

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xcev\x89')  # 0xc6ce7689
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_actor_transform))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'\xa5u=R')  # 0xa5753d52
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_time))

        data.write(b'\xef\xe4\xeaW')  # 0xefe4ea57
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rotation_controls.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/~\xc0\xa2')  # 0x2f7ec0a2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scale_controls.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i"g\xea')  # 0x692267ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.translation_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\xb8\xaa\xca')  # 0x51b8aaca
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.path_position.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            flags_actor_transform=data['flags_actor_transform'],
            duration=data['duration'],
            initial_time=data['initial_time'],
            rotation_controls=RotationSplines.from_json(data['rotation_controls']),
            scale_controls=ScaleSplines.from_json(data['scale_controls']),
            translation_control=TranslationSplines.from_json(data['translation_control']),
            path_position=Spline.from_json(data['path_position']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flags_actor_transform': self.flags_actor_transform,
            'duration': self.duration,
            'initial_time': self.initial_time,
            'rotation_controls': self.rotation_controls.to_json(),
            'scale_controls': self.scale_controls.to_json(),
            'translation_control': self.translation_control.to_json(),
            'path_position': self.path_position.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flags_actor_transform(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_controls(data: typing.BinaryIO, property_size: int):
    return RotationSplines.from_stream(data, property_size)


def _decode_scale_controls(data: typing.BinaryIO, property_size: int):
    return ScaleSplines.from_stream(data, property_size)


def _decode_translation_control(data: typing.BinaryIO, property_size: int):
    return TranslationSplines.from_stream(data, property_size)


def _decode_path_position(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc6ce7689: ('flags_actor_transform', _decode_flags_actor_transform),
    0x8b51e23f: ('duration', _decode_duration),
    0xa5753d52: ('initial_time', _decode_initial_time),
    0xefe4ea57: ('rotation_controls', _decode_rotation_controls),
    0x2f7ec0a2: ('scale_controls', _decode_scale_controls),
    0x692267ea: ('translation_control', _decode_translation_control),
    0x51b8aaca: ('path_position', _decode_path_position),
}
