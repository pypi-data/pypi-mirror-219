# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.RobotChickenFlyerStructB import RobotChickenFlyerStructB


@dataclasses.dataclass()
class UnknownStruct261(BaseProperty):
    attack_selector: enums.RobotChickenEnum = dataclasses.field(default=enums.RobotChickenEnum.Unknown1)
    health: float = dataclasses.field(default=3.0)
    robot_chicken_flyer_struct_b_0x002cfe87: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB)
    robot_chicken_flyer_struct_b_0x76c9c7ba: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB)
    robot_chicken_flyer_struct_b_0xedba2d6e: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB)
    robot_chicken_flyer_struct_b_0x9b03b5c0: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB)
    robot_chicken_flyer_struct_b_0x00705f14: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB)
    robot_chicken_flyer_struct_b_0x76956629: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB)
    robot_chicken_flyer_struct_b_0xede68cfd: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB)

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

        data.write(b'\x00,\xfe\x87')  # 0x2cfe87
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x002cfe87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xc9\xc7\xba')  # 0x76c9c7ba
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x76c9c7ba.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xba-n')  # 0xedba2d6e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0xedba2d6e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\x03\xb5\xc0')  # 0x9b03b5c0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x9b03b5c0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00p_\x14')  # 0x705f14
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x00705f14.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\x95f)')  # 0x76956629
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x76956629.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xe6\x8c\xfd')  # 0xede68cfd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0xede68cfd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            attack_selector=enums.RobotChickenEnum.from_json(data['attack_selector']),
            health=data['health'],
            robot_chicken_flyer_struct_b_0x002cfe87=RobotChickenFlyerStructB.from_json(data['robot_chicken_flyer_struct_b_0x002cfe87']),
            robot_chicken_flyer_struct_b_0x76c9c7ba=RobotChickenFlyerStructB.from_json(data['robot_chicken_flyer_struct_b_0x76c9c7ba']),
            robot_chicken_flyer_struct_b_0xedba2d6e=RobotChickenFlyerStructB.from_json(data['robot_chicken_flyer_struct_b_0xedba2d6e']),
            robot_chicken_flyer_struct_b_0x9b03b5c0=RobotChickenFlyerStructB.from_json(data['robot_chicken_flyer_struct_b_0x9b03b5c0']),
            robot_chicken_flyer_struct_b_0x00705f14=RobotChickenFlyerStructB.from_json(data['robot_chicken_flyer_struct_b_0x00705f14']),
            robot_chicken_flyer_struct_b_0x76956629=RobotChickenFlyerStructB.from_json(data['robot_chicken_flyer_struct_b_0x76956629']),
            robot_chicken_flyer_struct_b_0xede68cfd=RobotChickenFlyerStructB.from_json(data['robot_chicken_flyer_struct_b_0xede68cfd']),
        )

    def to_json(self) -> dict:
        return {
            'attack_selector': self.attack_selector.to_json(),
            'health': self.health,
            'robot_chicken_flyer_struct_b_0x002cfe87': self.robot_chicken_flyer_struct_b_0x002cfe87.to_json(),
            'robot_chicken_flyer_struct_b_0x76c9c7ba': self.robot_chicken_flyer_struct_b_0x76c9c7ba.to_json(),
            'robot_chicken_flyer_struct_b_0xedba2d6e': self.robot_chicken_flyer_struct_b_0xedba2d6e.to_json(),
            'robot_chicken_flyer_struct_b_0x9b03b5c0': self.robot_chicken_flyer_struct_b_0x9b03b5c0.to_json(),
            'robot_chicken_flyer_struct_b_0x00705f14': self.robot_chicken_flyer_struct_b_0x00705f14.to_json(),
            'robot_chicken_flyer_struct_b_0x76956629': self.robot_chicken_flyer_struct_b_0x76956629.to_json(),
            'robot_chicken_flyer_struct_b_0xede68cfd': self.robot_chicken_flyer_struct_b_0xede68cfd.to_json(),
        }


def _decode_attack_selector(data: typing.BinaryIO, property_size: int):
    return enums.RobotChickenEnum.from_stream(data)


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_robot_chicken_flyer_struct_b_0x002cfe87(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructB.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_b_0x76c9c7ba(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructB.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_b_0xedba2d6e(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructB.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_b_0x9b03b5c0(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructB.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_b_0x00705f14(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructB.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_b_0x76956629(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructB.from_stream(data, property_size)


def _decode_robot_chicken_flyer_struct_b_0xede68cfd(data: typing.BinaryIO, property_size: int):
    return RobotChickenFlyerStructB.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97d30f8b: ('attack_selector', _decode_attack_selector),
    0xf0668919: ('health', _decode_health),
    0x2cfe87: ('robot_chicken_flyer_struct_b_0x002cfe87', _decode_robot_chicken_flyer_struct_b_0x002cfe87),
    0x76c9c7ba: ('robot_chicken_flyer_struct_b_0x76c9c7ba', _decode_robot_chicken_flyer_struct_b_0x76c9c7ba),
    0xedba2d6e: ('robot_chicken_flyer_struct_b_0xedba2d6e', _decode_robot_chicken_flyer_struct_b_0xedba2d6e),
    0x9b03b5c0: ('robot_chicken_flyer_struct_b_0x9b03b5c0', _decode_robot_chicken_flyer_struct_b_0x9b03b5c0),
    0x705f14: ('robot_chicken_flyer_struct_b_0x00705f14', _decode_robot_chicken_flyer_struct_b_0x00705f14),
    0x76956629: ('robot_chicken_flyer_struct_b_0x76956629', _decode_robot_chicken_flyer_struct_b_0x76956629),
    0xede68cfd: ('robot_chicken_flyer_struct_b_0xede68cfd', _decode_robot_chicken_flyer_struct_b_0xede68cfd),
}
