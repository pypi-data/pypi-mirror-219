# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class HUDMemo(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    display_time: float = dataclasses.field(default=3.0)
    clear_window: bool = dataclasses.field(default=True)
    type_out: bool = dataclasses.field(default=True)
    display_type: int = dataclasses.field(default=0)
    message_type: enums.MessageType = dataclasses.field(default=enums.MessageType.Unknown1)
    has_border: bool = dataclasses.field(default=False)
    priority: int = dataclasses.field(default=1)
    string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    index_into_string: int = dataclasses.field(default=0)
    font_scale: float = dataclasses.field(default=1.0)
    enable_play_alert: bool = dataclasses.field(default=True)
    unknown_0xb7a3e235: bool = dataclasses.field(default=False)
    unknown_0x8f115e7a: bool = dataclasses.field(default=False)
    unknown_0xd25a8445: bool = dataclasses.field(default=False)
    animation: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    caad: AssetId = dataclasses.field(metadata={'asset_types': ['CAAD']}, default=default_asset_id)
    texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    texture_static: float = dataclasses.field(default=0.0)
    audio_stream: AssetId = dataclasses.field(metadata={'asset_types': ['STRM']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'MEMO'

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
        data.write(b'\x00\x15')  # 21 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1a&\xc1\xcc')  # 0x1a26c1cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.display_time))

        data.write(b'\x84\xe2Io')  # 0x84e2496f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.clear_window))

        data.write(b'\xaf\xd0\x15\x8e')  # 0xafd0158e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.type_out))

        data.write(b'J\xb3\xb9[')  # 0x4ab3b95b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.display_type))

        data.write(b'+N)\x0c')  # 0x2b4e290c
        data.write(b'\x00\x04')  # size
        self.message_type.to_stream(data)

        data.write(b'\xe4\xc5L\x15')  # 0xe4c54c15
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.has_border))

        data.write(b'B\x08vP')  # 0x42087650
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.priority))

        data.write(b'\x91\x82%\x0c')  # 0x9182250c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.string))

        data.write(b'd\x12B\x19')  # 0x64124219
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.index_into_string))

        data.write(b'\x01\x00\x9a\x8c')  # 0x1009a8c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.font_scale))

        data.write(b'\xfb\x0e\x87\xda')  # 0xfb0e87da
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_play_alert))

        data.write(b'\xb7\xa3\xe25')  # 0xb7a3e235
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xb7a3e235))

        data.write(b'\x8f\x11^z')  # 0x8f115e7a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x8f115e7a))

        data.write(b'\xd2Z\x84E')  # 0xd25a8445
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xd25a8445))

        data.write(b'\xa3\xd6?D')  # 0xa3d63f44
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\x95\xa1\x00\xab')  # 0x95a100ab
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caad))

        data.write(b'\xd1\xf6Xr')  # 0xd1f65872
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.texture))

        data.write(b'F\xdc\xa5(')  # 0x46dca528
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.texture_static))

        data.write(b'\xe5\xde\xb9\xc4')  # 0xe5deb9c4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.audio_stream))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            display_time=data['display_time'],
            clear_window=data['clear_window'],
            type_out=data['type_out'],
            display_type=data['display_type'],
            message_type=enums.MessageType.from_json(data['message_type']),
            has_border=data['has_border'],
            priority=data['priority'],
            string=data['string'],
            index_into_string=data['index_into_string'],
            font_scale=data['font_scale'],
            enable_play_alert=data['enable_play_alert'],
            unknown_0xb7a3e235=data['unknown_0xb7a3e235'],
            unknown_0x8f115e7a=data['unknown_0x8f115e7a'],
            unknown_0xd25a8445=data['unknown_0xd25a8445'],
            animation=AnimationParameters.from_json(data['animation']),
            model=data['model'],
            caad=data['caad'],
            texture=data['texture'],
            texture_static=data['texture_static'],
            audio_stream=data['audio_stream'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'display_time': self.display_time,
            'clear_window': self.clear_window,
            'type_out': self.type_out,
            'display_type': self.display_type,
            'message_type': self.message_type.to_json(),
            'has_border': self.has_border,
            'priority': self.priority,
            'string': self.string,
            'index_into_string': self.index_into_string,
            'font_scale': self.font_scale,
            'enable_play_alert': self.enable_play_alert,
            'unknown_0xb7a3e235': self.unknown_0xb7a3e235,
            'unknown_0x8f115e7a': self.unknown_0x8f115e7a,
            'unknown_0xd25a8445': self.unknown_0xd25a8445,
            'animation': self.animation.to_json(),
            'model': self.model,
            'caad': self.caad,
            'texture': self.texture,
            'texture_static': self.texture_static,
            'audio_stream': self.audio_stream,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_display_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_clear_window(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_type_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_display_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_message_type(data: typing.BinaryIO, property_size: int):
    return enums.MessageType.from_stream(data)


def _decode_has_border(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_index_into_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_font_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_enable_play_alert(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xb7a3e235(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x8f115e7a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xd25a8445(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_animation(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caad(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_texture_static(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_audio_stream(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x1a26c1cc: ('display_time', _decode_display_time),
    0x84e2496f: ('clear_window', _decode_clear_window),
    0xafd0158e: ('type_out', _decode_type_out),
    0x4ab3b95b: ('display_type', _decode_display_type),
    0x2b4e290c: ('message_type', _decode_message_type),
    0xe4c54c15: ('has_border', _decode_has_border),
    0x42087650: ('priority', _decode_priority),
    0x9182250c: ('string', _decode_string),
    0x64124219: ('index_into_string', _decode_index_into_string),
    0x1009a8c: ('font_scale', _decode_font_scale),
    0xfb0e87da: ('enable_play_alert', _decode_enable_play_alert),
    0xb7a3e235: ('unknown_0xb7a3e235', _decode_unknown_0xb7a3e235),
    0x8f115e7a: ('unknown_0x8f115e7a', _decode_unknown_0x8f115e7a),
    0xd25a8445: ('unknown_0xd25a8445', _decode_unknown_0xd25a8445),
    0xa3d63f44: ('animation', _decode_animation),
    0xc27ffa8f: ('model', _decode_model),
    0x95a100ab: ('caad', _decode_caad),
    0xd1f65872: ('texture', _decode_texture),
    0x46dca528: ('texture_static', _decode_texture_static),
    0xe5deb9c4: ('audio_stream', _decode_audio_stream),
}
