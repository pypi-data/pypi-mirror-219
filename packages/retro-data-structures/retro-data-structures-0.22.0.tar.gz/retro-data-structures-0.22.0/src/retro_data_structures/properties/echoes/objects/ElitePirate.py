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
from retro_data_structures.properties.echoes.archetypes.ShockWaveInfo import ShockWaveInfo
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class ElitePirate(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    melee_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    max_melee_range: float = dataclasses.field(default=9.0)
    min_shockwave_range: float = dataclasses.field(default=9.0)
    max_shockwave_range: float = dataclasses.field(default=35.0)
    min_rocket_range: float = dataclasses.field(default=15.0)
    max_rocket_range: float = dataclasses.field(default=80.0)
    unknown_0x5236c2b6: float = dataclasses.field(default=50.0)
    unknown_0x01eaab17: float = dataclasses.field(default=50.0)
    shielded_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    shielded_skin_rules: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    dark_shield: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    dark_shield_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    dark_shield_pop: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    light_shield: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    light_shield_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    light_shield_pop: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    taunt_interval: float = dataclasses.field(default=8.0)
    taunt_variance: float = dataclasses.field(default=3.0)
    single_shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    double_shock_wave_info: ShockWaveInfo = dataclasses.field(default_factory=ShockWaveInfo)
    unknown_0x28b39197: float = dataclasses.field(default=1.0)
    unknown_0xe27de71b: float = dataclasses.field(default=1.0)
    unknown_0x665e7ace: float = dataclasses.field(default=1.0)
    unknown_0xacd4d06d: float = dataclasses.field(default=2.0)
    rocket: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    rocket_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x624222f8: int = dataclasses.field(default=2)
    unknown_0x31e43a1c: int = dataclasses.field(default=4)
    repeated_attack_chance: float = dataclasses.field(default=0.10000000149011612)
    energy_absorb_duration: float = dataclasses.field(default=3.0)
    unknown_0xe47334ae: float = dataclasses.field(default=1.0)
    unknown_0x3dad897b: float = dataclasses.field(default=50.0)
    always_ff_0x06cf4324: int = dataclasses.field(default=0)
    always_ff_0x23f5e1ee: int = dataclasses.field(default=0)
    rocket_launcher_actor_info: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    rocket_launcher_anim_info: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x7e6e0d38: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    visor_electric_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    sound_visor_electric: int = dataclasses.field(default=0, metadata={'sound': True})
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'EPRT'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['ElitePirate.rel']

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
        data.write(b'\x00+')  # 43 properties

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
        self.patterned.to_stream(data, default_override={'average_attack_time': 3.5, 'attack_time_variation': 2.0, 'creature_size': 2})
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

        data.write(b'\xc9A`4')  # 0xc9416034
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x98s\xa1\xc1')  # 0x9873a1c1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_melee_range))

        data.write(b'(\t\\\xe6')  # 0x28095ce6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_shockwave_range))

        data.write(b'i\x1ec`')  # 0x691e6360
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_shockwave_range))

        data.write(b'\xe6)\x9f\xac')  # 0xe6299fac
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_rocket_range))

        data.write(b'A\x1d\x1f\xd5')  # 0x411d1fd5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_rocket_range))

        data.write(b'R6\xc2\xb6')  # 0x5236c2b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5236c2b6))

        data.write(b'\x01\xea\xab\x17')  # 0x1eaab17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x01eaab17))

        data.write(b'\x00\xae\x9ca')  # 0xae9c61
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shielded_model))

        data.write(b'\xac\xda\xe4\x08')  # 0xacdae408
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.shielded_skin_rules))

        data.write(b'\xaaH-\x8d')  # 0xaa482d8d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.dark_shield))

        data.write(b'\xee\xaf\x03\xc4')  # 0xeeaf03c4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.dark_shield_sound))

        data.write(b'\xafO\xaet')  # 0xaf4fae74
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.dark_shield_pop))

        data.write(b'd\xa1\xf5X')  # 0x64a1f558
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.light_shield))

        data.write(b'\xbf\x10st')  # 0xbf107374
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.light_shield_sound))

        data.write(b'\xb4:L\xaa')  # 0xb43a4caa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.light_shield_pop))

        data.write(b'a\xc4\xc0\xea')  # 0x61c4c0ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt_interval))

        data.write(b'\xf8-\x12r')  # 0xf82d1272
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.taunt_variance))

        data.write(b'\xb2\xeb\xbf\xc6')  # 0xb2ebbfc6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.single_shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\t%\r\xb2')  # 0x9250db2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.double_shock_wave_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'(\xb3\x91\x97')  # 0x28b39197
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x28b39197))

        data.write(b'\xe2}\xe7\x1b')  # 0xe27de71b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe27de71b))

        data.write(b'f^z\xce')  # 0x665e7ace
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x665e7ace))

        data.write(b'\xac\xd4\xd0m')  # 0xacd4d06d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xacd4d06d))

        data.write(b'\xf1\x99\xf5S')  # 0xf199f553
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.rocket))

        data.write(b'@c\xd4\\')  # 0x4063d45c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rocket_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'bB"\xf8')  # 0x624222f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x624222f8))

        data.write(b'1\xe4:\x1c')  # 0x31e43a1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x31e43a1c))

        data.write(b'\xd6F\x91\x19')  # 0xd6469119
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.repeated_attack_chance))

        data.write(b'm\x14%\xd8')  # 0x6d1425d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.energy_absorb_duration))

        data.write(b'\xe4s4\xae')  # 0xe47334ae
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe47334ae))

        data.write(b'=\xad\x89{')  # 0x3dad897b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3dad897b))

        data.write(b'\x06\xcfC$')  # 0x6cf4324
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.always_ff_0x06cf4324))

        data.write(b'#\xf5\xe1\xee')  # 0x23f5e1ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.always_ff_0x23f5e1ee))

        data.write(b'b\xc7D\xcd')  # 0x62c744cd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rocket_launcher_actor_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9+H\x1d')  # 0xb92b481d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.rocket_launcher_anim_info.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~n\r8')  # 0x7e6e0d38
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7e6e0d38.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbd2\x158')  # 0xbd321538
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.visor_electric_effect))

        data.write(b'X\xa4\x92\xef')  # 0x58a492ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_visor_electric))

        data.write(b'\xe6\x17H\xed')  # 0xe61748ed
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ing_possession_data.to_stream(data)
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
            melee_damage=DamageInfo.from_json(data['melee_damage']),
            max_melee_range=data['max_melee_range'],
            min_shockwave_range=data['min_shockwave_range'],
            max_shockwave_range=data['max_shockwave_range'],
            min_rocket_range=data['min_rocket_range'],
            max_rocket_range=data['max_rocket_range'],
            unknown_0x5236c2b6=data['unknown_0x5236c2b6'],
            unknown_0x01eaab17=data['unknown_0x01eaab17'],
            shielded_model=data['shielded_model'],
            shielded_skin_rules=data['shielded_skin_rules'],
            dark_shield=data['dark_shield'],
            dark_shield_sound=data['dark_shield_sound'],
            dark_shield_pop=data['dark_shield_pop'],
            light_shield=data['light_shield'],
            light_shield_sound=data['light_shield_sound'],
            light_shield_pop=data['light_shield_pop'],
            taunt_interval=data['taunt_interval'],
            taunt_variance=data['taunt_variance'],
            single_shock_wave_info=ShockWaveInfo.from_json(data['single_shock_wave_info']),
            double_shock_wave_info=ShockWaveInfo.from_json(data['double_shock_wave_info']),
            unknown_0x28b39197=data['unknown_0x28b39197'],
            unknown_0xe27de71b=data['unknown_0xe27de71b'],
            unknown_0x665e7ace=data['unknown_0x665e7ace'],
            unknown_0xacd4d06d=data['unknown_0xacd4d06d'],
            rocket=data['rocket'],
            rocket_damage=DamageInfo.from_json(data['rocket_damage']),
            unknown_0x624222f8=data['unknown_0x624222f8'],
            unknown_0x31e43a1c=data['unknown_0x31e43a1c'],
            repeated_attack_chance=data['repeated_attack_chance'],
            energy_absorb_duration=data['energy_absorb_duration'],
            unknown_0xe47334ae=data['unknown_0xe47334ae'],
            unknown_0x3dad897b=data['unknown_0x3dad897b'],
            always_ff_0x06cf4324=data['always_ff_0x06cf4324'],
            always_ff_0x23f5e1ee=data['always_ff_0x23f5e1ee'],
            rocket_launcher_actor_info=ActorParameters.from_json(data['rocket_launcher_actor_info']),
            rocket_launcher_anim_info=AnimationParameters.from_json(data['rocket_launcher_anim_info']),
            unknown_0x7e6e0d38=AnimationParameters.from_json(data['unknown_0x7e6e0d38']),
            visor_electric_effect=data['visor_electric_effect'],
            sound_visor_electric=data['sound_visor_electric'],
            ing_possession_data=IngPossessionData.from_json(data['ing_possession_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'melee_damage': self.melee_damage.to_json(),
            'max_melee_range': self.max_melee_range,
            'min_shockwave_range': self.min_shockwave_range,
            'max_shockwave_range': self.max_shockwave_range,
            'min_rocket_range': self.min_rocket_range,
            'max_rocket_range': self.max_rocket_range,
            'unknown_0x5236c2b6': self.unknown_0x5236c2b6,
            'unknown_0x01eaab17': self.unknown_0x01eaab17,
            'shielded_model': self.shielded_model,
            'shielded_skin_rules': self.shielded_skin_rules,
            'dark_shield': self.dark_shield,
            'dark_shield_sound': self.dark_shield_sound,
            'dark_shield_pop': self.dark_shield_pop,
            'light_shield': self.light_shield,
            'light_shield_sound': self.light_shield_sound,
            'light_shield_pop': self.light_shield_pop,
            'taunt_interval': self.taunt_interval,
            'taunt_variance': self.taunt_variance,
            'single_shock_wave_info': self.single_shock_wave_info.to_json(),
            'double_shock_wave_info': self.double_shock_wave_info.to_json(),
            'unknown_0x28b39197': self.unknown_0x28b39197,
            'unknown_0xe27de71b': self.unknown_0xe27de71b,
            'unknown_0x665e7ace': self.unknown_0x665e7ace,
            'unknown_0xacd4d06d': self.unknown_0xacd4d06d,
            'rocket': self.rocket,
            'rocket_damage': self.rocket_damage.to_json(),
            'unknown_0x624222f8': self.unknown_0x624222f8,
            'unknown_0x31e43a1c': self.unknown_0x31e43a1c,
            'repeated_attack_chance': self.repeated_attack_chance,
            'energy_absorb_duration': self.energy_absorb_duration,
            'unknown_0xe47334ae': self.unknown_0xe47334ae,
            'unknown_0x3dad897b': self.unknown_0x3dad897b,
            'always_ff_0x06cf4324': self.always_ff_0x06cf4324,
            'always_ff_0x23f5e1ee': self.always_ff_0x23f5e1ee,
            'rocket_launcher_actor_info': self.rocket_launcher_actor_info.to_json(),
            'rocket_launcher_anim_info': self.rocket_launcher_anim_info.to_json(),
            'unknown_0x7e6e0d38': self.unknown_0x7e6e0d38.to_json(),
            'visor_electric_effect': self.visor_electric_effect,
            'sound_visor_electric': self.sound_visor_electric,
            'ing_possession_data': self.ing_possession_data.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_melee_damage(self, asset_manager):
        yield from self.melee_damage.dependencies_for(asset_manager)

    def _dependencies_for_shielded_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shielded_model)

    def _dependencies_for_shielded_skin_rules(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.shielded_skin_rules)

    def _dependencies_for_dark_shield(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dark_shield)

    def _dependencies_for_dark_shield_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.dark_shield_sound)

    def _dependencies_for_dark_shield_pop(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dark_shield_pop)

    def _dependencies_for_light_shield(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.light_shield)

    def _dependencies_for_light_shield_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.light_shield_sound)

    def _dependencies_for_light_shield_pop(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.light_shield_pop)

    def _dependencies_for_single_shock_wave_info(self, asset_manager):
        yield from self.single_shock_wave_info.dependencies_for(asset_manager)

    def _dependencies_for_double_shock_wave_info(self, asset_manager):
        yield from self.double_shock_wave_info.dependencies_for(asset_manager)

    def _dependencies_for_rocket(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.rocket)

    def _dependencies_for_rocket_damage(self, asset_manager):
        yield from self.rocket_damage.dependencies_for(asset_manager)

    def _dependencies_for_rocket_launcher_actor_info(self, asset_manager):
        yield from self.rocket_launcher_actor_info.dependencies_for(asset_manager)

    def _dependencies_for_rocket_launcher_anim_info(self, asset_manager):
        yield from self.rocket_launcher_anim_info.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x7e6e0d38(self, asset_manager):
        yield from self.unknown_0x7e6e0d38.dependencies_for(asset_manager)

    def _dependencies_for_visor_electric_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.visor_electric_effect)

    def _dependencies_for_sound_visor_electric(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_visor_electric)

    def _dependencies_for_ing_possession_data(self, asset_manager):
        yield from self.ing_possession_data.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_melee_damage, "melee_damage", "DamageInfo"),
            (self._dependencies_for_shielded_model, "shielded_model", "AssetId"),
            (self._dependencies_for_shielded_skin_rules, "shielded_skin_rules", "AssetId"),
            (self._dependencies_for_dark_shield, "dark_shield", "AssetId"),
            (self._dependencies_for_dark_shield_sound, "dark_shield_sound", "int"),
            (self._dependencies_for_dark_shield_pop, "dark_shield_pop", "AssetId"),
            (self._dependencies_for_light_shield, "light_shield", "AssetId"),
            (self._dependencies_for_light_shield_sound, "light_shield_sound", "int"),
            (self._dependencies_for_light_shield_pop, "light_shield_pop", "AssetId"),
            (self._dependencies_for_single_shock_wave_info, "single_shock_wave_info", "ShockWaveInfo"),
            (self._dependencies_for_double_shock_wave_info, "double_shock_wave_info", "ShockWaveInfo"),
            (self._dependencies_for_rocket, "rocket", "AssetId"),
            (self._dependencies_for_rocket_damage, "rocket_damage", "DamageInfo"),
            (self._dependencies_for_rocket_launcher_actor_info, "rocket_launcher_actor_info", "ActorParameters"),
            (self._dependencies_for_rocket_launcher_anim_info, "rocket_launcher_anim_info", "AnimationParameters"),
            (self._dependencies_for_unknown_0x7e6e0d38, "unknown_0x7e6e0d38", "AnimationParameters"),
            (self._dependencies_for_visor_electric_effect, "visor_electric_effect", "AssetId"),
            (self._dependencies_for_sound_visor_electric, "sound_visor_electric", "int"),
            (self._dependencies_for_ing_possession_data, "ing_possession_data", "IngPossessionData"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for ElitePirate.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'average_attack_time': 3.5, 'attack_time_variation': 2.0, 'creature_size': 2})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_melee_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_max_melee_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_shockwave_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_shockwave_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_rocket_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_rocket_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5236c2b6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x01eaab17(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_shielded_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_shielded_skin_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_dark_shield(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_dark_shield_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_dark_shield_pop(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_light_shield(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_light_shield_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_light_shield_pop(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_taunt_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_taunt_variance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_single_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_double_shock_wave_info(data: typing.BinaryIO, property_size: int):
    return ShockWaveInfo.from_stream(data, property_size)


def _decode_unknown_0x28b39197(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe27de71b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x665e7ace(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xacd4d06d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rocket(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_rocket_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 5.0})


def _decode_unknown_0x624222f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x31e43a1c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_repeated_attack_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_energy_absorb_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe47334ae(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3dad897b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_always_ff_0x06cf4324(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_always_ff_0x23f5e1ee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_rocket_launcher_actor_info(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_rocket_launcher_anim_info(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x7e6e0d38(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_visor_electric_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_visor_electric(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xc9416034: ('melee_damage', _decode_melee_damage),
    0x9873a1c1: ('max_melee_range', _decode_max_melee_range),
    0x28095ce6: ('min_shockwave_range', _decode_min_shockwave_range),
    0x691e6360: ('max_shockwave_range', _decode_max_shockwave_range),
    0xe6299fac: ('min_rocket_range', _decode_min_rocket_range),
    0x411d1fd5: ('max_rocket_range', _decode_max_rocket_range),
    0x5236c2b6: ('unknown_0x5236c2b6', _decode_unknown_0x5236c2b6),
    0x1eaab17: ('unknown_0x01eaab17', _decode_unknown_0x01eaab17),
    0xae9c61: ('shielded_model', _decode_shielded_model),
    0xacdae408: ('shielded_skin_rules', _decode_shielded_skin_rules),
    0xaa482d8d: ('dark_shield', _decode_dark_shield),
    0xeeaf03c4: ('dark_shield_sound', _decode_dark_shield_sound),
    0xaf4fae74: ('dark_shield_pop', _decode_dark_shield_pop),
    0x64a1f558: ('light_shield', _decode_light_shield),
    0xbf107374: ('light_shield_sound', _decode_light_shield_sound),
    0xb43a4caa: ('light_shield_pop', _decode_light_shield_pop),
    0x61c4c0ea: ('taunt_interval', _decode_taunt_interval),
    0xf82d1272: ('taunt_variance', _decode_taunt_variance),
    0xb2ebbfc6: ('single_shock_wave_info', _decode_single_shock_wave_info),
    0x9250db2: ('double_shock_wave_info', _decode_double_shock_wave_info),
    0x28b39197: ('unknown_0x28b39197', _decode_unknown_0x28b39197),
    0xe27de71b: ('unknown_0xe27de71b', _decode_unknown_0xe27de71b),
    0x665e7ace: ('unknown_0x665e7ace', _decode_unknown_0x665e7ace),
    0xacd4d06d: ('unknown_0xacd4d06d', _decode_unknown_0xacd4d06d),
    0xf199f553: ('rocket', _decode_rocket),
    0x4063d45c: ('rocket_damage', _decode_rocket_damage),
    0x624222f8: ('unknown_0x624222f8', _decode_unknown_0x624222f8),
    0x31e43a1c: ('unknown_0x31e43a1c', _decode_unknown_0x31e43a1c),
    0xd6469119: ('repeated_attack_chance', _decode_repeated_attack_chance),
    0x6d1425d8: ('energy_absorb_duration', _decode_energy_absorb_duration),
    0xe47334ae: ('unknown_0xe47334ae', _decode_unknown_0xe47334ae),
    0x3dad897b: ('unknown_0x3dad897b', _decode_unknown_0x3dad897b),
    0x6cf4324: ('always_ff_0x06cf4324', _decode_always_ff_0x06cf4324),
    0x23f5e1ee: ('always_ff_0x23f5e1ee', _decode_always_ff_0x23f5e1ee),
    0x62c744cd: ('rocket_launcher_actor_info', _decode_rocket_launcher_actor_info),
    0xb92b481d: ('rocket_launcher_anim_info', _decode_rocket_launcher_anim_info),
    0x7e6e0d38: ('unknown_0x7e6e0d38', _decode_unknown_0x7e6e0d38),
    0xbd321538: ('visor_electric_effect', _decode_visor_electric_effect),
    0x58a492ef: ('sound_visor_electric', _decode_sound_visor_electric),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
}
