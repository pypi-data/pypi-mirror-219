# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.TextProperties import TextProperties
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color


@dataclasses.dataclass()
class DialogueMenu(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    text_properties: TextProperties = dataclasses.field(default_factory=TextProperties)
    japan_text_properties: TextProperties = dataclasses.field(default_factory=TextProperties)
    text_position_y: int = dataclasses.field(default=100)
    japan_text_position_y: int = dataclasses.field(default=100)
    selected_font_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    unknown_0x69fdb265: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    selection_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unknown_0x3c5e109a: int = dataclasses.field(default=110)
    default_selection: enums.DefaultSelection = dataclasses.field(default=enums.DefaultSelection.Unknown1)
    highlight_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    select_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DGMN'

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

        data.write(b'\xe0T>f')  # 0xe0543e66
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.text_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc8\xe4A\xfa')  # 0xc8e441fa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.japan_text_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{\x86\xe0\xa2')  # 0x7b86e0a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.text_position_y))

        data.write(b'\xeb\x1b\x90\xc2')  # 0xeb1b90c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.japan_text_position_y))

        data.write(b'\xefPYe')  # 0xef505965
        data.write(b'\x00\x10')  # size
        self.selected_font_color.to_stream(data)

        data.write(b'i\xfd\xb2e')  # 0x69fdb265
        data.write(b'\x00\x10')  # size
        self.unknown_0x69fdb265.to_stream(data)

        data.write(b'\xd1\xb7AQ')  # 0xd1b74151
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.selection_model))

        data.write(b'<^\x10\x9a')  # 0x3c5e109a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x3c5e109a))

        data.write(b'X\xcb\xcb\xca')  # 0x58cbcbca
        data.write(b'\x00\x04')  # size
        self.default_selection.to_stream(data)

        data.write(b'\xe8\xfen\x9d')  # 0xe8fe6e9d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.highlight_sound))

        data.write(b'\x9e\x87\xe0\xeb')  # 0x9e87e0eb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.select_sound))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            text_properties=TextProperties.from_json(data['text_properties']),
            japan_text_properties=TextProperties.from_json(data['japan_text_properties']),
            text_position_y=data['text_position_y'],
            japan_text_position_y=data['japan_text_position_y'],
            selected_font_color=Color.from_json(data['selected_font_color']),
            unknown_0x69fdb265=Color.from_json(data['unknown_0x69fdb265']),
            selection_model=data['selection_model'],
            unknown_0x3c5e109a=data['unknown_0x3c5e109a'],
            default_selection=enums.DefaultSelection.from_json(data['default_selection']),
            highlight_sound=data['highlight_sound'],
            select_sound=data['select_sound'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'text_properties': self.text_properties.to_json(),
            'japan_text_properties': self.japan_text_properties.to_json(),
            'text_position_y': self.text_position_y,
            'japan_text_position_y': self.japan_text_position_y,
            'selected_font_color': self.selected_font_color.to_json(),
            'unknown_0x69fdb265': self.unknown_0x69fdb265.to_json(),
            'selection_model': self.selection_model,
            'unknown_0x3c5e109a': self.unknown_0x3c5e109a,
            'default_selection': self.default_selection.to_json(),
            'highlight_sound': self.highlight_sound,
            'select_sound': self.select_sound,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_text_properties(data: typing.BinaryIO, property_size: int):
    return TextProperties.from_stream(data, property_size)


def _decode_japan_text_properties(data: typing.BinaryIO, property_size: int):
    return TextProperties.from_stream(data, property_size)


def _decode_text_position_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_japan_text_position_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_selected_font_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x69fdb265(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_selection_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x3c5e109a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_default_selection(data: typing.BinaryIO, property_size: int):
    return enums.DefaultSelection.from_stream(data)


def _decode_highlight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_select_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xe0543e66: ('text_properties', _decode_text_properties),
    0xc8e441fa: ('japan_text_properties', _decode_japan_text_properties),
    0x7b86e0a2: ('text_position_y', _decode_text_position_y),
    0xeb1b90c2: ('japan_text_position_y', _decode_japan_text_position_y),
    0xef505965: ('selected_font_color', _decode_selected_font_color),
    0x69fdb265: ('unknown_0x69fdb265', _decode_unknown_0x69fdb265),
    0xd1b74151: ('selection_model', _decode_selection_model),
    0x3c5e109a: ('unknown_0x3c5e109a', _decode_unknown_0x3c5e109a),
    0x58cbcbca: ('default_selection', _decode_default_selection),
    0xe8fe6e9d: ('highlight_sound', _decode_highlight_sound),
    0x9e87e0eb: ('select_sound', _decode_select_sound),
}
