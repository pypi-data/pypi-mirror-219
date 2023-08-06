# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Color import Color
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class DebrisExtended(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: Color = dataclasses.field(default_factory=Color)
    unknown_11: Color = dataclasses.field(default_factory=Color)
    unknown_12: float = dataclasses.field(default=0.0)
    unknown_13: Vector = dataclasses.field(default_factory=Vector)
    unknown_14: float = dataclasses.field(default=0.0)
    unknown_15: float = dataclasses.field(default=0.0)
    unknown_16: Vector = dataclasses.field(default_factory=Vector)
    model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unnamed: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_17: Vector = dataclasses.field(default_factory=Vector)
    unknown_18: bool = dataclasses.field(default=False)
    unknown_19: bool = dataclasses.field(default=False)
    unknown_20: int = dataclasses.field(default=0)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_21: Vector = dataclasses.field(default_factory=Vector)
    unknown_22: bool = dataclasses.field(default=False)
    unknown_23: bool = dataclasses.field(default=False)
    unknown_24: int = dataclasses.field(default=0)
    particle_3: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_25: Vector = dataclasses.field(default_factory=Vector)
    unknown_26: int = dataclasses.field(default=0)
    unknown_27: bool = dataclasses.field(default=False)
    unknown_28: bool = dataclasses.field(default=False)
    unknown_29: bool = dataclasses.field(default=False)
    unknown_30: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x45

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = Color.from_stream(data)
        unknown_11 = Color.from_stream(data)
        unknown_12 = struct.unpack('>f', data.read(4))[0]
        unknown_13 = Vector.from_stream(data)
        unknown_14 = struct.unpack('>f', data.read(4))[0]
        unknown_15 = struct.unpack('>f', data.read(4))[0]
        unknown_16 = Vector.from_stream(data)
        model = struct.unpack(">L", data.read(4))[0]
        unnamed = ActorParameters.from_stream(data, property_size)
        particle_1 = struct.unpack(">L", data.read(4))[0]
        unknown_17 = Vector.from_stream(data)
        unknown_18 = struct.unpack('>?', data.read(1))[0]
        unknown_19 = struct.unpack('>?', data.read(1))[0]
        unknown_20 = struct.unpack('>l', data.read(4))[0]
        particle_2 = struct.unpack(">L", data.read(4))[0]
        unknown_21 = Vector.from_stream(data)
        unknown_22 = struct.unpack('>?', data.read(1))[0]
        unknown_23 = struct.unpack('>?', data.read(1))[0]
        unknown_24 = struct.unpack('>l', data.read(4))[0]
        particle_3 = struct.unpack(">L", data.read(4))[0]
        unknown_25 = Vector.from_stream(data)
        unknown_26 = struct.unpack('>l', data.read(4))[0]
        unknown_27 = struct.unpack('>?', data.read(1))[0]
        unknown_28 = struct.unpack('>?', data.read(1))[0]
        unknown_29 = struct.unpack('>?', data.read(1))[0]
        unknown_30 = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, rotation, scale, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13, unknown_14, unknown_15, unknown_16, model, unnamed, particle_1, unknown_17, unknown_18, unknown_19, unknown_20, particle_2, unknown_21, unknown_22, unknown_23, unknown_24, particle_3, unknown_25, unknown_26, unknown_27, unknown_28, unknown_29, unknown_30)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b"\x00\x00\x00'")  # 39 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>f', self.unknown_9))
        self.unknown_10.to_stream(data)
        self.unknown_11.to_stream(data)
        data.write(struct.pack('>f', self.unknown_12))
        self.unknown_13.to_stream(data)
        data.write(struct.pack('>f', self.unknown_14))
        data.write(struct.pack('>f', self.unknown_15))
        self.unknown_16.to_stream(data)
        data.write(struct.pack(">L", self.model))
        self.unnamed.to_stream(data)
        data.write(struct.pack(">L", self.particle_1))
        self.unknown_17.to_stream(data)
        data.write(struct.pack('>?', self.unknown_18))
        data.write(struct.pack('>?', self.unknown_19))
        data.write(struct.pack('>l', self.unknown_20))
        data.write(struct.pack(">L", self.particle_2))
        self.unknown_21.to_stream(data)
        data.write(struct.pack('>?', self.unknown_22))
        data.write(struct.pack('>?', self.unknown_23))
        data.write(struct.pack('>l', self.unknown_24))
        data.write(struct.pack(">L", self.particle_3))
        self.unknown_25.to_stream(data)
        data.write(struct.pack('>l', self.unknown_26))
        data.write(struct.pack('>?', self.unknown_27))
        data.write(struct.pack('>?', self.unknown_28))
        data.write(struct.pack('>?', self.unknown_29))
        data.write(struct.pack('>?', self.unknown_30))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=Color.from_json(data['unknown_10']),
            unknown_11=Color.from_json(data['unknown_11']),
            unknown_12=data['unknown_12'],
            unknown_13=Vector.from_json(data['unknown_13']),
            unknown_14=data['unknown_14'],
            unknown_15=data['unknown_15'],
            unknown_16=Vector.from_json(data['unknown_16']),
            model=data['model'],
            unnamed=ActorParameters.from_json(data['unnamed']),
            particle_1=data['particle_1'],
            unknown_17=Vector.from_json(data['unknown_17']),
            unknown_18=data['unknown_18'],
            unknown_19=data['unknown_19'],
            unknown_20=data['unknown_20'],
            particle_2=data['particle_2'],
            unknown_21=Vector.from_json(data['unknown_21']),
            unknown_22=data['unknown_22'],
            unknown_23=data['unknown_23'],
            unknown_24=data['unknown_24'],
            particle_3=data['particle_3'],
            unknown_25=Vector.from_json(data['unknown_25']),
            unknown_26=data['unknown_26'],
            unknown_27=data['unknown_27'],
            unknown_28=data['unknown_28'],
            unknown_29=data['unknown_29'],
            unknown_30=data['unknown_30'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10.to_json(),
            'unknown_11': self.unknown_11.to_json(),
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13.to_json(),
            'unknown_14': self.unknown_14,
            'unknown_15': self.unknown_15,
            'unknown_16': self.unknown_16.to_json(),
            'model': self.model,
            'unnamed': self.unnamed.to_json(),
            'particle_1': self.particle_1,
            'unknown_17': self.unknown_17.to_json(),
            'unknown_18': self.unknown_18,
            'unknown_19': self.unknown_19,
            'unknown_20': self.unknown_20,
            'particle_2': self.particle_2,
            'unknown_21': self.unknown_21.to_json(),
            'unknown_22': self.unknown_22,
            'unknown_23': self.unknown_23,
            'unknown_24': self.unknown_24,
            'particle_3': self.particle_3,
            'unknown_25': self.unknown_25.to_json(),
            'unknown_26': self.unknown_26,
            'unknown_27': self.unknown_27,
            'unknown_28': self.unknown_28,
            'unknown_29': self.unknown_29,
            'unknown_30': self.unknown_30,
        }

    def _dependencies_for_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model)

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_particle_3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_3)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_model, "model", "AssetId"),
            (self._dependencies_for_unnamed, "unnamed", "ActorParameters"),
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_particle_3, "particle_3", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DebrisExtended.{field_name} ({field_type}): {e}"
                )
