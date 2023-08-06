# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.FOVInterpolationMethod import FOVInterpolationMethod
from retro_data_structures.properties.corruption.archetypes.MotionInterpolationMethod import MotionInterpolationMethod
from retro_data_structures.properties.corruption.archetypes.OrientationInterpolationMethod import OrientationInterpolationMethod


@dataclasses.dataclass()
class CinematicBlend(BaseProperty):
    motion_blend: MotionInterpolationMethod = dataclasses.field(default_factory=MotionInterpolationMethod)
    orientation_blend: OrientationInterpolationMethod = dataclasses.field(default_factory=OrientationInterpolationMethod)
    fov_blend: FOVInterpolationMethod = dataclasses.field(default_factory=FOVInterpolationMethod)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
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

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xb5\xc3g\xe9')  # 0xb5c367e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_blend.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7O\x8c\x89')  # 0xf74f8c89
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orientation_blend.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18\xe6\xbe\xd2')  # 0x18e6bed2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fov_blend.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_blend=MotionInterpolationMethod.from_json(data['motion_blend']),
            orientation_blend=OrientationInterpolationMethod.from_json(data['orientation_blend']),
            fov_blend=FOVInterpolationMethod.from_json(data['fov_blend']),
        )

    def to_json(self) -> dict:
        return {
            'motion_blend': self.motion_blend.to_json(),
            'orientation_blend': self.orientation_blend.to_json(),
            'fov_blend': self.fov_blend.to_json(),
        }


def _decode_motion_blend(data: typing.BinaryIO, property_size: int):
    return MotionInterpolationMethod.from_stream(data, property_size)


def _decode_orientation_blend(data: typing.BinaryIO, property_size: int):
    return OrientationInterpolationMethod.from_stream(data, property_size)


def _decode_fov_blend(data: typing.BinaryIO, property_size: int):
    return FOVInterpolationMethod.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb5c367e9: ('motion_blend', _decode_motion_blend),
    0xf74f8c89: ('orientation_blend', _decode_orientation_blend),
    0x18e6bed2: ('fov_blend', _decode_fov_blend),
}
