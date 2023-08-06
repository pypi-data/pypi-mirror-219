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
class PathCamera(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flags_path_camera: int = dataclasses.field(default=32)  # Flagset
    unknown_0xd4b29446: int = dataclasses.field(default=0)
    motion_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    target_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    target_control_spline: Spline = dataclasses.field(default_factory=Spline)
    fov_spline: Spline = dataclasses.field(default_factory=Spline)
    speed_control_spline: Spline = dataclasses.field(default_factory=Spline)
    spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    unknown_0x431769c6: bool = dataclasses.field(default=False)
    distance: float = dataclasses.field(default=4.0)
    speed: float = dataclasses.field(default=10.0)
    dampen_distance: float = dataclasses.field(default=3.0)
    initial_position: int = dataclasses.field(default=0)
    angular_speed: float = dataclasses.field(default=120.0)
    unknown_0x12861f7d: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x96ac52b0: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PCAM'

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\\\xbd[\xae')  # 0x5cbd5bae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.flags_path_camera))

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

        data.write(b"'\xe5\xf8t")  # 0x27e5f874
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_control_spline.to_stream(data)
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

        data.write(b'\xed\xd0q`')  # 0xedd07160
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.speed_control_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

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

        data.write(b'\xc3\xbfC\xbe')  # 0xc3bf43be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.distance))

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'2\xf85\xec')  # 0x32f835ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dampen_distance))

        data.write(b'\xe8\xfcr\xb6')  # 0xe8fc72b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.initial_position))

        data.write(b'\xbc\xd73?')  # 0xbcd7333f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.angular_speed))

        data.write(b'\x12\x86\x1f}')  # 0x12861f7d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x12861f7d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x96\xacR\xb0')  # 0x96ac52b0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x96ac52b0.to_stream(data)
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
            flags_path_camera=data['flags_path_camera'],
            unknown_0xd4b29446=data['unknown_0xd4b29446'],
            motion_spline_type=SplineType.from_json(data['motion_spline_type']),
            motion_control_spline=Spline.from_json(data['motion_control_spline']),
            target_spline_type=SplineType.from_json(data['target_spline_type']),
            target_control_spline=Spline.from_json(data['target_control_spline']),
            fov_spline=Spline.from_json(data['fov_spline']),
            speed_control_spline=Spline.from_json(data['speed_control_spline']),
            spline_type=SplineType.from_json(data['spline_type']),
            unknown_0x431769c6=data['unknown_0x431769c6'],
            distance=data['distance'],
            speed=data['speed'],
            dampen_distance=data['dampen_distance'],
            initial_position=data['initial_position'],
            angular_speed=data['angular_speed'],
            unknown_0x12861f7d=Spline.from_json(data['unknown_0x12861f7d']),
            unknown_0x96ac52b0=Spline.from_json(data['unknown_0x96ac52b0']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flags_path_camera': self.flags_path_camera,
            'unknown_0xd4b29446': self.unknown_0xd4b29446,
            'motion_spline_type': self.motion_spline_type.to_json(),
            'motion_control_spline': self.motion_control_spline.to_json(),
            'target_spline_type': self.target_spline_type.to_json(),
            'target_control_spline': self.target_control_spline.to_json(),
            'fov_spline': self.fov_spline.to_json(),
            'speed_control_spline': self.speed_control_spline.to_json(),
            'spline_type': self.spline_type.to_json(),
            'unknown_0x431769c6': self.unknown_0x431769c6,
            'distance': self.distance,
            'speed': self.speed,
            'dampen_distance': self.dampen_distance,
            'initial_position': self.initial_position,
            'angular_speed': self.angular_speed,
            'unknown_0x12861f7d': self.unknown_0x12861f7d.to_json(),
            'unknown_0x96ac52b0': self.unknown_0x96ac52b0.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_motion_spline_type(self, asset_manager):
        yield from self.motion_spline_type.dependencies_for(asset_manager)

    def _dependencies_for_target_spline_type(self, asset_manager):
        yield from self.target_spline_type.dependencies_for(asset_manager)

    def _dependencies_for_spline_type(self, asset_manager):
        yield from self.spline_type.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_motion_spline_type, "motion_spline_type", "SplineType"),
            (self._dependencies_for_target_spline_type, "target_spline_type", "SplineType"),
            (self._dependencies_for_spline_type, "spline_type", "SplineType"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PathCamera.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flags_path_camera(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0xd4b29446(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_motion_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_motion_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_target_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_target_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_fov_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_speed_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_unknown_0x431769c6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dampen_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_position(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_angular_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x12861f7d(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x96ac52b0(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x5cbd5bae: ('flags_path_camera', _decode_flags_path_camera),
    0xd4b29446: ('unknown_0xd4b29446', _decode_unknown_0xd4b29446),
    0x493d6a2d: ('motion_spline_type', _decode_motion_spline_type),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0x5604d304: ('target_spline_type', _decode_target_spline_type),
    0xc4dfbfa7: ('target_control_spline', _decode_target_control_spline),
    0x6868d4b3: ('fov_spline', _decode_fov_spline),
    0xedd07160: ('speed_control_spline', _decode_speed_control_spline),
    0x33e4685b: ('spline_type', _decode_spline_type),
    0x431769c6: ('unknown_0x431769c6', _decode_unknown_0x431769c6),
    0xc3bf43be: ('distance', _decode_distance),
    0x6392404e: ('speed', _decode_speed),
    0x32f835ec: ('dampen_distance', _decode_dampen_distance),
    0xe8fc72b6: ('initial_position', _decode_initial_position),
    0xbcd7333f: ('angular_speed', _decode_angular_speed),
    0x12861f7d: ('unknown_0x12861f7d', _decode_unknown_0x12861f7d),
    0x96ac52b0: ('unknown_0x96ac52b0', _decode_unknown_0x96ac52b0),
}
