# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.UnknownStruct7 import UnknownStruct7


@dataclasses.dataclass()
class UnknownStruct14(BaseProperty):
    turn_speed: float = dataclasses.field(default=540.0)
    movement_speed: float = dataclasses.field(default=75.0)
    unknown_0x79d90292: float = dataclasses.field(default=250.0)
    unknown_0x4839dde0: float = dataclasses.field(default=10.0)
    unknown_0x092ee266: float = dataclasses.field(default=15.0)
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_struct7: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7)

    @classmethod
    def game(cls) -> Game:
        return Game.CORRUPTION

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_count = struct.unpack(">H", data.read(2))[0]
        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'\x02\x0cx\xbb')  # 0x20c78bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_speed))

        data.write(b'Ao\x15\xe8')  # 0x416f15e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_speed))

        data.write(b'y\xd9\x02\x92')  # 0x79d90292
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x79d90292))

        data.write(b'H9\xdd\xe0')  # 0x4839dde0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4839dde0))

        data.write(b'\t.\xe2f')  # 0x92ee266
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x092ee266))

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'e\x9d\xf7m')  # 0x659df76d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            turn_speed=data['turn_speed'],
            movement_speed=data['movement_speed'],
            unknown_0x79d90292=data['unknown_0x79d90292'],
            unknown_0x4839dde0=data['unknown_0x4839dde0'],
            unknown_0x092ee266=data['unknown_0x092ee266'],
            damage=DamageInfo.from_json(data['damage']),
            unknown_struct7=UnknownStruct7.from_json(data['unknown_struct7']),
        )

    def to_json(self) -> dict:
        return {
            'turn_speed': self.turn_speed,
            'movement_speed': self.movement_speed,
            'unknown_0x79d90292': self.unknown_0x79d90292,
            'unknown_0x4839dde0': self.unknown_0x4839dde0,
            'unknown_0x092ee266': self.unknown_0x092ee266,
            'damage': self.damage.to_json(),
            'unknown_struct7': self.unknown_struct7.to_json(),
        }


def _decode_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x79d90292(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4839dde0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x092ee266(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_struct7(data: typing.BinaryIO, property_size: int):
    return UnknownStruct7.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x20c78bb: ('turn_speed', _decode_turn_speed),
    0x416f15e8: ('movement_speed', _decode_movement_speed),
    0x79d90292: ('unknown_0x79d90292', _decode_unknown_0x79d90292),
    0x4839dde0: ('unknown_0x4839dde0', _decode_unknown_0x4839dde0),
    0x92ee266: ('unknown_0x092ee266', _decode_unknown_0x092ee266),
    0x337f9524: ('damage', _decode_damage),
    0x659df76d: ('unknown_struct7', _decode_unknown_struct7),
}
