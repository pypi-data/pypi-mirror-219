# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.prime as enums
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Pickup(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    collision_scale: Vector = dataclasses.field(default_factory=Vector)
    scan_collision_offset: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000006: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.PowerBeam)
    capacity: int = dataclasses.field(default=0)
    amount: int = dataclasses.field(default=0)
    drop_rate: float = dataclasses.field(default=0.0)
    life_time: float = dataclasses.field(default=0.0)
    fade_length: float = dataclasses.field(default=0.0)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unnamed_0x0000000e: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    active: bool = dataclasses.field(default=False)
    spawn_delay: float = dataclasses.field(default=0.0)
    particle: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x11

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        collision_scale = Vector.from_stream(data)
        scan_collision_offset = Vector.from_stream(data)
        unnamed_0x00000006 = enums.PlayerItem.from_stream(data)
        capacity = struct.unpack('>l', data.read(4))[0]
        amount = struct.unpack('>l', data.read(4))[0]
        drop_rate = struct.unpack('>f', data.read(4))[0]
        life_time = struct.unpack('>f', data.read(4))[0]
        fade_length = struct.unpack('>f', data.read(4))[0]
        model = struct.unpack(">L", data.read(4))[0]
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        unnamed_0x0000000e = ActorParameters.from_stream(data, property_size)
        active = struct.unpack('>?', data.read(1))[0]
        spawn_delay = struct.unpack('>f', data.read(4))[0]
        particle = struct.unpack(">L", data.read(4))[0]
        return cls(name, position, rotation, scale, collision_scale, scan_collision_offset, unnamed_0x00000006, capacity, amount, drop_rate, life_time, fade_length, model, animation_parameters, unnamed_0x0000000e, active, spawn_delay, particle)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x12')  # 18 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.collision_scale.to_stream(data)
        self.scan_collision_offset.to_stream(data)
        self.unnamed_0x00000006.to_stream(data)
        data.write(struct.pack('>l', self.capacity))
        data.write(struct.pack('>l', self.amount))
        data.write(struct.pack('>f', self.drop_rate))
        data.write(struct.pack('>f', self.life_time))
        data.write(struct.pack('>f', self.fade_length))
        data.write(struct.pack(">L", self.model))
        self.animation_parameters.to_stream(data)
        self.unnamed_0x0000000e.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>f', self.spawn_delay))
        data.write(struct.pack(">L", self.particle))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            collision_scale=Vector.from_json(data['collision_scale']),
            scan_collision_offset=Vector.from_json(data['scan_collision_offset']),
            unnamed_0x00000006=enums.PlayerItem.from_json(data['unnamed_0x00000006']),
            capacity=data['capacity'],
            amount=data['amount'],
            drop_rate=data['drop_rate'],
            life_time=data['life_time'],
            fade_length=data['fade_length'],
            model=data['model'],
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            unnamed_0x0000000e=ActorParameters.from_json(data['unnamed_0x0000000e']),
            active=data['active'],
            spawn_delay=data['spawn_delay'],
            particle=data['particle'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'collision_scale': self.collision_scale.to_json(),
            'scan_collision_offset': self.scan_collision_offset.to_json(),
            'unnamed_0x00000006': self.unnamed_0x00000006.to_json(),
            'capacity': self.capacity,
            'amount': self.amount,
            'drop_rate': self.drop_rate,
            'life_time': self.life_time,
            'fade_length': self.fade_length,
            'model': self.model,
            'animation_parameters': self.animation_parameters.to_json(),
            'unnamed_0x0000000e': self.unnamed_0x0000000e.to_json(),
            'active': self.active,
            'spawn_delay': self.spawn_delay,
            'particle': self.particle,
        }

    def _dependencies_for_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000e(self, asset_manager):
        yield from self.unnamed_0x0000000e.dependencies_for(asset_manager)

    def _dependencies_for_particle(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_model, "model", "AssetId"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_unnamed_0x0000000e, "unnamed_0x0000000e", "ActorParameters"),
            (self._dependencies_for_particle, "particle", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Pickup.{field_name} ({field_type}): {e}"
                )
