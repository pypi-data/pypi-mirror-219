# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.dkc_returns.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileBounceData import ProjectileBounceData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileCollisionData import ProjectileCollisionData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileData import ProjectileData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileMotionData import ProjectileMotionData
from retro_data_structures.properties.dkc_returns.archetypes.ProjectileRenderData import ProjectileRenderData


@dataclasses.dataclass()
class Projectile(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    projectile_data: ProjectileData = dataclasses.field(default_factory=ProjectileData)
    projectile_render_data: ProjectileRenderData = dataclasses.field(default_factory=ProjectileRenderData)
    projectile_collision_data: ProjectileCollisionData = dataclasses.field(default_factory=ProjectileCollisionData)
    projectile_motion_data: ProjectileMotionData = dataclasses.field(default_factory=ProjectileMotionData)
    can_bounce: bool = dataclasses.field(default=False)
    projectile_bounce_data: ProjectileBounceData = dataclasses.field(default_factory=ProjectileBounceData)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PROJ'

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

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa5\xcc)\x82')  # 0xa5cc2982
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd9\r\xab\t')  # 0xd90dab09
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_render_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\xd9x_')  # 0x58d9785f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_collision_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x90\xdc\xef\x98')  # 0x90dcef98
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_motion_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xccB\x84\xa2')  # 0xcc4284a2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_bounce))

        data.write(b'P\xa7\xe9K')  # 0x50a7e94b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_bounce_data.to_stream(data)
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
            projectile_data=ProjectileData.from_json(data['projectile_data']),
            projectile_render_data=ProjectileRenderData.from_json(data['projectile_render_data']),
            projectile_collision_data=ProjectileCollisionData.from_json(data['projectile_collision_data']),
            projectile_motion_data=ProjectileMotionData.from_json(data['projectile_motion_data']),
            can_bounce=data['can_bounce'],
            projectile_bounce_data=ProjectileBounceData.from_json(data['projectile_bounce_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_information': self.actor_information.to_json(),
            'projectile_data': self.projectile_data.to_json(),
            'projectile_render_data': self.projectile_render_data.to_json(),
            'projectile_collision_data': self.projectile_collision_data.to_json(),
            'projectile_motion_data': self.projectile_motion_data.to_json(),
            'can_bounce': self.can_bounce,
            'projectile_bounce_data': self.projectile_bounce_data.to_json(),
        }


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_projectile_data(data: typing.BinaryIO, property_size: int):
    return ProjectileData.from_stream(data, property_size)


def _decode_projectile_render_data(data: typing.BinaryIO, property_size: int):
    return ProjectileRenderData.from_stream(data, property_size)


def _decode_projectile_collision_data(data: typing.BinaryIO, property_size: int):
    return ProjectileCollisionData.from_stream(data, property_size)


def _decode_projectile_motion_data(data: typing.BinaryIO, property_size: int):
    return ProjectileMotionData.from_stream(data, property_size)


def _decode_can_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_projectile_bounce_data(data: typing.BinaryIO, property_size: int):
    return ProjectileBounceData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xa5cc2982: ('projectile_data', _decode_projectile_data),
    0xd90dab09: ('projectile_render_data', _decode_projectile_render_data),
    0x58d9785f: ('projectile_collision_data', _decode_projectile_collision_data),
    0x90dcef98: ('projectile_motion_data', _decode_projectile_motion_data),
    0xcc4284a2: ('can_bounce', _decode_can_bounce),
    0x50a7e94b: ('projectile_bounce_data', _decode_projectile_bounce_data),
}
