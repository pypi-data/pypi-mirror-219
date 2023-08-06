# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.GuiWidgetProperties import GuiWidgetProperties


@dataclasses.dataclass()
class GuiSlider(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    gui_widget_properties: GuiWidgetProperties = dataclasses.field(default_factory=GuiWidgetProperties)
    min_value: float = dataclasses.field(default=0.0)
    max_value: float = dataclasses.field(default=255.0)
    increment: float = dataclasses.field(default=1.0)
    slide_speed: float = dataclasses.field(default=1.0)
    slide_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    slide_sound_volume: int = dataclasses.field(default=127)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'GSLD'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['ScriptGui.rel']

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

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data, default_override={'active': False})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91\xce\xfa\x1e')  # 0x91cefa1e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.gui_widget_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',\xcb\xbd\xfe')  # 0x2ccbbdfe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_value))

        data.write(b'l\x84\xc5\x88')  # 0x6c84c588
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_value))

        data.write(b'\x8ah\xdbR')  # 0x8a68db52
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.increment))

        data.write(b'\xed\xb6\x06+')  # 0xedb6062b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.slide_speed))

        data.write(b'\xd1XsK')  # 0xd158734b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.slide_sound))

        data.write(b' \xdd\xb6a')  # 0x20ddb661
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.slide_sound_volume))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            gui_widget_properties=GuiWidgetProperties.from_json(data['gui_widget_properties']),
            min_value=data['min_value'],
            max_value=data['max_value'],
            increment=data['increment'],
            slide_speed=data['slide_speed'],
            slide_sound=data['slide_sound'],
            slide_sound_volume=data['slide_sound_volume'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'gui_widget_properties': self.gui_widget_properties.to_json(),
            'min_value': self.min_value,
            'max_value': self.max_value,
            'increment': self.increment,
            'slide_speed': self.slide_speed,
            'slide_sound': self.slide_sound,
            'slide_sound_volume': self.slide_sound_volume,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_gui_widget_properties(self, asset_manager):
        yield from self.gui_widget_properties.dependencies_for(asset_manager)

    def _dependencies_for_slide_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.slide_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_gui_widget_properties, "gui_widget_properties", "GuiWidgetProperties"),
            (self._dependencies_for_slide_sound, "slide_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for GuiSlider.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size, default_override={'active': False})


def _decode_gui_widget_properties(data: typing.BinaryIO, property_size: int):
    return GuiWidgetProperties.from_stream(data, property_size)


def _decode_min_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_value(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_increment(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_slide_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_slide_sound_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x91cefa1e: ('gui_widget_properties', _decode_gui_widget_properties),
    0x2ccbbdfe: ('min_value', _decode_min_value),
    0x6c84c588: ('max_value', _decode_max_value),
    0x8a68db52: ('increment', _decode_increment),
    0xedb6062b: ('slide_speed', _decode_slide_speed),
    0xd158734b: ('slide_sound', _decode_slide_sound),
    0x20ddb661: ('slide_sound_volume', _decode_slide_sound_volume),
}
