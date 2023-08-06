# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
import retro_data_structures.enums.prime as enums
from retro_data_structures.properties.prime.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class SpacePirate(BaseObjectType):
    name: str = dataclasses.field(default='')
    position: Vector = dataclasses.field(default_factory=Vector)
    rotation: Vector = dataclasses.field(default_factory=Vector)
    scale: Vector = dataclasses.field(default_factory=Vector)
    unnamed_0x00000004: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    unnamed_0x00000005: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    aggression_check: float = dataclasses.field(default=0.0)
    cover_check: float = dataclasses.field(default=0.0)
    search_radius: float = dataclasses.field(default=0.0)
    fallback_check: float = dataclasses.field(default=0.0)
    fallback_radius: float = dataclasses.field(default=0.0)
    hearing_radius: float = dataclasses.field(default=0.0)
    flags: enums.Flags = dataclasses.field(default=enums.Flags(0))
    unknown_8: bool = dataclasses.field(default=False)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    sound_projectile: int = dataclasses.field(default=0, metadata={'sound': True})
    blade_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    kneel_attack_chance: float = dataclasses.field(default=0.0)
    kneel_attack_shot: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    kneel_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    dodge_check: float = dataclasses.field(default=0.0)
    sound_impact: int = dataclasses.field(default=0, metadata={'sound': True})
    average_next_shot_time: float = dataclasses.field(default=0.0)
    next_shot_time_variation: float = dataclasses.field(default=0.0)
    sound_alert: int = dataclasses.field(default=0, metadata={'sound': True})
    gun_track_delay: float = dataclasses.field(default=0.0)
    first_burst_count: int = dataclasses.field(default=0)
    cloak_opacity: float = dataclasses.field(default=0.0)
    max_cloak_opacity: float = dataclasses.field(default=0.0)
    dodge_delay_time_min: float = dataclasses.field(default=0.0)
    dodge_delay_time_max: float = dataclasses.field(default=0.0)
    sound_hurled: int = dataclasses.field(default=0, metadata={'sound': True})
    sound_death: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_19: float = dataclasses.field(default=0.0)
    avoid_distance: float = dataclasses.field(default=0.0)

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    def get_name(self) -> typing.Optional[str]:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    @classmethod
    def object_type(cls) -> int:
        return 0x24

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        property_count = struct.unpack(">L", data.read(4))[0]
        name = b"".join(iter(lambda: data.read(1), b'\x00')).decode("utf-8")
        position = Vector.from_stream(data)
        rotation = Vector.from_stream(data)
        scale = Vector.from_stream(data)
        unnamed_0x00000004 = PatternedAITypedef.from_stream(data, property_size)
        unnamed_0x00000005 = ActorParameters.from_stream(data, property_size)
        aggression_check = struct.unpack('>f', data.read(4))[0]
        cover_check = struct.unpack('>f', data.read(4))[0]
        search_radius = struct.unpack('>f', data.read(4))[0]
        fallback_check = struct.unpack('>f', data.read(4))[0]
        fallback_radius = struct.unpack('>f', data.read(4))[0]
        hearing_radius = struct.unpack('>f', data.read(4))[0]
        flags = enums.Flags.from_stream(data)
        unknown_8 = struct.unpack('>?', data.read(1))[0]
        projectile = struct.unpack(">L", data.read(4))[0]
        projectile_damage = DamageInfo.from_stream(data, property_size)
        sound_projectile = struct.unpack('>l', data.read(4))[0]
        blade_damage = DamageInfo.from_stream(data, property_size)
        kneel_attack_chance = struct.unpack('>f', data.read(4))[0]
        kneel_attack_shot = struct.unpack(">L", data.read(4))[0]
        kneel_attack_damage = DamageInfo.from_stream(data, property_size)
        dodge_check = struct.unpack('>f', data.read(4))[0]
        sound_impact = struct.unpack('>l', data.read(4))[0]
        average_next_shot_time = struct.unpack('>f', data.read(4))[0]
        next_shot_time_variation = struct.unpack('>f', data.read(4))[0]
        sound_alert = struct.unpack('>l', data.read(4))[0]
        gun_track_delay = struct.unpack('>f', data.read(4))[0]
        first_burst_count = struct.unpack('>l', data.read(4))[0]
        cloak_opacity = struct.unpack('>f', data.read(4))[0]
        max_cloak_opacity = struct.unpack('>f', data.read(4))[0]
        dodge_delay_time_min = struct.unpack('>f', data.read(4))[0]
        dodge_delay_time_max = struct.unpack('>f', data.read(4))[0]
        sound_hurled = struct.unpack('>l', data.read(4))[0]
        sound_death = struct.unpack('>l', data.read(4))[0]
        unknown_19 = struct.unpack('>f', data.read(4))[0]
        avoid_distance = struct.unpack('>f', data.read(4))[0]
        return cls(name, position, rotation, scale, unnamed_0x00000004, unnamed_0x00000005, aggression_check, cover_check, search_radius, fallback_check, fallback_radius, hearing_radius, flags, unknown_8, projectile, projectile_damage, sound_projectile, blade_damage, kneel_attack_chance, kneel_attack_shot, kneel_attack_damage, dodge_check, sound_impact, average_next_shot_time, next_shot_time_variation, sound_alert, gun_track_delay, first_burst_count, cloak_opacity, max_cloak_opacity, dodge_delay_time_min, dodge_delay_time_max, sound_hurled, sound_death, unknown_19, avoid_distance)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(b'\x00\x00\x00$')  # 36 properties
        data.write(self.name.encode("utf-8"))
        data.write(b'\x00')
        self.position.to_stream(data)
        self.rotation.to_stream(data)
        self.scale.to_stream(data)
        self.unnamed_0x00000004.to_stream(data)
        self.unnamed_0x00000005.to_stream(data)
        data.write(struct.pack('>f', self.aggression_check))
        data.write(struct.pack('>f', self.cover_check))
        data.write(struct.pack('>f', self.search_radius))
        data.write(struct.pack('>f', self.fallback_check))
        data.write(struct.pack('>f', self.fallback_radius))
        data.write(struct.pack('>f', self.hearing_radius))
        self.flags.to_stream(data)
        data.write(struct.pack('>?', self.unknown_8))
        data.write(struct.pack(">L", self.projectile))
        self.projectile_damage.to_stream(data)
        data.write(struct.pack('>l', self.sound_projectile))
        self.blade_damage.to_stream(data)
        data.write(struct.pack('>f', self.kneel_attack_chance))
        data.write(struct.pack(">L", self.kneel_attack_shot))
        self.kneel_attack_damage.to_stream(data)
        data.write(struct.pack('>f', self.dodge_check))
        data.write(struct.pack('>l', self.sound_impact))
        data.write(struct.pack('>f', self.average_next_shot_time))
        data.write(struct.pack('>f', self.next_shot_time_variation))
        data.write(struct.pack('>l', self.sound_alert))
        data.write(struct.pack('>f', self.gun_track_delay))
        data.write(struct.pack('>l', self.first_burst_count))
        data.write(struct.pack('>f', self.cloak_opacity))
        data.write(struct.pack('>f', self.max_cloak_opacity))
        data.write(struct.pack('>f', self.dodge_delay_time_min))
        data.write(struct.pack('>f', self.dodge_delay_time_max))
        data.write(struct.pack('>l', self.sound_hurled))
        data.write(struct.pack('>l', self.sound_death))
        data.write(struct.pack('>f', self.unknown_19))
        data.write(struct.pack('>f', self.avoid_distance))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            name=data['name'],
            position=Vector.from_json(data['position']),
            rotation=Vector.from_json(data['rotation']),
            scale=Vector.from_json(data['scale']),
            unnamed_0x00000004=PatternedAITypedef.from_json(data['unnamed_0x00000004']),
            unnamed_0x00000005=ActorParameters.from_json(data['unnamed_0x00000005']),
            aggression_check=data['aggression_check'],
            cover_check=data['cover_check'],
            search_radius=data['search_radius'],
            fallback_check=data['fallback_check'],
            fallback_radius=data['fallback_radius'],
            hearing_radius=data['hearing_radius'],
            flags=enums.Flags.from_json(data['flags']),
            unknown_8=data['unknown_8'],
            projectile=data['projectile'],
            projectile_damage=DamageInfo.from_json(data['projectile_damage']),
            sound_projectile=data['sound_projectile'],
            blade_damage=DamageInfo.from_json(data['blade_damage']),
            kneel_attack_chance=data['kneel_attack_chance'],
            kneel_attack_shot=data['kneel_attack_shot'],
            kneel_attack_damage=DamageInfo.from_json(data['kneel_attack_damage']),
            dodge_check=data['dodge_check'],
            sound_impact=data['sound_impact'],
            average_next_shot_time=data['average_next_shot_time'],
            next_shot_time_variation=data['next_shot_time_variation'],
            sound_alert=data['sound_alert'],
            gun_track_delay=data['gun_track_delay'],
            first_burst_count=data['first_burst_count'],
            cloak_opacity=data['cloak_opacity'],
            max_cloak_opacity=data['max_cloak_opacity'],
            dodge_delay_time_min=data['dodge_delay_time_min'],
            dodge_delay_time_max=data['dodge_delay_time_max'],
            sound_hurled=data['sound_hurled'],
            sound_death=data['sound_death'],
            unknown_19=data['unknown_19'],
            avoid_distance=data['avoid_distance'],
        )

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'position': self.position.to_json(),
            'rotation': self.rotation.to_json(),
            'scale': self.scale.to_json(),
            'unnamed_0x00000004': self.unnamed_0x00000004.to_json(),
            'unnamed_0x00000005': self.unnamed_0x00000005.to_json(),
            'aggression_check': self.aggression_check,
            'cover_check': self.cover_check,
            'search_radius': self.search_radius,
            'fallback_check': self.fallback_check,
            'fallback_radius': self.fallback_radius,
            'hearing_radius': self.hearing_radius,
            'flags': self.flags.to_json(),
            'unknown_8': self.unknown_8,
            'projectile': self.projectile,
            'projectile_damage': self.projectile_damage.to_json(),
            'sound_projectile': self.sound_projectile,
            'blade_damage': self.blade_damage.to_json(),
            'kneel_attack_chance': self.kneel_attack_chance,
            'kneel_attack_shot': self.kneel_attack_shot,
            'kneel_attack_damage': self.kneel_attack_damage.to_json(),
            'dodge_check': self.dodge_check,
            'sound_impact': self.sound_impact,
            'average_next_shot_time': self.average_next_shot_time,
            'next_shot_time_variation': self.next_shot_time_variation,
            'sound_alert': self.sound_alert,
            'gun_track_delay': self.gun_track_delay,
            'first_burst_count': self.first_burst_count,
            'cloak_opacity': self.cloak_opacity,
            'max_cloak_opacity': self.max_cloak_opacity,
            'dodge_delay_time_min': self.dodge_delay_time_min,
            'dodge_delay_time_max': self.dodge_delay_time_max,
            'sound_hurled': self.sound_hurled,
            'sound_death': self.sound_death,
            'unknown_19': self.unknown_19,
            'avoid_distance': self.avoid_distance,
        }

    def _dependencies_for_unnamed_0x00000004(self, asset_manager):
        yield from self.unnamed_0x00000004.dependencies_for(asset_manager)

    def _dependencies_for_unnamed_0x00000005(self, asset_manager):
        yield from self.unnamed_0x00000005.dependencies_for(asset_manager)

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

    def _dependencies_for_sound_alert(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_alert)

    def _dependencies_for_sound_hurled(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_hurled)

    def _dependencies_for_sound_death(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_death)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_unnamed_0x00000004, "unnamed_0x00000004", "PatternedAITypedef"),
            (self._dependencies_for_unnamed_0x00000005, "unnamed_0x00000005", "ActorParameters"),
            (self._dependencies_for_projectile, "projectile", "AssetId"),
            (self._dependencies_for_projectile_damage, "projectile_damage", "DamageInfo"),
            (self._dependencies_for_sound_projectile, "sound_projectile", "int"),
            (self._dependencies_for_blade_damage, "blade_damage", "DamageInfo"),
            (self._dependencies_for_kneel_attack_shot, "kneel_attack_shot", "AssetId"),
            (self._dependencies_for_kneel_attack_damage, "kneel_attack_damage", "DamageInfo"),
            (self._dependencies_for_sound_impact, "sound_impact", "int"),
            (self._dependencies_for_sound_alert, "sound_alert", "int"),
            (self._dependencies_for_sound_hurled, "sound_hurled", "int"),
            (self._dependencies_for_sound_death, "sound_death", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SpacePirate.{field_name} ({field_type}): {e}"
                )
