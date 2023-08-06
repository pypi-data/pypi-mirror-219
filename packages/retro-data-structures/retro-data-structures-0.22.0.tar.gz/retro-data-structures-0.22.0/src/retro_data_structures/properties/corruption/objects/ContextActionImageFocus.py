# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ContextActionImageFocus(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    initial_angle: float = dataclasses.field(default=0.0)
    min_angle: float = dataclasses.field(default=-90.0)
    max_angle: float = dataclasses.field(default=90.0)
    fudge_angle: float = dataclasses.field(default=2.0)
    lock_angle: float = dataclasses.field(default=0.0)
    lock_time: float = dataclasses.field(default=1.0)
    drift_angle: float = dataclasses.field(default=2.0)
    drift_period: float = dataclasses.field(default=4.0)
    rotation_scale: float = dataclasses.field(default=1.0)
    movement_distance: float = dataclasses.field(default=0.07500000298023224)
    rotation_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    animation: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CAIF'

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x90\xac\x80A')  # 0x90ac8041
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_angle))

        data.write(b'\x99,-\xf5')  # 0x992c2df5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_angle))

        data.write(b'\xd9cU\x83')  # 0xd9635583
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_angle))

        data.write(b'9\xbd\x0fp')  # 0x39bd0f70
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fudge_angle))

        data.write(b'd\xed\xce\xf1')  # 0x64edcef1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_angle))

        data.write(b'0\x8e\xdcD')  # 0x308edc44
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_time))

        data.write(b'G\x07#;')  # 0x4707233b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drift_angle))

        data.write(b'S\x9d0\x90')  # 0x539d3090
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drift_period))

        data.write(b'^\x0e\xe1W')  # 0x5e0ee157
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rotation_scale))

        data.write(b'\x1a\x8aE\xfe')  # 0x1a8a45fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_distance))

        data.write(b'\xd7\x02\xeb\xd7')  # 0xd702ebd7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rotation_sound))

        data.write(b'\xaa\xcd\xb1\x1c')  # 0xaacdb11c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.animation))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            initial_angle=data['initial_angle'],
            min_angle=data['min_angle'],
            max_angle=data['max_angle'],
            fudge_angle=data['fudge_angle'],
            lock_angle=data['lock_angle'],
            lock_time=data['lock_time'],
            drift_angle=data['drift_angle'],
            drift_period=data['drift_period'],
            rotation_scale=data['rotation_scale'],
            movement_distance=data['movement_distance'],
            rotation_sound=data['rotation_sound'],
            animation=data['animation'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'initial_angle': self.initial_angle,
            'min_angle': self.min_angle,
            'max_angle': self.max_angle,
            'fudge_angle': self.fudge_angle,
            'lock_angle': self.lock_angle,
            'lock_time': self.lock_time,
            'drift_angle': self.drift_angle,
            'drift_period': self.drift_period,
            'rotation_scale': self.rotation_scale,
            'movement_distance': self.movement_distance,
            'rotation_sound': self.rotation_sound,
            'animation': self.animation,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_initial_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fudge_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drift_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drift_period(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rotation_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x90ac8041: ('initial_angle', _decode_initial_angle),
    0x992c2df5: ('min_angle', _decode_min_angle),
    0xd9635583: ('max_angle', _decode_max_angle),
    0x39bd0f70: ('fudge_angle', _decode_fudge_angle),
    0x64edcef1: ('lock_angle', _decode_lock_angle),
    0x308edc44: ('lock_time', _decode_lock_time),
    0x4707233b: ('drift_angle', _decode_drift_angle),
    0x539d3090: ('drift_period', _decode_drift_period),
    0x5e0ee157: ('rotation_scale', _decode_rotation_scale),
    0x1a8a45fe: ('movement_distance', _decode_movement_distance),
    0xd702ebd7: ('rotation_sound', _decode_rotation_sound),
    0xaacdb11c: ('animation', _decode_animation),
}
