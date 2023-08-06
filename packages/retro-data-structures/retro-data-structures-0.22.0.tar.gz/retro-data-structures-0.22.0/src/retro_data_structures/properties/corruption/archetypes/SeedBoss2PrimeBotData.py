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
class SeedBoss2PrimeBotData(BaseProperty):
    unknown_0x313d0133: float = dataclasses.field(default=150.0)
    unknown_0xecb65675: float = dataclasses.field(default=500.0)
    unknown_0x80a300a5: float = dataclasses.field(default=2.5)
    unknown_0x8fe03c41: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x4bc36eee: float = dataclasses.field(default=160.0)
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    giant_electric_ball_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ring_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ring_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    ring_health: float = dataclasses.field(default=0.0)
    wheel_energy_beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x3e1b90ff: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    giant_contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sphere_contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x8461ab52: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x2872762b: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'1=\x013')  # 0x313d0133
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x313d0133))

        data.write(b'\xec\xb6Vu')  # 0xecb65675
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xecb65675))

        data.write(b'\x80\xa3\x00\xa5')  # 0x80a300a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x80a300a5))

        data.write(b'\x8f\xe0<A')  # 0x8fe03c41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8fe03c41))

        data.write(b'K\xc3n\xee')  # 0x4bc36eee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4bc36eee))

        data.write(b'\xa4\x0fe\xc2')  # 0xa40f65c2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'vQ\xec\x00')  # 0x7651ec00
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.giant_electric_ball_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x18\xf9\x18\x80')  # 0x18f91880
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ring_projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95b\xe5"')  # 0x9562e522
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ring_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe0yM\xb1')  # 0xe0794db1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ring_health))

        data.write(b'#\x1d\x0f\xc4')  # 0x231d0fc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.wheel_energy_beam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'>\x1b\x90\xff')  # 0x3e1b90ff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x3e1b90ff.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd0\x12(8')  # 0xd0122838
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.giant_contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12Y\xaa\xcd')  # 0x1259aacd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sphere_contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x84a\xabR')  # 0x8461ab52
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x8461ab52.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(rv+')  # 0x2872762b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x2872762b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0ck\x7f\xa9')  # 0xc6b7fa9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x313d0133=data['unknown_0x313d0133'],
            unknown_0xecb65675=data['unknown_0xecb65675'],
            unknown_0x80a300a5=data['unknown_0x80a300a5'],
            unknown_0x8fe03c41=data['unknown_0x8fe03c41'],
            unknown_0x4bc36eee=data['unknown_0x4bc36eee'],
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
            giant_electric_ball_damage=DamageInfo.from_json(data['giant_electric_ball_damage']),
            ring_projectile_damage=DamageInfo.from_json(data['ring_projectile_damage']),
            ring_vulnerability=DamageVulnerability.from_json(data['ring_vulnerability']),
            ring_health=data['ring_health'],
            wheel_energy_beam_damage=DamageInfo.from_json(data['wheel_energy_beam_damage']),
            damage_info_0x3e1b90ff=DamageInfo.from_json(data['damage_info_0x3e1b90ff']),
            giant_contact_damage=DamageInfo.from_json(data['giant_contact_damage']),
            sphere_contact_damage=DamageInfo.from_json(data['sphere_contact_damage']),
            damage_info_0x8461ab52=DamageInfo.from_json(data['damage_info_0x8461ab52']),
            damage_info_0x2872762b=DamageInfo.from_json(data['damage_info_0x2872762b']),
            damage_vulnerability=DamageVulnerability.from_json(data['damage_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x313d0133': self.unknown_0x313d0133,
            'unknown_0xecb65675': self.unknown_0xecb65675,
            'unknown_0x80a300a5': self.unknown_0x80a300a5,
            'unknown_0x8fe03c41': self.unknown_0x8fe03c41,
            'unknown_0x4bc36eee': self.unknown_0x4bc36eee,
            'shock_wave_info': self.shock_wave_info.to_json(),
            'giant_electric_ball_damage': self.giant_electric_ball_damage.to_json(),
            'ring_projectile_damage': self.ring_projectile_damage.to_json(),
            'ring_vulnerability': self.ring_vulnerability.to_json(),
            'ring_health': self.ring_health,
            'wheel_energy_beam_damage': self.wheel_energy_beam_damage.to_json(),
            'damage_info_0x3e1b90ff': self.damage_info_0x3e1b90ff.to_json(),
            'giant_contact_damage': self.giant_contact_damage.to_json(),
            'sphere_contact_damage': self.sphere_contact_damage.to_json(),
            'damage_info_0x8461ab52': self.damage_info_0x8461ab52.to_json(),
            'damage_info_0x2872762b': self.damage_info_0x2872762b.to_json(),
            'damage_vulnerability': self.damage_vulnerability.to_json(),
        }


def _decode_unknown_0x313d0133(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xecb65675(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x80a300a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8fe03c41(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4bc36eee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_giant_electric_ball_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_ring_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_ring_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_ring_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_wheel_energy_beam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0x3e1b90ff(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_giant_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_sphere_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0x8461ab52(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0x2872762b(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x313d0133: ('unknown_0x313d0133', _decode_unknown_0x313d0133),
    0xecb65675: ('unknown_0xecb65675', _decode_unknown_0xecb65675),
    0x80a300a5: ('unknown_0x80a300a5', _decode_unknown_0x80a300a5),
    0x8fe03c41: ('unknown_0x8fe03c41', _decode_unknown_0x8fe03c41),
    0x4bc36eee: ('unknown_0x4bc36eee', _decode_unknown_0x4bc36eee),
    0xa40f65c2: ('shock_wave_info', _decode_shock_wave_info),
    0x7651ec00: ('giant_electric_ball_damage', _decode_giant_electric_ball_damage),
    0x18f91880: ('ring_projectile_damage', _decode_ring_projectile_damage),
    0x9562e522: ('ring_vulnerability', _decode_ring_vulnerability),
    0xe0794db1: ('ring_health', _decode_ring_health),
    0x231d0fc4: ('wheel_energy_beam_damage', _decode_wheel_energy_beam_damage),
    0x3e1b90ff: ('damage_info_0x3e1b90ff', _decode_damage_info_0x3e1b90ff),
    0xd0122838: ('giant_contact_damage', _decode_giant_contact_damage),
    0x1259aacd: ('sphere_contact_damage', _decode_sphere_contact_damage),
    0x8461ab52: ('damage_info_0x8461ab52', _decode_damage_info_0x8461ab52),
    0x2872762b: ('damage_info_0x2872762b', _decode_damage_info_0x2872762b),
    0xc6b7fa9: ('damage_vulnerability', _decode_damage_vulnerability),
}
