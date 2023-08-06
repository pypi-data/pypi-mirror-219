# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct54 import UnknownStruct54


@dataclasses.dataclass()
class UnknownStruct53(BaseProperty):
    unknown_struct54: UnknownStruct54 = dataclasses.field(default_factory=UnknownStruct54)
    insert_chance: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'E\xd3\x90\x80')  # 0x45d39080
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct54.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1f\x9b\xcb\x8f')  # 0x1f9bcb8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.insert_chance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct54=UnknownStruct54.from_json(data['unknown_struct54']),
            insert_chance=data['insert_chance'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct54': self.unknown_struct54.to_json(),
            'insert_chance': self.insert_chance,
        }


def _decode_unknown_struct54(data: typing.BinaryIO, property_size: int):
    return UnknownStruct54.from_stream(data, property_size)


def _decode_insert_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x45d39080: ('unknown_struct54', _decode_unknown_struct54),
    0x1f9bcb8f: ('insert_chance', _decode_insert_chance),
}
