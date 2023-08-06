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
class Platform(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: Vector = dataclasses.field(default_factory=Vector)
    scan_offset: Vector = dataclasses.field(default_factory=Vector)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unnamed_0x00000008: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_2: float = dataclasses.field(default=0.0)
    active: bool = dataclasses.field(default=False)
    dcln: AssetId = dataclasses.field(metadata={'asset_types': ['DCLN']}, default=default_asset_id)
    unnamed_0x0000000c: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    unnamed_0x0000000d: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_3: bool = dataclasses.field(default=False)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: bool = dataclasses.field(default=False)
    unknown_6: int = dataclasses.field(default=0)
    unknown_7: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x8

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
        model = struct.unpack(">L", data.read(4))[0]
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        unnamed_0x00000008 = ActorParameters.from_stream(data, property_size)
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        active = struct.unpack('>?', data.read(1))[0]
        dcln = struct.unpack(">L", data.read(4))[0]
        unnamed_0x0000000c = HealthInfo.from_stream(data, property_size)
        unnamed_0x0000000d = DamageVulnerability.from_stream(data, property_size)
        unknown_3 = struct.unpack('>?', data.read(1))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>?', data.read(1))[0]
        unknown_6 = struct.unpack('>l', data.read(4))[0]
        unknown_7 = struct.unpack('>l', data.read(4))[0]
        return cls(name, position, rotation, scale, unknown_1, scan_offset, model, animation_parameters, unnamed_0x00000008, unknown_2, active, dcln, unnamed_0x0000000c, unnamed_0x0000000d, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x13')  # 19 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unknown_1.to_stream(data)
        self.scan_offset.to_stream(data)
        data.write(struct.pack(">L", self.model))
        self.animation_parameters.to_stream(data)
        self.unnamed_0x00000008.to_stream(data)
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack(">L", self.dcln))
        self.unnamed_0x0000000c.to_stream(data)
        self.unnamed_0x0000000d.to_stream(data)
        data.write(struct.pack('>?', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>?', self.unknown_5))
        data.write(struct.pack('>l', self.unknown_6))
        data.write(struct.pack('>l', self.unknown_7))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unknown_1=Vector.from_json(data['unknown_1']),
            scan_offset=Vector.from_json(data['scan_offset']),
            model=data['model'],
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            unnamed_0x00000008=ActorParameters.from_json(data['unnamed_0x00000008']),
            unknown_2=data['unknown_2'],
            active=data['active'],
            dcln=data['dcln'],
            unnamed_0x0000000c=HealthInfo.from_json(data['unnamed_0x0000000c']),
            unnamed_0x0000000d=DamageVulnerability.from_json(data['unnamed_0x0000000d']),
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unknown_1': self.unknown_1.to_json(),
            'scan_offset': self.scan_offset.to_json(),
            'model': self.model,
            'animation_parameters': self.animation_parameters.to_json(),
            'unnamed_0x00000008': self.unnamed_0x00000008.to_json(),
            'unknown_2': self.unknown_2,
            'active': self.active,
            'dcln': self.dcln,
            'unnamed_0x0000000c': self.unnamed_0x0000000c.to_json(),
            'unnamed_0x0000000d': self.unnamed_0x0000000d.to_json(),
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
        }

    def _dependencies_for_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000008(self, asset_manager):
        yield from self.unnamed_0x00000008.dependencies_for(asset_manager)

    def _dependencies_for_dcln(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dcln)

    def _dependencies_for_unnamed_0x0000000c(self, asset_manager):
        yield from self.unnamed_0x0000000c.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x0000000d(self, asset_manager):
        yield from self.unnamed_0x0000000d.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_model, "model", "AssetId"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_unnamed_0x00000008, "unnamed_0x00000008", "ActorParameters"),
            (self._dependencies_for_dcln, "dcln", "AssetId"),
            (self._dependencies_for_unnamed_0x0000000c, "unnamed_0x0000000c", "HealthInfo"),
            (self._dependencies_for_unnamed_0x0000000d, "unnamed_0x0000000d", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Platform.{field_name} ({field_type}): {e}"
                )
