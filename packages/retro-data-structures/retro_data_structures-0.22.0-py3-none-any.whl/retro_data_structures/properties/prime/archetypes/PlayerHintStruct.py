# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class PlayerHintStruct(BaseProperty):
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: bool = dataclasses.field(default=False)
    unknown_3: bool = dataclasses.field(default=False)
    unknown_4: bool = dataclasses.field(default=False)
    unknown_5: bool = dataclasses.field(default=False)
    disable_unmorph: bool = dataclasses.field(default=False)
    disable_morph: bool = dataclasses.field(default=False)
    disable_controls: bool = dataclasses.field(default=False)
    disable_boost: bool = dataclasses.field(default=False)
    activate_combat_visor: bool = dataclasses.field(default=False)
    activate_scan_visor: bool = dataclasses.field(default=False)
    activate_thermal_visor: bool = dataclasses.field(default=False)
    activate_x_ray_visor: bool = dataclasses.field(default=False)
    unknown_6: bool = dataclasses.field(default=False)
    face_object_on_unmorph: bool = dataclasses.field(default=False)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>?', data.read(1))[0]
        unknown_3 = struct.unpack('>?', data.read(1))[0]
        unknown_4 = struct.unpack('>?', data.read(1))[0]
        unknown_5 = struct.unpack('>?', data.read(1))[0]
        disable_unmorph = struct.unpack('>?', data.read(1))[0]
        disable_morph = struct.unpack('>?', data.read(1))[0]
        disable_controls = struct.unpack('>?', data.read(1))[0]
        disable_boost = struct.unpack('>?', data.read(1))[0]
        activate_combat_visor = struct.unpack('>?', data.read(1))[0]
        activate_scan_visor = struct.unpack('>?', data.read(1))[0]
        activate_thermal_visor = struct.unpack('>?', data.read(1))[0]
        activate_x_ray_visor = struct.unpack('>?', data.read(1))[0]
        unknown_6 = struct.unpack('>?', data.read(1))[0]
        face_object_on_unmorph = struct.unpack('>?', data.read(1))[0]
        return cls(unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, disable_unmorph, disable_morph, disable_controls, disable_boost, activate_combat_visor, activate_scan_visor, activate_thermal_visor, activate_x_ray_visor, unknown_6, face_object_on_unmorph)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>?', self.unknown_2))
        data.write(struct.pack('>?', self.unknown_3))
        data.write(struct.pack('>?', self.unknown_4))
        data.write(struct.pack('>?', self.unknown_5))
        data.write(struct.pack('>?', self.disable_unmorph))
        data.write(struct.pack('>?', self.disable_morph))
        data.write(struct.pack('>?', self.disable_controls))
        data.write(struct.pack('>?', self.disable_boost))
        data.write(struct.pack('>?', self.activate_combat_visor))
        data.write(struct.pack('>?', self.activate_scan_visor))
        data.write(struct.pack('>?', self.activate_thermal_visor))
        data.write(struct.pack('>?', self.activate_x_ray_visor))
        data.write(struct.pack('>?', self.unknown_6))
        data.write(struct.pack('>?', self.face_object_on_unmorph))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            disable_unmorph=data['disable_unmorph'],
            disable_morph=data['disable_morph'],
            disable_controls=data['disable_controls'],
            disable_boost=data['disable_boost'],
            activate_combat_visor=data['activate_combat_visor'],
            activate_scan_visor=data['activate_scan_visor'],
            activate_thermal_visor=data['activate_thermal_visor'],
            activate_x_ray_visor=data['activate_x_ray_visor'],
            unknown_6=data['unknown_6'],
            face_object_on_unmorph=data['face_object_on_unmorph'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'disable_unmorph': self.disable_unmorph,
            'disable_morph': self.disable_morph,
            'disable_controls': self.disable_controls,
            'disable_boost': self.disable_boost,
            'activate_combat_visor': self.activate_combat_visor,
            'activate_scan_visor': self.activate_scan_visor,
            'activate_thermal_visor': self.activate_thermal_visor,
            'activate_x_ray_visor': self.activate_x_ray_visor,
            'unknown_6': self.unknown_6,
            'face_object_on_unmorph': self.face_object_on_unmorph,
        }

    def dependencies_for(self, asset_manager):
        yield from []
