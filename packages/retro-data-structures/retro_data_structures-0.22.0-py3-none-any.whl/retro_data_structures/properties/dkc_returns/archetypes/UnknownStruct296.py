# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct287 import UnknownStruct287
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct288 import UnknownStruct288
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct290 import UnknownStruct290
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct291 import UnknownStruct291
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct292 import UnknownStruct292
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct295 import UnknownStruct295


@dataclasses.dataclass()
class UnknownStruct296(BaseProperty):
    unknown_struct287: UnknownStruct287 = dataclasses.field(default_factory=UnknownStruct287)
    unknown_struct288: UnknownStruct288 = dataclasses.field(default_factory=UnknownStruct288)
    unknown_struct290: UnknownStruct290 = dataclasses.field(default_factory=UnknownStruct290)
    unknown_struct291: UnknownStruct291 = dataclasses.field(default_factory=UnknownStruct291)
    unknown_struct292: UnknownStruct292 = dataclasses.field(default_factory=UnknownStruct292)
    unknown_struct295: UnknownStruct295 = dataclasses.field(default_factory=UnknownStruct295)

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'J\xe8R=')  # 0x4ae8523d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct287.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*Dqf')  # 0x2a447166
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct288.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdd\\p\x83')  # 0xdd5c7083
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct290.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6\x85s(')  # 0xe6857328
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct291.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+S\x1c/')  # 0x2b531c2f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct292.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\x91'\xfb\xc8")  # 0x9127fbc8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct295.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct287=UnknownStruct287.from_json(data['unknown_struct287']),
            unknown_struct288=UnknownStruct288.from_json(data['unknown_struct288']),
            unknown_struct290=UnknownStruct290.from_json(data['unknown_struct290']),
            unknown_struct291=UnknownStruct291.from_json(data['unknown_struct291']),
            unknown_struct292=UnknownStruct292.from_json(data['unknown_struct292']),
            unknown_struct295=UnknownStruct295.from_json(data['unknown_struct295']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct287': self.unknown_struct287.to_json(),
            'unknown_struct288': self.unknown_struct288.to_json(),
            'unknown_struct290': self.unknown_struct290.to_json(),
            'unknown_struct291': self.unknown_struct291.to_json(),
            'unknown_struct292': self.unknown_struct292.to_json(),
            'unknown_struct295': self.unknown_struct295.to_json(),
        }


def _decode_unknown_struct287(data: typing.BinaryIO, property_size: int):
    return UnknownStruct287.from_stream(data, property_size)


def _decode_unknown_struct288(data: typing.BinaryIO, property_size: int):
    return UnknownStruct288.from_stream(data, property_size)


def _decode_unknown_struct290(data: typing.BinaryIO, property_size: int):
    return UnknownStruct290.from_stream(data, property_size)


def _decode_unknown_struct291(data: typing.BinaryIO, property_size: int):
    return UnknownStruct291.from_stream(data, property_size)


def _decode_unknown_struct292(data: typing.BinaryIO, property_size: int):
    return UnknownStruct292.from_stream(data, property_size)


def _decode_unknown_struct295(data: typing.BinaryIO, property_size: int):
    return UnknownStruct295.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x4ae8523d: ('unknown_struct287', _decode_unknown_struct287),
    0x2a447166: ('unknown_struct288', _decode_unknown_struct288),
    0xdd5c7083: ('unknown_struct290', _decode_unknown_struct290),
    0xe6857328: ('unknown_struct291', _decode_unknown_struct291),
    0x2b531c2f: ('unknown_struct292', _decode_unknown_struct292),
    0x9127fbc8: ('unknown_struct295', _decode_unknown_struct295),
}
