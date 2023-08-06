# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.GuessStruct import GuessStruct
from retro_data_structures.properties.prime.archetypes.IntBool import IntBool
from retro_data_structures.properties.prime.archetypes.NewCameraShakerStruct import NewCameraShakerStruct
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class NewCameraShaker(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: bool = dataclasses.field(default=False)
    unnamed_0x00000003: IntBool = dataclasses.field(default_factory=IntBool)
    unnamed_0x00000004: GuessStruct = dataclasses.field(default_factory=GuessStruct)
    new_camera_shaker_struct_1: NewCameraShakerStruct = dataclasses.field(default_factory=NewCameraShakerStruct)
    new_camera_shaker_struct_2: NewCameraShakerStruct = dataclasses.field(default_factory=NewCameraShakerStruct)
    new_camera_shaker_struct_3: NewCameraShakerStruct = dataclasses.field(default_factory=NewCameraShakerStruct)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x89

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unnamed_0x00000003 = IntBool.from_stream(data, property_size)
        unnamed_0x00000004 = GuessStruct.from_stream(data, property_size)
        new_camera_shaker_struct_1 = NewCameraShakerStruct.from_stream(data, property_size)
        new_camera_shaker_struct_2 = NewCameraShakerStruct.from_stream(data, property_size)
        new_camera_shaker_struct_3 = NewCameraShakerStruct.from_stream(data, property_size)
        return cls(name, position, unknown_1, unnamed_0x00000003, unnamed_0x00000004, new_camera_shaker_struct_1, new_camera_shaker_struct_2, new_camera_shaker_struct_3)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x08')  # 8 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        self.unnamed_0x00000003.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.new_camera_shaker_struct_1.to_stream(data)
        self.new_camera_shaker_struct_2.to_stream(data)
        self.new_camera_shaker_struct_3.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            unknown_1=data['unknown_1'],
            unnamed_0x00000003=IntBool.from_json(data['unnamed_0x00000003']),
            unnamed_0x00000004=GuessStruct.from_json(data['unnamed_0x00000004']),
            new_camera_shaker_struct_1=NewCameraShakerStruct.from_json(data['new_camera_shaker_struct_1']),
            new_camera_shaker_struct_2=NewCameraShakerStruct.from_json(data['new_camera_shaker_struct_2']),
            new_camera_shaker_struct_3=NewCameraShakerStruct.from_json(data['new_camera_shaker_struct_3']),
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'unknown_1': self.unknown_1,
            'unnamed_0x00000003': self.unnamed_0x00000003.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'new_camera_shaker_struct_1': self.new_camera_shaker_struct_1.to_json(),
            'new_camera_shaker_struct_2': self.new_camera_shaker_struct_2.to_json(),
            'new_camera_shaker_struct_3': self.new_camera_shaker_struct_3.to_json(),
        }

    def _dependencies_for_unnamed_0x00000003(self, asset_manager):
        yield from self.unnamed_0x00000003.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_new_camera_shaker_struct_1(self, asset_manager):
        yield from self.new_camera_shaker_struct_1.dependencies_for(asset_manager)

    def _dependencies_for_new_camera_shaker_struct_2(self, asset_manager):
        yield from self.new_camera_shaker_struct_2.dependencies_for(asset_manager)

    def _dependencies_for_new_camera_shaker_struct_3(self, asset_manager):
        yield from self.new_camera_shaker_struct_3.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000003, "unnamed_0x00000003", "IntBool"),
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "GuessStruct"),
            (self._dependencies_for_new_camera_shaker_struct_1, "new_camera_shaker_struct_1", "NewCameraShakerStruct"),
            (self._dependencies_for_new_camera_shaker_struct_2, "new_camera_shaker_struct_2", "NewCameraShakerStruct"),
            (self._dependencies_for_new_camera_shaker_struct_3, "new_camera_shaker_struct_3", "NewCameraShakerStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for NewCameraShaker.{field_name} ({field_type}): {e}"
                )
