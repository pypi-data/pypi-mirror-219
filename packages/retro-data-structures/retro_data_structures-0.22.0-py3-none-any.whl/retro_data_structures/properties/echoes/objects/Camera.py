# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.SplineType import SplineType
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class Camera(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    animation_time: float = dataclasses.field(default=10.0)
    unknown_0x05c5fc6e: int = dataclasses.field(default=168)  # Flagset
    unknown_0xd4b29446: int = dataclasses.field(default=0)
    motion_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    target_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    target_control_spline: Spline = dataclasses.field(default_factory=Spline)
    fov_spline: Spline = dataclasses.field(default_factory=Spline)
    roll_spline: Spline = dataclasses.field(default_factory=Spline)
    slowmo_control_spline: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CAMR'

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
        self.editor_properties.to_stream(data, default_override={'active': False})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*S$Z')  # 0x2a53245a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.animation_time))

        data.write(b'\x05\xc5\xfcn')  # 0x5c5fc6e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown_0x05c5fc6e))

        data.write(b'\xd4\xb2\x94F')  # 0xd4b29446
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd4b29446))

        data.write(b'I=j-')  # 0x493d6a2d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_spline_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V\x04\xd3\x04')  # 0x5604d304
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.target_spline_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"'\xe5\xf8t")  # 0x27e5f874
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

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

        data.write(b'nm\x8e\xfd')  # 0x6e6d8efd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.roll_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\xf4y\x8e')  # 0xf4f4798e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.slowmo_control_spline.to_stream(data)
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
            animation_time=data['animation_time'],
            unknown_0x05c5fc6e=data['unknown_0x05c5fc6e'],
            unknown_0xd4b29446=data['unknown_0xd4b29446'],
            motion_spline_type=SplineType.from_json(data['motion_spline_type']),
            target_spline_type=SplineType.from_json(data['target_spline_type']),
            motion_control_spline=Spline.from_json(data['motion_control_spline']),
            target_control_spline=Spline.from_json(data['target_control_spline']),
            fov_spline=Spline.from_json(data['fov_spline']),
            roll_spline=Spline.from_json(data['roll_spline']),
            slowmo_control_spline=Spline.from_json(data['slowmo_control_spline']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'animation_time': self.animation_time,
            'unknown_0x05c5fc6e': self.unknown_0x05c5fc6e,
            'unknown_0xd4b29446': self.unknown_0xd4b29446,
            'motion_spline_type': self.motion_spline_type.to_json(),
            'target_spline_type': self.target_spline_type.to_json(),
            'motion_control_spline': self.motion_control_spline.to_json(),
            'target_control_spline': self.target_control_spline.to_json(),
            'fov_spline': self.fov_spline.to_json(),
            'roll_spline': self.roll_spline.to_json(),
            'slowmo_control_spline': self.slowmo_control_spline.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_motion_spline_type(self, asset_manager):
        yield from self.motion_spline_type.dependencies_for(asset_manager)

    def _dependencies_for_target_spline_type(self, asset_manager):
        yield from self.target_spline_type.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_motion_spline_type, "motion_spline_type", "SplineType"),
            (self._dependencies_for_target_spline_type, "target_spline_type", "SplineType"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Camera.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size, default_override={'active': False})


def _decode_animation_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x05c5fc6e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0xd4b29446(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_motion_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_target_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_motion_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_target_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_fov_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_roll_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_slowmo_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x2a53245a: ('animation_time', _decode_animation_time),
    0x5c5fc6e: ('unknown_0x05c5fc6e', _decode_unknown_0x05c5fc6e),
    0xd4b29446: ('unknown_0xd4b29446', _decode_unknown_0xd4b29446),
    0x493d6a2d: ('motion_spline_type', _decode_motion_spline_type),
    0x5604d304: ('target_spline_type', _decode_target_spline_type),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0xc4dfbfa7: ('target_control_spline', _decode_target_control_spline),
    0x6868d4b3: ('fov_spline', _decode_fov_spline),
    0x6e6d8efd: ('roll_spline', _decode_roll_spline),
    0xf4f4798e: ('slowmo_control_spline', _decode_slowmo_control_spline),
}
