# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EchoParameters import EchoParameters
from retro_data_structures.properties.echoes.archetypes.ShockWaveInfo import ShockWaveInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class DigitalGuardianData(BaseProperty):
    scannable_info_crippled: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    unknown_0x0faf6a8e: float = dataclasses.field(default=10.0)
    unknown_0xd3056808: float = dataclasses.field(default=17.0)
    unknown_0x304b47ee: float = dataclasses.field(default=5.0)
    leg_stab_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xb4561f28: float = dataclasses.field(default=75.0)
    toe_target_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    part_0x783635a6: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_toe_target: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_toe_target_attack: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_toe_target_explosion: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_toe_target_hit: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_shock_wave: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    vortex_attack_duration: float = dataclasses.field(default=5.0)
    vortex_attraction_force: float = dataclasses.field(default=50.0)
    unknown_0x348bff02: float = dataclasses.field(default=30.0)
    vortex_linear_velocity: float = dataclasses.field(default=20.0)
    vortex_linear_acceleration: float = dataclasses.field(default=20.0)
    vortex_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xfb5263e8: int = dataclasses.field(default=0)
    unknown_0x6aaf33e3: int = dataclasses.field(default=8191)
    unknown_0x4f5d725c: float = dataclasses.field(default=100.0)
    sound_vortex_flash: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    leg_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    shin_armor: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    unknown_0xe3dd61e6: float = dataclasses.field(default=100.0)
    sound_knee_armor_hit: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_knee_vulnerable: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    knee_armor: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    echo_parameters_0x7b5b7312: EchoParameters = dataclasses.field(default_factory=EchoParameters)
    unknown_0xa324e26c: float = dataclasses.field(default=2.0)
    unknown_0x6a754ebd: float = dataclasses.field(default=5.0)
    jump_timer: float = dataclasses.field(default=10.0)
    unknown_0x8106cda9: float = dataclasses.field(default=0.699999988079071)
    unknown_0x9e1b8105: float = dataclasses.field(default=0.699999988079071)
    unknown_0xa08fcc70: float = dataclasses.field(default=0.699999988079071)
    unknown_0x3254a16b: float = dataclasses.field(default=1.0)
    transmission_beacon: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    part_0x3fa7df1c: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    echo_parameters_0x021b6f9d: EchoParameters = dataclasses.field(default_factory=EchoParameters)
    sound_transmission_beacon: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_beacon_retract: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    unknown_0x4f6d27d3: float = dataclasses.field(default=500.0)
    part_0x71f0c674: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xc8ec315b: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_beacon_explode: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_beacon_hit: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    knee_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    vortex_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    toe_target_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x004')  # 52 properties

        data.write(b'*\xa6?\xc4')  # 0x2aa63fc4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scannable_info_crippled))

        data.write(b'\x0f\xafj\x8e')  # 0xfaf6a8e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0faf6a8e))

        data.write(b'\xd3\x05h\x08')  # 0xd3056808
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd3056808))

        data.write(b'0KG\xee')  # 0x304b47ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x304b47ee))

        data.write(b'\xef\xac\xfaP')  # 0xefacfa50
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.leg_stab_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 50.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4V\x1f(')  # 0xb4561f28
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb4561f28))

        data.write(b'\xbb\x06\xdd\x83')  # 0xbb06dd83
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.toe_target_model))

        data.write(b'x65\xa6')  # 0x783635a6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x783635a6))

        data.write(b'\x13\x84Zf')  # 0x13845a66
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_toe_target.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3\x05\xdc\xba')  # 0xa305dcba
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_toe_target_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\xec\x160')  # 0xc6ec1630
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_toe_target_explosion.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98A\x9e\xac')  # 0x98419eac
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_toe_target_hit.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\x91\xc9\xab')  # 0x4691c9ab
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_shock_wave.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8fG\x87\xcb')  # 0x8f4787cb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'vR~\x01')  # 0x76527e01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vortex_attack_duration))

        data.write(b'\xd2\x10\xdf\xdb')  # 0xd210dfdb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vortex_attraction_force))

        data.write(b'4\x8b\xff\x02')  # 0x348bff02
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x348bff02))

        data.write(b'\x84\xfe\xf1o')  # 0x84fef16f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vortex_linear_velocity))

        data.write(b'\x93\xa7JF')  # 0x93a74a46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vortex_linear_acceleration))

        data.write(b'\\\xa6\x12\xaa')  # 0x5ca612aa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vortex_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 50.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfbRc\xe8')  # 0xfb5263e8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xfb5263e8))

        data.write(b'j\xaf3\xe3')  # 0x6aaf33e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6aaf33e3))

        data.write(b'O]r\\')  # 0x4f5d725c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4f5d725c))

        data.write(b'{\xfa\xb4 ')  # 0x7bfab420
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_vortex_flash.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0\xa8d\x88')  # 0xc0a86488
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.leg_model))

        data.write(b'\x8d\xdd\x85\xca')  # 0x8ddd85ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shin_armor))

        data.write(b'\xe3\xdda\xe6')  # 0xe3dd61e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe3dd61e6))

        data.write(b'\x91\xd2\xa0B')  # 0x91d2a042
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_knee_armor_hit.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93\x86\xd2+')  # 0x9386d22b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_knee_vulnerable.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'^\xf8\xb2\x88')  # 0x5ef8b288
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.knee_armor))

        data.write(b'{[s\x12')  # 0x7b5b7312
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.echo_parameters_0x7b5b7312.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3$\xe2l')  # 0xa324e26c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa324e26c))

        data.write(b'juN\xbd')  # 0x6a754ebd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6a754ebd))

        data.write(b'\xc9\xfc\x99w')  # 0xc9fc9977
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_timer))

        data.write(b'\x81\x06\xcd\xa9')  # 0x8106cda9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8106cda9))

        data.write(b'\x9e\x1b\x81\x05')  # 0x9e1b8105
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9e1b8105))

        data.write(b'\xa0\x8f\xccp')  # 0xa08fcc70
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa08fcc70))

        data.write(b'2T\xa1k')  # 0x3254a16b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3254a16b))

        data.write(b'W\x96\xa1C')  # 0x5796a143
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.transmission_beacon))

        data.write(b'?\xa7\xdf\x1c')  # 0x3fa7df1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x3fa7df1c))

        data.write(b'\x02\x1bo\x9d')  # 0x21b6f9d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.echo_parameters_0x021b6f9d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'U\xa8\x01\x1c')  # 0x55a8011c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_transmission_beacon.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'z\xe7?\xb3')  # 0x7ae73fb3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa9\xe5\\\x8e')  # 0xa9e55c8e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_beacon_retract.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"Om'\xd3")  # 0x4f6d27d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4f6d27d3))

        data.write(b'q\xf0\xc6t')  # 0x71f0c674
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x71f0c674))

        data.write(b'\xc8\xec1[')  # 0xc8ec315b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xc8ec315b))

        data.write(b'\xee\xd5\xb9\x90')  # 0xeed5b990
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_beacon_explode.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'S_o\xec')  # 0x535f6fec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_beacon_hit.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'm\xba\xd23')  # 0x6dbad233
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.knee_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1%\x9e:')  # 0xf1259e3a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.vortex_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf1O27')  # 0xf14f3237
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.toe_target_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            scannable_info_crippled=data['scannable_info_crippled'],
            unknown_0x0faf6a8e=data['unknown_0x0faf6a8e'],
            unknown_0xd3056808=data['unknown_0xd3056808'],
            unknown_0x304b47ee=data['unknown_0x304b47ee'],
            leg_stab_damage=DamageInfo.from_json(data['leg_stab_damage']),
            unknown_0xb4561f28=data['unknown_0xb4561f28'],
            toe_target_model=data['toe_target_model'],
            part_0x783635a6=data['part_0x783635a6'],
            sound_toe_target=AudioPlaybackParms.from_json(data['sound_toe_target']),
            sound_toe_target_attack=AudioPlaybackParms.from_json(data['sound_toe_target_attack']),
            sound_toe_target_explosion=AudioPlaybackParms.from_json(data['sound_toe_target_explosion']),
            sound_toe_target_hit=AudioPlaybackParms.from_json(data['sound_toe_target_hit']),
            sound_shock_wave=AudioPlaybackParms.from_json(data['sound_shock_wave']),
            shock_wave_info=ShockWaveInfo.from_json(data['shock_wave_info']),
            vortex_attack_duration=data['vortex_attack_duration'],
            vortex_attraction_force=data['vortex_attraction_force'],
            unknown_0x348bff02=data['unknown_0x348bff02'],
            vortex_linear_velocity=data['vortex_linear_velocity'],
            vortex_linear_acceleration=data['vortex_linear_acceleration'],
            vortex_damage=DamageInfo.from_json(data['vortex_damage']),
            unknown_0xfb5263e8=data['unknown_0xfb5263e8'],
            unknown_0x6aaf33e3=data['unknown_0x6aaf33e3'],
            unknown_0x4f5d725c=data['unknown_0x4f5d725c'],
            sound_vortex_flash=AudioPlaybackParms.from_json(data['sound_vortex_flash']),
            leg_model=data['leg_model'],
            shin_armor=data['shin_armor'],
            unknown_0xe3dd61e6=data['unknown_0xe3dd61e6'],
            sound_knee_armor_hit=AudioPlaybackParms.from_json(data['sound_knee_armor_hit']),
            sound_knee_vulnerable=AudioPlaybackParms.from_json(data['sound_knee_vulnerable']),
            knee_armor=data['knee_armor'],
            echo_parameters_0x7b5b7312=EchoParameters.from_json(data['echo_parameters_0x7b5b7312']),
            unknown_0xa324e26c=data['unknown_0xa324e26c'],
            unknown_0x6a754ebd=data['unknown_0x6a754ebd'],
            jump_timer=data['jump_timer'],
            unknown_0x8106cda9=data['unknown_0x8106cda9'],
            unknown_0x9e1b8105=data['unknown_0x9e1b8105'],
            unknown_0xa08fcc70=data['unknown_0xa08fcc70'],
            unknown_0x3254a16b=data['unknown_0x3254a16b'],
            transmission_beacon=data['transmission_beacon'],
            part_0x3fa7df1c=data['part_0x3fa7df1c'],
            echo_parameters_0x021b6f9d=EchoParameters.from_json(data['echo_parameters_0x021b6f9d']),
            sound_transmission_beacon=AudioPlaybackParms.from_json(data['sound_transmission_beacon']),
            audio_playback_parms=AudioPlaybackParms.from_json(data['audio_playback_parms']),
            sound_beacon_retract=AudioPlaybackParms.from_json(data['sound_beacon_retract']),
            unknown_0x4f6d27d3=data['unknown_0x4f6d27d3'],
            part_0x71f0c674=data['part_0x71f0c674'],
            part_0xc8ec315b=data['part_0xc8ec315b'],
            sound_beacon_explode=AudioPlaybackParms.from_json(data['sound_beacon_explode']),
            sound_beacon_hit=AudioPlaybackParms.from_json(data['sound_beacon_hit']),
            knee_vulnerability=DamageVulnerability.from_json(data['knee_vulnerability']),
            vortex_vulnerability=DamageVulnerability.from_json(data['vortex_vulnerability']),
            toe_target_vulnerability=DamageVulnerability.from_json(data['toe_target_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'scannable_info_crippled': self.scannable_info_crippled,
            'unknown_0x0faf6a8e': self.unknown_0x0faf6a8e,
            'unknown_0xd3056808': self.unknown_0xd3056808,
            'unknown_0x304b47ee': self.unknown_0x304b47ee,
            'leg_stab_damage': self.leg_stab_damage.to_json(),
            'unknown_0xb4561f28': self.unknown_0xb4561f28,
            'toe_target_model': self.toe_target_model,
            'part_0x783635a6': self.part_0x783635a6,
            'sound_toe_target': self.sound_toe_target.to_json(),
            'sound_toe_target_attack': self.sound_toe_target_attack.to_json(),
            'sound_toe_target_explosion': self.sound_toe_target_explosion.to_json(),
            'sound_toe_target_hit': self.sound_toe_target_hit.to_json(),
            'sound_shock_wave': self.sound_shock_wave.to_json(),
            'shock_wave_info': self.shock_wave_info.to_json(),
            'vortex_attack_duration': self.vortex_attack_duration,
            'vortex_attraction_force': self.vortex_attraction_force,
            'unknown_0x348bff02': self.unknown_0x348bff02,
            'vortex_linear_velocity': self.vortex_linear_velocity,
            'vortex_linear_acceleration': self.vortex_linear_acceleration,
            'vortex_damage': self.vortex_damage.to_json(),
            'unknown_0xfb5263e8': self.unknown_0xfb5263e8,
            'unknown_0x6aaf33e3': self.unknown_0x6aaf33e3,
            'unknown_0x4f5d725c': self.unknown_0x4f5d725c,
            'sound_vortex_flash': self.sound_vortex_flash.to_json(),
            'leg_model': self.leg_model,
            'shin_armor': self.shin_armor,
            'unknown_0xe3dd61e6': self.unknown_0xe3dd61e6,
            'sound_knee_armor_hit': self.sound_knee_armor_hit.to_json(),
            'sound_knee_vulnerable': self.sound_knee_vulnerable.to_json(),
            'knee_armor': self.knee_armor,
            'echo_parameters_0x7b5b7312': self.echo_parameters_0x7b5b7312.to_json(),
            'unknown_0xa324e26c': self.unknown_0xa324e26c,
            'unknown_0x6a754ebd': self.unknown_0x6a754ebd,
            'jump_timer': self.jump_timer,
            'unknown_0x8106cda9': self.unknown_0x8106cda9,
            'unknown_0x9e1b8105': self.unknown_0x9e1b8105,
            'unknown_0xa08fcc70': self.unknown_0xa08fcc70,
            'unknown_0x3254a16b': self.unknown_0x3254a16b,
            'transmission_beacon': self.transmission_beacon,
            'part_0x3fa7df1c': self.part_0x3fa7df1c,
            'echo_parameters_0x021b6f9d': self.echo_parameters_0x021b6f9d.to_json(),
            'sound_transmission_beacon': self.sound_transmission_beacon.to_json(),
            'audio_playback_parms': self.audio_playback_parms.to_json(),
            'sound_beacon_retract': self.sound_beacon_retract.to_json(),
            'unknown_0x4f6d27d3': self.unknown_0x4f6d27d3,
            'part_0x71f0c674': self.part_0x71f0c674,
            'part_0xc8ec315b': self.part_0xc8ec315b,
            'sound_beacon_explode': self.sound_beacon_explode.to_json(),
            'sound_beacon_hit': self.sound_beacon_hit.to_json(),
            'knee_vulnerability': self.knee_vulnerability.to_json(),
            'vortex_vulnerability': self.vortex_vulnerability.to_json(),
            'toe_target_vulnerability': self.toe_target_vulnerability.to_json(),
        }

    def _dependencies_for_scannable_info_crippled(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scannable_info_crippled)

    def _dependencies_for_leg_stab_damage(self, asset_manager):
        yield from self.leg_stab_damage.dependencies_for(asset_manager)

    def _dependencies_for_toe_target_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.toe_target_model)

    def _dependencies_for_part_0x783635a6(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x783635a6)

    def _dependencies_for_sound_toe_target(self, asset_manager):
        yield from self.sound_toe_target.dependencies_for(asset_manager)

    def _dependencies_for_sound_toe_target_attack(self, asset_manager):
        yield from self.sound_toe_target_attack.dependencies_for(asset_manager)

    def _dependencies_for_sound_toe_target_explosion(self, asset_manager):
        yield from self.sound_toe_target_explosion.dependencies_for(asset_manager)

    def _dependencies_for_sound_toe_target_hit(self, asset_manager):
        yield from self.sound_toe_target_hit.dependencies_for(asset_manager)

    def _dependencies_for_sound_shock_wave(self, asset_manager):
        yield from self.sound_shock_wave.dependencies_for(asset_manager)

    def _dependencies_for_shock_wave_info(self, asset_manager):
        yield from self.shock_wave_info.dependencies_for(asset_manager)

    def _dependencies_for_vortex_damage(self, asset_manager):
        yield from self.vortex_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_vortex_flash(self, asset_manager):
        yield from self.sound_vortex_flash.dependencies_for(asset_manager)

    def _dependencies_for_leg_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.leg_model)

    def _dependencies_for_shin_armor(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shin_armor)

    def _dependencies_for_sound_knee_armor_hit(self, asset_manager):
        yield from self.sound_knee_armor_hit.dependencies_for(asset_manager)

    def _dependencies_for_sound_knee_vulnerable(self, asset_manager):
        yield from self.sound_knee_vulnerable.dependencies_for(asset_manager)

    def _dependencies_for_knee_armor(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.knee_armor)

    def _dependencies_for_echo_parameters_0x7b5b7312(self, asset_manager):
        yield from self.echo_parameters_0x7b5b7312.dependencies_for(asset_manager)

    def _dependencies_for_transmission_beacon(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.transmission_beacon)

    def _dependencies_for_part_0x3fa7df1c(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x3fa7df1c)

    def _dependencies_for_echo_parameters_0x021b6f9d(self, asset_manager):
        yield from self.echo_parameters_0x021b6f9d.dependencies_for(asset_manager)

    def _dependencies_for_sound_transmission_beacon(self, asset_manager):
        yield from self.sound_transmission_beacon.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms(self, asset_manager):
        yield from self.audio_playback_parms.dependencies_for(asset_manager)

    def _dependencies_for_sound_beacon_retract(self, asset_manager):
        yield from self.sound_beacon_retract.dependencies_for(asset_manager)

    def _dependencies_for_part_0x71f0c674(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x71f0c674)

    def _dependencies_for_part_0xc8ec315b(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xc8ec315b)

    def _dependencies_for_sound_beacon_explode(self, asset_manager):
        yield from self.sound_beacon_explode.dependencies_for(asset_manager)

    def _dependencies_for_sound_beacon_hit(self, asset_manager):
        yield from self.sound_beacon_hit.dependencies_for(asset_manager)

    def _dependencies_for_knee_vulnerability(self, asset_manager):
        yield from self.knee_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_vortex_vulnerability(self, asset_manager):
        yield from self.vortex_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_toe_target_vulnerability(self, asset_manager):
        yield from self.toe_target_vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_scannable_info_crippled, "scannable_info_crippled", "AssetId"),
            (self._dependencies_for_leg_stab_damage, "leg_stab_damage", "DamageInfo"),
            (self._dependencies_for_toe_target_model, "toe_target_model", "AssetId"),
            (self._dependencies_for_part_0x783635a6, "part_0x783635a6", "AssetId"),
            (self._dependencies_for_sound_toe_target, "sound_toe_target", "AudioPlaybackParms"),
            (self._dependencies_for_sound_toe_target_attack, "sound_toe_target_attack", "AudioPlaybackParms"),
            (self._dependencies_for_sound_toe_target_explosion, "sound_toe_target_explosion", "AudioPlaybackParms"),
            (self._dependencies_for_sound_toe_target_hit, "sound_toe_target_hit", "AudioPlaybackParms"),
            (self._dependencies_for_sound_shock_wave, "sound_shock_wave", "AudioPlaybackParms"),
            (self._dependencies_for_shock_wave_info, "shock_wave_info", "ShockWaveInfo"),
            (self._dependencies_for_vortex_damage, "vortex_damage", "DamageInfo"),
            (self._dependencies_for_sound_vortex_flash, "sound_vortex_flash", "AudioPlaybackParms"),
            (self._dependencies_for_leg_model, "leg_model", "AssetId"),
            (self._dependencies_for_shin_armor, "shin_armor", "AssetId"),
            (self._dependencies_for_sound_knee_armor_hit, "sound_knee_armor_hit", "AudioPlaybackParms"),
            (self._dependencies_for_sound_knee_vulnerable, "sound_knee_vulnerable", "AudioPlaybackParms"),
            (self._dependencies_for_knee_armor, "knee_armor", "AssetId"),
            (self._dependencies_for_echo_parameters_0x7b5b7312, "echo_parameters_0x7b5b7312", "EchoParameters"),
            (self._dependencies_for_transmission_beacon, "transmission_beacon", "AssetId"),
            (self._dependencies_for_part_0x3fa7df1c, "part_0x3fa7df1c", "AssetId"),
            (self._dependencies_for_echo_parameters_0x021b6f9d, "echo_parameters_0x021b6f9d", "EchoParameters"),
            (self._dependencies_for_sound_transmission_beacon, "sound_transmission_beacon", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms, "audio_playback_parms", "AudioPlaybackParms"),
            (self._dependencies_for_sound_beacon_retract, "sound_beacon_retract", "AudioPlaybackParms"),
            (self._dependencies_for_part_0x71f0c674, "part_0x71f0c674", "AssetId"),
            (self._dependencies_for_part_0xc8ec315b, "part_0xc8ec315b", "AssetId"),
            (self._dependencies_for_sound_beacon_explode, "sound_beacon_explode", "AudioPlaybackParms"),
            (self._dependencies_for_sound_beacon_hit, "sound_beacon_hit", "AudioPlaybackParms"),
            (self._dependencies_for_knee_vulnerability, "knee_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_vortex_vulnerability, "vortex_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_toe_target_vulnerability, "toe_target_vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DigitalGuardianData.{field_name} ({field_type}): {e}"
                )


def _decode_scannable_info_crippled(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x0faf6a8e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd3056808(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x304b47ee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_leg_stab_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 50.0, 'di_knock_back_power': 10.0})


def _decode_unknown_0xb4561f28(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_toe_target_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x783635a6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_toe_target(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_toe_target_attack(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_toe_target_explosion(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_toe_target_hit(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_shock_wave(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_vortex_attack_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vortex_attraction_force(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x348bff02(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vortex_linear_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vortex_linear_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vortex_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 50.0, 'di_knock_back_power': 10.0})


def _decode_unknown_0xfb5263e8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6aaf33e3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x4f5d725c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_vortex_flash(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_leg_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shin_armor(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0xe3dd61e6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_knee_armor_hit(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_knee_vulnerable(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_knee_armor(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_echo_parameters_0x7b5b7312(data: typing.BinaryIO, property_size: int):
    return EchoParameters.from_stream(data, property_size)


def _decode_unknown_0xa324e26c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6a754ebd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8106cda9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x9e1b8105(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa08fcc70(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3254a16b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_transmission_beacon(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x3fa7df1c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_echo_parameters_0x021b6f9d(data: typing.BinaryIO, property_size: int):
    return EchoParameters.from_stream(data, property_size)


def _decode_sound_transmission_beacon(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_beacon_retract(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_unknown_0x4f6d27d3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part_0x71f0c674(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0xc8ec315b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_beacon_explode(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_beacon_hit(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_knee_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_vortex_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_toe_target_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x2aa63fc4: ('scannable_info_crippled', _decode_scannable_info_crippled),
    0xfaf6a8e: ('unknown_0x0faf6a8e', _decode_unknown_0x0faf6a8e),
    0xd3056808: ('unknown_0xd3056808', _decode_unknown_0xd3056808),
    0x304b47ee: ('unknown_0x304b47ee', _decode_unknown_0x304b47ee),
    0xefacfa50: ('leg_stab_damage', _decode_leg_stab_damage),
    0xb4561f28: ('unknown_0xb4561f28', _decode_unknown_0xb4561f28),
    0xbb06dd83: ('toe_target_model', _decode_toe_target_model),
    0x783635a6: ('part_0x783635a6', _decode_part_0x783635a6),
    0x13845a66: ('sound_toe_target', _decode_sound_toe_target),
    0xa305dcba: ('sound_toe_target_attack', _decode_sound_toe_target_attack),
    0xc6ec1630: ('sound_toe_target_explosion', _decode_sound_toe_target_explosion),
    0x98419eac: ('sound_toe_target_hit', _decode_sound_toe_target_hit),
    0x4691c9ab: ('sound_shock_wave', _decode_sound_shock_wave),
    0x8f4787cb: ('shock_wave_info', _decode_shock_wave_info),
    0x76527e01: ('vortex_attack_duration', _decode_vortex_attack_duration),
    0xd210dfdb: ('vortex_attraction_force', _decode_vortex_attraction_force),
    0x348bff02: ('unknown_0x348bff02', _decode_unknown_0x348bff02),
    0x84fef16f: ('vortex_linear_velocity', _decode_vortex_linear_velocity),
    0x93a74a46: ('vortex_linear_acceleration', _decode_vortex_linear_acceleration),
    0x5ca612aa: ('vortex_damage', _decode_vortex_damage),
    0xfb5263e8: ('unknown_0xfb5263e8', _decode_unknown_0xfb5263e8),
    0x6aaf33e3: ('unknown_0x6aaf33e3', _decode_unknown_0x6aaf33e3),
    0x4f5d725c: ('unknown_0x4f5d725c', _decode_unknown_0x4f5d725c),
    0x7bfab420: ('sound_vortex_flash', _decode_sound_vortex_flash),
    0xc0a86488: ('leg_model', _decode_leg_model),
    0x8ddd85ca: ('shin_armor', _decode_shin_armor),
    0xe3dd61e6: ('unknown_0xe3dd61e6', _decode_unknown_0xe3dd61e6),
    0x91d2a042: ('sound_knee_armor_hit', _decode_sound_knee_armor_hit),
    0x9386d22b: ('sound_knee_vulnerable', _decode_sound_knee_vulnerable),
    0x5ef8b288: ('knee_armor', _decode_knee_armor),
    0x7b5b7312: ('echo_parameters_0x7b5b7312', _decode_echo_parameters_0x7b5b7312),
    0xa324e26c: ('unknown_0xa324e26c', _decode_unknown_0xa324e26c),
    0x6a754ebd: ('unknown_0x6a754ebd', _decode_unknown_0x6a754ebd),
    0xc9fc9977: ('jump_timer', _decode_jump_timer),
    0x8106cda9: ('unknown_0x8106cda9', _decode_unknown_0x8106cda9),
    0x9e1b8105: ('unknown_0x9e1b8105', _decode_unknown_0x9e1b8105),
    0xa08fcc70: ('unknown_0xa08fcc70', _decode_unknown_0xa08fcc70),
    0x3254a16b: ('unknown_0x3254a16b', _decode_unknown_0x3254a16b),
    0x5796a143: ('transmission_beacon', _decode_transmission_beacon),
    0x3fa7df1c: ('part_0x3fa7df1c', _decode_part_0x3fa7df1c),
    0x21b6f9d: ('echo_parameters_0x021b6f9d', _decode_echo_parameters_0x021b6f9d),
    0x55a8011c: ('sound_transmission_beacon', _decode_sound_transmission_beacon),
    0x7ae73fb3: ('audio_playback_parms', _decode_audio_playback_parms),
    0xa9e55c8e: ('sound_beacon_retract', _decode_sound_beacon_retract),
    0x4f6d27d3: ('unknown_0x4f6d27d3', _decode_unknown_0x4f6d27d3),
    0x71f0c674: ('part_0x71f0c674', _decode_part_0x71f0c674),
    0xc8ec315b: ('part_0xc8ec315b', _decode_part_0xc8ec315b),
    0xeed5b990: ('sound_beacon_explode', _decode_sound_beacon_explode),
    0x535f6fec: ('sound_beacon_hit', _decode_sound_beacon_hit),
    0x6dbad233: ('knee_vulnerability', _decode_knee_vulnerability),
    0xf1259e3a: ('vortex_vulnerability', _decode_vortex_vulnerability),
    0xf14f3237: ('toe_target_vulnerability', _decode_toe_target_vulnerability),
}
