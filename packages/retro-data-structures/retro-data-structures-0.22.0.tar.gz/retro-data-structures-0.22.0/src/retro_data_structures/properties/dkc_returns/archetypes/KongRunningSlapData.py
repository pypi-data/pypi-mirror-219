# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerAttackBounceData import PlayerAttackBounceData
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector


@dataclasses.dataclass()
class KongRunningSlapData(BaseProperty):
    running_slap_box_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=30.0, y=30.0, z=30.0))
    delay_jumping_after_running_slap: float = dataclasses.field(default=0.25)
    roll_controller_motion_detection_time: float = dataclasses.field(default=0.125)
    jump_from_roll_control_scalar: float = dataclasses.field(default=2.0)
    minimum_jump_height: float = dataclasses.field(default=2.0)
    maximum_jump_height: float = dataclasses.field(default=4.599999904632568)
    attack_bounce_data: PlayerAttackBounceData = dataclasses.field(default_factory=PlayerAttackBounceData)
    min_horizontal_controller_movement_to_trigger_running_slap: float = dataclasses.field(default=0.5)
    min_speed_to_trigger_running_slap: float = dataclasses.field(default=6.0)
    speed_multiplier: float = dataclasses.field(default=1.5)
    roll_duration: float = dataclasses.field(default=1.0)
    disallow_turn_duration: float = dataclasses.field(default=0.10000000149011612)
    roll_slap_duration: float = dataclasses.field(default=0.5)
    delay_between_rolls: float = dataclasses.field(default=0.4000000059604645)
    roll_attack_damage_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'F2"\x87')  # 0x46322287
        data.write(b'\x00\x0c')  # size
        self.running_slap_box_scale.to_stream(data)

        data.write(b'\x8ae\xfdg')  # 0x8a65fd67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_jumping_after_running_slap))

        data.write(b'3g\xbc\xa4')  # 0x3367bca4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.roll_controller_motion_detection_time))

        data.write(b'"\x15\xe6t')  # 0x2215e674
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_from_roll_control_scalar))

        data.write(b'yz\xa5Q')  # 0x797aa551
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_jump_height))

        data.write(b'8m\x9a\xd7')  # 0x386d9ad7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_jump_height))

        data.write(b'\x95\x83\xee\x9a')  # 0x9583ee9a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attack_bounce_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16\xb2a\xf8')  # 0x16b261f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_horizontal_controller_movement_to_trigger_running_slap))

        data.write(b'8uN\xc2')  # 0x38754ec2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_speed_to_trigger_running_slap))

        data.write(b'H\x85\xdf\xfa')  # 0x4885dffa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed_multiplier))

        data.write(b'\xc5\xa9!\xf0')  # 0xc5a921f0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.roll_duration))

        data.write(b'^\xe0gj')  # 0x5ee0676a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.disallow_turn_duration))

        data.write(b'+HPg')  # 0x2b485067
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.roll_slap_duration))

        data.write(b'A3\xdb\xe2')  # 0x4133dbe2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_between_rolls))

        data.write(b'\x9a\xdaD\xf7')  # 0x9ada44f7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.roll_attack_damage_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            running_slap_box_scale=Vector.from_json(data['running_slap_box_scale']),
            delay_jumping_after_running_slap=data['delay_jumping_after_running_slap'],
            roll_controller_motion_detection_time=data['roll_controller_motion_detection_time'],
            jump_from_roll_control_scalar=data['jump_from_roll_control_scalar'],
            minimum_jump_height=data['minimum_jump_height'],
            maximum_jump_height=data['maximum_jump_height'],
            attack_bounce_data=PlayerAttackBounceData.from_json(data['attack_bounce_data']),
            min_horizontal_controller_movement_to_trigger_running_slap=data['min_horizontal_controller_movement_to_trigger_running_slap'],
            min_speed_to_trigger_running_slap=data['min_speed_to_trigger_running_slap'],
            speed_multiplier=data['speed_multiplier'],
            roll_duration=data['roll_duration'],
            disallow_turn_duration=data['disallow_turn_duration'],
            roll_slap_duration=data['roll_slap_duration'],
            delay_between_rolls=data['delay_between_rolls'],
            roll_attack_damage_sound=data['roll_attack_damage_sound'],
        )

    def to_json(self) -> dict:
        return {
            'running_slap_box_scale': self.running_slap_box_scale.to_json(),
            'delay_jumping_after_running_slap': self.delay_jumping_after_running_slap,
            'roll_controller_motion_detection_time': self.roll_controller_motion_detection_time,
            'jump_from_roll_control_scalar': self.jump_from_roll_control_scalar,
            'minimum_jump_height': self.minimum_jump_height,
            'maximum_jump_height': self.maximum_jump_height,
            'attack_bounce_data': self.attack_bounce_data.to_json(),
            'min_horizontal_controller_movement_to_trigger_running_slap': self.min_horizontal_controller_movement_to_trigger_running_slap,
            'min_speed_to_trigger_running_slap': self.min_speed_to_trigger_running_slap,
            'speed_multiplier': self.speed_multiplier,
            'roll_duration': self.roll_duration,
            'disallow_turn_duration': self.disallow_turn_duration,
            'roll_slap_duration': self.roll_slap_duration,
            'delay_between_rolls': self.delay_between_rolls,
            'roll_attack_damage_sound': self.roll_attack_damage_sound,
        }


def _decode_running_slap_box_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_delay_jumping_after_running_slap(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_controller_motion_detection_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_from_roll_control_scalar(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_bounce_data(data: typing.BinaryIO, property_size: int):
    return PlayerAttackBounceData.from_stream(data, property_size)


def _decode_min_horizontal_controller_movement_to_trigger_running_slap(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_speed_to_trigger_running_slap(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_speed_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_disallow_turn_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_slap_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_between_rolls(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_roll_attack_damage_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x46322287: ('running_slap_box_scale', _decode_running_slap_box_scale),
    0x8a65fd67: ('delay_jumping_after_running_slap', _decode_delay_jumping_after_running_slap),
    0x3367bca4: ('roll_controller_motion_detection_time', _decode_roll_controller_motion_detection_time),
    0x2215e674: ('jump_from_roll_control_scalar', _decode_jump_from_roll_control_scalar),
    0x797aa551: ('minimum_jump_height', _decode_minimum_jump_height),
    0x386d9ad7: ('maximum_jump_height', _decode_maximum_jump_height),
    0x9583ee9a: ('attack_bounce_data', _decode_attack_bounce_data),
    0x16b261f8: ('min_horizontal_controller_movement_to_trigger_running_slap', _decode_min_horizontal_controller_movement_to_trigger_running_slap),
    0x38754ec2: ('min_speed_to_trigger_running_slap', _decode_min_speed_to_trigger_running_slap),
    0x4885dffa: ('speed_multiplier', _decode_speed_multiplier),
    0xc5a921f0: ('roll_duration', _decode_roll_duration),
    0x5ee0676a: ('disallow_turn_duration', _decode_disallow_turn_duration),
    0x2b485067: ('roll_slap_duration', _decode_roll_slap_duration),
    0x4133dbe2: ('delay_between_rolls', _decode_delay_between_rolls),
    0x9ada44f7: ('roll_attack_damage_sound', _decode_roll_attack_damage_sound),
}
