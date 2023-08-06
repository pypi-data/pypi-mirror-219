# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.SplineType import SplineType
from retro_data_structures.properties.echoes.core.Spline import Spline
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class SurfaceCamera(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flags_surface_camera: int = dataclasses.field(default=2)
    surface_type: int = dataclasses.field(default=1)
    spline: Spline = dataclasses.field(default_factory=Spline)
    player_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    unknown_0x431769c6: bool = dataclasses.field(default=False)
    target_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    unknown_0x33b4f106: bool = dataclasses.field(default=False)
    target_control_spline: Spline = dataclasses.field(default_factory=Spline)
    fov_spline: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SURC'

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1f\xfce\xd8')  # 0x1ffc65d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_surface_camera))

        data.write(b'\x14\x05\xb5\xe4')  # 0x1405b5e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.surface_type))

        data.write(b'\x92-\x15\x1f')  # 0x922d151f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1d\x8b\x93?')  # 0x1d8b933f
        data.write(b'\x00\x0c')  # size
        self.player_offset.to_stream(data)

        data.write(b'3\xe4h[')  # 0x33e4685b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spline_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\x17i\xc6')  # 0x431769c6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x431769c6))

        data.write(b'V\x04\xd3\x04')  # 0x5604d304
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.target_spline_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\xb4\xf1\x06')  # 0x33b4f106
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x33b4f106))

        data.write(b'\xc4\xdf\xbf\xa7')  # 0xc4dfbfa7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.target_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'hh\xd4\xb3')  # 0x6868d4b3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fov_spline.to_stream(data)
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
            flags_surface_camera=data['flags_surface_camera'],
            surface_type=data['surface_type'],
            spline=Spline.from_json(data['spline']),
            player_offset=Vector.from_json(data['player_offset']),
            spline_type=SplineType.from_json(data['spline_type']),
            unknown_0x431769c6=data['unknown_0x431769c6'],
            target_spline_type=SplineType.from_json(data['target_spline_type']),
            unknown_0x33b4f106=data['unknown_0x33b4f106'],
            target_control_spline=Spline.from_json(data['target_control_spline']),
            fov_spline=Spline.from_json(data['fov_spline']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flags_surface_camera': self.flags_surface_camera,
            'surface_type': self.surface_type,
            'spline': self.spline.to_json(),
            'player_offset': self.player_offset.to_json(),
            'spline_type': self.spline_type.to_json(),
            'unknown_0x431769c6': self.unknown_0x431769c6,
            'target_spline_type': self.target_spline_type.to_json(),
            'unknown_0x33b4f106': self.unknown_0x33b4f106,
            'target_control_spline': self.target_control_spline.to_json(),
            'fov_spline': self.fov_spline.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_spline_type(self, asset_manager):
        yield from self.spline_type.dependencies_for(asset_manager)

    def _dependencies_for_target_spline_type(self, asset_manager):
        yield from self.target_spline_type.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_spline_type, "spline_type", "SplineType"),
            (self._dependencies_for_target_spline_type, "target_spline_type", "SplineType"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SurfaceCamera.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flags_surface_camera(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_surface_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_player_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_unknown_0x431769c6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_target_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_unknown_0x33b4f106(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_target_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_fov_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x1ffc65d8: ('flags_surface_camera', _decode_flags_surface_camera),
    0x1405b5e4: ('surface_type', _decode_surface_type),
    0x922d151f: ('spline', _decode_spline),
    0x1d8b933f: ('player_offset', _decode_player_offset),
    0x33e4685b: ('spline_type', _decode_spline_type),
    0x431769c6: ('unknown_0x431769c6', _decode_unknown_0x431769c6),
    0x5604d304: ('target_spline_type', _decode_target_spline_type),
    0x33b4f106: ('unknown_0x33b4f106', _decode_unknown_0x33b4f106),
    0xc4dfbfa7: ('target_control_spline', _decode_target_control_spline),
    0x6868d4b3: ('fov_spline', _decode_fov_spline),
}
