# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct184 import UnknownStruct184
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct185 import UnknownStruct185
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class IslandArea(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    collision_model: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    character_animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    area_name: AssetId = dataclasses.field(metadata={'asset_types': ['STRG']}, default=default_asset_id)
    name: str = dataclasses.field(default='')
    area_type: enums.AreaType = dataclasses.field(default=enums.AreaType.Unknown1)
    unknown_struct184: UnknownStruct184 = dataclasses.field(default_factory=UnknownStruct184)
    unknown_struct185: UnknownStruct185 = dataclasses.field(default_factory=UnknownStruct185)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'ISAR'

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

        data.write(b'\xf3D\xc0\xb0')  # 0xf344c0b0
        data.write(b'\x00\x0c')  # size
        self.collision_box.to_stream(data)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.collision_model))

        data.write(b'\xa2D\xc9\xd8')  # 0xa244c9d8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.character_animation_information.to_stream(data)
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

        data.write(b';\x83\xdd1')  # 0x3b83dd31
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.area_name))

        data.write(b'j\x02\xf0_')  # 0x6a02f05f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\xe2\x9f\x9b')  # 0x28e29f9b
        data.write(b'\x00\x04')  # size
        self.area_type.to_stream(data)

        data.write(b'\xdfi)g')  # 0xdf692967
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct184.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0fr#W')  # 0xf722357
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct185.to_stream(data)
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
            collision_box=Vector.from_json(data['collision_box']),
            collision_offset=Vector.from_json(data['collision_offset']),
            model=data['model'],
            collision_model=data['collision_model'],
            character_animation_information=AnimationParameters.from_json(data['character_animation_information']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            area_name=data['area_name'],
            name=data['name'],
            area_type=enums.AreaType.from_json(data['area_type']),
            unknown_struct184=UnknownStruct184.from_json(data['unknown_struct184']),
            unknown_struct185=UnknownStruct185.from_json(data['unknown_struct185']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'model': self.model,
            'collision_model': self.collision_model,
            'character_animation_information': self.character_animation_information.to_json(),
            'actor_information': self.actor_information.to_json(),
            'area_name': self.area_name,
            'name': self.name,
            'area_type': self.area_type.to_json(),
            'unknown_struct184': self.unknown_struct184.to_json(),
            'unknown_struct185': self.unknown_struct185.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_character_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_area_name(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_area_type(data: typing.BinaryIO, property_size: int):
    return enums.AreaType.from_stream(data)


def _decode_unknown_struct184(data: typing.BinaryIO, property_size: int):
    return UnknownStruct184.from_stream(data, property_size)


def _decode_unknown_struct185(data: typing.BinaryIO, property_size: int):
    return UnknownStruct185.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xc27ffa8f: ('model', _decode_model),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xa244c9d8: ('character_animation_information', _decode_character_animation_information),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x3b83dd31: ('area_name', _decode_area_name),
    0x6a02f05f: ('name', _decode_name),
    0x28e29f9b: ('area_type', _decode_area_type),
    0xdf692967: ('unknown_struct184', _decode_unknown_struct184),
    0xf722357: ('unknown_struct185', _decode_unknown_struct185),
}
