# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.AuroraUnit2Data import AuroraUnit2Data
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef


@dataclasses.dataclass()
class AuroraUnit2(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    aurora_unit2_data_0x26594deb: AuroraUnit2Data = dataclasses.field(default_factory=AuroraUnit2Data)
    aurora_unit2_data_0x857bee96: AuroraUnit2Data = dataclasses.field(default_factory=AuroraUnit2Data)
    aurora_unit2_data_0xe74db2b8: AuroraUnit2Data = dataclasses.field(default_factory=AuroraUnit2Data)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'AUR2'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_AuroraUnit2.rso']

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

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'turn_speed': 360.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&YM\xeb')  # 0x26594deb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aurora_unit2_data_0x26594deb.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x85{\xee\x96')  # 0x857bee96
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aurora_unit2_data_0x857bee96.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7M\xb2\xb8')  # 0xe74db2b8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.aurora_unit2_data_0xe74db2b8.to_stream(data)
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
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            aurora_unit2_data_0x26594deb=AuroraUnit2Data.from_json(data['aurora_unit2_data_0x26594deb']),
            aurora_unit2_data_0x857bee96=AuroraUnit2Data.from_json(data['aurora_unit2_data_0x857bee96']),
            aurora_unit2_data_0xe74db2b8=AuroraUnit2Data.from_json(data['aurora_unit2_data_0xe74db2b8']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'aurora_unit2_data_0x26594deb': self.aurora_unit2_data_0x26594deb.to_json(),
            'aurora_unit2_data_0x857bee96': self.aurora_unit2_data_0x857bee96.to_json(),
            'aurora_unit2_data_0xe74db2b8': self.aurora_unit2_data_0xe74db2b8.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'turn_speed': 360.0})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_aurora_unit2_data_0x26594deb(data: typing.BinaryIO, property_size: int):
    return AuroraUnit2Data.from_stream(data, property_size)


def _decode_aurora_unit2_data_0x857bee96(data: typing.BinaryIO, property_size: int):
    return AuroraUnit2Data.from_stream(data, property_size)


def _decode_aurora_unit2_data_0xe74db2b8(data: typing.BinaryIO, property_size: int):
    return AuroraUnit2Data.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x26594deb: ('aurora_unit2_data_0x26594deb', _decode_aurora_unit2_data_0x26594deb),
    0x857bee96: ('aurora_unit2_data_0x857bee96', _decode_aurora_unit2_data_0x857bee96),
    0xe74db2b8: ('aurora_unit2_data_0xe74db2b8', _decode_aurora_unit2_data_0xe74db2b8),
}
