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
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class DarkTrooper(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    ing_possession_data: IngPossessionData = dataclasses.field(default_factory=IngPossessionData)
    flotsam: bool = dataclasses.field(default=False)
    avoid_down_frames: bool = dataclasses.field(default=False)
    melee_attack_min_range: float = dataclasses.field(default=0.0)
    melee_attack_max_range: float = dataclasses.field(default=5.0)
    melee_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown: float = dataclasses.field(default=1.0)
    ranged_attack_min_range: float = dataclasses.field(default=5.0)
    ranged_attack_max_range: float = dataclasses.field(default=18.0)
    ranged_attack_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    ranged_attack_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    ragdoll_impact_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    fires_missiles: bool = dataclasses.field(default=False)
    missile_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    missile_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    scannable_info_when_attacking: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'DKTR'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['PirateRagDoll.rel', 'DarkTrooper.rel']

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
        data.write(b'\x00\x13')  # 19 properties

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
        self.patterned.to_stream(data, default_override={'leash_radius': 100.0, 'collision_radius': 0.5, 'collision_height': 1.600000023841858, 'step_up_height': 1.0, 'creature_size': 1})
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

        data.write(b'\xc1\xd1\xe4e')  # 0xc1d1e465
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.flotsam))

        data.write(b"\xeb\xaf\xeb'")  # 0xebafeb27
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.avoid_down_frames))

        data.write(b'\xbe\xad\xf2\xe0')  # 0xbeadf2e0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_attack_min_range))

        data.write(b'\xfe\xe2\x8a\x96')  # 0xfee28a96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.melee_attack_max_range))

        data.write(b'My\x0e\xe9')  # 0x4d790ee9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.melee_attack_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'-\xca\x19\x9d')  # 0x2dca199d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown))

        data.write(b'Q":\x03')  # 0x51223a03
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ranged_attack_min_range))

        data.write(b'\x11mBu')  # 0x116d4275
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ranged_attack_max_range))

        data.write(b'\x98\xf9\xa3\x08')  # 0x98f9a308
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ranged_attack_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb8C(\x96')  # 0xb8432896
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.ranged_attack_projectile))

        data.write(b'IrwS')  # 0x49727753
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.ragdoll_impact_sound))

        data.write(b'\xc9\xfbj\x85')  # 0xc9fb6a85
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.fires_missiles))

        data.write(b'p\xe9qf')  # 0x70e97166
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.missile_projectile))

        data.write(b'%\x8c\xfbM')  # 0x258cfb4d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.missile_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8bo\x9bC')  # 0x8b6f9b43
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scannable_info_when_attacking))

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
            flotsam=data['flotsam'],
            avoid_down_frames=data['avoid_down_frames'],
            melee_attack_min_range=data['melee_attack_min_range'],
            melee_attack_max_range=data['melee_attack_max_range'],
            melee_attack_damage=DamageInfo.from_json(data['melee_attack_damage']),
            unknown=data['unknown'],
            ranged_attack_min_range=data['ranged_attack_min_range'],
            ranged_attack_max_range=data['ranged_attack_max_range'],
            ranged_attack_damage=DamageInfo.from_json(data['ranged_attack_damage']),
            ranged_attack_projectile=data['ranged_attack_projectile'],
            ragdoll_impact_sound=data['ragdoll_impact_sound'],
            fires_missiles=data['fires_missiles'],
            missile_projectile=data['missile_projectile'],
            missile_damage=DamageInfo.from_json(data['missile_damage']),
            scannable_info_when_attacking=data['scannable_info_when_attacking'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'ing_possession_data': self.ing_possession_data.to_json(),
            'flotsam': self.flotsam,
            'avoid_down_frames': self.avoid_down_frames,
            'melee_attack_min_range': self.melee_attack_min_range,
            'melee_attack_max_range': self.melee_attack_max_range,
            'melee_attack_damage': self.melee_attack_damage.to_json(),
            'unknown': self.unknown,
            'ranged_attack_min_range': self.ranged_attack_min_range,
            'ranged_attack_max_range': self.ranged_attack_max_range,
            'ranged_attack_damage': self.ranged_attack_damage.to_json(),
            'ranged_attack_projectile': self.ranged_attack_projectile,
            'ragdoll_impact_sound': self.ragdoll_impact_sound,
            'fires_missiles': self.fires_missiles,
            'missile_projectile': self.missile_projectile,
            'missile_damage': self.missile_damage.to_json(),
            'scannable_info_when_attacking': self.scannable_info_when_attacking,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_ing_possession_data(self, asset_manager):
        yield from self.ing_possession_data.dependencies_for(asset_manager)

    def _dependencies_for_melee_attack_damage(self, asset_manager):
        yield from self.melee_attack_damage.dependencies_for(asset_manager)

    def _dependencies_for_ranged_attack_damage(self, asset_manager):
        yield from self.ranged_attack_damage.dependencies_for(asset_manager)

    def _dependencies_for_ranged_attack_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.ranged_attack_projectile)

    def _dependencies_for_ragdoll_impact_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.ragdoll_impact_sound)

    def _dependencies_for_missile_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.missile_projectile)

    def _dependencies_for_missile_damage(self, asset_manager):
        yield from self.missile_damage.dependencies_for(asset_manager)

    def _dependencies_for_scannable_info_when_attacking(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scannable_info_when_attacking)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_ing_possession_data, "ing_possession_data", "IngPossessionData"),
            (self._dependencies_for_melee_attack_damage, "melee_attack_damage", "DamageInfo"),
            (self._dependencies_for_ranged_attack_damage, "ranged_attack_damage", "DamageInfo"),
            (self._dependencies_for_ranged_attack_projectile, "ranged_attack_projectile", "AssetId"),
            (self._dependencies_for_ragdoll_impact_sound, "ragdoll_impact_sound", "int"),
            (self._dependencies_for_missile_projectile, "missile_projectile", "AssetId"),
            (self._dependencies_for_missile_damage, "missile_damage", "DamageInfo"),
            (self._dependencies_for_scannable_info_when_attacking, "scannable_info_when_attacking", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for DarkTrooper.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'leash_radius': 100.0, 'collision_radius': 0.5, 'collision_height': 1.600000023841858, 'step_up_height': 1.0, 'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_ing_possession_data(data: typing.BinaryIO, property_size: int):
    return IngPossessionData.from_stream(data, property_size)


def _decode_flotsam(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_avoid_down_frames(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_melee_attack_min_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_attack_max_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_melee_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ranged_attack_min_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ranged_attack_max_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ranged_attack_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_ranged_attack_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ragdoll_impact_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_fires_missiles(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_missile_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_missile_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_scannable_info_when_attacking(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xe61748ed: ('ing_possession_data', _decode_ing_possession_data),
    0xc1d1e465: ('flotsam', _decode_flotsam),
    0xebafeb27: ('avoid_down_frames', _decode_avoid_down_frames),
    0xbeadf2e0: ('melee_attack_min_range', _decode_melee_attack_min_range),
    0xfee28a96: ('melee_attack_max_range', _decode_melee_attack_max_range),
    0x4d790ee9: ('melee_attack_damage', _decode_melee_attack_damage),
    0x2dca199d: ('unknown', _decode_unknown),
    0x51223a03: ('ranged_attack_min_range', _decode_ranged_attack_min_range),
    0x116d4275: ('ranged_attack_max_range', _decode_ranged_attack_max_range),
    0x98f9a308: ('ranged_attack_damage', _decode_ranged_attack_damage),
    0xb8432896: ('ranged_attack_projectile', _decode_ranged_attack_projectile),
    0x49727753: ('ragdoll_impact_sound', _decode_ragdoll_impact_sound),
    0xc9fb6a85: ('fires_missiles', _decode_fires_missiles),
    0x70e97166: ('missile_projectile', _decode_missile_projectile),
    0x258cfb4d: ('missile_damage', _decode_missile_damage),
    0x8b6f9b43: ('scannable_info_when_attacking', _decode_scannable_info_when_attacking),
}
