# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.DarkSamusData import DarkSamusData
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.corruption.archetypes.UnknownStruct27 import UnknownStruct27


@dataclasses.dataclass()
class DarkSamus(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_struct27: UnknownStruct27 = dataclasses.field(default_factory=UnknownStruct27)
    dark_samus_properties: DarkSamusData = dataclasses.field(default_factory=DarkSamusData)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    dark_samus_data: DarkSamusData = dataclasses.field(default_factory=DarkSamusData)
    patterned_ai_0x1464ae05: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    dark_samus_properties_elite_difficulty: DarkSamusData = dataclasses.field(default_factory=DarkSamusData)
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
        return 'DRKS'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_DarkSamus.rso']

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

        data.write(b'\x02\x14\xa7\xeb')  # 0x214a7eb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct27.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02\xc4<A')  # 0x2c43c41
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_samus_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdd\x04/\xe0')  # 0xdd042fe0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_samus_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x14d\xae\x05')  # 0x1464ae05
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_ai_0x1464ae05.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd0b\x1c\x92')  # 0xd0621c92
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_samus_properties_elite_difficulty.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xd0\x06s')  # 0x24d00673
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_ai_0x24d00673.to_stream(data)
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
            unknown_struct27=UnknownStruct27.from_json(data['unknown_struct27']),
            dark_samus_properties=DarkSamusData.from_json(data['dark_samus_properties']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            dark_samus_data=DarkSamusData.from_json(data['dark_samus_data']),
            patterned_ai_0x1464ae05=PatternedAITypedef.from_json(data['patterned_ai_0x1464ae05']),
            dark_samus_properties_elite_difficulty=DarkSamusData.from_json(data['dark_samus_properties_elite_difficulty']),
            patterned_ai_0x24d00673=PatternedAITypedef.from_json(data['patterned_ai_0x24d00673']),
            actor_information=ActorParameters.from_json(data['actor_information']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct27': self.unknown_struct27.to_json(),
            'dark_samus_properties': self.dark_samus_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'dark_samus_data': self.dark_samus_data.to_json(),
            'patterned_ai_0x1464ae05': self.patterned_ai_0x1464ae05.to_json(),
            'dark_samus_properties_elite_difficulty': self.dark_samus_properties_elite_difficulty.to_json(),
            'patterned_ai_0x24d00673': self.patterned_ai_0x24d00673.to_json(),
            'actor_information': self.actor_information.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_struct27(data: typing.BinaryIO, property_size: int):
    return UnknownStruct27.from_stream(data, property_size)


def _decode_dark_samus_properties(data: typing.BinaryIO, property_size: int):
    return DarkSamusData.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_dark_samus_data(data: typing.BinaryIO, property_size: int):
    return DarkSamusData.from_stream(data, property_size)


def _decode_patterned_ai_0x1464ae05(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_dark_samus_properties_elite_difficulty(data: typing.BinaryIO, property_size: int):
    return DarkSamusData.from_stream(data, property_size)


def _decode_patterned_ai_0x24d00673(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x214a7eb: ('unknown_struct27', _decode_unknown_struct27),
    0x2c43c41: ('dark_samus_properties', _decode_dark_samus_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0xdd042fe0: ('dark_samus_data', _decode_dark_samus_data),
    0x1464ae05: ('patterned_ai_0x1464ae05', _decode_patterned_ai_0x1464ae05),
    0xd0621c92: ('dark_samus_properties_elite_difficulty', _decode_dark_samus_properties_elite_difficulty),
    0x24d00673: ('patterned_ai_0x24d00673', _decode_patterned_ai_0x24d00673),
    0x7e397fed: ('actor_information', _decode_actor_information),
}
