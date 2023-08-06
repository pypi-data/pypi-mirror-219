# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.Convergence import Convergence


@dataclasses.dataclass()
class CameraMotion(BaseProperty):
    motion_type: Convergence = dataclasses.field(default_factory=Convergence)
    collision_type: int = dataclasses.field(default=2969932169)  # Choice

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xc1Tz\xf3')  # 0xc1547af3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6t\xea=')  # 0xb674ea3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.collision_type))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_type=Convergence.from_json(data['motion_type']),
            collision_type=data['collision_type'],
        )

    def to_json(self) -> dict:
        return {
            'motion_type': self.motion_type.to_json(),
            'collision_type': self.collision_type,
        }


def _decode_motion_type(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_collision_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc1547af3: ('motion_type', _decode_motion_type),
    0xb674ea3d: ('collision_type', _decode_collision_type),
}
