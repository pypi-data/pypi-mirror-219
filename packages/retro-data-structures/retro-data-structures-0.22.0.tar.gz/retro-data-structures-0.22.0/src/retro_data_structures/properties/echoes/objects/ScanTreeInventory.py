# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.echoes as enums
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.ScannableParameters import ScannableParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ScanTreeInventory(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    name_string_table: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    name_string_name: str = dataclasses.field(default='')
    inventory_slot: enums.InventorySlot = dataclasses.field(default=enums.InventorySlot.PowerBeam)
    scannable_parameters: ScannableParameters = dataclasses.field(default_factory=ScannableParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SCIN'

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
        data.write(b'\x00\x05')  # 5 properties

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

        data.write(b'=2o\x90')  # 0x3d326f90
        data.write(b'\x00\x04')  # size
        self.inventory_slot.to_stream(data)

        data.write(b'-\xa1\xec3')  # 0x2da1ec33
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scannable_parameters.to_stream(data)
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
            name_string_table=data['name_string_table'],
            name_string_name=data['name_string_name'],
            inventory_slot=enums.InventorySlot.from_json(data['inventory_slot']),
            scannable_parameters=ScannableParameters.from_json(data['scannable_parameters']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'name_string_table': self.name_string_table,
            'name_string_name': self.name_string_name,
            'inventory_slot': self.inventory_slot.to_json(),
            'scannable_parameters': self.scannable_parameters.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_name_string_table(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.name_string_table)

    def _dependencies_for_scannable_parameters(self, asset_manager):
        yield from self.scannable_parameters.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_name_string_table, "name_string_table", "AssetId"),
            (self._dependencies_for_scannable_parameters, "scannable_parameters", "ScannableParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ScanTreeInventory.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_name_string_table(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_name_string_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_inventory_slot(data: typing.BinaryIO, property_size: int):
    return enums.InventorySlot.from_stream(data)


def _decode_scannable_parameters(data: typing.BinaryIO, property_size: int):
    return ScannableParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x46219bac: ('name_string_table', _decode_name_string_table),
    0x32698bd6: ('name_string_name', _decode_name_string_name),
    0x3d326f90: ('inventory_slot', _decode_inventory_slot),
    0x2da1ec33: ('scannable_parameters', _decode_scannable_parameters),
}
