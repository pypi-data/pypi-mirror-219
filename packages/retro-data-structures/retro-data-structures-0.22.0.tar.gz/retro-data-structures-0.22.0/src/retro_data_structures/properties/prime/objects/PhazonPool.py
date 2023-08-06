# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class PhazonPool(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: bool = dataclasses.field(default=False)
    model_1: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    model_2: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_2: int = dataclasses.field(default=0)
    unnamed: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    force: Vector = dataclasses.field(default_factory=Vector)
    trigger_flags: int = dataclasses.field(default=0)
    pool_starting_value: float = dataclasses.field(default=0.0)
    phazon_beam_drain_per_second: float = dataclasses.field(default=0.0)
    time_until_regeneration: float = dataclasses.field(default=0.0)
    automatic_drain_dont_regenerate: bool = dataclasses.field(default=False)
    time_until_automatic_drain: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x87

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        model_1 = struct.unpack(">L", data.read(4))[0]
        model_2 = struct.unpack(">L", data.read(4))[0]
        particle_1 = struct.unpack(">L", data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unnamed = DamageInfo.from_stream(data, property_size)
        force = Vector.from_stream(data)
        trigger_flags = struct.unpack('>l', data.read(4))[0]
        pool_starting_value = struct.unpack('>f', data.read(4))[0]
        phazon_beam_drain_per_second = struct.unpack('>f', data.read(4))[0]
        time_until_regeneration = struct.unpack('>f', data.read(4))[0]
        automatic_drain_dont_regenerate = struct.unpack('>?', data.read(1))[0]
        time_until_automatic_drain = struct.unpack('>f', data.read(4))[0]
        return cls(name, position, rotation, scale, unknown_1, model_1, model_2, particle_1, particle_2, unknown_2, unnamed, force, trigger_flags, pool_starting_value, phazon_beam_drain_per_second, time_until_regeneration, automatic_drain_dont_regenerate, time_until_automatic_drain)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x12')  # 18 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack(">L", self.model_1))
        data.write(struct.pack(">L", self.model_2))
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack('>l', self.unknown_2))
        self.unnamed.to_stream(data)
        self.force.to_stream(data)
        data.write(struct.pack('>l', self.trigger_flags))
        data.write(struct.pack('>f', self.pool_starting_value))
        data.write(struct.pack('>f', self.phazon_beam_drain_per_second))
        data.write(struct.pack('>f', self.time_until_regeneration))
        data.write(struct.pack('>?', self.automatic_drain_dont_regenerate))
        data.write(struct.pack('>f', self.time_until_automatic_drain))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unknown_1=data['unknown_1'],
            model_1=data['model_1'],
            model_2=data['model_2'],
            particle_1=data['particle_1'],
            particle_2=data['particle_2'],
            unknown_2=data['unknown_2'],
            unnamed=DamageInfo.from_json(data['unnamed']),
            force=Vector.from_json(data['force']),
            trigger_flags=data['trigger_flags'],
            pool_starting_value=data['pool_starting_value'],
            phazon_beam_drain_per_second=data['phazon_beam_drain_per_second'],
            time_until_regeneration=data['time_until_regeneration'],
            automatic_drain_dont_regenerate=data['automatic_drain_dont_regenerate'],
            time_until_automatic_drain=data['time_until_automatic_drain'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unknown_1': self.unknown_1,
            'model_1': self.model_1,
            'model_2': self.model_2,
            'particle_1': self.particle_1,
            'particle_2': self.particle_2,
            'unknown_2': self.unknown_2,
            'unnamed': self.unnamed.to_json(),
            'force': self.force.to_json(),
            'trigger_flags': self.trigger_flags,
            'pool_starting_value': self.pool_starting_value,
            'phazon_beam_drain_per_second': self.phazon_beam_drain_per_second,
            'time_until_regeneration': self.time_until_regeneration,
            'automatic_drain_dont_regenerate': self.automatic_drain_dont_regenerate,
            'time_until_automatic_drain': self.time_until_automatic_drain,
        }

    def _dependencies_for_model_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_1)

    def _dependencies_for_model_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_2)

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_model_1, "model_1", "AssetId"),
            (self._dependencies_for_model_2, "model_2", "AssetId"),
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_unnamed, "unnamed", "DamageInfo"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PhazonPool.{field_name} ({field_type}): {e}"
                )
