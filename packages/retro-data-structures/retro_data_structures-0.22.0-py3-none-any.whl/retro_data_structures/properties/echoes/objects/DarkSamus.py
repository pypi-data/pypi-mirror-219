# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class DarkSamus(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_0x72edeb7d: float = dataclasses.field(default=-1.0)
    unknown_0x74fa22f0: float = dataclasses.field(default=-1.0)
    glide_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    missile_ricochet_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x6689925b: bool = dataclasses.field(default=False)
    txtr_0x3863160b: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    unknown_0x2c6a3344: float = dataclasses.field(default=100.0)
    melee_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part_0x6d40aa56: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x9603a544: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    dive_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x4aa5dd62: float = dataclasses.field(default=40.0)
    unknown_0x1ad7dc21: float = dataclasses.field(default=500.0)
    dive_attack_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    scatter_shot_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    scatter_shot_projectile2: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    scatter_shot_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x378285b9: float = dataclasses.field(default=0.0)
    unknown_0xd242e25f: float = dataclasses.field(default=300.0)
    normal_missile_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    normal_missile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x1f1ef7a9: int = dataclasses.field(default=1)
    unknown_0xc4a1a44e: int = dataclasses.field(default=3)
    super_missile_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    super_missile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    freeze_beam_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    freeze_beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    txtr_0x7ffeb33d: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    damage_interrupt_threshold: float = dataclasses.field(default=10.0)
    unknown_0xf317f4d5: float = dataclasses.field(default=4.0)
    sweep_swoosh: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sweep_beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    crsc: AssetId = dataclasses.field(metadata={'asset_types': ['CRSC']}, default=default_asset_id)
    sweep_beam_sound: int = dataclasses.field(default=0)
    unknown_0x0ef8dc15: int = dataclasses.field(default=0)
    invulnerable_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    invulnerable_skin_rules: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    boost_ball_model: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    boost_ball_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    boost_ball_glow: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    swhc_0x449aa4aa: AssetId = dataclasses.field(metadata={'asset_types': ['SWHC']}, default=default_asset_id)
    swhc_0x0345fa17: AssetId = dataclasses.field(metadata={'asset_types': ['SWHC']}, default=default_asset_id)
    sound_0x2c72576b: int = dataclasses.field(default=0, metadata={'sound': True})
    boost_ball_hit_player_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    boost_ball_collision: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    audio_playback_parms: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    part_0xa6c42023: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    ice_spread_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    part_0x908b06e9: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0x494de4a4: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sound_0xa861649f: int = dataclasses.field(default=0, metadata={'sound': True})
    damage_info_0x18402aa9: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part_0xe701daea: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    phazon_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    wpsc: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    damage_info_0x58769eb2: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    phazon_projectile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    phazon_enrage_sphere: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage_info_0x8f3af226: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    alternate_scannable_info: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DRKS'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['DarkSamus.rel']

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
        data.write(b'\x00?')  # 63 properties

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
        self.patterned.to_stream(data, default_override={'detection_range': 32.0, 'collision_radius': 0.5, 'collision_height': 1.0, 'creature_size': 1})
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

        data.write(b'r\xed\xeb}')  # 0x72edeb7d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x72edeb7d))

        data.write(b't\xfa"\xf0')  # 0x74fa22f0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x74fa22f0))

        data.write(b'\x1fF\x89g')  # 0x1f468967
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.glide_sound))

        data.write(b'\x1a\x08\xaa\xdc')  # 0x1a08aadc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.missile_ricochet_sound))

        data.write(b'f\x89\x92[')  # 0x6689925b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x6689925b))

        data.write(b'8c\x16\x0b')  # 0x3863160b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.txtr_0x3863160b))

        data.write(b',j3D')  # 0x2c6a3344
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2c6a3344))

        data.write(b'My\x0e\xe9')  # 0x4d790ee9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_attack_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'm@\xaaV')  # 0x6d40aa56
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x6d40aa56))

        data.write(b'\x96\x03\xa5D')  # 0x9603a544
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x9603a544))

        data.write(b'\x86\x88\xf55')  # 0x8688f535
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dive_attack_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'J\xa5\xddb')  # 0x4aa5dd62
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x4aa5dd62))

        data.write(b'\x1a\xd7\xdc!')  # 0x1ad7dc21
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x1ad7dc21))

        data.write(b'\xed0\xb0\xef')  # 0xed30b0ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.dive_attack_effect))

        data.write(b'\x85_\x07I')  # 0x855f0749
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scatter_shot_projectile))

        data.write(b'\x83\xa5Q\x7f')  # 0x83a5517f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scatter_shot_projectile2))

        data.write(b'\x8e\xa8pb')  # 0x8ea87062
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.scatter_shot_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'7\x82\x85\xb9')  # 0x378285b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x378285b9))

        data.write(b'\xd2B\xe2_')  # 0xd242e25f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd242e25f))

        data.write(b'\xe0\r\xb6-')  # 0xe00db62d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.normal_missile_projectile))

        data.write(b'\xc4\x12\x87\x92')  # 0xc4128792
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.normal_missile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1f\x1e\xf7\xa9')  # 0x1f1ef7a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x1f1ef7a9))

        data.write(b'\xc4\xa1\xa4N')  # 0xc4a1a44e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc4a1a44e))

        data.write(b')\xdbN\xe4')  # 0x29db4ee4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.super_missile_projectile))

        data.write(b'&c+~')  # 0x26632b7e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.super_missile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf9\x10Ji')  # 0xf9104a69
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.freeze_beam_projectile))

        data.write(b'\xb5\xba\x1f\xe7')  # 0xb5ba1fe7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.freeze_beam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x7f\xfe\xb3=')  # 0x7ffeb33d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.txtr_0x7ffeb33d))

        data.write(b'\x8fp\xd3\xf2')  # 0x8f70d3f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_interrupt_threshold))

        data.write(b'\xf3\x17\xf4\xd5')  # 0xf317f4d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf317f4d5))

        data.write(b"\xd2\x12'\x11")  # 0xd2122711
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sweep_swoosh))

        data.write(b'\x08\xc2\xbf\xe0')  # 0x8c2bfe0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.sweep_beam_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\xb6X\xf2')  # 0x68b658f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.crsc))

        data.write(b'\xea\x17\xcbf')  # 0xea17cb66
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sweep_beam_sound))

        data.write(b'\x0e\xf8\xdc\x15')  # 0xef8dc15
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x0ef8dc15))

        data.write(b'\x07-\xf31')  # 0x72df331
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.invulnerable_model))

        data.write(b'\xaa\x969\x9c')  # 0xaa96399c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.invulnerable_skin_rules))

        data.write(b'\xf1H\xf7(')  # 0xf148f728
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.boost_ball_model.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe1\x8d\xc6\xfc')  # 0xe18dc6fc
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.boost_ball_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xacC\xba4')  # 0xac43ba34
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.boost_ball_glow))

        data.write(b'D\x9a\xa4\xaa')  # 0x449aa4aa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.swhc_0x449aa4aa))

        data.write(b'\x03E\xfa\x17')  # 0x345fa17
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.swhc_0x0345fa17))

        data.write(b',rWk')  # 0x2c72576b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0x2c72576b))

        data.write(b'\x9e\x02i\x1c')  # 0x9e02691c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.boost_ball_hit_player_sound))

        data.write(b'43\xbc\x8b')  # 0x3433bc8b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.boost_ball_collision))

        data.write(b'HA\x18+')  # 0x4841182b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa6\xc4 #')  # 0xa6c42023
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xa6c42023))

        data.write(b'\xd3Y60')  # 0xd3593630
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.ice_spread_sound))

        data.write(b'\x90\x8b\x06\xe9')  # 0x908b06e9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x908b06e9))

        data.write(b'IM\xe4\xa4')  # 0x494de4a4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x494de4a4))

        data.write(b'\xa8ad\x9f')  # 0xa861649f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.sound_0xa861649f))

        data.write(b'\x18@*\xa9')  # 0x18402aa9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x18402aa9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe7\x01\xda\xea')  # 0xe701daea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xe701daea))

        data.write(b'\xbfb\xb63')  # 0xbf62b633
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.phazon_projectile))

        data.write(b'\x8d\x12?\xe9')  # 0x8d123fe9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.wpsc))

        data.write(b'Xv\x9e\xb2')  # 0x58769eb2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x58769eb2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'M\x8es_')  # 0x4d8e735f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.phazon_projectile_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x83\x10d\x05')  # 0x83106405
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.phazon_enrage_sphere))

        data.write(b'\x8f:\xf2&')  # 0x8f3af226
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info_0x8f3af226.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf6\n\xc5\xcc')  # 0xf60ac5cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.alternate_scannable_info))

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
            unknown_0x72edeb7d=data['unknown_0x72edeb7d'],
            unknown_0x74fa22f0=data['unknown_0x74fa22f0'],
            glide_sound=data['glide_sound'],
            missile_ricochet_sound=data['missile_ricochet_sound'],
            unknown_0x6689925b=data['unknown_0x6689925b'],
            txtr_0x3863160b=data['txtr_0x3863160b'],
            unknown_0x2c6a3344=data['unknown_0x2c6a3344'],
            melee_attack_damage=DamageInfo.from_json(data['melee_attack_damage']),
            part_0x6d40aa56=data['part_0x6d40aa56'],
            part_0x9603a544=data['part_0x9603a544'],
            dive_attack_damage=DamageInfo.from_json(data['dive_attack_damage']),
            unknown_0x4aa5dd62=data['unknown_0x4aa5dd62'],
            unknown_0x1ad7dc21=data['unknown_0x1ad7dc21'],
            dive_attack_effect=data['dive_attack_effect'],
            scatter_shot_projectile=data['scatter_shot_projectile'],
            scatter_shot_projectile2=data['scatter_shot_projectile2'],
            scatter_shot_damage=DamageInfo.from_json(data['scatter_shot_damage']),
            unknown_0x378285b9=data['unknown_0x378285b9'],
            unknown_0xd242e25f=data['unknown_0xd242e25f'],
            normal_missile_projectile=data['normal_missile_projectile'],
            normal_missile_damage=DamageInfo.from_json(data['normal_missile_damage']),
            unknown_0x1f1ef7a9=data['unknown_0x1f1ef7a9'],
            unknown_0xc4a1a44e=data['unknown_0xc4a1a44e'],
            super_missile_projectile=data['super_missile_projectile'],
            super_missile_damage=DamageInfo.from_json(data['super_missile_damage']),
            freeze_beam_projectile=data['freeze_beam_projectile'],
            freeze_beam_damage=DamageInfo.from_json(data['freeze_beam_damage']),
            txtr_0x7ffeb33d=data['txtr_0x7ffeb33d'],
            damage_interrupt_threshold=data['damage_interrupt_threshold'],
            unknown_0xf317f4d5=data['unknown_0xf317f4d5'],
            sweep_swoosh=data['sweep_swoosh'],
            sweep_beam_damage=DamageInfo.from_json(data['sweep_beam_damage']),
            crsc=data['crsc'],
            sweep_beam_sound=data['sweep_beam_sound'],
            unknown_0x0ef8dc15=data['unknown_0x0ef8dc15'],
            invulnerable_model=data['invulnerable_model'],
            invulnerable_skin_rules=data['invulnerable_skin_rules'],
            boost_ball_model=AnimationParameters.from_json(data['boost_ball_model']),
            boost_ball_damage=DamageInfo.from_json(data['boost_ball_damage']),
            boost_ball_glow=data['boost_ball_glow'],
            swhc_0x449aa4aa=data['swhc_0x449aa4aa'],
            swhc_0x0345fa17=data['swhc_0x0345fa17'],
            sound_0x2c72576b=data['sound_0x2c72576b'],
            boost_ball_hit_player_sound=data['boost_ball_hit_player_sound'],
            boost_ball_collision=data['boost_ball_collision'],
            audio_playback_parms=AudioPlaybackParms.from_json(data['audio_playback_parms']),
            part_0xa6c42023=data['part_0xa6c42023'],
            ice_spread_sound=data['ice_spread_sound'],
            part_0x908b06e9=data['part_0x908b06e9'],
            part_0x494de4a4=data['part_0x494de4a4'],
            sound_0xa861649f=data['sound_0xa861649f'],
            damage_info_0x18402aa9=DamageInfo.from_json(data['damage_info_0x18402aa9']),
            part_0xe701daea=data['part_0xe701daea'],
            phazon_projectile=data['phazon_projectile'],
            wpsc=data['wpsc'],
            damage_info_0x58769eb2=DamageInfo.from_json(data['damage_info_0x58769eb2']),
            phazon_projectile_damage=DamageInfo.from_json(data['phazon_projectile_damage']),
            phazon_enrage_sphere=data['phazon_enrage_sphere'],
            damage_info_0x8f3af226=DamageInfo.from_json(data['damage_info_0x8f3af226']),
            alternate_scannable_info=data['alternate_scannable_info'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_0x72edeb7d': self.unknown_0x72edeb7d,
            'unknown_0x74fa22f0': self.unknown_0x74fa22f0,
            'glide_sound': self.glide_sound,
            'missile_ricochet_sound': self.missile_ricochet_sound,
            'unknown_0x6689925b': self.unknown_0x6689925b,
            'txtr_0x3863160b': self.txtr_0x3863160b,
            'unknown_0x2c6a3344': self.unknown_0x2c6a3344,
            'melee_attack_damage': self.melee_attack_damage.to_json(),
            'part_0x6d40aa56': self.part_0x6d40aa56,
            'part_0x9603a544': self.part_0x9603a544,
            'dive_attack_damage': self.dive_attack_damage.to_json(),
            'unknown_0x4aa5dd62': self.unknown_0x4aa5dd62,
            'unknown_0x1ad7dc21': self.unknown_0x1ad7dc21,
            'dive_attack_effect': self.dive_attack_effect,
            'scatter_shot_projectile': self.scatter_shot_projectile,
            'scatter_shot_projectile2': self.scatter_shot_projectile2,
            'scatter_shot_damage': self.scatter_shot_damage.to_json(),
            'unknown_0x378285b9': self.unknown_0x378285b9,
            'unknown_0xd242e25f': self.unknown_0xd242e25f,
            'normal_missile_projectile': self.normal_missile_projectile,
            'normal_missile_damage': self.normal_missile_damage.to_json(),
            'unknown_0x1f1ef7a9': self.unknown_0x1f1ef7a9,
            'unknown_0xc4a1a44e': self.unknown_0xc4a1a44e,
            'super_missile_projectile': self.super_missile_projectile,
            'super_missile_damage': self.super_missile_damage.to_json(),
            'freeze_beam_projectile': self.freeze_beam_projectile,
            'freeze_beam_damage': self.freeze_beam_damage.to_json(),
            'txtr_0x7ffeb33d': self.txtr_0x7ffeb33d,
            'damage_interrupt_threshold': self.damage_interrupt_threshold,
            'unknown_0xf317f4d5': self.unknown_0xf317f4d5,
            'sweep_swoosh': self.sweep_swoosh,
            'sweep_beam_damage': self.sweep_beam_damage.to_json(),
            'crsc': self.crsc,
            'sweep_beam_sound': self.sweep_beam_sound,
            'unknown_0x0ef8dc15': self.unknown_0x0ef8dc15,
            'invulnerable_model': self.invulnerable_model,
            'invulnerable_skin_rules': self.invulnerable_skin_rules,
            'boost_ball_model': self.boost_ball_model.to_json(),
            'boost_ball_damage': self.boost_ball_damage.to_json(),
            'boost_ball_glow': self.boost_ball_glow,
            'swhc_0x449aa4aa': self.swhc_0x449aa4aa,
            'swhc_0x0345fa17': self.swhc_0x0345fa17,
            'sound_0x2c72576b': self.sound_0x2c72576b,
            'boost_ball_hit_player_sound': self.boost_ball_hit_player_sound,
            'boost_ball_collision': self.boost_ball_collision,
            'audio_playback_parms': self.audio_playback_parms.to_json(),
            'part_0xa6c42023': self.part_0xa6c42023,
            'ice_spread_sound': self.ice_spread_sound,
            'part_0x908b06e9': self.part_0x908b06e9,
            'part_0x494de4a4': self.part_0x494de4a4,
            'sound_0xa861649f': self.sound_0xa861649f,
            'damage_info_0x18402aa9': self.damage_info_0x18402aa9.to_json(),
            'part_0xe701daea': self.part_0xe701daea,
            'phazon_projectile': self.phazon_projectile,
            'wpsc': self.wpsc,
            'damage_info_0x58769eb2': self.damage_info_0x58769eb2.to_json(),
            'phazon_projectile_damage': self.phazon_projectile_damage.to_json(),
            'phazon_enrage_sphere': self.phazon_enrage_sphere,
            'damage_info_0x8f3af226': self.damage_info_0x8f3af226.to_json(),
            'alternate_scannable_info': self.alternate_scannable_info,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_glide_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.glide_sound)

    def _dependencies_for_missile_ricochet_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.missile_ricochet_sound)

    def _dependencies_for_txtr_0x3863160b(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.txtr_0x3863160b)

    def _dependencies_for_melee_attack_damage(self, asset_manager):
        yield from self.melee_attack_damage.dependencies_for(asset_manager)

    def _dependencies_for_part_0x6d40aa56(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x6d40aa56)

    def _dependencies_for_part_0x9603a544(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x9603a544)

    def _dependencies_for_dive_attack_damage(self, asset_manager):
        yield from self.dive_attack_damage.dependencies_for(asset_manager)

    def _dependencies_for_dive_attack_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.dive_attack_effect)

    def _dependencies_for_scatter_shot_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scatter_shot_projectile)

    def _dependencies_for_scatter_shot_projectile2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scatter_shot_projectile2)

    def _dependencies_for_scatter_shot_damage(self, asset_manager):
        yield from self.scatter_shot_damage.dependencies_for(asset_manager)

    def _dependencies_for_normal_missile_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.normal_missile_projectile)

    def _dependencies_for_normal_missile_damage(self, asset_manager):
        yield from self.normal_missile_damage.dependencies_for(asset_manager)

    def _dependencies_for_super_missile_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.super_missile_projectile)

    def _dependencies_for_super_missile_damage(self, asset_manager):
        yield from self.super_missile_damage.dependencies_for(asset_manager)

    def _dependencies_for_freeze_beam_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.freeze_beam_projectile)

    def _dependencies_for_freeze_beam_damage(self, asset_manager):
        yield from self.freeze_beam_damage.dependencies_for(asset_manager)

    def _dependencies_for_txtr_0x7ffeb33d(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.txtr_0x7ffeb33d)

    def _dependencies_for_sweep_swoosh(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.sweep_swoosh)

    def _dependencies_for_sweep_beam_damage(self, asset_manager):
        yield from self.sweep_beam_damage.dependencies_for(asset_manager)

    def _dependencies_for_crsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.crsc)

    def _dependencies_for_invulnerable_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.invulnerable_model)

    def _dependencies_for_invulnerable_skin_rules(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.invulnerable_skin_rules)

    def _dependencies_for_boost_ball_model(self, asset_manager):
        yield from self.boost_ball_model.dependencies_for(asset_manager)

    def _dependencies_for_boost_ball_damage(self, asset_manager):
        yield from self.boost_ball_damage.dependencies_for(asset_manager)

    def _dependencies_for_boost_ball_glow(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.boost_ball_glow)

    def _dependencies_for_swhc_0x449aa4aa(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.swhc_0x449aa4aa)

    def _dependencies_for_swhc_0x0345fa17(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.swhc_0x0345fa17)

    def _dependencies_for_sound_0x2c72576b(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0x2c72576b)

    def _dependencies_for_boost_ball_hit_player_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.boost_ball_hit_player_sound)

    def _dependencies_for_boost_ball_collision(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.boost_ball_collision)

    def _dependencies_for_audio_playback_parms(self, asset_manager):
        yield from self.audio_playback_parms.dependencies_for(asset_manager)

    def _dependencies_for_part_0xa6c42023(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xa6c42023)

    def _dependencies_for_ice_spread_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.ice_spread_sound)

    def _dependencies_for_part_0x908b06e9(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x908b06e9)

    def _dependencies_for_part_0x494de4a4(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x494de4a4)

    def _dependencies_for_sound_0xa861649f(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.sound_0xa861649f)

    def _dependencies_for_damage_info_0x18402aa9(self, asset_manager):
        yield from self.damage_info_0x18402aa9.dependencies_for(asset_manager)

    def _dependencies_for_part_0xe701daea(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xe701daea)

    def _dependencies_for_phazon_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.phazon_projectile)

    def _dependencies_for_wpsc(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.wpsc)

    def _dependencies_for_damage_info_0x58769eb2(self, asset_manager):
        yield from self.damage_info_0x58769eb2.dependencies_for(asset_manager)

    def _dependencies_for_phazon_projectile_damage(self, asset_manager):
        yield from self.phazon_projectile_damage.dependencies_for(asset_manager)

    def _dependencies_for_phazon_enrage_sphere(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.phazon_enrage_sphere)

    def _dependencies_for_damage_info_0x8f3af226(self, asset_manager):
        yield from self.damage_info_0x8f3af226.dependencies_for(asset_manager)

    def _dependencies_for_alternate_scannable_info(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.alternate_scannable_info)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_glide_sound, "glide_sound", "int"),
            (self._dependencies_for_missile_ricochet_sound, "missile_ricochet_sound", "int"),
            (self._dependencies_for_txtr_0x3863160b, "txtr_0x3863160b", "AssetId"),
            (self._dependencies_for_melee_attack_damage, "melee_attack_damage", "DamageInfo"),
            (self._dependencies_for_part_0x6d40aa56, "part_0x6d40aa56", "AssetId"),
            (self._dependencies_for_part_0x9603a544, "part_0x9603a544", "AssetId"),
            (self._dependencies_for_dive_attack_damage, "dive_attack_damage", "DamageInfo"),
            (self._dependencies_for_dive_attack_effect, "dive_attack_effect", "AssetId"),
            (self._dependencies_for_scatter_shot_projectile, "scatter_shot_projectile", "AssetId"),
            (self._dependencies_for_scatter_shot_projectile2, "scatter_shot_projectile2", "AssetId"),
            (self._dependencies_for_scatter_shot_damage, "scatter_shot_damage", "DamageInfo"),
            (self._dependencies_for_normal_missile_projectile, "normal_missile_projectile", "AssetId"),
            (self._dependencies_for_normal_missile_damage, "normal_missile_damage", "DamageInfo"),
            (self._dependencies_for_super_missile_projectile, "super_missile_projectile", "AssetId"),
            (self._dependencies_for_super_missile_damage, "super_missile_damage", "DamageInfo"),
            (self._dependencies_for_freeze_beam_projectile, "freeze_beam_projectile", "AssetId"),
            (self._dependencies_for_freeze_beam_damage, "freeze_beam_damage", "DamageInfo"),
            (self._dependencies_for_txtr_0x7ffeb33d, "txtr_0x7ffeb33d", "AssetId"),
            (self._dependencies_for_sweep_swoosh, "sweep_swoosh", "AssetId"),
            (self._dependencies_for_sweep_beam_damage, "sweep_beam_damage", "DamageInfo"),
            (self._dependencies_for_crsc, "crsc", "AssetId"),
            (self._dependencies_for_invulnerable_model, "invulnerable_model", "AssetId"),
            (self._dependencies_for_invulnerable_skin_rules, "invulnerable_skin_rules", "AssetId"),
            (self._dependencies_for_boost_ball_model, "boost_ball_model", "AnimationParameters"),
            (self._dependencies_for_boost_ball_damage, "boost_ball_damage", "DamageInfo"),
            (self._dependencies_for_boost_ball_glow, "boost_ball_glow", "AssetId"),
            (self._dependencies_for_swhc_0x449aa4aa, "swhc_0x449aa4aa", "AssetId"),
            (self._dependencies_for_swhc_0x0345fa17, "swhc_0x0345fa17", "AssetId"),
            (self._dependencies_for_sound_0x2c72576b, "sound_0x2c72576b", "int"),
            (self._dependencies_for_boost_ball_hit_player_sound, "boost_ball_hit_player_sound", "int"),
            (self._dependencies_for_boost_ball_collision, "boost_ball_collision", "AssetId"),
            (self._dependencies_for_audio_playback_parms, "audio_playback_parms", "AudioPlaybackParms"),
            (self._dependencies_for_part_0xa6c42023, "part_0xa6c42023", "AssetId"),
            (self._dependencies_for_ice_spread_sound, "ice_spread_sound", "int"),
            (self._dependencies_for_part_0x908b06e9, "part_0x908b06e9", "AssetId"),
            (self._dependencies_for_part_0x494de4a4, "part_0x494de4a4", "AssetId"),
            (self._dependencies_for_sound_0xa861649f, "sound_0xa861649f", "int"),
            (self._dependencies_for_damage_info_0x18402aa9, "damage_info_0x18402aa9", "DamageInfo"),
            (self._dependencies_for_part_0xe701daea, "part_0xe701daea", "AssetId"),
            (self._dependencies_for_phazon_projectile, "phazon_projectile", "AssetId"),
            (self._dependencies_for_wpsc, "wpsc", "AssetId"),
            (self._dependencies_for_damage_info_0x58769eb2, "damage_info_0x58769eb2", "DamageInfo"),
            (self._dependencies_for_phazon_projectile_damage, "phazon_projectile_damage", "DamageInfo"),
            (self._dependencies_for_phazon_enrage_sphere, "phazon_enrage_sphere", "AssetId"),
            (self._dependencies_for_damage_info_0x8f3af226, "damage_info_0x8f3af226", "DamageInfo"),
            (self._dependencies_for_alternate_scannable_info, "alternate_scannable_info", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DarkSamus.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'detection_range': 32.0, 'collision_radius': 0.5, 'collision_height': 1.0, 'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_unknown_0x72edeb7d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x74fa22f0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_glide_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_missile_ricochet_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6689925b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_txtr_0x3863160b(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x2c6a3344(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_part_0x6d40aa56(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x9603a544(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_dive_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x4aa5dd62(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x1ad7dc21(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dive_attack_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_scatter_shot_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_scatter_shot_projectile2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_scatter_shot_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x378285b9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd242e25f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_normal_missile_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_normal_missile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown_0x1f1ef7a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc4a1a44e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_super_missile_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_super_missile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_freeze_beam_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_freeze_beam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_txtr_0x7ffeb33d(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_damage_interrupt_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf317f4d5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_sweep_swoosh(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sweep_beam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_crsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sweep_beam_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x0ef8dc15(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_invulnerable_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_invulnerable_skin_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_boost_ball_model(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_boost_ball_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_boost_ball_glow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_swhc_0x449aa4aa(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_swhc_0x0345fa17(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_0x2c72576b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_boost_ball_hit_player_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_boost_ball_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_audio_playback_parms(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_part_0xa6c42023(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ice_spread_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_part_0x908b06e9(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0x494de4a4(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sound_0xa861649f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_damage_info_0x18402aa9(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_part_0xe701daea(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_phazon_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_wpsc(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_damage_info_0x58769eb2(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_phazon_projectile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 10.0, 'di_radius': 5.0})


def _decode_phazon_enrage_sphere(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_damage_info_0x8f3af226(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_alternate_scannable_info(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x72edeb7d: ('unknown_0x72edeb7d', _decode_unknown_0x72edeb7d),
    0x74fa22f0: ('unknown_0x74fa22f0', _decode_unknown_0x74fa22f0),
    0x1f468967: ('glide_sound', _decode_glide_sound),
    0x1a08aadc: ('missile_ricochet_sound', _decode_missile_ricochet_sound),
    0x6689925b: ('unknown_0x6689925b', _decode_unknown_0x6689925b),
    0x3863160b: ('txtr_0x3863160b', _decode_txtr_0x3863160b),
    0x2c6a3344: ('unknown_0x2c6a3344', _decode_unknown_0x2c6a3344),
    0x4d790ee9: ('melee_attack_damage', _decode_melee_attack_damage),
    0x6d40aa56: ('part_0x6d40aa56', _decode_part_0x6d40aa56),
    0x9603a544: ('part_0x9603a544', _decode_part_0x9603a544),
    0x8688f535: ('dive_attack_damage', _decode_dive_attack_damage),
    0x4aa5dd62: ('unknown_0x4aa5dd62', _decode_unknown_0x4aa5dd62),
    0x1ad7dc21: ('unknown_0x1ad7dc21', _decode_unknown_0x1ad7dc21),
    0xed30b0ef: ('dive_attack_effect', _decode_dive_attack_effect),
    0x855f0749: ('scatter_shot_projectile', _decode_scatter_shot_projectile),
    0x83a5517f: ('scatter_shot_projectile2', _decode_scatter_shot_projectile2),
    0x8ea87062: ('scatter_shot_damage', _decode_scatter_shot_damage),
    0x378285b9: ('unknown_0x378285b9', _decode_unknown_0x378285b9),
    0xd242e25f: ('unknown_0xd242e25f', _decode_unknown_0xd242e25f),
    0xe00db62d: ('normal_missile_projectile', _decode_normal_missile_projectile),
    0xc4128792: ('normal_missile_damage', _decode_normal_missile_damage),
    0x1f1ef7a9: ('unknown_0x1f1ef7a9', _decode_unknown_0x1f1ef7a9),
    0xc4a1a44e: ('unknown_0xc4a1a44e', _decode_unknown_0xc4a1a44e),
    0x29db4ee4: ('super_missile_projectile', _decode_super_missile_projectile),
    0x26632b7e: ('super_missile_damage', _decode_super_missile_damage),
    0xf9104a69: ('freeze_beam_projectile', _decode_freeze_beam_projectile),
    0xb5ba1fe7: ('freeze_beam_damage', _decode_freeze_beam_damage),
    0x7ffeb33d: ('txtr_0x7ffeb33d', _decode_txtr_0x7ffeb33d),
    0x8f70d3f2: ('damage_interrupt_threshold', _decode_damage_interrupt_threshold),
    0xf317f4d5: ('unknown_0xf317f4d5', _decode_unknown_0xf317f4d5),
    0xd2122711: ('sweep_swoosh', _decode_sweep_swoosh),
    0x8c2bfe0: ('sweep_beam_damage', _decode_sweep_beam_damage),
    0x68b658f2: ('crsc', _decode_crsc),
    0xea17cb66: ('sweep_beam_sound', _decode_sweep_beam_sound),
    0xef8dc15: ('unknown_0x0ef8dc15', _decode_unknown_0x0ef8dc15),
    0x72df331: ('invulnerable_model', _decode_invulnerable_model),
    0xaa96399c: ('invulnerable_skin_rules', _decode_invulnerable_skin_rules),
    0xf148f728: ('boost_ball_model', _decode_boost_ball_model),
    0xe18dc6fc: ('boost_ball_damage', _decode_boost_ball_damage),
    0xac43ba34: ('boost_ball_glow', _decode_boost_ball_glow),
    0x449aa4aa: ('swhc_0x449aa4aa', _decode_swhc_0x449aa4aa),
    0x345fa17: ('swhc_0x0345fa17', _decode_swhc_0x0345fa17),
    0x2c72576b: ('sound_0x2c72576b', _decode_sound_0x2c72576b),
    0x9e02691c: ('boost_ball_hit_player_sound', _decode_boost_ball_hit_player_sound),
    0x3433bc8b: ('boost_ball_collision', _decode_boost_ball_collision),
    0x4841182b: ('audio_playback_parms', _decode_audio_playback_parms),
    0xa6c42023: ('part_0xa6c42023', _decode_part_0xa6c42023),
    0xd3593630: ('ice_spread_sound', _decode_ice_spread_sound),
    0x908b06e9: ('part_0x908b06e9', _decode_part_0x908b06e9),
    0x494de4a4: ('part_0x494de4a4', _decode_part_0x494de4a4),
    0xa861649f: ('sound_0xa861649f', _decode_sound_0xa861649f),
    0x18402aa9: ('damage_info_0x18402aa9', _decode_damage_info_0x18402aa9),
    0xe701daea: ('part_0xe701daea', _decode_part_0xe701daea),
    0xbf62b633: ('phazon_projectile', _decode_phazon_projectile),
    0x8d123fe9: ('wpsc', _decode_wpsc),
    0x58769eb2: ('damage_info_0x58769eb2', _decode_damage_info_0x58769eb2),
    0x4d8e735f: ('phazon_projectile_damage', _decode_phazon_projectile_damage),
    0x83106405: ('phazon_enrage_sphere', _decode_phazon_enrage_sphere),
    0x8f3af226: ('damage_info_0x8f3af226', _decode_damage_info_0x8f3af226),
    0xf60ac5cc: ('alternate_scannable_info', _decode_alternate_scannable_info),
}
