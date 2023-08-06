# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ScanTreeMenu(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    name_string_table: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    name_string_name: str = dataclasses.field(default='')
    unknown_0x0261a4e0: int = dataclasses.field(default=0)
    menu_options_string_table: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    option_1_string_name: str = dataclasses.field(default='')
    unknown_0x50bce632: int = dataclasses.field(default=0)
    option_2_string_name: str = dataclasses.field(default='')
    unknown_0x420949dc: int = dataclasses.field(default=0)
    option_3_string_name: str = dataclasses.field(default='')
    unknown_0xfab52eb9: int = dataclasses.field(default=0)
    option_4_string_name: str = dataclasses.field(default='')
    unknown_0x67621600: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SCMN'

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
        data.write(b'\x00\r')  # 13 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F!\x9b\xac')  # 0x46219bac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.name_string_table))

        data.write(b'2i\x8b\xd6')  # 0x32698bd6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.name_string_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02a\xa4\xe0')  # 0x261a4e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x0261a4e0))

        data.write(b'\xa6\xa8t\xe9')  # 0xa6a874e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.menu_options_string_table))

        data.write(b'0S\x19$')  # 0x30531924
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.option_1_string_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\xbc\xe62')  # 0x50bce632
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x50bce632))

        data.write(b'\x01\xbb\x03\xb9')  # 0x1bb03b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.option_2_string_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'B\tI\xdc')  # 0x420949dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x420949dc))

        data.write(b'\xa7\xcc\x08\r')  # 0xa7cc080d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.option_3_string_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfa\xb5.\xb9')  # 0xfab52eb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xfab52eb9))

        data.write(b'bk6\x83')  # 0x626b3683
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.option_4_string_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'gb\x16\x00')  # 0x67621600
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x67621600))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            name_string_table=data['name_string_table'],
            name_string_name=data['name_string_name'],
            unknown_0x0261a4e0=data['unknown_0x0261a4e0'],
            menu_options_string_table=data['menu_options_string_table'],
            option_1_string_name=data['option_1_string_name'],
            unknown_0x50bce632=data['unknown_0x50bce632'],
            option_2_string_name=data['option_2_string_name'],
            unknown_0x420949dc=data['unknown_0x420949dc'],
            option_3_string_name=data['option_3_string_name'],
            unknown_0xfab52eb9=data['unknown_0xfab52eb9'],
            option_4_string_name=data['option_4_string_name'],
            unknown_0x67621600=data['unknown_0x67621600'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'name_string_table': self.name_string_table,
            'name_string_name': self.name_string_name,
            'unknown_0x0261a4e0': self.unknown_0x0261a4e0,
            'menu_options_string_table': self.menu_options_string_table,
            'option_1_string_name': self.option_1_string_name,
            'unknown_0x50bce632': self.unknown_0x50bce632,
            'option_2_string_name': self.option_2_string_name,
            'unknown_0x420949dc': self.unknown_0x420949dc,
            'option_3_string_name': self.option_3_string_name,
            'unknown_0xfab52eb9': self.unknown_0xfab52eb9,
            'option_4_string_name': self.option_4_string_name,
            'unknown_0x67621600': self.unknown_0x67621600,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_name_string_table(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.name_string_table)

    def _dependencies_for_menu_options_string_table(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.menu_options_string_table)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_name_string_table, "name_string_table", "AssetId"),
            (self._dependencies_for_menu_options_string_table, "menu_options_string_table", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ScanTreeMenu.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_name_string_table(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_name_string_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x0261a4e0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_menu_options_string_table(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_option_1_string_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x50bce632(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_option_2_string_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x420949dc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_option_3_string_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0xfab52eb9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_option_4_string_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_unknown_0x67621600(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x46219bac: ('name_string_table', _decode_name_string_table),
    0x32698bd6: ('name_string_name', _decode_name_string_name),
    0x261a4e0: ('unknown_0x0261a4e0', _decode_unknown_0x0261a4e0),
    0xa6a874e9: ('menu_options_string_table', _decode_menu_options_string_table),
    0x30531924: ('option_1_string_name', _decode_option_1_string_name),
    0x50bce632: ('unknown_0x50bce632', _decode_unknown_0x50bce632),
    0x1bb03b9: ('option_2_string_name', _decode_option_2_string_name),
    0x420949dc: ('unknown_0x420949dc', _decode_unknown_0x420949dc),
    0xa7cc080d: ('option_3_string_name', _decode_option_3_string_name),
    0xfab52eb9: ('unknown_0xfab52eb9', _decode_unknown_0xfab52eb9),
    0x626b3683: ('option_4_string_name', _decode_option_4_string_name),
    0x67621600: ('unknown_0x67621600', _decode_unknown_0x67621600),
}
