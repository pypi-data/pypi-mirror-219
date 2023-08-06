# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.TextProperties import TextProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Subtitle(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    text_properties: TextProperties = dataclasses.field(default_factory=TextProperties)
    text_position_x: int = dataclasses.field(default=0)
    text_position_y: int = dataclasses.field(default=0)
    japan_text_properties: TextProperties = dataclasses.field(default_factory=TextProperties)
    japan_text_position_x: int = dataclasses.field(default=0)
    japan_text_position_y: int = dataclasses.field(default=100)
    string_table: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    initial_string_index: int = dataclasses.field(default=0)
    fade_in_time: float = dataclasses.field(default=0.0)
    fade_out_time: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SUBT'

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
        data.write(b'\x00\x08')  # 8 properties
        num_properties_written = 8

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

        data.write(b'\xc3:\x87\xc7')  # 0xc33a87c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.text_position_x))

        data.write(b'{\x86\xe0\xa2')  # 0x7b86e0a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.text_position_y))

        if self.japan_text_properties != default_override.get('japan_text_properties', TextProperties()):
            num_properties_written += 1
            data.write(b'\xc8\xe4A\xfa')  # 0xc8e441fa
            before = data.tell()
            data.write(b'\x00\x00')  # size placeholder
            self.japan_text_properties.to_stream(data, default_override={'text_bounding_width': 640, 'text_bounding_height': 448})
            after = data.tell()
            data.seek(before)
            data.write(struct.pack(">H", after - before - 2))
            data.seek(after)

        if self.japan_text_position_x != default_override.get('japan_text_position_x', 0):
            num_properties_written += 1
            data.write(b'S\xa7\xf7\xa7')  # 0x53a7f7a7
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>l', self.japan_text_position_x))

        if self.japan_text_position_y != default_override.get('japan_text_position_y', 100):
            num_properties_written += 1
            data.write(b'\xeb\x1b\x90\xc2')  # 0xeb1b90c2
            data.write(b'\x00\x04')  # size
            data.write(struct.pack('>l', self.japan_text_position_y))

        data.write(b'\xfd\x95\xed*')  # 0xfd95ed2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.string_table))

        data.write(b'l\xe4f\x89')  # 0x6ce46689
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.initial_string_index))

        data.write(b'\x90\xaa4\x1f')  # 0x90aa341f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_in_time))

        data.write(b'|&\x9e\xbc')  # 0x7c269ebc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_time))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.write(struct.pack(">H", num_properties_written))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            text_properties=TextProperties.from_json(data['text_properties']),
            text_position_x=data['text_position_x'],
            text_position_y=data['text_position_y'],
            japan_text_properties=TextProperties.from_json(data['japan_text_properties']),
            japan_text_position_x=data['japan_text_position_x'],
            japan_text_position_y=data['japan_text_position_y'],
            string_table=data['string_table'],
            initial_string_index=data['initial_string_index'],
            fade_in_time=data['fade_in_time'],
            fade_out_time=data['fade_out_time'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'text_properties': self.text_properties.to_json(),
            'text_position_x': self.text_position_x,
            'text_position_y': self.text_position_y,
            'japan_text_properties': self.japan_text_properties.to_json(),
            'japan_text_position_x': self.japan_text_position_x,
            'japan_text_position_y': self.japan_text_position_y,
            'string_table': self.string_table,
            'initial_string_index': self.initial_string_index,
            'fade_in_time': self.fade_in_time,
            'fade_out_time': self.fade_out_time,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_text_properties(self, asset_manager):
        yield from self.text_properties.dependencies_for(asset_manager)

    def _dependencies_for_japan_text_properties(self, asset_manager):
        yield from self.japan_text_properties.dependencies_for(asset_manager)

    def _dependencies_for_string_table(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.string_table)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_text_properties, "text_properties", "TextProperties"),
            (self._dependencies_for_japan_text_properties, "japan_text_properties", "TextProperties"),
            (self._dependencies_for_string_table, "string_table", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Subtitle.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_text_properties(data: typing.BinaryIO, property_size: int):
    return TextProperties.from_stream(data, property_size)


def _decode_text_position_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_text_position_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_japan_text_properties(data: typing.BinaryIO, property_size: int):
    return TextProperties.from_stream(data, property_size, default_override={'text_bounding_width': 640, 'text_bounding_height': 448})


def _decode_japan_text_position_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_japan_text_position_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_string_table(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_initial_string_index(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_fade_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xe0543e66: ('text_properties', _decode_text_properties),
    0xc33a87c7: ('text_position_x', _decode_text_position_x),
    0x7b86e0a2: ('text_position_y', _decode_text_position_y),
    0xc8e441fa: ('japan_text_properties', _decode_japan_text_properties),
    0x53a7f7a7: ('japan_text_position_x', _decode_japan_text_position_x),
    0xeb1b90c2: ('japan_text_position_y', _decode_japan_text_position_y),
    0xfd95ed2a: ('string_table', _decode_string_table),
    0x6ce46689: ('initial_string_index', _decode_initial_string_index),
    0x90aa341f: ('fade_in_time', _decode_fade_in_time),
    0x7c269ebc: ('fade_out_time', _decode_fade_out_time),
}
