# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.SpindlePositionInterpolant import SpindlePositionInterpolant


@dataclasses.dataclass()
class UnknownStruct23(BaseProperty):
    look_at_position: SpindlePositionInterpolant = dataclasses.field(default_factory=SpindlePositionInterpolant)

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
        data.write(b'\x00\x01')  # 1 properties

        data.write(b'C\xa6\xde\xd6')  # 0x43a6ded6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.look_at_position.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            look_at_position=SpindlePositionInterpolant.from_json(data['look_at_position']),
        )

    def to_json(self) -> dict:
        return {
            'look_at_position': self.look_at_position.to_json(),
        }


def _decode_look_at_position(data: typing.BinaryIO, property_size: int):
    return SpindlePositionInterpolant.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x43a6ded6: ('look_at_position', _decode_look_at_position),
}
