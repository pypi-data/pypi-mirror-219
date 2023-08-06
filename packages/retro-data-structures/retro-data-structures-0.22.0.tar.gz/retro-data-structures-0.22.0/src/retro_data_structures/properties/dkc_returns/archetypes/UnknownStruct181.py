# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct181(BaseProperty):
    hud_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27)
    unknown_struct28_0x67a7c770: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
    unknown_struct28_0xc68bc9ec: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
    unknown_0x9be6a5d6: float = dataclasses.field(default=5.0)
    comment_delay: float = dataclasses.field(default=10.0)
    comment_duration: float = dataclasses.field(default=10.0)
    unknown_0xf34d7c81: int = dataclasses.field(default=3)
    input_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0xabc01c18: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    first_entry_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    first_exit_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    generic_entry_strings: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    generic_exit_strings: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x7f2a409c: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    failed_key_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    failed_capacity_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    coin_icon_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    exit_confirm: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    select: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD', 'STRG']}, default=default_asset_id)
    select_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    return_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg_0x9c31d707: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)

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
        data.write(b'\x00\x17')  # 23 properties

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g\xa7\xc7p')  # 0x67a7c770
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0x67a7c770.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x8b\xc9\xec')  # 0xc68bc9ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0xc68bc9ec.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\xe6\xa5\xd6')  # 0x9be6a5d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9be6a5d6))

        data.write(b'\x9e\xbe\x81-')  # 0x9ebe812d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.comment_delay))

        data.write(b'S\x1f\x1c\xe0')  # 0x531f1ce0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.comment_duration))

        data.write(b'\xf3M|\x81')  # 0xf34d7c81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xf34d7c81))

        data.write(b' \x0e\xbc^')  # 0x200ebc5e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.input_string))

        data.write(b'\xab\xc0\x1c\x18')  # 0xabc01c18
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xabc01c18))

        data.write(b'=\xaf;j')  # 0x3daf3b6a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.first_entry_string))

        data.write(b'\x8fa\xa2U')  # 0x8f61a255
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.first_exit_string))

        data.write(b'\xc2_.\x19')  # 0xc25f2e19
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.generic_entry_strings))

        data.write(b'p\xcc\xa1-')  # 0x70cca12d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.generic_exit_strings))

        data.write(b'\x7f*@\x9c')  # 0x7f2a409c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x7f2a409c))

        data.write(b'.\xb4\xa9\r')  # 0x2eb4a90d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.failed_key_string))

        data.write(b'\x89\x1at\x1f')  # 0x891a741f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.failed_capacity_string))

        data.write(b'p\xa2\x85T')  # 0x70a28554
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.coin_icon_string))

        data.write(b'vB\xefR')  # 0x7642ef52
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.exit_confirm))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'\xa4\rA\x0e')  # 0xa40d410e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_core))

        data.write(b'\x95\x85\xb5\x87')  # 0x9585b587
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.return_text))

        data.write(b'\x9c1\xd7\x07')  # 0x9c31d707
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x9c31d707))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hud_frame=data['hud_frame'],
            unknown_struct27=UnknownStruct27.from_json(data['unknown_struct27']),
            unknown_struct28_0x67a7c770=UnknownStruct28.from_json(data['unknown_struct28_0x67a7c770']),
            unknown_struct28_0xc68bc9ec=UnknownStruct28.from_json(data['unknown_struct28_0xc68bc9ec']),
            unknown_0x9be6a5d6=data['unknown_0x9be6a5d6'],
            comment_delay=data['comment_delay'],
            comment_duration=data['comment_duration'],
            unknown_0xf34d7c81=data['unknown_0xf34d7c81'],
            input_string=data['input_string'],
            strg_0xabc01c18=data['strg_0xabc01c18'],
            first_entry_string=data['first_entry_string'],
            first_exit_string=data['first_exit_string'],
            generic_entry_strings=data['generic_entry_strings'],
            generic_exit_strings=data['generic_exit_strings'],
            strg_0x7f2a409c=data['strg_0x7f2a409c'],
            failed_key_string=data['failed_key_string'],
            failed_capacity_string=data['failed_capacity_string'],
            coin_icon_string=data['coin_icon_string'],
            exit_confirm=data['exit_confirm'],
            select=data['select'],
            select_core=data['select_core'],
            return_text=data['return_text'],
            strg_0x9c31d707=data['strg_0x9c31d707'],
        )

    def to_json(self) -> dict:
        return {
            'hud_frame': self.hud_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'unknown_struct28_0x67a7c770': self.unknown_struct28_0x67a7c770.to_json(),
            'unknown_struct28_0xc68bc9ec': self.unknown_struct28_0xc68bc9ec.to_json(),
            'unknown_0x9be6a5d6': self.unknown_0x9be6a5d6,
            'comment_delay': self.comment_delay,
            'comment_duration': self.comment_duration,
            'unknown_0xf34d7c81': self.unknown_0xf34d7c81,
            'input_string': self.input_string,
            'strg_0xabc01c18': self.strg_0xabc01c18,
            'first_entry_string': self.first_entry_string,
            'first_exit_string': self.first_exit_string,
            'generic_entry_strings': self.generic_entry_strings,
            'generic_exit_strings': self.generic_exit_strings,
            'strg_0x7f2a409c': self.strg_0x7f2a409c,
            'failed_key_string': self.failed_key_string,
            'failed_capacity_string': self.failed_capacity_string,
            'coin_icon_string': self.coin_icon_string,
            'exit_confirm': self.exit_confirm,
            'select': self.select,
            'select_core': self.select_core,
            'return_text': self.return_text,
            'strg_0x9c31d707': self.strg_0x9c31d707,
        }


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct27(data: typing.BinaryIO, property_size: int):
    return UnknownStruct27.from_stream(data, property_size)


def _decode_unknown_struct28_0x67a7c770(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_unknown_struct28_0xc68bc9ec(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_unknown_0x9be6a5d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_comment_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_comment_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf34d7c81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_input_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xabc01c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_first_entry_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_first_exit_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_generic_entry_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_generic_exit_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x7f2a409c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_failed_key_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_failed_capacity_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_coin_icon_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_exit_confirm(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x9c31d707(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0x73e2819b: ('unknown_struct27', _decode_unknown_struct27),
    0x67a7c770: ('unknown_struct28_0x67a7c770', _decode_unknown_struct28_0x67a7c770),
    0xc68bc9ec: ('unknown_struct28_0xc68bc9ec', _decode_unknown_struct28_0xc68bc9ec),
    0x9be6a5d6: ('unknown_0x9be6a5d6', _decode_unknown_0x9be6a5d6),
    0x9ebe812d: ('comment_delay', _decode_comment_delay),
    0x531f1ce0: ('comment_duration', _decode_comment_duration),
    0xf34d7c81: ('unknown_0xf34d7c81', _decode_unknown_0xf34d7c81),
    0x200ebc5e: ('input_string', _decode_input_string),
    0xabc01c18: ('strg_0xabc01c18', _decode_strg_0xabc01c18),
    0x3daf3b6a: ('first_entry_string', _decode_first_entry_string),
    0x8f61a255: ('first_exit_string', _decode_first_exit_string),
    0xc25f2e19: ('generic_entry_strings', _decode_generic_entry_strings),
    0x70cca12d: ('generic_exit_strings', _decode_generic_exit_strings),
    0x7f2a409c: ('strg_0x7f2a409c', _decode_strg_0x7f2a409c),
    0x2eb4a90d: ('failed_key_string', _decode_failed_key_string),
    0x891a741f: ('failed_capacity_string', _decode_failed_capacity_string),
    0x70a28554: ('coin_icon_string', _decode_coin_icon_string),
    0x7642ef52: ('exit_confirm', _decode_exit_confirm),
    0x8ed65283: ('select', _decode_select),
    0xa40d410e: ('select_core', _decode_select_core),
    0x9585b587: ('return_text', _decode_return_text),
    0x9c31d707: ('strg_0x9c31d707', _decode_strg_0x9c31d707),
}
