# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.archetypes.PowerBombGuardianStageProperties import PowerBombGuardianStageProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class SporbBase(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_0x95e7a2c2: float = dataclasses.field(default=2.0)
    unknown_0x76ba1c18: float = dataclasses.field(default=2.0)
    unknown_0x3eb2de35: float = dataclasses.field(default=1.0)
    unknown_0xe50d8dd2: float = dataclasses.field(default=1.0)
    unknown_0x64d482d5: int = dataclasses.field(default=1)
    unknown_0xc3e002ac: int = dataclasses.field(default=1)
    shot_angle_variance: float = dataclasses.field(default=0.0)
    attack_aim_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    tendril_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0x35557a83: float = dataclasses.field(default=0.10000000149011612)
    grabber_out_acceleration: float = dataclasses.field(default=-10.0)
    grabber_in_acceleration: float = dataclasses.field(default=-100.0)
    unknown_0xbfddabd4: float = dataclasses.field(default=50.0)
    unknown_0x62bfaa35: float = dataclasses.field(default=0.0)
    grabber_attach_time: float = dataclasses.field(default=2.0)
    unknown_0xed82c56a: float = dataclasses.field(default=2.0)
    unknown_0xe918f440: float = dataclasses.field(default=2.0)
    spit_force: float = dataclasses.field(default=40.0)
    spit_damage: float = dataclasses.field(default=0.0)
    grab_damage: float = dataclasses.field(default=5.0)
    unknown_0x2cfade2c: float = dataclasses.field(default=10.0)
    unknown_0xb68e75cc: float = dataclasses.field(default=5.0)
    unknown_0x6d31262b: float = dataclasses.field(default=20.0)
    is_power_bomb_guardian: bool = dataclasses.field(default=False)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    power_bomb_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x03a76d35: float = dataclasses.field(default=20.0)
    unknown_0x6d4e0f5a: float = dataclasses.field(default=1.0)
    unknown_0x3538d49b: float = dataclasses.field(default=1.0)
    unknown_0xe89c7707: float = dataclasses.field(default=1.0)
    unknown_0x738d1f51: float = dataclasses.field(default=5.0)
    sound_0x9480c6d7: int = dataclasses.field(default=0)
    unknown_0x48df4182: float = dataclasses.field(default=20.0)
    unknown_0xe39482ad: float = dataclasses.field(default=0.0)
    unknown_0xdd8502cc: float = dataclasses.field(default=1.0)
    unknown_0x4ab8cf7d: float = dataclasses.field(default=0.4000000059604645)
    unknown_0xf5e28404: float = dataclasses.field(default=5.0)
    grabber_fire_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    grabber_flight_sound: int = dataclasses.field(default=0)
    grabber_hit_player_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    grabber_hit_world_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    grabber_retract_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x64e9152d: int = dataclasses.field(default=0, metadata={'sound': True})
    morphball_spit_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    grabber_explosion_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    ball_escape_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    needle_telegraph_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    grabber_telegraph_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    power_bomb_guardian_stage_properties_0x510dba97: PowerBombGuardianStageProperties = dataclasses.field(default_factory=PowerBombGuardianStageProperties)
    power_bomb_guardian_stage_properties_0x0b6c85f7: PowerBombGuardianStageProperties = dataclasses.field(default_factory=PowerBombGuardianStageProperties)
    power_bomb_guardian_stage_properties_0x8b9c92e8: PowerBombGuardianStageProperties = dataclasses.field(default_factory=PowerBombGuardianStageProperties)
    power_bomb_guardian_stage_properties_0xbfaefb37: PowerBombGuardianStageProperties = dataclasses.field(default_factory=PowerBombGuardianStageProperties)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SPBB'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Sporb.rel']

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x007')  # 55 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb3wGP')  # 0xb3774750
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.patterned.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~9\x7f\xed')  # 0x7e397fed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_information.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95\xe7\xa2\xc2')  # 0x95e7a2c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x95e7a2c2))

        data.write(b'v\xba\x1c\x18')  # 0x76ba1c18
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x76ba1c18))

        data.write(b'>\xb2\xde5')  # 0x3eb2de35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3eb2de35))

        data.write(b'\xe5\r\x8d\xd2')  # 0xe50d8dd2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe50d8dd2))

        data.write(b'd\xd4\x82\xd5')  # 0x64d482d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x64d482d5))

        data.write(b'\xc3\xe0\x02\xac')  # 0xc3e002ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc3e002ac))

        data.write(b'\xd7_\x9c\xf2')  # 0xd75f9cf2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shot_angle_variance))

        data.write(b'T\x0c\x1f\x87')  # 0x540c1f87
        data.write(b'\x00\x0c')  # size
        self.attack_aim_offset.to_stream(data)

        data.write(b'3\x86\x8c\x8f')  # 0x33868c8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.tendril_particle_effect))

        data.write(b'5Uz\x83')  # 0x35557a83
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x35557a83))

        data.write(b'#\xbd9C')  # 0x23bd3943
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grabber_out_acceleration))

        data.write(b'\xd9/H]')  # 0xd92f485d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grabber_in_acceleration))

        data.write(b'\xbf\xdd\xab\xd4')  # 0xbfddabd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbfddabd4))

        data.write(b'b\xbf\xaa5')  # 0x62bfaa35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x62bfaa35))

        data.write(b'C;^0')  # 0x433b5e30
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grabber_attach_time))

        data.write(b'\xed\x82\xc5j')  # 0xed82c56a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xed82c56a))

        data.write(b'\xe9\x18\xf4@')  # 0xe918f440
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe918f440))

        data.write(b"'1\xadt")  # 0x2731ad74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spit_force))

        data.write(b'\x03\xfb-\xd4')  # 0x3fb2dd4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spit_damage))

        data.write(b'\x95\xad\x88$')  # 0x95ad8824
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_damage))

        data.write(b',\xfa\xde,')  # 0x2cfade2c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2cfade2c))

        data.write(b'\xb6\x8eu\xcc')  # 0xb68e75cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb68e75cc))

        data.write(b'm1&+')  # 0x6d31262b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6d31262b))

        data.write(b'\xb6(\x85Z')  # 0xb628855a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_power_bomb_guardian))

        data.write(b'\x99\x07E\xdd')  # 0x990745dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.wpsc))

        data.write(b"_<'\xc6")  # 0x5f3c27c6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.power_bomb_projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_knock_back_power': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x03\xa7m5')  # 0x3a76d35
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x03a76d35))

        data.write(b'mN\x0fZ')  # 0x6d4e0f5a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6d4e0f5a))

        data.write(b'58\xd4\x9b')  # 0x3538d49b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3538d49b))

        data.write(b'\xe8\x9cw\x07')  # 0xe89c7707
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe89c7707))

        data.write(b's\x8d\x1fQ')  # 0x738d1f51
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x738d1f51))

        data.write(b'\x94\x80\xc6\xd7')  # 0x9480c6d7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x9480c6d7))

        data.write(b'H\xdfA\x82')  # 0x48df4182
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x48df4182))

        data.write(b'\xe3\x94\x82\xad')  # 0xe39482ad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe39482ad))

        data.write(b'\xdd\x85\x02\xcc')  # 0xdd8502cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdd8502cc))

        data.write(b'J\xb8\xcf}')  # 0x4ab8cf7d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4ab8cf7d))

        data.write(b'\xf5\xe2\x84\x04')  # 0xf5e28404
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf5e28404))

        data.write(b'\xa8}r\xfc')  # 0xa87d72fc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grabber_fire_sound))

        data.write(b'\x86a(^')  # 0x8661285e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grabber_flight_sound))

        data.write(b'A#2:')  # 0x4123323a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grabber_hit_player_sound))

        data.write(b'M.\xc58')  # 0x4d2ec538
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grabber_hit_world_sound))

        data.write(b'\xd5\x1c\xa0Q')  # 0xd51ca051
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grabber_retract_sound))

        data.write(b'd\xe9\x15-')  # 0x64e9152d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x64e9152d))

        data.write(b':\xcd\x0e\xcc')  # 0x3acd0ecc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.morphball_spit_sound))

        data.write(b'\xfe\xb6s\x17')  # 0xfeb67317
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grabber_explosion_sound))

        data.write(b'\x88\xa2\r\xb0')  # 0x88a20db0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.ball_escape_sound))

        data.write(b'\x95\xc1%\x7f')  # 0x95c1257f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.needle_telegraph_sound))

        data.write(b'&\x90\xe2\x16')  # 0x2690e216
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.grabber_telegraph_sound))

        data.write(b'Q\r\xba\x97')  # 0x510dba97
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.power_bomb_guardian_stage_properties_0x510dba97.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0bl\x85\xf7')  # 0xb6c85f7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.power_bomb_guardian_stage_properties_0x0b6c85f7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8b\x9c\x92\xe8')  # 0x8b9c92e8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.power_bomb_guardian_stage_properties_0x8b9c92e8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbf\xae\xfb7')  # 0xbfaefb37
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.power_bomb_guardian_stage_properties_0xbfaefb37.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            editor_properties=EditorProperties.from_json(data['editor_properties']),
            patterned=PatternedAITypedef.from_json(data['patterned']),
            actor_information=ActorParameters.from_json(data['actor_information']),
            unknown_0x95e7a2c2=data['unknown_0x95e7a2c2'],
            unknown_0x76ba1c18=data['unknown_0x76ba1c18'],
            unknown_0x3eb2de35=data['unknown_0x3eb2de35'],
            unknown_0xe50d8dd2=data['unknown_0xe50d8dd2'],
            unknown_0x64d482d5=data['unknown_0x64d482d5'],
            unknown_0xc3e002ac=data['unknown_0xc3e002ac'],
            shot_angle_variance=data['shot_angle_variance'],
            attack_aim_offset=Vector.from_json(data['attack_aim_offset']),
            tendril_particle_effect=data['tendril_particle_effect'],
            unknown_0x35557a83=data['unknown_0x35557a83'],
            grabber_out_acceleration=data['grabber_out_acceleration'],
            grabber_in_acceleration=data['grabber_in_acceleration'],
            unknown_0xbfddabd4=data['unknown_0xbfddabd4'],
            unknown_0x62bfaa35=data['unknown_0x62bfaa35'],
            grabber_attach_time=data['grabber_attach_time'],
            unknown_0xed82c56a=data['unknown_0xed82c56a'],
            unknown_0xe918f440=data['unknown_0xe918f440'],
            spit_force=data['spit_force'],
            spit_damage=data['spit_damage'],
            grab_damage=data['grab_damage'],
            unknown_0x2cfade2c=data['unknown_0x2cfade2c'],
            unknown_0xb68e75cc=data['unknown_0xb68e75cc'],
            unknown_0x6d31262b=data['unknown_0x6d31262b'],
            is_power_bomb_guardian=data['is_power_bomb_guardian'],
            wpsc=data['wpsc'],
            power_bomb_projectile_damage=DamageInfo.from_json(data['power_bomb_projectile_damage']),
            unknown_0x03a76d35=data['unknown_0x03a76d35'],
            unknown_0x6d4e0f5a=data['unknown_0x6d4e0f5a'],
            unknown_0x3538d49b=data['unknown_0x3538d49b'],
            unknown_0xe89c7707=data['unknown_0xe89c7707'],
            unknown_0x738d1f51=data['unknown_0x738d1f51'],
            sound_0x9480c6d7=data['sound_0x9480c6d7'],
            unknown_0x48df4182=data['unknown_0x48df4182'],
            unknown_0xe39482ad=data['unknown_0xe39482ad'],
            unknown_0xdd8502cc=data['unknown_0xdd8502cc'],
            unknown_0x4ab8cf7d=data['unknown_0x4ab8cf7d'],
            unknown_0xf5e28404=data['unknown_0xf5e28404'],
            grabber_fire_sound=data['grabber_fire_sound'],
            grabber_flight_sound=data['grabber_flight_sound'],
            grabber_hit_player_sound=data['grabber_hit_player_sound'],
            grabber_hit_world_sound=data['grabber_hit_world_sound'],
            grabber_retract_sound=data['grabber_retract_sound'],
            sound_0x64e9152d=data['sound_0x64e9152d'],
            morphball_spit_sound=data['morphball_spit_sound'],
            grabber_explosion_sound=data['grabber_explosion_sound'],
            ball_escape_sound=data['ball_escape_sound'],
            needle_telegraph_sound=data['needle_telegraph_sound'],
            grabber_telegraph_sound=data['grabber_telegraph_sound'],
            power_bomb_guardian_stage_properties_0x510dba97=PowerBombGuardianStageProperties.from_json(data['power_bomb_guardian_stage_properties_0x510dba97']),
            power_bomb_guardian_stage_properties_0x0b6c85f7=PowerBombGuardianStageProperties.from_json(data['power_bomb_guardian_stage_properties_0x0b6c85f7']),
            power_bomb_guardian_stage_properties_0x8b9c92e8=PowerBombGuardianStageProperties.from_json(data['power_bomb_guardian_stage_properties_0x8b9c92e8']),
            power_bomb_guardian_stage_properties_0xbfaefb37=PowerBombGuardianStageProperties.from_json(data['power_bomb_guardian_stage_properties_0xbfaefb37']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_0x95e7a2c2': self.unknown_0x95e7a2c2,
            'unknown_0x76ba1c18': self.unknown_0x76ba1c18,
            'unknown_0x3eb2de35': self.unknown_0x3eb2de35,
            'unknown_0xe50d8dd2': self.unknown_0xe50d8dd2,
            'unknown_0x64d482d5': self.unknown_0x64d482d5,
            'unknown_0xc3e002ac': self.unknown_0xc3e002ac,
            'shot_angle_variance': self.shot_angle_variance,
            'attack_aim_offset': self.attack_aim_offset.to_json(),
            'tendril_particle_effect': self.tendril_particle_effect,
            'unknown_0x35557a83': self.unknown_0x35557a83,
            'grabber_out_acceleration': self.grabber_out_acceleration,
            'grabber_in_acceleration': self.grabber_in_acceleration,
            'unknown_0xbfddabd4': self.unknown_0xbfddabd4,
            'unknown_0x62bfaa35': self.unknown_0x62bfaa35,
            'grabber_attach_time': self.grabber_attach_time,
            'unknown_0xed82c56a': self.unknown_0xed82c56a,
            'unknown_0xe918f440': self.unknown_0xe918f440,
            'spit_force': self.spit_force,
            'spit_damage': self.spit_damage,
            'grab_damage': self.grab_damage,
            'unknown_0x2cfade2c': self.unknown_0x2cfade2c,
            'unknown_0xb68e75cc': self.unknown_0xb68e75cc,
            'unknown_0x6d31262b': self.unknown_0x6d31262b,
            'is_power_bomb_guardian': self.is_power_bomb_guardian,
            'wpsc': self.wpsc,
            'power_bomb_projectile_damage': self.power_bomb_projectile_damage.to_json(),
            'unknown_0x03a76d35': self.unknown_0x03a76d35,
            'unknown_0x6d4e0f5a': self.unknown_0x6d4e0f5a,
            'unknown_0x3538d49b': self.unknown_0x3538d49b,
            'unknown_0xe89c7707': self.unknown_0xe89c7707,
            'unknown_0x738d1f51': self.unknown_0x738d1f51,
            'sound_0x9480c6d7': self.sound_0x9480c6d7,
            'unknown_0x48df4182': self.unknown_0x48df4182,
            'unknown_0xe39482ad': self.unknown_0xe39482ad,
            'unknown_0xdd8502cc': self.unknown_0xdd8502cc,
            'unknown_0x4ab8cf7d': self.unknown_0x4ab8cf7d,
            'unknown_0xf5e28404': self.unknown_0xf5e28404,
            'grabber_fire_sound': self.grabber_fire_sound,
            'grabber_flight_sound': self.grabber_flight_sound,
            'grabber_hit_player_sound': self.grabber_hit_player_sound,
            'grabber_hit_world_sound': self.grabber_hit_world_sound,
            'grabber_retract_sound': self.grabber_retract_sound,
            'sound_0x64e9152d': self.sound_0x64e9152d,
            'morphball_spit_sound': self.morphball_spit_sound,
            'grabber_explosion_sound': self.grabber_explosion_sound,
            'ball_escape_sound': self.ball_escape_sound,
            'needle_telegraph_sound': self.needle_telegraph_sound,
            'grabber_telegraph_sound': self.grabber_telegraph_sound,
            'power_bomb_guardian_stage_properties_0x510dba97': self.power_bomb_guardian_stage_properties_0x510dba97.to_json(),
            'power_bomb_guardian_stage_properties_0x0b6c85f7': self.power_bomb_guardian_stage_properties_0x0b6c85f7.to_json(),
            'power_bomb_guardian_stage_properties_0x8b9c92e8': self.power_bomb_guardian_stage_properties_0x8b9c92e8.to_json(),
            'power_bomb_guardian_stage_properties_0xbfaefb37': self.power_bomb_guardian_stage_properties_0xbfaefb37.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_tendril_particle_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.tendril_particle_effect)

    def _dependencies_for_wpsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc)

    def _dependencies_for_power_bomb_projectile_damage(self, asset_manager):
        yield from self.power_bomb_projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_grabber_fire_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.grabber_fire_sound)

    def _dependencies_for_grabber_hit_player_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.grabber_hit_player_sound)

    def _dependencies_for_grabber_hit_world_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.grabber_hit_world_sound)

    def _dependencies_for_grabber_retract_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.grabber_retract_sound)

    def _dependencies_for_sound_0x64e9152d(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x64e9152d)

    def _dependencies_for_morphball_spit_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.morphball_spit_sound)

    def _dependencies_for_grabber_explosion_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.grabber_explosion_sound)

    def _dependencies_for_ball_escape_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.ball_escape_sound)

    def _dependencies_for_needle_telegraph_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.needle_telegraph_sound)

    def _dependencies_for_grabber_telegraph_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.grabber_telegraph_sound)

    def _dependencies_for_power_bomb_guardian_stage_properties_0x510dba97(self, asset_manager):
        yield from self.power_bomb_guardian_stage_properties_0x510dba97.dependencies_for(asset_manager)

    def _dependencies_for_power_bomb_guardian_stage_properties_0x0b6c85f7(self, asset_manager):
        yield from self.power_bomb_guardian_stage_properties_0x0b6c85f7.dependencies_for(asset_manager)

    def _dependencies_for_power_bomb_guardian_stage_properties_0x8b9c92e8(self, asset_manager):
        yield from self.power_bomb_guardian_stage_properties_0x8b9c92e8.dependencies_for(asset_manager)

    def _dependencies_for_power_bomb_guardian_stage_properties_0xbfaefb37(self, asset_manager):
        yield from self.power_bomb_guardian_stage_properties_0xbfaefb37.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_tendril_particle_effect, "tendril_particle_effect", "AssetId"),
            (self._dependencies_for_wpsc, "wpsc", "AssetId"),
            (self._dependencies_for_power_bomb_projectile_damage, "power_bomb_projectile_damage", "DamageInfo"),
            (self._dependencies_for_grabber_fire_sound, "grabber_fire_sound", "int"),
            (self._dependencies_for_grabber_hit_player_sound, "grabber_hit_player_sound", "int"),
            (self._dependencies_for_grabber_hit_world_sound, "grabber_hit_world_sound", "int"),
            (self._dependencies_for_grabber_retract_sound, "grabber_retract_sound", "int"),
            (self._dependencies_for_sound_0x64e9152d, "sound_0x64e9152d", "int"),
            (self._dependencies_for_morphball_spit_sound, "morphball_spit_sound", "int"),
            (self._dependencies_for_grabber_explosion_sound, "grabber_explosion_sound", "int"),
            (self._dependencies_for_ball_escape_sound, "ball_escape_sound", "int"),
            (self._dependencies_for_needle_telegraph_sound, "needle_telegraph_sound", "int"),
            (self._dependencies_for_grabber_telegraph_sound, "grabber_telegraph_sound", "int"),
            (self._dependencies_for_power_bomb_guardian_stage_properties_0x510dba97, "power_bomb_guardian_stage_properties_0x510dba97", "PowerBombGuardianStageProperties"),
            (self._dependencies_for_power_bomb_guardian_stage_properties_0x0b6c85f7, "power_bomb_guardian_stage_properties_0x0b6c85f7", "PowerBombGuardianStageProperties"),
            (self._dependencies_for_power_bomb_guardian_stage_properties_0x8b9c92e8, "power_bomb_guardian_stage_properties_0x8b9c92e8", "PowerBombGuardianStageProperties"),
            (self._dependencies_for_power_bomb_guardian_stage_properties_0xbfaefb37, "power_bomb_guardian_stage_properties_0xbfaefb37", "PowerBombGuardianStageProperties"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SporbBase.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_unknown_0x95e7a2c2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x76ba1c18(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3eb2de35(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe50d8dd2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x64d482d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc3e002ac(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_shot_angle_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_aim_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_tendril_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x35557a83(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grabber_out_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grabber_in_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbfddabd4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x62bfaa35(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grabber_attach_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xed82c56a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe918f440(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_force(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grab_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2cfade2c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb68e75cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6d31262b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_power_bomb_guardian(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_wpsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_power_bomb_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_knock_back_power': 2.0})


def _decode_unknown_0x03a76d35(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6d4e0f5a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3538d49b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe89c7707(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x738d1f51(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_0x9480c6d7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x48df4182(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe39482ad(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdd8502cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4ab8cf7d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf5e28404(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grabber_fire_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grabber_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grabber_hit_player_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grabber_hit_world_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grabber_retract_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x64e9152d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_morphball_spit_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grabber_explosion_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ball_escape_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_needle_telegraph_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_grabber_telegraph_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_power_bomb_guardian_stage_properties_0x510dba97(data: typing.BinaryIO, property_size: int):
    return PowerBombGuardianStageProperties.from_stream(data, property_size)


def _decode_power_bomb_guardian_stage_properties_0x0b6c85f7(data: typing.BinaryIO, property_size: int):
    return PowerBombGuardianStageProperties.from_stream(data, property_size)


def _decode_power_bomb_guardian_stage_properties_0x8b9c92e8(data: typing.BinaryIO, property_size: int):
    return PowerBombGuardianStageProperties.from_stream(data, property_size)


def _decode_power_bomb_guardian_stage_properties_0xbfaefb37(data: typing.BinaryIO, property_size: int):
    return PowerBombGuardianStageProperties.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x95e7a2c2: ('unknown_0x95e7a2c2', _decode_unknown_0x95e7a2c2),
    0x76ba1c18: ('unknown_0x76ba1c18', _decode_unknown_0x76ba1c18),
    0x3eb2de35: ('unknown_0x3eb2de35', _decode_unknown_0x3eb2de35),
    0xe50d8dd2: ('unknown_0xe50d8dd2', _decode_unknown_0xe50d8dd2),
    0x64d482d5: ('unknown_0x64d482d5', _decode_unknown_0x64d482d5),
    0xc3e002ac: ('unknown_0xc3e002ac', _decode_unknown_0xc3e002ac),
    0xd75f9cf2: ('shot_angle_variance', _decode_shot_angle_variance),
    0x540c1f87: ('attack_aim_offset', _decode_attack_aim_offset),
    0x33868c8f: ('tendril_particle_effect', _decode_tendril_particle_effect),
    0x35557a83: ('unknown_0x35557a83', _decode_unknown_0x35557a83),
    0x23bd3943: ('grabber_out_acceleration', _decode_grabber_out_acceleration),
    0xd92f485d: ('grabber_in_acceleration', _decode_grabber_in_acceleration),
    0xbfddabd4: ('unknown_0xbfddabd4', _decode_unknown_0xbfddabd4),
    0x62bfaa35: ('unknown_0x62bfaa35', _decode_unknown_0x62bfaa35),
    0x433b5e30: ('grabber_attach_time', _decode_grabber_attach_time),
    0xed82c56a: ('unknown_0xed82c56a', _decode_unknown_0xed82c56a),
    0xe918f440: ('unknown_0xe918f440', _decode_unknown_0xe918f440),
    0x2731ad74: ('spit_force', _decode_spit_force),
    0x3fb2dd4: ('spit_damage', _decode_spit_damage),
    0x95ad8824: ('grab_damage', _decode_grab_damage),
    0x2cfade2c: ('unknown_0x2cfade2c', _decode_unknown_0x2cfade2c),
    0xb68e75cc: ('unknown_0xb68e75cc', _decode_unknown_0xb68e75cc),
    0x6d31262b: ('unknown_0x6d31262b', _decode_unknown_0x6d31262b),
    0xb628855a: ('is_power_bomb_guardian', _decode_is_power_bomb_guardian),
    0x990745dd: ('wpsc', _decode_wpsc),
    0x5f3c27c6: ('power_bomb_projectile_damage', _decode_power_bomb_projectile_damage),
    0x3a76d35: ('unknown_0x03a76d35', _decode_unknown_0x03a76d35),
    0x6d4e0f5a: ('unknown_0x6d4e0f5a', _decode_unknown_0x6d4e0f5a),
    0x3538d49b: ('unknown_0x3538d49b', _decode_unknown_0x3538d49b),
    0xe89c7707: ('unknown_0xe89c7707', _decode_unknown_0xe89c7707),
    0x738d1f51: ('unknown_0x738d1f51', _decode_unknown_0x738d1f51),
    0x9480c6d7: ('sound_0x9480c6d7', _decode_sound_0x9480c6d7),
    0x48df4182: ('unknown_0x48df4182', _decode_unknown_0x48df4182),
    0xe39482ad: ('unknown_0xe39482ad', _decode_unknown_0xe39482ad),
    0xdd8502cc: ('unknown_0xdd8502cc', _decode_unknown_0xdd8502cc),
    0x4ab8cf7d: ('unknown_0x4ab8cf7d', _decode_unknown_0x4ab8cf7d),
    0xf5e28404: ('unknown_0xf5e28404', _decode_unknown_0xf5e28404),
    0xa87d72fc: ('grabber_fire_sound', _decode_grabber_fire_sound),
    0x8661285e: ('grabber_flight_sound', _decode_grabber_flight_sound),
    0x4123323a: ('grabber_hit_player_sound', _decode_grabber_hit_player_sound),
    0x4d2ec538: ('grabber_hit_world_sound', _decode_grabber_hit_world_sound),
    0xd51ca051: ('grabber_retract_sound', _decode_grabber_retract_sound),
    0x64e9152d: ('sound_0x64e9152d', _decode_sound_0x64e9152d),
    0x3acd0ecc: ('morphball_spit_sound', _decode_morphball_spit_sound),
    0xfeb67317: ('grabber_explosion_sound', _decode_grabber_explosion_sound),
    0x88a20db0: ('ball_escape_sound', _decode_ball_escape_sound),
    0x95c1257f: ('needle_telegraph_sound', _decode_needle_telegraph_sound),
    0x2690e216: ('grabber_telegraph_sound', _decode_grabber_telegraph_sound),
    0x510dba97: ('power_bomb_guardian_stage_properties_0x510dba97', _decode_power_bomb_guardian_stage_properties_0x510dba97),
    0xb6c85f7: ('power_bomb_guardian_stage_properties_0x0b6c85f7', _decode_power_bomb_guardian_stage_properties_0x0b6c85f7),
    0x8b9c92e8: ('power_bomb_guardian_stage_properties_0x8b9c92e8', _decode_power_bomb_guardian_stage_properties_0x8b9c92e8),
    0xbfaefb37: ('power_bomb_guardian_stage_properties_0xbfaefb37', _decode_power_bomb_guardian_stage_properties_0xbfaefb37),
}
