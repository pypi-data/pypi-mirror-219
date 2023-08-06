# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties


@dataclasses.dataclass()
class Dock(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    dock_number: int = dataclasses.field(default=0)
    area_number: int = dataclasses.field(default=0)
    is_virtual: bool = dataclasses.field(default=False)
    load_connected_immediate: bool = dataclasses.field(default=True)
    show_soft_transition: bool = dataclasses.field(default=True)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DOCK'

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
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x11\x01\xe9\x1b')  # 0x1101e91b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dock_number))

        data.write(b'a\x0e\xec\x90')  # 0x610eec90
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.area_number))

        data.write(b'\x87\x0emo')  # 0x870e6d6f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_virtual))

        data.write(b'\xf3\x83\x9do')  # 0xf3839d6f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.load_connected_immediate))

        data.write(b'"-\x9d\xaf')  # 0x222d9daf
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.show_soft_transition))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            dock_number=data['dock_number'],
            area_number=data['area_number'],
            is_virtual=data['is_virtual'],
            load_connected_immediate=data['load_connected_immediate'],
            show_soft_transition=data['show_soft_transition'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'dock_number': self.dock_number,
            'area_number': self.area_number,
            'is_virtual': self.is_virtual,
            'load_connected_immediate': self.load_connected_immediate,
            'show_soft_transition': self.show_soft_transition,
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_dock_number(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_area_number(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_is_virtual(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_load_connected_immediate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_show_soft_transition(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x1101e91b: ('dock_number', _decode_dock_number),
    0x610eec90: ('area_number', _decode_area_number),
    0x870e6d6f: ('is_virtual', _decode_is_virtual),
    0xf3839d6f: ('load_connected_immediate', _decode_load_connected_immediate),
    0x222d9daf: ('show_soft_transition', _decode_show_soft_transition),
}
