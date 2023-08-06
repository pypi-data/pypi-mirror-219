# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.dkc_returns.archetypes.PlayerJumpHeights import PlayerJumpHeights


@dataclasses.dataclass()
class PlayerJumpData(BaseProperty):
    normal_jump_heights: PlayerJumpHeights = dataclasses.field(default_factory=PlayerJumpHeights)
    tar_inhibited_jump_heights: PlayerJumpHeights = dataclasses.field(default_factory=PlayerJumpHeights)
    jump_tap_time: float = dataclasses.field(default=0.05000000074505806)
    jump_pressed_early_maximum_time: float = dataclasses.field(default=0.12099999934434891)
    jump_bump_into_wall_speed: float = dataclasses.field(default=3.0)
    jump_crash_into_wall_speed: float = dataclasses.field(default=6.0)
    jump_bump_into_ceiling_speed: float = dataclasses.field(default=3.0)
    jump_crash_into_ceiling_speed: float = dataclasses.field(default=6.0)
    jump_wall_hit_hang_time: float = dataclasses.field(default=0.10000000149011612)
    jump_bump_into_wall_knockback_amount: float = dataclasses.field(default=0.25)
    jump_bump_into_wall_knockback_time: float = dataclasses.field(default=0.25)
    require_controller_input_for_jump_turns: bool = dataclasses.field(default=False)

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
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\x8b\xa1\xa2\x1a')  # 0x8ba1a21a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_jump_heights.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1c\x9ao\x1b')  # 0x1c9a6f1b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tar_inhibited_jump_heights.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x*\x03\x10')  # 0x782a0310
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_tap_time))

        data.write(b'\xca\xae\xc6\x8e')  # 0xcaaec68e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_pressed_early_maximum_time))

        data.write(b'i\xe6V\x8d')  # 0x69e6568d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_bump_into_wall_speed))

        data.write(b'\x16\xa7\xfb\x91')  # 0x16a7fb91
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_crash_into_wall_speed))

        data.write(b'\xe5p\xe6\xfe')  # 0xe570e6fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_bump_into_ceiling_speed))

        data.write(b'\xea>\x0f7')  # 0xea3e0f37
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_crash_into_ceiling_speed))

        data.write(b'Cl\xb2\xe7')  # 0x436cb2e7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_wall_hit_hang_time))

        data.write(b'\x9b\xa3\xf6q')  # 0x9ba3f671
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_bump_into_wall_knockback_amount))

        data.write(b'\x80\xfa\xa2\xf3')  # 0x80faa2f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_bump_into_wall_knockback_time))

        data.write(b'qb\xd6x')  # 0x7162d678
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.require_controller_input_for_jump_turns))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            normal_jump_heights=PlayerJumpHeights.from_json(data['normal_jump_heights']),
            tar_inhibited_jump_heights=PlayerJumpHeights.from_json(data['tar_inhibited_jump_heights']),
            jump_tap_time=data['jump_tap_time'],
            jump_pressed_early_maximum_time=data['jump_pressed_early_maximum_time'],
            jump_bump_into_wall_speed=data['jump_bump_into_wall_speed'],
            jump_crash_into_wall_speed=data['jump_crash_into_wall_speed'],
            jump_bump_into_ceiling_speed=data['jump_bump_into_ceiling_speed'],
            jump_crash_into_ceiling_speed=data['jump_crash_into_ceiling_speed'],
            jump_wall_hit_hang_time=data['jump_wall_hit_hang_time'],
            jump_bump_into_wall_knockback_amount=data['jump_bump_into_wall_knockback_amount'],
            jump_bump_into_wall_knockback_time=data['jump_bump_into_wall_knockback_time'],
            require_controller_input_for_jump_turns=data['require_controller_input_for_jump_turns'],
        )

    def to_json(self) -> dict:
        return {
            'normal_jump_heights': self.normal_jump_heights.to_json(),
            'tar_inhibited_jump_heights': self.tar_inhibited_jump_heights.to_json(),
            'jump_tap_time': self.jump_tap_time,
            'jump_pressed_early_maximum_time': self.jump_pressed_early_maximum_time,
            'jump_bump_into_wall_speed': self.jump_bump_into_wall_speed,
            'jump_crash_into_wall_speed': self.jump_crash_into_wall_speed,
            'jump_bump_into_ceiling_speed': self.jump_bump_into_ceiling_speed,
            'jump_crash_into_ceiling_speed': self.jump_crash_into_ceiling_speed,
            'jump_wall_hit_hang_time': self.jump_wall_hit_hang_time,
            'jump_bump_into_wall_knockback_amount': self.jump_bump_into_wall_knockback_amount,
            'jump_bump_into_wall_knockback_time': self.jump_bump_into_wall_knockback_time,
            'require_controller_input_for_jump_turns': self.require_controller_input_for_jump_turns,
        }


def _decode_normal_jump_heights(data: typing.BinaryIO, property_size: int):
    return PlayerJumpHeights.from_stream(data, property_size)


def _decode_tar_inhibited_jump_heights(data: typing.BinaryIO, property_size: int):
    return PlayerJumpHeights.from_stream(data, property_size)


def _decode_jump_tap_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_pressed_early_maximum_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_bump_into_wall_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_crash_into_wall_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_bump_into_ceiling_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_crash_into_ceiling_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_wall_hit_hang_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_bump_into_wall_knockback_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_bump_into_wall_knockback_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_require_controller_input_for_jump_turns(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8ba1a21a: ('normal_jump_heights', _decode_normal_jump_heights),
    0x1c9a6f1b: ('tar_inhibited_jump_heights', _decode_tar_inhibited_jump_heights),
    0x782a0310: ('jump_tap_time', _decode_jump_tap_time),
    0xcaaec68e: ('jump_pressed_early_maximum_time', _decode_jump_pressed_early_maximum_time),
    0x69e6568d: ('jump_bump_into_wall_speed', _decode_jump_bump_into_wall_speed),
    0x16a7fb91: ('jump_crash_into_wall_speed', _decode_jump_crash_into_wall_speed),
    0xe570e6fe: ('jump_bump_into_ceiling_speed', _decode_jump_bump_into_ceiling_speed),
    0xea3e0f37: ('jump_crash_into_ceiling_speed', _decode_jump_crash_into_ceiling_speed),
    0x436cb2e7: ('jump_wall_hit_hang_time', _decode_jump_wall_hit_hang_time),
    0x9ba3f671: ('jump_bump_into_wall_knockback_amount', _decode_jump_bump_into_wall_knockback_amount),
    0x80faa2f3: ('jump_bump_into_wall_knockback_time', _decode_jump_bump_into_wall_knockback_time),
    0x7162d678: ('require_controller_input_for_jump_turns', _decode_require_controller_input_for_jump_turns),
}
