# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class Shrieker(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    buried_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    hostile_accumulate_priority: float = dataclasses.field(default=0.10000000149011612)
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    combat_visor_max_volume: int = dataclasses.field(default=50)
    echo_visor_max_volume: int = dataclasses.field(default=100)
    melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    melee_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0x9b6a4437: float = dataclasses.field(default=1.0)
    melee_attack_time_variation: float = dataclasses.field(default=0.10000000149011612)
    melee_range: float = dataclasses.field(default=4.0)
    hover_height: float = dataclasses.field(default=0.0)
    missile_deflection_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=-1.5))
    missile_deflection_radius: float = dataclasses.field(default=15.0)
    unknown_0xe70ef8a3: float = dataclasses.field(default=1.0)
    sound_missile_deflection: int = dataclasses.field(default=0, metadata={'sound': True})
    dodge_time: float = dataclasses.field(default=3.0)
    dodge_percentage: float = dataclasses.field(default=20.0)
    detection_height: float = dataclasses.field(default=5.0)
    unknown_0x4753beb1: float = dataclasses.field(default=15.0)
    pop_detection_radius: float = dataclasses.field(default=10.0)
    morphball_detection_radius: float = dataclasses.field(default=5.0)
    visibility_change_time: float = dataclasses.field(default=0.5)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SHRK'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Shrieker.rel']

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
        data.write(b'\x00\x1c')  # 28 properties

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
        self.patterned.to_stream(data, default_override={'min_attack_range': 4.5, 'max_attack_range': 30.0, 'average_attack_time': 3.0, 'collision_height': 4.0, 'creature_size': 1})
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

        data.write(b'\xd7s)#')  # 0xd7732923
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.buried_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\x1c\xe5]')  # 0x281ce55d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hostile_accumulate_priority))

        data.write(b'\\\x07/\xd0')  # 0x5c072fd0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 4.5, 'di_knock_back_power': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x0fgk\xd9')  # 0xf676bd9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part))

        data.write(b'U;\x139')  # 0x553b1339
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_knock_back_power': 3.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile))

        data.write(b'mF\\\xc2')  # 0x6d465cc2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.combat_visor_max_volume))

        data.write(b'i\xec\x91\x07')  # 0x69ec9107
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.echo_visor_max_volume))

        data.write(b'\xc9A`4')  # 0xc9416034
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 4.5, 'di_knock_back_power': 4.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'b8\xb4\xb5')  # 0x6238b4b5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.melee_effect))

        data.write(b'\x9bjD7')  # 0x9b6a4437
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x9b6a4437))

        data.write(b'\xbe\x078\xef')  # 0xbe0738ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_attack_time_variation))

        data.write(b'9\xabb\xfb')  # 0x39ab62fb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_range))

        data.write(b'\xc7Y\x98\xaa')  # 0xc75998aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.hover_height))

        data.write(b'z\xb4\xab\x98')  # 0x7ab4ab98
        data.write(b'\x00\x0c')  # size
        self.missile_deflection_offset.to_stream(data)

        data.write(b'\x88\xfa*\xcf')  # 0x88fa2acf
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.missile_deflection_radius))

        data.write(b'\xe7\x0e\xf8\xa3')  # 0xe70ef8a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe70ef8a3))

        data.write(b"\x85'\xb3\x96")  # 0x8527b396
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_missile_deflection))

        data.write(b'gb[\xef')  # 0x67625bef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_time))

        data.write(b'\x1a\xafLC')  # 0x1aaf4c43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.dodge_percentage))

        data.write(b'\x9b\xb6\xcb\xc7')  # 0x9bb6cbc7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_height))

        data.write(b'GS\xbe\xb1')  # 0x4753beb1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4753beb1))

        data.write(b'\xee\x86<\x15')  # 0xee863c15
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pop_detection_radius))

        data.write(b'\xae!\xd2\x1d')  # 0xae21d21d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.morphball_detection_radius))

        data.write(b'=h\x9e\xdd')  # 0x3d689edd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.visibility_change_time))

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
            buried_vulnerability=DamageVulnerability.from_json(data['buried_vulnerability']),
            hostile_accumulate_priority=data['hostile_accumulate_priority'],
            damage_info=DamageInfo.from_json(data['damage_info']),
            part=data['part'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            projectile=data['projectile'],
            combat_visor_max_volume=data['combat_visor_max_volume'],
            echo_visor_max_volume=data['echo_visor_max_volume'],
            melee_damage=DamageInfo.from_json(data['melee_damage']),
            melee_effect=data['melee_effect'],
            unknown_0x9b6a4437=data['unknown_0x9b6a4437'],
            melee_attack_time_variation=data['melee_attack_time_variation'],
            melee_range=data['melee_range'],
            hover_height=data['hover_height'],
            missile_deflection_offset=Vector.from_json(data['missile_deflection_offset']),
            missile_deflection_radius=data['missile_deflection_radius'],
            unknown_0xe70ef8a3=data['unknown_0xe70ef8a3'],
            sound_missile_deflection=data['sound_missile_deflection'],
            dodge_time=data['dodge_time'],
            dodge_percentage=data['dodge_percentage'],
            detection_height=data['detection_height'],
            unknown_0x4753beb1=data['unknown_0x4753beb1'],
            pop_detection_radius=data['pop_detection_radius'],
            morphball_detection_radius=data['morphball_detection_radius'],
            visibility_change_time=data['visibility_change_time'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'buried_vulnerability': self.buried_vulnerability.to_json(),
            'hostile_accumulate_priority': self.hostile_accumulate_priority,
            'damage_info': self.damage_info.to_json(),
            'part': self.part,
            'projectile_damage': self.projectile_damage.to_json(),
            'projectile': self.projectile,
            'combat_visor_max_volume': self.combat_visor_max_volume,
            'echo_visor_max_volume': self.echo_visor_max_volume,
            'melee_damage': self.melee_damage.to_json(),
            'melee_effect': self.melee_effect,
            'unknown_0x9b6a4437': self.unknown_0x9b6a4437,
            'melee_attack_time_variation': self.melee_attack_time_variation,
            'melee_range': self.melee_range,
            'hover_height': self.hover_height,
            'missile_deflection_offset': self.missile_deflection_offset.to_json(),
            'missile_deflection_radius': self.missile_deflection_radius,
            'unknown_0xe70ef8a3': self.unknown_0xe70ef8a3,
            'sound_missile_deflection': self.sound_missile_deflection,
            'dodge_time': self.dodge_time,
            'dodge_percentage': self.dodge_percentage,
            'detection_height': self.detection_height,
            'unknown_0x4753beb1': self.unknown_0x4753beb1,
            'pop_detection_radius': self.pop_detection_radius,
            'morphball_detection_radius': self.morphball_detection_radius,
            'visibility_change_time': self.visibility_change_time,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_buried_vulnerability(self, asset_manager):
        yield from self.buried_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_damage_info(self, asset_manager):
        yield from self.damage_info.dependencies_for(asset_manager)

    def _dependencies_for_part(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part)

    def _dependencies_for_projectile_damage(self, asset_manager):
        yield from self.projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile)

    def _dependencies_for_melee_damage(self, asset_manager):
        yield from self.melee_damage.dependencies_for(asset_manager)

    def _dependencies_for_melee_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.melee_effect)

    def _dependencies_for_sound_missile_deflection(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_missile_deflection)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_buried_vulnerability, "buried_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_damage_info, "damage_info", "DamageInfo"),
            (self._dependencies_for_part, "part", "AssetId"),
            (self._dependencies_for_projectile_damage, "projectile_damage", "DamageInfo"),
            (self._dependencies_for_projectile, "projectile", "AssetId"),
            (self._dependencies_for_melee_damage, "melee_damage", "DamageInfo"),
            (self._dependencies_for_melee_effect, "melee_effect", "AssetId"),
            (self._dependencies_for_sound_missile_deflection, "sound_missile_deflection", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Shrieker.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'min_attack_range': 4.5, 'max_attack_range': 30.0, 'average_attack_time': 3.0, 'collision_height': 4.0, 'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_buried_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_hostile_accumulate_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 4.5, 'di_knock_back_power': 4.0})


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0, 'di_knock_back_power': 3.0})


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_combat_visor_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_echo_visor_max_volume(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 4.5, 'di_knock_back_power': 4.0})


def _decode_melee_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x9b6a4437(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_attack_time_variation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_hover_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_missile_deflection_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_missile_deflection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe70ef8a3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sound_missile_deflection(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dodge_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dodge_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_detection_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x4753beb1(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pop_detection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_morphball_detection_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_visibility_change_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xd7732923: ('buried_vulnerability', _decode_buried_vulnerability),
    0x281ce55d: ('hostile_accumulate_priority', _decode_hostile_accumulate_priority),
    0x5c072fd0: ('damage_info', _decode_damage_info),
    0xf676bd9: ('part', _decode_part),
    0x553b1339: ('projectile_damage', _decode_projectile_damage),
    0xef485db9: ('projectile', _decode_projectile),
    0x6d465cc2: ('combat_visor_max_volume', _decode_combat_visor_max_volume),
    0x69ec9107: ('echo_visor_max_volume', _decode_echo_visor_max_volume),
    0xc9416034: ('melee_damage', _decode_melee_damage),
    0x6238b4b5: ('melee_effect', _decode_melee_effect),
    0x9b6a4437: ('unknown_0x9b6a4437', _decode_unknown_0x9b6a4437),
    0xbe0738ef: ('melee_attack_time_variation', _decode_melee_attack_time_variation),
    0x39ab62fb: ('melee_range', _decode_melee_range),
    0xc75998aa: ('hover_height', _decode_hover_height),
    0x7ab4ab98: ('missile_deflection_offset', _decode_missile_deflection_offset),
    0x88fa2acf: ('missile_deflection_radius', _decode_missile_deflection_radius),
    0xe70ef8a3: ('unknown_0xe70ef8a3', _decode_unknown_0xe70ef8a3),
    0x8527b396: ('sound_missile_deflection', _decode_sound_missile_deflection),
    0x67625bef: ('dodge_time', _decode_dodge_time),
    0x1aaf4c43: ('dodge_percentage', _decode_dodge_percentage),
    0x9bb6cbc7: ('detection_height', _decode_detection_height),
    0x4753beb1: ('unknown_0x4753beb1', _decode_unknown_0x4753beb1),
    0xee863c15: ('pop_detection_radius', _decode_pop_detection_radius),
    0xae21d21d: ('morphball_detection_radius', _decode_morphball_detection_radius),
    0x3d689edd: ('visibility_change_time', _decode_visibility_change_time),
}
