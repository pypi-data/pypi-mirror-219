# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct182 import UnknownStruct182
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct183 import UnknownStruct183
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct28 import UnknownStruct28
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct36 import UnknownStruct36
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class IslandHUD(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    cursor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    disabled_cursor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    secondary_cursor_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unknown_struct182: UnknownStruct182 = dataclasses.field(default_factory=UnknownStruct182)
    unknown_struct36: UnknownStruct36 = dataclasses.field(default_factory=UnknownStruct36)
    unknown_struct183: UnknownStruct183 = dataclasses.field(default_factory=UnknownStruct183)
    unknown_struct28_0xc68bc9ec: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
    unknown_struct28_0x6bdd8b7a: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
    unknown_struct28_0xcc53c738: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
    unknown_struct28_0xbcf93a2a: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)
    unknown_struct28_0x6549e3f9: UnknownStruct28 = dataclasses.field(default_factory=UnknownStruct28)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'IHUD'

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

        data.write(b'\x0f\x94\x80j')  # 0xf94806a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cursor_model))

        data.write(b'\xd0/\xb1\xa1')  # 0xd02fb1a1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.disabled_cursor_model))

        data.write(b'\xa7@e\xce')  # 0xa74065ce
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.secondary_cursor_model))

        data.write(b'\x17C\xb7p')  # 0x1743b770
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct182.to_stream(data)
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

        data.write(b'\xeb|\x1b\xf2')  # 0xeb7c1bf2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct183.to_stream(data)
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

        data.write(b'\xccS\xc78')  # 0xcc53c738
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0xcc53c738.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc\xf9:*')  # 0xbcf93a2a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0xbcf93a2a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'eI\xe3\xf9')  # 0x6549e3f9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct28_0x6549e3f9.to_stream(data)
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
            cursor_model=data['cursor_model'],
            disabled_cursor_model=data['disabled_cursor_model'],
            secondary_cursor_model=data['secondary_cursor_model'],
            unknown_struct182=UnknownStruct182.from_json(data['unknown_struct182']),
            unknown_struct36=UnknownStruct36.from_json(data['unknown_struct36']),
            unknown_struct183=UnknownStruct183.from_json(data['unknown_struct183']),
            unknown_struct28_0xc68bc9ec=UnknownStruct28.from_json(data['unknown_struct28_0xc68bc9ec']),
            unknown_struct28_0x6bdd8b7a=UnknownStruct28.from_json(data['unknown_struct28_0x6bdd8b7a']),
            unknown_struct28_0xcc53c738=UnknownStruct28.from_json(data['unknown_struct28_0xcc53c738']),
            unknown_struct28_0xbcf93a2a=UnknownStruct28.from_json(data['unknown_struct28_0xbcf93a2a']),
            unknown_struct28_0x6549e3f9=UnknownStruct28.from_json(data['unknown_struct28_0x6549e3f9']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'cursor_model': self.cursor_model,
            'disabled_cursor_model': self.disabled_cursor_model,
            'secondary_cursor_model': self.secondary_cursor_model,
            'unknown_struct182': self.unknown_struct182.to_json(),
            'unknown_struct36': self.unknown_struct36.to_json(),
            'unknown_struct183': self.unknown_struct183.to_json(),
            'unknown_struct28_0xc68bc9ec': self.unknown_struct28_0xc68bc9ec.to_json(),
            'unknown_struct28_0x6bdd8b7a': self.unknown_struct28_0x6bdd8b7a.to_json(),
            'unknown_struct28_0xcc53c738': self.unknown_struct28_0xcc53c738.to_json(),
            'unknown_struct28_0xbcf93a2a': self.unknown_struct28_0xbcf93a2a.to_json(),
            'unknown_struct28_0x6549e3f9': self.unknown_struct28_0x6549e3f9.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_cursor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_disabled_cursor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_secondary_cursor_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct182(data: typing.BinaryIO, property_size: int):
    return UnknownStruct182.from_stream(data, property_size)


def _decode_unknown_struct36(data: typing.BinaryIO, property_size: int):
    return UnknownStruct36.from_stream(data, property_size)


def _decode_unknown_struct183(data: typing.BinaryIO, property_size: int):
    return UnknownStruct183.from_stream(data, property_size)


def _decode_unknown_struct28_0xc68bc9ec(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_unknown_struct28_0x6bdd8b7a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_unknown_struct28_0xcc53c738(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_unknown_struct28_0xbcf93a2a(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


def _decode_unknown_struct28_0x6549e3f9(data: typing.BinaryIO, property_size: int):
    return UnknownStruct28.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf94806a: ('cursor_model', _decode_cursor_model),
    0xd02fb1a1: ('disabled_cursor_model', _decode_disabled_cursor_model),
    0xa74065ce: ('secondary_cursor_model', _decode_secondary_cursor_model),
    0x1743b770: ('unknown_struct182', _decode_unknown_struct182),
    0x3f88e900: ('unknown_struct36', _decode_unknown_struct36),
    0xeb7c1bf2: ('unknown_struct183', _decode_unknown_struct183),
    0xc68bc9ec: ('unknown_struct28_0xc68bc9ec', _decode_unknown_struct28_0xc68bc9ec),
    0x6bdd8b7a: ('unknown_struct28_0x6bdd8b7a', _decode_unknown_struct28_0x6bdd8b7a),
    0xcc53c738: ('unknown_struct28_0xcc53c738', _decode_unknown_struct28_0xcc53c738),
    0xbcf93a2a: ('unknown_struct28_0xbcf93a2a', _decode_unknown_struct28_0xbcf93a2a),
    0x6549e3f9: ('unknown_struct28_0x6549e3f9', _decode_unknown_struct28_0x6549e3f9),
}
