# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.SandBossStructA import SandBossStructA
from retro_data_structures.properties.echoes.archetypes.UnknownStruct40 import UnknownStruct40
from retro_data_structures.properties.echoes.archetypes.UnknownStruct41 import UnknownStruct41
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SandBossData(BaseProperty):
    scannable_info1: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    command_index: int = dataclasses.field(default=0)
    cracked_sphere1: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cracked_sphere2: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cracked_sphere3: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    snap_jaw_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    spit_out_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xbf88fe4f: float = dataclasses.field(default=4.0)
    unknown_0x74c702b3: float = dataclasses.field(default=1.0)
    dark_beam_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    dark_beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x2b42dddf: float = dataclasses.field(default=90.0)
    unknown_0x1562e0d6: float = dataclasses.field(default=10.0)
    unknown_0xd0db2574: float = dataclasses.field(default=100.0)
    suck_air_time: float = dataclasses.field(default=7.0)
    suck_morphball_range: float = dataclasses.field(default=30.0)
    spit_morphball_time: float = dataclasses.field(default=5.0)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_struct40: UnknownStruct40 = dataclasses.field(default_factory=UnknownStruct40)
    unknown_struct41: UnknownStruct41 = dataclasses.field(default_factory=UnknownStruct41)
    sand_boss_struct_a_0x8b452a19: SandBossStructA = dataclasses.field(default_factory=SandBossStructA)
    sand_boss_struct_a_0x0cf8c54c: SandBossStructA = dataclasses.field(default_factory=SandBossStructA)
    model_with_tail_armor: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    skin_for_armored_tail: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    damage_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    stampede_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    suck_air_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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

        data.write(b'r\x12HB')  # 0x72124842
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scannable_info1))

        data.write(b'\xe3M|I')  # 0xe34d7c49
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.command_index))

        data.write(b'\xe4rb\xf5')  # 0xe47262f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.cracked_sphere1))

        data.write(b'b\xe6\x10[')  # 0x62e6105b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.cracked_sphere2))

        data.write(b'\xa9\xba\xc3\xfe')  # 0xa9bac3fe
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.cracked_sphere3))

        data.write(b'\x19\xc9\x1a\xaa')  # 0x19c91aaa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.snap_jaw_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'X\x88\x93d')  # 0x58889364
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.spit_out_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\x88\xfeO')  # 0xbf88fe4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbf88fe4f))

        data.write(b't\xc7\x02\xb3')  # 0x74c702b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x74c702b3))

        data.write(b'5\xee\x17]')  # 0x35ee175d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.dark_beam_projectile))

        data.write(b'\x94\xc2\x15\x0f')  # 0x94c2150f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_beam_damage.to_stream(data, default_override={'di_weapon_type': 1, 'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'+B\xdd\xdf')  # 0x2b42dddf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2b42dddf))

        data.write(b'\x15b\xe0\xd6')  # 0x1562e0d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1562e0d6))

        data.write(b'\xd0\xdb%t')  # 0xd0db2574
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd0db2574))

        data.write(b'\xf1\xae\xd4=')  # 0xf1aed43d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.suck_air_time))

        data.write(b'0U\xdd\x0e')  # 0x3055dd0e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.suck_morphball_range))

        data.write(b'o\x13Ye')  # 0x6f135965
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spit_morphball_time))

        data.write(b'\xc4\x90\x86\xd9')  # 0xc49086d9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part))

        data.write(b'\x957\x1a2')  # 0x95371a32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct40.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\x19\xe5a')  # 0x7619e561
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct41.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8bE*\x19')  # 0x8b452a19
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sand_boss_struct_a_0x8b452a19.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0c\xf8\xc5L')  # 0xcf8c54c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sand_boss_struct_a_0x0cf8c54c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbb\xd8F\x81')  # 0xbbd84681
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.model_with_tail_armor))

        data.write(b'\xdfm\xa1\xa2')  # 0xdf6da1a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.skin_for_armored_tail))

        data.write(b'\xb7\xec\xdc\xf9')  # 0xb7ecdcf9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x84N\xd7\x9c')  # 0x844ed79c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.stampede_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'w!\x01g')  # 0x77210167
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.suck_air_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scannable_info1=data['scannable_info1'],
            command_index=data['command_index'],
            cracked_sphere1=data['cracked_sphere1'],
            cracked_sphere2=data['cracked_sphere2'],
            cracked_sphere3=data['cracked_sphere3'],
            snap_jaw_damage=DamageInfo.from_json(data['snap_jaw_damage']),
            spit_out_damage=DamageInfo.from_json(data['spit_out_damage']),
            unknown_0xbf88fe4f=data['unknown_0xbf88fe4f'],
            unknown_0x74c702b3=data['unknown_0x74c702b3'],
            dark_beam_projectile=data['dark_beam_projectile'],
            dark_beam_damage=DamageInfo.from_json(data['dark_beam_damage']),
            unknown_0x2b42dddf=data['unknown_0x2b42dddf'],
            unknown_0x1562e0d6=data['unknown_0x1562e0d6'],
            unknown_0xd0db2574=data['unknown_0xd0db2574'],
            suck_air_time=data['suck_air_time'],
            suck_morphball_range=data['suck_morphball_range'],
            spit_morphball_time=data['spit_morphball_time'],
            part=data['part'],
            unknown_struct40=UnknownStruct40.from_json(data['unknown_struct40']),
            unknown_struct41=UnknownStruct41.from_json(data['unknown_struct41']),
            sand_boss_struct_a_0x8b452a19=SandBossStructA.from_json(data['sand_boss_struct_a_0x8b452a19']),
            sand_boss_struct_a_0x0cf8c54c=SandBossStructA.from_json(data['sand_boss_struct_a_0x0cf8c54c']),
            model_with_tail_armor=data['model_with_tail_armor'],
            skin_for_armored_tail=data['skin_for_armored_tail'],
            damage_vulnerability=DamageVulnerability.from_json(data['damage_vulnerability']),
            stampede_vulnerability=DamageVulnerability.from_json(data['stampede_vulnerability']),
            suck_air_vulnerability=DamageVulnerability.from_json(data['suck_air_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'scannable_info1': self.scannable_info1,
            'command_index': self.command_index,
            'cracked_sphere1': self.cracked_sphere1,
            'cracked_sphere2': self.cracked_sphere2,
            'cracked_sphere3': self.cracked_sphere3,
            'snap_jaw_damage': self.snap_jaw_damage.to_json(),
            'spit_out_damage': self.spit_out_damage.to_json(),
            'unknown_0xbf88fe4f': self.unknown_0xbf88fe4f,
            'unknown_0x74c702b3': self.unknown_0x74c702b3,
            'dark_beam_projectile': self.dark_beam_projectile,
            'dark_beam_damage': self.dark_beam_damage.to_json(),
            'unknown_0x2b42dddf': self.unknown_0x2b42dddf,
            'unknown_0x1562e0d6': self.unknown_0x1562e0d6,
            'unknown_0xd0db2574': self.unknown_0xd0db2574,
            'suck_air_time': self.suck_air_time,
            'suck_morphball_range': self.suck_morphball_range,
            'spit_morphball_time': self.spit_morphball_time,
            'part': self.part,
            'unknown_struct40': self.unknown_struct40.to_json(),
            'unknown_struct41': self.unknown_struct41.to_json(),
            'sand_boss_struct_a_0x8b452a19': self.sand_boss_struct_a_0x8b452a19.to_json(),
            'sand_boss_struct_a_0x0cf8c54c': self.sand_boss_struct_a_0x0cf8c54c.to_json(),
            'model_with_tail_armor': self.model_with_tail_armor,
            'skin_for_armored_tail': self.skin_for_armored_tail,
            'damage_vulnerability': self.damage_vulnerability.to_json(),
            'stampede_vulnerability': self.stampede_vulnerability.to_json(),
            'suck_air_vulnerability': self.suck_air_vulnerability.to_json(),
        }

    def _dependencies_for_scannable_info1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scannable_info1)

    def _dependencies_for_cracked_sphere1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.cracked_sphere1)

    def _dependencies_for_cracked_sphere2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.cracked_sphere2)

    def _dependencies_for_cracked_sphere3(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.cracked_sphere3)

    def _dependencies_for_snap_jaw_damage(self, asset_manager):
        yield from self.snap_jaw_damage.dependencies_for(asset_manager)

    def _dependencies_for_spit_out_damage(self, asset_manager):
        yield from self.spit_out_damage.dependencies_for(asset_manager)

    def _dependencies_for_dark_beam_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dark_beam_projectile)

    def _dependencies_for_dark_beam_damage(self, asset_manager):
        yield from self.dark_beam_damage.dependencies_for(asset_manager)

    def _dependencies_for_part(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part)

    def _dependencies_for_unknown_struct40(self, asset_manager):
        yield from self.unknown_struct40.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct41(self, asset_manager):
        yield from self.unknown_struct41.dependencies_for(asset_manager)

    def _dependencies_for_sand_boss_struct_a_0x8b452a19(self, asset_manager):
        yield from self.sand_boss_struct_a_0x8b452a19.dependencies_for(asset_manager)

    def _dependencies_for_sand_boss_struct_a_0x0cf8c54c(self, asset_manager):
        yield from self.sand_boss_struct_a_0x0cf8c54c.dependencies_for(asset_manager)

    def _dependencies_for_model_with_tail_armor(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_with_tail_armor)

    def _dependencies_for_skin_for_armored_tail(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.skin_for_armored_tail)

    def _dependencies_for_damage_vulnerability(self, asset_manager):
        yield from self.damage_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_stampede_vulnerability(self, asset_manager):
        yield from self.stampede_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_suck_air_vulnerability(self, asset_manager):
        yield from self.suck_air_vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_scannable_info1, "scannable_info1", "AssetId"),
            (self._dependencies_for_cracked_sphere1, "cracked_sphere1", "AssetId"),
            (self._dependencies_for_cracked_sphere2, "cracked_sphere2", "AssetId"),
            (self._dependencies_for_cracked_sphere3, "cracked_sphere3", "AssetId"),
            (self._dependencies_for_snap_jaw_damage, "snap_jaw_damage", "DamageInfo"),
            (self._dependencies_for_spit_out_damage, "spit_out_damage", "DamageInfo"),
            (self._dependencies_for_dark_beam_projectile, "dark_beam_projectile", "AssetId"),
            (self._dependencies_for_dark_beam_damage, "dark_beam_damage", "DamageInfo"),
            (self._dependencies_for_part, "part", "AssetId"),
            (self._dependencies_for_unknown_struct40, "unknown_struct40", "UnknownStruct40"),
            (self._dependencies_for_unknown_struct41, "unknown_struct41", "UnknownStruct41"),
            (self._dependencies_for_sand_boss_struct_a_0x8b452a19, "sand_boss_struct_a_0x8b452a19", "SandBossStructA"),
            (self._dependencies_for_sand_boss_struct_a_0x0cf8c54c, "sand_boss_struct_a_0x0cf8c54c", "SandBossStructA"),
            (self._dependencies_for_model_with_tail_armor, "model_with_tail_armor", "AssetId"),
            (self._dependencies_for_skin_for_armored_tail, "skin_for_armored_tail", "AssetId"),
            (self._dependencies_for_damage_vulnerability, "damage_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_stampede_vulnerability, "stampede_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_suck_air_vulnerability, "suck_air_vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SandBossData.{field_name} ({field_type}): {e}"
                )


def _decode_scannable_info1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_command_index(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cracked_sphere1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_cracked_sphere2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_cracked_sphere3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_snap_jaw_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_spit_out_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_unknown_0xbf88fe4f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x74c702b3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dark_beam_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_dark_beam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 1, 'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_unknown_0x2b42dddf(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1562e0d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd0db2574(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_suck_air_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_suck_morphball_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_morphball_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_struct40(data: typing.BinaryIO, property_size: int):
    return UnknownStruct40.from_stream(data, property_size)


def _decode_unknown_struct41(data: typing.BinaryIO, property_size: int):
    return UnknownStruct41.from_stream(data, property_size)


def _decode_sand_boss_struct_a_0x8b452a19(data: typing.BinaryIO, property_size: int):
    return SandBossStructA.from_stream(data, property_size)


def _decode_sand_boss_struct_a_0x0cf8c54c(data: typing.BinaryIO, property_size: int):
    return SandBossStructA.from_stream(data, property_size)


def _decode_model_with_tail_armor(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_skin_for_armored_tail(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_stampede_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_suck_air_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x72124842: ('scannable_info1', _decode_scannable_info1),
    0xe34d7c49: ('command_index', _decode_command_index),
    0xe47262f5: ('cracked_sphere1', _decode_cracked_sphere1),
    0x62e6105b: ('cracked_sphere2', _decode_cracked_sphere2),
    0xa9bac3fe: ('cracked_sphere3', _decode_cracked_sphere3),
    0x19c91aaa: ('snap_jaw_damage', _decode_snap_jaw_damage),
    0x58889364: ('spit_out_damage', _decode_spit_out_damage),
    0xbf88fe4f: ('unknown_0xbf88fe4f', _decode_unknown_0xbf88fe4f),
    0x74c702b3: ('unknown_0x74c702b3', _decode_unknown_0x74c702b3),
    0x35ee175d: ('dark_beam_projectile', _decode_dark_beam_projectile),
    0x94c2150f: ('dark_beam_damage', _decode_dark_beam_damage),
    0x2b42dddf: ('unknown_0x2b42dddf', _decode_unknown_0x2b42dddf),
    0x1562e0d6: ('unknown_0x1562e0d6', _decode_unknown_0x1562e0d6),
    0xd0db2574: ('unknown_0xd0db2574', _decode_unknown_0xd0db2574),
    0xf1aed43d: ('suck_air_time', _decode_suck_air_time),
    0x3055dd0e: ('suck_morphball_range', _decode_suck_morphball_range),
    0x6f135965: ('spit_morphball_time', _decode_spit_morphball_time),
    0xc49086d9: ('part', _decode_part),
    0x95371a32: ('unknown_struct40', _decode_unknown_struct40),
    0x7619e561: ('unknown_struct41', _decode_unknown_struct41),
    0x8b452a19: ('sand_boss_struct_a_0x8b452a19', _decode_sand_boss_struct_a_0x8b452a19),
    0xcf8c54c: ('sand_boss_struct_a_0x0cf8c54c', _decode_sand_boss_struct_a_0x0cf8c54c),
    0xbbd84681: ('model_with_tail_armor', _decode_model_with_tail_armor),
    0xdf6da1a2: ('skin_for_armored_tail', _decode_skin_for_armored_tail),
    0xb7ecdcf9: ('damage_vulnerability', _decode_damage_vulnerability),
    0x844ed79c: ('stampede_vulnerability', _decode_stampede_vulnerability),
    0x77210167: ('suck_air_vulnerability', _decode_suck_air_vulnerability),
}
