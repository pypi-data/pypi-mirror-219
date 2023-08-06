# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.corruption.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.corruption.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.corruption.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.corruption.archetypes.HoverThenHomeProjectile import HoverThenHomeProjectile
from retro_data_structures.properties.corruption.archetypes.LaunchProjectileData import LaunchProjectileData
from retro_data_structures.properties.corruption.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.corruption.archetypes.ScannableParameters import ScannableParameters
from retro_data_structures.properties.corruption.archetypes.SeedBoss1HandData import SeedBoss1HandData
from retro_data_structures.properties.corruption.archetypes.SeedBoss1Shield import SeedBoss1Shield
from retro_data_structures.properties.corruption.archetypes.SeedBoss1Stage import SeedBoss1Stage
from retro_data_structures.properties.corruption.archetypes.ShockWaveInfo import ShockWaveInfo
from retro_data_structures.properties.corruption.archetypes.UnknownStruct60 import UnknownStruct60
from retro_data_structures.properties.corruption.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.corruption.core.Color import Color
from retro_data_structures.properties.corruption.core.Spline import Spline
from retro_data_structures.properties.corruption.core.Vector import Vector


@dataclasses.dataclass()
class SeedBoss1Data(BaseProperty):
    unknown_0xd3ad55b6: float = dataclasses.field(default=0.0)
    foot_health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    foot_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    left_foot: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    left_knee: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    left_thigh: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    right_foot: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    right_knee: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    right_thigh: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x50edae7f: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x30969cfe: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0xb25e271d: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x5d71b85c: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x3d0a8add: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x43223a97: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x9b76ad84: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0xfb0d9f05: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x48ee50ad: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x85635b3b: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0xe51869ba: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cmdl_0x5cea873f: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    head_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    jaw_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    ice_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    head_ice_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    jaw_ice_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    head_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    head_frozen_time: float = dataclasses.field(default=0.0)
    shockwave: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    unknown_struct60: UnknownStruct60 = dataclasses.field(default_factory=UnknownStruct60)
    beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    beam_damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    orb_slot_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    foot_explosion: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    foot_explosion_sound: AssetId = dataclasses.field(metadata={'asset_types': ['CAUD']}, default=default_asset_id)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    launch_projectile_data_0x7c9c3b51: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    hover_then_home_projectile_0x730fe427: HoverThenHomeProjectile = dataclasses.field(default_factory=HoverThenHomeProjectile)
    unknown_0x050924d3: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0x6414e848: float = dataclasses.field(default=0.0)
    unknown_0x2a7a2da7: float = dataclasses.field(default=0.0)
    launch_projectile_data_0x4392c34a: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    hover_then_home_projectile_0x868e4192: HoverThenHomeProjectile = dataclasses.field(default_factory=HoverThenHomeProjectile)
    hand_projectile_size: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0x153c001b: float = dataclasses.field(default=0.0)
    unknown_0x473b730b: float = dataclasses.field(default=0.0)
    hand_projectile_damage_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0x38786921: AssetId = dataclasses.field(metadata={'asset_types': []}, default=default_asset_id)
    charge_player_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    launch_projectile_data_0x50ae6e55: LaunchProjectileData = dataclasses.field(default_factory=LaunchProjectileData)
    hand_data: SeedBoss1HandData = dataclasses.field(default_factory=SeedBoss1HandData)
    unknown_0x3196b2e7: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x77d3b386: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    color_hyper_shockwave: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    unknown_0x7ce5c47c: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    color_hyper_quake: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    color_energized: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=0.0, b=0.0, a=0.0))
    min_taunt_time: float = dataclasses.field(default=0.0)
    max_taunt_time: float = dataclasses.field(default=0.0)
    seed_boss1_stage_0x45694db0: SeedBoss1Stage = dataclasses.field(default_factory=SeedBoss1Stage)
    seed_boss1_stage_0x338c748d: SeedBoss1Stage = dataclasses.field(default_factory=SeedBoss1Stage)
    seed_boss1_stage_0xa8ff9e59: SeedBoss1Stage = dataclasses.field(default_factory=SeedBoss1Stage)
    seed_boss1_stage_0xde4606f7: SeedBoss1Stage = dataclasses.field(default_factory=SeedBoss1Stage)
    shield_info: SeedBoss1Shield = dataclasses.field(default_factory=SeedBoss1Shield)
    foot_contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x64588114: float = dataclasses.field(default=0.0)
    approach_player_distance: float = dataclasses.field(default=0.0)
    approach_player_delay: float = dataclasses.field(default=0.0)
    approach_player_time: float = dataclasses.field(default=0.0)
    unknown_0xc2be328d: Spline = dataclasses.field(default_factory=Spline)
    scannable_parameters: ScannableParameters = dataclasses.field(default_factory=ScannableParameters)

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
        data.write(b'\x00I')  # 73 properties

        data.write(b'\xd3\xadU\xb6')  # 0xd3ad55b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd3ad55b6))

        data.write(b'\xb3>\xb53')  # 0xb33eb533
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.foot_health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&\xfaF\x0b')  # 0x26fa460b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.foot_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xad\r\xe5\xac')  # 0xad0de5ac
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_foot))

        data.write(b'\xfc\x12\x8c\x15')  # 0xfc128c15
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_knee))

        data.write(b')\x9b\x8d3')  # 0x299b8d33
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.left_thigh))

        data.write(b'\xa5\xbb\x98\xa6')  # 0xa5bb98a6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_foot))

        data.write(b'\xf4\xa4\xf1\x1f')  # 0xf4a4f11f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_knee))

        data.write(b'\xc9F\xd2P')  # 0xc946d250
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_thigh))

        data.write(b'P\xed\xae\x7f')  # 0x50edae7f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x50edae7f))

        data.write(b'0\x96\x9c\xfe')  # 0x30969cfe
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x30969cfe))

        data.write(b"\xb2^'\x1d")  # 0xb25e271d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xb25e271d))

        data.write(b']q\xb8\\')  # 0x5d71b85c
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x5d71b85c))

        data.write(b'=\n\x8a\xdd')  # 0x3d0a8add
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x3d0a8add))

        data.write(b'C":\x97')  # 0x43223a97
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x43223a97))

        data.write(b'\x9bv\xad\x84')  # 0x9b76ad84
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x9b76ad84))

        data.write(b'\xfb\r\x9f\x05')  # 0xfb0d9f05
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xfb0d9f05))

        data.write(b'H\xeeP\xad')  # 0x48ee50ad
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x48ee50ad))

        data.write(b'\x85c[;')  # 0x85635b3b
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x85635b3b))

        data.write(b'\xe5\x18i\xba')  # 0xe51869ba
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0xe51869ba))

        data.write(b'\\\xea\x87?')  # 0x5cea873f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.cmdl_0x5cea873f))

        data.write(b'\xc2\x88\xaei')  # 0xc288ae69
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.head_model))

        data.write(b'\xcd\xbdD\xe1')  # 0xcdbd44e1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.jaw_model))

        data.write(b'j\xd6\xcb\xba')  # 0x6ad6cbba
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.ice_model))

        data.write(b':\xb7\x98G')  # 0x3ab79847
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.head_ice_model))

        data.write(b"'\xb3\r5")  # 0x27b30d35
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.jaw_ice_model))

        data.write(b'\xec7\xe2\xfa')  # 0xec37e2fa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.head_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcc\xca2I')  # 0xccca3249
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.head_frozen_time))

        data.write(b'<\xe6\xe4\x82')  # 0x3ce6e482
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shockwave.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'r\xe0\x05\x01')  # 0x72e00501
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct60.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x15\x98\x01*')  # 0x1598012a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98\x82\x19\x96')  # 0x98821996
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdd4\xc3\xc0')  # 0xdd34c3c0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.orb_slot_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'T{\x9a\x9a')  # 0x547b9a9a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.foot_explosion))

        data.write(b'\xea\xf90W')  # 0xeaf93057
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.foot_explosion_sound))

        data.write(b'6\xc0g\xc2')  # 0x36c067c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.wpsc))

        data.write(b'&\x1e\xef\xe7')  # 0x261eefe7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x81\x8f\x81\x0b')  # 0x818f810b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'|\x9c;Q')  # 0x7c9c3b51
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0x7c9c3b51.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"s\x0f\xe4'")  # 0x730fe427
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hover_then_home_projectile_0x730fe427.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05\t$\xd3')  # 0x50924d3
        data.write(b'\x00\x0c')  # size
        self.unknown_0x050924d3.to_stream(data)

        data.write(b'd\x14\xe8H')  # 0x6414e848
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6414e848))

        data.write(b'*z-\xa7')  # 0x2a7a2da7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2a7a2da7))

        data.write(b'C\x92\xc3J')  # 0x4392c34a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0x4392c34a.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86\x8eA\x92')  # 0x868e4192
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hover_then_home_projectile_0x868e4192.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc8\xe1eU')  # 0xc8e16555
        data.write(b'\x00\x0c')  # size
        self.hand_projectile_size.to_stream(data)

        data.write(b'\x15<\x00\x1b')  # 0x153c001b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x153c001b))

        data.write(b'G;s\x0b')  # 0x473b730b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x473b730b))

        data.write(b'\xae\xa6\x0f$')  # 0xaea60f24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hand_projectile_damage_effect))

        data.write(b'8xi!')  # 0x38786921
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.unknown_0x38786921))

        data.write(b'\x9ec\x06_')  # 0x9e63065f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.charge_player_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'P\xaenU')  # 0x50ae6e55
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.launch_projectile_data_0x50ae6e55.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x9fi\x1a')  # 0xc69f691a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hand_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'1\x96\xb2\xe7')  # 0x3196b2e7
        data.write(b'\x00\x10')  # size
        self.unknown_0x3196b2e7.to_stream(data)

        data.write(b'w\xd3\xb3\x86')  # 0x77d3b386
        data.write(b'\x00\x10')  # size
        self.unknown_0x77d3b386.to_stream(data)

        data.write(b'\xa9\xbe\x10\x81')  # 0xa9be1081
        data.write(b'\x00\x10')  # size
        self.color_hyper_shockwave.to_stream(data)

        data.write(b'|\xe5\xc4|')  # 0x7ce5c47c
        data.write(b'\x00\x10')  # size
        self.unknown_0x7ce5c47c.to_stream(data)

        data.write(b'\xf9el9')  # 0xf9656c39
        data.write(b'\x00\x10')  # size
        self.color_hyper_quake.to_stream(data)

        data.write(b'\xd7\x14*\xfe')  # 0xd7142afe
        data.write(b'\x00\x10')  # size
        self.color_energized.to_stream(data)

        data.write(b'\xc3q\x8e\xa0')  # 0xc3718ea0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_taunt_time))

        data.write(b'\xd6\xfaZR')  # 0xd6fa5a52
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_taunt_time))

        data.write(b'EiM\xb0')  # 0x45694db0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss1_stage_0x45694db0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'3\x8ct\x8d')  # 0x338c748d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss1_stage_0x338c748d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa8\xff\x9eY')  # 0xa8ff9e59
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss1_stage_0xa8ff9e59.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdeF\x06\xf7')  # 0xde4606f7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seed_boss1_stage_0xde4606f7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\x83\xf9r')  # 0x2883f972
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shield_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'@\xac\x1f\xd4')  # 0x40ac1fd4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.foot_contact_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'dX\x81\x14')  # 0x64588114
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x64588114))

        data.write(b'q-2t')  # 0x712d3274
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.approach_player_distance))

        data.write(b'P\xec\x86\xc1')  # 0x50ec86c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.approach_player_delay))

        data.write(b'Skt\x93')  # 0x536b7493
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.approach_player_time))

        data.write(b'\xc2\xbe2\x8d')  # 0xc2be328d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xc2be328d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x02/\xdc\xa5')  # 0x22fdca5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scannable_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0xd3ad55b6=data['unknown_0xd3ad55b6'],
            foot_health=HealthInfo.from_json(data['foot_health']),
            foot_vulnerability=DamageVulnerability.from_json(data['foot_vulnerability']),
            left_foot=data['left_foot'],
            left_knee=data['left_knee'],
            left_thigh=data['left_thigh'],
            right_foot=data['right_foot'],
            right_knee=data['right_knee'],
            right_thigh=data['right_thigh'],
            cmdl_0x50edae7f=data['cmdl_0x50edae7f'],
            cmdl_0x30969cfe=data['cmdl_0x30969cfe'],
            cmdl_0xb25e271d=data['cmdl_0xb25e271d'],
            cmdl_0x5d71b85c=data['cmdl_0x5d71b85c'],
            cmdl_0x3d0a8add=data['cmdl_0x3d0a8add'],
            cmdl_0x43223a97=data['cmdl_0x43223a97'],
            cmdl_0x9b76ad84=data['cmdl_0x9b76ad84'],
            cmdl_0xfb0d9f05=data['cmdl_0xfb0d9f05'],
            cmdl_0x48ee50ad=data['cmdl_0x48ee50ad'],
            cmdl_0x85635b3b=data['cmdl_0x85635b3b'],
            cmdl_0xe51869ba=data['cmdl_0xe51869ba'],
            cmdl_0x5cea873f=data['cmdl_0x5cea873f'],
            head_model=data['head_model'],
            jaw_model=data['jaw_model'],
            ice_model=data['ice_model'],
            head_ice_model=data['head_ice_model'],
            jaw_ice_model=data['jaw_ice_model'],
            head_vulnerability=DamageVulnerability.from_json(data['head_vulnerability']),
            head_frozen_time=data['head_frozen_time'],
            shockwave=ShockWaveInfo.from_json(data['shockwave']),
            unknown_struct60=UnknownStruct60.from_json(data['unknown_struct60']),
            beam_info=PlasmaBeamInfo.from_json(data['beam_info']),
            beam_damage_info=DamageInfo.from_json(data['beam_damage_info']),
            orb_slot_vulnerability=DamageVulnerability.from_json(data['orb_slot_vulnerability']),
            foot_explosion=data['foot_explosion'],
            foot_explosion_sound=data['foot_explosion_sound'],
            wpsc=data['wpsc'],
            damage_info=DamageInfo.from_json(data['damage_info']),
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
            launch_projectile_data_0x7c9c3b51=LaunchProjectileData.from_json(data['launch_projectile_data_0x7c9c3b51']),
            hover_then_home_projectile_0x730fe427=HoverThenHomeProjectile.from_json(data['hover_then_home_projectile_0x730fe427']),
            unknown_0x050924d3=Vector.from_json(data['unknown_0x050924d3']),
            unknown_0x6414e848=data['unknown_0x6414e848'],
            unknown_0x2a7a2da7=data['unknown_0x2a7a2da7'],
            launch_projectile_data_0x4392c34a=LaunchProjectileData.from_json(data['launch_projectile_data_0x4392c34a']),
            hover_then_home_projectile_0x868e4192=HoverThenHomeProjectile.from_json(data['hover_then_home_projectile_0x868e4192']),
            hand_projectile_size=Vector.from_json(data['hand_projectile_size']),
            unknown_0x153c001b=data['unknown_0x153c001b'],
            unknown_0x473b730b=data['unknown_0x473b730b'],
            hand_projectile_damage_effect=data['hand_projectile_damage_effect'],
            unknown_0x38786921=data['unknown_0x38786921'],
            charge_player_damage=DamageInfo.from_json(data['charge_player_damage']),
            launch_projectile_data_0x50ae6e55=LaunchProjectileData.from_json(data['launch_projectile_data_0x50ae6e55']),
            hand_data=SeedBoss1HandData.from_json(data['hand_data']),
            unknown_0x3196b2e7=Color.from_json(data['unknown_0x3196b2e7']),
            unknown_0x77d3b386=Color.from_json(data['unknown_0x77d3b386']),
            color_hyper_shockwave=Color.from_json(data['color_hyper_shockwave']),
            unknown_0x7ce5c47c=Color.from_json(data['unknown_0x7ce5c47c']),
            color_hyper_quake=Color.from_json(data['color_hyper_quake']),
            color_energized=Color.from_json(data['color_energized']),
            min_taunt_time=data['min_taunt_time'],
            max_taunt_time=data['max_taunt_time'],
            seed_boss1_stage_0x45694db0=SeedBoss1Stage.from_json(data['seed_boss1_stage_0x45694db0']),
            seed_boss1_stage_0x338c748d=SeedBoss1Stage.from_json(data['seed_boss1_stage_0x338c748d']),
            seed_boss1_stage_0xa8ff9e59=SeedBoss1Stage.from_json(data['seed_boss1_stage_0xa8ff9e59']),
            seed_boss1_stage_0xde4606f7=SeedBoss1Stage.from_json(data['seed_boss1_stage_0xde4606f7']),
            shield_info=SeedBoss1Shield.from_json(data['shield_info']),
            foot_contact_damage=DamageInfo.from_json(data['foot_contact_damage']),
            unknown_0x64588114=data['unknown_0x64588114'],
            approach_player_distance=data['approach_player_distance'],
            approach_player_delay=data['approach_player_delay'],
            approach_player_time=data['approach_player_time'],
            unknown_0xc2be328d=Spline.from_json(data['unknown_0xc2be328d']),
            scannable_parameters=ScannableParameters.from_json(data['scannable_parameters']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0xd3ad55b6': self.unknown_0xd3ad55b6,
            'foot_health': self.foot_health.to_json(),
            'foot_vulnerability': self.foot_vulnerability.to_json(),
            'left_foot': self.left_foot,
            'left_knee': self.left_knee,
            'left_thigh': self.left_thigh,
            'right_foot': self.right_foot,
            'right_knee': self.right_knee,
            'right_thigh': self.right_thigh,
            'cmdl_0x50edae7f': self.cmdl_0x50edae7f,
            'cmdl_0x30969cfe': self.cmdl_0x30969cfe,
            'cmdl_0xb25e271d': self.cmdl_0xb25e271d,
            'cmdl_0x5d71b85c': self.cmdl_0x5d71b85c,
            'cmdl_0x3d0a8add': self.cmdl_0x3d0a8add,
            'cmdl_0x43223a97': self.cmdl_0x43223a97,
            'cmdl_0x9b76ad84': self.cmdl_0x9b76ad84,
            'cmdl_0xfb0d9f05': self.cmdl_0xfb0d9f05,
            'cmdl_0x48ee50ad': self.cmdl_0x48ee50ad,
            'cmdl_0x85635b3b': self.cmdl_0x85635b3b,
            'cmdl_0xe51869ba': self.cmdl_0xe51869ba,
            'cmdl_0x5cea873f': self.cmdl_0x5cea873f,
            'head_model': self.head_model,
            'jaw_model': self.jaw_model,
            'ice_model': self.ice_model,
            'head_ice_model': self.head_ice_model,
            'jaw_ice_model': self.jaw_ice_model,
            'head_vulnerability': self.head_vulnerability.to_json(),
            'head_frozen_time': self.head_frozen_time,
            'shockwave': self.shockwave.to_json(),
            'unknown_struct60': self.unknown_struct60.to_json(),
            'beam_info': self.beam_info.to_json(),
            'beam_damage_info': self.beam_damage_info.to_json(),
            'orb_slot_vulnerability': self.orb_slot_vulnerability.to_json(),
            'foot_explosion': self.foot_explosion,
            'foot_explosion_sound': self.foot_explosion_sound,
            'wpsc': self.wpsc,
            'damage_info': self.damage_info.to_json(),
            'shock_wave_info': self.shock_wave_info.to_json(),
            'launch_projectile_data_0x7c9c3b51': self.launch_projectile_data_0x7c9c3b51.to_json(),
            'hover_then_home_projectile_0x730fe427': self.hover_then_home_projectile_0x730fe427.to_json(),
            'unknown_0x050924d3': self.unknown_0x050924d3.to_json(),
            'unknown_0x6414e848': self.unknown_0x6414e848,
            'unknown_0x2a7a2da7': self.unknown_0x2a7a2da7,
            'launch_projectile_data_0x4392c34a': self.launch_projectile_data_0x4392c34a.to_json(),
            'hover_then_home_projectile_0x868e4192': self.hover_then_home_projectile_0x868e4192.to_json(),
            'hand_projectile_size': self.hand_projectile_size.to_json(),
            'unknown_0x153c001b': self.unknown_0x153c001b,
            'unknown_0x473b730b': self.unknown_0x473b730b,
            'hand_projectile_damage_effect': self.hand_projectile_damage_effect,
            'unknown_0x38786921': self.unknown_0x38786921,
            'charge_player_damage': self.charge_player_damage.to_json(),
            'launch_projectile_data_0x50ae6e55': self.launch_projectile_data_0x50ae6e55.to_json(),
            'hand_data': self.hand_data.to_json(),
            'unknown_0x3196b2e7': self.unknown_0x3196b2e7.to_json(),
            'unknown_0x77d3b386': self.unknown_0x77d3b386.to_json(),
            'color_hyper_shockwave': self.color_hyper_shockwave.to_json(),
            'unknown_0x7ce5c47c': self.unknown_0x7ce5c47c.to_json(),
            'color_hyper_quake': self.color_hyper_quake.to_json(),
            'color_energized': self.color_energized.to_json(),
            'min_taunt_time': self.min_taunt_time,
            'max_taunt_time': self.max_taunt_time,
            'seed_boss1_stage_0x45694db0': self.seed_boss1_stage_0x45694db0.to_json(),
            'seed_boss1_stage_0x338c748d': self.seed_boss1_stage_0x338c748d.to_json(),
            'seed_boss1_stage_0xa8ff9e59': self.seed_boss1_stage_0xa8ff9e59.to_json(),
            'seed_boss1_stage_0xde4606f7': self.seed_boss1_stage_0xde4606f7.to_json(),
            'shield_info': self.shield_info.to_json(),
            'foot_contact_damage': self.foot_contact_damage.to_json(),
            'unknown_0x64588114': self.unknown_0x64588114,
            'approach_player_distance': self.approach_player_distance,
            'approach_player_delay': self.approach_player_delay,
            'approach_player_time': self.approach_player_time,
            'unknown_0xc2be328d': self.unknown_0xc2be328d.to_json(),
            'scannable_parameters': self.scannable_parameters.to_json(),
        }


def _decode_unknown_0xd3ad55b6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_foot_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_foot_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_left_foot(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_knee(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_left_thigh(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_foot(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_knee(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_thigh(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x50edae7f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x30969cfe(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0xb25e271d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x5d71b85c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x3d0a8add(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x43223a97(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x9b76ad84(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0xfb0d9f05(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x48ee50ad(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x85635b3b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0xe51869ba(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_cmdl_0x5cea873f(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_head_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_jaw_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_ice_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_head_ice_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_jaw_ice_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_head_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_head_frozen_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shockwave(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_unknown_struct60(data: typing.BinaryIO, property_size: int):
    return UnknownStruct60.from_stream(data, property_size)


def _decode_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size)


def _decode_beam_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_orb_slot_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_foot_explosion(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_foot_explosion_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_wpsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_launch_projectile_data_0x7c9c3b51(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_hover_then_home_projectile_0x730fe427(data: typing.BinaryIO, property_size: int):
    return HoverThenHomeProjectile.from_stream(data, property_size)


def _decode_unknown_0x050924d3(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x6414e848(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2a7a2da7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_projectile_data_0x4392c34a(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_hover_then_home_projectile_0x868e4192(data: typing.BinaryIO, property_size: int):
    return HoverThenHomeProjectile.from_stream(data, property_size)


def _decode_hand_projectile_size(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0x153c001b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x473b730b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hand_projectile_damage_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_unknown_0x38786921(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_charge_player_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_launch_projectile_data_0x50ae6e55(data: typing.BinaryIO, property_size: int):
    return LaunchProjectileData.from_stream(data, property_size)


def _decode_hand_data(data: typing.BinaryIO, property_size: int):
    return SeedBoss1HandData.from_stream(data, property_size)


def _decode_unknown_0x3196b2e7(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x77d3b386(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_color_hyper_shockwave(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x7ce5c47c(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_color_hyper_quake(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_color_energized(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_min_taunt_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_taunt_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_seed_boss1_stage_0x45694db0(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Stage.from_stream(data, property_size)


def _decode_seed_boss1_stage_0x338c748d(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Stage.from_stream(data, property_size)


def _decode_seed_boss1_stage_0xa8ff9e59(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Stage.from_stream(data, property_size)


def _decode_seed_boss1_stage_0xde4606f7(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Stage.from_stream(data, property_size)


def _decode_shield_info(data: typing.BinaryIO, property_size: int):
    return SeedBoss1Shield.from_stream(data, property_size)


def _decode_foot_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x64588114(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_approach_player_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_approach_player_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_approach_player_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc2be328d(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_scannable_parameters(data: typing.BinaryIO, property_size: int):
    return ScannableParameters.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xd3ad55b6: ('unknown_0xd3ad55b6', _decode_unknown_0xd3ad55b6),
    0xb33eb533: ('foot_health', _decode_foot_health),
    0x26fa460b: ('foot_vulnerability', _decode_foot_vulnerability),
    0xad0de5ac: ('left_foot', _decode_left_foot),
    0xfc128c15: ('left_knee', _decode_left_knee),
    0x299b8d33: ('left_thigh', _decode_left_thigh),
    0xa5bb98a6: ('right_foot', _decode_right_foot),
    0xf4a4f11f: ('right_knee', _decode_right_knee),
    0xc946d250: ('right_thigh', _decode_right_thigh),
    0x50edae7f: ('cmdl_0x50edae7f', _decode_cmdl_0x50edae7f),
    0x30969cfe: ('cmdl_0x30969cfe', _decode_cmdl_0x30969cfe),
    0xb25e271d: ('cmdl_0xb25e271d', _decode_cmdl_0xb25e271d),
    0x5d71b85c: ('cmdl_0x5d71b85c', _decode_cmdl_0x5d71b85c),
    0x3d0a8add: ('cmdl_0x3d0a8add', _decode_cmdl_0x3d0a8add),
    0x43223a97: ('cmdl_0x43223a97', _decode_cmdl_0x43223a97),
    0x9b76ad84: ('cmdl_0x9b76ad84', _decode_cmdl_0x9b76ad84),
    0xfb0d9f05: ('cmdl_0xfb0d9f05', _decode_cmdl_0xfb0d9f05),
    0x48ee50ad: ('cmdl_0x48ee50ad', _decode_cmdl_0x48ee50ad),
    0x85635b3b: ('cmdl_0x85635b3b', _decode_cmdl_0x85635b3b),
    0xe51869ba: ('cmdl_0xe51869ba', _decode_cmdl_0xe51869ba),
    0x5cea873f: ('cmdl_0x5cea873f', _decode_cmdl_0x5cea873f),
    0xc288ae69: ('head_model', _decode_head_model),
    0xcdbd44e1: ('jaw_model', _decode_jaw_model),
    0x6ad6cbba: ('ice_model', _decode_ice_model),
    0x3ab79847: ('head_ice_model', _decode_head_ice_model),
    0x27b30d35: ('jaw_ice_model', _decode_jaw_ice_model),
    0xec37e2fa: ('head_vulnerability', _decode_head_vulnerability),
    0xccca3249: ('head_frozen_time', _decode_head_frozen_time),
    0x3ce6e482: ('shockwave', _decode_shockwave),
    0x72e00501: ('unknown_struct60', _decode_unknown_struct60),
    0x1598012a: ('beam_info', _decode_beam_info),
    0x98821996: ('beam_damage_info', _decode_beam_damage_info),
    0xdd34c3c0: ('orb_slot_vulnerability', _decode_orb_slot_vulnerability),
    0x547b9a9a: ('foot_explosion', _decode_foot_explosion),
    0xeaf93057: ('foot_explosion_sound', _decode_foot_explosion_sound),
    0x36c067c2: ('wpsc', _decode_wpsc),
    0x261eefe7: ('damage_info', _decode_damage_info),
    0x818f810b: ('shock_wave_info', _decode_shock_wave_info),
    0x7c9c3b51: ('launch_projectile_data_0x7c9c3b51', _decode_launch_projectile_data_0x7c9c3b51),
    0x730fe427: ('hover_then_home_projectile_0x730fe427', _decode_hover_then_home_projectile_0x730fe427),
    0x50924d3: ('unknown_0x050924d3', _decode_unknown_0x050924d3),
    0x6414e848: ('unknown_0x6414e848', _decode_unknown_0x6414e848),
    0x2a7a2da7: ('unknown_0x2a7a2da7', _decode_unknown_0x2a7a2da7),
    0x4392c34a: ('launch_projectile_data_0x4392c34a', _decode_launch_projectile_data_0x4392c34a),
    0x868e4192: ('hover_then_home_projectile_0x868e4192', _decode_hover_then_home_projectile_0x868e4192),
    0xc8e16555: ('hand_projectile_size', _decode_hand_projectile_size),
    0x153c001b: ('unknown_0x153c001b', _decode_unknown_0x153c001b),
    0x473b730b: ('unknown_0x473b730b', _decode_unknown_0x473b730b),
    0xaea60f24: ('hand_projectile_damage_effect', _decode_hand_projectile_damage_effect),
    0x38786921: ('unknown_0x38786921', _decode_unknown_0x38786921),
    0x9e63065f: ('charge_player_damage', _decode_charge_player_damage),
    0x50ae6e55: ('launch_projectile_data_0x50ae6e55', _decode_launch_projectile_data_0x50ae6e55),
    0xc69f691a: ('hand_data', _decode_hand_data),
    0x3196b2e7: ('unknown_0x3196b2e7', _decode_unknown_0x3196b2e7),
    0x77d3b386: ('unknown_0x77d3b386', _decode_unknown_0x77d3b386),
    0xa9be1081: ('color_hyper_shockwave', _decode_color_hyper_shockwave),
    0x7ce5c47c: ('unknown_0x7ce5c47c', _decode_unknown_0x7ce5c47c),
    0xf9656c39: ('color_hyper_quake', _decode_color_hyper_quake),
    0xd7142afe: ('color_energized', _decode_color_energized),
    0xc3718ea0: ('min_taunt_time', _decode_min_taunt_time),
    0xd6fa5a52: ('max_taunt_time', _decode_max_taunt_time),
    0x45694db0: ('seed_boss1_stage_0x45694db0', _decode_seed_boss1_stage_0x45694db0),
    0x338c748d: ('seed_boss1_stage_0x338c748d', _decode_seed_boss1_stage_0x338c748d),
    0xa8ff9e59: ('seed_boss1_stage_0xa8ff9e59', _decode_seed_boss1_stage_0xa8ff9e59),
    0xde4606f7: ('seed_boss1_stage_0xde4606f7', _decode_seed_boss1_stage_0xde4606f7),
    0x2883f972: ('shield_info', _decode_shield_info),
    0x40ac1fd4: ('foot_contact_damage', _decode_foot_contact_damage),
    0x64588114: ('unknown_0x64588114', _decode_unknown_0x64588114),
    0x712d3274: ('approach_player_distance', _decode_approach_player_distance),
    0x50ec86c1: ('approach_player_delay', _decode_approach_player_delay),
    0x536b7493: ('approach_player_time', _decode_approach_player_time),
    0xc2be328d: ('unknown_0xc2be328d', _decode_unknown_0xc2be328d),
    0x22fdca5: ('scannable_parameters', _decode_scannable_parameters),
}
