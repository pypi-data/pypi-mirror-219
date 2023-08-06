# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct19 import UnknownStruct19
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct20 import UnknownStruct20
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class AreaNode(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    start_hidden: bool = dataclasses.field(default=False)
    play_cinematic: bool = dataclasses.field(default=False)
    unknown_0xa6f8611c: bool = dataclasses.field(default=False)
    node_type: enums.NodeType = dataclasses.field(default=enums.NodeType.Stage)
    name: str = dataclasses.field(default='')
    world_name: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    area_name: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    sort_order: int = dataclasses.field(default=0)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_model: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    unknown_0x33cf5665: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0xb7cd213c: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x9f93bc3f: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    world_level: AssetId = dataclasses.field(metadata={'asset_types': ['MLVL']}, default=default_asset_id)
    unknown_struct19: UnknownStruct19 = dataclasses.field(default_factory=UnknownStruct19)
    unknown_struct20: UnknownStruct20 = dataclasses.field(default_factory=UnknownStruct20)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ARNO'

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
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'M\xef{\x9b')  # 0x4def7b9b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.start_hidden))

        data.write(b'\xf1\xae/\x13')  # 0xf1ae2f13
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.play_cinematic))

        data.write(b'\xa6\xf8a\x1c')  # 0xa6f8611c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xa6f8611c))

        data.write(b'\x8d:\xb3\x14')  # 0x8d3ab314
        data.write(b'\x00\x04')  # size
        self.node_type.to_stream(data)

        data.write(b'j\x02\xf0_')  # 0x6a02f05f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'sv1\xad')  # 0x737631ad
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.world_name))

        data.write(b';\x83\xdd1')  # 0x3b83dd31
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.area_name))

        data.write(b'0\xcb\xdbh')  # 0x30cbdb68
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sort_order))

        data.write(b'\xf3D\xc0\xb0')  # 0xf344c0b0
        data.write(b'\x00\x0c')  # size
        self.collision_box.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collision_model))

        data.write(b'3\xcfVe')  # 0x33cf5665
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x33cf5665))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb7\xcd!<')  # 0xb7cd213c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xb7cd213c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9f\x93\xbc?')  # 0x9f93bc3f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x9f93bc3f.to_stream(data)
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

        data.write(b'jx\x9b\xe3')  # 0x6a789be3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.world_level))

        data.write(b'\xa9\xd2\x9e2')  # 0xa9d29e32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct19.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86\x96>\x8a')  # 0x86963e8a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct20.to_stream(data)
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
            start_hidden=data['start_hidden'],
            play_cinematic=data['play_cinematic'],
            unknown_0xa6f8611c=data['unknown_0xa6f8611c'],
            node_type=enums.NodeType.from_json(data['node_type']),
            name=data['name'],
            world_name=data['world_name'],
            area_name=data['area_name'],
            sort_order=data['sort_order'],
            collision_box=Vector.from_json(data['collision_box']),
            collision_offset=Vector.from_json(data['collision_offset']),
            collision_model=data['collision_model'],
            unknown_0x33cf5665=data['unknown_0x33cf5665'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            unknown_0xb7cd213c=AnimationParameters.from_json(data['unknown_0xb7cd213c']),
            unknown_0x9f93bc3f=AnimationParameters.from_json(data['unknown_0x9f93bc3f']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            world_level=data['world_level'],
            unknown_struct19=UnknownStruct19.from_json(data['unknown_struct19']),
            unknown_struct20=UnknownStruct20.from_json(data['unknown_struct20']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'start_hidden': self.start_hidden,
            'play_cinematic': self.play_cinematic,
            'unknown_0xa6f8611c': self.unknown_0xa6f8611c,
            'node_type': self.node_type.to_json(),
            'name': self.name,
            'world_name': self.world_name,
            'area_name': self.area_name,
            'sort_order': self.sort_order,
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'collision_model': self.collision_model,
            'unknown_0x33cf5665': self.unknown_0x33cf5665,
            'character_animation_information': self.character_animation_information.to_json(),
            'unknown_0xb7cd213c': self.unknown_0xb7cd213c.to_json(),
            'unknown_0x9f93bc3f': self.unknown_0x9f93bc3f.to_json(),
            'actor_information': self.actor_information.to_json(),
            'world_level': self.world_level,
            'unknown_struct19': self.unknown_struct19.to_json(),
            'unknown_struct20': self.unknown_struct20.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_start_hidden(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_play_cinematic(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xa6f8611c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_node_type(data: typing.BinaryIO, property_size: int):
    return enums.NodeType.from_stream(data)


def _decode_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_world_name(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_area_name(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_sort_order(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x33cf5665(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0xb7cd213c(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x9f93bc3f(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_world_level(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_struct19(data: typing.BinaryIO, property_size: int):
    return UnknownStruct19.from_stream(data, property_size)


def _decode_unknown_struct20(data: typing.BinaryIO, property_size: int):
    return UnknownStruct20.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x4def7b9b: ('start_hidden', _decode_start_hidden),
    0xf1ae2f13: ('play_cinematic', _decode_play_cinematic),
    0xa6f8611c: ('unknown_0xa6f8611c', _decode_unknown_0xa6f8611c),
    0x8d3ab314: ('node_type', _decode_node_type),
    0x6a02f05f: ('name', _decode_name),
    0x737631ad: ('world_name', _decode_world_name),
    0x3b83dd31: ('area_name', _decode_area_name),
    0x30cbdb68: ('sort_order', _decode_sort_order),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0x33cf5665: ('unknown_0x33cf5665', _decode_unknown_0x33cf5665),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0xb7cd213c: ('unknown_0xb7cd213c', _decode_unknown_0xb7cd213c),
    0x9f93bc3f: ('unknown_0x9f93bc3f', _decode_unknown_0x9f93bc3f),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x6a789be3: ('world_level', _decode_world_level),
    0xa9d29e32: ('unknown_struct19', _decode_unknown_struct19),
    0x86963e8a: ('unknown_struct20', _decode_unknown_struct20),
}
