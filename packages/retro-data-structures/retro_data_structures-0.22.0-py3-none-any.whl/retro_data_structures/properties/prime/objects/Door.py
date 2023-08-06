# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Door(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unnamed: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    scan_offset: Vector = dataclasses.field(default_factory=Vector)
    collision_size: Vector = dataclasses.field(default_factory=Vector)
    collision_offset: Vector = dataclasses.field(default_factory=Vector)
    active: bool = dataclasses.field(default=False)
    open: bool = dataclasses.field(default=False)
    unknown_6: bool = dataclasses.field(default=False)
    open_close_animation_length: float = dataclasses.field(default=0.0)
    unknown_8: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x3

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        unnamed = ActorParameters.from_stream(data, property_size)
        scan_offset = Vector.from_stream(data)
        collision_size = Vector.from_stream(data)
        collision_offset = Vector.from_stream(data)
        active = struct.unpack('>?', data.read(1))[0]
        open = struct.unpack('>?', data.read(1))[0]
        unknown_6 = struct.unpack('>?', data.read(1))[0]
        open_close_animation_length = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, scale, animation_parameters, unnamed, scan_offset, collision_size, collision_offset, active, open, unknown_6, open_close_animation_length, unknown_8)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0e')  # 14 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.animation_parameters.to_stream(data)
        self.unnamed.to_stream(data)
        self.scan_offset.to_stream(data)
        self.collision_size.to_stream(data)
        self.collision_offset.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>?', self.open))
        data.write(struct.pack('>?', self.unknown_6))
        data.write(struct.pack('>f', self.open_close_animation_length))
        data.write(struct.pack('>?', self.unknown_8))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            unnamed=ActorParameters.from_json(data['unnamed']),
            scan_offset=Vector.from_json(data['scan_offset']),
            collision_size=Vector.from_json(data['collision_size']),
            collision_offset=Vector.from_json(data['collision_offset']),
            active=data['active'],
            open=data['open'],
            unknown_6=data['unknown_6'],
            open_close_animation_length=data['open_close_animation_length'],
            unknown_8=data['unknown_8'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'animation_parameters': self.animation_parameters.to_json(),
            'unnamed': self.unnamed.to_json(),
            'scan_offset': self.scan_offset.to_json(),
            'collision_size': self.collision_size.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'active': self.active,
            'open': self.open,
            'unknown_6': self.unknown_6,
            'open_close_animation_length': self.open_close_animation_length,
            'unknown_8': self.unknown_8,
        }

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_unnamed, "unnamed", "ActorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Door.{field_name} ({field_type}): {e}"
                )
