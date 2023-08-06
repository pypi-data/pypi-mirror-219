# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct148 import UnknownStruct148
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct27 import UnknownStruct27
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct35 import UnknownStruct35
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct149(BaseProperty):
    pause_hud_frame: AssetId = dataclasses.field(metadata={'asset_types': ['FRME']}, default=default_asset_id)
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27)
    options_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    puzzle_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    strg: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    continue_game_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    quit_game_string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_struct35: UnknownStruct35 = dataclasses.field(default_factory=UnknownStruct35)
    quit_confirm_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    restart_confirm_text: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    unknown_struct148: UnknownStruct148 = dataclasses.field(default_factory=UnknownStruct148)

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

        data.write(b'@K\x98\xb2')  # 0x404b98b2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.pause_hud_frame))

        data.write(b's\xe2\x81\x9b')  # 0x73e2819b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\xcbR\xf1')  # 0xf7cb52f1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.options_string))

        data.write(b'\xa1qA\x02')  # 0xa1714102
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.puzzle_string))

        data.write(b',t\xe19')  # 0x2c74e139
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg))

        data.write(b'u%\xf9C')  # 0x7525f943
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.continue_game_string))

        data.write(b'$5h\x17')  # 0x24356817
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.quit_game_string))

        data.write(b'\xd8U$\xdb')  # 0xd85524db
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct35.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd\xb3\xaa\xc2')  # 0xfdb3aac2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.quit_confirm_text))

        data.write(b'+K~\xf6')  # 0x2b4b7ef6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.restart_confirm_text))

        data.write(b'\x98[\xfc\xd9')  # 0x985bfcd9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct148.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            pause_hud_frame=data['pause_hud_frame'],
            unknown_struct27=UnknownStruct27.from_json(data['unknown_struct27']),
            options_string=data['options_string'],
            puzzle_string=data['puzzle_string'],
            strg=data['strg'],
            continue_game_string=data['continue_game_string'],
            quit_game_string=data['quit_game_string'],
            unknown_struct35=UnknownStruct35.from_json(data['unknown_struct35']),
            quit_confirm_text=data['quit_confirm_text'],
            restart_confirm_text=data['restart_confirm_text'],
            unknown_struct148=UnknownStruct148.from_json(data['unknown_struct148']),
        )

    def to_json(self) -> dict:
        return {
            'pause_hud_frame': self.pause_hud_frame,
            'unknown_struct27': self.unknown_struct27.to_json(),
            'options_string': self.options_string,
            'puzzle_string': self.puzzle_string,
            'strg': self.strg,
            'continue_game_string': self.continue_game_string,
            'quit_game_string': self.quit_game_string,
            'unknown_struct35': self.unknown_struct35.to_json(),
            'quit_confirm_text': self.quit_confirm_text,
            'restart_confirm_text': self.restart_confirm_text,
            'unknown_struct148': self.unknown_struct148.to_json(),
        }


def _decode_pause_hud_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct27(data: typing.BinaryIO, property_size: int):
    return UnknownStruct27.from_stream(data, property_size)


def _decode_options_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_puzzle_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_continue_game_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_quit_game_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct35(data: typing.BinaryIO, property_size: int):
    return UnknownStruct35.from_stream(data, property_size)


def _decode_quit_confirm_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_restart_confirm_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct148(data: typing.BinaryIO, property_size: int):
    return UnknownStruct148.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x404b98b2: ('pause_hud_frame', _decode_pause_hud_frame),
    0x73e2819b: ('unknown_struct27', _decode_unknown_struct27),
    0xf7cb52f1: ('options_string', _decode_options_string),
    0xa1714102: ('puzzle_string', _decode_puzzle_string),
    0x2c74e139: ('strg', _decode_strg),
    0x7525f943: ('continue_game_string', _decode_continue_game_string),
    0x24356817: ('quit_game_string', _decode_quit_game_string),
    0xd85524db: ('unknown_struct35', _decode_unknown_struct35),
    0xfdb3aac2: ('quit_confirm_text', _decode_quit_confirm_text),
    0x2b4b7ef6: ('restart_confirm_text', _decode_restart_confirm_text),
    0x985bfcd9: ('unknown_struct148', _decode_unknown_struct148),
}
