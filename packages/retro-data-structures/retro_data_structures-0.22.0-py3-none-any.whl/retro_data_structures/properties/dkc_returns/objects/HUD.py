# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.BossHUD import BossHUD
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.PauseHUD import PauseHUD
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct147 import UnknownStruct147
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct156 import UnknownStruct156
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct157 import UnknownStruct157
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct159 import UnknownStruct159
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct162 import UnknownStruct162
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct164 import UnknownStruct164
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct36 import UnknownStruct36


@dataclasses.dataclass()
class HUD(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_struct147: UnknownStruct147 = dataclasses.field(default_factory=UnknownStruct147)
    pause_hud: PauseHUD = dataclasses.field(default_factory=PauseHUD)
    boss_hud: BossHUD = dataclasses.field(default_factory=BossHUD)
    unknown_struct156: UnknownStruct156 = dataclasses.field(default_factory=UnknownStruct156)
    unknown_struct157: UnknownStruct157 = dataclasses.field(default_factory=UnknownStruct157)
    unknown_struct159: UnknownStruct159 = dataclasses.field(default_factory=UnknownStruct159)
    unknown_struct162: UnknownStruct162 = dataclasses.field(default_factory=UnknownStruct162)
    unknown_struct164: UnknownStruct164 = dataclasses.field(default_factory=UnknownStruct164)
    unknown_struct28_0xc68bc9ec: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
    unknown_struct28_0x6bdd8b7a: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
    unknown_struct36: UnknownStruct36 = dataclasses.field(default_factory=UnknownStruct36)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'HUDD'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\x9c\x85\xda')  # 0x5d9c85da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct147.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10e\x969')  # 0x10659639
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pause_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaeA\xee\xd1')  # 0xae41eed1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.boss_hud.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9\x14\xbd\x82')  # 0xb914bd82
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct156.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0bYGA')  # 0xb594741
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct157.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\x84\x1cm')  # 0x51841c6d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct159.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10k0\x89')  # 0x106b3089
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct162.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'<(\x0ed')  # 0x3c280e64
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct164.to_stream(data)
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

        data.write(b'k\xdd\x8bz')  # 0x6bdd8b7a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0x6bdd8b7a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?\x88\xe9\x00')  # 0x3f88e900
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct36.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown_struct147=UnknownStruct147.from_json(data['unknown_struct147']),
            pause_hud=PauseHUD.from_json(data['pause_hud']),
            boss_hud=BossHUD.from_json(data['boss_hud']),
            unknown_struct156=UnknownStruct156.from_json(data['unknown_struct156']),
            unknown_struct157=UnknownStruct157.from_json(data['unknown_struct157']),
            unknown_struct159=UnknownStruct159.from_json(data['unknown_struct159']),
            unknown_struct162=UnknownStruct162.from_json(data['unknown_struct162']),
            unknown_struct164=UnknownStruct164.from_json(data['unknown_struct164']),
            unknown_struct28_0xc68bc9ec=UnknownStruct28.from_json(data['unknown_struct28_0xc68bc9ec']),
            unknown_struct28_0x6bdd8b7a=UnknownStruct28.from_json(data['unknown_struct28_0x6bdd8b7a']),
            unknown_struct36=UnknownStruct36.from_json(data['unknown_struct36']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct147': self.unknown_struct147.to_json(),
            'pause_hud': self.pause_hud.to_json(),
            'boss_hud': self.boss_hud.to_json(),
            'unknown_struct156': self.unknown_struct156.to_json(),
            'unknown_struct157': self.unknown_struct157.to_json(),
            'unknown_struct159': self.unknown_struct159.to_json(),
            'unknown_struct162': self.unknown_struct162.to_json(),
            'unknown_struct164': self.unknown_struct164.to_json(),
            'unknown_struct28_0xc68bc9ec': self.unknown_struct28_0xc68bc9ec.to_json(),
            'unknown_struct28_0x6bdd8b7a': self.unknown_struct28_0x6bdd8b7a.to_json(),
            'unknown_struct36': self.unknown_struct36.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_struct147(data: typing.BinaryIO, property_size: int):
    return UnknownStruct147.from_stream(data, property_size)


def _decode_pause_hud(data: typing.BinaryIO, property_size: int):
    return PauseHUD.from_stream(data, property_size)


def _decode_boss_hud(data: typing.BinaryIO, property_size: int):
    return BossHUD.from_stream(data, property_size)


def _decode_unknown_struct156(data: typing.BinaryIO, property_size: int):
    return UnknownStruct156.from_stream(data, property_size)


def _decode_unknown_struct157(data: typing.BinaryIO, property_size: int):
    return UnknownStruct157.from_stream(data, property_size)


def _decode_unknown_struct159(data: typing.BinaryIO, property_size: int):
    return UnknownStruct159.from_stream(data, property_size)


def _decode_unknown_struct162(data: typing.BinaryIO, property_size: int):
    return UnknownStruct162.from_stream(data, property_size)


def _decode_unknown_struct164(data: typing.BinaryIO, property_size: int):
    return UnknownStruct164.from_stream(data, property_size)


def _decode_unknown_struct28_0xc68bc9ec(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_unknown_struct28_0x6bdd8b7a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_unknown_struct36(data: typing.BinaryIO, property_size: int):
    return UnknownStruct36.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x5d9c85da: ('unknown_struct147', _decode_unknown_struct147),
    0x10659639: ('pause_hud', _decode_pause_hud),
    0xae41eed1: ('boss_hud', _decode_boss_hud),
    0xb914bd82: ('unknown_struct156', _decode_unknown_struct156),
    0xb594741: ('unknown_struct157', _decode_unknown_struct157),
    0x51841c6d: ('unknown_struct159', _decode_unknown_struct159),
    0x106b3089: ('unknown_struct162', _decode_unknown_struct162),
    0x3c280e64: ('unknown_struct164', _decode_unknown_struct164),
    0xc68bc9ec: ('unknown_struct28_0xc68bc9ec', _decode_unknown_struct28_0xc68bc9ec),
    0x6bdd8b7a: ('unknown_struct28_0x6bdd8b7a', _decode_unknown_struct28_0x6bdd8b7a),
    0x3f88e900: ('unknown_struct36', _decode_unknown_struct36),
}
