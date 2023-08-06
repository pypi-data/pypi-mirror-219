# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct186 import UnknownStruct186
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct187 import UnknownStruct187
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct188 import UnknownStruct188
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct189 import UnknownStruct189
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct190 import UnknownStruct190
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct191 import UnknownStruct191
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct54 import UnknownStruct54


@dataclasses.dataclass()
class UnknownStruct56(BaseProperty):
    unknown_struct54: UnknownStruct54 = dataclasses.field(default_factory=UnknownStruct54)
    unknown_struct186: UnknownStruct186 = dataclasses.field(default_factory=UnknownStruct186)
    unknown_struct187: UnknownStruct187 = dataclasses.field(default_factory=UnknownStruct187)
    unknown_struct188: UnknownStruct188 = dataclasses.field(default_factory=UnknownStruct188)
    unknown_struct189: UnknownStruct189 = dataclasses.field(default_factory=UnknownStruct189)
    unknown_struct190: UnknownStruct190 = dataclasses.field(default_factory=UnknownStruct190)
    unknown_struct191: UnknownStruct191 = dataclasses.field(default_factory=UnknownStruct191)
    frequency: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'E\xd3\x90\x80')  # 0x45d39080
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct54.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'D^\xf6i')  # 0x445ef669
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct186.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xec\x8d\xb6\x00')  # 0xec8db600
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct187.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcc\xb0\x8a4')  # 0xccb08a34
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct188.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01\x19|G')  # 0x1197c47
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct189.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1@"\\')  # 0xf140225c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct190.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbfE^\x0f')  # 0xbf455e0f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct191.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\xcb\xfe\xdc')  # 0x98cbfedc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.frequency))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct54=UnknownStruct54.from_json(data['unknown_struct54']),
            unknown_struct186=UnknownStruct186.from_json(data['unknown_struct186']),
            unknown_struct187=UnknownStruct187.from_json(data['unknown_struct187']),
            unknown_struct188=UnknownStruct188.from_json(data['unknown_struct188']),
            unknown_struct189=UnknownStruct189.from_json(data['unknown_struct189']),
            unknown_struct190=UnknownStruct190.from_json(data['unknown_struct190']),
            unknown_struct191=UnknownStruct191.from_json(data['unknown_struct191']),
            frequency=data['frequency'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct54': self.unknown_struct54.to_json(),
            'unknown_struct186': self.unknown_struct186.to_json(),
            'unknown_struct187': self.unknown_struct187.to_json(),
            'unknown_struct188': self.unknown_struct188.to_json(),
            'unknown_struct189': self.unknown_struct189.to_json(),
            'unknown_struct190': self.unknown_struct190.to_json(),
            'unknown_struct191': self.unknown_struct191.to_json(),
            'frequency': self.frequency,
        }


def _decode_unknown_struct54(data: typing.BinaryIO, property_size: int):
    return UnknownStruct54.from_stream(data, property_size)


def _decode_unknown_struct186(data: typing.BinaryIO, property_size: int):
    return UnknownStruct186.from_stream(data, property_size)


def _decode_unknown_struct187(data: typing.BinaryIO, property_size: int):
    return UnknownStruct187.from_stream(data, property_size)


def _decode_unknown_struct188(data: typing.BinaryIO, property_size: int):
    return UnknownStruct188.from_stream(data, property_size)


def _decode_unknown_struct189(data: typing.BinaryIO, property_size: int):
    return UnknownStruct189.from_stream(data, property_size)


def _decode_unknown_struct190(data: typing.BinaryIO, property_size: int):
    return UnknownStruct190.from_stream(data, property_size)


def _decode_unknown_struct191(data: typing.BinaryIO, property_size: int):
    return UnknownStruct191.from_stream(data, property_size)


def _decode_frequency(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x45d39080: ('unknown_struct54', _decode_unknown_struct54),
    0x445ef669: ('unknown_struct186', _decode_unknown_struct186),
    0xec8db600: ('unknown_struct187', _decode_unknown_struct187),
    0xccb08a34: ('unknown_struct188', _decode_unknown_struct188),
    0x1197c47: ('unknown_struct189', _decode_unknown_struct189),
    0xf140225c: ('unknown_struct190', _decode_unknown_struct190),
    0xbf455e0f: ('unknown_struct191', _decode_unknown_struct191),
    0x98cbfedc: ('frequency', _decode_frequency),
}
