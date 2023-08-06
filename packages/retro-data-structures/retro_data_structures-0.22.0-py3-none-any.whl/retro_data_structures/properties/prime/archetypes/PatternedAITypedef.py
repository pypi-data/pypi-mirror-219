# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.prime.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.prime.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.prime.archetypes.HealthInfo import HealthInfo
from retro_data_structures.properties.prime.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.prime.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.prime.core.Vector import Vector


@dataclasses.dataclass()
class PatternedAITypedef(BaseProperty):
    mass: float = dataclasses.field(default=0.0)
    speed: float = dataclasses.field(default=0.0)
    turn_speed: float = dataclasses.field(default=0.0)
    detection_range: float = dataclasses.field(default=0.0)
    detection_height_range: float = dataclasses.field(default=0.0)
    detection_angle: float = dataclasses.field(default=0.0)
    min_attack_range: float = dataclasses.field(default=0.0)
    max_attack_range: float = dataclasses.field(default=0.0)
    average_attack_time: float = dataclasses.field(default=0.0)
    attack_time_variation: float = dataclasses.field(default=0.0)
    leash_radius: float = dataclasses.field(default=0.0)
    player_leash_radius: float = dataclasses.field(default=0.0)
    player_leash_time: float = dataclasses.field(default=0.0)
    contact_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    damage_wait_time: float = dataclasses.field(default=0.0)
    unnamed: HealthInfo = dataclasses.field(default_factory=HealthInfo)
    vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    unknown_1: float = dataclasses.field(default=0.0)
    unknown_2: float = dataclasses.field(default=0.0)
    unknown_3: Vector = dataclasses.field(default_factory=Vector)
    unknown_4: float = dataclasses.field(default=0.0)
    unknown_5: float = dataclasses.field(default=0.0)
    unknown_6: float = dataclasses.field(default=0.0)
    unknown_7: float = dataclasses.field(default=0.0)
    death_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    animation_parameters: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    active: bool = dataclasses.field(default=False)
    state_machine: AssetId = dataclasses.field(metadata={'asset_types': ['AFSM']}, default=default_asset_id)
    unknown_8: float = dataclasses.field(default=0.0)
    unknown_9: float = dataclasses.field(default=0.0)
    unknown_10: float = dataclasses.field(default=0.0)
    unknown_11: int = dataclasses.field(default=0)
    unknown_12: Vector = dataclasses.field(default_factory=Vector)
    particle_1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_13: int = dataclasses.field(default=0)
    unknown_14: Vector = dataclasses.field(default_factory=Vector)
    particle_2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ice_shatter_sound: int = dataclasses.field(default=0, metadata={'sound': True})

    @classmethod
    def game(cls) -> Game:
        return Game.PRIME

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: typing.Optional[int] = None, default_override: typing.Optional[dict] = None):
        property_size = None  # Atomic
        mass = struct.unpack('>f', data.read(4))[0]
        speed = struct.unpack('>f', data.read(4))[0]
        turn_speed = struct.unpack('>f', data.read(4))[0]
        detection_range = struct.unpack('>f', data.read(4))[0]
        detection_height_range = struct.unpack('>f', data.read(4))[0]
        detection_angle = struct.unpack('>f', data.read(4))[0]
        min_attack_range = struct.unpack('>f', data.read(4))[0]
        max_attack_range = struct.unpack('>f', data.read(4))[0]
        average_attack_time = struct.unpack('>f', data.read(4))[0]
        attack_time_variation = struct.unpack('>f', data.read(4))[0]
        leash_radius = struct.unpack('>f', data.read(4))[0]
        player_leash_radius = struct.unpack('>f', data.read(4))[0]
        player_leash_time = struct.unpack('>f', data.read(4))[0]
        contact_damage = DamageInfo.from_stream(data, property_size)
        damage_wait_time = struct.unpack('>f', data.read(4))[0]
        unnamed = HealthInfo.from_stream(data, property_size)
        vulnerability = DamageVulnerability.from_stream(data, property_size)
        unknown_1 = struct.unpack('>f', data.read(4))[0]
        unknown_2 = struct.unpack('>f', data.read(4))[0]
        unknown_3 = Vector.from_stream(data)
        unknown_4 = struct.unpack('>f', data.read(4))[0]
        unknown_5 = struct.unpack('>f', data.read(4))[0]
        unknown_6 = struct.unpack('>f', data.read(4))[0]
        unknown_7 = struct.unpack('>f', data.read(4))[0]
        death_sound = struct.unpack('>l', data.read(4))[0]
        animation_parameters = AnimationParameters.from_stream(data, property_size)
        active = struct.unpack('>?', data.read(1))[0]
        state_machine = struct.unpack(">L", data.read(4))[0]
        unknown_8 = struct.unpack('>f', data.read(4))[0]
        unknown_9 = struct.unpack('>f', data.read(4))[0]
        unknown_10 = struct.unpack('>f', data.read(4))[0]
        unknown_11 = struct.unpack('>l', data.read(4))[0]
        unknown_12 = Vector.from_stream(data)
        particle_1 = struct.unpack(">L", data.read(4))[0]
        unknown_13 = struct.unpack('>l', data.read(4))[0]
        unknown_14 = Vector.from_stream(data)
        particle_2 = struct.unpack(">L", data.read(4))[0]
        ice_shatter_sound = struct.unpack('>l', data.read(4))[0]
        return cls(mass, speed, turn_speed, detection_range, detection_height_range, detection_angle, min_attack_range, max_attack_range, average_attack_time, attack_time_variation, leash_radius, player_leash_radius, player_leash_time, contact_damage, damage_wait_time, unnamed, vulnerability, unknown_1, unknown_2, unknown_3, unknown_4, unknown_5, unknown_6, unknown_7, death_sound, animation_parameters, active, state_machine, unknown_8, unknown_9, unknown_10, unknown_11, unknown_12, particle_1, unknown_13, unknown_14, particle_2, ice_shatter_sound)

    def to_stream(self, data: typing.BinaryIO, default_override: typing.Optional[dict] = None):
        default_override = default_override or {}
        data.write(struct.pack('>f', self.mass))
        data.write(struct.pack('>f', self.speed))
        data.write(struct.pack('>f', self.turn_speed))
        data.write(struct.pack('>f', self.detection_range))
        data.write(struct.pack('>f', self.detection_height_range))
        data.write(struct.pack('>f', self.detection_angle))
        data.write(struct.pack('>f', self.min_attack_range))
        data.write(struct.pack('>f', self.max_attack_range))
        data.write(struct.pack('>f', self.average_attack_time))
        data.write(struct.pack('>f', self.attack_time_variation))
        data.write(struct.pack('>f', self.leash_radius))
        data.write(struct.pack('>f', self.player_leash_radius))
        data.write(struct.pack('>f', self.player_leash_time))
        self.contact_damage.to_stream(data)
        data.write(struct.pack('>f', self.damage_wait_time))
        self.unnamed.to_stream(data)
        self.vulnerability.to_stream(data)
        data.write(struct.pack('>f', self.unknown_1))
        data.write(struct.pack('>f', self.unknown_2))
        self.unknown_3.to_stream(data)
        data.write(struct.pack('>f', self.unknown_4))
        data.write(struct.pack('>f', self.unknown_5))
        data.write(struct.pack('>f', self.unknown_6))
        data.write(struct.pack('>f', self.unknown_7))
        data.write(struct.pack('>l', self.death_sound))
        self.animation_parameters.to_stream(data)
        data.write(struct.pack('>?', self.active))
        data.write(struct.pack(">L", self.state_machine))
        data.write(struct.pack('>f', self.unknown_8))
        data.write(struct.pack('>f', self.unknown_9))
        data.write(struct.pack('>f', self.unknown_10))
        data.write(struct.pack('>l', self.unknown_11))
        self.unknown_12.to_stream(data)
        data.write(struct.pack(">L", self.particle_1))
        data.write(struct.pack('>l', self.unknown_13))
        self.unknown_14.to_stream(data)
        data.write(struct.pack(">L", self.particle_2))
        data.write(struct.pack('>l', self.ice_shatter_sound))

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            mass=data['mass'],
            speed=data['speed'],
            turn_speed=data['turn_speed'],
            detection_range=data['detection_range'],
            detection_height_range=data['detection_height_range'],
            detection_angle=data['detection_angle'],
            min_attack_range=data['min_attack_range'],
            max_attack_range=data['max_attack_range'],
            average_attack_time=data['average_attack_time'],
            attack_time_variation=data['attack_time_variation'],
            leash_radius=data['leash_radius'],
            player_leash_radius=data['player_leash_radius'],
            player_leash_time=data['player_leash_time'],
            contact_damage=DamageInfo.from_json(data['contact_damage']),
            damage_wait_time=data['damage_wait_time'],
            unnamed=HealthInfo.from_json(data['unnamed']),
            vulnerability=DamageVulnerability.from_json(data['vulnerability']),
            unknown_1=data['unknown_1'],
            unknown_2=data['unknown_2'],
            unknown_3=Vector.from_json(data['unknown_3']),
            unknown_4=data['unknown_4'],
            unknown_5=data['unknown_5'],
            unknown_6=data['unknown_6'],
            unknown_7=data['unknown_7'],
            death_sound=data['death_sound'],
            animation_parameters=AnimationParameters.from_json(data['animation_parameters']),
            active=data['active'],
            state_machine=data['state_machine'],
            unknown_8=data['unknown_8'],
            unknown_9=data['unknown_9'],
            unknown_10=data['unknown_10'],
            unknown_11=data['unknown_11'],
            unknown_12=Vector.from_json(data['unknown_12']),
            particle_1=data['particle_1'],
            unknown_13=data['unknown_13'],
            unknown_14=Vector.from_json(data['unknown_14']),
            particle_2=data['particle_2'],
            ice_shatter_sound=data['ice_shatter_sound'],
        )

    def to_json(self) -> dict:
        return {
            'mass': self.mass,
            'speed': self.speed,
            'turn_speed': self.turn_speed,
            'detection_range': self.detection_range,
            'detection_height_range': self.detection_height_range,
            'detection_angle': self.detection_angle,
            'min_attack_range': self.min_attack_range,
            'max_attack_range': self.max_attack_range,
            'average_attack_time': self.average_attack_time,
            'attack_time_variation': self.attack_time_variation,
            'leash_radius': self.leash_radius,
            'player_leash_radius': self.player_leash_radius,
            'player_leash_time': self.player_leash_time,
            'contact_damage': self.contact_damage.to_json(),
            'damage_wait_time': self.damage_wait_time,
            'unnamed': self.unnamed.to_json(),
            'vulnerability': self.vulnerability.to_json(),
            'unknown_1': self.unknown_1,
            'unknown_2': self.unknown_2,
            'unknown_3': self.unknown_3.to_json(),
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'death_sound': self.death_sound,
            'animation_parameters': self.animation_parameters.to_json(),
            'active': self.active,
            'state_machine': self.state_machine,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'unknown_12': self.unknown_12.to_json(),
            'particle_1': self.particle_1,
            'unknown_13': self.unknown_13,
            'unknown_14': self.unknown_14.to_json(),
            'particle_2': self.particle_2,
            'ice_shatter_sound': self.ice_shatter_sound,
        }

    def _dependencies_for_contact_damage(self, asset_manager):
        yield from self.contact_damage.dependencies_for(asset_manager)

    def _dependencies_for_unnamed(self, asset_manager):
        yield from self.unnamed.dependencies_for(asset_manager)

    def _dependencies_for_vulnerability(self, asset_manager):
        yield from self.vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_death_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.death_sound)

    def _dependencies_for_animation_parameters(self, asset_manager):
        yield from self.animation_parameters.dependencies_for(asset_manager)

    def _dependencies_for_state_machine(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.state_machine)

    def _dependencies_for_particle_1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_1)

    def _dependencies_for_particle_2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.particle_2)

    def _dependencies_for_ice_shatter_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.ice_shatter_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_contact_damage, "contact_damage", "DamageInfo"),
            (self._dependencies_for_unnamed, "unnamed", "HealthInfo"),
            (self._dependencies_for_vulnerability, "vulnerability", "DamageVulnerability"),
            (self._dependencies_for_death_sound, "death_sound", "int"),
            (self._dependencies_for_animation_parameters, "animation_parameters", "AnimationParameters"),
            (self._dependencies_for_state_machine, "state_machine", "AssetId"),
            (self._dependencies_for_particle_1, "particle_1", "AssetId"),
            (self._dependencies_for_particle_2, "particle_2", "AssetId"),
            (self._dependencies_for_ice_shatter_sound, "ice_shatter_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for PatternedAITypedef.{field_name} ({field_type}): {e}"
                )
