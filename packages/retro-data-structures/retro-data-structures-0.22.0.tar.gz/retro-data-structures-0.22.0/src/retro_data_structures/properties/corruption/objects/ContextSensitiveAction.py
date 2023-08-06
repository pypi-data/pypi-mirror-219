# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class ContextSensitiveAction(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    animation: int = dataclasses.field(default=0)
    rotation_blend_mode: enums.RotationBlendMode = dataclasses.field(default=enums.RotationBlendMode.Unknown1)
    blend: Spline = dataclasses.field(default_factory=Spline)
    mode: enums.Mode = dataclasses.field(default=enums.Mode.Unknown1)
    controller_type: enums.ControllerType = dataclasses.field(default=enums.ControllerType.Unknown1)
    unknown: float = dataclasses.field(default=1.0)
    hide_aiming_cursor: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CSAC'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_ScriptContextSensitiveAction.rso']

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

        data.write(b'\xaa\xcd\xb1\x1c')  # 0xaacdb11c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation))

        data.write(b'\xb0h\xf4\x0b')  # 0xb068f40b
        data.write(b'\x00\x04')  # size
        self.rotation_blend_mode.to_stream(data)

        data.write(b'\xf9\xdf\xe0\x1d')  # 0xf9dfe01d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.blend.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8\xf6\x0f\x9a')  # 0xb8f60f9a
        data.write(b'\x00\x04')  # size
        self.mode.to_stream(data)

        data.write(b'\x89r\xa8o')  # 0x8972a86f
        data.write(b'\x00\x04')  # size
        self.controller_type.to_stream(data)

        data.write(b'\xbf\n\xdf@')  # 0xbf0adf40
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'\xca@\x16\xa1')  # 0xca4016a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.hide_aiming_cursor))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            animation=data['animation'],
            rotation_blend_mode=enums.RotationBlendMode.from_json(data['rotation_blend_mode']),
            blend=Spline.from_json(data['blend']),
            mode=enums.Mode.from_json(data['mode']),
            controller_type=enums.ControllerType.from_json(data['controller_type']),
            unknown=data['unknown'],
            hide_aiming_cursor=data['hide_aiming_cursor'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'animation': self.animation,
            'rotation_blend_mode': self.rotation_blend_mode.to_json(),
            'blend': self.blend.to_json(),
            'mode': self.mode.to_json(),
            'controller_type': self.controller_type.to_json(),
            'unknown': self.unknown,
            'hide_aiming_cursor': self.hide_aiming_cursor,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_rotation_blend_mode(data: typing.BinaryIO, property_size: int):
    return enums.RotationBlendMode.from_stream(data)


def _decode_blend(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return enums.Mode.from_stream(data)


def _decode_controller_type(data: typing.BinaryIO, property_size: int):
    return enums.ControllerType.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hide_aiming_cursor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xaacdb11c: ('animation', _decode_animation),
    0xb068f40b: ('rotation_blend_mode', _decode_rotation_blend_mode),
    0xf9dfe01d: ('blend', _decode_blend),
    0xb8f60f9a: ('mode', _decode_mode),
    0x8972a86f: ('controller_type', _decode_controller_type),
    0xbf0adf40: ('unknown', _decode_unknown),
    0xca4016a1: ('hide_aiming_cursor', _decode_hide_aiming_cursor),
}
