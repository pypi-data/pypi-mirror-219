# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.prime.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Actor(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: Vector = dataclasses.field(default_factory=Vector)
    scan_offset: Vector = dataclasses.field(default_factory=Vector)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unnamed_0x00000008: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    unnamed_0x00000009: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unnamed_0x0000000c: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    auto_play_animation: bool = dataclasses.field(default=False)
    unknown_5: bool = dataclasses.field(default=False)
    bounding_box_collision: bool = dataclasses.field(default=False)
    unknown_7: bool = dataclasses.field(default=False)
    active: bool = dataclasses.field(default=False)
    unknown_9: int = dataclasses.field(default=0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: bool = dataclasses.field(default=False)
    unknown_12: bool = dataclasses.field(default=False)
    unknown_13: bool = dataclasses.field(default=False)
    unknown_14: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x0

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unknown_1 = Vector.from_stream(data)
        scan_offset = Vector.from_stream(data)
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unnamed_0x00000008 = HealthInfo.from_stream(data, property_size)
        unnamed_0x00000009 = DamageVulnerability.from_stream(data, property_size)
        model = struct.unpack(">L", data.read(4))[0]
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        unnamed_0x0000000c = ActorParameters.from_stream(data, property_size)
        auto_play_animation = struct.unpack('>?', data.read(1))[0]
        unknown_5 = struct.unpack('>?', data.read(1))[0]
        bounding_box_collision = struct.unpack('>?', data.read(1))[0]
        unknown_7 = struct.unpack('>?', data.read(1))[0]
        active = struct.unpack('>?', data.read(1))[0]
        unknown_9 = struct.unpack('>l', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>?', data.read(1))[0]
        unknown_12 = struct.unpack('>?', data.read(1))[0]
        unknown_13 = struct.unpack('>?', data.read(1))[0]
        unknown_14 = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, scale, unknown_1, scan_offset, unknown_2, unknown_3, unnamed_0x00000008, unnamed_0x00000009, model, animation_parameters, unnamed_0x0000000c, auto_play_animation, unknown_5, bounding_box_collision, unknown_7, active, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13, unknown_14)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x18')  # 24 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unknown_1.to_stream(data)
        self.scan_offset.to_stream(data)
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        self.unnamed_0x00000008.to_stream(data)
        self.unnamed_0x00000009.to_stream(data)
        data.write(struct.pack(">L", self.model))
        self.animation_parameters.to_stream(data)
        self.unnamed_0x0000000c.to_stream(data)
        data.write(struct.pack('>?', self.auto_play_animation))
        data.write(struct.pack('>?', self.unknown_5))
        data.write(struct.pack('>?', self.bounding_box_collision))
        data.write(struct.pack('>?', self.unknown_7))
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack('>l', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>?', self.unknown_11))
        data.write(struct.pack('>?', self.unknown_12))
        data.write(struct.pack('>?', self.unknown_13))
        data.write(struct.pack('>?', self.unknown_14))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unknown_1=Vector.from_json(data['unknown_1']),
            scan_offset=Vector.from_json(data['scan_offset']),
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unnamed_0x00000008=HealthInfo.from_json(data['unnamed_0x00000008']),
            unnamed_0x00000009=DamageVulnerability.from_json(data['unnamed_0x00000009']),
            model=data['model'],
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            unnamed_0x0000000c=ActorParameters.from_json(data['unnamed_0x0000000c']),
            auto_play_animation=data['auto_play_animation'],
            unknown_5=data['unknown_5'],
            bounding_box_collision=data['bounding_box_collision'],
            unknown_7=data['unknown_7'],
            active=data['active'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=data['unknown_12'],
            unknown_13=data['unknown_13'],
            unknown_14=data['unknown_14'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unknown_1': self.unknown_1.to_json(),
            'scan_offset': self.scan_offset.to_json(),
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unnamed_0x00000008': self.unnamed_0x00000008.to_json(),
            'unnamed_0x00000009': self.unnamed_0x00000009.to_json(),
            'model': self.model,
            'animation_parameters': self.animation_parameters.to_json(),
            'unnamed_0x0000000c': self.unnamed_0x0000000c.to_json(),
            'auto_play_animation': self.auto_play_animation,
            'unknown_5': self.unknown_5,
            'bounding_box_collision': self.bounding_box_collision,
            'unknown_7': self.unknown_7,
            'active': self.active,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
            'unknown_14': self.unknown_14,
        }

    def _dependencies_for_unnamed_0x00000008(self, asset_manager):
        yield from self.unnamed_0x00000008.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000009(self, asset_manager):
        yield from self.unnamed_0x00000009.dependencies_for(asset_manager)

    def _dependencies_for_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000c(self, asset_manager):
        yield from self.unnamed_0x0000000c.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000008, "unnamed_0x00000008", "HealthInfo"),
            (self._dependencies_for_unnamed_0x00000009, "unnamed_0x00000009", "DamageVulnerability"),
            (self._dependencies_for_model, "model", "AssetId"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_unnamed_0x0000000c, "unnamed_0x0000000c", "ActorParameters"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Actor.{field_name} ({field_type}): {e}"
                )
