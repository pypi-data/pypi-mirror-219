# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.IngPossessionData import IngPossessionData


@dataclasses.dataclass()
class SplitterMainChassisData(BaseProperty):
    unknown_0xcef5c2fe: int = dataclasses.field(default=124)
    leg_stab_attack_interval: float = dataclasses.field(default=2.0)
    unknown_0xf6047d40: float = dataclasses.field(default=2.5)
    unknown_0x5130fd39: float = dataclasses.field(default=6.0)
    leg_stab_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    min_dodge_interval: float = dataclasses.field(default=3.0)
    dodge_chance: float = dataclasses.field(default=100.0)
    deployment_speed: float = dataclasses.field(default=40.0)
    scan_duration: float = dataclasses.field(default=3.0)
    laser_sweep_interval: float = dataclasses.field(default=6.0)
    unknown_0xb3ea58f8: float = dataclasses.field(default=30.0)
    unknown_0x14ded881: float = dataclasses.field(default=60.0)
    unknown_0x35eedd1c: float = dataclasses.field(default=20.0)
    unknown_0x2dde6bfb: float = dataclasses.field(default=20.0)
    unknown_0x8ae1ee93: float = dataclasses.field(default=60.0)
    unknown_0x5027d1aa: float = dataclasses.field(default=20.0)
    spin_attack_interval: float = dataclasses.field(default=6.0)
    unknown_0xf65e430f: float = dataclasses.field(default=6.0)
    unknown_0x43722555: float = dataclasses.field(default=1.5)
    unknown_0x8935377c: float = dataclasses.field(default=10.0)
    unknown_0x2e01b705: float = dataclasses.field(default=30.0)
    unknown_0xd5f34476: int = dataclasses.field(default=4)
    unknown_0x21296bdc: float = dataclasses.field(default=30.0)
    spin_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_alerted: int = dataclasses.field(default=0, metadata={'sound': True})
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)
    spin_attack_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

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

        data.write(b'\xce\xf5\xc2\xfe')  # 0xcef5c2fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xcef5c2fe))

        data.write(b'\xa8\xfd\xdb\xa0')  # 0xa8fddba0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.leg_stab_attack_interval))

        data.write(b'\xf6\x04}@')  # 0xf6047d40
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf6047d40))

        data.write(b'Q0\xfd9')  # 0x5130fd39
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5130fd39))

        data.write(b'\xef\xac\xfaP')  # 0xefacfa50
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.leg_stab_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x99\xa5Y9')  # 0x99a55939
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_dodge_interval))

        data.write(b'G\xbe2\x98')  # 0x47be3298
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_chance))

        data.write(b'\xee\xadkM')  # 0xeead6b4d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.deployment_speed))

        data.write(b'\xf8M\x8f\xda')  # 0xf84d8fda
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.scan_duration))

        data.write(b'\x0f\xbaI+')  # 0xfba492b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.laser_sweep_interval))

        data.write(b'\xb3\xeaX\xf8')  # 0xb3ea58f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb3ea58f8))

        data.write(b'\x14\xde\xd8\x81')  # 0x14ded881
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x14ded881))

        data.write(b'5\xee\xdd\x1c')  # 0x35eedd1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x35eedd1c))

        data.write(b'-\xdek\xfb')  # 0x2dde6bfb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2dde6bfb))

        data.write(b'\x8a\xe1\xee\x93')  # 0x8ae1ee93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8ae1ee93))

        data.write(b"P'\xd1\xaa")  # 0x5027d1aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5027d1aa))

        data.write(b'\xd8\x94\x06b')  # 0xd8940662
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spin_attack_interval))

        data.write(b'\xf6^C\x0f')  # 0xf65e430f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf65e430f))

        data.write(b'Cr%U')  # 0x43722555
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x43722555))

        data.write(b'\x8957|')  # 0x8935377c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8935377c))

        data.write(b'.\x01\xb7\x05')  # 0x2e01b705
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2e01b705))

        data.write(b'\xd5\xf3Dv')  # 0xd5f34476
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd5f34476))

        data.write(b'!)k\xdc')  # 0x21296bdc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x21296bdc))

        data.write(b'\xcf\xac\xffS')  # 0xcfacff53
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spin_attack_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa6\x1c*f')  # 0xa61c2a66
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_alerted))

        data.write(b'\xe6\x17H\xed')  # 0xe61748ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_possession_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xe2<\xc5')  # 0x24e23cc5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spin_attack_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xcef5c2fe=data['unknown_0xcef5c2fe'],
            leg_stab_attack_interval=data['leg_stab_attack_interval'],
            unknown_0xf6047d40=data['unknown_0xf6047d40'],
            unknown_0x5130fd39=data['unknown_0x5130fd39'],
            leg_stab_damage=DamageInfo.from_json(data['leg_stab_damage']),
            min_dodge_interval=data['min_dodge_interval'],
            dodge_chance=data['dodge_chance'],
            deployment_speed=data['deployment_speed'],
            scan_duration=data['scan_duration'],
            laser_sweep_interval=data['laser_sweep_interval'],
            unknown_0xb3ea58f8=data['unknown_0xb3ea58f8'],
            unknown_0x14ded881=data['unknown_0x14ded881'],
            unknown_0x35eedd1c=data['unknown_0x35eedd1c'],
            unknown_0x2dde6bfb=data['unknown_0x2dde6bfb'],
            unknown_0x8ae1ee93=data['unknown_0x8ae1ee93'],
            unknown_0x5027d1aa=data['unknown_0x5027d1aa'],
            spin_attack_interval=data['spin_attack_interval'],
            unknown_0xf65e430f=data['unknown_0xf65e430f'],
            unknown_0x43722555=data['unknown_0x43722555'],
            unknown_0x8935377c=data['unknown_0x8935377c'],
            unknown_0x2e01b705=data['unknown_0x2e01b705'],
            unknown_0xd5f34476=data['unknown_0xd5f34476'],
            unknown_0x21296bdc=data['unknown_0x21296bdc'],
            spin_attack_damage=DamageInfo.from_json(data['spin_attack_damage']),
            sound_alerted=data['sound_alerted'],
            ing_possession_data=IngPossessionData.from_json(data['ing_possession_data']),
            spin_attack_vulnerability=DamageVulnerability.from_json(data['spin_attack_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xcef5c2fe': self.unknown_0xcef5c2fe,
            'leg_stab_attack_interval': self.leg_stab_attack_interval,
            'unknown_0xf6047d40': self.unknown_0xf6047d40,
            'unknown_0x5130fd39': self.unknown_0x5130fd39,
            'leg_stab_damage': self.leg_stab_damage.to_json(),
            'min_dodge_interval': self.min_dodge_interval,
            'dodge_chance': self.dodge_chance,
            'deployment_speed': self.deployment_speed,
            'scan_duration': self.scan_duration,
            'laser_sweep_interval': self.laser_sweep_interval,
            'unknown_0xb3ea58f8': self.unknown_0xb3ea58f8,
            'unknown_0x14ded881': self.unknown_0x14ded881,
            'unknown_0x35eedd1c': self.unknown_0x35eedd1c,
            'unknown_0x2dde6bfb': self.unknown_0x2dde6bfb,
            'unknown_0x8ae1ee93': self.unknown_0x8ae1ee93,
            'unknown_0x5027d1aa': self.unknown_0x5027d1aa,
            'spin_attack_interval': self.spin_attack_interval,
            'unknown_0xf65e430f': self.unknown_0xf65e430f,
            'unknown_0x43722555': self.unknown_0x43722555,
            'unknown_0x8935377c': self.unknown_0x8935377c,
            'unknown_0x2e01b705': self.unknown_0x2e01b705,
            'unknown_0xd5f34476': self.unknown_0xd5f34476,
            'unknown_0x21296bdc': self.unknown_0x21296bdc,
            'spin_attack_damage': self.spin_attack_damage.to_json(),
            'sound_alerted': self.sound_alerted,
            'ing_possession_data': self.ing_possession_data.to_json(),
            'spin_attack_vulnerability': self.spin_attack_vulnerability.to_json(),
        }

    def _dependencies_for_leg_stab_damage(self, asset_manager):
        yield from self.leg_stab_damage.dependencies_for(asset_manager)

    def _dependencies_for_spin_attack_damage(self, asset_manager):
        yield from self.spin_attack_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_alerted(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_alerted)

    def _dependencies_for_ing_possession_data(self, asset_manager):
        yield from self.ing_possession_data.dependencies_for(asset_manager)

    def _dependencies_for_spin_attack_vulnerability(self, asset_manager):
        yield from self.spin_attack_vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_leg_stab_damage, "leg_stab_damage", "DamageInfo"),
            (self._dependencies_for_spin_attack_damage, "spin_attack_damage", "DamageInfo"),
            (self._dependencies_for_sound_alerted, "sound_alerted", "int"),
            (self._dependencies_for_ing_possession_data, "ing_possession_data", "IngPossessionData"),
            (self._dependencies_for_spin_attack_vulnerability, "spin_attack_vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SplitterMainChassisData.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0xcef5c2fe(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_leg_stab_attack_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf6047d40(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5130fd39(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_leg_stab_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})


def _decode_min_dodge_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_deployment_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_scan_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_laser_sweep_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb3ea58f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x14ded881(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x35eedd1c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2dde6bfb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8ae1ee93(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5027d1aa(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spin_attack_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf65e430f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x43722555(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8935377c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2e01b705(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd5f34476(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x21296bdc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spin_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})


def _decode_sound_alerted(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


def _decode_spin_attack_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xcef5c2fe: ('unknown_0xcef5c2fe', _decode_unknown_0xcef5c2fe),
    0xa8fddba0: ('leg_stab_attack_interval', _decode_leg_stab_attack_interval),
    0xf6047d40: ('unknown_0xf6047d40', _decode_unknown_0xf6047d40),
    0x5130fd39: ('unknown_0x5130fd39', _decode_unknown_0x5130fd39),
    0xefacfa50: ('leg_stab_damage', _decode_leg_stab_damage),
    0x99a55939: ('min_dodge_interval', _decode_min_dodge_interval),
    0x47be3298: ('dodge_chance', _decode_dodge_chance),
    0xeead6b4d: ('deployment_speed', _decode_deployment_speed),
    0xf84d8fda: ('scan_duration', _decode_scan_duration),
    0xfba492b: ('laser_sweep_interval', _decode_laser_sweep_interval),
    0xb3ea58f8: ('unknown_0xb3ea58f8', _decode_unknown_0xb3ea58f8),
    0x14ded881: ('unknown_0x14ded881', _decode_unknown_0x14ded881),
    0x35eedd1c: ('unknown_0x35eedd1c', _decode_unknown_0x35eedd1c),
    0x2dde6bfb: ('unknown_0x2dde6bfb', _decode_unknown_0x2dde6bfb),
    0x8ae1ee93: ('unknown_0x8ae1ee93', _decode_unknown_0x8ae1ee93),
    0x5027d1aa: ('unknown_0x5027d1aa', _decode_unknown_0x5027d1aa),
    0xd8940662: ('spin_attack_interval', _decode_spin_attack_interval),
    0xf65e430f: ('unknown_0xf65e430f', _decode_unknown_0xf65e430f),
    0x43722555: ('unknown_0x43722555', _decode_unknown_0x43722555),
    0x8935377c: ('unknown_0x8935377c', _decode_unknown_0x8935377c),
    0x2e01b705: ('unknown_0x2e01b705', _decode_unknown_0x2e01b705),
    0xd5f34476: ('unknown_0xd5f34476', _decode_unknown_0xd5f34476),
    0x21296bdc: ('unknown_0x21296bdc', _decode_unknown_0x21296bdc),
    0xcfacff53: ('spin_attack_damage', _decode_spin_attack_damage),
    0xa61c2a66: ('sound_alerted', _decode_sound_alerted),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
    0x24e23cc5: ('spin_attack_vulnerability', _decode_spin_attack_vulnerability),
}
