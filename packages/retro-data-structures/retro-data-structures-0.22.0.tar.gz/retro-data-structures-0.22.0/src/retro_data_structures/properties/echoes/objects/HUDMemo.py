# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class HUDMemo(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    display_time: float = dataclasses.field(default=3.0)
    clear_window: bool = dataclasses.field(default=True)
    player1: bool = dataclasses.field(default=True)
    player2: bool = dataclasses.field(default=True)
    player3: bool = dataclasses.field(default=True)
    player4: bool = dataclasses.field(default=True)
    type_out: bool = dataclasses.field(default=True)
    use_originator: bool = dataclasses.field(default=False)
    display_type: int = dataclasses.field(default=0)
    string: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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
        data.write(b'\x00\x0b')  # 11 properties

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

        data.write(b'\xa8\xfa\xdf\xa5')  # 0xa8fadfa5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player1))

        data.write(b'\xefZ\xa5u')  # 0xef5aa575
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player2))

        data.write(b'\xd2:\x8c\xc5')  # 0xd23a8cc5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player3))

        data.write(b'`\x1aP\xd5')  # 0x601a50d5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.player4))

        data.write(b'\xaf\xd0\x15\x8e')  # 0xafd0158e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.type_out))

        data.write(b'\xbdo{\x11')  # 0xbd6f7b11
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_originator))

        data.write(b'J\xb3\xb9[')  # 0x4ab3b95b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.display_type))

        data.write(b'\x91\x82%\x0c')  # 0x9182250c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.string))

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
            player1=data['player1'],
            player2=data['player2'],
            player3=data['player3'],
            player4=data['player4'],
            type_out=data['type_out'],
            use_originator=data['use_originator'],
            display_type=data['display_type'],
            string=data['string'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'display_time': self.display_time,
            'clear_window': self.clear_window,
            'player1': self.player1,
            'player2': self.player2,
            'player3': self.player3,
            'player4': self.player4,
            'type_out': self.type_out,
            'use_originator': self.use_originator,
            'display_type': self.display_type,
            'string': self.string,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_string(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.string)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_string, "string", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for HUDMemo.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_display_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_clear_window(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_player1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_player2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_player3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_player4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_type_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_originator(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_display_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_string(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x1a26c1cc: ('display_time', _decode_display_time),
    0x84e2496f: ('clear_window', _decode_clear_window),
    0xa8fadfa5: ('player1', _decode_player1),
    0xef5aa575: ('player2', _decode_player2),
    0xd23a8cc5: ('player3', _decode_player3),
    0x601a50d5: ('player4', _decode_player4),
    0xafd0158e: ('type_out', _decode_type_out),
    0xbd6f7b11: ('use_originator', _decode_use_originator),
    0x4ab3b95b: ('display_type', _decode_display_type),
    0x9182250c: ('string', _decode_string),
}
