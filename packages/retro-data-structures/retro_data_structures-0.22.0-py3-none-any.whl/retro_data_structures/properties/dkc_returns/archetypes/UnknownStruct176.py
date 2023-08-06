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
class UnknownStruct176(BaseProperty):
    gui_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27)
    title: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    start1_player: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    start2_player: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    extras: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    options: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    back_core: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    player1_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    player2_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    extras_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    options_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    unknown_struct28: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
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
        data.write(b'\x00\x10')  # 16 properties

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

        data.write(b'1D\x97\x04')  # 0x31449704
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.start1_player))

        data.write(b'F\xdaE\xf4')  # 0x46da45f4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.start2_player))

        data.write(b'\xf19\xaf\x99')  # 0xf139af99
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.extras))

        data.write(b'\xac\xe4\x06~')  # 0xace4067e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.options))

        data.write(b'\xe93dU')  # 0xe9336455
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back))

        data.write(b'w\x0b\xcd;')  # 0x770bcd3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.back_core))

        data.write(b'C\x05OG')  # 0x43054f47
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'\xd6\xf9\xa7\x0f')  # 0xd6f9a70f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.player1_sound))

        data.write(b'O\x1b\xc1\x0e')  # 0x4f1bc10e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.player2_sound))

        data.write(b'\xca\xc2S\x16')  # 0xcac25316
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.extras_sound))

        data.write(b'\xea\x11\x9b,')  # 0xea119b2c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.options_sound))

        data.write(b'\x8c\x9cWL')  # 0x8c9c574c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28.to_stream(data)
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
            unknown_struct27=UnknownStruct27.from_json(data['unknown_struct27']),
            title=data['title'],
            start1_player=data['start1_player'],
            start2_player=data['start2_player'],
            extras=data['extras'],
            options=data['options'],
            back=data['back'],
            back_core=data['back_core'],
            strg=data['strg'],
            player1_sound=data['player1_sound'],
            player2_sound=data['player2_sound'],
            extras_sound=data['extras_sound'],
            options_sound=data['options_sound'],
            unknown_struct28=UnknownStruct28.from_json(data['unknown_struct28']),
            text_background=data['text_background'],
        )

    def to_json(self) -> dict:
        return {
            'gui_frame': self.gui_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'title': self.title,
            'start1_player': self.start1_player,
            'start2_player': self.start2_player,
            'extras': self.extras,
            'options': self.options,
            'back': self.back,
            'back_core': self.back_core,
            'strg': self.strg,
            'player1_sound': self.player1_sound,
            'player2_sound': self.player2_sound,
            'extras_sound': self.extras_sound,
            'options_sound': self.options_sound,
            'unknown_struct28': self.unknown_struct28.to_json(),
            'text_background': self.text_background,
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct27(data: typing.BinaryIO, property_size: int):
    return UnknownStruct27.from_stream(data, property_size)


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_start1_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_start2_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_extras(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_options(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_back_core(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_player1_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_player2_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_extras_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_options_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct28(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_text_background(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0x73e2819b: ('unknown_struct27', _decode_unknown_struct27),
    0xa4f20c17: ('title', _decode_title),
    0x31449704: ('start1_player', _decode_start1_player),
    0x46da45f4: ('start2_player', _decode_start2_player),
    0xf139af99: ('extras', _decode_extras),
    0xace4067e: ('options', _decode_options),
    0xe9336455: ('back', _decode_back),
    0x770bcd3b: ('back_core', _decode_back_core),
    0x43054f47: ('strg', _decode_strg),
    0xd6f9a70f: ('player1_sound', _decode_player1_sound),
    0x4f1bc10e: ('player2_sound', _decode_player2_sound),
    0xcac25316: ('extras_sound', _decode_extras_sound),
    0xea119b2c: ('options_sound', _decode_options_sound),
    0x8c9c574c: ('unknown_struct28', _decode_unknown_struct28),
    0xe119319b: ('text_background', _decode_text_background),
}
