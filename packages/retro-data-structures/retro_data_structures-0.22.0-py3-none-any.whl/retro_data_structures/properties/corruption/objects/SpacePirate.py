# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.corruption.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.corruption.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.corruption.archetypes.FriendlyData import FriendlyData
from retro_data_structures.properties.corruption.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.corruption.archetypes.SpacePirateData import SpacePirateData


@dataclasses.dataclass()
class SpacePirate(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    patterned_info: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    friendly_data: FriendlyData = dataclasses.field(default_factory=FriendlyData)
    space_pirate_info: SpacePirateData = dataclasses.field(default_factory=SpacePirateData)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PIRT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['RSO_SpacePirate.rso']

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

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'C\xbb\xb1\xdd')  # 0x43bbb1dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned_info.to_stream(data, default_override={'damage_wait_time': 3.0, 'collision_radius': 0.800000011920929, 'collision_height': 4.5, 'step_up_height': 0.30000001192092896, 'creature_size': 1, 'turn_speed': 360.0, 'detection_range': 50.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'average_attack_time': 1.0, 'attack_time_variation': 0.5})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6w\xaf,')  # 0xe677af2c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.friendly_data.to_stream(data, default_override={'is_grabbable': True})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdd\xa1\xca\xce')  # 0xdda1cace
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.space_pirate_info.to_stream(data)
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
            actor_information=ActorParameters.from_json(data['actor_information']),
            patterned_info=PatternedAITypedef.from_json(data['patterned_info']),
            friendly_data=FriendlyData.from_json(data['friendly_data']),
            space_pirate_info=SpacePirateData.from_json(data['space_pirate_info']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'patterned_info': self.patterned_info.to_json(),
            'friendly_data': self.friendly_data.to_json(),
            'space_pirate_info': self.space_pirate_info.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_patterned_info(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'damage_wait_time': 3.0, 'collision_radius': 0.800000011920929, 'collision_height': 4.5, 'step_up_height': 0.30000001192092896, 'creature_size': 1, 'turn_speed': 360.0, 'detection_range': 50.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'average_attack_time': 1.0, 'attack_time_variation': 0.5})


def _decode_friendly_data(data: typing.BinaryIO, property_size: int):
    return FriendlyData.from_stream(data, property_size, default_override={'is_grabbable': True})


def _decode_space_pirate_info(data: typing.BinaryIO, property_size: int):
    return SpacePirateData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x43bbb1dd: ('patterned_info', _decode_patterned_info),
    0xe677af2c: ('friendly_data', _decode_friendly_data),
    0xdda1cace: ('space_pirate_info', _decode_space_pirate_info),
}
