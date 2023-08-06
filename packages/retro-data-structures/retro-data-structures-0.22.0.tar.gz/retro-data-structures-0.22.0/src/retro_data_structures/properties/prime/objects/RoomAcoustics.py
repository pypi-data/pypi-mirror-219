# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType


@dataclasses.dataclass()
class RoomAcoustics(BaseObjectType):
    name: str = dataclasses.field(default='')
    unknown_1: bool = dataclasses.field(default=False)
    unknown_2: int = dataclasses.field(default=0)
    unknown_3: bool = dataclasses.field(default=False)
    unknown_4: bool = dataclasses.field(default=False)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    unknown_8: float = dataclasses.field(default=0.0)
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: bool = dataclasses.field(default=False)
    unknown_12: float = dataclasses.field(default=0.0)
    unknown_13: float = dataclasses.field(default=0.0)
    unknown_14: float = dataclasses.field(default=0.0)
    unknown_15: bool = dataclasses.field(default=False)
    unknown_16: bool = dataclasses.field(default=False)
    unknown_17: float = dataclasses.field(default=0.0)
    unknown_18: float = dataclasses.field(default=0.0)
    unknown_19: float = dataclasses.field(default=0.0)
    unknown_20: float = dataclasses.field(default=0.0)
    unknown_21: float = dataclasses.field(default=0.0)
    unknown_22: bool = dataclasses.field(default=False)
    unknown_23: int = dataclasses.field(default=0)
    unknown_24: int = dataclasses.field(default=0)
    unknown_25: int = dataclasses.field(default=0)
    unknown_26: int = dataclasses.field(default=0)
    unknown_27: int = dataclasses.field(default=0)
    unknown_28: int = dataclasses.field(default=0)
    unknown_29: int = dataclasses.field(default=0)
    unknown_30: int = dataclasses.field(default=0)
    unknown_31: int = dataclasses.field(default=0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x5D

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        unknown_1 = struct.unpack('>?', data.read(1))[0]
        unknown_2 = struct.unpack('>l', data.read(4))[0]
        unknown_3 = struct.unpack('>?', data.read(1))[0]
        unknown_4 = struct.unpack('>?', data.read(1))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>?', data.read(1))[0]
        unknown_12 = struct.unpack('>f', data.read(4))[0]
        unknown_13 = struct.unpack('>f', data.read(4))[0]
        unknown_14 = struct.unpack('>f', data.read(4))[0]
        unknown_15 = struct.unpack('>?', data.read(1))[0]
        unknown_16 = struct.unpack('>?', data.read(1))[0]
        unknown_17 = struct.unpack('>f', data.read(4))[0]
        unknown_18 = struct.unpack('>f', data.read(4))[0]
        unknown_19 = struct.unpack('>f', data.read(4))[0]
        unknown_20 = struct.unpack('>f', data.read(4))[0]
        unknown_21 = struct.unpack('>f', data.read(4))[0]
        unknown_22 = struct.unpack('>?', data.read(1))[0]
        unknown_23 = struct.unpack('>l', data.read(4))[0]
        unknown_24 = struct.unpack('>l', data.read(4))[0]
        unknown_25 = struct.unpack('>l', data.read(4))[0]
        unknown_26 = struct.unpack('>l', data.read(4))[0]
        unknown_27 = struct.unpack('>l', data.read(4))[0]
        unknown_28 = struct.unpack('>l', data.read(4))[0]
        unknown_29 = struct.unpack('>l', data.read(4))[0]
        unknown_30 = struct.unpack('>l', data.read(4))[0]
        unknown_31 = struct.unpack('>l', data.read(4))[0]
        return cls(name, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, unknown_13, unknown_14, unknown_15, unknown_16, unknown_17, unknown_18, unknown_19, unknown_20, unknown_21, unknown_22, unknown_23, unknown_24, unknown_25, unknown_26, unknown_27, unknown_28, unknown_29, unknown_30, unknown_31)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00 ')  # 32 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        data.write(struct.pack('>?', self.unknown_1))
        data.write(struct.pack('>l', self.unknown_2))
        data.write(struct.pack('>?', self.unknown_3))
        data.write(struct.pack('>?', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>?', self.unknown_11))
        data.write(struct.pack('>f', self.unknown_12))
        data.write(struct.pack('>f', self.unknown_13))
        data.write(struct.pack('>f', self.unknown_14))
        data.write(struct.pack('>?', self.unknown_15))
        data.write(struct.pack('>?', self.unknown_16))
        data.write(struct.pack('>f', self.unknown_17))
        data.write(struct.pack('>f', self.unknown_18))
        data.write(struct.pack('>f', self.unknown_19))
        data.write(struct.pack('>f', self.unknown_20))
        data.write(struct.pack('>f', self.unknown_21))
        data.write(struct.pack('>?', self.unknown_22))
        data.write(struct.pack('>l', self.unknown_23))
        data.write(struct.pack('>l', self.unknown_24))
        data.write(struct.pack('>l', self.unknown_25))
        data.write(struct.pack('>l', self.unknown_26))
        data.write(struct.pack('>l', self.unknown_27))
        data.write(struct.pack('>l', self.unknown_28))
        data.write(struct.pack('>l', self.unknown_29))
        data.write(struct.pack('>l', self.unknown_30))
        data.write(struct.pack('>l', self.unknown_31))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
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
            unknown_20=data['unknown_20'],
            unknown_21=data['unknown_21'],
            unknown_22=data['unknown_22'],
            unknown_23=data['unknown_23'],
            unknown_24=data['unknown_24'],
            unknown_25=data['unknown_25'],
            unknown_26=data['unknown_26'],
            unknown_27=data['unknown_27'],
            unknown_28=data['unknown_28'],
            unknown_29=data['unknown_29'],
            unknown_30=data['unknown_30'],
            unknown_31=data['unknown_31'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
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
            'unknown_20': self.unknown_20,
            'unknown_21': self.unknown_21,
            'unknown_22': self.unknown_22,
            'unknown_23': self.unknown_23,
            'unknown_24': self.unknown_24,
            'unknown_25': self.unknown_25,
            'unknown_26': self.unknown_26,
            'unknown_27': self.unknown_27,
            'unknown_28': self.unknown_28,
            'unknown_29': self.unknown_29,
            'unknown_30': self.unknown_30,
            'unknown_31': self.unknown_31,
        }

    def dependencies_for(self, asset_manager):
        yield from []
