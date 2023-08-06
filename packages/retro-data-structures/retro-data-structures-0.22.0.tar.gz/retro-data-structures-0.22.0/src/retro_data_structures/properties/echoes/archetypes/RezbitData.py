# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class RezbitData(BaseProperty):
    hearing_radius: float = dataclasses.field(default=20.0)
    unknown_0x4a6c4b40: float = dataclasses.field(default=20.0)
    unknown_0x30d11671: float = dataclasses.field(default=10.0)
    model_no_holos: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    skin_no_holos: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    shield_down_time: float = dataclasses.field(default=3.0)
    unknown_0xffb37b81: float = dataclasses.field(default=2.0)
    shield_up_time: float = dataclasses.field(default=3.0)
    unknown_0x0d1d1648: float = dataclasses.field(default=1.0)
    shield_explode_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_shield_explode: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_shield_on: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_shield_off: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    sound_flinch: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    unknown_0xad120ad7: float = dataclasses.field(default=12.0)
    unknown_0xe70ef8a3: float = dataclasses.field(default=1.2000000476837158)
    audio_playback_parms: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    unknown_0x70e597d4: float = dataclasses.field(default=2.0)
    unknown_0x94980a67: float = dataclasses.field(default=100.0)
    unknown_0xd02f08b0: float = dataclasses.field(default=2.0)
    unknown_0x53e84718: float = dataclasses.field(default=100.0)
    unknown_0x6fbc1bf9: float = dataclasses.field(default=4.0)
    energy_bolt_chance: float = dataclasses.field(default=50.0)
    cutting_laser_chance: float = dataclasses.field(default=50.0)
    unknown_0x075491ca: float = dataclasses.field(default=20.0)
    unknown_0x54f2892e: float = dataclasses.field(default=40.0)
    energy_bolt_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    energy_bolt_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    energy_bolt_attack_duration: float = dataclasses.field(default=4.0)
    unknown_0x28944183: float = dataclasses.field(default=2.0)
    unknown_0xc7a69a59: float = dataclasses.field(default=0.5)
    sound_energy_bolt: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    unknown_0x9ede657f: float = dataclasses.field(default=0.0)
    unknown_0xcd787d9b: float = dataclasses.field(default=30.0)
    virus_attack_time: float = dataclasses.field(default=6.0)
    virus_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_always_ff: int = dataclasses.field(default=0)
    sound_0xbb3f8a7b: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x601f846d: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x64c7990d: float = dataclasses.field(default=20.0)
    unknown_0x376181e9: float = dataclasses.field(default=40.0)
    cutting_laser_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_cutting_laser: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    cutting_laser_beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    shield_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x00-')  # 45 properties

        data.write(b'\xediH\x8f')  # 0xed69488f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hearing_radius))

        data.write(b'JlK@')  # 0x4a6c4b40
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4a6c4b40))

        data.write(b'0\xd1\x16q')  # 0x30d11671
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x30d11671))

        data.write(b'\xc8\x0b\xb6\xe4')  # 0xc80bb6e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.model_no_holos))

        data.write(b'\x05Hc\x19')  # 0x5486319
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.skin_no_holos))

        data.write(b'\x89\x80\xa4i')  # 0x8980a469
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shield_down_time))

        data.write(b'\xff\xb3{\x81')  # 0xffb37b81
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xffb37b81))

        data.write(b'D\x85y\xcd')  # 0x448579cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shield_up_time))

        data.write(b'\r\x1d\x16H')  # 0xd1d1648
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0d1d1648))

        data.write(b'\xa4\x1fu\xef')  # 0xa41f75ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shield_explode_effect))

        data.write(b'\xa3N-\x84')  # 0xa34e2d84
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_shield_explode.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8cY\x8eA')  # 0x8c598e41
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_shield_on.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4I\x1e\xd5')  # 0xf4491ed5
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_shield_off.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'}\x83!X')  # 0x7d832158
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_flinch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xad\x12\n\xd7')  # 0xad120ad7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xad120ad7))

        data.write(b'\xe7\x0e\xf8\xa3')  # 0xe70ef8a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe70ef8a3))

        data.write(b'k\xf2\xff`')  # 0x6bf2ff60
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'p\xe5\x97\xd4')  # 0x70e597d4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x70e597d4))

        data.write(b'\x94\x98\ng')  # 0x94980a67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x94980a67))

        data.write(b'\xd0/\x08\xb0')  # 0xd02f08b0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd02f08b0))

        data.write(b'S\xe8G\x18')  # 0x53e84718
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x53e84718))

        data.write(b'o\xbc\x1b\xf9')  # 0x6fbc1bf9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6fbc1bf9))

        data.write(b"\xdc'`\x15")  # 0xdc276015
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.energy_bolt_chance))

        data.write(b',\xa3\xe9\xcd')  # 0x2ca3e9cd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cutting_laser_chance))

        data.write(b'\x07T\x91\xca')  # 0x75491ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x075491ca))

        data.write(b'T\xf2\x89.')  # 0x54f2892e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x54f2892e))

        data.write(b'`\x0c_@')  # 0x600c5f40
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.energy_bolt_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'/\x11\tK')  # 0x2f11094b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.energy_bolt_projectile))

        data.write(b'\xa1\xf3P\xf5')  # 0xa1f350f5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.energy_bolt_attack_duration))

        data.write(b'(\x94A\x83')  # 0x28944183
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x28944183))

        data.write(b'\xc7\xa6\x9aY')  # 0xc7a69a59
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc7a69a59))

        data.write(b'\xbd>\xb0\x01')  # 0xbd3eb001
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_energy_bolt.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9e\xdee\x7f')  # 0x9ede657f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9ede657f))

        data.write(b'\xcdx}\x9b')  # 0xcd787d9b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcd787d9b))

        data.write(b'J};\x04')  # 0x4a7d3b04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.virus_attack_time))

        data.write(b'\x16\x86\x9bW')  # 0x16869b57
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.virus_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97=|\xc3')  # 0x973d7cc3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_always_ff))

        data.write(b'\xbb?\x8a{')  # 0xbb3f8a7b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xbb3f8a7b))

        data.write(b'`\x1f\x84m')  # 0x601f846d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x601f846d))

        data.write(b'd\xc7\x99\r')  # 0x64c7990d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x64c7990d))

        data.write(b'7a\x81\xe9')  # 0x376181e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x376181e9))

        data.write(b'\xbbX\xc0\x88')  # 0xbb58c088
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cutting_laser_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'xd\xca2')  # 0x7864ca32
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sound_cutting_laser.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'YvM\xbb')  # 0x59764dbb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cutting_laser_beam_info.to_stream(data, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd3O\x13#')  # 0xd34f1323
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.shield_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            hearing_radius=data['hearing_radius'],
            unknown_0x4a6c4b40=data['unknown_0x4a6c4b40'],
            unknown_0x30d11671=data['unknown_0x30d11671'],
            model_no_holos=data['model_no_holos'],
            skin_no_holos=data['skin_no_holos'],
            shield_down_time=data['shield_down_time'],
            unknown_0xffb37b81=data['unknown_0xffb37b81'],
            shield_up_time=data['shield_up_time'],
            unknown_0x0d1d1648=data['unknown_0x0d1d1648'],
            shield_explode_effect=data['shield_explode_effect'],
            sound_shield_explode=AudioPlaybackParms.from_json(data['sound_shield_explode']),
            sound_shield_on=AudioPlaybackParms.from_json(data['sound_shield_on']),
            sound_shield_off=AudioPlaybackParms.from_json(data['sound_shield_off']),
            sound_flinch=AudioPlaybackParms.from_json(data['sound_flinch']),
            unknown_0xad120ad7=data['unknown_0xad120ad7'],
            unknown_0xe70ef8a3=data['unknown_0xe70ef8a3'],
            audio_playback_parms=AudioPlaybackParms.from_json(data['audio_playback_parms']),
            unknown_0x70e597d4=data['unknown_0x70e597d4'],
            unknown_0x94980a67=data['unknown_0x94980a67'],
            unknown_0xd02f08b0=data['unknown_0xd02f08b0'],
            unknown_0x53e84718=data['unknown_0x53e84718'],
            unknown_0x6fbc1bf9=data['unknown_0x6fbc1bf9'],
            energy_bolt_chance=data['energy_bolt_chance'],
            cutting_laser_chance=data['cutting_laser_chance'],
            unknown_0x075491ca=data['unknown_0x075491ca'],
            unknown_0x54f2892e=data['unknown_0x54f2892e'],
            energy_bolt_damage=DamageInfo.from_json(data['energy_bolt_damage']),
            energy_bolt_projectile=data['energy_bolt_projectile'],
            energy_bolt_attack_duration=data['energy_bolt_attack_duration'],
            unknown_0x28944183=data['unknown_0x28944183'],
            unknown_0xc7a69a59=data['unknown_0xc7a69a59'],
            sound_energy_bolt=AudioPlaybackParms.from_json(data['sound_energy_bolt']),
            unknown_0x9ede657f=data['unknown_0x9ede657f'],
            unknown_0xcd787d9b=data['unknown_0xcd787d9b'],
            virus_attack_time=data['virus_attack_time'],
            virus_damage=DamageInfo.from_json(data['virus_damage']),
            sound_always_ff=data['sound_always_ff'],
            sound_0xbb3f8a7b=data['sound_0xbb3f8a7b'],
            sound_0x601f846d=data['sound_0x601f846d'],
            unknown_0x64c7990d=data['unknown_0x64c7990d'],
            unknown_0x376181e9=data['unknown_0x376181e9'],
            cutting_laser_damage=DamageInfo.from_json(data['cutting_laser_damage']),
            sound_cutting_laser=AudioPlaybackParms.from_json(data['sound_cutting_laser']),
            cutting_laser_beam_info=PlasmaBeamInfo.from_json(data['cutting_laser_beam_info']),
            shield_vulnerability=DamageVulnerability.from_json(data['shield_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'hearing_radius': self.hearing_radius,
            'unknown_0x4a6c4b40': self.unknown_0x4a6c4b40,
            'unknown_0x30d11671': self.unknown_0x30d11671,
            'model_no_holos': self.model_no_holos,
            'skin_no_holos': self.skin_no_holos,
            'shield_down_time': self.shield_down_time,
            'unknown_0xffb37b81': self.unknown_0xffb37b81,
            'shield_up_time': self.shield_up_time,
            'unknown_0x0d1d1648': self.unknown_0x0d1d1648,
            'shield_explode_effect': self.shield_explode_effect,
            'sound_shield_explode': self.sound_shield_explode.to_json(),
            'sound_shield_on': self.sound_shield_on.to_json(),
            'sound_shield_off': self.sound_shield_off.to_json(),
            'sound_flinch': self.sound_flinch.to_json(),
            'unknown_0xad120ad7': self.unknown_0xad120ad7,
            'unknown_0xe70ef8a3': self.unknown_0xe70ef8a3,
            'audio_playback_parms': self.audio_playback_parms.to_json(),
            'unknown_0x70e597d4': self.unknown_0x70e597d4,
            'unknown_0x94980a67': self.unknown_0x94980a67,
            'unknown_0xd02f08b0': self.unknown_0xd02f08b0,
            'unknown_0x53e84718': self.unknown_0x53e84718,
            'unknown_0x6fbc1bf9': self.unknown_0x6fbc1bf9,
            'energy_bolt_chance': self.energy_bolt_chance,
            'cutting_laser_chance': self.cutting_laser_chance,
            'unknown_0x075491ca': self.unknown_0x075491ca,
            'unknown_0x54f2892e': self.unknown_0x54f2892e,
            'energy_bolt_damage': self.energy_bolt_damage.to_json(),
            'energy_bolt_projectile': self.energy_bolt_projectile,
            'energy_bolt_attack_duration': self.energy_bolt_attack_duration,
            'unknown_0x28944183': self.unknown_0x28944183,
            'unknown_0xc7a69a59': self.unknown_0xc7a69a59,
            'sound_energy_bolt': self.sound_energy_bolt.to_json(),
            'unknown_0x9ede657f': self.unknown_0x9ede657f,
            'unknown_0xcd787d9b': self.unknown_0xcd787d9b,
            'virus_attack_time': self.virus_attack_time,
            'virus_damage': self.virus_damage.to_json(),
            'sound_always_ff': self.sound_always_ff,
            'sound_0xbb3f8a7b': self.sound_0xbb3f8a7b,
            'sound_0x601f846d': self.sound_0x601f846d,
            'unknown_0x64c7990d': self.unknown_0x64c7990d,
            'unknown_0x376181e9': self.unknown_0x376181e9,
            'cutting_laser_damage': self.cutting_laser_damage.to_json(),
            'sound_cutting_laser': self.sound_cutting_laser.to_json(),
            'cutting_laser_beam_info': self.cutting_laser_beam_info.to_json(),
            'shield_vulnerability': self.shield_vulnerability.to_json(),
        }

    def _dependencies_for_model_no_holos(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.model_no_holos)

    def _dependencies_for_skin_no_holos(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.skin_no_holos)

    def _dependencies_for_shield_explode_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shield_explode_effect)

    def _dependencies_for_sound_shield_explode(self, asset_manager):
        yield from self.sound_shield_explode.dependencies_for(asset_manager)

    def _dependencies_for_sound_shield_on(self, asset_manager):
        yield from self.sound_shield_on.dependencies_for(asset_manager)

    def _dependencies_for_sound_shield_off(self, asset_manager):
        yield from self.sound_shield_off.dependencies_for(asset_manager)

    def _dependencies_for_sound_flinch(self, asset_manager):
        yield from self.sound_flinch.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms(self, asset_manager):
        yield from self.audio_playback_parms.dependencies_for(asset_manager)

    def _dependencies_for_energy_bolt_damage(self, asset_manager):
        yield from self.energy_bolt_damage.dependencies_for(asset_manager)

    def _dependencies_for_energy_bolt_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.energy_bolt_projectile)

    def _dependencies_for_sound_energy_bolt(self, asset_manager):
        yield from self.sound_energy_bolt.dependencies_for(asset_manager)

    def _dependencies_for_virus_damage(self, asset_manager):
        yield from self.virus_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_0xbb3f8a7b(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xbb3f8a7b)

    def _dependencies_for_sound_0x601f846d(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x601f846d)

    def _dependencies_for_cutting_laser_damage(self, asset_manager):
        yield from self.cutting_laser_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_cutting_laser(self, asset_manager):
        yield from self.sound_cutting_laser.dependencies_for(asset_manager)

    def _dependencies_for_cutting_laser_beam_info(self, asset_manager):
        yield from self.cutting_laser_beam_info.dependencies_for(asset_manager)

    def _dependencies_for_shield_vulnerability(self, asset_manager):
        yield from self.shield_vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_model_no_holos, "model_no_holos", "AssetId"),
            (self._dependencies_for_skin_no_holos, "skin_no_holos", "AssetId"),
            (self._dependencies_for_shield_explode_effect, "shield_explode_effect", "AssetId"),
            (self._dependencies_for_sound_shield_explode, "sound_shield_explode", "AudioPlaybackParms"),
            (self._dependencies_for_sound_shield_on, "sound_shield_on", "AudioPlaybackParms"),
            (self._dependencies_for_sound_shield_off, "sound_shield_off", "AudioPlaybackParms"),
            (self._dependencies_for_sound_flinch, "sound_flinch", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms, "audio_playback_parms", "AudioPlaybackParms"),
            (self._dependencies_for_energy_bolt_damage, "energy_bolt_damage", "DamageInfo"),
            (self._dependencies_for_energy_bolt_projectile, "energy_bolt_projectile", "AssetId"),
            (self._dependencies_for_sound_energy_bolt, "sound_energy_bolt", "AudioPlaybackParms"),
            (self._dependencies_for_virus_damage, "virus_damage", "DamageInfo"),
            (self._dependencies_for_sound_0xbb3f8a7b, "sound_0xbb3f8a7b", "int"),
            (self._dependencies_for_sound_0x601f846d, "sound_0x601f846d", "int"),
            (self._dependencies_for_cutting_laser_damage, "cutting_laser_damage", "DamageInfo"),
            (self._dependencies_for_sound_cutting_laser, "sound_cutting_laser", "AudioPlaybackParms"),
            (self._dependencies_for_cutting_laser_beam_info, "cutting_laser_beam_info", "PlasmaBeamInfo"),
            (self._dependencies_for_shield_vulnerability, "shield_vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for RezbitData.{field_name} ({field_type}): {e}"
                )


def _decode_hearing_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4a6c4b40(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x30d11671(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model_no_holos(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_skin_no_holos(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shield_down_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xffb37b81(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shield_up_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0d1d1648(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shield_explode_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_shield_explode(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_shield_on(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_shield_off(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_sound_flinch(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_unknown_0xad120ad7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe70ef8a3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_audio_playback_parms(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_unknown_0x70e597d4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x94980a67(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd02f08b0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x53e84718(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6fbc1bf9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_energy_bolt_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cutting_laser_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x075491ca(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x54f2892e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_energy_bolt_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})


def _decode_energy_bolt_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_energy_bolt_attack_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x28944183(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc7a69a59(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_energy_bolt(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_unknown_0x9ede657f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcd787d9b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_virus_attack_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_virus_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})


def _decode_sound_always_ff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0xbb3f8a7b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x601f846d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x64c7990d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x376181e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cutting_laser_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})


def _decode_sound_cutting_laser(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_cutting_laser_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})


def _decode_shield_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xed69488f: ('hearing_radius', _decode_hearing_radius),
    0x4a6c4b40: ('unknown_0x4a6c4b40', _decode_unknown_0x4a6c4b40),
    0x30d11671: ('unknown_0x30d11671', _decode_unknown_0x30d11671),
    0xc80bb6e4: ('model_no_holos', _decode_model_no_holos),
    0x5486319: ('skin_no_holos', _decode_skin_no_holos),
    0x8980a469: ('shield_down_time', _decode_shield_down_time),
    0xffb37b81: ('unknown_0xffb37b81', _decode_unknown_0xffb37b81),
    0x448579cd: ('shield_up_time', _decode_shield_up_time),
    0xd1d1648: ('unknown_0x0d1d1648', _decode_unknown_0x0d1d1648),
    0xa41f75ef: ('shield_explode_effect', _decode_shield_explode_effect),
    0xa34e2d84: ('sound_shield_explode', _decode_sound_shield_explode),
    0x8c598e41: ('sound_shield_on', _decode_sound_shield_on),
    0xf4491ed5: ('sound_shield_off', _decode_sound_shield_off),
    0x7d832158: ('sound_flinch', _decode_sound_flinch),
    0xad120ad7: ('unknown_0xad120ad7', _decode_unknown_0xad120ad7),
    0xe70ef8a3: ('unknown_0xe70ef8a3', _decode_unknown_0xe70ef8a3),
    0x6bf2ff60: ('audio_playback_parms', _decode_audio_playback_parms),
    0x70e597d4: ('unknown_0x70e597d4', _decode_unknown_0x70e597d4),
    0x94980a67: ('unknown_0x94980a67', _decode_unknown_0x94980a67),
    0xd02f08b0: ('unknown_0xd02f08b0', _decode_unknown_0xd02f08b0),
    0x53e84718: ('unknown_0x53e84718', _decode_unknown_0x53e84718),
    0x6fbc1bf9: ('unknown_0x6fbc1bf9', _decode_unknown_0x6fbc1bf9),
    0xdc276015: ('energy_bolt_chance', _decode_energy_bolt_chance),
    0x2ca3e9cd: ('cutting_laser_chance', _decode_cutting_laser_chance),
    0x75491ca: ('unknown_0x075491ca', _decode_unknown_0x075491ca),
    0x54f2892e: ('unknown_0x54f2892e', _decode_unknown_0x54f2892e),
    0x600c5f40: ('energy_bolt_damage', _decode_energy_bolt_damage),
    0x2f11094b: ('energy_bolt_projectile', _decode_energy_bolt_projectile),
    0xa1f350f5: ('energy_bolt_attack_duration', _decode_energy_bolt_attack_duration),
    0x28944183: ('unknown_0x28944183', _decode_unknown_0x28944183),
    0xc7a69a59: ('unknown_0xc7a69a59', _decode_unknown_0xc7a69a59),
    0xbd3eb001: ('sound_energy_bolt', _decode_sound_energy_bolt),
    0x9ede657f: ('unknown_0x9ede657f', _decode_unknown_0x9ede657f),
    0xcd787d9b: ('unknown_0xcd787d9b', _decode_unknown_0xcd787d9b),
    0x4a7d3b04: ('virus_attack_time', _decode_virus_attack_time),
    0x16869b57: ('virus_damage', _decode_virus_damage),
    0x973d7cc3: ('sound_always_ff', _decode_sound_always_ff),
    0xbb3f8a7b: ('sound_0xbb3f8a7b', _decode_sound_0xbb3f8a7b),
    0x601f846d: ('sound_0x601f846d', _decode_sound_0x601f846d),
    0x64c7990d: ('unknown_0x64c7990d', _decode_unknown_0x64c7990d),
    0x376181e9: ('unknown_0x376181e9', _decode_unknown_0x376181e9),
    0xbb58c088: ('cutting_laser_damage', _decode_cutting_laser_damage),
    0x7864ca32: ('sound_cutting_laser', _decode_sound_cutting_laser),
    0x59764dbb: ('cutting_laser_beam_info', _decode_cutting_laser_beam_info),
    0xd34f1323: ('shield_vulnerability', _decode_shield_vulnerability),
}
