# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.SpawnPointStruct import SpawnPointStruct


@dataclasses.dataclass()
class SpawnPoint(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    first_spawn: bool = dataclasses.field(default=True)
    morphed: bool = dataclasses.field(default=False)
    amount: SpawnPointStruct = dataclasses.field(default_factory=SpawnPointStruct)
    capacity: SpawnPointStruct = dataclasses.field(default_factory=SpawnPointStruct)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SPWN'

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

        data.write(b'\xc0\xe4R\x1b')  # 0xc0e4521b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.first_spawn))

        data.write(b'\xb9\xc4\x0f\x92')  # 0xb9c40f92
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.morphed))

        data.write(b'L\x1dL\xc9')  # 0x4c1d4cc9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.amount.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@\x81\xbf\x95')  # 0x4081bf95
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.capacity.to_stream(data)
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
            first_spawn=data['first_spawn'],
            morphed=data['morphed'],
            amount=SpawnPointStruct.from_json(data['amount']),
            capacity=SpawnPointStruct.from_json(data['capacity']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'first_spawn': self.first_spawn,
            'morphed': self.morphed,
            'amount': self.amount.to_json(),
            'capacity': self.capacity.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_amount(self, asset_manager):
        yield from self.amount.dependencies_for(asset_manager)

    def _dependencies_for_capacity(self, asset_manager):
        yield from self.capacity.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_amount, "amount", "SpawnPointStruct"),
            (self._dependencies_for_capacity, "capacity", "SpawnPointStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SpawnPoint.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_first_spawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_morphed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_amount(data: typing.BinaryIO, property_size: int):
    return SpawnPointStruct.from_stream(data, property_size)


def _decode_capacity(data: typing.BinaryIO, property_size: int):
    return SpawnPointStruct.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xc0e4521b: ('first_spawn', _decode_first_spawn),
    0xb9c40f92: ('morphed', _decode_morphed),
    0x4c1d4cc9: ('amount', _decode_amount),
    0x4081bf95: ('capacity', _decode_capacity),
}
