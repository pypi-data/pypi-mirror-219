# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.SpindleCameraStruct import SpindleCameraStruct
from retro_data_structures.properties.echoes.archetypes.SplineType import SplineType
from retro_data_structures.properties.echoes.core.Spline import Spline


@dataclasses.dataclass()
class SpindleCamera(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    flags_spindle_camera: int = dataclasses.field(default=6400)
    spindle_camera_struct_0xe56495fb: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x239debfc: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x27e8d703: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x2f914525: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x23aa31b7: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0xe9e388af: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0xde5a2c87: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x1b3b2394: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0xf5666b6e: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x66c618aa: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0xb36d0fb6: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0xcbb013cb: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x4abfb789: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0xfb6a407a: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x3ae66f80: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_0x6654ae92: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    target_spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    unknown_0x33b4f106: bool = dataclasses.field(default=False)
    target_control_spline: Spline = dataclasses.field(default_factory=Spline)
    spline_type: SplineType = dataclasses.field(default_factory=SplineType)
    unknown_0x431769c6: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SPND'

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
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b';\xf4\xeb\xa8')  # 0x3bf4eba8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_spindle_camera))

        data.write(b'\xe5d\x95\xfb')  # 0xe56495fb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0xe56495fb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'#\x9d\xeb\xfc')  # 0x239debfc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x239debfc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"'\xe8\xd7\x03")  # 0x27e8d703
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x27e8d703.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/\x91E%')  # 0x2f914525
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x2f914525.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'#\xaa1\xb7')  # 0x23aa31b7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x23aa31b7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9\xe3\x88\xaf')  # 0xe9e388af
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0xe9e388af.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdeZ,\x87')  # 0xde5a2c87
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0xde5a2c87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b;#\x94')  # 0x1b3b2394
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x1b3b2394.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf5fkn')  # 0xf5666b6e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0xf5666b6e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'f\xc6\x18\xaa')  # 0x66c618aa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x66c618aa.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3m\x0f\xb6')  # 0xb36d0fb6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0xb36d0fb6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcb\xb0\x13\xcb')  # 0xcbb013cb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0xcbb013cb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J\xbf\xb7\x89')  # 0x4abfb789
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x4abfb789.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfbj@z')  # 0xfb6a407a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0xfb6a407a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':\xe6o\x80')  # 0x3ae66f80
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x3ae66f80.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'fT\xae\x92')  # 0x6654ae92
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spindle_camera_struct_0x6654ae92.to_stream(data)
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

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            flags_spindle_camera=data['flags_spindle_camera'],
            spindle_camera_struct_0xe56495fb=SpindleCameraStruct.from_json(data['spindle_camera_struct_0xe56495fb']),
            spindle_camera_struct_0x239debfc=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x239debfc']),
            spindle_camera_struct_0x27e8d703=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x27e8d703']),
            spindle_camera_struct_0x2f914525=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x2f914525']),
            spindle_camera_struct_0x23aa31b7=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x23aa31b7']),
            spindle_camera_struct_0xe9e388af=SpindleCameraStruct.from_json(data['spindle_camera_struct_0xe9e388af']),
            spindle_camera_struct_0xde5a2c87=SpindleCameraStruct.from_json(data['spindle_camera_struct_0xde5a2c87']),
            spindle_camera_struct_0x1b3b2394=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x1b3b2394']),
            spindle_camera_struct_0xf5666b6e=SpindleCameraStruct.from_json(data['spindle_camera_struct_0xf5666b6e']),
            spindle_camera_struct_0x66c618aa=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x66c618aa']),
            spindle_camera_struct_0xb36d0fb6=SpindleCameraStruct.from_json(data['spindle_camera_struct_0xb36d0fb6']),
            spindle_camera_struct_0xcbb013cb=SpindleCameraStruct.from_json(data['spindle_camera_struct_0xcbb013cb']),
            spindle_camera_struct_0x4abfb789=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x4abfb789']),
            spindle_camera_struct_0xfb6a407a=SpindleCameraStruct.from_json(data['spindle_camera_struct_0xfb6a407a']),
            spindle_camera_struct_0x3ae66f80=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x3ae66f80']),
            spindle_camera_struct_0x6654ae92=SpindleCameraStruct.from_json(data['spindle_camera_struct_0x6654ae92']),
            target_spline_type=SplineType.from_json(data['target_spline_type']),
            unknown_0x33b4f106=data['unknown_0x33b4f106'],
            target_control_spline=Spline.from_json(data['target_control_spline']),
            spline_type=SplineType.from_json(data['spline_type']),
            unknown_0x431769c6=data['unknown_0x431769c6'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'flags_spindle_camera': self.flags_spindle_camera,
            'spindle_camera_struct_0xe56495fb': self.spindle_camera_struct_0xe56495fb.to_json(),
            'spindle_camera_struct_0x239debfc': self.spindle_camera_struct_0x239debfc.to_json(),
            'spindle_camera_struct_0x27e8d703': self.spindle_camera_struct_0x27e8d703.to_json(),
            'spindle_camera_struct_0x2f914525': self.spindle_camera_struct_0x2f914525.to_json(),
            'spindle_camera_struct_0x23aa31b7': self.spindle_camera_struct_0x23aa31b7.to_json(),
            'spindle_camera_struct_0xe9e388af': self.spindle_camera_struct_0xe9e388af.to_json(),
            'spindle_camera_struct_0xde5a2c87': self.spindle_camera_struct_0xde5a2c87.to_json(),
            'spindle_camera_struct_0x1b3b2394': self.spindle_camera_struct_0x1b3b2394.to_json(),
            'spindle_camera_struct_0xf5666b6e': self.spindle_camera_struct_0xf5666b6e.to_json(),
            'spindle_camera_struct_0x66c618aa': self.spindle_camera_struct_0x66c618aa.to_json(),
            'spindle_camera_struct_0xb36d0fb6': self.spindle_camera_struct_0xb36d0fb6.to_json(),
            'spindle_camera_struct_0xcbb013cb': self.spindle_camera_struct_0xcbb013cb.to_json(),
            'spindle_camera_struct_0x4abfb789': self.spindle_camera_struct_0x4abfb789.to_json(),
            'spindle_camera_struct_0xfb6a407a': self.spindle_camera_struct_0xfb6a407a.to_json(),
            'spindle_camera_struct_0x3ae66f80': self.spindle_camera_struct_0x3ae66f80.to_json(),
            'spindle_camera_struct_0x6654ae92': self.spindle_camera_struct_0x6654ae92.to_json(),
            'target_spline_type': self.target_spline_type.to_json(),
            'unknown_0x33b4f106': self.unknown_0x33b4f106,
            'target_control_spline': self.target_control_spline.to_json(),
            'spline_type': self.spline_type.to_json(),
            'unknown_0x431769c6': self.unknown_0x431769c6,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0xe56495fb(self, asset_manager):
        yield from self.spindle_camera_struct_0xe56495fb.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x239debfc(self, asset_manager):
        yield from self.spindle_camera_struct_0x239debfc.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x27e8d703(self, asset_manager):
        yield from self.spindle_camera_struct_0x27e8d703.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x2f914525(self, asset_manager):
        yield from self.spindle_camera_struct_0x2f914525.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x23aa31b7(self, asset_manager):
        yield from self.spindle_camera_struct_0x23aa31b7.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0xe9e388af(self, asset_manager):
        yield from self.spindle_camera_struct_0xe9e388af.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0xde5a2c87(self, asset_manager):
        yield from self.spindle_camera_struct_0xde5a2c87.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x1b3b2394(self, asset_manager):
        yield from self.spindle_camera_struct_0x1b3b2394.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0xf5666b6e(self, asset_manager):
        yield from self.spindle_camera_struct_0xf5666b6e.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x66c618aa(self, asset_manager):
        yield from self.spindle_camera_struct_0x66c618aa.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0xb36d0fb6(self, asset_manager):
        yield from self.spindle_camera_struct_0xb36d0fb6.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0xcbb013cb(self, asset_manager):
        yield from self.spindle_camera_struct_0xcbb013cb.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x4abfb789(self, asset_manager):
        yield from self.spindle_camera_struct_0x4abfb789.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0xfb6a407a(self, asset_manager):
        yield from self.spindle_camera_struct_0xfb6a407a.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x3ae66f80(self, asset_manager):
        yield from self.spindle_camera_struct_0x3ae66f80.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_0x6654ae92(self, asset_manager):
        yield from self.spindle_camera_struct_0x6654ae92.dependencies_for(asset_manager)

    def _dependencies_for_target_spline_type(self, asset_manager):
        yield from self.target_spline_type.dependencies_for(asset_manager)

    def _dependencies_for_spline_type(self, asset_manager):
        yield from self.spline_type.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_spindle_camera_struct_0xe56495fb, "spindle_camera_struct_0xe56495fb", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x239debfc, "spindle_camera_struct_0x239debfc", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x27e8d703, "spindle_camera_struct_0x27e8d703", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x2f914525, "spindle_camera_struct_0x2f914525", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x23aa31b7, "spindle_camera_struct_0x23aa31b7", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0xe9e388af, "spindle_camera_struct_0xe9e388af", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0xde5a2c87, "spindle_camera_struct_0xde5a2c87", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x1b3b2394, "spindle_camera_struct_0x1b3b2394", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0xf5666b6e, "spindle_camera_struct_0xf5666b6e", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x66c618aa, "spindle_camera_struct_0x66c618aa", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0xb36d0fb6, "spindle_camera_struct_0xb36d0fb6", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0xcbb013cb, "spindle_camera_struct_0xcbb013cb", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x4abfb789, "spindle_camera_struct_0x4abfb789", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0xfb6a407a, "spindle_camera_struct_0xfb6a407a", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x3ae66f80, "spindle_camera_struct_0x3ae66f80", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_0x6654ae92, "spindle_camera_struct_0x6654ae92", "SpindleCameraStruct"),
            (self._dependencies_for_target_spline_type, "target_spline_type", "SplineType"),
            (self._dependencies_for_spline_type, "spline_type", "SplineType"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SpindleCamera.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_flags_spindle_camera(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_spindle_camera_struct_0xe56495fb(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x239debfc(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x27e8d703(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x2f914525(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x23aa31b7(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0xe9e388af(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0xde5a2c87(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x1b3b2394(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0xf5666b6e(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x66c618aa(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0xb36d0fb6(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0xcbb013cb(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x4abfb789(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0xfb6a407a(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x3ae66f80(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_spindle_camera_struct_0x6654ae92(data: typing.BinaryIO, property_size: int):
    return SpindleCameraStruct.from_stream(data, property_size)


def _decode_target_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_unknown_0x33b4f106(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_target_control_spline(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_spline_type(data: typing.BinaryIO, property_size: int):
    return SplineType.from_stream(data, property_size)


def _decode_unknown_0x431769c6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x3bf4eba8: ('flags_spindle_camera', _decode_flags_spindle_camera),
    0xe56495fb: ('spindle_camera_struct_0xe56495fb', _decode_spindle_camera_struct_0xe56495fb),
    0x239debfc: ('spindle_camera_struct_0x239debfc', _decode_spindle_camera_struct_0x239debfc),
    0x27e8d703: ('spindle_camera_struct_0x27e8d703', _decode_spindle_camera_struct_0x27e8d703),
    0x2f914525: ('spindle_camera_struct_0x2f914525', _decode_spindle_camera_struct_0x2f914525),
    0x23aa31b7: ('spindle_camera_struct_0x23aa31b7', _decode_spindle_camera_struct_0x23aa31b7),
    0xe9e388af: ('spindle_camera_struct_0xe9e388af', _decode_spindle_camera_struct_0xe9e388af),
    0xde5a2c87: ('spindle_camera_struct_0xde5a2c87', _decode_spindle_camera_struct_0xde5a2c87),
    0x1b3b2394: ('spindle_camera_struct_0x1b3b2394', _decode_spindle_camera_struct_0x1b3b2394),
    0xf5666b6e: ('spindle_camera_struct_0xf5666b6e', _decode_spindle_camera_struct_0xf5666b6e),
    0x66c618aa: ('spindle_camera_struct_0x66c618aa', _decode_spindle_camera_struct_0x66c618aa),
    0xb36d0fb6: ('spindle_camera_struct_0xb36d0fb6', _decode_spindle_camera_struct_0xb36d0fb6),
    0xcbb013cb: ('spindle_camera_struct_0xcbb013cb', _decode_spindle_camera_struct_0xcbb013cb),
    0x4abfb789: ('spindle_camera_struct_0x4abfb789', _decode_spindle_camera_struct_0x4abfb789),
    0xfb6a407a: ('spindle_camera_struct_0xfb6a407a', _decode_spindle_camera_struct_0xfb6a407a),
    0x3ae66f80: ('spindle_camera_struct_0x3ae66f80', _decode_spindle_camera_struct_0x3ae66f80),
    0x6654ae92: ('spindle_camera_struct_0x6654ae92', _decode_spindle_camera_struct_0x6654ae92),
    0x5604d304: ('target_spline_type', _decode_target_spline_type),
    0x33b4f106: ('unknown_0x33b4f106', _decode_unknown_0x33b4f106),
    0xc4dfbfa7: ('target_control_spline', _decode_target_control_spline),
    0x33e4685b: ('spline_type', _decode_spline_type),
    0x431769c6: ('unknown_0x431769c6', _decode_unknown_0x431769c6),
}
