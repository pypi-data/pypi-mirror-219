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
from retro_data_structures.properties.echoes.archetypes.UnknownStruct10 import UnknownStruct10
from retro_data_structures.properties.echoes.archetypes.UnknownStruct11 import UnknownStruct11
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class CommandoPirate(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)
    sound: int = dataclasses.field(default=0)
    aggressiveness: float = dataclasses.field(default=10.0)
    cover_check: float = dataclasses.field(default=50.0)
    search_radius: float = dataclasses.field(default=30.0)
    dodge_check: float = dataclasses.field(default=80.0)
    sound_impact: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_hurled: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_death: int = dataclasses.field(default=0, metadata={'sound': True})
    always_ff_0xfca76593: int = dataclasses.field(default=0)
    always_ff_0x467c3d94: int = dataclasses.field(default=0)
    blade_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_projectile: int = dataclasses.field(default=0, metadata={'sound': True})
    hearing_radius: float = dataclasses.field(default=20.0)
    unknown_struct10: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10)
    unknown_struct11: UnknownStruct11 = dataclasses.field(default_factory=UnknownStruct11)
    unknown_0x71587b45: float = dataclasses.field(default=0.10000000149011612)
    unknown_0x7903312e: float = dataclasses.field(default=0.05000000074505806)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'CMDO'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['PirateRagDoll.rel', 'CommandoPirate.rel']

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
        data.write(b'\x00\x17')  # 23 properties

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
        self.patterned.to_stream(data, default_override={'turn_speed': 360.0, 'detection_angle': 90.0, 'average_attack_time': 1.0, 'attack_time_variation': 0.5, 'damage_wait_time': 3.0, 'collision_radius': 0.800000011920929, 'collision_height': 3.0, 'step_up_height': 0.30000001192092896, 'creature_size': 1})
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

        data.write(b'z\xbe\xd4\xce')  # 0x7abed4ce
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound))

        data.write(b'\x95y\xb1\xf2')  # 0x9579b1f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.aggressiveness))

        data.write(b'\xf8\x9a\xb4\x19')  # 0xf89ab419
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.cover_check))

        data.write(b'\xed\x9b\xf5\xa3')  # 0xed9bf5a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.search_radius))

        data.write(b'\xdc6\xe7E')  # 0xdc36e745
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_check))

        data.write(b'\x1b\xb1n\xa5')  # 0x1bb16ea5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_impact))

        data.write(b';\xb3z\x8f')  # 0x3bb37a8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_hurled))

        data.write(b'\xe1`\xb5\x93')  # 0xe160b593
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_death))

        data.write(b'\xfc\xa7e\x93')  # 0xfca76593
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.always_ff_0xfca76593))

        data.write(b'F|=\x94')  # 0x467c3d94
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.always_ff_0x467c3d94))

        data.write(b'\xa5\x91$0')  # 0xa5912430
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.blade_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_knock_back_power': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

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

        data.write(b'\xediH\x8f')  # 0xed69488f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hearing_radius))

        data.write(b'\xfbCRW')  # 0xfb435257
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'8\x8e\x16\xc9')  # 0x388e16c9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct11.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'qX{E')  # 0x71587b45
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x71587b45))

        data.write(b'y\x031.')  # 0x7903312e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7903312e))

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
            sound=data['sound'],
            aggressiveness=data['aggressiveness'],
            cover_check=data['cover_check'],
            search_radius=data['search_radius'],
            dodge_check=data['dodge_check'],
            sound_impact=data['sound_impact'],
            sound_hurled=data['sound_hurled'],
            sound_death=data['sound_death'],
            always_ff_0xfca76593=data['always_ff_0xfca76593'],
            always_ff_0x467c3d94=data['always_ff_0x467c3d94'],
            blade_damage=DamageInfo.from_json(data['blade_damage']),
            projectile=data['projectile'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            sound_projectile=data['sound_projectile'],
            hearing_radius=data['hearing_radius'],
            unknown_struct10=UnknownStruct10.from_json(data['unknown_struct10']),
            unknown_struct11=UnknownStruct11.from_json(data['unknown_struct11']),
            unknown_0x71587b45=data['unknown_0x71587b45'],
            unknown_0x7903312e=data['unknown_0x7903312e'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'ing_possession_data': self.ing_possession_data.to_json(),
            'sound': self.sound,
            'aggressiveness': self.aggressiveness,
            'cover_check': self.cover_check,
            'search_radius': self.search_radius,
            'dodge_check': self.dodge_check,
            'sound_impact': self.sound_impact,
            'sound_hurled': self.sound_hurled,
            'sound_death': self.sound_death,
            'always_ff_0xfca76593': self.always_ff_0xfca76593,
            'always_ff_0x467c3d94': self.always_ff_0x467c3d94,
            'blade_damage': self.blade_damage.to_json(),
            'projectile': self.projectile,
            'projectile_damage': self.projectile_damage.to_json(),
            'sound_projectile': self.sound_projectile,
            'hearing_radius': self.hearing_radius,
            'unknown_struct10': self.unknown_struct10.to_json(),
            'unknown_struct11': self.unknown_struct11.to_json(),
            'unknown_0x71587b45': self.unknown_0x71587b45,
            'unknown_0x7903312e': self.unknown_0x7903312e,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_ing_possession_data(self, asset_manager):
        yield from self.ing_possession_data.dependencies_for(asset_manager)

    def _dependencies_for_sound_impact(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_impact)

    def _dependencies_for_sound_hurled(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_hurled)

    def _dependencies_for_sound_death(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_death)

    def _dependencies_for_blade_damage(self, asset_manager):
        yield from self.blade_damage.dependencies_for(asset_manager)

    def _dependencies_for_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile)

    def _dependencies_for_projectile_damage(self, asset_manager):
        yield from self.projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_sound_projectile(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_projectile)

    def _dependencies_for_unknown_struct10(self, asset_manager):
        yield from self.unknown_struct10.dependencies_for(asset_manager)

    def _dependencies_for_unknown_struct11(self, asset_manager):
        yield from self.unknown_struct11.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_ing_possession_data, "ing_possession_data", "IngPossessionData"),
            (self._dependencies_for_sound_impact, "sound_impact", "int"),
            (self._dependencies_for_sound_hurled, "sound_hurled", "int"),
            (self._dependencies_for_sound_death, "sound_death", "int"),
            (self._dependencies_for_blade_damage, "blade_damage", "DamageInfo"),
            (self._dependencies_for_projectile, "projectile", "AssetId"),
            (self._dependencies_for_projectile_damage, "projectile_damage", "DamageInfo"),
            (self._dependencies_for_sound_projectile, "sound_projectile", "int"),
            (self._dependencies_for_unknown_struct10, "unknown_struct10", "UnknownStruct10"),
            (self._dependencies_for_unknown_struct11, "unknown_struct11", "UnknownStruct11"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for CommandoPirate.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'turn_speed': 360.0, 'detection_angle': 90.0, 'average_attack_time': 1.0, 'attack_time_variation': 0.5, 'damage_wait_time': 3.0, 'collision_radius': 0.800000011920929, 'collision_height': 3.0, 'step_up_height': 0.30000001192092896, 'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


def _decode_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_aggressiveness(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_cover_check(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_search_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_check(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_impact(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_hurled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_sound_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_always_ff_0xfca76593(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_always_ff_0x467c3d94(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_blade_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_knock_back_power': 5.0})


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_sound_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_hearing_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_struct10(data: typing.BinaryIO, property_size: int):
    return UnknownStruct10.from_stream(data, property_size)


def _decode_unknown_struct11(data: typing.BinaryIO, property_size: int):
    return UnknownStruct11.from_stream(data, property_size)


def _decode_unknown_0x71587b45(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7903312e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
    0x7abed4ce: ('sound', _decode_sound),
    0x9579b1f2: ('aggressiveness', _decode_aggressiveness),
    0xf89ab419: ('cover_check', _decode_cover_check),
    0xed9bf5a3: ('search_radius', _decode_search_radius),
    0xdc36e745: ('dodge_check', _decode_dodge_check),
    0x1bb16ea5: ('sound_impact', _decode_sound_impact),
    0x3bb37a8f: ('sound_hurled', _decode_sound_hurled),
    0xe160b593: ('sound_death', _decode_sound_death),
    0xfca76593: ('always_ff_0xfca76593', _decode_always_ff_0xfca76593),
    0x467c3d94: ('always_ff_0x467c3d94', _decode_always_ff_0x467c3d94),
    0xa5912430: ('blade_damage', _decode_blade_damage),
    0xef485db9: ('projectile', _decode_projectile),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0xeac27605: ('sound_projectile', _decode_sound_projectile),
    0xed69488f: ('hearing_radius', _decode_hearing_radius),
    0xfb435257: ('unknown_struct10', _decode_unknown_struct10),
    0x388e16c9: ('unknown_struct11', _decode_unknown_struct11),
    0x71587b45: ('unknown_0x71587b45', _decode_unknown_0x71587b45),
    0x7903312e: ('unknown_0x7903312e', _decode_unknown_0x7903312e),
}
