# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct29 import UnknownStruct29
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct172(BaseProperty):
    unknown_struct29: UnknownStruct29 = dataclasses.field(default_factory=UnknownStruct29)
    image_names: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    left_arrow: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    right_arrow: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    left_arrow_pressed: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    right_arrow_pressed: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    left_image_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    right_image_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'0[22')  # 0x305b3232
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct29.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x11\x9eu\xac')  # 0x119e75ac
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.image_names))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

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

        data.write(b'\xc4+h\xc9')  # 0xc42b68c9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_image_sound))

        data.write(b'R\xf8//')  # 0x52f82f2f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_image_sound))

        data.write(b'\xe1\x191\x9b')  # 0xe119319b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.text_background))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_struct29=UnknownStruct29.from_json(data['unknown_struct29']),
            image_names=data['image_names'],
            back=data['back'],
            back_core=data['back_core'],
            left_arrow=data['left_arrow'],
            right_arrow=data['right_arrow'],
            left_arrow_pressed=data['left_arrow_pressed'],
            right_arrow_pressed=data['right_arrow_pressed'],
            left_image_sound=data['left_image_sound'],
            right_image_sound=data['right_image_sound'],
            text_background=data['text_background'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_struct29': self.unknown_struct29.to_json(),
            'image_names': self.image_names,
            'back': self.back,
            'back_core': self.back_core,
            'left_arrow': self.left_arrow,
            'right_arrow': self.right_arrow,
            'left_arrow_pressed': self.left_arrow_pressed,
            'right_arrow_pressed': self.right_arrow_pressed,
            'left_image_sound': self.left_image_sound,
            'right_image_sound': self.right_image_sound,
            'text_background': self.text_background,
        }


def _decode_unknown_struct29(data: typing.BinaryIO, property_size: int):
    return UnknownStruct29.from_stream(data, property_size)


def _decode_image_names(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_image_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_image_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x305b3232: ('unknown_struct29', _decode_unknown_struct29),
    0x119e75ac: ('image_names', _decode_image_names),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0x314cdc24: ('left_arrow', _decode_left_arrow),
    0xd1918347: ('right_arrow', _decode_right_arrow),
    0xb4510efe: ('left_arrow_pressed', _decode_left_arrow_pressed),
    0x54cd1874: ('right_arrow_pressed', _decode_right_arrow_pressed),
    0xc42b68c9: ('left_image_sound', _decode_left_image_sound),
    0x52f82f2f: ('right_image_sound', _decode_right_image_sound),
    0xe119319b: ('text_background', _decode_text_background),
}
