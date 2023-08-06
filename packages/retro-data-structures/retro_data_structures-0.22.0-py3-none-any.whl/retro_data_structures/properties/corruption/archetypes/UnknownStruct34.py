# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability


@dataclasses.dataclass()
class UnknownStruct34(BaseProperty):
    speed_increase: float = dataclasses.field(default=1.2000000476837158)
    hyper_mode_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    min_hyper_mode_time: float = dataclasses.field(default=20.0)
    max_hyper_mode_time: float = dataclasses.field(default=25.0)
    min_cloaked_time: float = dataclasses.field(default=10.0)
    max_cloaked_time: float = dataclasses.field(default=15.0)
    unknown_0x587fa387: float = dataclasses.field(default=3.0)
    unknown_0x3e9ac5f3: float = dataclasses.field(default=4.0)
    melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    radial_melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    energy_wave_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)

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
        data.write(b'\x00\x0b')  # 11 properties

        data.write(b'eR\xbc\xc0')  # 0x6552bcc0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed_increase))

        data.write(b'\xc8\xa1\xea\xc8')  # 0xc8a1eac8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_mode_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xe3ZB')  # 0xede35a42
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_hyper_mode_time))

        data.write(b'\xfe\xa6\xbc\xe9')  # 0xfea6bce9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_hyper_mode_time))

        data.write(b'\x86\x06Dq')  # 0x86064471
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_cloaked_time))

        data.write(b'!2\xc4\x08')  # 0x2132c408
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_cloaked_time))

        data.write(b'X\x7f\xa3\x87')  # 0x587fa387
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x587fa387))

        data.write(b'>\x9a\xc5\xf3')  # 0x3e9ac5f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3e9ac5f3))

        data.write(b'\xc9A`4')  # 0xc9416034
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'_\x11\x89;')  # 0x5f11893b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.radial_melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7\xedn\xbb')  # 0x37ed6ebb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energy_wave_projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            speed_increase=data['speed_increase'],
            hyper_mode_vulnerability=DamageVulnerability.from_json(data['hyper_mode_vulnerability']),
            min_hyper_mode_time=data['min_hyper_mode_time'],
            max_hyper_mode_time=data['max_hyper_mode_time'],
            min_cloaked_time=data['min_cloaked_time'],
            max_cloaked_time=data['max_cloaked_time'],
            unknown_0x587fa387=data['unknown_0x587fa387'],
            unknown_0x3e9ac5f3=data['unknown_0x3e9ac5f3'],
            melee_damage=DamageInfo.from_json(data['melee_damage']),
            radial_melee_damage=DamageInfo.from_json(data['radial_melee_damage']),
            energy_wave_projectile_damage=DamageInfo.from_json(data['energy_wave_projectile_damage']),
        )

    def to_json(self) -> dict:
        return {
            'speed_increase': self.speed_increase,
            'hyper_mode_vulnerability': self.hyper_mode_vulnerability.to_json(),
            'min_hyper_mode_time': self.min_hyper_mode_time,
            'max_hyper_mode_time': self.max_hyper_mode_time,
            'min_cloaked_time': self.min_cloaked_time,
            'max_cloaked_time': self.max_cloaked_time,
            'unknown_0x587fa387': self.unknown_0x587fa387,
            'unknown_0x3e9ac5f3': self.unknown_0x3e9ac5f3,
            'melee_damage': self.melee_damage.to_json(),
            'radial_melee_damage': self.radial_melee_damage.to_json(),
            'energy_wave_projectile_damage': self.energy_wave_projectile_damage.to_json(),
        }


def _decode_speed_increase(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_min_hyper_mode_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_hyper_mode_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_cloaked_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_cloaked_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x587fa387(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3e9ac5f3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_radial_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_energy_wave_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x6552bcc0: ('speed_increase', _decode_speed_increase),
    0xc8a1eac8: ('hyper_mode_vulnerability', _decode_hyper_mode_vulnerability),
    0xede35a42: ('min_hyper_mode_time', _decode_min_hyper_mode_time),
    0xfea6bce9: ('max_hyper_mode_time', _decode_max_hyper_mode_time),
    0x86064471: ('min_cloaked_time', _decode_min_cloaked_time),
    0x2132c408: ('max_cloaked_time', _decode_max_cloaked_time),
    0x587fa387: ('unknown_0x587fa387', _decode_unknown_0x587fa387),
    0x3e9ac5f3: ('unknown_0x3e9ac5f3', _decode_unknown_0x3e9ac5f3),
    0xc9416034: ('melee_damage', _decode_melee_damage),
    0x5f11893b: ('radial_melee_damage', _decode_radial_melee_damage),
    0x37ed6ebb: ('energy_wave_projectile_damage', _decode_energy_wave_projectile_damage),
}
