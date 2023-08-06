# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.GuessStruct import GuessStruct
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class Steam(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_1: Vector = dataclasses.field(default_factory=Vector)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: bool = dataclasses.field(default=False)
    texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    guess_struct_1: GuessStruct = dataclasses.field(default_factory=GuessStruct)
    guess_struct_2: GuessStruct = dataclasses.field(default_factory=GuessStruct)
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
        return 0x46

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed = DamageInfo.from_stream(data, property_size)
        unknown_1 = Vector.from_stream(data)
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>?', data.read(1))[0]
        texture = struct.unpack(">L", data.read(4))[0]
        guess_struct_1 = GuessStruct.from_stream(data, property_size)
        guess_struct_2 = GuessStruct.from_stream(data, property_size)
        unknown_8 = struct.unpack('>?', data.read(1))[0]
        return cls(name, position, scale, unnamed, unknown_1, unknown_2, unknown_3, texture, guess_struct_1, guess_struct_2, unknown_8)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x0b')  # 11 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed.to_stream(data)
        self.unknown_1.to_stream(data)
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>?', self.unknown_3))
        data.write(struct.pack(">L", self.texture))
        self.guess_struct_1.to_stream(data)
        self.guess_struct_2.to_stream(data)
        data.write(struct.pack('>?', self.unknown_8))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            scale=Vector.from_json(data['scale']),
            unnamed=DamageInfo.from_json(data['unnamed']),
            unknown_1=Vector.from_json(data['unknown_1']),
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            texture=data['texture'],
            guess_struct_1=GuessStruct.from_json(data['guess_struct_1']),
            guess_struct_2=GuessStruct.from_json(data['guess_struct_2']),
            unknown_8=data['unknown_8'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'scale': self.scale.to_json(),
            'unnamed': self.unnamed.to_json(),
            'unknown_1': self.unknown_1.to_json(),
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'texture': self.texture,
            'guess_struct_1': self.guess_struct_1.to_json(),
            'guess_struct_2': self.guess_struct_2.to_json(),
            'unknown_8': self.unknown_8,
        }

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def _dependencies_for_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.texture)

    def _dependencies_for_guess_struct_1(self, asset_manager):
        yield from self.guess_struct_1.dependencies_for(asset_manager)

    def _dependencies_for_guess_struct_2(self, asset_manager):
        yield from self.guess_struct_2.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed, "unnamed", "DamageInfo"),
            (self._dependencies_for_texture, "texture", "AssetId"),
            (self._dependencies_for_guess_struct_1, "guess_struct_1", "GuessStruct"),
            (self._dependencies_for_guess_struct_2, "guess_struct_2", "GuessStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Steam.{field_name} ({field_type}): {e}"
                )
