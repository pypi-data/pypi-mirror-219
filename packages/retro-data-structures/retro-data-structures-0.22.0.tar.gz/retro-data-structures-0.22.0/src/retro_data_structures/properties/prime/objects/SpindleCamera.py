# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.prime.archetypes.PlayerHintStruct import PlayerHintStruct
from retro_data_structures.properties.prime.archetypes.SpindleCameraStruct import SpindleCameraStruct
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class SpindleCamera(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    unknown_1: bool = dataclasses.field(default=False)
    unnamed: PlayerHintStruct = dataclasses.field(default_factory=PlayerHintStruct)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: float = dataclasses.field(default=0.0)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    spindle_camera_struct_1: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_2: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_3: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_4: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_5: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_6: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_7: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_8: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_9: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_10: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_11: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_12: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_13: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_14: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)
    spindle_camera_struct_15: SpindleCameraStruct = dataclasses.field(default_factory=SpindleCameraStruct)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x71

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unnamed = PlayerHintStruct.from_stream(data, property_size)
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = struct.unpack('>f', data.read(4))[0]
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        spindle_camera_struct_1 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_2 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_3 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_4 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_5 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_6 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_7 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_8 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_9 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_10 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_11 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_12 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_13 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_14 = SpindleCameraStruct.from_stream(data, property_size)
        spindle_camera_struct_15 = SpindleCameraStruct.from_stream(data, property_size)
        return cls(name, position, rotation, unknown_1, unnamed, unknown_2, unknown_3, unknown_4, unknown_5, spindle_camera_struct_1, spindle_camera_struct_2, spindle_camera_struct_3, spindle_camera_struct_4, spindle_camera_struct_5, spindle_camera_struct_6, spindle_camera_struct_7, spindle_camera_struct_8, spindle_camera_struct_9, spindle_camera_struct_10, spindle_camera_struct_11, spindle_camera_struct_12, spindle_camera_struct_13, spindle_camera_struct_14, spindle_camera_struct_15)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00\x18')  # 24 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        data.write(struct.pack('>?', self.unknown_1))
        self.unnamed.to_stream(data)
        data.write(struct.pack('>f', self.unknown_2))
        data.write(struct.pack('>f', self.unknown_3))
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        self.spindle_camera_struct_1.to_stream(data)
        self.spindle_camera_struct_2.to_stream(data)
        self.spindle_camera_struct_3.to_stream(data)
        self.spindle_camera_struct_4.to_stream(data)
        self.spindle_camera_struct_5.to_stream(data)
        self.spindle_camera_struct_6.to_stream(data)
        self.spindle_camera_struct_7.to_stream(data)
        self.spindle_camera_struct_8.to_stream(data)
        self.spindle_camera_struct_9.to_stream(data)
        self.spindle_camera_struct_10.to_stream(data)
        self.spindle_camera_struct_11.to_stream(data)
        self.spindle_camera_struct_12.to_stream(data)
        self.spindle_camera_struct_13.to_stream(data)
        self.spindle_camera_struct_14.to_stream(data)
        self.spindle_camera_struct_15.to_stream(data)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            unknown_1=data['unknown_1'],
            unnamed=PlayerHintStruct.from_json(data['unnamed']),
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            spindle_camera_struct_1=SpindleCameraStruct.from_json(data['spindle_camera_struct_1']),
            spindle_camera_struct_2=SpindleCameraStruct.from_json(data['spindle_camera_struct_2']),
            spindle_camera_struct_3=SpindleCameraStruct.from_json(data['spindle_camera_struct_3']),
            spindle_camera_struct_4=SpindleCameraStruct.from_json(data['spindle_camera_struct_4']),
            spindle_camera_struct_5=SpindleCameraStruct.from_json(data['spindle_camera_struct_5']),
            spindle_camera_struct_6=SpindleCameraStruct.from_json(data['spindle_camera_struct_6']),
            spindle_camera_struct_7=SpindleCameraStruct.from_json(data['spindle_camera_struct_7']),
            spindle_camera_struct_8=SpindleCameraStruct.from_json(data['spindle_camera_struct_8']),
            spindle_camera_struct_9=SpindleCameraStruct.from_json(data['spindle_camera_struct_9']),
            spindle_camera_struct_10=SpindleCameraStruct.from_json(data['spindle_camera_struct_10']),
            spindle_camera_struct_11=SpindleCameraStruct.from_json(data['spindle_camera_struct_11']),
            spindle_camera_struct_12=SpindleCameraStruct.from_json(data['spindle_camera_struct_12']),
            spindle_camera_struct_13=SpindleCameraStruct.from_json(data['spindle_camera_struct_13']),
            spindle_camera_struct_14=SpindleCameraStruct.from_json(data['spindle_camera_struct_14']),
            spindle_camera_struct_15=SpindleCameraStruct.from_json(data['spindle_camera_struct_15']),
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'unknown_1': self.unknown_1,
            'unnamed': self.unnamed.to_json(),
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'spindle_camera_struct_1': self.spindle_camera_struct_1.to_json(),
            'spindle_camera_struct_2': self.spindle_camera_struct_2.to_json(),
            'spindle_camera_struct_3': self.spindle_camera_struct_3.to_json(),
            'spindle_camera_struct_4': self.spindle_camera_struct_4.to_json(),
            'spindle_camera_struct_5': self.spindle_camera_struct_5.to_json(),
            'spindle_camera_struct_6': self.spindle_camera_struct_6.to_json(),
            'spindle_camera_struct_7': self.spindle_camera_struct_7.to_json(),
            'spindle_camera_struct_8': self.spindle_camera_struct_8.to_json(),
            'spindle_camera_struct_9': self.spindle_camera_struct_9.to_json(),
            'spindle_camera_struct_10': self.spindle_camera_struct_10.to_json(),
            'spindle_camera_struct_11': self.spindle_camera_struct_11.to_json(),
            'spindle_camera_struct_12': self.spindle_camera_struct_12.to_json(),
            'spindle_camera_struct_13': self.spindle_camera_struct_13.to_json(),
            'spindle_camera_struct_14': self.spindle_camera_struct_14.to_json(),
            'spindle_camera_struct_15': self.spindle_camera_struct_15.to_json(),
        }

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_1(self, asset_manager):
        yield from self.spindle_camera_struct_1.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_2(self, asset_manager):
        yield from self.spindle_camera_struct_2.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_3(self, asset_manager):
        yield from self.spindle_camera_struct_3.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_4(self, asset_manager):
        yield from self.spindle_camera_struct_4.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_5(self, asset_manager):
        yield from self.spindle_camera_struct_5.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_6(self, asset_manager):
        yield from self.spindle_camera_struct_6.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_7(self, asset_manager):
        yield from self.spindle_camera_struct_7.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_8(self, asset_manager):
        yield from self.spindle_camera_struct_8.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_9(self, asset_manager):
        yield from self.spindle_camera_struct_9.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_10(self, asset_manager):
        yield from self.spindle_camera_struct_10.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_11(self, asset_manager):
        yield from self.spindle_camera_struct_11.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_12(self, asset_manager):
        yield from self.spindle_camera_struct_12.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_13(self, asset_manager):
        yield from self.spindle_camera_struct_13.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_14(self, asset_manager):
        yield from self.spindle_camera_struct_14.dependencies_for(asset_manager)

    def _dependencies_for_spindle_camera_struct_15(self, asset_manager):
        yield from self.spindle_camera_struct_15.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed, "unnamed", "PlayerHintStruct"),
            (self._dependencies_for_spindle_camera_struct_1, "spindle_camera_struct_1", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_2, "spindle_camera_struct_2", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_3, "spindle_camera_struct_3", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_4, "spindle_camera_struct_4", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_5, "spindle_camera_struct_5", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_6, "spindle_camera_struct_6", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_7, "spindle_camera_struct_7", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_8, "spindle_camera_struct_8", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_9, "spindle_camera_struct_9", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_10, "spindle_camera_struct_10", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_11, "spindle_camera_struct_11", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_12, "spindle_camera_struct_12", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_13, "spindle_camera_struct_13", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_14, "spindle_camera_struct_14", "SpindleCameraStruct"),
            (self._dependencies_for_spindle_camera_struct_15, "spindle_camera_struct_15", "SpindleCameraStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SpindleCamera.{field_name} ({field_type}): {e}"
                )
