# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct237 import UnknownStruct237
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct238 import UnknownStruct238
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct239 import UnknownStruct239


@dataclasses.dataclass()
class UnknownStruct240(BaseProperty):
    mod_should_attack_chance: float = dataclasses.field(default=3.0)
    unknown: float = dataclasses.field(default=3.0)
    unknown_struct237: UnknownStruct237 = dataclasses.field(default_factory=UnknownStruct237)
    unknown_struct238: UnknownStruct238 = dataclasses.field(default_factory=UnknownStruct238)
    unknown_struct239: UnknownStruct239 = dataclasses.field(default_factory=UnknownStruct239)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'9\x1fP\xeb')  # 0x391f50eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mod_should_attack_chance))

        data.write(b'\x88\xe8\xcb\xa1')  # 0x88e8cba1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'U\x99\x0e\xd8')  # 0x55990ed8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct237.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe5\x91^p')  # 0xe5915e70
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct238.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x84\x85^\x0f')  # 0x84855e0f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct239.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            mod_should_attack_chance=data['mod_should_attack_chance'],
            unknown=data['unknown'],
            unknown_struct237=UnknownStruct237.from_json(data['unknown_struct237']),
            unknown_struct238=UnknownStruct238.from_json(data['unknown_struct238']),
            unknown_struct239=UnknownStruct239.from_json(data['unknown_struct239']),
        )

    def to_json(self) -> dict:
        return {
            'mod_should_attack_chance': self.mod_should_attack_chance,
            'unknown': self.unknown,
            'unknown_struct237': self.unknown_struct237.to_json(),
            'unknown_struct238': self.unknown_struct238.to_json(),
            'unknown_struct239': self.unknown_struct239.to_json(),
        }


def _decode_mod_should_attack_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct237(data: typing.BinaryIO, property_size: int):
    return UnknownStruct237.from_stream(data, property_size)


def _decode_unknown_struct238(data: typing.BinaryIO, property_size: int):
    return UnknownStruct238.from_stream(data, property_size)


def _decode_unknown_struct239(data: typing.BinaryIO, property_size: int):
    return UnknownStruct239.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x391f50eb: ('mod_should_attack_chance', _decode_mod_should_attack_chance),
    0x88e8cba1: ('unknown', _decode_unknown),
    0x55990ed8: ('unknown_struct237', _decode_unknown_struct237),
    0xe5915e70: ('unknown_struct238', _decode_unknown_struct238),
    0x84855e0f: ('unknown_struct239', _decode_unknown_struct239),
}
