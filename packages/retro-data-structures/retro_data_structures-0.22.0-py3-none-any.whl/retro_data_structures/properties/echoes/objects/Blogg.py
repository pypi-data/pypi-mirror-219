# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.BloggStruct import BloggStruct
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.IngPossessionData import IngPossessionData
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Blogg(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    min_attack_angle: float = dataclasses.field(default=30.0)
    max_attack_angle: float = dataclasses.field(default=30.0)
    unknown_0x32455774: float = dataclasses.field(default=2.0)
    unknown_0xc1c8d862: float = dataclasses.field(default=2.0)
    unknown_0xa19d5f62: int = dataclasses.field(default=1)
    projectile_particle_effect: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    body_damage_multiplier: float = dataclasses.field(default=1.0)
    mouth_damage_multiplier: float = dataclasses.field(default=1.0)
    mouth_damage_angle: float = dataclasses.field(default=45.0)
    armor_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    charge_damage_radius: float = dataclasses.field(default=2.0)
    charge_damage: float = dataclasses.field(default=10.0)
    bite_damage: float = dataclasses.field(default=10.0)
    ball_spit_damage: float = dataclasses.field(default=10.0)
    charge_turn_speed: float = dataclasses.field(default=900.0)
    fish_attraction_radius: float = dataclasses.field(default=10.0)
    fish_attraction_priority: float = dataclasses.field(default=0.5)
    aggressiveness: float = dataclasses.field(default=0.5)
    unknown_0x479ccc37: float = dataclasses.field(default=0.75)
    unknown_0x689a803f: float = dataclasses.field(default=1.0)
    unknown_0x800a2b0d: float = dataclasses.field(default=0.30000001192092896)
    charge_speed_multiplier: float = dataclasses.field(default=1.0)
    max_melee_range: float = dataclasses.field(default=10.0)
    unknown_0x6a78c607: float = dataclasses.field(default=20.0)
    unknown_0x2c8d9fc4: float = dataclasses.field(default=5.0)
    unknown_0xd1f82f92: float = dataclasses.field(default=5.0)
    unknown_0x5109fb4e: float = dataclasses.field(default=2.0)
    max_collision_time: float = dataclasses.field(default=0.20000000298023224)
    mouth_open_sound: int = dataclasses.field(default=0)
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)
    ing_possessed_armor_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    is_mega_blogg: bool = dataclasses.field(default=False)
    projectile_blur_radius: float = dataclasses.field(default=4.0)
    projectile_blur_time: float = dataclasses.field(default=4.0)
    blogg_struct_0x3874576d: BloggStruct = dataclasses.field(default_factory=BloggStruct)
    blogg_struct_0x97dd1aa7: BloggStruct = dataclasses.field(default_factory=BloggStruct)
    blogg_struct_0xf2ba21e1: BloggStruct = dataclasses.field(default_factory=BloggStruct)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'BLOG'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Blogg.rel']

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
        data.write(b'\x00)')  # 41 properties

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
        self.patterned.to_stream(data, default_override={'creature_size': 1})
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

        data.write(b'V+\xf3\xfd')  # 0x562bf3fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_attack_angle))

        data.write(b'\xf1\x1fs\x84')  # 0xf11f7384
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_attack_angle))

        data.write(b'2EWt')  # 0x32455774
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x32455774))

        data.write(b'\xc1\xc8\xd8b')  # 0xc1c8d862
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc1c8d862))

        data.write(b'\xa1\x9d_b')  # 0xa19d5f62
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xa19d5f62))

        data.write(b'\x02\xd1\x17n')  # 0x2d1176e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile_particle_effect))

        data.write(b'U;\x139')  # 0x553b1339
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_knock_back_power': 2.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f\x8cLi')  # 0x7f8c4c69
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.body_damage_multiplier))

        data.write(b'l6\xa6\xdd')  # 0x6c36a6dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mouth_damage_multiplier))

        data.write(b'\x10\xff\xe7`')  # 0x10ffe760
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mouth_damage_angle))

        data.write(b'\x89m[\xd9')  # 0x896d5bd9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.armor_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\xd7\x9b\n')  # 0xe7d79b0a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_damage_radius))

        data.write(b'\xb1]\x8a\xf8')  # 0xb15d8af8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_damage))

        data.write(b'R\x10\xcdh')  # 0x5210cd68
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.bite_damage))

        data.write(b'G\x9b\x12$')  # 0x479b1224
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ball_spit_damage))

        data.write(b')\x0e^\x0b')  # 0x290e5e0b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_turn_speed))

        data.write(b'?\xfc\xd8\xae')  # 0x3ffcd8ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fish_attraction_radius))

        data.write(b'\x8b\x1b\x04a')  # 0x8b1b0461
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fish_attraction_priority))

        data.write(b'\x95y\xb1\xf2')  # 0x9579b1f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aggressiveness))

        data.write(b'G\x9c\xcc7')  # 0x479ccc37
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x479ccc37))

        data.write(b'h\x9a\x80?')  # 0x689a803f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x689a803f))

        data.write(b'\x80\n+\r')  # 0x800a2b0d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x800a2b0d))

        data.write(b'\x82\xdfw\xa1')  # 0x82df77a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.charge_speed_multiplier))

        data.write(b'\x98s\xa1\xc1')  # 0x9873a1c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_melee_range))

        data.write(b'jx\xc6\x07')  # 0x6a78c607
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6a78c607))

        data.write(b',\x8d\x9f\xc4')  # 0x2c8d9fc4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2c8d9fc4))

        data.write(b'\xd1\xf8/\x92')  # 0xd1f82f92
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd1f82f92))

        data.write(b'Q\t\xfbN')  # 0x5109fb4e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5109fb4e))

        data.write(b'd\x8a$\x86')  # 0x648a2486
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_collision_time))

        data.write(b'\x04\x19I\xb8')  # 0x41949b8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.mouth_open_sound))

        data.write(b'\xe6\x17H\xed')  # 0xe61748ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_possession_data.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'*\xf6\xff%')  # 0x2af6ff25
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_possessed_armor_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'O\xc9\xdf\xe4')  # 0x4fc9dfe4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_mega_blogg))

        data.write(b'-\xd3f.')  # 0x2dd3662e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_blur_radius))

        data.write(b'oA\xbb\xe7')  # 0x6f41bbe7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_blur_time))

        data.write(b'8tWm')  # 0x3874576d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.blogg_struct_0x3874576d.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x97\xdd\x1a\xa7')  # 0x97dd1aa7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.blogg_struct_0x97dd1aa7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf2\xba!\xe1')  # 0xf2ba21e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.blogg_struct_0xf2ba21e1.to_stream(data)
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
            min_attack_angle=data['min_attack_angle'],
            max_attack_angle=data['max_attack_angle'],
            unknown_0x32455774=data['unknown_0x32455774'],
            unknown_0xc1c8d862=data['unknown_0xc1c8d862'],
            unknown_0xa19d5f62=data['unknown_0xa19d5f62'],
            projectile_particle_effect=data['projectile_particle_effect'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            body_damage_multiplier=data['body_damage_multiplier'],
            mouth_damage_multiplier=data['mouth_damage_multiplier'],
            mouth_damage_angle=data['mouth_damage_angle'],
            armor_vulnerability=DamageVulnerability.from_json(data['armor_vulnerability']),
            charge_damage_radius=data['charge_damage_radius'],
            charge_damage=data['charge_damage'],
            bite_damage=data['bite_damage'],
            ball_spit_damage=data['ball_spit_damage'],
            charge_turn_speed=data['charge_turn_speed'],
            fish_attraction_radius=data['fish_attraction_radius'],
            fish_attraction_priority=data['fish_attraction_priority'],
            aggressiveness=data['aggressiveness'],
            unknown_0x479ccc37=data['unknown_0x479ccc37'],
            unknown_0x689a803f=data['unknown_0x689a803f'],
            unknown_0x800a2b0d=data['unknown_0x800a2b0d'],
            charge_speed_multiplier=data['charge_speed_multiplier'],
            max_melee_range=data['max_melee_range'],
            unknown_0x6a78c607=data['unknown_0x6a78c607'],
            unknown_0x2c8d9fc4=data['unknown_0x2c8d9fc4'],
            unknown_0xd1f82f92=data['unknown_0xd1f82f92'],
            unknown_0x5109fb4e=data['unknown_0x5109fb4e'],
            max_collision_time=data['max_collision_time'],
            mouth_open_sound=data['mouth_open_sound'],
            ing_possession_data=IngPossessionData.from_json(data['ing_possession_data']),
            ing_possessed_armor_vulnerability=DamageVulnerability.from_json(data['ing_possessed_armor_vulnerability']),
            is_mega_blogg=data['is_mega_blogg'],
            projectile_blur_radius=data['projectile_blur_radius'],
            projectile_blur_time=data['projectile_blur_time'],
            blogg_struct_0x3874576d=BloggStruct.from_json(data['blogg_struct_0x3874576d']),
            blogg_struct_0x97dd1aa7=BloggStruct.from_json(data['blogg_struct_0x97dd1aa7']),
            blogg_struct_0xf2ba21e1=BloggStruct.from_json(data['blogg_struct_0xf2ba21e1']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'min_attack_angle': self.min_attack_angle,
            'max_attack_angle': self.max_attack_angle,
            'unknown_0x32455774': self.unknown_0x32455774,
            'unknown_0xc1c8d862': self.unknown_0xc1c8d862,
            'unknown_0xa19d5f62': self.unknown_0xa19d5f62,
            'projectile_particle_effect': self.projectile_particle_effect,
            'projectile_damage': self.projectile_damage.to_json(),
            'body_damage_multiplier': self.body_damage_multiplier,
            'mouth_damage_multiplier': self.mouth_damage_multiplier,
            'mouth_damage_angle': self.mouth_damage_angle,
            'armor_vulnerability': self.armor_vulnerability.to_json(),
            'charge_damage_radius': self.charge_damage_radius,
            'charge_damage': self.charge_damage,
            'bite_damage': self.bite_damage,
            'ball_spit_damage': self.ball_spit_damage,
            'charge_turn_speed': self.charge_turn_speed,
            'fish_attraction_radius': self.fish_attraction_radius,
            'fish_attraction_priority': self.fish_attraction_priority,
            'aggressiveness': self.aggressiveness,
            'unknown_0x479ccc37': self.unknown_0x479ccc37,
            'unknown_0x689a803f': self.unknown_0x689a803f,
            'unknown_0x800a2b0d': self.unknown_0x800a2b0d,
            'charge_speed_multiplier': self.charge_speed_multiplier,
            'max_melee_range': self.max_melee_range,
            'unknown_0x6a78c607': self.unknown_0x6a78c607,
            'unknown_0x2c8d9fc4': self.unknown_0x2c8d9fc4,
            'unknown_0xd1f82f92': self.unknown_0xd1f82f92,
            'unknown_0x5109fb4e': self.unknown_0x5109fb4e,
            'max_collision_time': self.max_collision_time,
            'mouth_open_sound': self.mouth_open_sound,
            'ing_possession_data': self.ing_possession_data.to_json(),
            'ing_possessed_armor_vulnerability': self.ing_possessed_armor_vulnerability.to_json(),
            'is_mega_blogg': self.is_mega_blogg,
            'projectile_blur_radius': self.projectile_blur_radius,
            'projectile_blur_time': self.projectile_blur_time,
            'blogg_struct_0x3874576d': self.blogg_struct_0x3874576d.to_json(),
            'blogg_struct_0x97dd1aa7': self.blogg_struct_0x97dd1aa7.to_json(),
            'blogg_struct_0xf2ba21e1': self.blogg_struct_0xf2ba21e1.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_projectile_particle_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile_particle_effect)

    def _dependencies_for_projectile_damage(self, asset_manager):
        yield from self.projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_armor_vulnerability(self, asset_manager):
        yield from self.armor_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_ing_possession_data(self, asset_manager):
        yield from self.ing_possession_data.dependencies_for(asset_manager)

    def _dependencies_for_ing_possessed_armor_vulnerability(self, asset_manager):
        yield from self.ing_possessed_armor_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_blogg_struct_0x3874576d(self, asset_manager):
        yield from self.blogg_struct_0x3874576d.dependencies_for(asset_manager)

    def _dependencies_for_blogg_struct_0x97dd1aa7(self, asset_manager):
        yield from self.blogg_struct_0x97dd1aa7.dependencies_for(asset_manager)

    def _dependencies_for_blogg_struct_0xf2ba21e1(self, asset_manager):
        yield from self.blogg_struct_0xf2ba21e1.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_projectile_particle_effect, "projectile_particle_effect", "AssetId"),
            (self._dependencies_for_projectile_damage, "projectile_damage", "DamageInfo"),
            (self._dependencies_for_armor_vulnerability, "armor_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_ing_possession_data, "ing_possession_data", "IngPossessionData"),
            (self._dependencies_for_ing_possessed_armor_vulnerability, "ing_possessed_armor_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_blogg_struct_0x3874576d, "blogg_struct_0x3874576d", "BloggStruct"),
            (self._dependencies_for_blogg_struct_0x97dd1aa7, "blogg_struct_0x97dd1aa7", "BloggStruct"),
            (self._dependencies_for_blogg_struct_0xf2ba21e1, "blogg_struct_0xf2ba21e1", "BloggStruct"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Blogg.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_min_attack_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_attack_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x32455774(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc1c8d862(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xa19d5f62(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_projectile_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_knock_back_power': 2.0})


def _decode_body_damage_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mouth_damage_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mouth_damage_angle(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_armor_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_charge_damage_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bite_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ball_spit_damage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fish_attraction_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fish_attraction_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_aggressiveness(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x479ccc37(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x689a803f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x800a2b0d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_charge_speed_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_melee_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6a78c607(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2c8d9fc4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd1f82f92(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5109fb4e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_collision_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mouth_open_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


def _decode_ing_possessed_armor_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_is_mega_blogg(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_projectile_blur_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile_blur_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_blogg_struct_0x3874576d(data: typing.BinaryIO, property_size: int):
    return BloggStruct.from_stream(data, property_size)


def _decode_blogg_struct_0x97dd1aa7(data: typing.BinaryIO, property_size: int):
    return BloggStruct.from_stream(data, property_size)


def _decode_blogg_struct_0xf2ba21e1(data: typing.BinaryIO, property_size: int):
    return BloggStruct.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x562bf3fd: ('min_attack_angle', _decode_min_attack_angle),
    0xf11f7384: ('max_attack_angle', _decode_max_attack_angle),
    0x32455774: ('unknown_0x32455774', _decode_unknown_0x32455774),
    0xc1c8d862: ('unknown_0xc1c8d862', _decode_unknown_0xc1c8d862),
    0xa19d5f62: ('unknown_0xa19d5f62', _decode_unknown_0xa19d5f62),
    0x2d1176e: ('projectile_particle_effect', _decode_projectile_particle_effect),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0x7f8c4c69: ('body_damage_multiplier', _decode_body_damage_multiplier),
    0x6c36a6dd: ('mouth_damage_multiplier', _decode_mouth_damage_multiplier),
    0x10ffe760: ('mouth_damage_angle', _decode_mouth_damage_angle),
    0x896d5bd9: ('armor_vulnerability', _decode_armor_vulnerability),
    0xe7d79b0a: ('charge_damage_radius', _decode_charge_damage_radius),
    0xb15d8af8: ('charge_damage', _decode_charge_damage),
    0x5210cd68: ('bite_damage', _decode_bite_damage),
    0x479b1224: ('ball_spit_damage', _decode_ball_spit_damage),
    0x290e5e0b: ('charge_turn_speed', _decode_charge_turn_speed),
    0x3ffcd8ae: ('fish_attraction_radius', _decode_fish_attraction_radius),
    0x8b1b0461: ('fish_attraction_priority', _decode_fish_attraction_priority),
    0x9579b1f2: ('aggressiveness', _decode_aggressiveness),
    0x479ccc37: ('unknown_0x479ccc37', _decode_unknown_0x479ccc37),
    0x689a803f: ('unknown_0x689a803f', _decode_unknown_0x689a803f),
    0x800a2b0d: ('unknown_0x800a2b0d', _decode_unknown_0x800a2b0d),
    0x82df77a1: ('charge_speed_multiplier', _decode_charge_speed_multiplier),
    0x9873a1c1: ('max_melee_range', _decode_max_melee_range),
    0x6a78c607: ('unknown_0x6a78c607', _decode_unknown_0x6a78c607),
    0x2c8d9fc4: ('unknown_0x2c8d9fc4', _decode_unknown_0x2c8d9fc4),
    0xd1f82f92: ('unknown_0xd1f82f92', _decode_unknown_0xd1f82f92),
    0x5109fb4e: ('unknown_0x5109fb4e', _decode_unknown_0x5109fb4e),
    0x648a2486: ('max_collision_time', _decode_max_collision_time),
    0x41949b8: ('mouth_open_sound', _decode_mouth_open_sound),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
    0x2af6ff25: ('ing_possessed_armor_vulnerability', _decode_ing_possessed_armor_vulnerability),
    0x4fc9dfe4: ('is_mega_blogg', _decode_is_mega_blogg),
    0x2dd3662e: ('projectile_blur_radius', _decode_projectile_blur_radius),
    0x6f41bbe7: ('projectile_blur_time', _decode_projectile_blur_time),
    0x3874576d: ('blogg_struct_0x3874576d', _decode_blogg_struct_0x3874576d),
    0x97dd1aa7: ('blogg_struct_0x97dd1aa7', _decode_blogg_struct_0x97dd1aa7),
    0xf2ba21e1: ('blogg_struct_0xf2ba21e1', _decode_blogg_struct_0xf2ba21e1),
}
