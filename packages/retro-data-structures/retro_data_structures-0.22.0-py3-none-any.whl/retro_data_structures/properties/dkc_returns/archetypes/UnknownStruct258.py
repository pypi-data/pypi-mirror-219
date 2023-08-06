# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.RobotChickenStructB import RobotChickenStructB


@dataclasses.dataclass()
class UnknownStruct258(BaseProperty):
    attack_selector: enums.RobotChickenEnum = dataclasses.field(default=enums.RobotChickenEnum.Unknown1)
    health: float = dataclasses.field(default=3.0)
    static_hazard: RobotChickenStructB = dataclasses.field(default_factory=RobotChickenStructB)
    robot_chicken_struct_b_0x8bfefc72: RobotChickenStructB = dataclasses.field(default_factory=RobotChickenStructB)
    robot_chicken_struct_b_0x108d16a6: RobotChickenStructB = dataclasses.field(default_factory=RobotChickenStructB)
    robot_chicken_struct_b_0x66348e08: RobotChickenStructB = dataclasses.field(default_factory=RobotChickenStructB)
    robot_chicken_struct_b_0xfd4764dc: RobotChickenStructB = dataclasses.field(default_factory=RobotChickenStructB)
    robot_chicken_struct_b_0x8ba25de1: RobotChickenStructB = dataclasses.field(default_factory=RobotChickenStructB)
    robot_chicken_struct_b_0x10d1b735: RobotChickenStructB = dataclasses.field(default_factory=RobotChickenStructB)

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x97\xd3\x0f\x8b')  # 0x97d30f8b
        data.write(b'\x00\x04')  # size
        self.attack_selector.to_stream(data)

        data.write(b'\xf0f\x89\x19')  # 0xf0668919
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.health))

        data.write(b'\xfd\x1b\xc5O')  # 0xfd1bc54f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.static_hazard.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\xfe\xfcr')  # 0x8bfefc72
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_b_0x8bfefc72.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10\x8d\x16\xa6')  # 0x108d16a6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_b_0x108d16a6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'f4\x8e\x08')  # 0x66348e08
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_b_0x66348e08.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfdGd\xdc')  # 0xfd4764dc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_b_0xfd4764dc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\xa2]\xe1')  # 0x8ba25de1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_b_0x8ba25de1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10\xd1\xb75')  # 0x10d1b735
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_struct_b_0x10d1b735.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            attack_selector=enums.RobotChickenEnum.from_json(data['attack_selector']),
            health=data['health'],
            static_hazard=RobotChickenStructB.from_json(data['static_hazard']),
            robot_chicken_struct_b_0x8bfefc72=RobotChickenStructB.from_json(data['robot_chicken_struct_b_0x8bfefc72']),
            robot_chicken_struct_b_0x108d16a6=RobotChickenStructB.from_json(data['robot_chicken_struct_b_0x108d16a6']),
            robot_chicken_struct_b_0x66348e08=RobotChickenStructB.from_json(data['robot_chicken_struct_b_0x66348e08']),
            robot_chicken_struct_b_0xfd4764dc=RobotChickenStructB.from_json(data['robot_chicken_struct_b_0xfd4764dc']),
            robot_chicken_struct_b_0x8ba25de1=RobotChickenStructB.from_json(data['robot_chicken_struct_b_0x8ba25de1']),
            robot_chicken_struct_b_0x10d1b735=RobotChickenStructB.from_json(data['robot_chicken_struct_b_0x10d1b735']),
        )

    def to_json(self) -> dict:
        return {
            'attack_selector': self.attack_selector.to_json(),
            'health': self.health,
            'static_hazard': self.static_hazard.to_json(),
            'robot_chicken_struct_b_0x8bfefc72': self.robot_chicken_struct_b_0x8bfefc72.to_json(),
            'robot_chicken_struct_b_0x108d16a6': self.robot_chicken_struct_b_0x108d16a6.to_json(),
            'robot_chicken_struct_b_0x66348e08': self.robot_chicken_struct_b_0x66348e08.to_json(),
            'robot_chicken_struct_b_0xfd4764dc': self.robot_chicken_struct_b_0xfd4764dc.to_json(),
            'robot_chicken_struct_b_0x8ba25de1': self.robot_chicken_struct_b_0x8ba25de1.to_json(),
            'robot_chicken_struct_b_0x10d1b735': self.robot_chicken_struct_b_0x10d1b735.to_json(),
        }


def _decode_attack_selector(data: typing.BinaryIO, property_size: int):
    return enums.RobotChickenEnum.from_stream(data)


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_static_hazard(data: typing.BinaryIO, property_size: int):
    return RobotChickenStructB.from_stream(data, property_size)


def _decode_robot_chicken_struct_b_0x8bfefc72(data: typing.BinaryIO, property_size: int):
    return RobotChickenStructB.from_stream(data, property_size)


def _decode_robot_chicken_struct_b_0x108d16a6(data: typing.BinaryIO, property_size: int):
    return RobotChickenStructB.from_stream(data, property_size)


def _decode_robot_chicken_struct_b_0x66348e08(data: typing.BinaryIO, property_size: int):
    return RobotChickenStructB.from_stream(data, property_size)


def _decode_robot_chicken_struct_b_0xfd4764dc(data: typing.BinaryIO, property_size: int):
    return RobotChickenStructB.from_stream(data, property_size)


def _decode_robot_chicken_struct_b_0x8ba25de1(data: typing.BinaryIO, property_size: int):
    return RobotChickenStructB.from_stream(data, property_size)


def _decode_robot_chicken_struct_b_0x10d1b735(data: typing.BinaryIO, property_size: int):
    return RobotChickenStructB.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97d30f8b: ('attack_selector', _decode_attack_selector),
    0xf0668919: ('health', _decode_health),
    0xfd1bc54f: ('static_hazard', _decode_static_hazard),
    0x8bfefc72: ('robot_chicken_struct_b_0x8bfefc72', _decode_robot_chicken_struct_b_0x8bfefc72),
    0x108d16a6: ('robot_chicken_struct_b_0x108d16a6', _decode_robot_chicken_struct_b_0x108d16a6),
    0x66348e08: ('robot_chicken_struct_b_0x66348e08', _decode_robot_chicken_struct_b_0x66348e08),
    0xfd4764dc: ('robot_chicken_struct_b_0xfd4764dc', _decode_robot_chicken_struct_b_0xfd4764dc),
    0x8ba25de1: ('robot_chicken_struct_b_0x8ba25de1', _decode_robot_chicken_struct_b_0x8ba25de1),
    0x10d1b735: ('robot_chicken_struct_b_0x10d1b735', _decode_robot_chicken_struct_b_0x10d1b735),
}
