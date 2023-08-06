# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct154 import UnknownStruct154
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct155 import UnknownStruct155
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct156(BaseProperty):
    gui_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    title_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unlock_concept_art: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unlock_music: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unlock_diorama: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    continue_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    core_continue_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    retry_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    core_retry_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    retry_confirm_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x8ae3361b: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x8416a311: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_struct154: UnknownStruct154 = dataclasses.field(default_factory=UnknownStruct154)
    unknown_struct155: UnknownStruct155 = dataclasses.field(default_factory=UnknownStruct155)
    unknown_struct26_0x860139ad: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x6a598a9b: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x3be205da: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    unknown_struct26_0x96cd80d1: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)

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
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\xef\xc5\xa17')  # 0xefc5a137
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title_text))

        data.write(b'yX\x9b\xf4')  # 0x79589bf4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_concept_art))

        data.write(b'\n\xf7\x07\xdf')  # 0xaf707df
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_music))

        data.write(b'\\\xe2\xa9\xa9')  # 0x5ce2a9a9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unlock_diorama))

        data.write(b"\x1f['\x1d")  # 0x1f5b271d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.continue_text))

        data.write(b'D\x9fRu')  # 0x449f5275
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.core_continue_text))

        data.write(b'L\xaf\xdd\xd1')  # 0x4cafddd1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.retry_text))

        data.write(b'6\x1c\xcf\x90')  # 0x361ccf90
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.core_retry_text))

        data.write(b'J\\\xb6\xef')  # 0x4a5cb6ef
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.retry_confirm_text))

        data.write(b'\x8a\xe36\x1b')  # 0x8ae3361b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x8ae3361b))

        data.write(b'\x84\x16\xa3\x11')  # 0x8416a311
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x8416a311))

        data.write(b'\xf0\xa3\x97\x8e')  # 0xf0a3978e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct154.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0b\xdeR\x16')  # 0xbde5216
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct155.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86\x019\xad')  # 0x860139ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x860139ad.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'jY\x8a\x9b')  # 0x6a598a9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x6a598a9b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b';\xe2\x05\xda')  # 0x3be205da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x3be205da.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x96\xcd\x80\xd1')  # 0x96cd80d1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x96cd80d1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gui_frame=data['gui_frame'],
            title_text=data['title_text'],
            unlock_concept_art=data['unlock_concept_art'],
            unlock_music=data['unlock_music'],
            unlock_diorama=data['unlock_diorama'],
            continue_text=data['continue_text'],
            core_continue_text=data['core_continue_text'],
            retry_text=data['retry_text'],
            core_retry_text=data['core_retry_text'],
            retry_confirm_text=data['retry_confirm_text'],
            strg_0x8ae3361b=data['strg_0x8ae3361b'],
            strg_0x8416a311=data['strg_0x8416a311'],
            unknown_struct154=UnknownStruct154.from_json(data['unknown_struct154']),
            unknown_struct155=UnknownStruct155.from_json(data['unknown_struct155']),
            unknown_struct26_0x860139ad=UnknownStruct26.from_json(data['unknown_struct26_0x860139ad']),
            unknown_struct26_0x6a598a9b=UnknownStruct26.from_json(data['unknown_struct26_0x6a598a9b']),
            unknown_struct26_0x3be205da=UnknownStruct26.from_json(data['unknown_struct26_0x3be205da']),
            unknown_struct26_0x96cd80d1=UnknownStruct26.from_json(data['unknown_struct26_0x96cd80d1']),
        )

    def to_json(self) -> dict:
        return {
            'gui_frame': self.gui_frame,
            'title_text': self.title_text,
            'unlock_concept_art': self.unlock_concept_art,
            'unlock_music': self.unlock_music,
            'unlock_diorama': self.unlock_diorama,
            'continue_text': self.continue_text,
            'core_continue_text': self.core_continue_text,
            'retry_text': self.retry_text,
            'core_retry_text': self.core_retry_text,
            'retry_confirm_text': self.retry_confirm_text,
            'strg_0x8ae3361b': self.strg_0x8ae3361b,
            'strg_0x8416a311': self.strg_0x8416a311,
            'unknown_struct154': self.unknown_struct154.to_json(),
            'unknown_struct155': self.unknown_struct155.to_json(),
            'unknown_struct26_0x860139ad': self.unknown_struct26_0x860139ad.to_json(),
            'unknown_struct26_0x6a598a9b': self.unknown_struct26_0x6a598a9b.to_json(),
            'unknown_struct26_0x3be205da': self.unknown_struct26_0x3be205da.to_json(),
            'unknown_struct26_0x96cd80d1': self.unknown_struct26_0x96cd80d1.to_json(),
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_concept_art(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unlock_diorama(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_continue_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_core_continue_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_retry_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_core_retry_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_retry_confirm_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x8ae3361b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x8416a311(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct154(data: typing.BinaryIO, property_size: int):
    return UnknownStruct154.from_stream(data, property_size)


def _decode_unknown_struct155(data: typing.BinaryIO, property_size: int):
    return UnknownStruct155.from_stream(data, property_size)


def _decode_unknown_struct26_0x860139ad(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x6a598a9b(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x3be205da(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_unknown_struct26_0x96cd80d1(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0xefc5a137: ('title_text', _decode_title_text),
    0x79589bf4: ('unlock_concept_art', _decode_unlock_concept_art),
    0xaf707df: ('unlock_music', _decode_unlock_music),
    0x5ce2a9a9: ('unlock_diorama', _decode_unlock_diorama),
    0x1f5b271d: ('continue_text', _decode_continue_text),
    0x449f5275: ('core_continue_text', _decode_core_continue_text),
    0x4cafddd1: ('retry_text', _decode_retry_text),
    0x361ccf90: ('core_retry_text', _decode_core_retry_text),
    0x4a5cb6ef: ('retry_confirm_text', _decode_retry_confirm_text),
    0x8ae3361b: ('strg_0x8ae3361b', _decode_strg_0x8ae3361b),
    0x8416a311: ('strg_0x8416a311', _decode_strg_0x8416a311),
    0xf0a3978e: ('unknown_struct154', _decode_unknown_struct154),
    0xbde5216: ('unknown_struct155', _decode_unknown_struct155),
    0x860139ad: ('unknown_struct26_0x860139ad', _decode_unknown_struct26_0x860139ad),
    0x6a598a9b: ('unknown_struct26_0x6a598a9b', _decode_unknown_struct26_0x6a598a9b),
    0x3be205da: ('unknown_struct26_0x3be205da', _decode_unknown_struct26_0x3be205da),
    0x96cd80d1: ('unknown_struct26_0x96cd80d1', _decode_unknown_struct26_0x96cd80d1),
}
