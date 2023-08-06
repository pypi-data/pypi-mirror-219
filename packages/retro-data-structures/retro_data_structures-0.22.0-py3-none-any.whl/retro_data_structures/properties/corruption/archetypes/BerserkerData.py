# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.corruption.archetypes.ShockWaveInfo import ShockWaveInfo
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Spline import Spline


@dataclasses.dataclass()
class BerserkerData(BaseProperty):
    turn_threshold: float = dataclasses.field(default=60.0)
    unknown_0x76ebc21a: bool = dataclasses.field(default=True)
    melee_attack_range: float = dataclasses.field(default=10.0)
    unknown_0xc4db42e3: bool = dataclasses.field(default=True)
    ball_slam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0xbb7977b9: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ground_pound_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    pirate_as_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    phazon_cannon_beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    damage_info_0x97321af1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xfd5e7062: float = dataclasses.field(default=25.0)
    unknown_0xbd110814: float = dataclasses.field(default=100.0)
    unknown_0x3d947337: float = dataclasses.field(default=45.0)
    unknown_0x1a975a02: float = dataclasses.field(default=10.0)
    launch_projectile_data_0x066bc855: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    unknown_0x67e0e4b4: float = dataclasses.field(default=25.0)
    unknown_0xb7ad7067: float = dataclasses.field(default=10.0)
    unknown_0xf7e20811: float = dataclasses.field(default=25.0)
    unknown_0x4db474b8: float = dataclasses.field(default=45.0)
    unknown_0x68d3daa4: Spline = dataclasses.field(default_factory=Spline)
    unknown_0x1b359207: float = dataclasses.field(default=60.0)
    unknown_0xc12f397a: float = dataclasses.field(default=20.0)
    unknown_0x4bfee56b: float = dataclasses.field(default=1.0)
    unknown_0x8f3be6e1: float = dataclasses.field(default=0.5)
    unknown_0xdd825dc3: float = dataclasses.field(default=180.0)
    unknown_0x869415a3: float = dataclasses.field(default=5.0)
    unknown_0xc6db6dd5: float = dataclasses.field(default=25.0)
    phazon_grapple_time: float = dataclasses.field(default=5.0)
    unknown_0x58e6d9b8: float = dataclasses.field(default=20.0)
    unknown_0xcf111a99: float = dataclasses.field(default=20.0)
    phazon_grapple_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x92f0b2c7: float = dataclasses.field(default=20.0)
    unknown_0xbc2f8f30: float = dataclasses.field(default=0.5)
    unknown_0x910ad1e0: float = dataclasses.field(default=0.699999988079071)
    unknown_0x4566b3ef: float = dataclasses.field(default=0.5)
    approach_player_chance: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x24f779ca: float = dataclasses.field(default=0.800000011920929)
    armored_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    armor_health: float = dataclasses.field(default=500.0)
    armor_model1: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_model2: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_model3: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_model4: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    armor_model5: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unknown_0x09e8c7fd: float = dataclasses.field(default=1.399999976158142)
    weak_spot_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    provoked_head_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0x69d66ec4: float = dataclasses.field(default=10.0)
    unknown_0x299916b2: float = dataclasses.field(default=30.0)
    launch_projectile_data_0xfe51924e: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    launch_projectile_data_0x9b9c702c: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    launch_projectile_data_0x567ba94a: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    launch_projectile_data_0xf4d5150f: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    launch_projectile_data_0x8647c581: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    unknown_0x15d26d26: float = dataclasses.field(default=0.25)
    unknown_0x81eaa9d4: float = dataclasses.field(default=250.0)
    is_gandrayda: bool = dataclasses.field(default=False)
    is_chieftain: bool = dataclasses.field(default=False)
    shoulder_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    shoulder_health: float = dataclasses.field(default=100.0)
    unknown_0x268e5cb2: float = dataclasses.field(default=0.10000000149011612)
    left_shoulder_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    right_shoulder_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    weak_spot_armored_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    damage_vulnerability_0x200545bd: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    damage_vulnerability_0xf3ea94dc: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0xedf1189f: bool = dataclasses.field(default=False)
    minor_shockwave: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    unknown_0x0c1a5644: float = dataclasses.field(default=10.0)
    unknown_0xc6af2fd0: float = dataclasses.field(default=10.0)

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
        data.write(b'\x00G')  # 71 properties

        data.write(b"\xc0\xac'\x1e")  # 0xc0ac271e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.turn_threshold))

        data.write(b'v\xeb\xc2\x1a')  # 0x76ebc21a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x76ebc21a))

        data.write(b'\xc3\xe4=\x0e')  # 0xc3e43d0e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_attack_range))

        data.write(b'\xc4\xdbB\xe3')  # 0xc4db42e3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc4db42e3))

        data.write(b't\xbf\xfax')  # 0x74bffa78
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ball_slam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbbyw\xb9')  # 0xbb7977b9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0xbb7977b9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'G8\xc3!')  # 0x4738c321
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ground_pound_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\xe0\x03\xc1')  # 0xf4e003c1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.pirate_as_projectile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe0\xdb\xf2/')  # 0xe0dbf22f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.phazon_cannon_beam_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x972\x1a\xf1')  # 0x97321af1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x97321af1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfd^pb')  # 0xfd5e7062
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfd5e7062))

        data.write(b'\xbd\x11\x08\x14')  # 0xbd110814
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbd110814))

        data.write(b'=\x94s7')  # 0x3d947337
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3d947337))

        data.write(b'\x1a\x97Z\x02')  # 0x1a975a02
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1a975a02))

        data.write(b'\x06k\xc8U')  # 0x66bc855
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0x066bc855.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'g\xe0\xe4\xb4')  # 0x67e0e4b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x67e0e4b4))

        data.write(b'\xb7\xadpg')  # 0xb7ad7067
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb7ad7067))

        data.write(b'\xf7\xe2\x08\x11')  # 0xf7e20811
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf7e20811))

        data.write(b'M\xb4t\xb8')  # 0x4db474b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4db474b8))

        data.write(b'h\xd3\xda\xa4')  # 0x68d3daa4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x68d3daa4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1b5\x92\x07')  # 0x1b359207
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1b359207))

        data.write(b'\xc1/9z')  # 0xc12f397a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc12f397a))

        data.write(b'K\xfe\xe5k')  # 0x4bfee56b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4bfee56b))

        data.write(b'\x8f;\xe6\xe1')  # 0x8f3be6e1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8f3be6e1))

        data.write(b'\xdd\x82]\xc3')  # 0xdd825dc3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdd825dc3))

        data.write(b'\x86\x94\x15\xa3')  # 0x869415a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x869415a3))

        data.write(b'\xc6\xdbm\xd5')  # 0xc6db6dd5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc6db6dd5))

        data.write(b'\xdc\x8dx\x87')  # 0xdc8d7887
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.phazon_grapple_time))

        data.write(b'X\xe6\xd9\xb8')  # 0x58e6d9b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x58e6d9b8))

        data.write(b'\xcf\x11\x1a\x99')  # 0xcf111a99
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcf111a99))

        data.write(b'q\x9f\xd0k')  # 0x719fd06b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.phazon_grapple_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x92\xf0\xb2\xc7')  # 0x92f0b2c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x92f0b2c7))

        data.write(b'\xbc/\x8f0')  # 0xbc2f8f30
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbc2f8f30))

        data.write(b'\x91\n\xd1\xe0')  # 0x910ad1e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x910ad1e0))

        data.write(b'Ef\xb3\xef')  # 0x4566b3ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4566b3ef))

        data.write(b'o\xe5\r2')  # 0x6fe50d32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.approach_player_chance))

        data.write(b'$\xf7y\xca')  # 0x24f779ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x24f779ca))

        data.write(b'\xc6\xba\x97S')  # 0xc6ba9753
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.armored_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x83C\x90\x84')  # 0x83439084
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.armor_health))

        data.write(b'\x04T}4')  # 0x4547d34
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.armor_model1))

        data.write(b'\x82\xc0\x0f\x9a')  # 0x82c00f9a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.armor_model2))

        data.write(b'I\x9c\xdc?')  # 0x499cdc3f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.armor_model3))

        data.write(b'T\x99\xec\x87')  # 0x5499ec87
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.armor_model4))

        data.write(b'\x9f\xc5?"')  # 0x9fc53f22
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.armor_model5))

        data.write(b'\t\xe8\xc7\xfd')  # 0x9e8c7fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x09e8c7fd))

        data.write(b'J\xe5\x7f\xeb')  # 0x4ae57feb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.weak_spot_model))

        data.write(b'N\x1dq\xa1')  # 0x4e1d71a1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.provoked_head_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i\xd6n\xc4')  # 0x69d66ec4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x69d66ec4))

        data.write(b')\x99\x16\xb2')  # 0x299916b2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x299916b2))

        data.write(b'\xfeQ\x92N')  # 0xfe51924e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0xfe51924e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\x9cp,')  # 0x9b9c702c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0x9b9c702c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'V{\xa9J')  # 0x567ba94a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0x567ba94a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\xd5\x15\x0f')  # 0xf4d5150f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0xf4d5150f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86G\xc5\x81')  # 0x8647c581
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0x8647c581.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\xd2m&')  # 0x15d26d26
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x15d26d26))

        data.write(b'\x81\xea\xa9\xd4')  # 0x81eaa9d4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x81eaa9d4))

        data.write(b'S\x1a\x8c\x85')  # 0x531a8c85
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_gandrayda))

        data.write(b'g{\xd8\xab')  # 0x677bd8ab
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_chieftain))

        data.write(b'\xc6\xe60\x0f')  # 0xc6e6300f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shoulder_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15 V\x8a')  # 0x1520568a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shoulder_health))

        data.write(b'&\x8e\\\xb2')  # 0x268e5cb2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x268e5cb2))

        data.write(b'e\x0b\xa28')  # 0x650ba238
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_shoulder_model))

        data.write(b'h\x86T\x10')  # 0x68865410
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_shoulder_model))

        data.write(b'4-\xaez')  # 0x342dae7a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weak_spot_armored_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b' \x05E\xbd')  # 0x200545bd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability_0x200545bd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3\xea\x94\xdc')  # 0xf3ea94dc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability_0xf3ea94dc.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xf1\x18\x9f')  # 0xedf1189f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xedf1189f))

        data.write(b'\x84e3\xcc')  # 0x846533cc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.minor_shockwave.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*\xf1T\x8b')  # 0x2af1548b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0c\x1aVD')  # 0xc1a5644
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0c1a5644))

        data.write(b'\xc6\xaf/\xd0')  # 0xc6af2fd0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc6af2fd0))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            turn_threshold=data['turn_threshold'],
            unknown_0x76ebc21a=data['unknown_0x76ebc21a'],
            melee_attack_range=data['melee_attack_range'],
            unknown_0xc4db42e3=data['unknown_0xc4db42e3'],
            ball_slam_damage=DamageInfo.from_json(data['ball_slam_damage']),
            damage_info_0xbb7977b9=DamageInfo.from_json(data['damage_info_0xbb7977b9']),
            ground_pound_damage=DamageInfo.from_json(data['ground_pound_damage']),
            pirate_as_projectile_damage=DamageInfo.from_json(data['pirate_as_projectile_damage']),
            phazon_cannon_beam_info=PlasmaBeamInfo.from_json(data['phazon_cannon_beam_info']),
            damage_info_0x97321af1=DamageInfo.from_json(data['damage_info_0x97321af1']),
            unknown_0xfd5e7062=data['unknown_0xfd5e7062'],
            unknown_0xbd110814=data['unknown_0xbd110814'],
            unknown_0x3d947337=data['unknown_0x3d947337'],
            unknown_0x1a975a02=data['unknown_0x1a975a02'],
            launch_projectile_data_0x066bc855=LaunchProjectileData.from_json(data['launch_projectile_data_0x066bc855']),
            unknown_0x67e0e4b4=data['unknown_0x67e0e4b4'],
            unknown_0xb7ad7067=data['unknown_0xb7ad7067'],
            unknown_0xf7e20811=data['unknown_0xf7e20811'],
            unknown_0x4db474b8=data['unknown_0x4db474b8'],
            unknown_0x68d3daa4=Spline.from_json(data['unknown_0x68d3daa4']),
            unknown_0x1b359207=data['unknown_0x1b359207'],
            unknown_0xc12f397a=data['unknown_0xc12f397a'],
            unknown_0x4bfee56b=data['unknown_0x4bfee56b'],
            unknown_0x8f3be6e1=data['unknown_0x8f3be6e1'],
            unknown_0xdd825dc3=data['unknown_0xdd825dc3'],
            unknown_0x869415a3=data['unknown_0x869415a3'],
            unknown_0xc6db6dd5=data['unknown_0xc6db6dd5'],
            phazon_grapple_time=data['phazon_grapple_time'],
            unknown_0x58e6d9b8=data['unknown_0x58e6d9b8'],
            unknown_0xcf111a99=data['unknown_0xcf111a99'],
            phazon_grapple_damage=DamageInfo.from_json(data['phazon_grapple_damage']),
            unknown_0x92f0b2c7=data['unknown_0x92f0b2c7'],
            unknown_0xbc2f8f30=data['unknown_0xbc2f8f30'],
            unknown_0x910ad1e0=data['unknown_0x910ad1e0'],
            unknown_0x4566b3ef=data['unknown_0x4566b3ef'],
            approach_player_chance=data['approach_player_chance'],
            unknown_0x24f779ca=data['unknown_0x24f779ca'],
            armored_vulnerability=DamageVulnerability.from_json(data['armored_vulnerability']),
            armor_health=data['armor_health'],
            armor_model1=data['armor_model1'],
            armor_model2=data['armor_model2'],
            armor_model3=data['armor_model3'],
            armor_model4=data['armor_model4'],
            armor_model5=data['armor_model5'],
            unknown_0x09e8c7fd=data['unknown_0x09e8c7fd'],
            weak_spot_model=data['weak_spot_model'],
            provoked_head_vulnerability=DamageVulnerability.from_json(data['provoked_head_vulnerability']),
            unknown_0x69d66ec4=data['unknown_0x69d66ec4'],
            unknown_0x299916b2=data['unknown_0x299916b2'],
            launch_projectile_data_0xfe51924e=LaunchProjectileData.from_json(data['launch_projectile_data_0xfe51924e']),
            launch_projectile_data_0x9b9c702c=LaunchProjectileData.from_json(data['launch_projectile_data_0x9b9c702c']),
            launch_projectile_data_0x567ba94a=LaunchProjectileData.from_json(data['launch_projectile_data_0x567ba94a']),
            launch_projectile_data_0xf4d5150f=LaunchProjectileData.from_json(data['launch_projectile_data_0xf4d5150f']),
            launch_projectile_data_0x8647c581=LaunchProjectileData.from_json(data['launch_projectile_data_0x8647c581']),
            unknown_0x15d26d26=data['unknown_0x15d26d26'],
            unknown_0x81eaa9d4=data['unknown_0x81eaa9d4'],
            is_gandrayda=data['is_gandrayda'],
            is_chieftain=data['is_chieftain'],
            shoulder_vulnerability=DamageVulnerability.from_json(data['shoulder_vulnerability']),
            shoulder_health=data['shoulder_health'],
            unknown_0x268e5cb2=data['unknown_0x268e5cb2'],
            left_shoulder_model=data['left_shoulder_model'],
            right_shoulder_model=data['right_shoulder_model'],
            weak_spot_armored_vulnerability=DamageVulnerability.from_json(data['weak_spot_armored_vulnerability']),
            damage_vulnerability_0x200545bd=DamageVulnerability.from_json(data['damage_vulnerability_0x200545bd']),
            damage_vulnerability_0xf3ea94dc=DamageVulnerability.from_json(data['damage_vulnerability_0xf3ea94dc']),
            unknown_0xedf1189f=data['unknown_0xedf1189f'],
            minor_shockwave=ShockWaveInfo.from_json(data['minor_shockwave']),
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
            unknown_0x0c1a5644=data['unknown_0x0c1a5644'],
            unknown_0xc6af2fd0=data['unknown_0xc6af2fd0'],
        )

    def to_json(self) -> dict:
        return {
            'turn_threshold': self.turn_threshold,
            'unknown_0x76ebc21a': self.unknown_0x76ebc21a,
            'melee_attack_range': self.melee_attack_range,
            'unknown_0xc4db42e3': self.unknown_0xc4db42e3,
            'ball_slam_damage': self.ball_slam_damage.to_json(),
            'damage_info_0xbb7977b9': self.damage_info_0xbb7977b9.to_json(),
            'ground_pound_damage': self.ground_pound_damage.to_json(),
            'pirate_as_projectile_damage': self.pirate_as_projectile_damage.to_json(),
            'phazon_cannon_beam_info': self.phazon_cannon_beam_info.to_json(),
            'damage_info_0x97321af1': self.damage_info_0x97321af1.to_json(),
            'unknown_0xfd5e7062': self.unknown_0xfd5e7062,
            'unknown_0xbd110814': self.unknown_0xbd110814,
            'unknown_0x3d947337': self.unknown_0x3d947337,
            'unknown_0x1a975a02': self.unknown_0x1a975a02,
            'launch_projectile_data_0x066bc855': self.launch_projectile_data_0x066bc855.to_json(),
            'unknown_0x67e0e4b4': self.unknown_0x67e0e4b4,
            'unknown_0xb7ad7067': self.unknown_0xb7ad7067,
            'unknown_0xf7e20811': self.unknown_0xf7e20811,
            'unknown_0x4db474b8': self.unknown_0x4db474b8,
            'unknown_0x68d3daa4': self.unknown_0x68d3daa4.to_json(),
            'unknown_0x1b359207': self.unknown_0x1b359207,
            'unknown_0xc12f397a': self.unknown_0xc12f397a,
            'unknown_0x4bfee56b': self.unknown_0x4bfee56b,
            'unknown_0x8f3be6e1': self.unknown_0x8f3be6e1,
            'unknown_0xdd825dc3': self.unknown_0xdd825dc3,
            'unknown_0x869415a3': self.unknown_0x869415a3,
            'unknown_0xc6db6dd5': self.unknown_0xc6db6dd5,
            'phazon_grapple_time': self.phazon_grapple_time,
            'unknown_0x58e6d9b8': self.unknown_0x58e6d9b8,
            'unknown_0xcf111a99': self.unknown_0xcf111a99,
            'phazon_grapple_damage': self.phazon_grapple_damage.to_json(),
            'unknown_0x92f0b2c7': self.unknown_0x92f0b2c7,
            'unknown_0xbc2f8f30': self.unknown_0xbc2f8f30,
            'unknown_0x910ad1e0': self.unknown_0x910ad1e0,
            'unknown_0x4566b3ef': self.unknown_0x4566b3ef,
            'approach_player_chance': self.approach_player_chance,
            'unknown_0x24f779ca': self.unknown_0x24f779ca,
            'armored_vulnerability': self.armored_vulnerability.to_json(),
            'armor_health': self.armor_health,
            'armor_model1': self.armor_model1,
            'armor_model2': self.armor_model2,
            'armor_model3': self.armor_model3,
            'armor_model4': self.armor_model4,
            'armor_model5': self.armor_model5,
            'unknown_0x09e8c7fd': self.unknown_0x09e8c7fd,
            'weak_spot_model': self.weak_spot_model,
            'provoked_head_vulnerability': self.provoked_head_vulnerability.to_json(),
            'unknown_0x69d66ec4': self.unknown_0x69d66ec4,
            'unknown_0x299916b2': self.unknown_0x299916b2,
            'launch_projectile_data_0xfe51924e': self.launch_projectile_data_0xfe51924e.to_json(),
            'launch_projectile_data_0x9b9c702c': self.launch_projectile_data_0x9b9c702c.to_json(),
            'launch_projectile_data_0x567ba94a': self.launch_projectile_data_0x567ba94a.to_json(),
            'launch_projectile_data_0xf4d5150f': self.launch_projectile_data_0xf4d5150f.to_json(),
            'launch_projectile_data_0x8647c581': self.launch_projectile_data_0x8647c581.to_json(),
            'unknown_0x15d26d26': self.unknown_0x15d26d26,
            'unknown_0x81eaa9d4': self.unknown_0x81eaa9d4,
            'is_gandrayda': self.is_gandrayda,
            'is_chieftain': self.is_chieftain,
            'shoulder_vulnerability': self.shoulder_vulnerability.to_json(),
            'shoulder_health': self.shoulder_health,
            'unknown_0x268e5cb2': self.unknown_0x268e5cb2,
            'left_shoulder_model': self.left_shoulder_model,
            'right_shoulder_model': self.right_shoulder_model,
            'weak_spot_armored_vulnerability': self.weak_spot_armored_vulnerability.to_json(),
            'damage_vulnerability_0x200545bd': self.damage_vulnerability_0x200545bd.to_json(),
            'damage_vulnerability_0xf3ea94dc': self.damage_vulnerability_0xf3ea94dc.to_json(),
            'unknown_0xedf1189f': self.unknown_0xedf1189f,
            'minor_shockwave': self.minor_shockwave.to_json(),
            'shock_wave_info': self.shock_wave_info.to_json(),
            'unknown_0x0c1a5644': self.unknown_0x0c1a5644,
            'unknown_0xc6af2fd0': self.unknown_0xc6af2fd0,
        }


def _decode_turn_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ebc21a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_melee_attack_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc4db42e3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ball_slam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info_0xbb7977b9(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_ground_pound_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_pirate_as_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_phazon_cannon_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size)


def _decode_damage_info_0x97321af1(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0xfd5e7062(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbd110814(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3d947337(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1a975a02(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_projectile_data_0x066bc855(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_unknown_0x67e0e4b4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb7ad7067(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf7e20811(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4db474b8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x68d3daa4(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_unknown_0x1b359207(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc12f397a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4bfee56b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8f3be6e1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdd825dc3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x869415a3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc6db6dd5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phazon_grapple_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x58e6d9b8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcf111a99(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phazon_grapple_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x92f0b2c7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbc2f8f30(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x910ad1e0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4566b3ef(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_approach_player_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x24f779ca(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_armored_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_armor_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_armor_model1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_armor_model2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_armor_model3(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_armor_model4(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_armor_model5(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x09e8c7fd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_weak_spot_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_provoked_head_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0x69d66ec4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x299916b2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_projectile_data_0xfe51924e(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_launch_projectile_data_0x9b9c702c(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_launch_projectile_data_0x567ba94a(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_launch_projectile_data_0xf4d5150f(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_launch_projectile_data_0x8647c581(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_unknown_0x15d26d26(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x81eaa9d4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_gandrayda(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_chieftain(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_shoulder_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_shoulder_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x268e5cb2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_left_shoulder_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_shoulder_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_weak_spot_armored_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_damage_vulnerability_0x200545bd(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_damage_vulnerability_0xf3ea94dc(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0xedf1189f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minor_shockwave(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_unknown_0x0c1a5644(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc6af2fd0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc0ac271e: ('turn_threshold', _decode_turn_threshold),
    0x76ebc21a: ('unknown_0x76ebc21a', _decode_unknown_0x76ebc21a),
    0xc3e43d0e: ('melee_attack_range', _decode_melee_attack_range),
    0xc4db42e3: ('unknown_0xc4db42e3', _decode_unknown_0xc4db42e3),
    0x74bffa78: ('ball_slam_damage', _decode_ball_slam_damage),
    0xbb7977b9: ('damage_info_0xbb7977b9', _decode_damage_info_0xbb7977b9),
    0x4738c321: ('ground_pound_damage', _decode_ground_pound_damage),
    0xf4e003c1: ('pirate_as_projectile_damage', _decode_pirate_as_projectile_damage),
    0xe0dbf22f: ('phazon_cannon_beam_info', _decode_phazon_cannon_beam_info),
    0x97321af1: ('damage_info_0x97321af1', _decode_damage_info_0x97321af1),
    0xfd5e7062: ('unknown_0xfd5e7062', _decode_unknown_0xfd5e7062),
    0xbd110814: ('unknown_0xbd110814', _decode_unknown_0xbd110814),
    0x3d947337: ('unknown_0x3d947337', _decode_unknown_0x3d947337),
    0x1a975a02: ('unknown_0x1a975a02', _decode_unknown_0x1a975a02),
    0x66bc855: ('launch_projectile_data_0x066bc855', _decode_launch_projectile_data_0x066bc855),
    0x67e0e4b4: ('unknown_0x67e0e4b4', _decode_unknown_0x67e0e4b4),
    0xb7ad7067: ('unknown_0xb7ad7067', _decode_unknown_0xb7ad7067),
    0xf7e20811: ('unknown_0xf7e20811', _decode_unknown_0xf7e20811),
    0x4db474b8: ('unknown_0x4db474b8', _decode_unknown_0x4db474b8),
    0x68d3daa4: ('unknown_0x68d3daa4', _decode_unknown_0x68d3daa4),
    0x1b359207: ('unknown_0x1b359207', _decode_unknown_0x1b359207),
    0xc12f397a: ('unknown_0xc12f397a', _decode_unknown_0xc12f397a),
    0x4bfee56b: ('unknown_0x4bfee56b', _decode_unknown_0x4bfee56b),
    0x8f3be6e1: ('unknown_0x8f3be6e1', _decode_unknown_0x8f3be6e1),
    0xdd825dc3: ('unknown_0xdd825dc3', _decode_unknown_0xdd825dc3),
    0x869415a3: ('unknown_0x869415a3', _decode_unknown_0x869415a3),
    0xc6db6dd5: ('unknown_0xc6db6dd5', _decode_unknown_0xc6db6dd5),
    0xdc8d7887: ('phazon_grapple_time', _decode_phazon_grapple_time),
    0x58e6d9b8: ('unknown_0x58e6d9b8', _decode_unknown_0x58e6d9b8),
    0xcf111a99: ('unknown_0xcf111a99', _decode_unknown_0xcf111a99),
    0x719fd06b: ('phazon_grapple_damage', _decode_phazon_grapple_damage),
    0x92f0b2c7: ('unknown_0x92f0b2c7', _decode_unknown_0x92f0b2c7),
    0xbc2f8f30: ('unknown_0xbc2f8f30', _decode_unknown_0xbc2f8f30),
    0x910ad1e0: ('unknown_0x910ad1e0', _decode_unknown_0x910ad1e0),
    0x4566b3ef: ('unknown_0x4566b3ef', _decode_unknown_0x4566b3ef),
    0x6fe50d32: ('approach_player_chance', _decode_approach_player_chance),
    0x24f779ca: ('unknown_0x24f779ca', _decode_unknown_0x24f779ca),
    0xc6ba9753: ('armored_vulnerability', _decode_armored_vulnerability),
    0x83439084: ('armor_health', _decode_armor_health),
    0x4547d34: ('armor_model1', _decode_armor_model1),
    0x82c00f9a: ('armor_model2', _decode_armor_model2),
    0x499cdc3f: ('armor_model3', _decode_armor_model3),
    0x5499ec87: ('armor_model4', _decode_armor_model4),
    0x9fc53f22: ('armor_model5', _decode_armor_model5),
    0x9e8c7fd: ('unknown_0x09e8c7fd', _decode_unknown_0x09e8c7fd),
    0x4ae57feb: ('weak_spot_model', _decode_weak_spot_model),
    0x4e1d71a1: ('provoked_head_vulnerability', _decode_provoked_head_vulnerability),
    0x69d66ec4: ('unknown_0x69d66ec4', _decode_unknown_0x69d66ec4),
    0x299916b2: ('unknown_0x299916b2', _decode_unknown_0x299916b2),
    0xfe51924e: ('launch_projectile_data_0xfe51924e', _decode_launch_projectile_data_0xfe51924e),
    0x9b9c702c: ('launch_projectile_data_0x9b9c702c', _decode_launch_projectile_data_0x9b9c702c),
    0x567ba94a: ('launch_projectile_data_0x567ba94a', _decode_launch_projectile_data_0x567ba94a),
    0xf4d5150f: ('launch_projectile_data_0xf4d5150f', _decode_launch_projectile_data_0xf4d5150f),
    0x8647c581: ('launch_projectile_data_0x8647c581', _decode_launch_projectile_data_0x8647c581),
    0x15d26d26: ('unknown_0x15d26d26', _decode_unknown_0x15d26d26),
    0x81eaa9d4: ('unknown_0x81eaa9d4', _decode_unknown_0x81eaa9d4),
    0x531a8c85: ('is_gandrayda', _decode_is_gandrayda),
    0x677bd8ab: ('is_chieftain', _decode_is_chieftain),
    0xc6e6300f: ('shoulder_vulnerability', _decode_shoulder_vulnerability),
    0x1520568a: ('shoulder_health', _decode_shoulder_health),
    0x268e5cb2: ('unknown_0x268e5cb2', _decode_unknown_0x268e5cb2),
    0x650ba238: ('left_shoulder_model', _decode_left_shoulder_model),
    0x68865410: ('right_shoulder_model', _decode_right_shoulder_model),
    0x342dae7a: ('weak_spot_armored_vulnerability', _decode_weak_spot_armored_vulnerability),
    0x200545bd: ('damage_vulnerability_0x200545bd', _decode_damage_vulnerability_0x200545bd),
    0xf3ea94dc: ('damage_vulnerability_0xf3ea94dc', _decode_damage_vulnerability_0xf3ea94dc),
    0xedf1189f: ('unknown_0xedf1189f', _decode_unknown_0xedf1189f),
    0x846533cc: ('minor_shockwave', _decode_minor_shockwave),
    0x2af1548b: ('shock_wave_info', _decode_shock_wave_info),
    0xc1a5644: ('unknown_0x0c1a5644', _decode_unknown_0x0c1a5644),
    0xc6af2fd0: ('unknown_0xc6af2fd0', _decode_unknown_0xc6af2fd0),
}
