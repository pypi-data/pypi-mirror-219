# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct27(BaseProperty):
    appear: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    in_place: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    disappear: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    off_screen: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    up: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    down: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    left: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    right: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    cancel: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    select: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD', 'STRG']}, default=default_asset_id)
    error: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'\xb2\xf9&t')  # 0xb2f92674
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.appear))

        data.write(b'\x12\xaa8\xc2')  # 0x12aa38c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.in_place))

        data.write(b'\x0c\xfe\x9a\xd0')  # 0xcfe9ad0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.disappear))

        data.write(b'\xe2?\xe8\xa7')  # 0xe23fe8a7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.off_screen))

        data.write(b'\xdc\xd1F\x11')  # 0xdcd14611
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.up))

        data.write(b'L\xff&\x83')  # 0x4cff2683
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.down))

        data.write(b'\x05\x03.\xd4')  # 0x5032ed4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left))

        data.write(b'g\x1d\xbf\xb5')  # 0x671dbfb5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right))

        data.write(b'M\x07\xa2\xff')  # 0x4d07a2ff
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cancel))

        data.write(b'\x8e\xd6R\x83')  # 0x8ed65283
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select))

        data.write(b'\xab_\x1bT')  # 0xab5f1b54
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.error))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            appear=data['appear'],
            in_place=data['in_place'],
            disappear=data['disappear'],
            off_screen=data['off_screen'],
            up=data['up'],
            down=data['down'],
            left=data['left'],
            right=data['right'],
            cancel=data['cancel'],
            select=data['select'],
            error=data['error'],
        )

    def to_json(self) -> dict:
        return {
            'appear': self.appear,
            'in_place': self.in_place,
            'disappear': self.disappear,
            'off_screen': self.off_screen,
            'up': self.up,
            'down': self.down,
            'left': self.left,
            'right': self.right,
            'cancel': self.cancel,
            'select': self.select,
            'error': self.error,
        }


_FAST_FORMAT = None
_FAST_IDS = (0xb2f92674, 0x12aa38c2, 0xcfe9ad0, 0xe23fe8a7, 0xdcd14611, 0x4cff2683, 0x5032ed4, 0x671dbfb5, 0x4d07a2ff, 0x8ed65283, 0xab5f1b54)


def _fast_decode(data: typing.BinaryIO, property_count: int) -> typing.Optional[UnknownStruct27]:
    if property_count != 11:
        return None

    global _FAST_FORMAT
    if _FAST_FORMAT is None:
        _FAST_FORMAT = struct.Struct('>LHQLHQLHQLHQLHQLHQLHQLHQLHQLHQLHQ')

    before = data.tell()
    dec = _FAST_FORMAT.unpack(data.read(154))
    if (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30]) != _FAST_IDS:
        data.seek(before)
        return None

    return UnknownStruct27(
        dec[2],
        dec[5],
        dec[8],
        dec[11],
        dec[14],
        dec[17],
        dec[20],
        dec[23],
        dec[26],
        dec[29],
        dec[32],
    )


def _decode_appear(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_in_place(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_disappear(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_off_screen(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_up(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_down(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cancel(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_error(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb2f92674: ('appear', _decode_appear),
    0x12aa38c2: ('in_place', _decode_in_place),
    0xcfe9ad0: ('disappear', _decode_disappear),
    0xe23fe8a7: ('off_screen', _decode_off_screen),
    0xdcd14611: ('up', _decode_up),
    0x4cff2683: ('down', _decode_down),
    0x5032ed4: ('left', _decode_left),
    0x671dbfb5: ('right', _decode_right),
    0x4d07a2ff: ('cancel', _decode_cancel),
    0x8ed65283: ('select', _decode_select),
    0xab5f1b54: ('error', _decode_error),
}
