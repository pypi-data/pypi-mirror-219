# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct31(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29)
    title: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    music: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    sound_fx: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    left_arrow: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    right_arrow: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    left_arrow_pressed: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    right_arrow_pressed: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    appear_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    disappear_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    in_place_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    up_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    down_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    cancel_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    inc_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    dec_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    error_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
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
        data.write(b'\x00\x14')  # 20 properties

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

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'\xbb\x19\xd2\xf3')  # 0xbb19d2f3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.music))

        data.write(b'\xdf\x08\x0e\xa1')  # 0xdf080ea1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.sound_fx))

        data.write(b'1L\xdc$')  # 0x314cdc24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_arrow))

        data.write(b'\xd1\x91\x83G')  # 0xd1918347
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_arrow))

        data.write(b'\xb4Q\x0e\xfe')  # 0xb4510efe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_arrow_pressed))

        data.write(b'T\xcd\x18t')  # 0x54cd1874
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_arrow_pressed))

        data.write(b'\xc0,#O')  # 0xc02c234f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.appear_sound))

        data.write(b'm&~\x88')  # 0x6d267e88
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.disappear_sound))

        data.write(b'/\x90\xd2W')  # 0x2f90d257
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.in_place_sound))

        data.write(b'g\xf8}\x00')  # 0x67f87d00
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.up_sound))

        data.write(b'\xb4\x8a\x1f\x83')  # 0xb48a1f83
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.down_sound))

        data.write(b'H_ \x08')  # 0x485f2008
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cancel_sound))

        data.write(b'{\xeeVn')  # 0x7bee566e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.inc_sound))

        data.write(b'MP\x92\x1e')  # 0x4d50921e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dec_sound))

        data.write(b'EY\xa4\xfd')  # 0x4559a4fd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.error_sound))

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct29=UnknownStruct29.from_json(data['unknown_struct29']),
            title=data['title'],
            back=data['back'],
            back_core=data['back_core'],
            music=data['music'],
            sound_fx=data['sound_fx'],
            left_arrow=data['left_arrow'],
            right_arrow=data['right_arrow'],
            left_arrow_pressed=data['left_arrow_pressed'],
            right_arrow_pressed=data['right_arrow_pressed'],
            appear_sound=data['appear_sound'],
            disappear_sound=data['disappear_sound'],
            in_place_sound=data['in_place_sound'],
            up_sound=data['up_sound'],
            down_sound=data['down_sound'],
            cancel_sound=data['cancel_sound'],
            inc_sound=data['inc_sound'],
            dec_sound=data['dec_sound'],
            error_sound=data['error_sound'],
            text_background=data['text_background'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'title': self.title,
            'back': self.back,
            'back_core': self.back_core,
            'music': self.music,
            'sound_fx': self.sound_fx,
            'left_arrow': self.left_arrow,
            'right_arrow': self.right_arrow,
            'left_arrow_pressed': self.left_arrow_pressed,
            'right_arrow_pressed': self.right_arrow_pressed,
            'appear_sound': self.appear_sound,
            'disappear_sound': self.disappear_sound,
            'in_place_sound': self.in_place_sound,
            'up_sound': self.up_sound,
            'down_sound': self.down_sound,
            'cancel_sound': self.cancel_sound,
            'inc_sound': self.inc_sound,
            'dec_sound': self.dec_sound,
            'error_sound': self.error_sound,
            'text_background': self.text_background,
        }


def _decode_unknown_struct29(data: typing.BinaryIO, property_size: int):
    return UnknownStruct29.from_stream(data, property_size)


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_music(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sound_fx(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_appear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_disappear_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_in_place_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_up_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_down_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cancel_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_inc_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dec_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_error_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x305b3232: ('unknown_struct29', _decode_unknown_struct29),
    0xa4f20c17: ('title', _decode_title),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0xbb19d2f3: ('music', _decode_music),
    0xdf080ea1: ('sound_fx', _decode_sound_fx),
    0x314cdc24: ('left_arrow', _decode_left_arrow),
    0xd1918347: ('right_arrow', _decode_right_arrow),
    0xb4510efe: ('left_arrow_pressed', _decode_left_arrow_pressed),
    0x54cd1874: ('right_arrow_pressed', _decode_right_arrow_pressed),
    0xc02c234f: ('appear_sound', _decode_appear_sound),
    0x6d267e88: ('disappear_sound', _decode_disappear_sound),
    0x2f90d257: ('in_place_sound', _decode_in_place_sound),
    0x67f87d00: ('up_sound', _decode_up_sound),
    0xb48a1f83: ('down_sound', _decode_down_sound),
    0x485f2008: ('cancel_sound', _decode_cancel_sound),
    0x7bee566e: ('inc_sound', _decode_inc_sound),
    0x4d50921e: ('dec_sound', _decode_dec_sound),
    0x4559a4fd: ('error_sound', _decode_error_sound),
    0xe119319b: ('text_background', _decode_text_background),
}
