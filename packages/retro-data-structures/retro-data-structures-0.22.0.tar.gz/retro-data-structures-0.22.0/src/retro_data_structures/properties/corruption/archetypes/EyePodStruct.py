# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData


@dataclasses.dataclass()
class EyePodStruct(BaseProperty):
    hyper_mode_check_chance: float = dataclasses.field(default=100.0)
    unknown_0xc8e312dd: float = dataclasses.field(default=10.0)
    unknown_0x2e83bd3c: float = dataclasses.field(default=15.0)
    unknown_0xf06a131d: float = dataclasses.field(default=20.0)
    unknown_0x160abcfc: float = dataclasses.field(default=30.0)
    hyper_mode_duration_min: float = dataclasses.field(default=20.0)
    hyper_mode_duration_max: float = dataclasses.field(default=30.0)
    hyper_mode_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0x95e7a2c2: float = dataclasses.field(default=3.0)
    unknown_0x76ba1c18: float = dataclasses.field(default=6.0)
    unknown_0x64d482d5: int = dataclasses.field(default=4)
    unknown_0xc3e002ac: int = dataclasses.field(default=7)
    unknown_0x77b6541c: float = dataclasses.field(default=0.20000000298023224)
    unknown_0x9c889645: float = dataclasses.field(default=5.0)
    launch_projectile_data: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)

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
        data.write(b'\x00\x0f')  # 15 properties

        data.write(b'\xf0DR\xf3')  # 0xf04452f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_mode_check_chance))

        data.write(b'\xc8\xe3\x12\xdd')  # 0xc8e312dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc8e312dd))

        data.write(b'.\x83\xbd<')  # 0x2e83bd3c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2e83bd3c))

        data.write(b'\xf0j\x13\x1d')  # 0xf06a131d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf06a131d))

        data.write(b'\x16\n\xbc\xfc')  # 0x160abcfc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x160abcfc))

        data.write(b'Hf\xdfl')  # 0x4866df6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_mode_duration_min))

        data.write(b'\xae\x06p\x8d')  # 0xae06708d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hyper_mode_duration_max))

        data.write(b'\xc8\xa1\xea\xc8')  # 0xc8a1eac8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hyper_mode_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\xe7\xa2\xc2')  # 0x95e7a2c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95e7a2c2))

        data.write(b'v\xba\x1c\x18')  # 0x76ba1c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76ba1c18))

        data.write(b'd\xd4\x82\xd5')  # 0x64d482d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x64d482d5))

        data.write(b'\xc3\xe0\x02\xac')  # 0xc3e002ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc3e002ac))

        data.write(b'w\xb6T\x1c')  # 0x77b6541c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x77b6541c))

        data.write(b'\x9c\x88\x96E')  # 0x9c889645
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9c889645))

        data.write(b'\x11G<\x13')  # 0x11473c13
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hyper_mode_check_chance=data['hyper_mode_check_chance'],
            unknown_0xc8e312dd=data['unknown_0xc8e312dd'],
            unknown_0x2e83bd3c=data['unknown_0x2e83bd3c'],
            unknown_0xf06a131d=data['unknown_0xf06a131d'],
            unknown_0x160abcfc=data['unknown_0x160abcfc'],
            hyper_mode_duration_min=data['hyper_mode_duration_min'],
            hyper_mode_duration_max=data['hyper_mode_duration_max'],
            hyper_mode_vulnerability=DamageVulnerability.from_json(data['hyper_mode_vulnerability']),
            unknown_0x95e7a2c2=data['unknown_0x95e7a2c2'],
            unknown_0x76ba1c18=data['unknown_0x76ba1c18'],
            unknown_0x64d482d5=data['unknown_0x64d482d5'],
            unknown_0xc3e002ac=data['unknown_0xc3e002ac'],
            unknown_0x77b6541c=data['unknown_0x77b6541c'],
            unknown_0x9c889645=data['unknown_0x9c889645'],
            launch_projectile_data=LaunchProjectileData.from_json(data['launch_projectile_data']),
        )

    def to_json(self) -> dict:
        return {
            'hyper_mode_check_chance': self.hyper_mode_check_chance,
            'unknown_0xc8e312dd': self.unknown_0xc8e312dd,
            'unknown_0x2e83bd3c': self.unknown_0x2e83bd3c,
            'unknown_0xf06a131d': self.unknown_0xf06a131d,
            'unknown_0x160abcfc': self.unknown_0x160abcfc,
            'hyper_mode_duration_min': self.hyper_mode_duration_min,
            'hyper_mode_duration_max': self.hyper_mode_duration_max,
            'hyper_mode_vulnerability': self.hyper_mode_vulnerability.to_json(),
            'unknown_0x95e7a2c2': self.unknown_0x95e7a2c2,
            'unknown_0x76ba1c18': self.unknown_0x76ba1c18,
            'unknown_0x64d482d5': self.unknown_0x64d482d5,
            'unknown_0xc3e002ac': self.unknown_0xc3e002ac,
            'unknown_0x77b6541c': self.unknown_0x77b6541c,
            'unknown_0x9c889645': self.unknown_0x9c889645,
            'launch_projectile_data': self.launch_projectile_data.to_json(),
        }


def _decode_hyper_mode_check_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc8e312dd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2e83bd3c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf06a131d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x160abcfc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_duration_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_duration_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hyper_mode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0x95e7a2c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ba1c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x64d482d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc3e002ac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x77b6541c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9c889645(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_projectile_data(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf04452f3: ('hyper_mode_check_chance', _decode_hyper_mode_check_chance),
    0xc8e312dd: ('unknown_0xc8e312dd', _decode_unknown_0xc8e312dd),
    0x2e83bd3c: ('unknown_0x2e83bd3c', _decode_unknown_0x2e83bd3c),
    0xf06a131d: ('unknown_0xf06a131d', _decode_unknown_0xf06a131d),
    0x160abcfc: ('unknown_0x160abcfc', _decode_unknown_0x160abcfc),
    0x4866df6c: ('hyper_mode_duration_min', _decode_hyper_mode_duration_min),
    0xae06708d: ('hyper_mode_duration_max', _decode_hyper_mode_duration_max),
    0xc8a1eac8: ('hyper_mode_vulnerability', _decode_hyper_mode_vulnerability),
    0x95e7a2c2: ('unknown_0x95e7a2c2', _decode_unknown_0x95e7a2c2),
    0x76ba1c18: ('unknown_0x76ba1c18', _decode_unknown_0x76ba1c18),
    0x64d482d5: ('unknown_0x64d482d5', _decode_unknown_0x64d482d5),
    0xc3e002ac: ('unknown_0xc3e002ac', _decode_unknown_0xc3e002ac),
    0x77b6541c: ('unknown_0x77b6541c', _decode_unknown_0x77b6541c),
    0x9c889645: ('unknown_0x9c889645', _decode_unknown_0x9c889645),
    0x11473c13: ('launch_projectile_data', _decode_launch_projectile_data),
}
