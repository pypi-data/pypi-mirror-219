# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.BasicSwarmProperties import BasicSwarmProperties
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EmperorIngStage3StructA import EmperorIngStage3StructA
from retro_data_structures.properties.echoes.archetypes.EmperorIngStage3StructB import EmperorIngStage3StructB
from retro_data_structures.properties.echoes.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.echoes.archetypes.ShockWaveInfo import ShockWaveInfo
from retro_data_structures.properties.echoes.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class EmperorIngStage3Data(BaseProperty):
    taunt_frequency: float = dataclasses.field(default=0.0)
    yellow_health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    health: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerable_time: float = dataclasses.field(default=0.0)
    vulnerable_damage_threshold: float = dataclasses.field(default=0.0)
    red_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    light_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    dark_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    jump_slide_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ground_pound_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    emperor_ing_stage3_struct_a_0x98e311c1: EmperorIngStage3StructA = dataclasses.field(default_factory=EmperorIngStage3StructA)
    emperor_ing_stage3_struct_a_0x93dae216: EmperorIngStage3StructA = dataclasses.field(default_factory=EmperorIngStage3StructA)
    light_swarm_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    light_swarm_properties: BasicSwarmProperties = dataclasses.field(default_factory=BasicSwarmProperties)
    light_swarm_death_sound: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    audio_playback_parms: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    unknown_struct26: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26)
    jump_attack_shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    sound: int = dataclasses.field(default=0, metadata={'sound': True})
    emperor_ing_stage3_struct_b_0xe843417f: EmperorIngStage3StructB = dataclasses.field(default_factory=EmperorIngStage3StructB)
    emperor_ing_stage3_struct_b_0xd13bec3f: EmperorIngStage3StructB = dataclasses.field(default_factory=EmperorIngStage3StructB)
    emperor_ing_stage3_struct_b_0xc61388ff: EmperorIngStage3StructB = dataclasses.field(default_factory=EmperorIngStage3StructB)
    emperor_ing_stage3_struct_b_0xa3cab6bf: EmperorIngStage3StructB = dataclasses.field(default_factory=EmperorIngStage3StructB)

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
        data.write(b'\x00\x19')  # 25 properties

        data.write(b'):\x0c\x19')  # 0x293a0c19
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt_frequency))

        data.write(b'\x8a?v\x0c')  # 0x8a3f760c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.yellow_health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcf\x90\xd1^')  # 0xcf90d15e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.health.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'i\xbc\\\xd4')  # 0x69bc5cd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vulnerable_time))

        data.write(b'\xb1\x10\xe59')  # 0xb110e539
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vulnerable_damage_threshold))

        data.write(b'\x8dp\xd6z')  # 0x8d70d67a
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.red_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x89\xc1B\xf7')  # 0x89c142f7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.light_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x88U\xc1\x18')  # 0x8855c118
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dark_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc9A`4')  # 0xc9416034
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x14@\xd1R')  # 0x1440d152
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xefX+\xd6')  # 0xef582bd6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_slide_damage.to_stream(data)
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

        data.write(b'\x98\xe3\x11\xc1')  # 0x98e311c1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.emperor_ing_stage3_struct_a_0x98e311c1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93\xda\xe2\x16')  # 0x93dae216
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.emperor_ing_stage3_struct_a_0x93dae216.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'O\x82\xb9\xe5')  # 0x4f82b9e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.light_swarm_effect))

        data.write(b'\x04>\x9c.')  # 0x43e9c2e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.light_swarm_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x91\x00\x15\x08')  # 0x91001508
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.light_swarm_death_sound.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x03U)S')  # 0x3552953
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xaf~03')  # 0xaf7e3033
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xabN\xd4V')  # 0xab4ed456
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.jump_attack_shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98_r\xfd')  # 0x985f72fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound))

        data.write(b'\xe8CA\x7f')  # 0xe843417f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.emperor_ing_stage3_struct_b_0xe843417f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1;\xec?')  # 0xd13bec3f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.emperor_ing_stage3_struct_b_0xd13bec3f.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x13\x88\xff')  # 0xc61388ff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.emperor_ing_stage3_struct_b_0xc61388ff.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3\xca\xb6\xbf')  # 0xa3cab6bf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.emperor_ing_stage3_struct_b_0xa3cab6bf.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            taunt_frequency=data['taunt_frequency'],
            yellow_health=HealthInfo.from_json(data['yellow_health']),
            health=HealthInfo.from_json(data['health']),
            vulnerable_time=data['vulnerable_time'],
            vulnerable_damage_threshold=data['vulnerable_damage_threshold'],
            red_vulnerability=DamageVulnerability.from_json(data['red_vulnerability']),
            light_vulnerability=DamageVulnerability.from_json(data['light_vulnerability']),
            dark_vulnerability=DamageVulnerability.from_json(data['dark_vulnerability']),
            melee_damage=DamageInfo.from_json(data['melee_damage']),
            damage_info=DamageInfo.from_json(data['damage_info']),
            jump_slide_damage=DamageInfo.from_json(data['jump_slide_damage']),
            ground_pound_damage=DamageInfo.from_json(data['ground_pound_damage']),
            emperor_ing_stage3_struct_a_0x98e311c1=EmperorIngStage3StructA.from_json(data['emperor_ing_stage3_struct_a_0x98e311c1']),
            emperor_ing_stage3_struct_a_0x93dae216=EmperorIngStage3StructA.from_json(data['emperor_ing_stage3_struct_a_0x93dae216']),
            light_swarm_effect=data['light_swarm_effect'],
            light_swarm_properties=BasicSwarmProperties.from_json(data['light_swarm_properties']),
            light_swarm_death_sound=AudioPlaybackParms.from_json(data['light_swarm_death_sound']),
            audio_playback_parms=AudioPlaybackParms.from_json(data['audio_playback_parms']),
            unknown_struct26=UnknownStruct26.from_json(data['unknown_struct26']),
            jump_attack_shock_wave_info=ShockWaveInfo.from_json(data['jump_attack_shock_wave_info']),
            sound=data['sound'],
            emperor_ing_stage3_struct_b_0xe843417f=EmperorIngStage3StructB.from_json(data['emperor_ing_stage3_struct_b_0xe843417f']),
            emperor_ing_stage3_struct_b_0xd13bec3f=EmperorIngStage3StructB.from_json(data['emperor_ing_stage3_struct_b_0xd13bec3f']),
            emperor_ing_stage3_struct_b_0xc61388ff=EmperorIngStage3StructB.from_json(data['emperor_ing_stage3_struct_b_0xc61388ff']),
            emperor_ing_stage3_struct_b_0xa3cab6bf=EmperorIngStage3StructB.from_json(data['emperor_ing_stage3_struct_b_0xa3cab6bf']),
        )

    def to_json(self) -> dict:
        return {
            'taunt_frequency': self.taunt_frequency,
            'yellow_health': self.yellow_health.to_json(),
            'health': self.health.to_json(),
            'vulnerable_time': self.vulnerable_time,
            'vulnerable_damage_threshold': self.vulnerable_damage_threshold,
            'red_vulnerability': self.red_vulnerability.to_json(),
            'light_vulnerability': self.light_vulnerability.to_json(),
            'dark_vulnerability': self.dark_vulnerability.to_json(),
            'melee_damage': self.melee_damage.to_json(),
            'damage_info': self.damage_info.to_json(),
            'jump_slide_damage': self.jump_slide_damage.to_json(),
            'ground_pound_damage': self.ground_pound_damage.to_json(),
            'emperor_ing_stage3_struct_a_0x98e311c1': self.emperor_ing_stage3_struct_a_0x98e311c1.to_json(),
            'emperor_ing_stage3_struct_a_0x93dae216': self.emperor_ing_stage3_struct_a_0x93dae216.to_json(),
            'light_swarm_effect': self.light_swarm_effect,
            'light_swarm_properties': self.light_swarm_properties.to_json(),
            'light_swarm_death_sound': self.light_swarm_death_sound.to_json(),
            'audio_playback_parms': self.audio_playback_parms.to_json(),
            'unknown_struct26': self.unknown_struct26.to_json(),
            'jump_attack_shock_wave_info': self.jump_attack_shock_wave_info.to_json(),
            'sound': self.sound,
            'emperor_ing_stage3_struct_b_0xe843417f': self.emperor_ing_stage3_struct_b_0xe843417f.to_json(),
            'emperor_ing_stage3_struct_b_0xd13bec3f': self.emperor_ing_stage3_struct_b_0xd13bec3f.to_json(),
            'emperor_ing_stage3_struct_b_0xc61388ff': self.emperor_ing_stage3_struct_b_0xc61388ff.to_json(),
            'emperor_ing_stage3_struct_b_0xa3cab6bf': self.emperor_ing_stage3_struct_b_0xa3cab6bf.to_json(),
        }

    def _dependencies_for_yellow_health(self, asset_manager):
        yield from self.yellow_health.dependencies_for(asset_manager)

    def _dependencies_for_health(self, asset_manager):
        yield from self.health.dependencies_for(asset_manager)

    def _dependencies_for_red_vulnerability(self, asset_manager):
        yield from self.red_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_light_vulnerability(self, asset_manager):
        yield from self.light_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_dark_vulnerability(self, asset_manager):
        yield from self.dark_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_melee_damage(self, asset_manager):
        yield from self.melee_damage.dependencies_for(asset_manager)

    def _dependencies_for_damage_info(self, asset_manager):
        yield from self.damage_info.dependencies_for(asset_manager)

    def _dependencies_for_jump_slide_damage(self, asset_manager):
        yield from self.jump_slide_damage.dependencies_for(asset_manager)

    def _dependencies_for_ground_pound_damage(self, asset_manager):
        yield from self.ground_pound_damage.dependencies_for(asset_manager)

    def _dependencies_for_emperor_ing_stage3_struct_a_0x98e311c1(self, asset_manager):
        yield from self.emperor_ing_stage3_struct_a_0x98e311c1.dependencies_for(asset_manager)

    def _dependencies_for_emperor_ing_stage3_struct_a_0x93dae216(self, asset_manager):
        yield from self.emperor_ing_stage3_struct_a_0x93dae216.dependencies_for(asset_manager)

    def _dependencies_for_light_swarm_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.light_swarm_effect)

    def _dependencies_for_light_swarm_properties(self, asset_manager):
        yield from self.light_swarm_properties.dependencies_for(asset_manager)

    def _dependencies_for_light_swarm_death_sound(self, asset_manager):
        yield from self.light_swarm_death_sound.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms(self, asset_manager):
        yield from self.audio_playback_parms.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct26(self, asset_manager):
        yield from self.unknown_struct26.dependencies_for(asset_manager)

    def _dependencies_for_jump_attack_shock_wave_info(self, asset_manager):
        yield from self.jump_attack_shock_wave_info.dependencies_for(asset_manager)

    def _dependencies_for_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound)

    def _dependencies_for_emperor_ing_stage3_struct_b_0xe843417f(self, asset_manager):
        yield from self.emperor_ing_stage3_struct_b_0xe843417f.dependencies_for(asset_manager)

    def _dependencies_for_emperor_ing_stage3_struct_b_0xd13bec3f(self, asset_manager):
        yield from self.emperor_ing_stage3_struct_b_0xd13bec3f.dependencies_for(asset_manager)

    def _dependencies_for_emperor_ing_stage3_struct_b_0xc61388ff(self, asset_manager):
        yield from self.emperor_ing_stage3_struct_b_0xc61388ff.dependencies_for(asset_manager)

    def _dependencies_for_emperor_ing_stage3_struct_b_0xa3cab6bf(self, asset_manager):
        yield from self.emperor_ing_stage3_struct_b_0xa3cab6bf.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_yellow_health, "yellow_health", "HealthInfo"),
            (self._dependencies_for_health, "health", "HealthInfo"),
            (self._dependencies_for_red_vulnerability, "red_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_light_vulnerability, "light_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_dark_vulnerability, "dark_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_melee_damage, "melee_damage", "DamageInfo"),
            (self._dependencies_for_damage_info, "damage_info", "DamageInfo"),
            (self._dependencies_for_jump_slide_damage, "jump_slide_damage", "DamageInfo"),
            (self._dependencies_for_ground_pound_damage, "ground_pound_damage", "DamageInfo"),
            (self._dependencies_for_emperor_ing_stage3_struct_a_0x98e311c1, "emperor_ing_stage3_struct_a_0x98e311c1", "EmperorIngStage3StructA"),
            (self._dependencies_for_emperor_ing_stage3_struct_a_0x93dae216, "emperor_ing_stage3_struct_a_0x93dae216", "EmperorIngStage3StructA"),
            (self._dependencies_for_light_swarm_effect, "light_swarm_effect", "AssetId"),
            (self._dependencies_for_light_swarm_properties, "light_swarm_properties", "BasicSwarmProperties"),
            (self._dependencies_for_light_swarm_death_sound, "light_swarm_death_sound", "AudioPlaybackParms"),
            (self._dependencies_for_audio_playback_parms, "audio_playback_parms", "AudioPlaybackParms"),
            (self._dependencies_for_unknown_struct26, "unknown_struct26", "UnknownStruct26"),
            (self._dependencies_for_jump_attack_shock_wave_info, "jump_attack_shock_wave_info", "ShockWaveInfo"),
            (self._dependencies_for_sound, "sound", "int"),
            (self._dependencies_for_emperor_ing_stage3_struct_b_0xe843417f, "emperor_ing_stage3_struct_b_0xe843417f", "EmperorIngStage3StructB"),
            (self._dependencies_for_emperor_ing_stage3_struct_b_0xd13bec3f, "emperor_ing_stage3_struct_b_0xd13bec3f", "EmperorIngStage3StructB"),
            (self._dependencies_for_emperor_ing_stage3_struct_b_0xc61388ff, "emperor_ing_stage3_struct_b_0xc61388ff", "EmperorIngStage3StructB"),
            (self._dependencies_for_emperor_ing_stage3_struct_b_0xa3cab6bf, "emperor_ing_stage3_struct_b_0xa3cab6bf", "EmperorIngStage3StructB"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for EmperorIngStage3Data.{field_name} ({field_type}): {e}"
                )


def _decode_taunt_frequency(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_yellow_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_health(data: typing.BinaryIO, property_size: int):
    return HealthInfo.from_stream(data, property_size)


def _decode_vulnerable_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vulnerable_damage_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_red_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_light_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_dark_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_jump_slide_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_ground_pound_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_emperor_ing_stage3_struct_a_0x98e311c1(data: typing.BinaryIO, property_size: int):
    return EmperorIngStage3StructA.from_stream(data, property_size)


def _decode_emperor_ing_stage3_struct_a_0x93dae216(data: typing.BinaryIO, property_size: int):
    return EmperorIngStage3StructA.from_stream(data, property_size)


def _decode_light_swarm_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_light_swarm_properties(data: typing.BinaryIO, property_size: int):
    return BasicSwarmProperties.from_stream(data, property_size)


def _decode_light_swarm_death_sound(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_audio_playback_parms(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_unknown_struct26(data: typing.BinaryIO, property_size: int):
    return UnknownStruct26.from_stream(data, property_size)


def _decode_jump_attack_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_emperor_ing_stage3_struct_b_0xe843417f(data: typing.BinaryIO, property_size: int):
    return EmperorIngStage3StructB.from_stream(data, property_size)


def _decode_emperor_ing_stage3_struct_b_0xd13bec3f(data: typing.BinaryIO, property_size: int):
    return EmperorIngStage3StructB.from_stream(data, property_size)


def _decode_emperor_ing_stage3_struct_b_0xc61388ff(data: typing.BinaryIO, property_size: int):
    return EmperorIngStage3StructB.from_stream(data, property_size)


def _decode_emperor_ing_stage3_struct_b_0xa3cab6bf(data: typing.BinaryIO, property_size: int):
    return EmperorIngStage3StructB.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x293a0c19: ('taunt_frequency', _decode_taunt_frequency),
    0x8a3f760c: ('yellow_health', _decode_yellow_health),
    0xcf90d15e: ('health', _decode_health),
    0x69bc5cd4: ('vulnerable_time', _decode_vulnerable_time),
    0xb110e539: ('vulnerable_damage_threshold', _decode_vulnerable_damage_threshold),
    0x8d70d67a: ('red_vulnerability', _decode_red_vulnerability),
    0x89c142f7: ('light_vulnerability', _decode_light_vulnerability),
    0x8855c118: ('dark_vulnerability', _decode_dark_vulnerability),
    0xc9416034: ('melee_damage', _decode_melee_damage),
    0x1440d152: ('damage_info', _decode_damage_info),
    0xef582bd6: ('jump_slide_damage', _decode_jump_slide_damage),
    0x4738c321: ('ground_pound_damage', _decode_ground_pound_damage),
    0x98e311c1: ('emperor_ing_stage3_struct_a_0x98e311c1', _decode_emperor_ing_stage3_struct_a_0x98e311c1),
    0x93dae216: ('emperor_ing_stage3_struct_a_0x93dae216', _decode_emperor_ing_stage3_struct_a_0x93dae216),
    0x4f82b9e5: ('light_swarm_effect', _decode_light_swarm_effect),
    0x43e9c2e: ('light_swarm_properties', _decode_light_swarm_properties),
    0x91001508: ('light_swarm_death_sound', _decode_light_swarm_death_sound),
    0x3552953: ('audio_playback_parms', _decode_audio_playback_parms),
    0xaf7e3033: ('unknown_struct26', _decode_unknown_struct26),
    0xab4ed456: ('jump_attack_shock_wave_info', _decode_jump_attack_shock_wave_info),
    0x985f72fd: ('sound', _decode_sound),
    0xe843417f: ('emperor_ing_stage3_struct_b_0xe843417f', _decode_emperor_ing_stage3_struct_b_0xe843417f),
    0xd13bec3f: ('emperor_ing_stage3_struct_b_0xd13bec3f', _decode_emperor_ing_stage3_struct_b_0xd13bec3f),
    0xc61388ff: ('emperor_ing_stage3_struct_b_0xc61388ff', _decode_emperor_ing_stage3_struct_b_0xc61388ff),
    0xa3cab6bf: ('emperor_ing_stage3_struct_b_0xa3cab6bf', _decode_emperor_ing_stage3_struct_b_0xa3cab6bf),
}
