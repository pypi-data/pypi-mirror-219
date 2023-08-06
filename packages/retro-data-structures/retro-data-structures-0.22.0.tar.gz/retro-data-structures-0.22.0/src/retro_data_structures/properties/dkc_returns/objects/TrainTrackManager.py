# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct273 import UnknownStruct273
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct274 import UnknownStruct274
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct275 import UnknownStruct275


@dataclasses.dataclass()
class TrainTrackManager(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_struct273: UnknownStruct273 = dataclasses.field(default_factory=UnknownStruct273)
    unknown_struct274: UnknownStruct274 = dataclasses.field(default_factory=UnknownStruct274)
    unknown_struct275: UnknownStruct275 = dataclasses.field(default_factory=UnknownStruct275)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'TMGR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_MoleTrain.rso']

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
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>\xdfW\xb4')  # 0x3edf57b4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct273.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x01\x9c\x93\x92')  # 0x19c9392
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct274.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18q\xba\x9b')  # 0x1871ba9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct275.to_stream(data)
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
            unknown_struct273=UnknownStruct273.from_json(data['unknown_struct273']),
            unknown_struct274=UnknownStruct274.from_json(data['unknown_struct274']),
            unknown_struct275=UnknownStruct275.from_json(data['unknown_struct275']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct273': self.unknown_struct273.to_json(),
            'unknown_struct274': self.unknown_struct274.to_json(),
            'unknown_struct275': self.unknown_struct275.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_struct273(data: typing.BinaryIO, property_size: int):
    return UnknownStruct273.from_stream(data, property_size)


def _decode_unknown_struct274(data: typing.BinaryIO, property_size: int):
    return UnknownStruct274.from_stream(data, property_size)


def _decode_unknown_struct275(data: typing.BinaryIO, property_size: int):
    return UnknownStruct275.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x3edf57b4: ('unknown_struct273', _decode_unknown_struct273),
    0x19c9392: ('unknown_struct274', _decode_unknown_struct274),
    0x1871ba9b: ('unknown_struct275', _decode_unknown_struct275),
}
