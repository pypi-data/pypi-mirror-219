# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.echoes.archetypes.PlatformMotionProperties import PlatformMotionProperties
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class Platform(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    collision_box: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animation_information: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    collision_model: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    x_ray_transparency: float = dataclasses.field(default=1.0)
    maximum_splashes: int = dataclasses.field(default=200)
    splash_generation_rate: int = dataclasses.field(default=20)
    render_rain_splashes: bool = dataclasses.field(default=False)
    unknown_0xf203bc81: bool = dataclasses.field(default=False)
    motion_properties: PlatformMotionProperties = dataclasses.field(default_factory=PlatformMotionProperties)
    unknown_0x24fdeea1: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.15000000596046448, z=0.0))
    random_animation_offset: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PLAT'

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
        data.write(b'\x00\x11')  # 17 properties

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
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.model))

        data.write(b'\xe2_\xb0\x8c')  # 0xe25fb08c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.animation_information.to_stream(data)
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

        data.write(b'\x0f\xc9f\xdc')  # 0xfc966dc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.collision_model))

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'aP\xd6\x87')  # 0x6150d687
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.x_ray_transparency))

        data.write(b'\xdc\xd5o\xe8')  # 0xdcd56fe8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.maximum_splashes))

        data.write(b'h-\xe1\\')  # 0x682de15c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.splash_generation_rate))

        data.write(b'\xac:\xdd\xa6')  # 0xac3adda6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.render_rain_splashes))

        data.write(b'\xf2\x03\xbc\x81')  # 0xf203bc81
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xf203bc81))

        data.write(b'\n\x9d\xbf\x91')  # 0xa9dbf91
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xfd\xee\xa1')  # 0x24fdeea1
        data.write(b'\x00\x0c')  # size
        self.unknown_0x24fdeea1.to_stream(data)

        data.write(b'\xbfi\xc0>')  # 0xbf69c03e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.random_animation_offset))

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
            animation_information=AnimationParameters.from_json(data['animation_information']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            collision_model=data['collision_model'],
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            x_ray_transparency=data['x_ray_transparency'],
            maximum_splashes=data['maximum_splashes'],
            splash_generation_rate=data['splash_generation_rate'],
            render_rain_splashes=data['render_rain_splashes'],
            unknown_0xf203bc81=data['unknown_0xf203bc81'],
            motion_properties=PlatformMotionProperties.from_json(data['motion_properties']),
            unknown_0x24fdeea1=Vector.from_json(data['unknown_0x24fdeea1']),
            random_animation_offset=data['random_animation_offset'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'collision_box': self.collision_box.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'model': self.model,
            'animation_information': self.animation_information.to_json(),
            'actor_information': self.actor_information.to_json(),
            'collision_model': self.collision_model,
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'x_ray_transparency': self.x_ray_transparency,
            'maximum_splashes': self.maximum_splashes,
            'splash_generation_rate': self.splash_generation_rate,
            'render_rain_splashes': self.render_rain_splashes,
            'unknown_0xf203bc81': self.unknown_0xf203bc81,
            'motion_properties': self.motion_properties.to_json(),
            'unknown_0x24fdeea1': self.unknown_0x24fdeea1.to_json(),
            'random_animation_offset': self.random_animation_offset,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model)

    def _dependencies_for_animation_information(self, asset_manager):
        yield from self.animation_information.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_collision_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.collision_model)

    def _dependencies_for_health(self, asset_manager):
        yield from self.health.dependencies_for(asset_manager)

    def _dependencies_for_vulnerability(self, asset_manager):
        yield from self.vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_motion_properties(self, asset_manager):
        yield from self.motion_properties.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_model, "model", "AssetId"),
            (self._dependencies_for_animation_information, "animation_information", "AnimationParameters"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_collision_model, "collision_model", "AssetId"),
            (self._dependencies_for_health, "health", "HealthInfo"),
            (self._dependencies_for_vulnerability, "vulnerability", "DamageVulnerability"),
            (self._dependencies_for_motion_properties, "motion_properties", "PlatformMotionProperties"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Platform.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_collision_box(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_animation_information(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_collision_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_x_ray_transparency(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_splashes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_splash_generation_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_render_rain_splashes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xf203bc81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_motion_properties(data: typing.BinaryIO, property_size: int):
    return PlatformMotionProperties.from_stream(data, property_size)


def _decode_unknown_0x24fdeea1(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_random_animation_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xf344c0b0: ('collision_box', _decode_collision_box),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xc27ffa8f: ('model', _decode_model),
    0xe25fb08c: ('animation_information', _decode_animation_information),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xfc966dc: ('collision_model', _decode_collision_model),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0x6150d687: ('x_ray_transparency', _decode_x_ray_transparency),
    0xdcd56fe8: ('maximum_splashes', _decode_maximum_splashes),
    0x682de15c: ('splash_generation_rate', _decode_splash_generation_rate),
    0xac3adda6: ('render_rain_splashes', _decode_render_rain_splashes),
    0xf203bc81: ('unknown_0xf203bc81', _decode_unknown_0xf203bc81),
    0xa9dbf91: ('motion_properties', _decode_motion_properties),
    0x24fdeea1: ('unknown_0x24fdeea1', _decode_unknown_0x24fdeea1),
    0xbf69c03e: ('random_animation_offset', _decode_random_animation_offset),
}
