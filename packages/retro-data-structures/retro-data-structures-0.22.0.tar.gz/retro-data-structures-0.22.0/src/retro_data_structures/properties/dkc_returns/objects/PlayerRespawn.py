# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct24 import UnknownStruct24
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct248 import UnknownStruct248
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct249 import UnknownStruct249
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters


@dataclasses.dataclass()
class PlayerRespawn(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    player_freeze: bool = dataclasses.field(default=True)
    player_thaw_time: float = dataclasses.field(default=1.0)
    camera_freeze: bool = dataclasses.field(default=True)
    unknown_struct248: UnknownStruct248 = dataclasses.field(default_factory=UnknownStruct248)
    unknown_struct249: UnknownStruct249 = dataclasses.field(default_factory=UnknownStruct249)
    layer_list: UnknownStruct24 = dataclasses.field(default_factory=UnknownStruct24)
    balloon_character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    multiplayer_balloon_anim: int = dataclasses.field(default=0)
    dk_balloon_character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    diddy_balloon_character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    super_guide_dk_character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PRSP'

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

        data.write(b'e\x00\x16\xed')  # 0x650016ed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player_freeze))

        data.write(b'3\x0e\xdcD')  # 0x330edc44
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_thaw_time))

        data.write(b'\x1d=\xc68')  # 0x1d3dc638
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.camera_freeze))

        data.write(b'=\x97\xfe\xf6')  # 0x3d97fef6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct248.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xccR\x8e\xd6')  # 0xcc528ed6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct249.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Ak\xd9\xeb')  # 0x416bd9eb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.layer_list.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf8\xb3\xab\xe0')  # 0xf8b3abe0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.balloon_character.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V?5\xc8')  # 0x563f35c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.multiplayer_balloon_anim))

        data.write(b'2\xce\x89\x9f')  # 0x32ce899f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dk_balloon_character.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16,\x82|')  # 0x162c827c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.diddy_balloon_character.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x89\x9f\x84s')  # 0x899f8473
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_guide_dk_character.to_stream(data)
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
            player_freeze=data['player_freeze'],
            player_thaw_time=data['player_thaw_time'],
            camera_freeze=data['camera_freeze'],
            unknown_struct248=UnknownStruct248.from_json(data['unknown_struct248']),
            unknown_struct249=UnknownStruct249.from_json(data['unknown_struct249']),
            layer_list=UnknownStruct24.from_json(data['layer_list']),
            balloon_character=AnimationParameters.from_json(data['balloon_character']),
            multiplayer_balloon_anim=data['multiplayer_balloon_anim'],
            dk_balloon_character=AnimationParameters.from_json(data['dk_balloon_character']),
            diddy_balloon_character=AnimationParameters.from_json(data['diddy_balloon_character']),
            super_guide_dk_character=AnimationParameters.from_json(data['super_guide_dk_character']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'player_freeze': self.player_freeze,
            'player_thaw_time': self.player_thaw_time,
            'camera_freeze': self.camera_freeze,
            'unknown_struct248': self.unknown_struct248.to_json(),
            'unknown_struct249': self.unknown_struct249.to_json(),
            'layer_list': self.layer_list.to_json(),
            'balloon_character': self.balloon_character.to_json(),
            'multiplayer_balloon_anim': self.multiplayer_balloon_anim,
            'dk_balloon_character': self.dk_balloon_character.to_json(),
            'diddy_balloon_character': self.diddy_balloon_character.to_json(),
            'super_guide_dk_character': self.super_guide_dk_character.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_player_freeze(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_player_thaw_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_camera_freeze(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct248(data: typing.BinaryIO, property_size: int):
    return UnknownStruct248.from_stream(data, property_size)


def _decode_unknown_struct249(data: typing.BinaryIO, property_size: int):
    return UnknownStruct249.from_stream(data, property_size)


def _decode_layer_list(data: typing.BinaryIO, property_size: int):
    return UnknownStruct24.from_stream(data, property_size)


def _decode_balloon_character(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_multiplayer_balloon_anim(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dk_balloon_character(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_diddy_balloon_character(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_super_guide_dk_character(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x650016ed: ('player_freeze', _decode_player_freeze),
    0x330edc44: ('player_thaw_time', _decode_player_thaw_time),
    0x1d3dc638: ('camera_freeze', _decode_camera_freeze),
    0x3d97fef6: ('unknown_struct248', _decode_unknown_struct248),
    0xcc528ed6: ('unknown_struct249', _decode_unknown_struct249),
    0x416bd9eb: ('layer_list', _decode_layer_list),
    0xf8b3abe0: ('balloon_character', _decode_balloon_character),
    0x563f35c8: ('multiplayer_balloon_anim', _decode_multiplayer_balloon_anim),
    0x32ce899f: ('dk_balloon_character', _decode_dk_balloon_character),
    0x162c827c: ('diddy_balloon_character', _decode_diddy_balloon_character),
    0x899f8473: ('super_guide_dk_character', _decode_super_guide_dk_character),
}
