# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class UnknownStruct3(BaseProperty):
    unknown_0x17cd8b2a: float = dataclasses.field(default=90.0)
    unknown_0x1473dad2: float = dataclasses.field(default=90.0)
    unknown_0x3650ce75: float = dataclasses.field(default=60.0)
    unknown_0x78520e6e: float = dataclasses.field(default=60.0)
    damage_angle: float = dataclasses.field(default=30.0)
    horiz_speed: float = dataclasses.field(default=30.0)
    vert_speed: float = dataclasses.field(default=30.0)
    fire_rate: float = dataclasses.field(default=1.0)
    unknown_0xf9bd253e: float = dataclasses.field(default=0.0)
    max_attack_angle: float = dataclasses.field(default=90.0)
    max_attack_range: float = dataclasses.field(default=40.0)
    start_attack_range: float = dataclasses.field(default=20.0)
    attack_leash_timer: float = dataclasses.field(default=2.0)
    weapon_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    weapon_effect: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    state_machine: AssetId = dataclasses.field(metadata={'asset_types': ['AFSM', 'FSM2']}, default=default_asset_id)
    telegraph_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)

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
        data.write(b'\x00\x13')  # 19 properties

        data.write(b'\x17\xcd\x8b*')  # 0x17cd8b2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x17cd8b2a))

        data.write(b'\x14s\xda\xd2')  # 0x1473dad2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1473dad2))

        data.write(b'6P\xceu')  # 0x3650ce75
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3650ce75))

        data.write(b'xR\x0en')  # 0x78520e6e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x78520e6e))

        data.write(b'\xa3\x9a]r')  # 0xa39a5d72
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_angle))

        data.write(b'\xfb.2\xdb')  # 0xfb2e32db
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horiz_speed))

        data.write(b'\x1b<\x86\x83')  # 0x1b3c8683
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_speed))

        data.write(b'\xc6\xe4\x8f\x18')  # 0xc6e48f18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fire_rate))

        data.write(b'\xf9\xbd%>')  # 0xf9bd253e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf9bd253e))

        data.write(b'\xf1\x1fs\x84')  # 0xf11f7384
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_angle))

        data.write(b'\xffw\xc9o')  # 0xff77c96f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_range))

        data.write(b"\xb6?'L")  # 0xb63f274c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_attack_range))

        data.write(b'\xf8\xd1\xeaw')  # 0xf8d1ea77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_leash_timer))

        data.write(b'\x8e_~\x96')  # 0x8e5f7e96
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weapon_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc43`\xa7')  # 0xc43360a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.weapon_effect))

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'{q\xae\x90')  # 0x7b71ae90
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'UtA`')  # 0x55744160
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.state_machine))

        data.write(b'\x8fh\xac!')  # 0x8f68ac21
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.telegraph_effect))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x17cd8b2a=data['unknown_0x17cd8b2a'],
            unknown_0x1473dad2=data['unknown_0x1473dad2'],
            unknown_0x3650ce75=data['unknown_0x3650ce75'],
            unknown_0x78520e6e=data['unknown_0x78520e6e'],
            damage_angle=data['damage_angle'],
            horiz_speed=data['horiz_speed'],
            vert_speed=data['vert_speed'],
            fire_rate=data['fire_rate'],
            unknown_0xf9bd253e=data['unknown_0xf9bd253e'],
            max_attack_angle=data['max_attack_angle'],
            max_attack_range=data['max_attack_range'],
            start_attack_range=data['start_attack_range'],
            attack_leash_timer=data['attack_leash_timer'],
            weapon_damage=DamageInfo.from_json(data['weapon_damage']),
            weapon_effect=data['weapon_effect'],
            health=HealthInfo.from_json(data['health']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            state_machine=data['state_machine'],
            telegraph_effect=data['telegraph_effect'],
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x17cd8b2a': self.unknown_0x17cd8b2a,
            'unknown_0x1473dad2': self.unknown_0x1473dad2,
            'unknown_0x3650ce75': self.unknown_0x3650ce75,
            'unknown_0x78520e6e': self.unknown_0x78520e6e,
            'damage_angle': self.damage_angle,
            'horiz_speed': self.horiz_speed,
            'vert_speed': self.vert_speed,
            'fire_rate': self.fire_rate,
            'unknown_0xf9bd253e': self.unknown_0xf9bd253e,
            'max_attack_angle': self.max_attack_angle,
            'max_attack_range': self.max_attack_range,
            'start_attack_range': self.start_attack_range,
            'attack_leash_timer': self.attack_leash_timer,
            'weapon_damage': self.weapon_damage.to_json(),
            'weapon_effect': self.weapon_effect,
            'health': self.health.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'state_machine': self.state_machine,
            'telegraph_effect': self.telegraph_effect,
        }

    def _dependencies_for_weapon_damage(self, asset_manager):
        yield from self.weapon_damage.dependencies_for(asset_manager)

    def _dependencies_for_weapon_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.weapon_effect)

    def _dependencies_for_health(self, asset_manager):
        yield from self.health.dependencies_for(asset_manager)

    def _dependencies_for_vulnerability(self, asset_manager):
        yield from self.vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_state_machine(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.state_machine)

    def _dependencies_for_telegraph_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.telegraph_effect)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_weapon_damage, "weapon_damage", "DamageInfo"),
            (self._dependencies_for_weapon_effect, "weapon_effect", "AssetId"),
            (self._dependencies_for_health, "health", "HealthInfo"),
            (self._dependencies_for_vulnerability, "vulnerability", "DamageVulnerability"),
            (self._dependencies_for_state_machine, "state_machine", "AssetId"),
            (self._dependencies_for_telegraph_effect, "telegraph_effect", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct3.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0x17cd8b2a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1473dad2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3650ce75(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x78520e6e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horiz_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fire_rate(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf9bd253e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_start_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_leash_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_weapon_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_weapon_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_state_machine(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_telegraph_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x17cd8b2a: ('unknown_0x17cd8b2a', _decode_unknown_0x17cd8b2a),
    0x1473dad2: ('unknown_0x1473dad2', _decode_unknown_0x1473dad2),
    0x3650ce75: ('unknown_0x3650ce75', _decode_unknown_0x3650ce75),
    0x78520e6e: ('unknown_0x78520e6e', _decode_unknown_0x78520e6e),
    0xa39a5d72: ('damage_angle', _decode_damage_angle),
    0xfb2e32db: ('horiz_speed', _decode_horiz_speed),
    0x1b3c8683: ('vert_speed', _decode_vert_speed),
    0xc6e48f18: ('fire_rate', _decode_fire_rate),
    0xf9bd253e: ('unknown_0xf9bd253e', _decode_unknown_0xf9bd253e),
    0xf11f7384: ('max_attack_angle', _decode_max_attack_angle),
    0xff77c96f: ('max_attack_range', _decode_max_attack_range),
    0xb63f274c: ('start_attack_range', _decode_start_attack_range),
    0xf8d1ea77: ('attack_leash_timer', _decode_attack_leash_timer),
    0x8e5f7e96: ('weapon_damage', _decode_weapon_damage),
    0xc43360a7: ('weapon_effect', _decode_weapon_effect),
    0xcf90d15e: ('health', _decode_health),
    0x7b71ae90: ('vulnerability', _decode_vulnerability),
    0x55744160: ('state_machine', _decode_state_machine),
    0x8f68ac21: ('telegraph_effect', _decode_telegraph_effect),
}
