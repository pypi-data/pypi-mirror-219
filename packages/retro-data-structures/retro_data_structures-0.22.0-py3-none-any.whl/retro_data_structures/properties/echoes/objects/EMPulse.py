# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class EMPulse(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    initial_size: float = dataclasses.field(default=0.10000000149011612)
    final_size: float = dataclasses.field(default=34.0)
    duration: float = dataclasses.field(default=1.3329999446868896)
    unknown_0x96bd6426: float = dataclasses.field(default=1.0)
    unknown_0xd7aa5ba0: float = dataclasses.field(default=3.0)
    backward_forward_sweep_chance: float = dataclasses.field(default=0.4000000059604645)
    unknown_0xce54e50e: float = dataclasses.field(default=0.800000011920929)
    explosion: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'EMPU'

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data, default_override={'active': False})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'cm\xf2\xdb')  # 0x636df2db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_size))

        data.write(b'\x1ef\x86\xfe')  # 0x1e6686fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.final_size))

        data.write(b'\x8bQ\xe2?')  # 0x8b51e23f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.duration))

        data.write(b'\x96\xbdd&')  # 0x96bd6426
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x96bd6426))

        data.write(b'\xd7\xaa[\xa0')  # 0xd7aa5ba0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd7aa5ba0))

        data.write(b'\x15\xeb\xb6\xe9')  # 0x15ebb6e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.backward_forward_sweep_chance))

        data.write(b'\xceT\xe5\x0e')  # 0xce54e50e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xce54e50e))

        data.write(b'\xd8\xc6\xd1\\')  # 0xd8c6d15c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.explosion))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            initial_size=data['initial_size'],
            final_size=data['final_size'],
            duration=data['duration'],
            unknown_0x96bd6426=data['unknown_0x96bd6426'],
            unknown_0xd7aa5ba0=data['unknown_0xd7aa5ba0'],
            backward_forward_sweep_chance=data['backward_forward_sweep_chance'],
            unknown_0xce54e50e=data['unknown_0xce54e50e'],
            explosion=data['explosion'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'initial_size': self.initial_size,
            'final_size': self.final_size,
            'duration': self.duration,
            'unknown_0x96bd6426': self.unknown_0x96bd6426,
            'unknown_0xd7aa5ba0': self.unknown_0xd7aa5ba0,
            'backward_forward_sweep_chance': self.backward_forward_sweep_chance,
            'unknown_0xce54e50e': self.unknown_0xce54e50e,
            'explosion': self.explosion,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_explosion(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.explosion)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_explosion, "explosion", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for EMPulse.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size, default_override={'active': False})


def _decode_initial_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_final_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x96bd6426(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd7aa5ba0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_backward_forward_sweep_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xce54e50e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x636df2db: ('initial_size', _decode_initial_size),
    0x1e6686fe: ('final_size', _decode_final_size),
    0x8b51e23f: ('duration', _decode_duration),
    0x96bd6426: ('unknown_0x96bd6426', _decode_unknown_0x96bd6426),
    0xd7aa5ba0: ('unknown_0xd7aa5ba0', _decode_unknown_0xd7aa5ba0),
    0x15ebb6e9: ('backward_forward_sweep_chance', _decode_backward_forward_sweep_chance),
    0xce54e50e: ('unknown_0xce54e50e', _decode_unknown_0xce54e50e),
    0xd8c6d15c: ('explosion', _decode_explosion),
}
