# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.TweakPlayer.GrappleBeam import GrappleBeam


@dataclasses.dataclass()
class Grapple(BaseProperty):
    grapple_distance: float = dataclasses.field(default=25.0)
    grapple_beam_length: float = dataclasses.field(default=10.0)
    grapple_swing_time: float = dataclasses.field(default=3.299999952316284)
    grapple_max_velocity: float = dataclasses.field(default=23.0)
    grapple_camera_speed: float = dataclasses.field(default=90.0)
    grapple_pull_close_distance: float = dataclasses.field(default=0.5)
    grapple_pull_dampen_distance: float = dataclasses.field(default=2.0)
    grapple_pull_velocity: float = dataclasses.field(default=30.0)
    grapple_pull_camera_speed: float = dataclasses.field(default=90.0)
    grapple_turn_rate: float = dataclasses.field(default=35.0)
    grapple_jump_force: float = dataclasses.field(default=13.0)
    grapple_release_time: float = dataclasses.field(default=1.0)
    grapple_control_scheme: int = dataclasses.field(default=2)
    grapple_hold_orbit_button: bool = dataclasses.field(default=True)
    grapple_turn_controls_reversed: bool = dataclasses.field(default=True)
    beam: GrappleBeam = dataclasses.field(default_factory=GrappleBeam)
    unknown_0x755f0513: float = dataclasses.field(default=10.0)
    unknown_0x15cf139d: float = dataclasses.field(default=10.0)
    unknown_0x2d255c98: float = dataclasses.field(default=10.0)
    unknown_0x4db54a16: float = dataclasses.field(default=10.0)

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
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'\xa7&1k')  # 0xa726316b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_distance))

        data.write(b'3\xe7\x9bQ')  # 0x33e79b51
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_beam_length))

        data.write(b'\x9d\xd3\xe8\x8b')  # 0x9dd3e88b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_swing_time))

        data.write(b'\xfb`[\xa4')  # 0xfb605ba4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_max_velocity))

        data.write(b'\xfe\x98\xb8\xe9')  # 0xfe98b8e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_camera_speed))

        data.write(b'\x92\x10\xa2^')  # 0x9210a25e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_close_distance))

        data.write(b'\xbe\x0c\x8b^')  # 0xbe0c8b5e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_dampen_distance))

        data.write(b'&\x03\xa0\xbe')  # 0x2603a0be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_velocity))

        data.write(b'[\x98\xa3\xbd')  # 0x5b98a3bd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_pull_camera_speed))

        data.write(b'\x87\xd4\xb5\xd6')  # 0x87d4b5d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_turn_rate))

        data.write(b'\xb7\xf8*\x9f')  # 0xb7f82a9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_jump_force))

        data.write(b'9Tx\xa8')  # 0x395478a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grapple_release_time))

        data.write(b'\x93\xc0\x13\xc9')  # 0x93c013c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grapple_control_scheme))

        data.write(b'\x8e\xee\xd66')  # 0x8eeed636
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grapple_hold_orbit_button))

        data.write(b'\xe1\xeb\x12\xe2')  # 0xe1eb12e2
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.grapple_turn_controls_reversed))

        data.write(b'\xae\x1f\xc4|')  # 0xae1fc47c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'u_\x05\x13')  # 0x755f0513
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x755f0513))

        data.write(b'\x15\xcf\x13\x9d')  # 0x15cf139d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x15cf139d))

        data.write(b'-%\\\x98')  # 0x2d255c98
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2d255c98))

        data.write(b'M\xb5J\x16')  # 0x4db54a16
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4db54a16))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            grapple_distance=data['grapple_distance'],
            grapple_beam_length=data['grapple_beam_length'],
            grapple_swing_time=data['grapple_swing_time'],
            grapple_max_velocity=data['grapple_max_velocity'],
            grapple_camera_speed=data['grapple_camera_speed'],
            grapple_pull_close_distance=data['grapple_pull_close_distance'],
            grapple_pull_dampen_distance=data['grapple_pull_dampen_distance'],
            grapple_pull_velocity=data['grapple_pull_velocity'],
            grapple_pull_camera_speed=data['grapple_pull_camera_speed'],
            grapple_turn_rate=data['grapple_turn_rate'],
            grapple_jump_force=data['grapple_jump_force'],
            grapple_release_time=data['grapple_release_time'],
            grapple_control_scheme=data['grapple_control_scheme'],
            grapple_hold_orbit_button=data['grapple_hold_orbit_button'],
            grapple_turn_controls_reversed=data['grapple_turn_controls_reversed'],
            beam=GrappleBeam.from_json(data['beam']),
            unknown_0x755f0513=data['unknown_0x755f0513'],
            unknown_0x15cf139d=data['unknown_0x15cf139d'],
            unknown_0x2d255c98=data['unknown_0x2d255c98'],
            unknown_0x4db54a16=data['unknown_0x4db54a16'],
        )

    def to_json(self) -> dict:
        return {
            'grapple_distance': self.grapple_distance,
            'grapple_beam_length': self.grapple_beam_length,
            'grapple_swing_time': self.grapple_swing_time,
            'grapple_max_velocity': self.grapple_max_velocity,
            'grapple_camera_speed': self.grapple_camera_speed,
            'grapple_pull_close_distance': self.grapple_pull_close_distance,
            'grapple_pull_dampen_distance': self.grapple_pull_dampen_distance,
            'grapple_pull_velocity': self.grapple_pull_velocity,
            'grapple_pull_camera_speed': self.grapple_pull_camera_speed,
            'grapple_turn_rate': self.grapple_turn_rate,
            'grapple_jump_force': self.grapple_jump_force,
            'grapple_release_time': self.grapple_release_time,
            'grapple_control_scheme': self.grapple_control_scheme,
            'grapple_hold_orbit_button': self.grapple_hold_orbit_button,
            'grapple_turn_controls_reversed': self.grapple_turn_controls_reversed,
            'beam': self.beam.to_json(),
            'unknown_0x755f0513': self.unknown_0x755f0513,
            'unknown_0x15cf139d': self.unknown_0x15cf139d,
            'unknown_0x2d255c98': self.unknown_0x2d255c98,
            'unknown_0x4db54a16': self.unknown_0x4db54a16,
        }


def _decode_grapple_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_beam_length(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_swing_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_max_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_camera_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_pull_close_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_pull_dampen_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_pull_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_pull_camera_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_turn_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_jump_force(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_release_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_control_scheme(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grapple_hold_orbit_button(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_grapple_turn_controls_reversed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_beam(data: typing.BinaryIO, property_size: int):
    return GrappleBeam.from_stream(data, property_size)


def _decode_unknown_0x755f0513(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x15cf139d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2d255c98(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4db54a16(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa726316b: ('grapple_distance', _decode_grapple_distance),
    0x33e79b51: ('grapple_beam_length', _decode_grapple_beam_length),
    0x9dd3e88b: ('grapple_swing_time', _decode_grapple_swing_time),
    0xfb605ba4: ('grapple_max_velocity', _decode_grapple_max_velocity),
    0xfe98b8e9: ('grapple_camera_speed', _decode_grapple_camera_speed),
    0x9210a25e: ('grapple_pull_close_distance', _decode_grapple_pull_close_distance),
    0xbe0c8b5e: ('grapple_pull_dampen_distance', _decode_grapple_pull_dampen_distance),
    0x2603a0be: ('grapple_pull_velocity', _decode_grapple_pull_velocity),
    0x5b98a3bd: ('grapple_pull_camera_speed', _decode_grapple_pull_camera_speed),
    0x87d4b5d6: ('grapple_turn_rate', _decode_grapple_turn_rate),
    0xb7f82a9f: ('grapple_jump_force', _decode_grapple_jump_force),
    0x395478a8: ('grapple_release_time', _decode_grapple_release_time),
    0x93c013c9: ('grapple_control_scheme', _decode_grapple_control_scheme),
    0x8eeed636: ('grapple_hold_orbit_button', _decode_grapple_hold_orbit_button),
    0xe1eb12e2: ('grapple_turn_controls_reversed', _decode_grapple_turn_controls_reversed),
    0xae1fc47c: ('beam', _decode_beam),
    0x755f0513: ('unknown_0x755f0513', _decode_unknown_0x755f0513),
    0x15cf139d: ('unknown_0x15cf139d', _decode_unknown_0x15cf139d),
    0x2d255c98: ('unknown_0x2d255c98', _decode_unknown_0x2d255c98),
    0x4db54a16: ('unknown_0x4db54a16', _decode_unknown_0x4db54a16),
}
