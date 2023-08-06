# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.InterpolationMethod import InterpolationMethod
from retro_data_structures.properties.corruption.archetypes.NonSlowdown import NonSlowdown


@dataclasses.dataclass()
class MotionInterpolationMethod(BaseProperty):
    motion_type: enums.MotionType = dataclasses.field(default=enums.MotionType.Unknown2)
    non_slowdown: NonSlowdown = dataclasses.field(default_factory=NonSlowdown)
    motion_control: InterpolationMethod = dataclasses.field(default_factory=InterpolationMethod)

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

        data.write(b'\x94\x8a\xf5q')  # 0x948af571
        data.write(b'\x00\x04')  # size
        self.motion_type.to_stream(data)

        data.write(b'y\xdeK\xa5')  # 0x79de4ba5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.non_slowdown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\x7f\x9fE')  # 0x287f9f45
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_control.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_type=enums.MotionType.from_json(data['motion_type']),
            non_slowdown=NonSlowdown.from_json(data['non_slowdown']),
            motion_control=InterpolationMethod.from_json(data['motion_control']),
        )

    def to_json(self) -> dict:
        return {
            'motion_type': self.motion_type.to_json(),
            'non_slowdown': self.non_slowdown.to_json(),
            'motion_control': self.motion_control.to_json(),
        }


def _decode_motion_type(data: typing.BinaryIO, property_size: int):
    return enums.MotionType.from_stream(data)


def _decode_non_slowdown(data: typing.BinaryIO, property_size: int):
    return NonSlowdown.from_stream(data, property_size)


def _decode_motion_control(data: typing.BinaryIO, property_size: int):
    return InterpolationMethod.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x948af571: ('motion_type', _decode_motion_type),
    0x79de4ba5: ('non_slowdown', _decode_non_slowdown),
    0x287f9f45: ('motion_control', _decode_motion_control),
}
