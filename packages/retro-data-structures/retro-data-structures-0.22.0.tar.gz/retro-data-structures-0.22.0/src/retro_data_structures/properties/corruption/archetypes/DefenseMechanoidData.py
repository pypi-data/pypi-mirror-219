# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.ShockWaveInfo import ShockWaveInfo


@dataclasses.dataclass()
class DefenseMechanoidData(BaseProperty):
    unknown_0xd41f1468: bool = dataclasses.field(default=True)
    unknown_0x77259804: bool = dataclasses.field(default=True)
    unknown_0xec877653: float = dataclasses.field(default=200.0)
    unknown_0x09555889: float = dataclasses.field(default=45.0)
    unknown_0x5ceca2a6: float = dataclasses.field(default=100.0)
    jammer_antenna_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    command_core_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0x6735f19b: float = dataclasses.field(default=25.0)
    unknown_0x0a9689e2: float = dataclasses.field(default=25.0)
    unknown_0xa65f4b32: float = dataclasses.field(default=25.0)
    unknown_0x78871ce9: float = dataclasses.field(default=25.0)
    min_jump_interval: float = dataclasses.field(default=15.0)
    max_jump_interval: float = dataclasses.field(default=25.0)
    min_missile_interval: float = dataclasses.field(default=1.5)
    max_missile_interval: float = dataclasses.field(default=3.0)
    min_taunt_interval: float = dataclasses.field(default=10.0)
    max_taunt_interval: float = dataclasses.field(default=20.0)
    min_distance_adjust_interval: float = dataclasses.field(default=7.0)
    max_distance_adjust_interval: float = dataclasses.field(default=12.0)
    unknown_0xbc801a3e: float = dataclasses.field(default=4.0)
    unknown_0xc060b62b: float = dataclasses.field(default=10.0)
    unknown_0x2766a717: float = dataclasses.field(default=50.0)
    unknown_0x29ea27db: float = dataclasses.field(default=10.0)
    missile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    huge_missile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    pulse_shockwave: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    seeker_bomb_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)

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
        data.write(b'\x00\x1b')  # 27 properties

        data.write(b'\xd4\x1f\x14h')  # 0xd41f1468
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xd41f1468))

        data.write(b'w%\x98\x04')  # 0x77259804
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x77259804))

        data.write(b'\xec\x87vS')  # 0xec877653
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xec877653))

        data.write(b'\tUX\x89')  # 0x9555889
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x09555889))

        data.write(b'\\\xec\xa2\xa6')  # 0x5ceca2a6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5ceca2a6))

        data.write(b'\xff\x8c@V')  # 0xff8c4056
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jammer_antenna_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x99\xbb\xc2\xde')  # 0x99bbc2de
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.command_core_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g5\xf1\x9b')  # 0x6735f19b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6735f19b))

        data.write(b'\n\x96\x89\xe2')  # 0xa9689e2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0a9689e2))

        data.write(b'\xa6_K2')  # 0xa65f4b32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa65f4b32))

        data.write(b'x\x87\x1c\xe9')  # 0x78871ce9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x78871ce9))

        data.write(b'\xcd\xf4\xd7U')  # 0xcdf4d755
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_jump_interval))

        data.write(b'\xe4\x8a*M')  # 0xe48a2a4d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_jump_interval))

        data.write(b'\xed"6\x86')  # 0xed223686
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_missile_interval))

        data.write(b'\xe9\xb8\x07\xac')  # 0xe9b807ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_missile_interval))

        data.write(b'3\xa2\x98\xcd')  # 0x33a298cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_taunt_interval))

        data.write(b' \xe7~f')  # 0x20e77e66
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_taunt_interval))

        data.write(b'\xaa\xfe>C')  # 0xaafe3e43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_distance_adjust_interval))

        data.write(b'\x1a\xc1$\x7f')  # 0x1ac1247f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_distance_adjust_interval))

        data.write(b'\xbc\x80\x1a>')  # 0xbc801a3e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbc801a3e))

        data.write(b'\xc0`\xb6+')  # 0xc060b62b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc060b62b))

        data.write(b"'f\xa7\x17")  # 0x2766a717
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2766a717))

        data.write(b")\xea'\xdb")  # 0x29ea27db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x29ea27db))

        data.write(b'%\x8c\xfbM')  # 0x258cfb4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.missile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\xd9\x9a\xbc')  # 0xf4d99abc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.huge_missile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1|;n')  # 0xe17c3b6e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pulse_shockwave.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'YU\tR')  # 0x59550952
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seeker_bomb_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xd41f1468=data['unknown_0xd41f1468'],
            unknown_0x77259804=data['unknown_0x77259804'],
            unknown_0xec877653=data['unknown_0xec877653'],
            unknown_0x09555889=data['unknown_0x09555889'],
            unknown_0x5ceca2a6=data['unknown_0x5ceca2a6'],
            jammer_antenna_vulnerability=DamageVulnerability.from_json(data['jammer_antenna_vulnerability']),
            command_core_vulnerability=DamageVulnerability.from_json(data['command_core_vulnerability']),
            unknown_0x6735f19b=data['unknown_0x6735f19b'],
            unknown_0x0a9689e2=data['unknown_0x0a9689e2'],
            unknown_0xa65f4b32=data['unknown_0xa65f4b32'],
            unknown_0x78871ce9=data['unknown_0x78871ce9'],
            min_jump_interval=data['min_jump_interval'],
            max_jump_interval=data['max_jump_interval'],
            min_missile_interval=data['min_missile_interval'],
            max_missile_interval=data['max_missile_interval'],
            min_taunt_interval=data['min_taunt_interval'],
            max_taunt_interval=data['max_taunt_interval'],
            min_distance_adjust_interval=data['min_distance_adjust_interval'],
            max_distance_adjust_interval=data['max_distance_adjust_interval'],
            unknown_0xbc801a3e=data['unknown_0xbc801a3e'],
            unknown_0xc060b62b=data['unknown_0xc060b62b'],
            unknown_0x2766a717=data['unknown_0x2766a717'],
            unknown_0x29ea27db=data['unknown_0x29ea27db'],
            missile_damage=DamageInfo.from_json(data['missile_damage']),
            huge_missile_damage=DamageInfo.from_json(data['huge_missile_damage']),
            pulse_shockwave=ShockWaveInfo.from_json(data['pulse_shockwave']),
            seeker_bomb_damage=DamageInfo.from_json(data['seeker_bomb_damage']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xd41f1468': self.unknown_0xd41f1468,
            'unknown_0x77259804': self.unknown_0x77259804,
            'unknown_0xec877653': self.unknown_0xec877653,
            'unknown_0x09555889': self.unknown_0x09555889,
            'unknown_0x5ceca2a6': self.unknown_0x5ceca2a6,
            'jammer_antenna_vulnerability': self.jammer_antenna_vulnerability.to_json(),
            'command_core_vulnerability': self.command_core_vulnerability.to_json(),
            'unknown_0x6735f19b': self.unknown_0x6735f19b,
            'unknown_0x0a9689e2': self.unknown_0x0a9689e2,
            'unknown_0xa65f4b32': self.unknown_0xa65f4b32,
            'unknown_0x78871ce9': self.unknown_0x78871ce9,
            'min_jump_interval': self.min_jump_interval,
            'max_jump_interval': self.max_jump_interval,
            'min_missile_interval': self.min_missile_interval,
            'max_missile_interval': self.max_missile_interval,
            'min_taunt_interval': self.min_taunt_interval,
            'max_taunt_interval': self.max_taunt_interval,
            'min_distance_adjust_interval': self.min_distance_adjust_interval,
            'max_distance_adjust_interval': self.max_distance_adjust_interval,
            'unknown_0xbc801a3e': self.unknown_0xbc801a3e,
            'unknown_0xc060b62b': self.unknown_0xc060b62b,
            'unknown_0x2766a717': self.unknown_0x2766a717,
            'unknown_0x29ea27db': self.unknown_0x29ea27db,
            'missile_damage': self.missile_damage.to_json(),
            'huge_missile_damage': self.huge_missile_damage.to_json(),
            'pulse_shockwave': self.pulse_shockwave.to_json(),
            'seeker_bomb_damage': self.seeker_bomb_damage.to_json(),
        }


def _decode_unknown_0xd41f1468(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x77259804(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xec877653(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x09555889(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5ceca2a6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jammer_antenna_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_command_core_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0x6735f19b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0a9689e2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa65f4b32(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x78871ce9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_jump_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_jump_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_missile_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_missile_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_taunt_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_taunt_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_distance_adjust_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_distance_adjust_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbc801a3e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc060b62b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2766a717(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x29ea27db(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_huge_missile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_pulse_shockwave(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_seeker_bomb_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd41f1468: ('unknown_0xd41f1468', _decode_unknown_0xd41f1468),
    0x77259804: ('unknown_0x77259804', _decode_unknown_0x77259804),
    0xec877653: ('unknown_0xec877653', _decode_unknown_0xec877653),
    0x9555889: ('unknown_0x09555889', _decode_unknown_0x09555889),
    0x5ceca2a6: ('unknown_0x5ceca2a6', _decode_unknown_0x5ceca2a6),
    0xff8c4056: ('jammer_antenna_vulnerability', _decode_jammer_antenna_vulnerability),
    0x99bbc2de: ('command_core_vulnerability', _decode_command_core_vulnerability),
    0x6735f19b: ('unknown_0x6735f19b', _decode_unknown_0x6735f19b),
    0xa9689e2: ('unknown_0x0a9689e2', _decode_unknown_0x0a9689e2),
    0xa65f4b32: ('unknown_0xa65f4b32', _decode_unknown_0xa65f4b32),
    0x78871ce9: ('unknown_0x78871ce9', _decode_unknown_0x78871ce9),
    0xcdf4d755: ('min_jump_interval', _decode_min_jump_interval),
    0xe48a2a4d: ('max_jump_interval', _decode_max_jump_interval),
    0xed223686: ('min_missile_interval', _decode_min_missile_interval),
    0xe9b807ac: ('max_missile_interval', _decode_max_missile_interval),
    0x33a298cd: ('min_taunt_interval', _decode_min_taunt_interval),
    0x20e77e66: ('max_taunt_interval', _decode_max_taunt_interval),
    0xaafe3e43: ('min_distance_adjust_interval', _decode_min_distance_adjust_interval),
    0x1ac1247f: ('max_distance_adjust_interval', _decode_max_distance_adjust_interval),
    0xbc801a3e: ('unknown_0xbc801a3e', _decode_unknown_0xbc801a3e),
    0xc060b62b: ('unknown_0xc060b62b', _decode_unknown_0xc060b62b),
    0x2766a717: ('unknown_0x2766a717', _decode_unknown_0x2766a717),
    0x29ea27db: ('unknown_0x29ea27db', _decode_unknown_0x29ea27db),
    0x258cfb4d: ('missile_damage', _decode_missile_damage),
    0xf4d99abc: ('huge_missile_damage', _decode_huge_missile_damage),
    0xe17c3b6e: ('pulse_shockwave', _decode_pulse_shockwave),
    0x59550952: ('seeker_bomb_damage', _decode_seeker_bomb_damage),
}
