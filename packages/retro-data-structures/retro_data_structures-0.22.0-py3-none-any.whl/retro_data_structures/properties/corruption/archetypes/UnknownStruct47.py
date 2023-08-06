# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct47(BaseProperty):
    attack_speed: float = dataclasses.field(default=15.0)
    delay_time: float = dataclasses.field(default=2.0)
    drop_delay: float = dataclasses.field(default=2.0)
    launch_speed: float = dataclasses.field(default=5.0)
    drop_height: float = dataclasses.field(default=5.0)
    radius_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    collision_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    turn_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    explode_range: float = dataclasses.field(default=1.0)

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
        data.write(b'\x00\t')  # 9 properties

        data.write(b'l\n+\xc8')  # 0x6c0a2bc8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_speed))

        data.write(b'\x8e\x16\xe0\x12')  # 0x8e16e012
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_time))

        data.write(b'\x00\x97\xf2\x82')  # 0x97f282
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drop_delay))

        data.write(b'18\x1a\x17')  # 0x31381a17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_speed))

        data.write(b'8\xa5Vo')  # 0x38a5566f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drop_height))

        data.write(b'\x08mX\xdd')  # 0x86d58dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.radius_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'.hl*')  # 0x2e686c2a
        data.write(b'\x00\x0c')  # size
        self.collision_offset.to_stream(data)

        data.write(b'\xc4\xc3\x94\x03')  # 0xc4c39403
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.turn_sound))

        data.write(b'\x9a\x9a9\xb3')  # 0x9a9a39b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.explode_range))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            attack_speed=data['attack_speed'],
            delay_time=data['delay_time'],
            drop_delay=data['drop_delay'],
            launch_speed=data['launch_speed'],
            drop_height=data['drop_height'],
            radius_damage=DamageInfo.from_json(data['radius_damage']),
            collision_offset=Vector.from_json(data['collision_offset']),
            turn_sound=data['turn_sound'],
            explode_range=data['explode_range'],
        )

    def to_json(self) -> dict:
        return {
            'attack_speed': self.attack_speed,
            'delay_time': self.delay_time,
            'drop_delay': self.drop_delay,
            'launch_speed': self.launch_speed,
            'drop_height': self.drop_height,
            'radius_damage': self.radius_damage.to_json(),
            'collision_offset': self.collision_offset.to_json(),
            'turn_sound': self.turn_sound,
            'explode_range': self.explode_range,
        }


def _decode_attack_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_collision_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_turn_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_explode_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6c0a2bc8: ('attack_speed', _decode_attack_speed),
    0x8e16e012: ('delay_time', _decode_delay_time),
    0x97f282: ('drop_delay', _decode_drop_delay),
    0x31381a17: ('launch_speed', _decode_launch_speed),
    0x38a5566f: ('drop_height', _decode_drop_height),
    0x86d58dd: ('radius_damage', _decode_radius_damage),
    0x2e686c2a: ('collision_offset', _decode_collision_offset),
    0xc4c39403: ('turn_sound', _decode_turn_sound),
    0x9a9a39b3: ('explode_range', _decode_explode_range),
}
