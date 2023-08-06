# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.corruption.archetypes.RundasData import RundasData
from retro_data_structures.properties.corruption.archetypes.UnknownStruct55 import UnknownStruct55


@dataclasses.dataclass()
class Rundas(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_struct55: UnknownStruct55 = dataclasses.field(default_factory=UnknownStruct55)
    rundas_data_0x9d90d49f: RundasData = dataclasses.field(default_factory=RundasData)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    rundas_data_0x877b2ce9: RundasData = dataclasses.field(default_factory=RundasData)
    patterned_ai_0x1464ae05: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    rundas_data_0xce6183d8: RundasData = dataclasses.field(default_factory=RundasData)
    patterned_ai_0x24d00673: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'RUND'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_Rundas.rso']

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
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa6y\x07\t')  # 0xa6790709
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct55.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9d\x90\xd4\x9f')  # 0x9d90d49f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rundas_data_0x9d90d49f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'leash_radius': 100.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x87{,\xe9')  # 0x877b2ce9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rundas_data_0x877b2ce9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x14d\xae\x05')  # 0x1464ae05
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_ai_0x1464ae05.to_stream(data, default_override={'leash_radius': 100.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcea\x83\xd8')  # 0xce6183d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rundas_data_0xce6183d8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xd0\x06s')  # 0x24d00673
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_ai_0x24d00673.to_stream(data, default_override={'leash_radius': 100.0})
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

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            unknown_struct55=UnknownStruct55.from_json(data['unknown_struct55']),
            rundas_data_0x9d90d49f=RundasData.from_json(data['rundas_data_0x9d90d49f']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            rundas_data_0x877b2ce9=RundasData.from_json(data['rundas_data_0x877b2ce9']),
            patterned_ai_0x1464ae05=PatternedAITypedef.from_json(data['patterned_ai_0x1464ae05']),
            rundas_data_0xce6183d8=RundasData.from_json(data['rundas_data_0xce6183d8']),
            patterned_ai_0x24d00673=PatternedAITypedef.from_json(data['patterned_ai_0x24d00673']),
            actor_information=ActorParameters.from_json(data['actor_information']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct55': self.unknown_struct55.to_json(),
            'rundas_data_0x9d90d49f': self.rundas_data_0x9d90d49f.to_json(),
            'patterned': self.patterned.to_json(),
            'rundas_data_0x877b2ce9': self.rundas_data_0x877b2ce9.to_json(),
            'patterned_ai_0x1464ae05': self.patterned_ai_0x1464ae05.to_json(),
            'rundas_data_0xce6183d8': self.rundas_data_0xce6183d8.to_json(),
            'patterned_ai_0x24d00673': self.patterned_ai_0x24d00673.to_json(),
            'actor_information': self.actor_information.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_struct55(data: typing.BinaryIO, property_size: int):
    return UnknownStruct55.from_stream(data, property_size)


def _decode_rundas_data_0x9d90d49f(data: typing.BinaryIO, property_size: int):
    return RundasData.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'leash_radius': 100.0})


def _decode_rundas_data_0x877b2ce9(data: typing.BinaryIO, property_size: int):
    return RundasData.from_stream(data, property_size)


def _decode_patterned_ai_0x1464ae05(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'leash_radius': 100.0})


def _decode_rundas_data_0xce6183d8(data: typing.BinaryIO, property_size: int):
    return RundasData.from_stream(data, property_size)


def _decode_patterned_ai_0x24d00673(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'leash_radius': 100.0})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xa6790709: ('unknown_struct55', _decode_unknown_struct55),
    0x9d90d49f: ('rundas_data_0x9d90d49f', _decode_rundas_data_0x9d90d49f),
    0xb3774750: ('patterned', _decode_patterned),
    0x877b2ce9: ('rundas_data_0x877b2ce9', _decode_rundas_data_0x877b2ce9),
    0x1464ae05: ('patterned_ai_0x1464ae05', _decode_patterned_ai_0x1464ae05),
    0xce6183d8: ('rundas_data_0xce6183d8', _decode_rundas_data_0xce6183d8),
    0x24d00673: ('patterned_ai_0x24d00673', _decode_patterned_ai_0x24d00673),
    0x7e397fed: ('actor_information', _decode_actor_information),
}
