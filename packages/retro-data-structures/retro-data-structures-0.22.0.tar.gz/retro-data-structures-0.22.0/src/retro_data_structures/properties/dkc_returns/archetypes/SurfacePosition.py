# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence
from retro_data_structures.properties.dkc_returns.archetypes.OffsetInterpolant import OffsetInterpolant


@dataclasses.dataclass()
class SurfacePosition(BaseProperty):
    flags_surface_position: int = dataclasses.field(default=1)
    player_offset: OffsetInterpolant = dataclasses.field(default_factory=OffsetInterpolant)
    convergence: Convergence = dataclasses.field(default_factory=Convergence)

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
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\x9d\x99\xb2\xe3')  # 0x9d99b2e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.flags_surface_position))

        data.write(b'\xe6\x9cQ\xd7')  # 0xe69c51d7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.player_offset.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\x91\x08\xa5')  # 0x959108a5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            flags_surface_position=data['flags_surface_position'],
            player_offset=OffsetInterpolant.from_json(data['player_offset']),
            convergence=Convergence.from_json(data['convergence']),
        )

    def to_json(self) -> dict:
        return {
            'flags_surface_position': self.flags_surface_position,
            'player_offset': self.player_offset.to_json(),
            'convergence': self.convergence.to_json(),
        }


def _decode_flags_surface_position(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_player_offset(data: typing.BinaryIO, property_size: int):
    return OffsetInterpolant.from_stream(data, property_size)


def _decode_convergence(data: typing.BinaryIO, property_size: int):
    return Convergence.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9d99b2e3: ('flags_surface_position', _decode_flags_surface_position),
    0xe69c51d7: ('player_offset', _decode_player_offset),
    0x959108a5: ('convergence', _decode_convergence),
}
