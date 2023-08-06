# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.AudioPlaybackParms import AudioPlaybackParms
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.DamageVulnerability import DamageVulnerability
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.IngPossessionData import IngPossessionData
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Grenchler(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_0x04d51e3a: float = dataclasses.field(default=50.0)
    is_grapple_guardian: bool = dataclasses.field(default=False)
    has_health_bar: bool = dataclasses.field(default=False)
    damage_vulnerability: DamageVulnerability = dataclasses.field(default_factory=DamageVulnerability)
    tail: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0x0abef809: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    tailless_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    tailless_skin_rules: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    unknown_0x9b193ae8: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    unknown_0xc24cf580: AnimationParameters = dataclasses.field(default_factory=AnimationParameters)
    cmdl: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    cskr: AssetId = dataclasses.field(metadata={'asset_types': ['CSKR']}, default=default_asset_id)
    tail_hit_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    tail_destroyed_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    unknown_0x5d8f2bee: float = dataclasses.field(default=4.5)
    unknown_0x7bd1a35f: float = dataclasses.field(default=-1.0)
    unknown_0xea4b88c8: float = dataclasses.field(default=8.0)
    unknown_0xaa04f0be: float = dataclasses.field(default=40.0)
    unknown_0x98d5d373: float = dataclasses.field(default=2.0)
    unknown_0xd89aab05: float = dataclasses.field(default=8.0)
    unknown_0x2e6096ee: float = dataclasses.field(default=2.0)
    unknown_0x6e2fee98: float = dataclasses.field(default=3.0)
    unknown_0x49632b31: float = dataclasses.field(default=6.0)
    bite_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x262b2508: float = dataclasses.field(default=9.0)
    unknown_0x66645d7e: float = dataclasses.field(default=25.0)
    unknown_0x909e6095: float = dataclasses.field(default=1.0)
    unknown_0xd0d118e3: float = dataclasses.field(default=1.5)
    electric_effect: AssetId = dataclasses.field(metadata={'asset_types': ['ELSC']}, default=default_asset_id)
    beam_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x680ce795: float = dataclasses.field(default=45.0)
    audio_playback_parms_0xad47febe: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    unknown_0x06f7ceed: float = dataclasses.field(default=0.5)
    unknown_0x46b8b69b: float = dataclasses.field(default=8.0)
    unknown_0xb0428b70: float = dataclasses.field(default=1.0)
    unknown_0xf00df306: float = dataclasses.field(default=1.5)
    unknown_0xb00775e6: float = dataclasses.field(default=20.0)
    burst_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    burst_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    surface_rings_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xbf4daae6: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_always_ff: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part_0xffcee1a9: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grapple_swoosh: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grapple_beam_part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grapple_hit_fx: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    grapple_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    audio_playback_parms_0xb6b9074b: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    beam_effect: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    unknown_0xd4753ff4: int = dataclasses.field(default=4)
    unknown_0x05fc6001: float = dataclasses.field(default=20.0)
    unknown_0x13e5b580: float = dataclasses.field(default=20.0)
    unknown_0xfc6f199d: float = dataclasses.field(default=10.0)
    grapple_visor_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    damage_info: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    part_0x54b6bfa1: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    audio_playback_parms_0x5cf705f2: AudioPlaybackParms = dataclasses.field(default_factory=AudioPlaybackParms)
    part_0xb9f9f4f2: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    alternate_scannable_info: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
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
        return 'GRCH'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Grenchler.rel']

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
        self.patterned.to_stream(data, default_override={'leash_radius': 100.0, 'collision_radius': 1.600000023841858, 'collision_height': 2.5, 'step_up_height': 1.0, 'creature_size': 1})
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

        data.write(b'\x04\xd5\x1e:')  # 0x4d51e3a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x04d51e3a))

        data.write(b'3@\x8e\x7f')  # 0x33408e7f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_grapple_guardian))

        data.write(b'g\xb6\xea\x0b')  # 0x67b6ea0b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.has_health_bar))

        data.write(b'\ns&\xa3')  # 0xa7326a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_vulnerability.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa1\x8fbk')  # 0xa18f626b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.tail.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\n\xbe\xf8\t')  # 0xabef809
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x0abef809.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'O:Ef')  # 0x4f3a4566
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.tailless_model))

        data.write(b'@\x1b\xc1\x11')  # 0x401bc111
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.tailless_skin_rules))

        data.write(b'\x9b\x19:\xe8')  # 0x9b193ae8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x9b193ae8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc2L\xf5\x80')  # 0xc24cf580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xc24cf580.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'r%\x8f\xe7')  # 0x72258fe7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.cmdl))

        data.write(b'\xe5\xfb\xa2L')  # 0xe5fba24c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.cskr))

        data.write(b'U\xc5\x12\x13')  # 0x55c51213
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.tail_hit_sound))

        data.write(b'8^G8')  # 0x385e4738
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.tail_destroyed_sound))

        data.write(b']\x8f+\xee')  # 0x5d8f2bee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5d8f2bee))

        data.write(b'{\xd1\xa3_')  # 0x7bd1a35f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x7bd1a35f))

        data.write(b'\xeaK\x88\xc8')  # 0xea4b88c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xea4b88c8))

        data.write(b'\xaa\x04\xf0\xbe')  # 0xaa04f0be
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xaa04f0be))

        data.write(b'\x98\xd5\xd3s')  # 0x98d5d373
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x98d5d373))

        data.write(b'\xd8\x9a\xab\x05')  # 0xd89aab05
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd89aab05))

        data.write(b'.`\x96\xee')  # 0x2e6096ee
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2e6096ee))

        data.write(b'n/\xee\x98')  # 0x6e2fee98
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6e2fee98))

        data.write(b'Ic+1')  # 0x49632b31
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x49632b31))

        data.write(b'\xdfclK')  # 0xdf636c4b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bite_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&+%\x08')  # 0x262b2508
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x262b2508))

        data.write(b'fd]~')  # 0x66645d7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x66645d7e))

        data.write(b'\x90\x9e`\x95')  # 0x909e6095
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x909e6095))

        data.write(b'\xd0\xd1\x18\xe3')  # 0xd0d118e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd0d118e3))

        data.write(b'I\xfa\xe1C')  # 0x49fae143
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.electric_effect))

        data.write(b'\x13\xe3\x0eM')  # 0x13e30e4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.beam_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\x0c\xe7\x95')  # 0x680ce795
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x680ce795))

        data.write(b'\xadG\xfe\xbe')  # 0xad47febe
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0xad47febe.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x06\xf7\xce\xed')  # 0x6f7ceed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x06f7ceed))

        data.write(b'F\xb8\xb6\x9b')  # 0x46b8b69b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x46b8b69b))

        data.write(b'\xb0B\x8bp')  # 0xb0428b70
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb0428b70))

        data.write(b'\xf0\r\xf3\x06')  # 0xf00df306
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf00df306))

        data.write(b'\xb0\x07u\xe6')  # 0xb00775e6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xb00775e6))

        data.write(b'~\xf9\xaag')  # 0x7ef9aa67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.burst_projectile))

        data.write(b'R\x85\xdb\x00')  # 0x5285db00
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.burst_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'0\xb8\x1a~')  # 0x30b81a7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.surface_rings_effect))

        data.write(b'\xbfM\xaa\xe6')  # 0xbf4daae6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xbf4daae6))

        data.write(b'p$zn')  # 0x70247a6e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_always_ff))

        data.write(b'\xff\xce\xe1\xa9')  # 0xffcee1a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xffcee1a9))

        data.write(b'\xae\x1f*&')  # 0xae1f2a26
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grapple_swoosh))

        data.write(b'\r\xab\xf0\xaf')  # 0xdabf0af
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grapple_beam_part))

        data.write(b'\xe5\x17F\xd1')  # 0xe51746d1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grapple_hit_fx))

        data.write(b',\xe7R\x0f')  # 0x2ce7520f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.grapple_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6\xb9\x07K')  # 0xb6b9074b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0xb6b9074b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05C\x9a\x08')  # 0x5439a08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.beam_effect))

        data.write(b'\xd4u?\xf4')  # 0xd4753ff4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xd4753ff4))

        data.write(b'\x05\xfc`\x01')  # 0x5fc6001
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x05fc6001))

        data.write(b'\x13\xe5\xb5\x80')  # 0x13e5b580
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x13e5b580))

        data.write(b'\xfco\x19\x9d')  # 0xfc6f199d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xfc6f199d))

        data.write(b'\xf6P%\x96')  # 0xf6502596
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.grapple_visor_effect))

        data.write(b'n\xc2d\x14')  # 0x6ec26414
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.damage_info.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'T\xb6\xbf\xa1')  # 0x54b6bfa1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0x54b6bfa1))

        data.write(b'\\\xf7\x05\xf2')  # 0x5cf705f2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.audio_playback_parms_0x5cf705f2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb9\xf9\xf4\xf2')  # 0xb9f9f4f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part_0xb9f9f4f2))

        data.write(b'\xf6\n\xc5\xcc')  # 0xf60ac5cc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.alternate_scannable_info))

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
            unknown_0x04d51e3a=data['unknown_0x04d51e3a'],
            is_grapple_guardian=data['is_grapple_guardian'],
            has_health_bar=data['has_health_bar'],
            damage_vulnerability=DamageVulnerability.from_json(data['damage_vulnerability']),
            tail=AnimationParameters.from_json(data['tail']),
            unknown_0x0abef809=AnimationParameters.from_json(data['unknown_0x0abef809']),
            tailless_model=data['tailless_model'],
            tailless_skin_rules=data['tailless_skin_rules'],
            unknown_0x9b193ae8=AnimationParameters.from_json(data['unknown_0x9b193ae8']),
            unknown_0xc24cf580=AnimationParameters.from_json(data['unknown_0xc24cf580']),
            cmdl=data['cmdl'],
            cskr=data['cskr'],
            tail_hit_sound=data['tail_hit_sound'],
            tail_destroyed_sound=data['tail_destroyed_sound'],
            unknown_0x5d8f2bee=data['unknown_0x5d8f2bee'],
            unknown_0x7bd1a35f=data['unknown_0x7bd1a35f'],
            unknown_0xea4b88c8=data['unknown_0xea4b88c8'],
            unknown_0xaa04f0be=data['unknown_0xaa04f0be'],
            unknown_0x98d5d373=data['unknown_0x98d5d373'],
            unknown_0xd89aab05=data['unknown_0xd89aab05'],
            unknown_0x2e6096ee=data['unknown_0x2e6096ee'],
            unknown_0x6e2fee98=data['unknown_0x6e2fee98'],
            unknown_0x49632b31=data['unknown_0x49632b31'],
            bite_damage=DamageInfo.from_json(data['bite_damage']),
            unknown_0x262b2508=data['unknown_0x262b2508'],
            unknown_0x66645d7e=data['unknown_0x66645d7e'],
            unknown_0x909e6095=data['unknown_0x909e6095'],
            unknown_0xd0d118e3=data['unknown_0xd0d118e3'],
            electric_effect=data['electric_effect'],
            beam_damage=DamageInfo.from_json(data['beam_damage']),
            unknown_0x680ce795=data['unknown_0x680ce795'],
            audio_playback_parms_0xad47febe=AudioPlaybackParms.from_json(data['audio_playback_parms_0xad47febe']),
            unknown_0x06f7ceed=data['unknown_0x06f7ceed'],
            unknown_0x46b8b69b=data['unknown_0x46b8b69b'],
            unknown_0xb0428b70=data['unknown_0xb0428b70'],
            unknown_0xf00df306=data['unknown_0xf00df306'],
            unknown_0xb00775e6=data['unknown_0xb00775e6'],
            burst_projectile=data['burst_projectile'],
            burst_damage=DamageInfo.from_json(data['burst_damage']),
            surface_rings_effect=data['surface_rings_effect'],
            part_0xbf4daae6=data['part_0xbf4daae6'],
            part_always_ff=data['part_always_ff'],
            part_0xffcee1a9=data['part_0xffcee1a9'],
            grapple_swoosh=data['grapple_swoosh'],
            grapple_beam_part=data['grapple_beam_part'],
            grapple_hit_fx=data['grapple_hit_fx'],
            grapple_damage=DamageInfo.from_json(data['grapple_damage']),
            audio_playback_parms_0xb6b9074b=AudioPlaybackParms.from_json(data['audio_playback_parms_0xb6b9074b']),
            beam_effect=data['beam_effect'],
            unknown_0xd4753ff4=data['unknown_0xd4753ff4'],
            unknown_0x05fc6001=data['unknown_0x05fc6001'],
            unknown_0x13e5b580=data['unknown_0x13e5b580'],
            unknown_0xfc6f199d=data['unknown_0xfc6f199d'],
            grapple_visor_effect=data['grapple_visor_effect'],
            damage_info=DamageInfo.from_json(data['damage_info']),
            part_0x54b6bfa1=data['part_0x54b6bfa1'],
            audio_playback_parms_0x5cf705f2=AudioPlaybackParms.from_json(data['audio_playback_parms_0x5cf705f2']),
            part_0xb9f9f4f2=data['part_0xb9f9f4f2'],
            alternate_scannable_info=data['alternate_scannable_info'],
            ing_possession_data=IngPossessionData.from_json(data['ing_possession_data']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_0x04d51e3a': self.unknown_0x04d51e3a,
            'is_grapple_guardian': self.is_grapple_guardian,
            'has_health_bar': self.has_health_bar,
            'damage_vulnerability': self.damage_vulnerability.to_json(),
            'tail': self.tail.to_json(),
            'unknown_0x0abef809': self.unknown_0x0abef809.to_json(),
            'tailless_model': self.tailless_model,
            'tailless_skin_rules': self.tailless_skin_rules,
            'unknown_0x9b193ae8': self.unknown_0x9b193ae8.to_json(),
            'unknown_0xc24cf580': self.unknown_0xc24cf580.to_json(),
            'cmdl': self.cmdl,
            'cskr': self.cskr,
            'tail_hit_sound': self.tail_hit_sound,
            'tail_destroyed_sound': self.tail_destroyed_sound,
            'unknown_0x5d8f2bee': self.unknown_0x5d8f2bee,
            'unknown_0x7bd1a35f': self.unknown_0x7bd1a35f,
            'unknown_0xea4b88c8': self.unknown_0xea4b88c8,
            'unknown_0xaa04f0be': self.unknown_0xaa04f0be,
            'unknown_0x98d5d373': self.unknown_0x98d5d373,
            'unknown_0xd89aab05': self.unknown_0xd89aab05,
            'unknown_0x2e6096ee': self.unknown_0x2e6096ee,
            'unknown_0x6e2fee98': self.unknown_0x6e2fee98,
            'unknown_0x49632b31': self.unknown_0x49632b31,
            'bite_damage': self.bite_damage.to_json(),
            'unknown_0x262b2508': self.unknown_0x262b2508,
            'unknown_0x66645d7e': self.unknown_0x66645d7e,
            'unknown_0x909e6095': self.unknown_0x909e6095,
            'unknown_0xd0d118e3': self.unknown_0xd0d118e3,
            'electric_effect': self.electric_effect,
            'beam_damage': self.beam_damage.to_json(),
            'unknown_0x680ce795': self.unknown_0x680ce795,
            'audio_playback_parms_0xad47febe': self.audio_playback_parms_0xad47febe.to_json(),
            'unknown_0x06f7ceed': self.unknown_0x06f7ceed,
            'unknown_0x46b8b69b': self.unknown_0x46b8b69b,
            'unknown_0xb0428b70': self.unknown_0xb0428b70,
            'unknown_0xf00df306': self.unknown_0xf00df306,
            'unknown_0xb00775e6': self.unknown_0xb00775e6,
            'burst_projectile': self.burst_projectile,
            'burst_damage': self.burst_damage.to_json(),
            'surface_rings_effect': self.surface_rings_effect,
            'part_0xbf4daae6': self.part_0xbf4daae6,
            'part_always_ff': self.part_always_ff,
            'part_0xffcee1a9': self.part_0xffcee1a9,
            'grapple_swoosh': self.grapple_swoosh,
            'grapple_beam_part': self.grapple_beam_part,
            'grapple_hit_fx': self.grapple_hit_fx,
            'grapple_damage': self.grapple_damage.to_json(),
            'audio_playback_parms_0xb6b9074b': self.audio_playback_parms_0xb6b9074b.to_json(),
            'beam_effect': self.beam_effect,
            'unknown_0xd4753ff4': self.unknown_0xd4753ff4,
            'unknown_0x05fc6001': self.unknown_0x05fc6001,
            'unknown_0x13e5b580': self.unknown_0x13e5b580,
            'unknown_0xfc6f199d': self.unknown_0xfc6f199d,
            'grapple_visor_effect': self.grapple_visor_effect,
            'damage_info': self.damage_info.to_json(),
            'part_0x54b6bfa1': self.part_0x54b6bfa1,
            'audio_playback_parms_0x5cf705f2': self.audio_playback_parms_0x5cf705f2.to_json(),
            'part_0xb9f9f4f2': self.part_0xb9f9f4f2,
            'alternate_scannable_info': self.alternate_scannable_info,
            'ing_possession_data': self.ing_possession_data.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_damage_vulnerability(self, asset_manager):
        yield from self.damage_vulnerability.dependencies_for(asset_manager)

    def _dependencies_for_tail(self, asset_manager):
        yield from self.tail.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0x0abef809(self, asset_manager):
        yield from self.unknown_0x0abef809.dependencies_for(asset_manager)

    def _dependencies_for_tailless_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.tailless_model)

    def _dependencies_for_tailless_skin_rules(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.tailless_skin_rules)

    def _dependencies_for_unknown_0x9b193ae8(self, asset_manager):
        yield from self.unknown_0x9b193ae8.dependencies_for(asset_manager)

    def _dependencies_for_unknown_0xc24cf580(self, asset_manager):
        yield from self.unknown_0xc24cf580.dependencies_for(asset_manager)

    def _dependencies_for_cmdl(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.cmdl)

    def _dependencies_for_cskr(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.cskr)

    def _dependencies_for_tail_hit_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.tail_hit_sound)

    def _dependencies_for_tail_destroyed_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.tail_destroyed_sound)

    def _dependencies_for_bite_damage(self, asset_manager):
        yield from self.bite_damage.dependencies_for(asset_manager)

    def _dependencies_for_electric_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.electric_effect)

    def _dependencies_for_beam_damage(self, asset_manager):
        yield from self.beam_damage.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0xad47febe(self, asset_manager):
        yield from self.audio_playback_parms_0xad47febe.dependencies_for(asset_manager)

    def _dependencies_for_burst_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.burst_projectile)

    def _dependencies_for_burst_damage(self, asset_manager):
        yield from self.burst_damage.dependencies_for(asset_manager)

    def _dependencies_for_surface_rings_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.surface_rings_effect)

    def _dependencies_for_part_0xbf4daae6(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xbf4daae6)

    def _dependencies_for_part_always_ff(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_always_ff)

    def _dependencies_for_part_0xffcee1a9(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xffcee1a9)

    def _dependencies_for_grapple_swoosh(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grapple_swoosh)

    def _dependencies_for_grapple_beam_part(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grapple_beam_part)

    def _dependencies_for_grapple_hit_fx(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grapple_hit_fx)

    def _dependencies_for_grapple_damage(self, asset_manager):
        yield from self.grapple_damage.dependencies_for(asset_manager)

    def _dependencies_for_audio_playback_parms_0xb6b9074b(self, asset_manager):
        yield from self.audio_playback_parms_0xb6b9074b.dependencies_for(asset_manager)

    def _dependencies_for_beam_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.beam_effect)

    def _dependencies_for_grapple_visor_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.grapple_visor_effect)

    def _dependencies_for_damage_info(self, asset_manager):
        yield from self.damage_info.dependencies_for(asset_manager)

    def _dependencies_for_part_0x54b6bfa1(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0x54b6bfa1)

    def _dependencies_for_audio_playback_parms_0x5cf705f2(self, asset_manager):
        yield from self.audio_playback_parms_0x5cf705f2.dependencies_for(asset_manager)

    def _dependencies_for_part_0xb9f9f4f2(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part_0xb9f9f4f2)

    def _dependencies_for_alternate_scannable_info(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.alternate_scannable_info)

    def _dependencies_for_ing_possession_data(self, asset_manager):
        yield from self.ing_possession_data.dependencies_for(asset_manager)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_damage_vulnerability, "damage_vulnerability", "DamageVulnerability"),
            (self._dependencies_for_tail, "tail", "AnimationParameters"),
            (self._dependencies_for_unknown_0x0abef809, "unknown_0x0abef809", "AnimationParameters"),
            (self._dependencies_for_tailless_model, "tailless_model", "AssetId"),
            (self._dependencies_for_tailless_skin_rules, "tailless_skin_rules", "AssetId"),
            (self._dependencies_for_unknown_0x9b193ae8, "unknown_0x9b193ae8", "AnimationParameters"),
            (self._dependencies_for_unknown_0xc24cf580, "unknown_0xc24cf580", "AnimationParameters"),
            (self._dependencies_for_cmdl, "cmdl", "AssetId"),
            (self._dependencies_for_cskr, "cskr", "AssetId"),
            (self._dependencies_for_tail_hit_sound, "tail_hit_sound", "int"),
            (self._dependencies_for_tail_destroyed_sound, "tail_destroyed_sound", "int"),
            (self._dependencies_for_bite_damage, "bite_damage", "DamageInfo"),
            (self._dependencies_for_electric_effect, "electric_effect", "AssetId"),
            (self._dependencies_for_beam_damage, "beam_damage", "DamageInfo"),
            (self._dependencies_for_audio_playback_parms_0xad47febe, "audio_playback_parms_0xad47febe", "AudioPlaybackParms"),
            (self._dependencies_for_burst_projectile, "burst_projectile", "AssetId"),
            (self._dependencies_for_burst_damage, "burst_damage", "DamageInfo"),
            (self._dependencies_for_surface_rings_effect, "surface_rings_effect", "AssetId"),
            (self._dependencies_for_part_0xbf4daae6, "part_0xbf4daae6", "AssetId"),
            (self._dependencies_for_part_always_ff, "part_always_ff", "AssetId"),
            (self._dependencies_for_part_0xffcee1a9, "part_0xffcee1a9", "AssetId"),
            (self._dependencies_for_grapple_swoosh, "grapple_swoosh", "AssetId"),
            (self._dependencies_for_grapple_beam_part, "grapple_beam_part", "AssetId"),
            (self._dependencies_for_grapple_hit_fx, "grapple_hit_fx", "AssetId"),
            (self._dependencies_for_grapple_damage, "grapple_damage", "DamageInfo"),
            (self._dependencies_for_audio_playback_parms_0xb6b9074b, "audio_playback_parms_0xb6b9074b", "AudioPlaybackParms"),
            (self._dependencies_for_beam_effect, "beam_effect", "AssetId"),
            (self._dependencies_for_grapple_visor_effect, "grapple_visor_effect", "AssetId"),
            (self._dependencies_for_damage_info, "damage_info", "DamageInfo"),
            (self._dependencies_for_part_0x54b6bfa1, "part_0x54b6bfa1", "AssetId"),
            (self._dependencies_for_audio_playback_parms_0x5cf705f2, "audio_playback_parms_0x5cf705f2", "AudioPlaybackParms"),
            (self._dependencies_for_part_0xb9f9f4f2, "part_0xb9f9f4f2", "AssetId"),
            (self._dependencies_for_alternate_scannable_info, "alternate_scannable_info", "AssetId"),
            (self._dependencies_for_ing_possession_data, "ing_possession_data", "IngPossessionData"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Grenchler.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'leash_radius': 100.0, 'collision_radius': 1.600000023841858, 'collision_height': 2.5, 'step_up_height': 1.0, 'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_unknown_0x04d51e3a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_is_grapple_guardian(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_has_health_bar(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_damage_vulnerability(data: typing.BinaryIO, property_size: int):
    return DamageVulnerability.from_stream(data, property_size)


def _decode_tail(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0x0abef809(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_tailless_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_tailless_skin_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0x9b193ae8(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_unknown_0xc24cf580(data: typing.BinaryIO, property_size: int):
    return AnimationParameters.from_stream(data, property_size)


def _decode_cmdl(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_cskr(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_tail_hit_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_tail_destroyed_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x5d8f2bee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x7bd1a35f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xea4b88c8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xaa04f0be(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x98d5d373(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd89aab05(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2e6096ee(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6e2fee98(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x49632b31(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_bite_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_unknown_0x262b2508(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x66645d7e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x909e6095(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd0d118e3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_electric_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_beam_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_unknown_0x680ce795(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_audio_playback_parms_0xad47febe(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_unknown_0x06f7ceed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x46b8b69b(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb0428b70(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf00df306(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xb00775e6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_burst_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_burst_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_surface_rings_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0xbf4daae6(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_always_ff(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part_0xffcee1a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grapple_swoosh(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grapple_beam_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grapple_hit_fx(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_grapple_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_audio_playback_parms_0xb6b9074b(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_beam_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0xd4753ff4(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x05fc6001(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x13e5b580(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xfc6f199d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grapple_visor_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_damage_info(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_part_0x54b6bfa1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_audio_playback_parms_0x5cf705f2(data: typing.BinaryIO, property_size: int):
    return AudioPlaybackParms.from_stream(data, property_size)


def _decode_part_0xb9f9f4f2(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_alternate_scannable_info(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x4d51e3a: ('unknown_0x04d51e3a', _decode_unknown_0x04d51e3a),
    0x33408e7f: ('is_grapple_guardian', _decode_is_grapple_guardian),
    0x67b6ea0b: ('has_health_bar', _decode_has_health_bar),
    0xa7326a3: ('damage_vulnerability', _decode_damage_vulnerability),
    0xa18f626b: ('tail', _decode_tail),
    0xabef809: ('unknown_0x0abef809', _decode_unknown_0x0abef809),
    0x4f3a4566: ('tailless_model', _decode_tailless_model),
    0x401bc111: ('tailless_skin_rules', _decode_tailless_skin_rules),
    0x9b193ae8: ('unknown_0x9b193ae8', _decode_unknown_0x9b193ae8),
    0xc24cf580: ('unknown_0xc24cf580', _decode_unknown_0xc24cf580),
    0x72258fe7: ('cmdl', _decode_cmdl),
    0xe5fba24c: ('cskr', _decode_cskr),
    0x55c51213: ('tail_hit_sound', _decode_tail_hit_sound),
    0x385e4738: ('tail_destroyed_sound', _decode_tail_destroyed_sound),
    0x5d8f2bee: ('unknown_0x5d8f2bee', _decode_unknown_0x5d8f2bee),
    0x7bd1a35f: ('unknown_0x7bd1a35f', _decode_unknown_0x7bd1a35f),
    0xea4b88c8: ('unknown_0xea4b88c8', _decode_unknown_0xea4b88c8),
    0xaa04f0be: ('unknown_0xaa04f0be', _decode_unknown_0xaa04f0be),
    0x98d5d373: ('unknown_0x98d5d373', _decode_unknown_0x98d5d373),
    0xd89aab05: ('unknown_0xd89aab05', _decode_unknown_0xd89aab05),
    0x2e6096ee: ('unknown_0x2e6096ee', _decode_unknown_0x2e6096ee),
    0x6e2fee98: ('unknown_0x6e2fee98', _decode_unknown_0x6e2fee98),
    0x49632b31: ('unknown_0x49632b31', _decode_unknown_0x49632b31),
    0xdf636c4b: ('bite_damage', _decode_bite_damage),
    0x262b2508: ('unknown_0x262b2508', _decode_unknown_0x262b2508),
    0x66645d7e: ('unknown_0x66645d7e', _decode_unknown_0x66645d7e),
    0x909e6095: ('unknown_0x909e6095', _decode_unknown_0x909e6095),
    0xd0d118e3: ('unknown_0xd0d118e3', _decode_unknown_0xd0d118e3),
    0x49fae143: ('electric_effect', _decode_electric_effect),
    0x13e30e4d: ('beam_damage', _decode_beam_damage),
    0x680ce795: ('unknown_0x680ce795', _decode_unknown_0x680ce795),
    0xad47febe: ('audio_playback_parms_0xad47febe', _decode_audio_playback_parms_0xad47febe),
    0x6f7ceed: ('unknown_0x06f7ceed', _decode_unknown_0x06f7ceed),
    0x46b8b69b: ('unknown_0x46b8b69b', _decode_unknown_0x46b8b69b),
    0xb0428b70: ('unknown_0xb0428b70', _decode_unknown_0xb0428b70),
    0xf00df306: ('unknown_0xf00df306', _decode_unknown_0xf00df306),
    0xb00775e6: ('unknown_0xb00775e6', _decode_unknown_0xb00775e6),
    0x7ef9aa67: ('burst_projectile', _decode_burst_projectile),
    0x5285db00: ('burst_damage', _decode_burst_damage),
    0x30b81a7e: ('surface_rings_effect', _decode_surface_rings_effect),
    0xbf4daae6: ('part_0xbf4daae6', _decode_part_0xbf4daae6),
    0x70247a6e: ('part_always_ff', _decode_part_always_ff),
    0xffcee1a9: ('part_0xffcee1a9', _decode_part_0xffcee1a9),
    0xae1f2a26: ('grapple_swoosh', _decode_grapple_swoosh),
    0xdabf0af: ('grapple_beam_part', _decode_grapple_beam_part),
    0xe51746d1: ('grapple_hit_fx', _decode_grapple_hit_fx),
    0x2ce7520f: ('grapple_damage', _decode_grapple_damage),
    0xb6b9074b: ('audio_playback_parms_0xb6b9074b', _decode_audio_playback_parms_0xb6b9074b),
    0x5439a08: ('beam_effect', _decode_beam_effect),
    0xd4753ff4: ('unknown_0xd4753ff4', _decode_unknown_0xd4753ff4),
    0x5fc6001: ('unknown_0x05fc6001', _decode_unknown_0x05fc6001),
    0x13e5b580: ('unknown_0x13e5b580', _decode_unknown_0x13e5b580),
    0xfc6f199d: ('unknown_0xfc6f199d', _decode_unknown_0xfc6f199d),
    0xf6502596: ('grapple_visor_effect', _decode_grapple_visor_effect),
    0x6ec26414: ('damage_info', _decode_damage_info),
    0x54b6bfa1: ('part_0x54b6bfa1', _decode_part_0x54b6bfa1),
    0x5cf705f2: ('audio_playback_parms_0x5cf705f2', _decode_audio_playback_parms_0x5cf705f2),
    0xb9f9f4f2: ('part_0xb9f9f4f2', _decode_part_0xb9f9f4f2),
    0xf60ac5cc: ('alternate_scannable_info', _decode_alternate_scannable_info),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
}
