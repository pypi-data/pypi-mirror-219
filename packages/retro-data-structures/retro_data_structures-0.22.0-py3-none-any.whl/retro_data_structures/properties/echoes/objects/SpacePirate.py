# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.IngPossessionData import IngPossessionData
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.archetypes.SpacePirateWeaponData import SpacePirateWeaponData
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class SpacePirate(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)
    aggressiveness: float = dataclasses.field(default=10.0)
    cover_check: float = dataclasses.field(default=50.0)
    search_radius: float = dataclasses.field(default=20.0)
    fall_back_check: float = dataclasses.field(default=20.0)
    fall_back_radius: float = dataclasses.field(default=10.0)
    hearing_radius: float = dataclasses.field(default=20.0)
    sound: int = dataclasses.field(default=0)
    unknown_0xce670970: bool = dataclasses.field(default=False)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_projectile: int = dataclasses.field(default=0, metadata={'sound': True})
    blade_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    kneel_attack_chance: float = dataclasses.field(default=10.0)
    kneel_attack_shot: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    kneel_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    dodge_check: float = dataclasses.field(default=80.0)
    sound_impact: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x71587b45: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x7903312e: float = dataclasses.field(default=0.05000000074505806)
    unknown_0x5080162a: float = dataclasses.field(default=0.10000000149011612)
    unknown_0xc78b40e0: float = dataclasses.field(default=0.05000000074505806)
    sound_alert: int = dataclasses.field(default=0)
    gun_track_delay: float = dataclasses.field(default=1.0)
    unknown_0x1b454a27: int = dataclasses.field(default=0)
    cloak_opacity: float = dataclasses.field(default=0.10000000149011612)
    max_cloak_opacity: float = dataclasses.field(default=0.75)
    unknown_0x61e801d4: float = dataclasses.field(default=5.0)
    unknown_0xf19b113e: float = dataclasses.field(default=10.0)
    sound_hurled: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_death: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x8708b7d3: float = dataclasses.field(default=0.20000000298023224)
    avoid_distance: float = dataclasses.field(default=10.0)
    weapon_data: SpacePirateWeaponData = dataclasses.field(default_factory=SpacePirateWeaponData)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'PIRT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['PirateRagDoll.rel', 'SpacePirate.rel']

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
        data.write(b'\x00%')  # 37 properties

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
        self.patterned.to_stream(data, default_override={'turn_speed': 360.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'average_attack_time': 1.0, 'attack_time_variation': 0.5, 'damage_wait_time': 3.0, 'collision_radius': 0.800000011920929, 'collision_height': 3.0, 'step_up_height': 0.30000001192092896, 'creature_size': 1})
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

        data.write(b'\xe6\x17H\xed')  # 0xe61748ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_possession_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x95y\xb1\xf2')  # 0x9579b1f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aggressiveness))

        data.write(b'\xf8\x9a\xb4\x19')  # 0xf89ab419
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cover_check))

        data.write(b'\xed\x9b\xf5\xa3')  # 0xed9bf5a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.search_radius))

        data.write(b'\xc3\xa2|\xf8')  # 0xc3a27cf8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fall_back_check))

        data.write(b'\xf0\xcf]\xd7')  # 0xf0cf5dd7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fall_back_radius))

        data.write(b'\xediH\x8f')  # 0xed69488f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hearing_radius))

        data.write(b'\xa6J\xb9\xb8')  # 0xa64ab9b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound))

        data.write(b'\xceg\tp')  # 0xce670970
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xce670970))

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile))

        data.write(b'U;\x139')  # 0x553b1339
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xea\xc2v\x05')  # 0xeac27605
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_projectile))

        data.write(b'\xa5\x91$0')  # 0xa5912430
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.blade_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'O@\x87\xed')  # 0x4f4087ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.kneel_attack_chance))

        data.write(b'\xda\x11"\xeb')  # 0xda1122eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.kneel_attack_shot))

        data.write(b'D\x149!')  # 0x44143921
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.kneel_attack_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xdc6\xe7E')  # 0xdc36e745
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_check))

        data.write(b'\x1b\xb1n\xa5')  # 0x1bb16ea5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_impact))

        data.write(b'qX{E')  # 0x71587b45
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x71587b45))

        data.write(b'y\x031.')  # 0x7903312e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7903312e))

        data.write(b'P\x80\x16*')  # 0x5080162a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5080162a))

        data.write(b'\xc7\x8b@\xe0')  # 0xc78b40e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc78b40e0))

        data.write(b'8d1\xac')  # 0x386431ac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_alert))

        data.write(b'\xb2\xac-\x96')  # 0xb2ac2d96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gun_track_delay))

        data.write(b"\x1bEJ'")  # 0x1b454a27
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x1b454a27))

        data.write(b'[\xc6\xf1\xd5')  # 0x5bc6f1d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cloak_opacity))

        data.write(b'|\x02\x1d~')  # 0x7c021d7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_cloak_opacity))

        data.write(b'a\xe8\x01\xd4')  # 0x61e801d4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x61e801d4))

        data.write(b'\xf1\x9b\x11>')  # 0xf19b113e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf19b113e))

        data.write(b';\xb3z\x8f')  # 0x3bb37a8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_hurled))

        data.write(b'\xe1`\xb5\x93')  # 0xe160b593
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_death))

        data.write(b'\x87\x08\xb7\xd3')  # 0x8708b7d3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8708b7d3))

        data.write(b'+\x19\xcd\x88')  # 0x2b19cd88
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.avoid_distance))

        data.write(b'\xdc\x89\xcc<')  # 0xdc89cc3c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.weapon_data.to_stream(data)
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
            ing_possession_data=IngPossessionData.from_json(data['ing_possession_data']),
            aggressiveness=data['aggressiveness'],
            cover_check=data['cover_check'],
            search_radius=data['search_radius'],
            fall_back_check=data['fall_back_check'],
            fall_back_radius=data['fall_back_radius'],
            hearing_radius=data['hearing_radius'],
            sound=data['sound'],
            unknown_0xce670970=data['unknown_0xce670970'],
            projectile=data['projectile'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            sound_projectile=data['sound_projectile'],
            blade_damage=DamageInfo.from_json(data['blade_damage']),
            kneel_attack_chance=data['kneel_attack_chance'],
            kneel_attack_shot=data['kneel_attack_shot'],
            kneel_attack_damage=DamageInfo.from_json(data['kneel_attack_damage']),
            dodge_check=data['dodge_check'],
            sound_impact=data['sound_impact'],
            unknown_0x71587b45=data['unknown_0x71587b45'],
            unknown_0x7903312e=data['unknown_0x7903312e'],
            unknown_0x5080162a=data['unknown_0x5080162a'],
            unknown_0xc78b40e0=data['unknown_0xc78b40e0'],
            sound_alert=data['sound_alert'],
            gun_track_delay=data['gun_track_delay'],
            unknown_0x1b454a27=data['unknown_0x1b454a27'],
            cloak_opacity=data['cloak_opacity'],
            max_cloak_opacity=data['max_cloak_opacity'],
            unknown_0x61e801d4=data['unknown_0x61e801d4'],
            unknown_0xf19b113e=data['unknown_0xf19b113e'],
            sound_hurled=data['sound_hurled'],
            sound_death=data['sound_death'],
            unknown_0x8708b7d3=data['unknown_0x8708b7d3'],
            avoid_distance=data['avoid_distance'],
            weapon_data=SpacePirateWeaponData.from_json(data['weapon_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'ing_possession_data': self.ing_possession_data.to_json(),
            'aggressiveness': self.aggressiveness,
            'cover_check': self.cover_check,
            'search_radius': self.search_radius,
            'fall_back_check': self.fall_back_check,
            'fall_back_radius': self.fall_back_radius,
            'hearing_radius': self.hearing_radius,
            'sound': self.sound,
            'unknown_0xce670970': self.unknown_0xce670970,
            'projectile': self.projectile,
            'projectile_damage': self.projectile_damage.to_json(),
            'sound_projectile': self.sound_projectile,
            'blade_damage': self.blade_damage.to_json(),
            'kneel_attack_chance': self.kneel_attack_chance,
            'kneel_attack_shot': self.kneel_attack_shot,
            'kneel_attack_damage': self.kneel_attack_damage.to_json(),
            'dodge_check': self.dodge_check,
            'sound_impact': self.sound_impact,
            'unknown_0x71587b45': self.unknown_0x71587b45,
            'unknown_0x7903312e': self.unknown_0x7903312e,
            'unknown_0x5080162a': self.unknown_0x5080162a,
            'unknown_0xc78b40e0': self.unknown_0xc78b40e0,
            'sound_alert': self.sound_alert,
            'gun_track_delay': self.gun_track_delay,
            'unknown_0x1b454a27': self.unknown_0x1b454a27,
            'cloak_opacity': self.cloak_opacity,
            'max_cloak_opacity': self.max_cloak_opacity,
            'unknown_0x61e801d4': self.unknown_0x61e801d4,
            'unknown_0xf19b113e': self.unknown_0xf19b113e,
            'sound_hurled': self.sound_hurled,
            'sound_death': self.sound_death,
            'unknown_0x8708b7d3': self.unknown_0x8708b7d3,
            'avoid_distance': self.avoid_distance,
            'weapon_data': self.weapon_data.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_ing_possession_data(self, asset_manager):
        yield from self.ing_possession_data.dependencies_for(asset_manager)

    def _dependencies_for_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile)

    def _dependencies_for_projectile_damage(self, asset_manager):
        yield from self.projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_projectile(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_projectile)

    def _dependencies_for_blade_damage(self, asset_manager):
        yield from self.blade_damage.dependencies_for(asset_manager)

    def _dependencies_for_kneel_attack_shot(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.kneel_attack_shot)

    def _dependencies_for_kneel_attack_damage(self, asset_manager):
        yield from self.kneel_attack_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_impact(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_impact)

    def _dependencies_for_sound_hurled(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_hurled)

    def _dependencies_for_sound_death(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_death)

    def _dependencies_for_weapon_data(self, asset_manager):
        yield from self.weapon_data.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_ing_possession_data, "ing_possession_data", "IngPossessionData"),
            (self._dependencies_for_projectile, "projectile", "AssetId"),
            (self._dependencies_for_projectile_damage, "projectile_damage", "DamageInfo"),
            (self._dependencies_for_sound_projectile, "sound_projectile", "int"),
            (self._dependencies_for_blade_damage, "blade_damage", "DamageInfo"),
            (self._dependencies_for_kneel_attack_shot, "kneel_attack_shot", "AssetId"),
            (self._dependencies_for_kneel_attack_damage, "kneel_attack_damage", "DamageInfo"),
            (self._dependencies_for_sound_impact, "sound_impact", "int"),
            (self._dependencies_for_sound_hurled, "sound_hurled", "int"),
            (self._dependencies_for_sound_death, "sound_death", "int"),
            (self._dependencies_for_weapon_data, "weapon_data", "SpacePirateWeaponData"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SpacePirate.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'turn_speed': 360.0, 'detection_angle': 90.0, 'min_attack_range': 4.0, 'average_attack_time': 1.0, 'attack_time_variation': 0.5, 'damage_wait_time': 3.0, 'collision_radius': 0.800000011920929, 'collision_height': 3.0, 'step_up_height': 0.30000001192092896, 'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


def _decode_aggressiveness(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cover_check(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_search_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fall_back_check(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fall_back_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hearing_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xce670970(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_sound_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_blade_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_knock_back_power': 5.0})


def _decode_kneel_attack_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_kneel_attack_shot(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_kneel_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0})


def _decode_dodge_check(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_impact(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x71587b45(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7903312e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5080162a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc78b40e0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_alert(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_gun_track_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1b454a27(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_cloak_opacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_cloak_opacity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x61e801d4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf19b113e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_hurled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x8708b7d3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_avoid_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_weapon_data(data: typing.BinaryIO, property_size: int):
    return SpacePirateWeaponData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
    0x9579b1f2: ('aggressiveness', _decode_aggressiveness),
    0xf89ab419: ('cover_check', _decode_cover_check),
    0xed9bf5a3: ('search_radius', _decode_search_radius),
    0xc3a27cf8: ('fall_back_check', _decode_fall_back_check),
    0xf0cf5dd7: ('fall_back_radius', _decode_fall_back_radius),
    0xed69488f: ('hearing_radius', _decode_hearing_radius),
    0xa64ab9b8: ('sound', _decode_sound),
    0xce670970: ('unknown_0xce670970', _decode_unknown_0xce670970),
    0xef485db9: ('projectile', _decode_projectile),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0xeac27605: ('sound_projectile', _decode_sound_projectile),
    0xa5912430: ('blade_damage', _decode_blade_damage),
    0x4f4087ed: ('kneel_attack_chance', _decode_kneel_attack_chance),
    0xda1122eb: ('kneel_attack_shot', _decode_kneel_attack_shot),
    0x44143921: ('kneel_attack_damage', _decode_kneel_attack_damage),
    0xdc36e745: ('dodge_check', _decode_dodge_check),
    0x1bb16ea5: ('sound_impact', _decode_sound_impact),
    0x71587b45: ('unknown_0x71587b45', _decode_unknown_0x71587b45),
    0x7903312e: ('unknown_0x7903312e', _decode_unknown_0x7903312e),
    0x5080162a: ('unknown_0x5080162a', _decode_unknown_0x5080162a),
    0xc78b40e0: ('unknown_0xc78b40e0', _decode_unknown_0xc78b40e0),
    0x386431ac: ('sound_alert', _decode_sound_alert),
    0xb2ac2d96: ('gun_track_delay', _decode_gun_track_delay),
    0x1b454a27: ('unknown_0x1b454a27', _decode_unknown_0x1b454a27),
    0x5bc6f1d5: ('cloak_opacity', _decode_cloak_opacity),
    0x7c021d7e: ('max_cloak_opacity', _decode_max_cloak_opacity),
    0x61e801d4: ('unknown_0x61e801d4', _decode_unknown_0x61e801d4),
    0xf19b113e: ('unknown_0xf19b113e', _decode_unknown_0xf19b113e),
    0x3bb37a8f: ('sound_hurled', _decode_sound_hurled),
    0xe160b593: ('sound_death', _decode_sound_death),
    0x8708b7d3: ('unknown_0x8708b7d3', _decode_unknown_0x8708b7d3),
    0x2b19cd88: ('avoid_distance', _decode_avoid_distance),
    0xdc89cc3c: ('weapon_data', _decode_weapon_data),
}
