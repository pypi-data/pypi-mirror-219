# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct180(BaseProperty):
    gui_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27)
    title: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    hidden_name: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    left_arrow: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    left_arrow_pressed: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    right_arrow: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    right_arrow_pressed: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    return_: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    return_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)

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
        data.write(b'\x00\n')  # 10 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'x\xa2\xb4\xb0')  # 0x78a2b4b0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hidden_name))

        data.write(b'1L\xdc$')  # 0x314cdc24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_arrow))

        data.write(b'\xb4Q\x0e\xfe')  # 0xb4510efe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_arrow_pressed))

        data.write(b'\xd1\x91\x83G')  # 0xd1918347
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_arrow))

        data.write(b'T\xcd\x18t')  # 0x54cd1874
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_arrow_pressed))

        data.write(b'G\x1f\xea\x86')  # 0x471fea86
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.return_))

        data.write(b'\xa0\x1e\x08\x87')  # 0xa01e0887
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.return_core))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            gui_frame=data['gui_frame'],
            unknown_struct27=UnknownStruct27.from_json(data['unknown_struct27']),
            title=data['title'],
            hidden_name=data['hidden_name'],
            left_arrow=data['left_arrow'],
            left_arrow_pressed=data['left_arrow_pressed'],
            right_arrow=data['right_arrow'],
            right_arrow_pressed=data['right_arrow_pressed'],
            return_=data['return_'],
            return_core=data['return_core'],
        )

    def to_json(self) -> dict:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'title': self.title,
            'hidden_name': self.hidden_name,
            'left_arrow': self.left_arrow,
            'left_arrow_pressed': self.left_arrow_pressed,
            'right_arrow': self.right_arrow,
            'right_arrow_pressed': self.right_arrow_pressed,
            'return_': self.return_,
            'return_core': self.return_core,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct27(data: typing.BinaryIO, property_size: int):
    return UnknownStruct27.from_stream(data, property_size)


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_hidden_name(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_arrow_pressed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_return_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x73e2819b: ('unknown_struct27', _decode_unknown_struct27),
    0xa4f20c17: ('title', _decode_title),
    0x78a2b4b0: ('hidden_name', _decode_hidden_name),
    0x314cdc24: ('left_arrow', _decode_left_arrow),
    0xb4510efe: ('left_arrow_pressed', _decode_left_arrow_pressed),
    0xd1918347: ('right_arrow', _decode_right_arrow),
    0x54cd1874: ('right_arrow_pressed', _decode_right_arrow_pressed),
    0x471fea86: ('return_', _decode_return_),
    0xa01e0887: ('return_core', _decode_return_core),
}
