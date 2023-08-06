# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.CameraOrientation import CameraOrientation
from retro_data_structures.properties.corruption.archetypes.CinematicBlend import CinematicBlend
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.SavedStateID import SavedStateID
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class CinematicCamera(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    object_id: SavedStateID = dataclasses.field(default_factory=SavedStateID)
    camera_mode: enums.CameraMode = dataclasses.field(default=enums.CameraMode.Unknown1)
    use_script_object_transform: bool = dataclasses.field(default=False)
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    cinematic_start_type: enums.CinematicStartType = dataclasses.field(default=enums.CinematicStartType.Unknown1)
    blend: CinematicBlend = dataclasses.field(default_factory=CinematicBlend)
    cinematic_ends_type: enums.CinematicEndsType = dataclasses.field(default=enums.CinematicEndsType.Unknown1)
    end_time: float = dataclasses.field(default=10.0)
    unknown: int = dataclasses.field(default=2132)  # Flagset
    motion_control_spline: Spline = dataclasses.field(default_factory=Spline)
    target_control_spline: Spline = dataclasses.field(default_factory=Spline)
    orientation_behavior: CameraOrientation = dataclasses.field(default_factory=CameraOrientation)
    fov_spline: Spline = dataclasses.field(default_factory=Spline)
    roll_spline: Spline = dataclasses.field(default_factory=Spline)
    slowmo_control_spline: Spline = dataclasses.field(default_factory=Spline)
    near_plane_distance_spline: Spline = dataclasses.field(default_factory=Spline)
    far_plane_distance_spline: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CINE'

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

        data.write(b'\x16\xd9\xa7]')  # 0x16d9a75d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.object_id.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcc\x08\xef\x1b')  # 0xcc08ef1b
        data.write(b'\x00\x04')  # size
        self.camera_mode.to_stream(data)

        data.write(b'c\x87\xe4K')  # 0x6387e44b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_script_object_transform))

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb1\xac\x91v')  # 0xb1ac9176
        data.write(b'\x00\x04')  # size
        self.cinematic_start_type.to_stream(data)

        data.write(b'\x9e\xc6Rs')  # 0x9ec65273
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.blend.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97J\x96\x1f')  # 0x974a961f
        data.write(b'\x00\x04')  # size
        self.cinematic_ends_type.to_stream(data)

        data.write(b'\xab\x81Q\xea')  # 0xab8151ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.end_time))

        data.write(b'\x05\xc5\xfcn')  # 0x5c5fc6e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.unknown))

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

        data.write(b'e\xfc\x11\xff')  # 0x65fc11ff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_behavior.to_stream(data, default_override={'orientation_type': 648890987, 'flags_orientation': 12})
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

        data.write(b')QX\x02')  # 0x29515802
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.near_plane_distance_spline.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdf\x18e\xa6')  # 0xdf1865a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.far_plane_distance_spline.to_stream(data)
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
            object_id=SavedStateID.from_json(data['object_id']),
            camera_mode=enums.CameraMode.from_json(data['camera_mode']),
            use_script_object_transform=data['use_script_object_transform'],
            animation=AnimationParameters.from_json(data['animation']),
            cinematic_start_type=enums.CinematicStartType.from_json(data['cinematic_start_type']),
            blend=CinematicBlend.from_json(data['blend']),
            cinematic_ends_type=enums.CinematicEndsType.from_json(data['cinematic_ends_type']),
            end_time=data['end_time'],
            unknown=data['unknown'],
            motion_control_spline=Spline.from_json(data['motion_control_spline']),
            target_control_spline=Spline.from_json(data['target_control_spline']),
            orientation_behavior=CameraOrientation.from_json(data['orientation_behavior']),
            fov_spline=Spline.from_json(data['fov_spline']),
            roll_spline=Spline.from_json(data['roll_spline']),
            slowmo_control_spline=Spline.from_json(data['slowmo_control_spline']),
            near_plane_distance_spline=Spline.from_json(data['near_plane_distance_spline']),
            far_plane_distance_spline=Spline.from_json(data['far_plane_distance_spline']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'object_id': self.object_id.to_json(),
            'camera_mode': self.camera_mode.to_json(),
            'use_script_object_transform': self.use_script_object_transform,
            'animation': self.animation.to_json(),
            'cinematic_start_type': self.cinematic_start_type.to_json(),
            'blend': self.blend.to_json(),
            'cinematic_ends_type': self.cinematic_ends_type.to_json(),
            'end_time': self.end_time,
            'unknown': self.unknown,
            'motion_control_spline': self.motion_control_spline.to_json(),
            'target_control_spline': self.target_control_spline.to_json(),
            'orientation_behavior': self.orientation_behavior.to_json(),
            'fov_spline': self.fov_spline.to_json(),
            'roll_spline': self.roll_spline.to_json(),
            'slowmo_control_spline': self.slowmo_control_spline.to_json(),
            'near_plane_distance_spline': self.near_plane_distance_spline.to_json(),
            'far_plane_distance_spline': self.far_plane_distance_spline.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_object_id(data: typing.BinaryIO, property_size: int):
    return SavedStateID.from_stream(data, property_size)


def _decode_camera_mode(data: typing.BinaryIO, property_size: int):
    return enums.CameraMode.from_stream(data)


def _decode_use_script_object_transform(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_cinematic_start_type(data: typing.BinaryIO, property_size: int):
    return enums.CinematicStartType.from_stream(data)


def _decode_blend(data: typing.BinaryIO, property_size: int):
    return CinematicBlend.from_stream(data, property_size)


def _decode_cinematic_ends_type(data: typing.BinaryIO, property_size: int):
    return enums.CinematicEndsType.from_stream(data)


def _decode_end_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_motion_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_target_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_orientation_behavior(data: typing.BinaryIO, property_size: int):
    return CameraOrientation.from_stream(data, property_size, default_override={'orientation_type': 648890987, 'flags_orientation': 12})


def _decode_fov_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_roll_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_slowmo_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_near_plane_distance_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_far_plane_distance_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x16d9a75d: ('object_id', _decode_object_id),
    0xcc08ef1b: ('camera_mode', _decode_camera_mode),
    0x6387e44b: ('use_script_object_transform', _decode_use_script_object_transform),
    0xa3d63f44: ('animation', _decode_animation),
    0xb1ac9176: ('cinematic_start_type', _decode_cinematic_start_type),
    0x9ec65273: ('blend', _decode_blend),
    0x974a961f: ('cinematic_ends_type', _decode_cinematic_ends_type),
    0xab8151ea: ('end_time', _decode_end_time),
    0x5c5fc6e: ('unknown', _decode_unknown),
    0x27e5f874: ('motion_control_spline', _decode_motion_control_spline),
    0xc4dfbfa7: ('target_control_spline', _decode_target_control_spline),
    0x65fc11ff: ('orientation_behavior', _decode_orientation_behavior),
    0x6868d4b3: ('fov_spline', _decode_fov_spline),
    0x6e6d8efd: ('roll_spline', _decode_roll_spline),
    0xf4f4798e: ('slowmo_control_spline', _decode_slowmo_control_spline),
    0x29515802: ('near_plane_distance_spline', _decode_near_plane_distance_spline),
    0xdf1865a6: ('far_plane_distance_spline', _decode_far_plane_distance_spline),
}
