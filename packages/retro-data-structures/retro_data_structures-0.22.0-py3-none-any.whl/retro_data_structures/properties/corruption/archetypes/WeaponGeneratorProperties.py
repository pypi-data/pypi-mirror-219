# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
import retro_data_structures.enums.corruption as enums
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.StaticGeometryTest import StaticGeometryTest
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class WeaponGeneratorProperties(BaseProperty):
    damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    weapon: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    fire_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    script_weapon_type: enums.ScriptWeaponType = dataclasses.field(default=enums.ScriptWeaponType.Unknown1)
    collision_checks: enums.CollisionChecks = dataclasses.field(default=enums.CollisionChecks.Unknown4)
    static_geometry_test: StaticGeometryTest = dataclasses.field(default_factory=StaticGeometryTest)
    unknown: bool = dataclasses.field(default=False)
    locator_name: str = dataclasses.field(default='')

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
        data.write(b'\x00\x08')  # 8 properties

        data.write(b'3\x7f\x95$')  # 0x337f9524
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\xf6\xb2\x90')  # 0x9ef6b290
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.weapon))

        data.write(b'N\x83\xf4\xa7')  # 0x4e83f4a7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.fire_sound))

        data.write(b'\xba\xda\x8d\xea')  # 0xbada8dea
        data.write(b'\x00\x04')  # size
        self.script_weapon_type.to_stream(data)

        data.write(b'\x92\x1bx\xa9')  # 0x921b78a9
        data.write(b'\x00\x04')  # size
        self.collision_checks.to_stream(data)

        data.write(b'\xfb\x0f\x95I')  # 0xfb0f9549
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.static_geometry_test.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'H-V\x9d')  # 0x482d569d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\xfb\xc6\xc1\x10')  # 0xfbc6c110
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.locator_name.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            damage=DamageInfo.from_json(data['damage']),
            weapon=data['weapon'],
            fire_sound=data['fire_sound'],
            script_weapon_type=enums.ScriptWeaponType.from_json(data['script_weapon_type']),
            collision_checks=enums.CollisionChecks.from_json(data['collision_checks']),
            static_geometry_test=StaticGeometryTest.from_json(data['static_geometry_test']),
            unknown=data['unknown'],
            locator_name=data['locator_name'],
        )

    def to_json(self) -> dict:
        return {
            'damage': self.damage.to_json(),
            'weapon': self.weapon,
            'fire_sound': self.fire_sound,
            'script_weapon_type': self.script_weapon_type.to_json(),
            'collision_checks': self.collision_checks.to_json(),
            'static_geometry_test': self.static_geometry_test.to_json(),
            'unknown': self.unknown,
            'locator_name': self.locator_name,
        }


def _decode_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_weapon(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fire_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_script_weapon_type(data: typing.BinaryIO, property_size: int):
    return enums.ScriptWeaponType.from_stream(data)


def _decode_collision_checks(data: typing.BinaryIO, property_size: int):
    return enums.CollisionChecks.from_stream(data)


def _decode_static_geometry_test(data: typing.BinaryIO, property_size: int):
    return StaticGeometryTest.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_locator_name(data: typing.BinaryIO, property_size: int):
    return b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x337f9524: ('damage', _decode_damage),
    0x9ef6b290: ('weapon', _decode_weapon),
    0x4e83f4a7: ('fire_sound', _decode_fire_sound),
    0xbada8dea: ('script_weapon_type', _decode_script_weapon_type),
    0x921b78a9: ('collision_checks', _decode_collision_checks),
    0xfb0f9549: ('static_geometry_test', _decode_static_geometry_test),
    0x482d569d: ('unknown', _decode_unknown),
    0xfbc6c110: ('locator_name', _decode_locator_name),
}
