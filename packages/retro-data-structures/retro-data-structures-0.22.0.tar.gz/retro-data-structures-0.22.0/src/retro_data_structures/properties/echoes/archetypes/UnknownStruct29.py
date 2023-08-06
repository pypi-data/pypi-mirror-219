# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.IngBoostBallGuardianStruct import IngBoostBallGuardianStruct
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Spline import Spline
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class UnknownStruct29(BaseProperty):
    boost_ball_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.7999999523162842, y=1.7999999523162842, z=1.7999999523162842))
    boost_ball_mass: float = dataclasses.field(default=150.0)
    unknown_0xbea96fb7: float = dataclasses.field(default=0.5)
    boost_ball_speed: Spline = dataclasses.field(default_factory=Spline)
    damage_info_0x0e1a78bd: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0x19c3d263: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0xd8047cba: float = dataclasses.field(default=10.0)
    unknown_0x7b21e31a: float = dataclasses.field(default=3.0)
    boost_ball_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    part_0x15534429: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    boost_ball_shield_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    spsc: AssetId = dataclasses.field(metadata={'asset_types': ['SPSC']}, default=default_asset_id)
    sound_bounce: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_into_ball: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_outof_ball: int = dataclasses.field(default=0, metadata={'sound': True})
    sound: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_boost: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_rolling: int = dataclasses.field(default=0, metadata={'sound': True})
    boost_ball_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_0xee69b993: int = dataclasses.field(default=2)
    unknown_0x4b2de673: int = dataclasses.field(default=3)
    search_cone_angle: float = dataclasses.field(default=80.0)
    unknown_0xb0e85d53: float = dataclasses.field(default=0.20000000298023224)
    damage_info_0x5616d5f1: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_info_0xed685533: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part_0xd771ec43: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x2009a977: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x62ab33a2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ing_boost_ball_guardian_struct_0xbab98497: IngBoostBallGuardianStruct = dataclasses.field(default_factory=IngBoostBallGuardianStruct)
    ing_boost_ball_guardian_struct_0xfe18a18f: IngBoostBallGuardianStruct = dataclasses.field(default_factory=IngBoostBallGuardianStruct)
    ing_boost_ball_guardian_struct_0xc2784287: IngBoostBallGuardianStruct = dataclasses.field(default_factory=IngBoostBallGuardianStruct)

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
        data.write(b'\x00\x1f')  # 31 properties

        data.write(b'\xa3"\xf5\x1d')  # 0xa322f51d
        data.write(b'\x00\x0c')  # size
        self.boost_ball_scale.to_stream(data)

        data.write(b'R\x8d\x95\x1e')  # 0x528d951e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.boost_ball_mass))

        data.write(b'\xbe\xa9o\xb7')  # 0xbea96fb7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xbea96fb7))

        data.write(b'\xa2[\x96\xe1')  # 0xa25b96e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.boost_ball_speed.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0e\x1ax\xbd')  # 0xe1a78bd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x0e1a78bd.to_stream(data, default_override={'di_weapon_type': 7, 'di_damage': 30.0, 'di_radius': 1.5, 'di_knock_back_power': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x19\xc3\xd2c')  # 0x19c3d263
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x19c3d263.to_stream(data, default_override={'di_weapon_type': 7, 'di_damage': 30.0, 'di_radius': 1.5, 'di_knock_back_power': 6.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd8\x04|\xba')  # 0xd8047cba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd8047cba))

        data.write(b'{!\xe3\x1a')  # 0x7b21e31a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7b21e31a))

        data.write(b'\x188\x14y')  # 0x18381479
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.boost_ball_model))

        data.write(b'\x15SD)')  # 0x15534429
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x15534429))

        data.write(b'L\xce\xb7\xad')  # 0x4cceb7ad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.boost_ball_shield_effect))

        data.write(b'\xe4\x1c\xb4I')  # 0xe41cb449
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.spsc))

        data.write(b'gX\xbf\x01')  # 0x6758bf01
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_bounce))

        data.write(b'\x8d\x9e\x01O')  # 0x8d9e014f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_into_ball))

        data.write(b'\xe3Z\xe4\xbe')  # 0xe35ae4be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_outof_ball))

        data.write(b'\x9fsr\xb3')  # 0x9f7372b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound))

        data.write(b'\xddi\xa1\x16')  # 0xdd69a116
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_boost))

        data.write(b'\xbfB\xc3\xec')  # 0xbf42c3ec
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_rolling))

        data.write(b'B\xec\xa5#')  # 0x42eca523
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.boost_ball_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xeei\xb9\x93')  # 0xee69b993
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xee69b993))

        data.write(b'K-\xe6s')  # 0x4b2de673
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x4b2de673))

        data.write(b'*ps\xce')  # 0x2a7073ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.search_cone_angle))

        data.write(b'\xb0\xe8]S')  # 0xb0e85d53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb0e85d53))

        data.write(b'V\x16\xd5\xf1')  # 0x5616d5f1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x5616d5f1.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xedhU3')  # 0xed685533
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0xed685533.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd7q\xecC')  # 0xd771ec43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xd771ec43))

        data.write(b' \t\xa9w')  # 0x2009a977
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x2009a977))

        data.write(b'b\xab3\xa2')  # 0x62ab33a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x62ab33a2))

        data.write(b'\xba\xb9\x84\x97')  # 0xbab98497
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_boost_ball_guardian_struct_0xbab98497.to_stream(data, default_override={'locomotion_speed_scale': 1.0, 'ing_spot_speed_scale': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfe\x18\xa1\x8f')  # 0xfe18a18f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_boost_ball_guardian_struct_0xfe18a18f.to_stream(data, default_override={'locomotion_speed_scale': 1.0, 'ing_spot_speed_scale': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2xB\x87')  # 0xc2784287
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_boost_ball_guardian_struct_0xc2784287.to_stream(data, default_override={'locomotion_speed_scale': 1.0, 'ing_spot_speed_scale': 1.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            boost_ball_scale=Vector.from_json(data['boost_ball_scale']),
            boost_ball_mass=data['boost_ball_mass'],
            unknown_0xbea96fb7=data['unknown_0xbea96fb7'],
            boost_ball_speed=Spline.from_json(data['boost_ball_speed']),
            damage_info_0x0e1a78bd=DamageInfo.from_json(data['damage_info_0x0e1a78bd']),
            damage_info_0x19c3d263=DamageInfo.from_json(data['damage_info_0x19c3d263']),
            unknown_0xd8047cba=data['unknown_0xd8047cba'],
            unknown_0x7b21e31a=data['unknown_0x7b21e31a'],
            boost_ball_model=data['boost_ball_model'],
            part_0x15534429=data['part_0x15534429'],
            boost_ball_shield_effect=data['boost_ball_shield_effect'],
            spsc=data['spsc'],
            sound_bounce=data['sound_bounce'],
            sound_into_ball=data['sound_into_ball'],
            sound_outof_ball=data['sound_outof_ball'],
            sound=data['sound'],
            sound_boost=data['sound_boost'],
            sound_rolling=data['sound_rolling'],
            boost_ball_vulnerability=DamageVulnerability.from_json(data['boost_ball_vulnerability']),
            unknown_0xee69b993=data['unknown_0xee69b993'],
            unknown_0x4b2de673=data['unknown_0x4b2de673'],
            search_cone_angle=data['search_cone_angle'],
            unknown_0xb0e85d53=data['unknown_0xb0e85d53'],
            damage_info_0x5616d5f1=DamageInfo.from_json(data['damage_info_0x5616d5f1']),
            damage_info_0xed685533=DamageInfo.from_json(data['damage_info_0xed685533']),
            part_0xd771ec43=data['part_0xd771ec43'],
            part_0x2009a977=data['part_0x2009a977'],
            part_0x62ab33a2=data['part_0x62ab33a2'],
            ing_boost_ball_guardian_struct_0xbab98497=IngBoostBallGuardianStruct.from_json(data['ing_boost_ball_guardian_struct_0xbab98497']),
            ing_boost_ball_guardian_struct_0xfe18a18f=IngBoostBallGuardianStruct.from_json(data['ing_boost_ball_guardian_struct_0xfe18a18f']),
            ing_boost_ball_guardian_struct_0xc2784287=IngBoostBallGuardianStruct.from_json(data['ing_boost_ball_guardian_struct_0xc2784287']),
        )

    def to_json(self) -> dict:
        return {
            'boost_ball_scale': self.boost_ball_scale.to_json(),
            'boost_ball_mass': self.boost_ball_mass,
            'unknown_0xbea96fb7': self.unknown_0xbea96fb7,
            'boost_ball_speed': self.boost_ball_speed.to_json(),
            'damage_info_0x0e1a78bd': self.damage_info_0x0e1a78bd.to_json(),
            'damage_info_0x19c3d263': self.damage_info_0x19c3d263.to_json(),
            'unknown_0xd8047cba': self.unknown_0xd8047cba,
            'unknown_0x7b21e31a': self.unknown_0x7b21e31a,
            'boost_ball_model': self.boost_ball_model,
            'part_0x15534429': self.part_0x15534429,
            'boost_ball_shield_effect': self.boost_ball_shield_effect,
            'spsc': self.spsc,
            'sound_bounce': self.sound_bounce,
            'sound_into_ball': self.sound_into_ball,
            'sound_outof_ball': self.sound_outof_ball,
            'sound': self.sound,
            'sound_boost': self.sound_boost,
            'sound_rolling': self.sound_rolling,
            'boost_ball_vulnerability': self.boost_ball_vulnerability.to_json(),
            'unknown_0xee69b993': self.unknown_0xee69b993,
            'unknown_0x4b2de673': self.unknown_0x4b2de673,
            'search_cone_angle': self.search_cone_angle,
            'unknown_0xb0e85d53': self.unknown_0xb0e85d53,
            'damage_info_0x5616d5f1': self.damage_info_0x5616d5f1.to_json(),
            'damage_info_0xed685533': self.damage_info_0xed685533.to_json(),
            'part_0xd771ec43': self.part_0xd771ec43,
            'part_0x2009a977': self.part_0x2009a977,
            'part_0x62ab33a2': self.part_0x62ab33a2,
            'ing_boost_ball_guardian_struct_0xbab98497': self.ing_boost_ball_guardian_struct_0xbab98497.to_json(),
            'ing_boost_ball_guardian_struct_0xfe18a18f': self.ing_boost_ball_guardian_struct_0xfe18a18f.to_json(),
            'ing_boost_ball_guardian_struct_0xc2784287': self.ing_boost_ball_guardian_struct_0xc2784287.to_json(),
        }

    def _dependencies_for_damage_info_0x0e1a78bd(self, asset_manager):
        yield from self.damage_info_0x0e1a78bd.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_0x19c3d263(self, asset_manager):
        yield from self.damage_info_0x19c3d263.dependencies_for(asset_manager)

    def _dependencies_for_boost_ball_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.boost_ball_model)

    def _dependencies_for_part_0x15534429(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x15534429)

    def _dependencies_for_boost_ball_shield_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.boost_ball_shield_effect)

    def _dependencies_for_spsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.spsc)

    def _dependencies_for_sound_bounce(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_bounce)

    def _dependencies_for_sound_into_ball(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_into_ball)

    def _dependencies_for_sound_outof_ball(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_outof_ball)

    def _dependencies_for_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound)

    def _dependencies_for_sound_boost(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_boost)

    def _dependencies_for_sound_rolling(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_rolling)

    def _dependencies_for_boost_ball_vulnerability(self, asset_manager):
        yield from self.boost_ball_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_0x5616d5f1(self, asset_manager):
        yield from self.damage_info_0x5616d5f1.dependencies_for(asset_manager)

    def _dependencies_for_damage_info_0xed685533(self, asset_manager):
        yield from self.damage_info_0xed685533.dependencies_for(asset_manager)

    def _dependencies_for_part_0xd771ec43(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xd771ec43)

    def _dependencies_for_part_0x2009a977(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x2009a977)

    def _dependencies_for_part_0x62ab33a2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x62ab33a2)

    def _dependencies_for_ing_boost_ball_guardian_struct_0xbab98497(self, asset_manager):
        yield from self.ing_boost_ball_guardian_struct_0xbab98497.dependencies_for(asset_manager)

    def _dependencies_for_ing_boost_ball_guardian_struct_0xfe18a18f(self, asset_manager):
        yield from self.ing_boost_ball_guardian_struct_0xfe18a18f.dependencies_for(asset_manager)

    def _dependencies_for_ing_boost_ball_guardian_struct_0xc2784287(self, asset_manager):
        yield from self.ing_boost_ball_guardian_struct_0xc2784287.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_damage_info_0x0e1a78bd, "damage_info_0x0e1a78bd", "DamageInfo"),
            (self._dependencies_for_damage_info_0x19c3d263, "damage_info_0x19c3d263", "DamageInfo"),
            (self._dependencies_for_boost_ball_model, "boost_ball_model", "AssetId"),
            (self._dependencies_for_part_0x15534429, "part_0x15534429", "AssetId"),
            (self._dependencies_for_boost_ball_shield_effect, "boost_ball_shield_effect", "AssetId"),
            (self._dependencies_for_spsc, "spsc", "AssetId"),
            (self._dependencies_for_sound_bounce, "sound_bounce", "int"),
            (self._dependencies_for_sound_into_ball, "sound_into_ball", "int"),
            (self._dependencies_for_sound_outof_ball, "sound_outof_ball", "int"),
            (self._dependencies_for_sound, "sound", "int"),
            (self._dependencies_for_sound_boost, "sound_boost", "int"),
            (self._dependencies_for_sound_rolling, "sound_rolling", "int"),
            (self._dependencies_for_boost_ball_vulnerability, "boost_ball_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_damage_info_0x5616d5f1, "damage_info_0x5616d5f1", "DamageInfo"),
            (self._dependencies_for_damage_info_0xed685533, "damage_info_0xed685533", "DamageInfo"),
            (self._dependencies_for_part_0xd771ec43, "part_0xd771ec43", "AssetId"),
            (self._dependencies_for_part_0x2009a977, "part_0x2009a977", "AssetId"),
            (self._dependencies_for_part_0x62ab33a2, "part_0x62ab33a2", "AssetId"),
            (self._dependencies_for_ing_boost_ball_guardian_struct_0xbab98497, "ing_boost_ball_guardian_struct_0xbab98497", "IngBoostBallGuardianStruct"),
            (self._dependencies_for_ing_boost_ball_guardian_struct_0xfe18a18f, "ing_boost_ball_guardian_struct_0xfe18a18f", "IngBoostBallGuardianStruct"),
            (self._dependencies_for_ing_boost_ball_guardian_struct_0xc2784287, "ing_boost_ball_guardian_struct_0xc2784287", "IngBoostBallGuardianStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for UnknownStruct29.{field_name} ({field_type}): {e}"
                )


def _decode_boost_ball_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_boost_ball_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xbea96fb7(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_ball_speed(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


def _decode_damage_info_0x0e1a78bd(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 7, 'di_damage': 30.0, 'di_radius': 1.5, 'di_knock_back_power': 4.0})


def _decode_damage_info_0x19c3d263(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 7, 'di_damage': 30.0, 'di_radius': 1.5, 'di_knock_back_power': 6.0})


def _decode_unknown_0xd8047cba(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7b21e31a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_boost_ball_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x15534429(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_boost_ball_shield_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_spsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_bounce(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_into_ball(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_outof_ball(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_boost(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_rolling(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_boost_ball_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_unknown_0xee69b993(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x4b2de673(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_search_cone_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb0e85d53(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info_0x5616d5f1(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 20.0, 'di_knock_back_power': 10.0})


def _decode_damage_info_0xed685533(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_knock_back_power': 5.0})


def _decode_part_0xd771ec43(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x2009a977(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x62ab33a2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ing_boost_ball_guardian_struct_0xbab98497(data: typing.BinaryIO, property_size: int):
    return IngBoostBallGuardianStruct.from_stream(data, property_size, default_override={'locomotion_speed_scale': 1.0, 'ing_spot_speed_scale': 1.0})


def _decode_ing_boost_ball_guardian_struct_0xfe18a18f(data: typing.BinaryIO, property_size: int):
    return IngBoostBallGuardianStruct.from_stream(data, property_size, default_override={'locomotion_speed_scale': 1.0, 'ing_spot_speed_scale': 1.0})


def _decode_ing_boost_ball_guardian_struct_0xc2784287(data: typing.BinaryIO, property_size: int):
    return IngBoostBallGuardianStruct.from_stream(data, property_size, default_override={'locomotion_speed_scale': 1.0, 'ing_spot_speed_scale': 1.0})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa322f51d: ('boost_ball_scale', _decode_boost_ball_scale),
    0x528d951e: ('boost_ball_mass', _decode_boost_ball_mass),
    0xbea96fb7: ('unknown_0xbea96fb7', _decode_unknown_0xbea96fb7),
    0xa25b96e1: ('boost_ball_speed', _decode_boost_ball_speed),
    0xe1a78bd: ('damage_info_0x0e1a78bd', _decode_damage_info_0x0e1a78bd),
    0x19c3d263: ('damage_info_0x19c3d263', _decode_damage_info_0x19c3d263),
    0xd8047cba: ('unknown_0xd8047cba', _decode_unknown_0xd8047cba),
    0x7b21e31a: ('unknown_0x7b21e31a', _decode_unknown_0x7b21e31a),
    0x18381479: ('boost_ball_model', _decode_boost_ball_model),
    0x15534429: ('part_0x15534429', _decode_part_0x15534429),
    0x4cceb7ad: ('boost_ball_shield_effect', _decode_boost_ball_shield_effect),
    0xe41cb449: ('spsc', _decode_spsc),
    0x6758bf01: ('sound_bounce', _decode_sound_bounce),
    0x8d9e014f: ('sound_into_ball', _decode_sound_into_ball),
    0xe35ae4be: ('sound_outof_ball', _decode_sound_outof_ball),
    0x9f7372b3: ('sound', _decode_sound),
    0xdd69a116: ('sound_boost', _decode_sound_boost),
    0xbf42c3ec: ('sound_rolling', _decode_sound_rolling),
    0x42eca523: ('boost_ball_vulnerability', _decode_boost_ball_vulnerability),
    0xee69b993: ('unknown_0xee69b993', _decode_unknown_0xee69b993),
    0x4b2de673: ('unknown_0x4b2de673', _decode_unknown_0x4b2de673),
    0x2a7073ce: ('search_cone_angle', _decode_search_cone_angle),
    0xb0e85d53: ('unknown_0xb0e85d53', _decode_unknown_0xb0e85d53),
    0x5616d5f1: ('damage_info_0x5616d5f1', _decode_damage_info_0x5616d5f1),
    0xed685533: ('damage_info_0xed685533', _decode_damage_info_0xed685533),
    0xd771ec43: ('part_0xd771ec43', _decode_part_0xd771ec43),
    0x2009a977: ('part_0x2009a977', _decode_part_0x2009a977),
    0x62ab33a2: ('part_0x62ab33a2', _decode_part_0x62ab33a2),
    0xbab98497: ('ing_boost_ball_guardian_struct_0xbab98497', _decode_ing_boost_ball_guardian_struct_0xbab98497),
    0xfe18a18f: ('ing_boost_ball_guardian_struct_0xfe18a18f', _decode_ing_boost_ball_guardian_struct_0xfe18a18f),
    0xc2784287: ('ing_boost_ball_guardian_struct_0xc2784287', _decode_ing_boost_ball_guardian_struct_0xc2784287),
}
