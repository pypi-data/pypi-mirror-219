# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct192 import UnknownStruct192
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct56 import UnknownStruct56
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class JungleBossStructA(BaseProperty):
    texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    health: float = dataclasses.field(default=15.0)
    unknown_struct56_0x02eb59dc: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56)
    unknown_struct56_0xf0bcb424: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56)
    unknown_struct56_0x17a112b3: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56)
    unknown_struct56_0xcf626995: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56)
    unknown_struct56_0x287fcf02: UnknownStruct56 = dataclasses.field(default_factory=UnknownStruct56)
    unknown_struct192: UnknownStruct192 = dataclasses.field(default_factory=UnknownStruct192)

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

        data.write(b'\xd1\xf6Xr')  # 0xd1f65872
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.texture))

        data.write(b'\xf0f\x89\x19')  # 0xf0668919
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.health))

        data.write(b'\x02\xebY\xdc')  # 0x2eb59dc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0x02eb59dc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf0\xbc\xb4$')  # 0xf0bcb424
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0xf0bcb424.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x17\xa1\x12\xb3')  # 0x17a112b3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0x17a112b3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcfbi\x95')  # 0xcf626995
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0xcf626995.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\x7f\xcf\x02')  # 0x287fcf02
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct56_0x287fcf02.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'rTJ\xfd')  # 0x72544afd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct192.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            texture=data['texture'],
            health=data['health'],
            unknown_struct56_0x02eb59dc=UnknownStruct56.from_json(data['unknown_struct56_0x02eb59dc']),
            unknown_struct56_0xf0bcb424=UnknownStruct56.from_json(data['unknown_struct56_0xf0bcb424']),
            unknown_struct56_0x17a112b3=UnknownStruct56.from_json(data['unknown_struct56_0x17a112b3']),
            unknown_struct56_0xcf626995=UnknownStruct56.from_json(data['unknown_struct56_0xcf626995']),
            unknown_struct56_0x287fcf02=UnknownStruct56.from_json(data['unknown_struct56_0x287fcf02']),
            unknown_struct192=UnknownStruct192.from_json(data['unknown_struct192']),
        )

    def to_json(self) -> dict:
        return {
            'texture': self.texture,
            'health': self.health,
            'unknown_struct56_0x02eb59dc': self.unknown_struct56_0x02eb59dc.to_json(),
            'unknown_struct56_0xf0bcb424': self.unknown_struct56_0xf0bcb424.to_json(),
            'unknown_struct56_0x17a112b3': self.unknown_struct56_0x17a112b3.to_json(),
            'unknown_struct56_0xcf626995': self.unknown_struct56_0xcf626995.to_json(),
            'unknown_struct56_0x287fcf02': self.unknown_struct56_0x287fcf02.to_json(),
            'unknown_struct192': self.unknown_struct192.to_json(),
        }


def _decode_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct56_0x02eb59dc(data: typing.BinaryIO, property_size: int):
    return UnknownStruct56.from_stream(data, property_size)


def _decode_unknown_struct56_0xf0bcb424(data: typing.BinaryIO, property_size: int):
    return UnknownStruct56.from_stream(data, property_size)


def _decode_unknown_struct56_0x17a112b3(data: typing.BinaryIO, property_size: int):
    return UnknownStruct56.from_stream(data, property_size)


def _decode_unknown_struct56_0xcf626995(data: typing.BinaryIO, property_size: int):
    return UnknownStruct56.from_stream(data, property_size)


def _decode_unknown_struct56_0x287fcf02(data: typing.BinaryIO, property_size: int):
    return UnknownStruct56.from_stream(data, property_size)


def _decode_unknown_struct192(data: typing.BinaryIO, property_size: int):
    return UnknownStruct192.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd1f65872: ('texture', _decode_texture),
    0xf0668919: ('health', _decode_health),
    0x2eb59dc: ('unknown_struct56_0x02eb59dc', _decode_unknown_struct56_0x02eb59dc),
    0xf0bcb424: ('unknown_struct56_0xf0bcb424', _decode_unknown_struct56_0xf0bcb424),
    0x17a112b3: ('unknown_struct56_0x17a112b3', _decode_unknown_struct56_0x17a112b3),
    0xcf626995: ('unknown_struct56_0xcf626995', _decode_unknown_struct56_0xcf626995),
    0x287fcf02: ('unknown_struct56_0x287fcf02', _decode_unknown_struct56_0x287fcf02),
    0x72544afd: ('unknown_struct192', _decode_unknown_struct192),
}
