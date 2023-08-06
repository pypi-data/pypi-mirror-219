# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence


@dataclasses.dataclass()
class UnknownStruct76(BaseProperty):
    motion_type: Convergence = dataclasses.field(default_factory=Convergence)
    use_vertical_motion: bool = dataclasses.field(default=False)
    convergence: Convergence = dataclasses.field(default_factory=Convergence)
    collision_type: enums.CollisionType = dataclasses.field(default=enums.CollisionType.Unknown1)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xc1Tz\xf3')  # 0xc1547af3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_type.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}\x0b\xca\x87')  # 0x7d0bca87
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_vertical_motion))

        data.write(b'\xd9\xa9\x0e\xc3')  # 0xd9a90ec3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6t\xea=')  # 0xb674ea3d
        data.write(b'\x00\x04')  # size
        self.collision_type.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            motion_type=Convergence.from_json(data['motion_type']),
            use_vertical_motion=data['use_vertical_motion'],
            convergence=Convergence.from_json(data['convergence']),
            collision_type=enums.CollisionType.from_json(data['collision_type']),
        )

    def to_json(self) -> dict:
        return {
            'motion_type': self.motion_type.to_json(),
            'use_vertical_motion': self.use_vertical_motion,
            'convergence': self.convergence.to_json(),
            'collision_type': self.collision_type.to_json(),
        }


def _decode_motion_type(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_use_vertical_motion(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_convergence(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


def _decode_collision_type(data: typing.BinaryIO, property_size: int):
    return enums.CollisionType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc1547af3: ('motion_type', _decode_motion_type),
    0x7d0bca87: ('use_vertical_motion', _decode_use_vertical_motion),
    0xd9a90ec3: ('convergence', _decode_convergence),
    0xb674ea3d: ('collision_type', _decode_collision_type),
}
