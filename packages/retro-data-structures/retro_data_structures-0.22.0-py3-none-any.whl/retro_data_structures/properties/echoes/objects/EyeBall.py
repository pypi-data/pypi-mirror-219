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
from retro_data_structures.properties.echoes.core.Color import Color


@dataclasses.dataclass()
class EyeBall(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    patterned: PatternedAITypedef = dataclasses.field(default_factory=PatternedAITypedef)
    actor_information: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    close_time: float = dataclasses.field(default=3.0)
    fire_wait_time: float = dataclasses.field(default=3.0)
    projectile: AssetId = dataclasses.field(metadata={'asset_types': ['WPSC']}, default=default_asset_id)
    ray_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo)
    plasma_burn: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    plasma_pulse: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    plasma_texture: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    plasma_glow: AssetId = dataclasses.field(metadata={'asset_types': ['TXTR']}, default=default_asset_id)
    laser_inner_color: Color = dataclasses.field(default_factory=lambda: Color(r=1.0, g=1.0, b=1.0, a=0.0))
    laser_outer_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.0, g=1.0, b=0.0, a=0.0))
    unknown_0x81d14be8: int = dataclasses.field(default=0)
    unknown_0x6e1320d6: int = dataclasses.field(default=0)
    unknown_0x85249bd5: int = dataclasses.field(default=0)
    unknown_0x6ae6f0eb: int = dataclasses.field(default=0)
    laser_sound: int = dataclasses.field(default=0, metadata={'sound': True})
    should_be_triggered: bool = dataclasses.field(default=False)
    max_audible_distance: float = dataclasses.field(default=50.0)
    drop_off: float = dataclasses.field(default=0.20000000298023224)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'EYEB'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['EyeBall.rel']

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
        data.write(b'\x00\x15')  # 21 properties

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
        self.patterned.to_stream(data)
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

        data.write(b'\xd0\xd8\x8e\xa6')  # 0xd0d88ea6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.close_time))

        data.write(b'\xc0\x0c\xf8!')  # 0xc00cf821
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fire_wait_time))

        data.write(b'\xefH]\xb9')  # 0xef485db9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.projectile))

        data.write(b'"\xa9\xf2\xd2')  # 0x22a9f2d2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.ray_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xbc\x19T\x9c')  # 0xbc19549c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.plasma_burn))

        data.write(b'(\xcd\x86\xfa')  # 0x28cd86fa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.plasma_pulse))

        data.write(b'\xd7\xa1\x12\x1d')  # 0xd7a1121d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.plasma_texture))

        data.write(b'\xb7\xaa\x95\x8e')  # 0xb7aa958e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.plasma_glow))

        data.write(b'd>PR')  # 0x643e5052
        data.write(b'\x00\x10')  # size
        self.laser_inner_color.to_stream(data)

        data.write(b'\xe1\x16C\xdd')  # 0xe11643dd
        data.write(b'\x00\x10')  # size
        self.laser_outer_color.to_stream(data)

        data.write(b'\x81\xd1K\xe8')  # 0x81d14be8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x81d14be8))

        data.write(b'n\x13 \xd6')  # 0x6e1320d6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6e1320d6))

        data.write(b'\x85$\x9b\xd5')  # 0x85249bd5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x85249bd5))

        data.write(b'j\xe6\xf0\xeb')  # 0x6ae6f0eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x6ae6f0eb))

        data.write(b'\xe4x\x02\x19')  # 0xe4780219
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.laser_sound))

        data.write(b'.`=\xed')  # 0x2e603ded
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.should_be_triggered))

        data.write(b'!NH\xa0')  # 0x214e48a0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_audible_distance))

        data.write(b'\x08\xbf.T')  # 0x8bf2e54
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drop_off))

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
            close_time=data['close_time'],
            fire_wait_time=data['fire_wait_time'],
            projectile=data['projectile'],
            ray_damage=DamageInfo.from_json(data['ray_damage']),
            plasma_burn=data['plasma_burn'],
            plasma_pulse=data['plasma_pulse'],
            plasma_texture=data['plasma_texture'],
            plasma_glow=data['plasma_glow'],
            laser_inner_color=Color.from_json(data['laser_inner_color']),
            laser_outer_color=Color.from_json(data['laser_outer_color']),
            unknown_0x81d14be8=data['unknown_0x81d14be8'],
            unknown_0x6e1320d6=data['unknown_0x6e1320d6'],
            unknown_0x85249bd5=data['unknown_0x85249bd5'],
            unknown_0x6ae6f0eb=data['unknown_0x6ae6f0eb'],
            laser_sound=data['laser_sound'],
            should_be_triggered=data['should_be_triggered'],
            max_audible_distance=data['max_audible_distance'],
            drop_off=data['drop_off'],
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'patterned': self.patterned.to_json(),
            'actor_information': self.actor_information.to_json(),
            'close_time': self.close_time,
            'fire_wait_time': self.fire_wait_time,
            'projectile': self.projectile,
            'ray_damage': self.ray_damage.to_json(),
            'plasma_burn': self.plasma_burn,
            'plasma_pulse': self.plasma_pulse,
            'plasma_texture': self.plasma_texture,
            'plasma_glow': self.plasma_glow,
            'laser_inner_color': self.laser_inner_color.to_json(),
            'laser_outer_color': self.laser_outer_color.to_json(),
            'unknown_0x81d14be8': self.unknown_0x81d14be8,
            'unknown_0x6e1320d6': self.unknown_0x6e1320d6,
            'unknown_0x85249bd5': self.unknown_0x85249bd5,
            'unknown_0x6ae6f0eb': self.unknown_0x6ae6f0eb,
            'laser_sound': self.laser_sound,
            'should_be_triggered': self.should_be_triggered,
            'max_audible_distance': self.max_audible_distance,
            'drop_off': self.drop_off,
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_patterned(self, asset_manager):
        yield from self.patterned.dependencies_for(asset_manager)

    def _dependencies_for_actor_information(self, asset_manager):
        yield from self.actor_information.dependencies_for(asset_manager)

    def _dependencies_for_projectile(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.projectile)

    def _dependencies_for_ray_damage(self, asset_manager):
        yield from self.ray_damage.dependencies_for(asset_manager)

    def _dependencies_for_plasma_burn(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.plasma_burn)

    def _dependencies_for_plasma_pulse(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.plasma_pulse)

    def _dependencies_for_plasma_texture(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.plasma_texture)

    def _dependencies_for_plasma_glow(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.plasma_glow)

    def _dependencies_for_laser_sound(self, asset_manager):
        yield from asset_manager.get_audio_group_dependency(self.laser_sound)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_patterned, "patterned", "PatternedAITypedef"),
            (self._dependencies_for_actor_information, "actor_information", "ActorParameters"),
            (self._dependencies_for_projectile, "projectile", "AssetId"),
            (self._dependencies_for_ray_damage, "ray_damage", "DamageInfo"),
            (self._dependencies_for_plasma_burn, "plasma_burn", "AssetId"),
            (self._dependencies_for_plasma_pulse, "plasma_pulse", "AssetId"),
            (self._dependencies_for_plasma_texture, "plasma_texture", "AssetId"),
            (self._dependencies_for_plasma_glow, "plasma_glow", "AssetId"),
            (self._dependencies_for_laser_sound, "laser_sound", "int"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for EyeBall.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_patterned(data: typing.BinaryIO, property_size: int):
    return PatternedAITypedef.from_stream(data, property_size)


def _decode_actor_information(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_close_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fire_wait_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectile(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_ray_damage(data: typing.BinaryIO, property_size: int):
    return DamageInfo.from_stream(data, property_size)


def _decode_plasma_burn(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_plasma_pulse(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_plasma_texture(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_plasma_glow(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_laser_inner_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_laser_outer_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_unknown_0x81d14be8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6e1320d6(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x85249bd5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x6ae6f0eb(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_laser_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_should_be_triggered(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_max_audible_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop_off(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xb3774750: ('patterned', _decode_patterned),
    0x7e397fed: ('actor_information', _decode_actor_information),
    0xd0d88ea6: ('close_time', _decode_close_time),
    0xc00cf821: ('fire_wait_time', _decode_fire_wait_time),
    0xef485db9: ('projectile', _decode_projectile),
    0x22a9f2d2: ('ray_damage', _decode_ray_damage),
    0xbc19549c: ('plasma_burn', _decode_plasma_burn),
    0x28cd86fa: ('plasma_pulse', _decode_plasma_pulse),
    0xd7a1121d: ('plasma_texture', _decode_plasma_texture),
    0xb7aa958e: ('plasma_glow', _decode_plasma_glow),
    0x643e5052: ('laser_inner_color', _decode_laser_inner_color),
    0xe11643dd: ('laser_outer_color', _decode_laser_outer_color),
    0x81d14be8: ('unknown_0x81d14be8', _decode_unknown_0x81d14be8),
    0x6e1320d6: ('unknown_0x6e1320d6', _decode_unknown_0x6e1320d6),
    0x85249bd5: ('unknown_0x85249bd5', _decode_unknown_0x85249bd5),
    0x6ae6f0eb: ('unknown_0x6ae6f0eb', _decode_unknown_0x6ae6f0eb),
    0xe4780219: ('laser_sound', _decode_laser_sound),
    0x2e603ded: ('should_be_triggered', _decode_should_be_triggered),
    0x214e48a0: ('max_audible_distance', _decode_max_audible_distance),
    0x8bf2e54: ('drop_off', _decode_drop_off),
}
