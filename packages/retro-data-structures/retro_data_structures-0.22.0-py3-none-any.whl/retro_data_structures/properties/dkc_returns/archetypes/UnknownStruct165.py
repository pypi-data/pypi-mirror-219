# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct165(BaseProperty):
    gui_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    unknown_0xe9ae9114: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_0x8f321be8: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    core_text_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_0xc022b7a6: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_0xcc4eb20d: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    background_sound: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        if default_override is None and (result := _fast_decode(data, property_count)) is not None:
            return result

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
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\xe9\xae\x91\x14')  # 0xe9ae9114
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xe9ae9114))

        data.write(b'\x8f2\x1b\xe8')  # 0x8f321be8
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x8f321be8))

        data.write(b'\xe7W d')  # 0xe7572064
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.core_text_string))

        data.write(b'\xc0"\xb7\xa6')  # 0xc022b7a6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xc022b7a6))

        data.write(b'\xccN\xb2\r')  # 0xcc4eb20d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0xcc4eb20d))

        data.write(b'\xf7\xe6u\xfe')  # 0xf7e675fe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.background_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gui_frame=data['gui_frame'],
            unknown_0xe9ae9114=data['unknown_0xe9ae9114'],
            unknown_0x8f321be8=data['unknown_0x8f321be8'],
            core_text_string=data['core_text_string'],
            unknown_0xc022b7a6=data['unknown_0xc022b7a6'],
            unknown_0xcc4eb20d=data['unknown_0xcc4eb20d'],
            background_sound=data['background_sound'],
        )

    def to_json(self) -> dict:
        return {
            'gui_frame': self.gui_frame,
            'unknown_0xe9ae9114': self.unknown_0xe9ae9114,
            'unknown_0x8f321be8': self.unknown_0x8f321be8,
            'core_text_string': self.core_text_string,
            'unknown_0xc022b7a6': self.unknown_0xc022b7a6,
            'unknown_0xcc4eb20d': self.unknown_0xcc4eb20d,
            'background_sound': self.background_sound,
        }


_FAST_FORMAT = None
_FAST_IDS = (0x806052cb, 0xe9ae9114, 0x8f321be8, 0xe7572064, 0xc022b7a6, 0xcc4eb20d, 0xf7e675fe)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct165]:
    if property_count != 7:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQLHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(98))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct165(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
    )


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xe9ae9114(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x8f321be8(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_core_text_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xc022b7a6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0xcc4eb20d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_background_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0xe9ae9114: ('unknown_0xe9ae9114', _decode_unknown_0xe9ae9114),
    0x8f321be8: ('unknown_0x8f321be8', _decode_unknown_0x8f321be8),
    0xe7572064: ('core_text_string', _decode_core_text_string),
    0xc022b7a6: ('unknown_0xc022b7a6', _decode_unknown_0xc022b7a6),
    0xcc4eb20d: ('unknown_0xcc4eb20d', _decode_unknown_0xcc4eb20d),
    0xf7e675fe: ('background_sound', _decode_background_sound),
}
