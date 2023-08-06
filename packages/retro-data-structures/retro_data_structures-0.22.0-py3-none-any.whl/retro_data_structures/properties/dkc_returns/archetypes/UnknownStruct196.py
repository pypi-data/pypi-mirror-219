# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct196(BaseProperty):
    launch_direction: enums.LaunchDirection = dataclasses.field(default=enums.LaunchDirection.Unknown1)
    unknown: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=0.0, z=0.0))
    initial_velocity: float = dataclasses.field(default=10.0)
    gravity: float = dataclasses.field(default=1.0)

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

        data.write(b'\x1f~\xf4I')  # 0x1f7ef449
        data.write(b'\x00\x04')  # size
        self.launch_direction.to_stream(data)

        data.write(b'\xc0\x02R\x00')  # 0xc0025200
        data.write(b'\x00\x0c')  # size
        self.unknown.to_stream(data)

        data.write(b'\x81G0\x93')  # 0x81473093
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_velocity))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            launch_direction=enums.LaunchDirection.from_json(data['launch_direction']),
            unknown=Vector.from_json(data['unknown']),
            initial_velocity=data['initial_velocity'],
            gravity=data['gravity'],
        )

    def to_json(self) -> dict:
        return {
            'launch_direction': self.launch_direction.to_json(),
            'unknown': self.unknown.to_json(),
            'initial_velocity': self.initial_velocity,
            'gravity': self.gravity,
        }


def _decode_launch_direction(data: typing.BinaryIO, property_size: int):
    return enums.LaunchDirection.from_stream(data)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_initial_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1f7ef449: ('launch_direction', _decode_launch_direction),
    0xc0025200: ('unknown', _decode_unknown),
    0x81473093: ('initial_velocity', _decode_initial_velocity),
    0x2f2ae3e5: ('gravity', _decode_gravity),
}
