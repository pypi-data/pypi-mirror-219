# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.PlasmaBeamInfo import PlasmaBeamInfo
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class UnknownStruct28(BaseProperty):
    unknown_0x01789abd: int = dataclasses.field(default=0)
    hearing_radius: float = dataclasses.field(default=50.0)
    ing_spot_max_speed: float = dataclasses.field(default=15.0)
    unknown_0x8d42a8d5: float = dataclasses.field(default=7.0)
    unknown_0x84586bfd: float = dataclasses.field(default=25.0)
    unknown_0x50398a06: float = dataclasses.field(default=25.0)
    ing_spot_turn_speed: float = dataclasses.field(default=360.0)
    ing_spot_blob_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ing_spot_hit_normal_damage: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ing_spot_hit_heavy_damage: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ing_spot_death: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_ing_spot_idle: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_ing_spot_move: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0xb392943a: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x24ecc1e9: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_ing_spot_death: int = dataclasses.field(default=0, metadata={'sound': True})
    part_0x3c2d681e: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    srsc: AssetId = dataclasses.field(metadata={'asset_types': ['SRSC']}, default=default_asset_id)
    part_0x3da219c7: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0x23271976: float = dataclasses.field(default=0.3499999940395355)
    part_0x081e9e6c: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0xcb39eccb: float = dataclasses.field(default=15.0)
    unknown_0x587ca175: float = dataclasses.field(default=1.5)
    unknown_0x0bd7d5a9: float = dataclasses.field(default=1.5)
    sound_swarm_move: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x5650366a: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_body_projectile_blaster_middle: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x0c13c5a8: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_0x148b81e4: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x5d0d2c40: float = dataclasses.field(default=15.0)
    unknown_0xc620183a: float = dataclasses.field(default=1.5)
    frustration_time: float = dataclasses.field(default=2.0)
    taunt_chance: float = dataclasses.field(default=25.0)
    aggressiveness: float = dataclasses.field(default=10.0)
    arm_swipe_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    body_projectile_contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xa0d63374: float = dataclasses.field(default=20.0)
    body_projectile_suck_time: float = dataclasses.field(default=5.0)
    body_projectile_splat_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    body_projectile_speed: float = dataclasses.field(default=25.0)
    body_projectile_drop_time: float = dataclasses.field(default=2.0)
    unknown_0xe6ddb662: float = dataclasses.field(default=20.0)
    unknown_0xb57bae86: float = dataclasses.field(default=40.0)
    sound_body_projectile: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_body_projectile_splat_wall: int = dataclasses.field(default=0, metadata={'sound': True})
    body_projectile_odds: float = dataclasses.field(default=70.0)
    unknown_0xfa6edeb5: float = dataclasses.field(default=40.0)
    unknown_0xa9c8c651: float = dataclasses.field(default=100.0)
    mini_portal_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_mini_portal: int = dataclasses.field(default=0, metadata={'sound': True})
    mini_portal_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    mini_portal_beam_info: PlasmaBeamInfo = dataclasses.field(default_factory=PlasmaBeamInfo)
    light_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    light_attenuation: float = dataclasses.field(default=5.0)
    ing_spot_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)

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
        data.write(b'\x007')  # 55 properties

        data.write(b'\x01x\x9a\xbd')  # 0x1789abd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x01789abd))

        data.write(b'\xediH\x8f')  # 0xed69488f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hearing_radius))

        data.write(b'\x95\xb4|\xf9')  # 0x95b47cf9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ing_spot_max_speed))

        data.write(b'\x8dB\xa8\xd5')  # 0x8d42a8d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8d42a8d5))

        data.write(b'\x84Xk\xfd')  # 0x84586bfd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x84586bfd))

        data.write(b'P9\x8a\x06')  # 0x50398a06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x50398a06))

        data.write(b'\xea\xa3\xc3\xf8')  # 0xeaa3c3f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ing_spot_turn_speed))

        data.write(b'\xccZI\x18')  # 0xcc5a4918
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.ing_spot_blob_effect))

        data.write(b'\x88Q\xdc\x01')  # 0x8851dc01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.ing_spot_hit_normal_damage))

        data.write(b']\x01\x10\x0f')  # 0x5d01100f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.ing_spot_hit_heavy_damage))

        data.write(b'\x9aV\x89.')  # 0x9a56892e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.ing_spot_death))

        data.write(b'L\xab0\xa9')  # 0x4cab30a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_ing_spot_idle))

        data.write(b'\x8f\x83\xbes')  # 0x8f83be73
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_ing_spot_move))

        data.write(b'\xb3\x92\x94:')  # 0xb392943a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xb392943a))

        data.write(b'$\xec\xc1\xe9')  # 0x24ecc1e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x24ecc1e9))

        data.write(b'D\x89\x93^')  # 0x4489935e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_ing_spot_death))

        data.write(b'<-h\x1e')  # 0x3c2d681e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x3c2d681e))

        data.write(b'\xd5v\xf3y')  # 0xd576f379
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.srsc))

        data.write(b'=\xa2\x19\xc7')  # 0x3da219c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x3da219c7))

        data.write(b"#'\x19v")  # 0x23271976
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x23271976))

        data.write(b'\x08\x1e\x9el')  # 0x81e9e6c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x081e9e6c))

        data.write(b'\xcb9\xec\xcb')  # 0xcb39eccb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcb39eccb))

        data.write(b'X|\xa1u')  # 0x587ca175
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x587ca175))

        data.write(b'\x0b\xd7\xd5\xa9')  # 0xbd7d5a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x0bd7d5a9))

        data.write(b'\xe8\xea[\xc8')  # 0xe8ea5bc8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_swarm_move))

        data.write(b'VP6j')  # 0x5650366a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x5650366a))

        data.write(b'\xb0\x9a\xf7\x06')  # 0xb09af706
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_body_projectile_blaster_middle))

        data.write(b'\x0c\x13\xc5\xa8')  # 0xc13c5a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x0c13c5a8))

        data.write(b'\x14\x8b\x81\xe4')  # 0x148b81e4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x148b81e4))

        data.write(b']\r,@')  # 0x5d0d2c40
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5d0d2c40))

        data.write(b'\xc6 \x18:')  # 0xc620183a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc620183a))

        data.write(b'}\x19\xc3\xca')  # 0x7d19c3ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.frustration_time))

        data.write(b'\xa7\x7fb\x12')  # 0xa77f6212
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt_chance))

        data.write(b'\x95y\xb1\xf2')  # 0x9579b1f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aggressiveness))

        data.write(b'\x91]\xa3t')  # 0x915da374
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.arm_swipe_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xab%\x8fk')  # 0xab258f6b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.body_projectile_contact_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa0\xd63t')  # 0xa0d63374
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa0d63374))

        data.write(b'\xdf\xea`\xa2')  # 0xdfea60a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.body_projectile_suck_time))

        data.write(b'`\x1c\xc5\xb4')  # 0x601cc5b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.body_projectile_splat_effect))

        data.write(b'\xce\x98\x08 ')  # 0xce980820
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.body_projectile_speed))

        data.write(b'\xb7R\xc1w')  # 0xb752c177
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.body_projectile_drop_time))

        data.write(b'\xe6\xdd\xb6b')  # 0xe6ddb662
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe6ddb662))

        data.write(b'\xb5{\xae\x86')  # 0xb57bae86
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb57bae86))

        data.write(b' %\x85\x8b')  # 0x2025858b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_body_projectile))

        data.write(b'\x19\xf8\xfe\xe6')  # 0x19f8fee6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_body_projectile_splat_wall))

        data.write(b'\xdct\x1f\xbd')  # 0xdc741fbd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.body_projectile_odds))

        data.write(b'\xfan\xde\xb5')  # 0xfa6edeb5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfa6edeb5))

        data.write(b'\xa9\xc8\xc6Q')  # 0xa9c8c651
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xa9c8c651))

        data.write(b'\xa9&\xf8\xa8')  # 0xa926f8a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.mini_portal_effect))

        data.write(b'@Q\xfd\x1a')  # 0x4051fd1a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_mini_portal))

        data.write(b'BJm7')  # 0x424a6d37
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mini_portal_projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9c\x17\th')  # 0x9c170968
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.mini_portal_beam_info.to_stream(data, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd>\xfe}')  # 0xbd3efe7d
        data.write(b'\x00\x10')  # size
        self.light_color.to_stream(data)

        data.write(b'\xd2K\x88\x8f')  # 0xd24b888f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.light_attenuation))

        data.write(b'\x1b\x96\xff\x8b')  # 0x1b96ff8b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_spot_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            unknown_0x01789abd=data['unknown_0x01789abd'],
            hearing_radius=data['hearing_radius'],
            ing_spot_max_speed=data['ing_spot_max_speed'],
            unknown_0x8d42a8d5=data['unknown_0x8d42a8d5'],
            unknown_0x84586bfd=data['unknown_0x84586bfd'],
            unknown_0x50398a06=data['unknown_0x50398a06'],
            ing_spot_turn_speed=data['ing_spot_turn_speed'],
            ing_spot_blob_effect=data['ing_spot_blob_effect'],
            ing_spot_hit_normal_damage=data['ing_spot_hit_normal_damage'],
            ing_spot_hit_heavy_damage=data['ing_spot_hit_heavy_damage'],
            ing_spot_death=data['ing_spot_death'],
            sound_ing_spot_idle=data['sound_ing_spot_idle'],
            sound_ing_spot_move=data['sound_ing_spot_move'],
            sound_0xb392943a=data['sound_0xb392943a'],
            sound_0x24ecc1e9=data['sound_0x24ecc1e9'],
            sound_ing_spot_death=data['sound_ing_spot_death'],
            part_0x3c2d681e=data['part_0x3c2d681e'],
            srsc=data['srsc'],
            part_0x3da219c7=data['part_0x3da219c7'],
            unknown_0x23271976=data['unknown_0x23271976'],
            part_0x081e9e6c=data['part_0x081e9e6c'],
            unknown_0xcb39eccb=data['unknown_0xcb39eccb'],
            unknown_0x587ca175=data['unknown_0x587ca175'],
            unknown_0x0bd7d5a9=data['unknown_0x0bd7d5a9'],
            sound_swarm_move=data['sound_swarm_move'],
            sound_0x5650366a=data['sound_0x5650366a'],
            sound_body_projectile_blaster_middle=data['sound_body_projectile_blaster_middle'],
            sound_0x0c13c5a8=data['sound_0x0c13c5a8'],
            sound_0x148b81e4=data['sound_0x148b81e4'],
            unknown_0x5d0d2c40=data['unknown_0x5d0d2c40'],
            unknown_0xc620183a=data['unknown_0xc620183a'],
            frustration_time=data['frustration_time'],
            taunt_chance=data['taunt_chance'],
            aggressiveness=data['aggressiveness'],
            arm_swipe_damage=DamageInfo.from_json(data['arm_swipe_damage']),
            body_projectile_contact_damage=DamageInfo.from_json(data['body_projectile_contact_damage']),
            unknown_0xa0d63374=data['unknown_0xa0d63374'],
            body_projectile_suck_time=data['body_projectile_suck_time'],
            body_projectile_splat_effect=data['body_projectile_splat_effect'],
            body_projectile_speed=data['body_projectile_speed'],
            body_projectile_drop_time=data['body_projectile_drop_time'],
            unknown_0xe6ddb662=data['unknown_0xe6ddb662'],
            unknown_0xb57bae86=data['unknown_0xb57bae86'],
            sound_body_projectile=data['sound_body_projectile'],
            sound_body_projectile_splat_wall=data['sound_body_projectile_splat_wall'],
            body_projectile_odds=data['body_projectile_odds'],
            unknown_0xfa6edeb5=data['unknown_0xfa6edeb5'],
            unknown_0xa9c8c651=data['unknown_0xa9c8c651'],
            mini_portal_effect=data['mini_portal_effect'],
            sound_mini_portal=data['sound_mini_portal'],
            mini_portal_projectile_damage=DamageInfo.from_json(data['mini_portal_projectile_damage']),
            mini_portal_beam_info=PlasmaBeamInfo.from_json(data['mini_portal_beam_info']),
            light_color=Color.from_json(data['light_color']),
            light_attenuation=data['light_attenuation'],
            ing_spot_vulnerability=DamageVulnerability.from_json(data['ing_spot_vulnerability']),
        )

    def to_json(self) -> dict:
        return {
            'unknown_0x01789abd': self.unknown_0x01789abd,
            'hearing_radius': self.hearing_radius,
            'ing_spot_max_speed': self.ing_spot_max_speed,
            'unknown_0x8d42a8d5': self.unknown_0x8d42a8d5,
            'unknown_0x84586bfd': self.unknown_0x84586bfd,
            'unknown_0x50398a06': self.unknown_0x50398a06,
            'ing_spot_turn_speed': self.ing_spot_turn_speed,
            'ing_spot_blob_effect': self.ing_spot_blob_effect,
            'ing_spot_hit_normal_damage': self.ing_spot_hit_normal_damage,
            'ing_spot_hit_heavy_damage': self.ing_spot_hit_heavy_damage,
            'ing_spot_death': self.ing_spot_death,
            'sound_ing_spot_idle': self.sound_ing_spot_idle,
            'sound_ing_spot_move': self.sound_ing_spot_move,
            'sound_0xb392943a': self.sound_0xb392943a,
            'sound_0x24ecc1e9': self.sound_0x24ecc1e9,
            'sound_ing_spot_death': self.sound_ing_spot_death,
            'part_0x3c2d681e': self.part_0x3c2d681e,
            'srsc': self.srsc,
            'part_0x3da219c7': self.part_0x3da219c7,
            'unknown_0x23271976': self.unknown_0x23271976,
            'part_0x081e9e6c': self.part_0x081e9e6c,
            'unknown_0xcb39eccb': self.unknown_0xcb39eccb,
            'unknown_0x587ca175': self.unknown_0x587ca175,
            'unknown_0x0bd7d5a9': self.unknown_0x0bd7d5a9,
            'sound_swarm_move': self.sound_swarm_move,
            'sound_0x5650366a': self.sound_0x5650366a,
            'sound_body_projectile_blaster_middle': self.sound_body_projectile_blaster_middle,
            'sound_0x0c13c5a8': self.sound_0x0c13c5a8,
            'sound_0x148b81e4': self.sound_0x148b81e4,
            'unknown_0x5d0d2c40': self.unknown_0x5d0d2c40,
            'unknown_0xc620183a': self.unknown_0xc620183a,
            'frustration_time': self.frustration_time,
            'taunt_chance': self.taunt_chance,
            'aggressiveness': self.aggressiveness,
            'arm_swipe_damage': self.arm_swipe_damage.to_json(),
            'body_projectile_contact_damage': self.body_projectile_contact_damage.to_json(),
            'unknown_0xa0d63374': self.unknown_0xa0d63374,
            'body_projectile_suck_time': self.body_projectile_suck_time,
            'body_projectile_splat_effect': self.body_projectile_splat_effect,
            'body_projectile_speed': self.body_projectile_speed,
            'body_projectile_drop_time': self.body_projectile_drop_time,
            'unknown_0xe6ddb662': self.unknown_0xe6ddb662,
            'unknown_0xb57bae86': self.unknown_0xb57bae86,
            'sound_body_projectile': self.sound_body_projectile,
            'sound_body_projectile_splat_wall': self.sound_body_projectile_splat_wall,
            'body_projectile_odds': self.body_projectile_odds,
            'unknown_0xfa6edeb5': self.unknown_0xfa6edeb5,
            'unknown_0xa9c8c651': self.unknown_0xa9c8c651,
            'mini_portal_effect': self.mini_portal_effect,
            'sound_mini_portal': self.sound_mini_portal,
            'mini_portal_projectile_damage': self.mini_portal_projectile_damage.to_json(),
            'mini_portal_beam_info': self.mini_portal_beam_info.to_json(),
            'light_color': self.light_color.to_json(),
            'light_attenuation': self.light_attenuation,
            'ing_spot_vulnerability': self.ing_spot_vulnerability.to_json(),
        }

    def _dependencies_for_ing_spot_blob_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.ing_spot_blob_effect)

    def _dependencies_for_ing_spot_hit_normal_damage(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.ing_spot_hit_normal_damage)

    def _dependencies_for_ing_spot_hit_heavy_damage(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.ing_spot_hit_heavy_damage)

    def _dependencies_for_ing_spot_death(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.ing_spot_death)

    def _dependencies_for_sound_ing_spot_idle(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_ing_spot_idle)

    def _dependencies_for_sound_ing_spot_move(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_ing_spot_move)

    def _dependencies_for_sound_0xb392943a(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xb392943a)

    def _dependencies_for_sound_0x24ecc1e9(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x24ecc1e9)

    def _dependencies_for_sound_ing_spot_death(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_ing_spot_death)

    def _dependencies_for_part_0x3c2d681e(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x3c2d681e)

    def _dependencies_for_srsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.srsc)

    def _dependencies_for_part_0x3da219c7(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x3da219c7)

    def _dependencies_for_part_0x081e9e6c(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x081e9e6c)

    def _dependencies_for_sound_swarm_move(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_swarm_move)

    def _dependencies_for_sound_0x5650366a(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x5650366a)

    def _dependencies_for_sound_body_projectile_blaster_middle(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_body_projectile_blaster_middle)

    def _dependencies_for_sound_0x0c13c5a8(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x0c13c5a8)

    def _dependencies_for_sound_0x148b81e4(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x148b81e4)

    def _dependencies_for_arm_swipe_damage(self, asset_manager):
        yield from self.arm_swipe_damage.dependencies_for(asset_manager)

    def _dependencies_for_body_projectile_contact_damage(self, asset_manager):
        yield from self.body_projectile_contact_damage.dependencies_for(asset_manager)

    def _dependencies_for_body_projectile_splat_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.body_projectile_splat_effect)

    def _dependencies_for_sound_body_projectile(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_body_projectile)

    def _dependencies_for_sound_body_projectile_splat_wall(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_body_projectile_splat_wall)

    def _dependencies_for_mini_portal_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.mini_portal_effect)

    def _dependencies_for_sound_mini_portal(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_mini_portal)

    def _dependencies_for_mini_portal_projectile_damage(self, asset_manager):
        yield from self.mini_portal_projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_mini_portal_beam_info(self, asset_manager):
        yield from self.mini_portal_beam_info.dependencies_for(asset_manager)

    def _dependencies_for_ing_spot_vulnerability(self, asset_manager):
        yield from self.ing_spot_vulnerability.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_ing_spot_blob_effect, "ing_spot_blob_effect", "AssetId"),
            (self._dependencies_for_ing_spot_hit_normal_damage, "ing_spot_hit_normal_damage", "AssetId"),
            (self._dependencies_for_ing_spot_hit_heavy_damage, "ing_spot_hit_heavy_damage", "AssetId"),
            (self._dependencies_for_ing_spot_death, "ing_spot_death", "AssetId"),
            (self._dependencies_for_sound_ing_spot_idle, "sound_ing_spot_idle", "int"),
            (self._dependencies_for_sound_ing_spot_move, "sound_ing_spot_move", "int"),
            (self._dependencies_for_sound_0xb392943a, "sound_0xb392943a", "int"),
            (self._dependencies_for_sound_0x24ecc1e9, "sound_0x24ecc1e9", "int"),
            (self._dependencies_for_sound_ing_spot_death, "sound_ing_spot_death", "int"),
            (self._dependencies_for_part_0x3c2d681e, "part_0x3c2d681e", "AssetId"),
            (self._dependencies_for_srsc, "srsc", "AssetId"),
            (self._dependencies_for_part_0x3da219c7, "part_0x3da219c7", "AssetId"),
            (self._dependencies_for_part_0x081e9e6c, "part_0x081e9e6c", "AssetId"),
            (self._dependencies_for_sound_swarm_move, "sound_swarm_move", "int"),
            (self._dependencies_for_sound_0x5650366a, "sound_0x5650366a", "int"),
            (self._dependencies_for_sound_body_projectile_blaster_middle, "sound_body_projectile_blaster_middle", "int"),
            (self._dependencies_for_sound_0x0c13c5a8, "sound_0x0c13c5a8", "int"),
            (self._dependencies_for_sound_0x148b81e4, "sound_0x148b81e4", "int"),
            (self._dependencies_for_arm_swipe_damage, "arm_swipe_damage", "DamageInfo"),
            (self._dependencies_for_body_projectile_contact_damage, "body_projectile_contact_damage", "DamageInfo"),
            (self._dependencies_for_body_projectile_splat_effect, "body_projectile_splat_effect", "AssetId"),
            (self._dependencies_for_sound_body_projectile, "sound_body_projectile", "int"),
            (self._dependencies_for_sound_body_projectile_splat_wall, "sound_body_projectile_splat_wall", "int"),
            (self._dependencies_for_mini_portal_effect, "mini_portal_effect", "AssetId"),
            (self._dependencies_for_sound_mini_portal, "sound_mini_portal", "int"),
            (self._dependencies_for_mini_portal_projectile_damage, "mini_portal_projectile_damage", "DamageInfo"),
            (self._dependencies_for_mini_portal_beam_info, "mini_portal_beam_info", "PlasmaBeamInfo"),
            (self._dependencies_for_ing_spot_vulnerability, "ing_spot_vulnerability", "DamageVulnerability"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct28.{field_name} ({field_type}): {e}"
                )


def _decode_unknown_0x01789abd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_hearing_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ing_spot_max_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8d42a8d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x84586bfd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x50398a06(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ing_spot_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ing_spot_blob_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ing_spot_hit_normal_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ing_spot_hit_heavy_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ing_spot_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_ing_spot_idle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_ing_spot_move(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0xb392943a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x24ecc1e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_ing_spot_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_part_0x3c2d681e(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_srsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x3da219c7(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x23271976(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_part_0x081e9e6c(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0xcb39eccb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x587ca175(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x0bd7d5a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_swarm_move(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x5650366a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_body_projectile_blaster_middle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x0c13c5a8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_0x148b81e4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x5d0d2c40(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc620183a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_frustration_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_taunt_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_aggressiveness(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_arm_swipe_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_body_projectile_contact_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 5.0})


def _decode_unknown_0xa0d63374(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_body_projectile_suck_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_body_projectile_splat_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_body_projectile_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_body_projectile_drop_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe6ddb662(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb57bae86(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_body_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_body_projectile_splat_wall(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_body_projectile_odds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfa6edeb5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa9c8c651(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mini_portal_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_mini_portal(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mini_portal_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_mini_portal_beam_info(data: typing.BinaryIO, property_size: int):
    return PlasmaBeamInfo.from_stream(data, property_size, default_override={'length': 500.0, 'expansion_speed': 4.0, 'life_time': 1.0, 'pulse_speed': 20.0, 'shutdown_time': 0.25, 'pulse_effect_scale': 2.0, 'inner_color': Color(r=0.49803900718688965, g=0.49803900718688965, b=0.49803900718688965, a=0.49803900718688965), 'outer_color': Color(r=0.6000000238418579, g=0.6000000238418579, b=0.0, a=0.49803900718688965)})


def _decode_light_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_light_attenuation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ing_spot_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x1789abd: ('unknown_0x01789abd', _decode_unknown_0x01789abd),
    0xed69488f: ('hearing_radius', _decode_hearing_radius),
    0x95b47cf9: ('ing_spot_max_speed', _decode_ing_spot_max_speed),
    0x8d42a8d5: ('unknown_0x8d42a8d5', _decode_unknown_0x8d42a8d5),
    0x84586bfd: ('unknown_0x84586bfd', _decode_unknown_0x84586bfd),
    0x50398a06: ('unknown_0x50398a06', _decode_unknown_0x50398a06),
    0xeaa3c3f8: ('ing_spot_turn_speed', _decode_ing_spot_turn_speed),
    0xcc5a4918: ('ing_spot_blob_effect', _decode_ing_spot_blob_effect),
    0x8851dc01: ('ing_spot_hit_normal_damage', _decode_ing_spot_hit_normal_damage),
    0x5d01100f: ('ing_spot_hit_heavy_damage', _decode_ing_spot_hit_heavy_damage),
    0x9a56892e: ('ing_spot_death', _decode_ing_spot_death),
    0x4cab30a9: ('sound_ing_spot_idle', _decode_sound_ing_spot_idle),
    0x8f83be73: ('sound_ing_spot_move', _decode_sound_ing_spot_move),
    0xb392943a: ('sound_0xb392943a', _decode_sound_0xb392943a),
    0x24ecc1e9: ('sound_0x24ecc1e9', _decode_sound_0x24ecc1e9),
    0x4489935e: ('sound_ing_spot_death', _decode_sound_ing_spot_death),
    0x3c2d681e: ('part_0x3c2d681e', _decode_part_0x3c2d681e),
    0xd576f379: ('srsc', _decode_srsc),
    0x3da219c7: ('part_0x3da219c7', _decode_part_0x3da219c7),
    0x23271976: ('unknown_0x23271976', _decode_unknown_0x23271976),
    0x81e9e6c: ('part_0x081e9e6c', _decode_part_0x081e9e6c),
    0xcb39eccb: ('unknown_0xcb39eccb', _decode_unknown_0xcb39eccb),
    0x587ca175: ('unknown_0x587ca175', _decode_unknown_0x587ca175),
    0xbd7d5a9: ('unknown_0x0bd7d5a9', _decode_unknown_0x0bd7d5a9),
    0xe8ea5bc8: ('sound_swarm_move', _decode_sound_swarm_move),
    0x5650366a: ('sound_0x5650366a', _decode_sound_0x5650366a),
    0xb09af706: ('sound_body_projectile_blaster_middle', _decode_sound_body_projectile_blaster_middle),
    0xc13c5a8: ('sound_0x0c13c5a8', _decode_sound_0x0c13c5a8),
    0x148b81e4: ('sound_0x148b81e4', _decode_sound_0x148b81e4),
    0x5d0d2c40: ('unknown_0x5d0d2c40', _decode_unknown_0x5d0d2c40),
    0xc620183a: ('unknown_0xc620183a', _decode_unknown_0xc620183a),
    0x7d19c3ca: ('frustration_time', _decode_frustration_time),
    0xa77f6212: ('taunt_chance', _decode_taunt_chance),
    0x9579b1f2: ('aggressiveness', _decode_aggressiveness),
    0x915da374: ('arm_swipe_damage', _decode_arm_swipe_damage),
    0xab258f6b: ('body_projectile_contact_damage', _decode_body_projectile_contact_damage),
    0xa0d63374: ('unknown_0xa0d63374', _decode_unknown_0xa0d63374),
    0xdfea60a2: ('body_projectile_suck_time', _decode_body_projectile_suck_time),
    0x601cc5b4: ('body_projectile_splat_effect', _decode_body_projectile_splat_effect),
    0xce980820: ('body_projectile_speed', _decode_body_projectile_speed),
    0xb752c177: ('body_projectile_drop_time', _decode_body_projectile_drop_time),
    0xe6ddb662: ('unknown_0xe6ddb662', _decode_unknown_0xe6ddb662),
    0xb57bae86: ('unknown_0xb57bae86', _decode_unknown_0xb57bae86),
    0x2025858b: ('sound_body_projectile', _decode_sound_body_projectile),
    0x19f8fee6: ('sound_body_projectile_splat_wall', _decode_sound_body_projectile_splat_wall),
    0xdc741fbd: ('body_projectile_odds', _decode_body_projectile_odds),
    0xfa6edeb5: ('unknown_0xfa6edeb5', _decode_unknown_0xfa6edeb5),
    0xa9c8c651: ('unknown_0xa9c8c651', _decode_unknown_0xa9c8c651),
    0xa926f8a8: ('mini_portal_effect', _decode_mini_portal_effect),
    0x4051fd1a: ('sound_mini_portal', _decode_sound_mini_portal),
    0x424a6d37: ('mini_portal_projectile_damage', _decode_mini_portal_projectile_damage),
    0x9c170968: ('mini_portal_beam_info', _decode_mini_portal_beam_info),
    0xbd3efe7d: ('light_color', _decode_light_color),
    0xd24b888f: ('light_attenuation', _decode_light_attenuation),
    0x1b96ff8b: ('ing_spot_vulnerability', _decode_ing_spot_vulnerability),
}
