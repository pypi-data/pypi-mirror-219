# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct30 import UnknownStruct30
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct31 import UnknownStruct31
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct148(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29)
    title: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    audio: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    controllers: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_struct31: UnknownStruct31 = dataclasses.field(default_factory=UnknownStruct31)
    unknown_struct30: UnknownStruct30 = dataclasses.field(default_factory=UnknownStruct30)

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

        data.write(b'0[22')  # 0x305b3232
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'\xa0\x99\xca4')  # 0xa099ca34
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.audio))

        data.write(b'\xefY\xeaO')  # 0xef59ea4f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.controllers))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'\x07\xba\xa1\x1b')  # 0x7baa11b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct31.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcb/\xf7\x02')  # 0xcb2ff702
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct30.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct29=UnknownStruct29.from_json(data['unknown_struct29']),
            title=data['title'],
            audio=data['audio'],
            controllers=data['controllers'],
            back=data['back'],
            back_core=data['back_core'],
            unknown_struct31=UnknownStruct31.from_json(data['unknown_struct31']),
            unknown_struct30=UnknownStruct30.from_json(data['unknown_struct30']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'title': self.title,
            'audio': self.audio,
            'controllers': self.controllers,
            'back': self.back,
            'back_core': self.back_core,
            'unknown_struct31': self.unknown_struct31.to_json(),
            'unknown_struct30': self.unknown_struct30.to_json(),
        }


def _decode_unknown_struct29(data: typing.BinaryIO, property_size: int):
    return UnknownStruct29.from_stream(data, property_size)


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_audio(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_controllers(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct31(data: typing.BinaryIO, property_size: int):
    return UnknownStruct31.from_stream(data, property_size)


def _decode_unknown_struct30(data: typing.BinaryIO, property_size: int):
    return UnknownStruct30.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x305b3232: ('unknown_struct29', _decode_unknown_struct29),
    0xa4f20c17: ('title', _decode_title),
    0xa099ca34: ('audio', _decode_audio),
    0xef59ea4f: ('controllers', _decode_controllers),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0x7baa11b: ('unknown_struct31', _decode_unknown_struct31),
    0xcb2ff702: ('unknown_struct30', _decode_unknown_struct30),
}
