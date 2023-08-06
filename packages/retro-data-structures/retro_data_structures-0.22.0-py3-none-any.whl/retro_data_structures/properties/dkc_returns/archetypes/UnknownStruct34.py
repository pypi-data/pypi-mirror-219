# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct34(BaseProperty):
    hud_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    appear_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    disappear_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    change_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    string_table: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)

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
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xf2)\x9e\xd6')  # 0xf2299ed6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hud_frame))

        data.write(b'\xc0,#O')  # 0xc02c234f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.appear_sound))

        data.write(b'm&~\x88')  # 0x6d267e88
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.disappear_sound))

        data.write(b'\xb8\xe3C\xf5')  # 0xb8e343f5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.change_sound))

        data.write(b'\xfd\x95\xed*')  # 0xfd95ed2a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.string_table))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hud_frame=data['hud_frame'],
            appear_sound=data['appear_sound'],
            disappear_sound=data['disappear_sound'],
            change_sound=data['change_sound'],
            string_table=data['string_table'],
        )

    def to_json(self) -> dict:
        return {
            'hud_frame': self.hud_frame,
            'appear_sound': self.appear_sound,
            'disappear_sound': self.disappear_sound,
            'change_sound': self.change_sound,
            'string_table': self.string_table,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xf2299ed6, 0xc02c234f, 0x6d267e88, 0xb8e343f5, 0xfd95ed2a)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct34]:
    if property_count != 5:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(70))
    if (dec[0], dec[3], dec[6], dec[9], dec[12]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct34(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
    )


def _decode_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_appear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_disappear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_change_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_string_table(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf2299ed6: ('hud_frame', _decode_hud_frame),
    0xc02c234f: ('appear_sound', _decode_appear_sound),
    0x6d267e88: ('disappear_sound', _decode_disappear_sound),
    0xb8e343f5: ('change_sound', _decode_change_sound),
    0xfd95ed2a: ('string_table', _decode_string_table),
}
