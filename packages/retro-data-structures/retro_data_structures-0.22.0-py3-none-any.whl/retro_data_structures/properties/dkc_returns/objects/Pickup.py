# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.PickupData import PickupData
from retro_data_structures.properties.dkc_returns.archetypes.SavedStateID import SavedStateID
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct244 import UnknownStruct244
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class Pickup(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    object_id: SavedStateID = dataclasses.field(default_factory=SavedStateID)
    collision_size: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    ghost_model: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    ghost_character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    pickup_data: PickupData = dataclasses.field(default_factory=PickupData)
    can_cause_damage: bool = dataclasses.field(default=False)
    unknown_struct244: UnknownStruct244 = dataclasses.field(default_factory=UnknownStruct244)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PCKP'

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16\xd9\xa7]')  # 0x16d9a75d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.object_id.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b':>\x03\xba')  # 0x3a3e03ba
        data.write(b'\x00\x0c')  # size
        self.collision_size.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b',\xf4\tx')  # 0x2cf40978
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ghost_model))

        data.write(b'1(\x97o')  # 0x3128976f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ghost_character_animation_information.to_stream(data)
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

        data.write(b'\xd5E\xf3k')  # 0xd545f36b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pickup_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb07M4')  # 0xb0374d34
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_cause_damage))

        data.write(b'\x9d\xa7\xab\xfa')  # 0x9da7abfa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct244.to_stream(data)
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
            object_id=SavedStateID.from_json(data['object_id']),
            collision_size=Vector.from_json(data['collision_size']),
            collision_offset=Vector.from_json(data['collision_offset']),
            model=data['model'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            ghost_model=data['ghost_model'],
            ghost_character_animation_information=AnimationParameters.from_json(data['ghost_character_animation_information']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            pickup_data=PickupData.from_json(data['pickup_data']),
            can_cause_damage=data['can_cause_damage'],
            unknown_struct244=UnknownStruct244.from_json(data['unknown_struct244']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'object_id': self.object_id.to_json(),
            'collision_size': self.collision_size.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'model': self.model,
            'character_animation_information': self.character_animation_information.to_json(),
            'ghost_model': self.ghost_model,
            'ghost_character_animation_information': self.ghost_character_animation_information.to_json(),
            'actor_information': self.actor_information.to_json(),
            'pickup_data': self.pickup_data.to_json(),
            'can_cause_damage': self.can_cause_damage,
            'unknown_struct244': self.unknown_struct244.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_object_id(data: typing.BinaryIO, property_size: int):
    return SavedStateID.from_stream(data, property_size)


def _decode_collision_size(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_ghost_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ghost_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_pickup_data(data: typing.BinaryIO, property_size: int):
    return PickupData.from_stream(data, property_size)


def _decode_can_cause_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_struct244(data: typing.BinaryIO, property_size: int):
    return UnknownStruct244.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x16d9a75d: ('object_id', _decode_object_id),
    0x3a3e03ba: ('collision_size', _decode_collision_size),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xc27ffa8f: ('model', _decode_model),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0x2cf40978: ('ghost_model', _decode_ghost_model),
    0x3128976f: ('ghost_character_animation_information', _decode_ghost_character_animation_information),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xd545f36b: ('pickup_data', _decode_pickup_data),
    0xb0374d34: ('can_cause_damage', _decode_can_cause_damage),
    0x9da7abfa: ('unknown_struct244', _decode_unknown_struct244),
}
