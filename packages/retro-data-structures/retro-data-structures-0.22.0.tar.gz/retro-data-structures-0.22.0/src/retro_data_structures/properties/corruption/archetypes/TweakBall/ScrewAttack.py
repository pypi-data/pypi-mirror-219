# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.TDamageInfo import TDamageInfo


@dataclasses.dataclass()
class ScrewAttack(BaseProperty):
    screw_attack_gravity: float = dataclasses.field(default=40.0)
    unknown_0xcb77fb28: float = dataclasses.field(default=4.5)
    unknown_0x3fdeb046: float = dataclasses.field(default=4.5)
    unknown_0x691b244d: int = dataclasses.field(default=5)
    screw_attack_vertical_jump_velocity: float = dataclasses.field(default=20.0)
    screw_attack_horizontal_jump_velocity: float = dataclasses.field(default=20.0)
    unknown_0x3d03d8a6: float = dataclasses.field(default=10.0)
    unknown_0xf1f2498f: float = dataclasses.field(default=0.75)
    unknown_0x4b0aba1c: float = dataclasses.field(default=0.75)
    screw_attack_wall_jump_max_time: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x315df4d7: float = dataclasses.field(default=30.0)
    screw_attack_wall_jump_vertical_velocity: float = dataclasses.field(default=20.0)
    unknown_0xc5b758f5: float = dataclasses.field(default=30.0)
    screw_attack_wall_jump_horizontal_velocity: float = dataclasses.field(default=20.0)
    screw_attack_wall_jump_gravity: float = dataclasses.field(default=40.0)
    screw_attack_damage: TDamageInfo = dataclasses.field(default_factory=TDamageInfo)

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
        data.write(b'\x00\x10')  # 16 properties

        data.write(b'~\xabK\xab')  # 0x7eab4bab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screw_attack_gravity))

        data.write(b'\xcbw\xfb(')  # 0xcb77fb28
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcb77fb28))

        data.write(b'?\xde\xb0F')  # 0x3fdeb046
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3fdeb046))

        data.write(b'i\x1b$M')  # 0x691b244d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x691b244d))

        data.write(b'Y\x1d\xa5\xb4')  # 0x591da5b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screw_attack_vertical_jump_velocity))

        data.write(b'\xe4(\xf21')  # 0xe428f231
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screw_attack_horizontal_jump_velocity))

        data.write(b'=\x03\xd8\xa6')  # 0x3d03d8a6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3d03d8a6))

        data.write(b'\xf1\xf2I\x8f')  # 0xf1f2498f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf1f2498f))

        data.write(b'K\n\xba\x1c')  # 0x4b0aba1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4b0aba1c))

        data.write(b'\x145\x11@')  # 0x14351140
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screw_attack_wall_jump_max_time))

        data.write(b'1]\xf4\xd7')  # 0x315df4d7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x315df4d7))

        data.write(b']\xec3\xc5')  # 0x5dec33c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screw_attack_wall_jump_vertical_velocity))

        data.write(b'\xc5\xb7X\xf5')  # 0xc5b758f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc5b758f5))

        data.write(b'\xb8C\x13\x84')  # 0xb8431384
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screw_attack_wall_jump_horizontal_velocity))

        data.write(b'8\xf8@\x11')  # 0x38f84011
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.screw_attack_wall_jump_gravity))

        data.write(b'\xb3r\xec\xab')  # 0xb372ecab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.screw_attack_damage.to_stream(data, default_override={'weapon_type': 7, 'damage_amount': 50.0, 'radius_damage_amount': 50.0, 'damage_radius': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            screw_attack_gravity=data['screw_attack_gravity'],
            unknown_0xcb77fb28=data['unknown_0xcb77fb28'],
            unknown_0x3fdeb046=data['unknown_0x3fdeb046'],
            unknown_0x691b244d=data['unknown_0x691b244d'],
            screw_attack_vertical_jump_velocity=data['screw_attack_vertical_jump_velocity'],
            screw_attack_horizontal_jump_velocity=data['screw_attack_horizontal_jump_velocity'],
            unknown_0x3d03d8a6=data['unknown_0x3d03d8a6'],
            unknown_0xf1f2498f=data['unknown_0xf1f2498f'],
            unknown_0x4b0aba1c=data['unknown_0x4b0aba1c'],
            screw_attack_wall_jump_max_time=data['screw_attack_wall_jump_max_time'],
            unknown_0x315df4d7=data['unknown_0x315df4d7'],
            screw_attack_wall_jump_vertical_velocity=data['screw_attack_wall_jump_vertical_velocity'],
            unknown_0xc5b758f5=data['unknown_0xc5b758f5'],
            screw_attack_wall_jump_horizontal_velocity=data['screw_attack_wall_jump_horizontal_velocity'],
            screw_attack_wall_jump_gravity=data['screw_attack_wall_jump_gravity'],
            screw_attack_damage=TDamageInfo.from_json(data['screw_attack_damage']),
        )

    def to_json(self) -> dict:
        return {
            'screw_attack_gravity': self.screw_attack_gravity,
            'unknown_0xcb77fb28': self.unknown_0xcb77fb28,
            'unknown_0x3fdeb046': self.unknown_0x3fdeb046,
            'unknown_0x691b244d': self.unknown_0x691b244d,
            'screw_attack_vertical_jump_velocity': self.screw_attack_vertical_jump_velocity,
            'screw_attack_horizontal_jump_velocity': self.screw_attack_horizontal_jump_velocity,
            'unknown_0x3d03d8a6': self.unknown_0x3d03d8a6,
            'unknown_0xf1f2498f': self.unknown_0xf1f2498f,
            'unknown_0x4b0aba1c': self.unknown_0x4b0aba1c,
            'screw_attack_wall_jump_max_time': self.screw_attack_wall_jump_max_time,
            'unknown_0x315df4d7': self.unknown_0x315df4d7,
            'screw_attack_wall_jump_vertical_velocity': self.screw_attack_wall_jump_vertical_velocity,
            'unknown_0xc5b758f5': self.unknown_0xc5b758f5,
            'screw_attack_wall_jump_horizontal_velocity': self.screw_attack_wall_jump_horizontal_velocity,
            'screw_attack_wall_jump_gravity': self.screw_attack_wall_jump_gravity,
            'screw_attack_damage': self.screw_attack_damage.to_json(),
        }


def _decode_screw_attack_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcb77fb28(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3fdeb046(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x691b244d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_screw_attack_vertical_jump_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screw_attack_horizontal_jump_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3d03d8a6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf1f2498f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4b0aba1c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screw_attack_wall_jump_max_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x315df4d7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screw_attack_wall_jump_vertical_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc5b758f5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screw_attack_wall_jump_horizontal_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screw_attack_wall_jump_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_screw_attack_damage(data: typing.BinaryIO, property_size: int):
    return TDamageInfo.from_stream(data, property_size, default_override={'weapon_type': 7, 'damage_amount': 50.0, 'radius_damage_amount': 50.0, 'damage_radius': 2.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7eab4bab: ('screw_attack_gravity', _decode_screw_attack_gravity),
    0xcb77fb28: ('unknown_0xcb77fb28', _decode_unknown_0xcb77fb28),
    0x3fdeb046: ('unknown_0x3fdeb046', _decode_unknown_0x3fdeb046),
    0x691b244d: ('unknown_0x691b244d', _decode_unknown_0x691b244d),
    0x591da5b4: ('screw_attack_vertical_jump_velocity', _decode_screw_attack_vertical_jump_velocity),
    0xe428f231: ('screw_attack_horizontal_jump_velocity', _decode_screw_attack_horizontal_jump_velocity),
    0x3d03d8a6: ('unknown_0x3d03d8a6', _decode_unknown_0x3d03d8a6),
    0xf1f2498f: ('unknown_0xf1f2498f', _decode_unknown_0xf1f2498f),
    0x4b0aba1c: ('unknown_0x4b0aba1c', _decode_unknown_0x4b0aba1c),
    0x14351140: ('screw_attack_wall_jump_max_time', _decode_screw_attack_wall_jump_max_time),
    0x315df4d7: ('unknown_0x315df4d7', _decode_unknown_0x315df4d7),
    0x5dec33c5: ('screw_attack_wall_jump_vertical_velocity', _decode_screw_attack_wall_jump_vertical_velocity),
    0xc5b758f5: ('unknown_0xc5b758f5', _decode_unknown_0xc5b758f5),
    0xb8431384: ('screw_attack_wall_jump_horizontal_velocity', _decode_screw_attack_wall_jump_horizontal_velocity),
    0x38f84011: ('screw_attack_wall_jump_gravity', _decode_screw_attack_wall_jump_gravity),
    0xb372ecab: ('screw_attack_damage', _decode_screw_attack_damage),
}
