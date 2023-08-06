# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.corruption.archetypes.SeedBoss2PrimeBotData import SeedBoss2PrimeBotData
from retro_data_structures.properties.corruption.archetypes.UnknownStruct58 import UnknownStruct58


@dataclasses.dataclass()
class SeedBoss2PrimeBot(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    unknown_struct58: UnknownStruct58 = dataclasses.field(default_factory=UnknownStruct58)
    seed_boss2_prime_bot_data_0xb1461bc0: SeedBoss2PrimeBotData = dataclasses.field(default_factory=SeedBoss2PrimeBotData)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    seed_boss2_prime_bot_data_0xd578f188: SeedBoss2PrimeBotData = dataclasses.field(default_factory=SeedBoss2PrimeBotData)
    patterned_ai_0x1464ae05: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    seed_boss2_prime_bot_data_0xe3585b48: SeedBoss2PrimeBotData = dataclasses.field(default_factory=SeedBoss2PrimeBotData)
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
        return 'SB2P'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_SeedBoss2.rso']

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

        data.write(b'\x96x(s')  # 0x96782873
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct58.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb1F\x1b\xc0')  # 0xb1461bc0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss2_prime_bot_data_0xb1461bc0.to_stream(data)
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

        data.write(b'\xd5x\xf1\x88')  # 0xd578f188
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss2_prime_bot_data_0xd578f188.to_stream(data)
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

        data.write(b'\xe3X[H')  # 0xe3585b48
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss2_prime_bot_data_0xe3585b48.to_stream(data)
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
            unknown_struct58=UnknownStruct58.from_json(data['unknown_struct58']),
            seed_boss2_prime_bot_data_0xb1461bc0=SeedBoss2PrimeBotData.from_json(data['seed_boss2_prime_bot_data_0xb1461bc0']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            seed_boss2_prime_bot_data_0xd578f188=SeedBoss2PrimeBotData.from_json(data['seed_boss2_prime_bot_data_0xd578f188']),
            patterned_ai_0x1464ae05=PatternedAITypedef.from_json(data['patterned_ai_0x1464ae05']),
            seed_boss2_prime_bot_data_0xe3585b48=SeedBoss2PrimeBotData.from_json(data['seed_boss2_prime_bot_data_0xe3585b48']),
            patterned_ai_0x24d00673=PatternedAITypedef.from_json(data['patterned_ai_0x24d00673']),
            actor_information=ActorParameters.from_json(data['actor_information']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'unknown_struct58': self.unknown_struct58.to_json(),
            'seed_boss2_prime_bot_data_0xb1461bc0': self.seed_boss2_prime_bot_data_0xb1461bc0.to_json(),
            'patterned': self.patterned.to_json(),
            'seed_boss2_prime_bot_data_0xd578f188': self.seed_boss2_prime_bot_data_0xd578f188.to_json(),
            'patterned_ai_0x1464ae05': self.patterned_ai_0x1464ae05.to_json(),
            'seed_boss2_prime_bot_data_0xe3585b48': self.seed_boss2_prime_bot_data_0xe3585b48.to_json(),
            'patterned_ai_0x24d00673': self.patterned_ai_0x24d00673.to_json(),
            'actor_information': self.actor_information.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_unknown_struct58(data: typing.BinaryIO, property_size: int):
    return UnknownStruct58.from_stream(data, property_size)


def _decode_seed_boss2_prime_bot_data_0xb1461bc0(data: typing.BinaryIO, property_size: int):
    return SeedBoss2PrimeBotData.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_seed_boss2_prime_bot_data_0xd578f188(data: typing.BinaryIO, property_size: int):
    return SeedBoss2PrimeBotData.from_stream(data, property_size)


def _decode_patterned_ai_0x1464ae05(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_seed_boss2_prime_bot_data_0xe3585b48(data: typing.BinaryIO, property_size: int):
    return SeedBoss2PrimeBotData.from_stream(data, property_size)


def _decode_patterned_ai_0x24d00673(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x96782873: ('unknown_struct58', _decode_unknown_struct58),
    0xb1461bc0: ('seed_boss2_prime_bot_data_0xb1461bc0', _decode_seed_boss2_prime_bot_data_0xb1461bc0),
    0xb3774750: ('patterned', _decode_patterned),
    0xd578f188: ('seed_boss2_prime_bot_data_0xd578f188', _decode_seed_boss2_prime_bot_data_0xd578f188),
    0x1464ae05: ('patterned_ai_0x1464ae05', _decode_patterned_ai_0x1464ae05),
    0xe3585b48: ('seed_boss2_prime_bot_data_0xe3585b48', _decode_seed_boss2_prime_bot_data_0xe3585b48),
    0x24d00673: ('patterned_ai_0x24d00673', _decode_patterned_ai_0x24d00673),
    0x7e397fed: ('actor_information', _decode_actor_information),
}
