# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct167(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29)
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27)
    strg: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    title: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    select: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD', 'STRG']}, default=default_asset_id)
    caud_0x7b084ab6: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    select_diddy_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    select_shield_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    select_heart_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0xa0c913a9: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'D\xf5u\x07')  # 0x44f57507
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x011\x80\xf0')  # 0x13180f0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'{\x08J\xb6')  # 0x7b084ab6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x7b084ab6))

        data.write(b'fg\xc9\xb1')  # 0x6667c9b1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_diddy_sound))

        data.write(b'y\xd4P\xb1')  # 0x79d450b1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_shield_sound))

        data.write(b'<\xf9Gp')  # 0x3cf94770
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_heart_sound))

        data.write(b'\xa0\xc9\x13\xa9')  # 0xa0c913a9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0xa0c913a9))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct29=UnknownStruct29.from_json(data['unknown_struct29']),
            unknown_struct27=UnknownStruct27.from_json(data['unknown_struct27']),
            strg=data['strg'],
            title=data['title'],
            back=data['back'],
            select=data['select'],
            caud_0x7b084ab6=data['caud_0x7b084ab6'],
            select_diddy_sound=data['select_diddy_sound'],
            select_shield_sound=data['select_shield_sound'],
            select_heart_sound=data['select_heart_sound'],
            caud_0xa0c913a9=data['caud_0xa0c913a9'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'unknown_struct27': self.unknown_struct27.to_json(),
            'strg': self.strg,
            'title': self.title,
            'back': self.back,
            'select': self.select,
            'caud_0x7b084ab6': self.caud_0x7b084ab6,
            'select_diddy_sound': self.select_diddy_sound,
            'select_shield_sound': self.select_shield_sound,
            'select_heart_sound': self.select_heart_sound,
            'caud_0xa0c913a9': self.caud_0xa0c913a9,
        }


def _decode_unknown_struct29(data: typing.BinaryIO, property_size: int):
    return UnknownStruct29.from_stream(data, property_size)


def _decode_unknown_struct27(data: typing.BinaryIO, property_size: int):
    return UnknownStruct27.from_stream(data, property_size)


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x7b084ab6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_diddy_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_shield_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_heart_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0xa0c913a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x44f57507: ('unknown_struct29', _decode_unknown_struct29),
    0x73e2819b: ('unknown_struct27', _decode_unknown_struct27),
    0x13180f0: ('strg', _decode_strg),
    0xa4f20c17: ('title', _decode_title),
    0xe9336455: ('back', _decode_back),
    0x8ed65283: ('select', _decode_select),
    0x7b084ab6: ('caud_0x7b084ab6', _decode_caud_0x7b084ab6),
    0x6667c9b1: ('select_diddy_sound', _decode_select_diddy_sound),
    0x79d450b1: ('select_shield_sound', _decode_select_shield_sound),
    0x3cf94770: ('select_heart_sound', _decode_select_heart_sound),
    0xa0c913a9: ('caud_0xa0c913a9', _decode_caud_0xa0c913a9),
}
