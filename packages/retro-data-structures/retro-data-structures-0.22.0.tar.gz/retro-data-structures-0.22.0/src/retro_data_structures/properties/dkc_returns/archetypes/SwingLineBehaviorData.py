# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SwingLineBehaviorData(BaseProperty):
    attach_to_line_locator_name: str = dataclasses.field(default='')
    line_end_point_locator_name: str = dataclasses.field(default='')
    swing_line_additive_length: float = dataclasses.field(default=5.0)
    swing_line_dist_backwards: float = dataclasses.field(default=0.44999998807907104)
    swing_line_type: enums.SwingLineType = dataclasses.field(default=enums.SwingLineType.Unknown1)
    swing_line_max_angle: float = dataclasses.field(default=60.0)
    swing_line_length: float = dataclasses.field(default=2.5)
    time_apex_to_apex: float = dataclasses.field(default=2.0)
    start_position_time_scale: float = dataclasses.field(default=1.0)
    orient_creature_with_line: bool = dataclasses.field(default=True)
    jettison_line_scale_speed: float = dataclasses.field(default=12.0)
    death_line_action: enums.DeathLineAction = dataclasses.field(default=enums.DeathLineAction.Unknown1)
    curve_line_additive_scale: float = dataclasses.field(default=1.0)
    curve_line_ramp_in_speed: float = dataclasses.field(default=3.0)
    curve_line_ramp_out_speed: float = dataclasses.field(default=2.0)
    curve_line_depart_apex_angle_to_ramp_in: float = dataclasses.field(default=20.0)
    curve_line_approach_apex_angle_to_ramp_out: float = dataclasses.field(default=10.0)
    curve_line_middle: bool = dataclasses.field(default=True)
    dwell_dist_from_anchor: float = dataclasses.field(default=0.0)
    dwell_time: float = dataclasses.field(default=3.0)
    climb_down_distance: float = dataclasses.field(default=4.0)
    climb_down_speed: float = dataclasses.field(default=1.5)
    drop_at_line_end: bool = dataclasses.field(default=False)
    drop_to_ground_rule: AssetId = dataclasses.field(metadata={'asset_types': ['RULE']}, default=default_asset_id)
    hang_around_time: float = dataclasses.field(default=2.0)
    climb_up_speed: float = dataclasses.field(default=1.5)
    end_of_line_jiggle_scale: float = dataclasses.field(default=0.0)

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
        data.write(b'\x00\x1b')  # 27 properties

        data.write(b'\xa1:+\xf2')  # 0xa13a2bf2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.attach_to_line_locator_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\xed\xcf\x89')  # 0xf9edcf89
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.line_end_point_locator_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\x9c\x90t')  # 0x589c9074
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_line_additive_length))

        data.write(b'\x85c\xee*')  # 0x8563ee2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_line_dist_backwards))

        data.write(b'\x174\xf8\x91')  # 0x1734f891
        data.write(b'\x00\x04')  # size
        self.swing_line_type.to_stream(data)

        data.write(b'\xc0.\xfb\xe3')  # 0xc02efbe3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_line_max_angle))

        data.write(b'\xee\x89\n(')  # 0xee890a28
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.swing_line_length))

        data.write(b"\xbb\xe1'\x1e")  # 0xbbe1271e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.time_apex_to_apex))

        data.write(b'\xf6\x13\x10-')  # 0xf613102d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_position_time_scale))

        data.write(b'5\xbaR\xb1')  # 0x35ba52b1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.orient_creature_with_line))

        data.write(b'\xe3^\xd2\x18')  # 0xe35ed218
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jettison_line_scale_speed))

        data.write(b' 7\xe5\x11')  # 0x2037e511
        data.write(b'\x00\x04')  # size
        self.death_line_action.to_stream(data)

        data.write(b')d\n-')  # 0x29640a2d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_additive_scale))

        data.write(b'\x84h\xbe\xb1')  # 0x8468beb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_ramp_in_speed))

        data.write(b'U\xee;\xf9')  # 0x55ee3bf9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_ramp_out_speed))

        data.write(b'\xf8\xb1\xd1\x83')  # 0xf8b1d183
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_depart_apex_angle_to_ramp_in))

        data.write(b"\xe1'\xb1\x13")  # 0xe127b113
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.curve_line_approach_apex_angle_to_ramp_out))

        data.write(b'C\xcaFS')  # 0x43ca4653
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.curve_line_middle))

        data.write(b'\xb3|\x98\x90')  # 0xb37c9890
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dwell_dist_from_anchor))

        data.write(b'\xcd\xf7\xce\xb9')  # 0xcdf7ceb9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dwell_time))

        data.write(b'\xe9\x08L\x1f')  # 0xe9084c1f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_down_distance))

        data.write(b'\xa4zp7')  # 0xa47a7037
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_down_speed))

        data.write(b':\xa6A\x11')  # 0x3aa64111
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.drop_at_line_end))

        data.write(b'O\xa9\xf7\xc2')  # 0x4fa9f7c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.drop_to_ground_rule))

        data.write(b'\xf5\xbe\xe5\x8e')  # 0xf5bee58e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hang_around_time))

        data.write(b'\xe2v\x04\xbe')  # 0xe27604be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.climb_up_speed))

        data.write(b'\xaf\xe0\x0e\xf0')  # 0xafe00ef0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.end_of_line_jiggle_scale))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            attach_to_line_locator_name=data['attach_to_line_locator_name'],
            line_end_point_locator_name=data['line_end_point_locator_name'],
            swing_line_additive_length=data['swing_line_additive_length'],
            swing_line_dist_backwards=data['swing_line_dist_backwards'],
            swing_line_type=enums.SwingLineType.from_json(data['swing_line_type']),
            swing_line_max_angle=data['swing_line_max_angle'],
            swing_line_length=data['swing_line_length'],
            time_apex_to_apex=data['time_apex_to_apex'],
            start_position_time_scale=data['start_position_time_scale'],
            orient_creature_with_line=data['orient_creature_with_line'],
            jettison_line_scale_speed=data['jettison_line_scale_speed'],
            death_line_action=enums.DeathLineAction.from_json(data['death_line_action']),
            curve_line_additive_scale=data['curve_line_additive_scale'],
            curve_line_ramp_in_speed=data['curve_line_ramp_in_speed'],
            curve_line_ramp_out_speed=data['curve_line_ramp_out_speed'],
            curve_line_depart_apex_angle_to_ramp_in=data['curve_line_depart_apex_angle_to_ramp_in'],
            curve_line_approach_apex_angle_to_ramp_out=data['curve_line_approach_apex_angle_to_ramp_out'],
            curve_line_middle=data['curve_line_middle'],
            dwell_dist_from_anchor=data['dwell_dist_from_anchor'],
            dwell_time=data['dwell_time'],
            climb_down_distance=data['climb_down_distance'],
            climb_down_speed=data['climb_down_speed'],
            drop_at_line_end=data['drop_at_line_end'],
            drop_to_ground_rule=data['drop_to_ground_rule'],
            hang_around_time=data['hang_around_time'],
            climb_up_speed=data['climb_up_speed'],
            end_of_line_jiggle_scale=data['end_of_line_jiggle_scale'],
        )

    def to_json(self) -> dict:
        return {
            'attach_to_line_locator_name': self.attach_to_line_locator_name,
            'line_end_point_locator_name': self.line_end_point_locator_name,
            'swing_line_additive_length': self.swing_line_additive_length,
            'swing_line_dist_backwards': self.swing_line_dist_backwards,
            'swing_line_type': self.swing_line_type.to_json(),
            'swing_line_max_angle': self.swing_line_max_angle,
            'swing_line_length': self.swing_line_length,
            'time_apex_to_apex': self.time_apex_to_apex,
            'start_position_time_scale': self.start_position_time_scale,
            'orient_creature_with_line': self.orient_creature_with_line,
            'jettison_line_scale_speed': self.jettison_line_scale_speed,
            'death_line_action': self.death_line_action.to_json(),
            'curve_line_additive_scale': self.curve_line_additive_scale,
            'curve_line_ramp_in_speed': self.curve_line_ramp_in_speed,
            'curve_line_ramp_out_speed': self.curve_line_ramp_out_speed,
            'curve_line_depart_apex_angle_to_ramp_in': self.curve_line_depart_apex_angle_to_ramp_in,
            'curve_line_approach_apex_angle_to_ramp_out': self.curve_line_approach_apex_angle_to_ramp_out,
            'curve_line_middle': self.curve_line_middle,
            'dwell_dist_from_anchor': self.dwell_dist_from_anchor,
            'dwell_time': self.dwell_time,
            'climb_down_distance': self.climb_down_distance,
            'climb_down_speed': self.climb_down_speed,
            'drop_at_line_end': self.drop_at_line_end,
            'drop_to_ground_rule': self.drop_to_ground_rule,
            'hang_around_time': self.hang_around_time,
            'climb_up_speed': self.climb_up_speed,
            'end_of_line_jiggle_scale': self.end_of_line_jiggle_scale,
        }


def _decode_attach_to_line_locator_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_line_end_point_locator_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


def _decode_swing_line_additive_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_line_dist_backwards(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_line_type(data: typing.BinaryIO, property_size: int):
    return enums.SwingLineType.from_stream(data)


def _decode_swing_line_max_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_swing_line_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_time_apex_to_apex(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_position_time_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_orient_creature_with_line(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_jettison_line_scale_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_death_line_action(data: typing.BinaryIO, property_size: int):
    return enums.DeathLineAction.from_stream(data)


def _decode_curve_line_additive_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_ramp_in_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_ramp_out_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_depart_apex_angle_to_ramp_in(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_approach_apex_angle_to_ramp_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_curve_line_middle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_dwell_dist_from_anchor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dwell_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_down_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_down_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop_at_line_end(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_drop_to_ground_rule(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_hang_around_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_climb_up_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_end_of_line_jiggle_scale(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa13a2bf2: ('attach_to_line_locator_name', _decode_attach_to_line_locator_name),
    0xf9edcf89: ('line_end_point_locator_name', _decode_line_end_point_locator_name),
    0x589c9074: ('swing_line_additive_length', _decode_swing_line_additive_length),
    0x8563ee2a: ('swing_line_dist_backwards', _decode_swing_line_dist_backwards),
    0x1734f891: ('swing_line_type', _decode_swing_line_type),
    0xc02efbe3: ('swing_line_max_angle', _decode_swing_line_max_angle),
    0xee890a28: ('swing_line_length', _decode_swing_line_length),
    0xbbe1271e: ('time_apex_to_apex', _decode_time_apex_to_apex),
    0xf613102d: ('start_position_time_scale', _decode_start_position_time_scale),
    0x35ba52b1: ('orient_creature_with_line', _decode_orient_creature_with_line),
    0xe35ed218: ('jettison_line_scale_speed', _decode_jettison_line_scale_speed),
    0x2037e511: ('death_line_action', _decode_death_line_action),
    0x29640a2d: ('curve_line_additive_scale', _decode_curve_line_additive_scale),
    0x8468beb1: ('curve_line_ramp_in_speed', _decode_curve_line_ramp_in_speed),
    0x55ee3bf9: ('curve_line_ramp_out_speed', _decode_curve_line_ramp_out_speed),
    0xf8b1d183: ('curve_line_depart_apex_angle_to_ramp_in', _decode_curve_line_depart_apex_angle_to_ramp_in),
    0xe127b113: ('curve_line_approach_apex_angle_to_ramp_out', _decode_curve_line_approach_apex_angle_to_ramp_out),
    0x43ca4653: ('curve_line_middle', _decode_curve_line_middle),
    0xb37c9890: ('dwell_dist_from_anchor', _decode_dwell_dist_from_anchor),
    0xcdf7ceb9: ('dwell_time', _decode_dwell_time),
    0xe9084c1f: ('climb_down_distance', _decode_climb_down_distance),
    0xa47a7037: ('climb_down_speed', _decode_climb_down_speed),
    0x3aa64111: ('drop_at_line_end', _decode_drop_at_line_end),
    0x4fa9f7c2: ('drop_to_ground_rule', _decode_drop_to_ground_rule),
    0xf5bee58e: ('hang_around_time', _decode_hang_around_time),
    0xe27604be: ('climb_up_speed', _decode_climb_up_speed),
    0xafe00ef0: ('end_of_line_jiggle_scale', _decode_end_of_line_jiggle_scale),
}
