# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct28(BaseProperty):
    hud_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    appear_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    no_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    yes_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    animated_appear: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x0c9c9c3b: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    caud_0x6a6aa42e: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    animated_disappear: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    no: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    no_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    yes: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    yes_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    ok: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    ok_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_struct26: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b'\xc0,#O')  # 0xc02c234f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.appear_sound))

        data.write(b"'|\x04\xff")  # 0x277c04ff
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no_sound))

        data.write(b'\x10\x8d\x90q')  # 0x108d9071
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.yes_sound))

        data.write(b'u\xach<')  # 0x75ac683c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.animated_appear))

        data.write(b'\x0c\x9c\x9c;')  # 0xc9c9c3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x0c9c9c3b))

        data.write(b'jj\xa4.')  # 0x6a6aa42e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud_0x6a6aa42e))

        data.write(b'\x07\x8c\x81\x9f')  # 0x78c819f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.animated_disappear))

        data.write(b'K\x88>k')  # 0x4b883e6b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no))

        data.write(b'9=\\x')  # 0x393d5c78
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.no_core))

        data.write(b'@\x01y\x17')  # 0x40017917
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.yes))

        data.write(b'\x10\x92"\x93')  # 0x10922293
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.yes_core))

        data.write(b'vnw\xc9')  # 0x766e77c9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ok))

        data.write(b'\xf1X#\xc2')  # 0xf15823c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ok_core))

        data.write(b'jY\x8a\x9b')  # 0x6a598a9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hud_frame=data['hud_frame'],
            appear_sound=data['appear_sound'],
            no_sound=data['no_sound'],
            yes_sound=data['yes_sound'],
            animated_appear=data['animated_appear'],
            caud_0x0c9c9c3b=data['caud_0x0c9c9c3b'],
            caud_0x6a6aa42e=data['caud_0x6a6aa42e'],
            animated_disappear=data['animated_disappear'],
            no=data['no'],
            no_core=data['no_core'],
            yes=data['yes'],
            yes_core=data['yes_core'],
            ok=data['ok'],
            ok_core=data['ok_core'],
            unknown_struct26=UnknownStruct26.from_json(data['unknown_struct26']),
        )

    def to_json(self) -> dict:
        return {
            'hud_frame': self.hud_frame,
            'appear_sound': self.appear_sound,
            'no_sound': self.no_sound,
            'yes_sound': self.yes_sound,
            'animated_appear': self.animated_appear,
            'caud_0x0c9c9c3b': self.caud_0x0c9c9c3b,
            'caud_0x6a6aa42e': self.caud_0x6a6aa42e,
            'animated_disappear': self.animated_disappear,
            'no': self.no,
            'no_core': self.no_core,
            'yes': self.yes,
            'yes_core': self.yes_core,
            'ok': self.ok,
            'ok_core': self.ok_core,
            'unknown_struct26': self.unknown_struct26.to_json(),
        }


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_appear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_no_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_yes_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animated_appear(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x0c9c9c3b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud_0x6a6aa42e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_animated_disappear(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_no(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_no_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_yes(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_yes_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ok(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ok_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct26(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0xc02c234f: ('appear_sound', _decode_appear_sound),
    0x277c04ff: ('no_sound', _decode_no_sound),
    0x108d9071: ('yes_sound', _decode_yes_sound),
    0x75ac683c: ('animated_appear', _decode_animated_appear),
    0xc9c9c3b: ('caud_0x0c9c9c3b', _decode_caud_0x0c9c9c3b),
    0x6a6aa42e: ('caud_0x6a6aa42e', _decode_caud_0x6a6aa42e),
    0x78c819f: ('animated_disappear', _decode_animated_disappear),
    0x4b883e6b: ('no', _decode_no),
    0x393d5c78: ('no_core', _decode_no_core),
    0x40017917: ('yes', _decode_yes),
    0x10922293: ('yes_core', _decode_yes_core),
    0x766e77c9: ('ok', _decode_ok),
    0xf15823c2: ('ok_core', _decode_ok_core),
    0x6a598a9b: ('unknown_struct26', _decode_unknown_struct26),
}
