# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.ReactiveActorBehaviors import ReactiveActorBehaviors
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class ReactiveActor(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    detection_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    detection_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    start_enabled: bool = dataclasses.field(default=True)
    texture_set: int = dataclasses.field(default=0)
    behaviors: ReactiveActorBehaviors = dataclasses.field(default_factory=ReactiveActorBehaviors)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'REAC'

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

        data.write(b'lD\x7f\xf0')  # 0x6c447ff0
        data.write(b'\x00\x0c')  # size
        self.detection_box.to_stream(data)

        data.write(b'=\xafS\x02')  # 0x3daf5302
        data.write(b'\x00\x0c')  # size
        self.detection_offset.to_stream(data)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'{\xc2\xf6\xcf')  # 0x7bc2f6cf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character.to_stream(data)
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

        data.write(b'/|Y\xdc')  # 0x2f7c59dc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_enabled))

        data.write(b'k@\xac\xef')  # 0x6b40acef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.texture_set))

        data.write(b'\xc7\xbd\x10"')  # 0xc7bd1022
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.behaviors.to_stream(data)
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
            detection_box=Vector.from_json(data['detection_box']),
            detection_offset=Vector.from_json(data['detection_offset']),
            model=data['model'],
            character=AnimationParameters.from_json(data['character']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            start_enabled=data['start_enabled'],
            texture_set=data['texture_set'],
            behaviors=ReactiveActorBehaviors.from_json(data['behaviors']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'detection_box': self.detection_box.to_json(),
            'detection_offset': self.detection_offset.to_json(),
            'model': self.model,
            'character': self.character.to_json(),
            'actor_information': self.actor_information.to_json(),
            'start_enabled': self.start_enabled,
            'texture_set': self.texture_set,
            'behaviors': self.behaviors.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_detection_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_detection_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_start_enabled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_behaviors(data: typing.BinaryIO, property_size: int):
    return ReactiveActorBehaviors.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x6c447ff0: ('detection_box', _decode_detection_box),
    0x3daf5302: ('detection_offset', _decode_detection_offset),
    0xc27ffa8f: ('model', _decode_model),
    0x7bc2f6cf: ('character', _decode_character),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x2f7c59dc: ('start_enabled', _decode_start_enabled),
    0x6b40acef: ('texture_set', _decode_texture_set),
    0xc7bd1022: ('behaviors', _decode_behaviors),
}
