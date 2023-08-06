# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.DamageInfo import DamageInfo
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.archetypes.PatternedAITypedef import PatternedAITypedef
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id


@dataclasses.dataclass()
class Lumite(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    unknown_0x2d9ebd7f: float = dataclasses.field(default=8.0)
    unknown_0x6dd1c509: float = dataclasses.field(default=30.0)
    small_shot_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    small_shot_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    unknown_0x6d5356bb: float = dataclasses.field(default=8.0)
    unknown_0x2d1c2ecd: float = dataclasses.field(default=30.0)
    big_shot_projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    big_shot_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    trail_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    sunlight_enter_exit_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    unknown_0xe05d93ef: float = dataclasses.field(default=5.0)
    unknown_0x47691396: float = dataclasses.field(default=45.0)
    phase_in_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    phase_out_sound: int = dataclasses.field(default=0, metadata={'sound': True})

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'LUMI'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['Lumite.rel']

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
        data.write(b'\x00\x11')  # 17 properties

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
        self.patterned.to_stream(data, default_override={'leash_radius': 100.0, 'collision_radius': 0.10000000149011612, 'collision_height': 0.10000000149011612, 'step_up_height': 1.0, 'creature_size': 1})
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

        data.write(b'-\x9e\xbd\x7f')  # 0x2d9ebd7f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2d9ebd7f))

        data.write(b'm\xd1\xc5\t')  # 0x6dd1c509
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6dd1c509))

        data.write(b'H\x15tS')  # 0x48157453
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.small_shot_projectile))

        data.write(b's\x07\xc3k')  # 0x7307c36b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.small_shot_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'mSV\xbb')  # 0x6d5356bb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x6d5356bb))

        data.write(b'-\x1c.\xcd')  # 0x2d1c2ecd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x2d1c2ecd))

        data.write(b'\xd0[\x1d$')  # 0xd05b1d24
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.big_shot_projectile))

        data.write(b'\xbd\xfei\x9d')  # 0xbdfe699d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.big_shot_damage.to_stream(data, default_override={'di_weapon_type': 11, 'di_damage': 5.0})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'6\xee\xe7\x91')  # 0x36eee791
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.trail_effect))

        data.write(b'\xd2\x87\x9e\xbb')  # 0xd2879ebb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.sunlight_enter_exit_effect))

        data.write(b'\xe0]\x93\xef')  # 0xe05d93ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe05d93ef))

        data.write(b'Gi\x13\x96')  # 0x47691396
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x47691396))

        data.write(b'\xa4#\x13#')  # 0xa4231323
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.phase_in_sound))

        data.write(b':\xafxq')  # 0x3aaf7871
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.phase_out_sound))

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
            unknown_0x2d9ebd7f=data['unknown_0x2d9ebd7f'],
            unknown_0x6dd1c509=data['unknown_0x6dd1c509'],
            small_shot_projectile=data['small_shot_projectile'],
            small_shot_damage=DamageInfo.from_json(data['small_shot_damage']),
            unknown_0x6d5356bb=data['unknown_0x6d5356bb'],
            unknown_0x2d1c2ecd=data['unknown_0x2d1c2ecd'],
            big_shot_projectile=data['big_shot_projectile'],
            big_shot_damage=DamageInfo.from_json(data['big_shot_damage']),
            trail_effect=data['trail_effect'],
            sunlight_enter_exit_effect=data['sunlight_enter_exit_effect'],
            unknown_0xe05d93ef=data['unknown_0xe05d93ef'],
            unknown_0x47691396=data['unknown_0x47691396'],
            phase_in_sound=data['phase_in_sound'],
            phase_out_sound=data['phase_out_sound'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'unknown_0x2d9ebd7f': self.unknown_0x2d9ebd7f,
            'unknown_0x6dd1c509': self.unknown_0x6dd1c509,
            'small_shot_projectile': self.small_shot_projectile,
            'small_shot_damage': self.small_shot_damage.to_json(),
            'unknown_0x6d5356bb': self.unknown_0x6d5356bb,
            'unknown_0x2d1c2ecd': self.unknown_0x2d1c2ecd,
            'big_shot_projectile': self.big_shot_projectile,
            'big_shot_damage': self.big_shot_damage.to_json(),
            'trail_effect': self.trail_effect,
            'sunlight_enter_exit_effect': self.sunlight_enter_exit_effect,
            'unknown_0xe05d93ef': self.unknown_0xe05d93ef,
            'unknown_0x47691396': self.unknown_0x47691396,
            'phase_in_sound': self.phase_in_sound,
            'phase_out_sound': self.phase_out_sound,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_small_shot_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.small_shot_projectile)

    def _dependencies_for_small_shot_damage(self, asset_manager):
        yield from self.small_shot_damage.dependencies_for(asset_manager)

    def _dependencies_for_big_shot_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.big_shot_projectile)

    def _dependencies_for_big_shot_damage(self, asset_manager):
        yield from self.big_shot_damage.dependencies_for(asset_manager)

    def _dependencies_for_trail_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.trail_effect)

    def _dependencies_for_sunlight_enter_exit_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.sunlight_enter_exit_effect)

    def _dependencies_for_phase_in_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.phase_in_sound)

    def _dependencies_for_phase_out_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.phase_out_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_small_shot_projectile, "small_shot_projectile", "AssetId"),
            (self._dependencies_for_small_shot_damage, "small_shot_damage", "DamageInfo"),
            (self._dependencies_for_big_shot_projectile, "big_shot_projectile", "AssetId"),
            (self._dependencies_for_big_shot_damage, "big_shot_damage", "DamageInfo"),
            (self._dependencies_for_trail_effect, "trail_effect", "AssetId"),
            (self._dependencies_for_sunlight_enter_exit_effect, "sunlight_enter_exit_effect", "AssetId"),
            (self._dependencies_for_phase_in_sound, "phase_in_sound", "int"),
            (self._dependencies_for_phase_out_sound, "phase_out_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for Lumite.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size, default_override={'leash_radius': 100.0, 'collision_radius': 0.10000000149011612, 'collision_height': 0.10000000149011612, 'step_up_height': 1.0, 'creature_size': 1})


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_unknown_0x2d9ebd7f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x6dd1c509(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_small_shot_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_small_shot_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_unknown_0x6d5356bb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x2d1c2ecd(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_big_shot_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_big_shot_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size, default_override={'di_weapon_type': 11, 'di_damage': 5.0})


def _decode_trail_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_sunlight_enter_exit_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_unknown_0xe05d93ef(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x47691396(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_phase_in_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_phase_out_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0x2d9ebd7f: ('unknown_0x2d9ebd7f', _decode_unknown_0x2d9ebd7f),
    0x6dd1c509: ('unknown_0x6dd1c509', _decode_unknown_0x6dd1c509),
    0x48157453: ('small_shot_projectile', _decode_small_shot_projectile),
    0x7307c36b: ('small_shot_damage', _decode_small_shot_damage),
    0x6d5356bb: ('unknown_0x6d5356bb', _decode_unknown_0x6d5356bb),
    0x2d1c2ecd: ('unknown_0x2d1c2ecd', _decode_unknown_0x2d1c2ecd),
    0xd05b1d24: ('big_shot_projectile', _decode_big_shot_projectile),
    0xbdfe699d: ('big_shot_damage', _decode_big_shot_damage),
    0x36eee791: ('trail_effect', _decode_trail_effect),
    0xd2879ebb: ('sunlight_enter_exit_effect', _decode_sunlight_enter_exit_effect),
    0xe05d93ef: ('unknown_0xe05d93ef', _decode_unknown_0xe05d93ef),
    0x47691396: ('unknown_0x47691396', _decode_unknown_0x47691396),
    0xa4231323: ('phase_in_sound', _decode_phase_in_sound),
    0x3aaf7871: ('phase_out_sound', _decode_phase_out_sound),
}
