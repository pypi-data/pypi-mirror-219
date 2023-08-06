# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.Animations import Animations
from retro_data_structures.properties.dkc_returns.archetypes.Groups import Groups
from retro_data_structures.properties.dkc_returns.archetypes.Sets import Sets


@dataclasses.dataclass()
class RetronomeMessage(BaseProperty):
    time_offset: float = dataclasses.field(default=0.0)
    sets: Sets = dataclasses.field(default_factory=Sets)
    groups: Groups = dataclasses.field(default_factory=Groups)
    animations: Animations = dataclasses.field(default_factory=Animations)

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

        data.write(b'%9\xdeF')  # 0x2539de46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_offset))

        data.write(b'J\xb7\xd5\xb8')  # 0x4ab7d5b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sets.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfe%|\xe1')  # 0xfe257ce1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.groups.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7\x8aK\x1f')  # 0xd78a4b1f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animations.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            time_offset=data['time_offset'],
            sets=Sets.from_json(data['sets']),
            groups=Groups.from_json(data['groups']),
            animations=Animations.from_json(data['animations']),
        )

    def to_json(self) -> dict:
        return {
            'time_offset': self.time_offset,
            'sets': self.sets.to_json(),
            'groups': self.groups.to_json(),
            'animations': self.animations.to_json(),
        }


def _decode_time_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sets(data: typing.BinaryIO, property_size: int):
    return Sets.from_stream(data, property_size)


def _decode_groups(data: typing.BinaryIO, property_size: int):
    return Groups.from_stream(data, property_size)


def _decode_animations(data: typing.BinaryIO, property_size: int):
    return Animations.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2539de46: ('time_offset', _decode_time_offset),
    0x4ab7d5b8: ('sets', _decode_sets),
    0xfe257ce1: ('groups', _decode_groups),
    0xd78a4b1f: ('animations', _decode_animations),
}
