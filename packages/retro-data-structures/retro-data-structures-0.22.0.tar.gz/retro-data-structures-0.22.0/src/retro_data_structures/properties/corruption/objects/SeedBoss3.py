# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.corruption.archetypes.SeedBoss3Data import SeedBoss3Data
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class SeedBoss3(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    seed_boss3_data_0xfd27ed67: SeedBoss3Data = dataclasses.field(default_factory=SeedBoss3Data)
    seed_boss3_data_0x5292969e: SeedBoss3Data = dataclasses.field(default_factory=SeedBoss3Data)
    seed_boss3_data_0xcf9d77e8: SeedBoss3Data = dataclasses.field(default_factory=SeedBoss3Data)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    patterned_ai_0x5c056cef: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    patterned_ai_0x8be7ecb7: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
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
        return 'BOS3'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_SeedBoss3.rso']

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

        data.write(b"\xfd'\xedg")  # 0xfd27ed67
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss3_data_0xfd27ed67.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'R\x92\x96\x9e')  # 0x5292969e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss3_data_0x5292969e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcf\x9dw\xe8')  # 0xcf9d77e8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss3_data_0xcf9d77e8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data, default_override={'mass': 1000.0, 'damage_wait_time': 0.009999999776482582, 'creature_size': 2, 'turn_speed': 90.0, 'grapple_icon_offset': Vector(x=0.0, y=2.0, z=-0.5)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\\\x05l\xef')  # 0x5c056cef
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_ai_0x5c056cef.to_stream(data, default_override={'mass': 1000.0, 'damage_wait_time': 0.009999999776482582, 'creature_size': 2, 'turn_speed': 90.0, 'grapple_icon_offset': Vector(x=0.0, y=2.0, z=-0.5)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\xe7\xec\xb7')  # 0x8be7ecb7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_ai_0x8be7ecb7.to_stream(data, default_override={'mass': 1000.0, 'damage_wait_time': 0.009999999776482582, 'creature_size': 2, 'turn_speed': 90.0, 'grapple_icon_offset': Vector(x=0.0, y=2.0, z=-0.5)})
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
            seed_boss3_data_0xfd27ed67=SeedBoss3Data.from_json(data['seed_boss3_data_0xfd27ed67']),
            seed_boss3_data_0x5292969e=SeedBoss3Data.from_json(data['seed_boss3_data_0x5292969e']),
            seed_boss3_data_0xcf9d77e8=SeedBoss3Data.from_json(data['seed_boss3_data_0xcf9d77e8']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            patterned_ai_0x5c056cef=PatternedAITypedef.from_json(data['patterned_ai_0x5c056cef']),
            patterned_ai_0x8be7ecb7=PatternedAITypedef.from_json(data['patterned_ai_0x8be7ecb7']),
            actor_information=ActorParameters.from_json(data['actor_information']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'seed_boss3_data_0xfd27ed67': self.seed_boss3_data_0xfd27ed67.to_json(),
            'seed_boss3_data_0x5292969e': self.seed_boss3_data_0x5292969e.to_json(),
            'seed_boss3_data_0xcf9d77e8': self.seed_boss3_data_0xcf9d77e8.to_json(),
            'patterned': self.patterned.to_json(),
            'patterned_ai_0x5c056cef': self.patterned_ai_0x5c056cef.to_json(),
            'patterned_ai_0x8be7ecb7': self.patterned_ai_0x8be7ecb7.to_json(),
            'actor_information': self.actor_information.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_seed_boss3_data_0xfd27ed67(data: typing.BinaryIO, property_size: int):
    return SeedBoss3Data.from_stream(data, property_size)


def _decode_seed_boss3_data_0x5292969e(data: typing.BinaryIO, property_size: int):
    return SeedBoss3Data.from_stream(data, property_size)


def _decode_seed_boss3_data_0xcf9d77e8(data: typing.BinaryIO, property_size: int):
    return SeedBoss3Data.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'mass': 1000.0, 'damage_wait_time': 0.009999999776482582, 'creature_size': 2, 'turn_speed': 90.0, 'grapple_icon_offset': Vector(x=0.0, y=2.0, z=-0.5)})


def _decode_patterned_ai_0x5c056cef(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'mass': 1000.0, 'damage_wait_time': 0.009999999776482582, 'creature_size': 2, 'turn_speed': 90.0, 'grapple_icon_offset': Vector(x=0.0, y=2.0, z=-0.5)})


def _decode_patterned_ai_0x8be7ecb7(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'mass': 1000.0, 'damage_wait_time': 0.009999999776482582, 'creature_size': 2, 'turn_speed': 90.0, 'grapple_icon_offset': Vector(x=0.0, y=2.0, z=-0.5)})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xfd27ed67: ('seed_boss3_data_0xfd27ed67', _decode_seed_boss3_data_0xfd27ed67),
    0x5292969e: ('seed_boss3_data_0x5292969e', _decode_seed_boss3_data_0x5292969e),
    0xcf9d77e8: ('seed_boss3_data_0xcf9d77e8', _decode_seed_boss3_data_0xcf9d77e8),
    0xb3774750: ('patterned', _decode_patterned),
    0x5c056cef: ('patterned_ai_0x5c056cef', _decode_patterned_ai_0x5c056cef),
    0x8be7ecb7: ('patterned_ai_0x8be7ecb7', _decode_patterned_ai_0x8be7ecb7),
    0x7e397fed: ('actor_information', _decode_actor_information),
}
