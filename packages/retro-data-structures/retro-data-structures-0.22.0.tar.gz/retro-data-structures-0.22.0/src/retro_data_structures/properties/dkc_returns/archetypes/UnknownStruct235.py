# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct232 import UnknownStruct232
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct233 import UnknownStruct233
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct234 import UnknownStruct234


@dataclasses.dataclass()
class UnknownStruct235(BaseProperty):
    first_attack_delay: float = dataclasses.field(default=2.0)
    unknown_struct232: UnknownStruct232 = dataclasses.field(default_factory=UnknownStruct232)
    unknown_struct233: UnknownStruct233 = dataclasses.field(default_factory=UnknownStruct233)
    unknown_struct234: UnknownStruct234 = dataclasses.field(default_factory=UnknownStruct234)

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

        data.write(b'[\x94DK')  # 0x5b94444b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.first_attack_delay))

        data.write(b'\xfeMd\x82')  # 0xfe4d6482
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct232.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's\xffV\x13')  # 0x73ff5613
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct233.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc7\x15\x0eZ')  # 0xc7150e5a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct234.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            first_attack_delay=data['first_attack_delay'],
            unknown_struct232=UnknownStruct232.from_json(data['unknown_struct232']),
            unknown_struct233=UnknownStruct233.from_json(data['unknown_struct233']),
            unknown_struct234=UnknownStruct234.from_json(data['unknown_struct234']),
        )

    def to_json(self) -> dict:
        return {
            'first_attack_delay': self.first_attack_delay,
            'unknown_struct232': self.unknown_struct232.to_json(),
            'unknown_struct233': self.unknown_struct233.to_json(),
            'unknown_struct234': self.unknown_struct234.to_json(),
        }


def _decode_first_attack_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct232(data: typing.BinaryIO, property_size: int):
    return UnknownStruct232.from_stream(data, property_size)


def _decode_unknown_struct233(data: typing.BinaryIO, property_size: int):
    return UnknownStruct233.from_stream(data, property_size)


def _decode_unknown_struct234(data: typing.BinaryIO, property_size: int):
    return UnknownStruct234.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5b94444b: ('first_attack_delay', _decode_first_attack_delay),
    0xfe4d6482: ('unknown_struct232', _decode_unknown_struct232),
    0x73ff5613: ('unknown_struct233', _decode_unknown_struct233),
    0xc7150e5a: ('unknown_struct234', _decode_unknown_struct234),
}
