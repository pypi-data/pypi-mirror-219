# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct166(BaseProperty):
    gui_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    freelook_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    freelook_prompt_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0xe8ac748d: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0xfebbc04e: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x5eeb7f9d: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0xcbc01154: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x777cf37f: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x66b1160b: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x7f1e6dec: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    cancel_prompt_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x6b016db2: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    select: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD', 'STRG']}, default=default_asset_id)
    select_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    menu: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    menu_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27)
    text_background: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)

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

        data.write(b'\xf5\xcb\x9f2')  # 0xf5cb9f32
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.freelook_text))

        data.write(b'!\xcb-\x81')  # 0x21cb2d81
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.freelook_prompt_text))

        data.write(b'\xe8\xact\x8d')  # 0xe8ac748d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xe8ac748d))

        data.write(b'\xfe\xbb\xc0N')  # 0xfebbc04e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xfebbc04e))

        data.write(b'^\xeb\x7f\x9d')  # 0x5eeb7f9d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x5eeb7f9d))

        data.write(b'\xcb\xc0\x11T')  # 0xcbc01154
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xcbc01154))

        data.write(b'w|\xf3\x7f')  # 0x777cf37f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x777cf37f))

        data.write(b'f\xb1\x16\x0b')  # 0x66b1160b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x66b1160b))

        data.write(b'\x7f\x1em\xec')  # 0x7f1e6dec
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x7f1e6dec))

        data.write(b'\xb7\x99\x06Q')  # 0xb7990651
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cancel_prompt_text))

        data.write(b'k\x01m\xb2')  # 0x6b016db2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x6b016db2))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'\xa4\rA\x0e')  # 0xa40d410e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_core))

        data.write(b'\xea\xcb\xa7U')  # 0xeacba755
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.menu))

        data.write(b'\xa1\x8e\xdf-')  # 0xa18edf2d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.menu_core))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gui_frame=data['gui_frame'],
            freelook_text=data['freelook_text'],
            freelook_prompt_text=data['freelook_prompt_text'],
            strg_0xe8ac748d=data['strg_0xe8ac748d'],
            strg_0xfebbc04e=data['strg_0xfebbc04e'],
            strg_0x5eeb7f9d=data['strg_0x5eeb7f9d'],
            strg_0xcbc01154=data['strg_0xcbc01154'],
            strg_0x777cf37f=data['strg_0x777cf37f'],
            strg_0x66b1160b=data['strg_0x66b1160b'],
            strg_0x7f1e6dec=data['strg_0x7f1e6dec'],
            cancel_prompt_text=data['cancel_prompt_text'],
            strg_0x6b016db2=data['strg_0x6b016db2'],
            select=data['select'],
            select_core=data['select_core'],
            menu=data['menu'],
            menu_core=data['menu_core'],
            unknown_struct27=UnknownStruct27.from_json(data['unknown_struct27']),
            text_background=data['text_background'],
        )

    def to_json(self) -> dict:
        return {
            'gui_frame': self.gui_frame,
            'freelook_text': self.freelook_text,
            'freelook_prompt_text': self.freelook_prompt_text,
            'strg_0xe8ac748d': self.strg_0xe8ac748d,
            'strg_0xfebbc04e': self.strg_0xfebbc04e,
            'strg_0x5eeb7f9d': self.strg_0x5eeb7f9d,
            'strg_0xcbc01154': self.strg_0xcbc01154,
            'strg_0x777cf37f': self.strg_0x777cf37f,
            'strg_0x66b1160b': self.strg_0x66b1160b,
            'strg_0x7f1e6dec': self.strg_0x7f1e6dec,
            'cancel_prompt_text': self.cancel_prompt_text,
            'strg_0x6b016db2': self.strg_0x6b016db2,
            'select': self.select,
            'select_core': self.select_core,
            'menu': self.menu,
            'menu_core': self.menu_core,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'text_background': self.text_background,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_freelook_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_freelook_prompt_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xe8ac748d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xfebbc04e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x5eeb7f9d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xcbc01154(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x777cf37f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x66b1160b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x7f1e6dec(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cancel_prompt_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x6b016db2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_menu(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_menu_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct27(data: typing.BinaryIO, property_size: int):
    return UnknownStruct27.from_stream(data, property_size)


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0xf5cb9f32: ('freelook_text', _decode_freelook_text),
    0x21cb2d81: ('freelook_prompt_text', _decode_freelook_prompt_text),
    0xe8ac748d: ('strg_0xe8ac748d', _decode_strg_0xe8ac748d),
    0xfebbc04e: ('strg_0xfebbc04e', _decode_strg_0xfebbc04e),
    0x5eeb7f9d: ('strg_0x5eeb7f9d', _decode_strg_0x5eeb7f9d),
    0xcbc01154: ('strg_0xcbc01154', _decode_strg_0xcbc01154),
    0x777cf37f: ('strg_0x777cf37f', _decode_strg_0x777cf37f),
    0x66b1160b: ('strg_0x66b1160b', _decode_strg_0x66b1160b),
    0x7f1e6dec: ('strg_0x7f1e6dec', _decode_strg_0x7f1e6dec),
    0xb7990651: ('cancel_prompt_text', _decode_cancel_prompt_text),
    0x6b016db2: ('strg_0x6b016db2', _decode_strg_0x6b016db2),
    0x8ed65283: ('select', _decode_select),
    0xa40d410e: ('select_core', _decode_select_core),
    0xeacba755: ('menu', _decode_menu),
    0xa18edf2d: ('menu_core', _decode_menu_core),
    0x73e2819b: ('unknown_struct27', _decode_unknown_struct27),
    0xe119319b: ('text_background', _decode_text_background),
}
