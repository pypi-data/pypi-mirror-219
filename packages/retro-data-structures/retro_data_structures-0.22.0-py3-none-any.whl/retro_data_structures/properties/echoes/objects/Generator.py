# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class Generator(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    random_count: int = dataclasses.field(default=1)
    unique_locations: bool = dataclasses.field(default=False)
    keep_orientation: bool = dataclasses.field(default=False)
    use_originator_transform: bool = dataclasses.field(default=False)
    offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    random_scale_min: float = dataclasses.field(default=1.0)
    random_scale_max: float = dataclasses.field(default=1.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'GENR'

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
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'?\xa6qE')  # 0x3fa67145
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.random_count))

        data.write(b'\x88\x97\x8eI')  # 0x88978e49
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unique_locations))

        data.write(b'\x1e\xb8\xe2T')  # 0x1eb8e254
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.keep_orientation))

        data.write(b'\x03Z^\x10')  # 0x35a5e10
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_originator_transform))

        data.write(b'FGpd')  # 0x46477064
        data.write(b'\x00\x0c')  # size
        self.offset.to_stream(data)

        data.write(b'\xc3\x86\x1bd')  # 0xc3861b64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_scale_min))

        data.write(b'%\xe6\xb4\x85')  # 0x25e6b485
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_scale_max))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            random_count=data['random_count'],
            unique_locations=data['unique_locations'],
            keep_orientation=data['keep_orientation'],
            use_originator_transform=data['use_originator_transform'],
            offset=Vector.from_json(data['offset']),
            random_scale_min=data['random_scale_min'],
            random_scale_max=data['random_scale_max'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'random_count': self.random_count,
            'unique_locations': self.unique_locations,
            'keep_orientation': self.keep_orientation,
            'use_originator_transform': self.use_originator_transform,
            'offset': self.offset.to_json(),
            'random_scale_min': self.random_scale_min,
            'random_scale_max': self.random_scale_max,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Generator.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_random_count(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unique_locations(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_keep_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_originator_transform(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_random_scale_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_random_scale_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x3fa67145: ('random_count', _decode_random_count),
    0x88978e49: ('unique_locations', _decode_unique_locations),
    0x1eb8e254: ('keep_orientation', _decode_keep_orientation),
    0x35a5e10: ('use_originator_transform', _decode_use_originator_transform),
    0x46477064: ('offset', _decode_offset),
    0xc3861b64: ('random_scale_min', _decode_random_scale_min),
    0x25e6b485: ('random_scale_max', _decode_random_scale_max),
}
