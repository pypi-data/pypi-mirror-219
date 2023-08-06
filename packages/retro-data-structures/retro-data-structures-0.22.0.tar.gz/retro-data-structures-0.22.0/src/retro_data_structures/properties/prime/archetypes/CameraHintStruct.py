# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty


@dataclasses.dataclass()
class CameraHintStruct(BaseProperty):
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: bool = dataclasses.field(default=False)
    unknown_3: bool = dataclasses.field(default=False)
    unknown_4: bool = dataclasses.field(default=False)
    unknown_5: bool = dataclasses.field(default=False)
    unknown_6: bool = dataclasses.field(default=False)
    unknown_7: bool = dataclasses.field(default=False)
    unknown_8: bool = dataclasses.field(default=False)
    unknown_9: bool = dataclasses.field(default=False)
    unknown_10: bool = dataclasses.field(default=False)
    unknown_11: bool = dataclasses.field(default=False)
    unknown_12: bool = dataclasses.field(default=False)
    unknown_13: bool = dataclasses.field(default=False)
    unknown_14: bool = dataclasses.field(default=False)
    unknown_15: bool = dataclasses.field(default=False)
    unknown_16: bool = dataclasses.field(default=False)
    unknown_17: bool = dataclasses.field(default=False)
    unknown_18: bool = dataclasses.field(default=False)
    unknown_19: bool = dataclasses.field(default=False)
    unknown_21: bool = dataclasses.field(default=False)
    unknown_22: bool = dataclasses.field(default=False)
    unknown_23: bool = dataclasses.field(default=False)

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
        unknown_6 = struct.unpack('>?', data.read(1))[0]
        unknown_7 = struct.unpack('>?', data.read(1))[0]
        unknown_8 = struct.unpack('>?', data.read(1))[0]
        unknown_9 = struct.unpack('>?', data.read(1))[0]
        unknown_10 = struct.unpack('>?', data.read(1))[0]
        unknown_11 = struct.unpack('>?', data.read(1))[0]
        unknown_12 = struct.unpack('>?', data.read(1))[0]
        unknown_13 = struct.unpack('>?', data.read(1))[0]
        unknown_14 = struct.unpack('>?', data.read(1))[0]
        unknown_15 = struct.unpack('>?', data.read(1))[0]
        unknown_16 = struct.unpack('>?', data.read(1))[0]
        unknown_17 = struct.unpack('>?', data.read(1))[0]
        unknown_18 = struct.unpack('>?', data.read(1))[0]
        unknown_19 = struct.unpack('>?', data.read(1))[0]
        unknown_21 = struct.unpack('>?', data.read(1))[0]
        unknown_22 = struct.unpack('>?', data.read(1))[0]
        unknown_23 = struct.unpack('>?', data.read(1))[0]
        return cls(unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13, unknown_14, unknown_15, unknown_16, unknown_17, unknown_18, unknown_19, unknown_21, unknown_22, unknown_23)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>?', self.unknown_2))
        data.write(struct.pack('>?', self.unknown_3))
        data.write(struct.pack('>?', self.unknown_4))
        data.write(struct.pack('>?', self.unknown_5))
        data.write(struct.pack('>?', self.unknown_6))
        data.write(struct.pack('>?', self.unknown_7))
        data.write(struct.pack('>?', self.unknown_8))
        data.write(struct.pack('>?', self.unknown_9))
        data.write(struct.pack('>?', self.unknown_10))
        data.write(struct.pack('>?', self.unknown_11))
        data.write(struct.pack('>?', self.unknown_12))
        data.write(struct.pack('>?', self.unknown_13))
        data.write(struct.pack('>?', self.unknown_14))
        data.write(struct.pack('>?', self.unknown_15))
        data.write(struct.pack('>?', self.unknown_16))
        data.write(struct.pack('>?', self.unknown_17))
        data.write(struct.pack('>?', self.unknown_18))
        data.write(struct.pack('>?', self.unknown_19))
        data.write(struct.pack('>?', self.unknown_21))
        data.write(struct.pack('>?', self.unknown_22))
        data.write(struct.pack('>?', self.unknown_23))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=data['unknown_3'],
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=data['unknown_12'],
            unknown_13=data['unknown_13'],
            unknown_14=data['unknown_14'],
            unknown_15=data['unknown_15'],
            unknown_16=data['unknown_16'],
            unknown_17=data['unknown_17'],
            unknown_18=data['unknown_18'],
            unknown_19=data['unknown_19'],
            unknown_21=data['unknown_21'],
            unknown_22=data['unknown_22'],
            unknown_23=data['unknown_23'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12,
            'unknown_13': self.unknown_13,
            'unknown_14': self.unknown_14,
            'unknown_15': self.unknown_15,
            'unknown_16': self.unknown_16,
            'unknown_17': self.unknown_17,
            'unknown_18': self.unknown_18,
            'unknown_19': self.unknown_19,
            'unknown_21': self.unknown_21,
            'unknown_22': self.unknown_22,
            'unknown_23': self.unknown_23,
        }

    def dependencies_for(self, asset_manager):
        yield from []
