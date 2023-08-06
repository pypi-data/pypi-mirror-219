# Generated File
import dataclasses
import struct
import typing

from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.echoes.archetypes.ActorParameters import ActorParameters
from retro_data_structures.properties.echoes.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.echoes.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.echoes.core.Spline import Spline
from retro_data_structures.properties.echoes.core.Vector import Vector


@dataclasses.dataclass()
class SafeZoneCrystal(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties)
    actor_parameters: ActorParameters = dataclasses.field(default_factory=ActorParameters)
    scannable_info_collapsed: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    scannable_info_entangled: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    scannable_info_light: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    scannable_info_annihilator: AssetId = dataclasses.field(metadata={'asset_types': ['SCAN']}, default=default_asset_id)
    safezone_type: int = dataclasses.field(default=0)
    initially_entangled: bool = dataclasses.field(default=False)
    collapsed_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    expanded_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    entangled_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    part: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    echo_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    normal_crystal: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    entangled_crystal: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    energized_model: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    echo_crystal: AssetId = dataclasses.field(metadata={'asset_types': ['CMDL']}, default=default_asset_id)
    max_time_expanded: float = dataclasses.field(default=5.0)
    max_time_entangled: float = dataclasses.field(default=5.0)
    unknown_0xf0a45c32: float = dataclasses.field(default=5.0)
    unknown_0xd8116003: float = dataclasses.field(default=5.0)
    unknown_0x415046ed: float = dataclasses.field(default=3.0)
    unknown_0xec9c01b2: float = dataclasses.field(default=1.0)
    unknown_0x545540e5: float = dataclasses.field(default=5.0)
    power_beam_refresh_effect: AssetId = dataclasses.field(metadata={'asset_types': ['PART']}, default=default_asset_id)
    hit_radius: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0))
    hit_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    effect_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0))
    unknown_0xbbbee60b: Spline = dataclasses.field(default_factory=Spline)

    @classmethod
    def game(cls) -> Game:
        return Game.ECHOES

    def get_name(self) -> typing.Optional[str]:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'SFZC'

    @classmethod
    def modules(cls) -> typing.List[str]:
        return ['ScriptSafeZone.rel']

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
        data.write(b'\x00\x1d')  # 29 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd2\x9c\x03\x1d')  # 0xd29c031d
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.actor_parameters.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\x8b3#')  # 0x9b8b3323
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scannable_info_collapsed))

        data.write(b'\xe3n \xa7')  # 0xe36e20a7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scannable_info_entangled))

        data.write(b'\xacyM\xa8')  # 0xac794da8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scannable_info_light))

        data.write(b'\xc2\x1f&O')  # 0xc21f264f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.scannable_info_annihilator))

        data.write(b'\x11\x15\xfbh')  # 0x1115fb68
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.safezone_type))

        data.write(b'\xa0\xd9\xe8\x7f')  # 0xa0d9e87f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.initially_entangled))

        data.write(b'B\xa0F\xc2')  # 0x42a046c2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.collapsed_effect))

        data.write(b'[\x91\xff8')  # 0x5b91ff38
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.expanded_effect))

        data.write(b'[\x82u\xbc')  # 0x5b8275bc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.entangled_effect))

        data.write(b'\xad\xac\xec\x90')  # 0xadacec90
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.part))

        data.write(b'\r.J\xd3')  # 0xd2e4ad3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.echo_effect))

        data.write(b'q\xef\xff\xc4')  # 0x71efffc4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.normal_crystal))

        data.write(b'\xc3\xdd\x9bu')  # 0xc3dd9b75
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.entangled_crystal))

        data.write(b'\xf1\xf3\xd9\x0f')  # 0xf1f3d90f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.energized_model))

        data.write(b'\x1e\x86K\x83')  # 0x1e864b83
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.echo_crystal))

        data.write(b'\xbd0\xf7\xa3')  # 0xbd30f7a3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_time_expanded))

        data.write(b'\xa7\xbd\xc4\xf8')  # 0xa7bdc4f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_time_entangled))

        data.write(b'\xf0\xa4\\2')  # 0xf0a45c32
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf0a45c32))

        data.write(b'\xd8\x11`\x03')  # 0xd8116003
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xd8116003))

        data.write(b'APF\xed')  # 0x415046ed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x415046ed))

        data.write(b'\xec\x9c\x01\xb2')  # 0xec9c01b2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xec9c01b2))

        data.write(b'TU@\xe5')  # 0x545540e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x545540e5))

        data.write(b'T\x90\xe2\x14')  # 0x5490e214
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.power_beam_refresh_effect))

        data.write(b'\x88~\x8a\x8b')  # 0x887e8a8b
        data.write(b'\x00\x0c')  # size
        self.hit_radius.to_stream(data)

        data.write(b'\xb7\xf5dm')  # 0xb7f5646d
        data.write(b'\x00\x0c')  # size
        self.hit_offset.to_stream(data)

        data.write(b'A\xb7+,')  # 0x41b72b2c
        data.write(b'\x00\x0c')  # size
        self.effect_offset.to_stream(data)

        data.write(b'\xbb\xbe\xe6\x0b')  # 0xbbbee60b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xbbbee60b.to_stream(data)
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
            actor_parameters=ActorParameters.from_json(data['actor_parameters']),
            scannable_info_collapsed=data['scannable_info_collapsed'],
            scannable_info_entangled=data['scannable_info_entangled'],
            scannable_info_light=data['scannable_info_light'],
            scannable_info_annihilator=data['scannable_info_annihilator'],
            safezone_type=data['safezone_type'],
            initially_entangled=data['initially_entangled'],
            collapsed_effect=data['collapsed_effect'],
            expanded_effect=data['expanded_effect'],
            entangled_effect=data['entangled_effect'],
            part=data['part'],
            echo_effect=data['echo_effect'],
            normal_crystal=data['normal_crystal'],
            entangled_crystal=data['entangled_crystal'],
            energized_model=data['energized_model'],
            echo_crystal=data['echo_crystal'],
            max_time_expanded=data['max_time_expanded'],
            max_time_entangled=data['max_time_entangled'],
            unknown_0xf0a45c32=data['unknown_0xf0a45c32'],
            unknown_0xd8116003=data['unknown_0xd8116003'],
            unknown_0x415046ed=data['unknown_0x415046ed'],
            unknown_0xec9c01b2=data['unknown_0xec9c01b2'],
            unknown_0x545540e5=data['unknown_0x545540e5'],
            power_beam_refresh_effect=data['power_beam_refresh_effect'],
            hit_radius=Vector.from_json(data['hit_radius']),
            hit_offset=Vector.from_json(data['hit_offset']),
            effect_offset=Vector.from_json(data['effect_offset']),
            unknown_0xbbbee60b=Spline.from_json(data['unknown_0xbbbee60b']),
        )

    def to_json(self) -> dict:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'actor_parameters': self.actor_parameters.to_json(),
            'scannable_info_collapsed': self.scannable_info_collapsed,
            'scannable_info_entangled': self.scannable_info_entangled,
            'scannable_info_light': self.scannable_info_light,
            'scannable_info_annihilator': self.scannable_info_annihilator,
            'safezone_type': self.safezone_type,
            'initially_entangled': self.initially_entangled,
            'collapsed_effect': self.collapsed_effect,
            'expanded_effect': self.expanded_effect,
            'entangled_effect': self.entangled_effect,
            'part': self.part,
            'echo_effect': self.echo_effect,
            'normal_crystal': self.normal_crystal,
            'entangled_crystal': self.entangled_crystal,
            'energized_model': self.energized_model,
            'echo_crystal': self.echo_crystal,
            'max_time_expanded': self.max_time_expanded,
            'max_time_entangled': self.max_time_entangled,
            'unknown_0xf0a45c32': self.unknown_0xf0a45c32,
            'unknown_0xd8116003': self.unknown_0xd8116003,
            'unknown_0x415046ed': self.unknown_0x415046ed,
            'unknown_0xec9c01b2': self.unknown_0xec9c01b2,
            'unknown_0x545540e5': self.unknown_0x545540e5,
            'power_beam_refresh_effect': self.power_beam_refresh_effect,
            'hit_radius': self.hit_radius.to_json(),
            'hit_offset': self.hit_offset.to_json(),
            'effect_offset': self.effect_offset.to_json(),
            'unknown_0xbbbee60b': self.unknown_0xbbbee60b.to_json(),
        }

    def _dependencies_for_editor_properties(self, asset_manager):
        yield from self.editor_properties.dependencies_for(asset_manager)

    def _dependencies_for_actor_parameters(self, asset_manager):
        yield from self.actor_parameters.dependencies_for(asset_manager)

    def _dependencies_for_scannable_info_collapsed(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scannable_info_collapsed)

    def _dependencies_for_scannable_info_entangled(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scannable_info_entangled)

    def _dependencies_for_scannable_info_light(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scannable_info_light)

    def _dependencies_for_scannable_info_annihilator(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.scannable_info_annihilator)

    def _dependencies_for_collapsed_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.collapsed_effect)

    def _dependencies_for_expanded_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.expanded_effect)

    def _dependencies_for_entangled_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.entangled_effect)

    def _dependencies_for_part(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.part)

    def _dependencies_for_echo_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.echo_effect)

    def _dependencies_for_normal_crystal(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.normal_crystal)

    def _dependencies_for_entangled_crystal(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.entangled_crystal)

    def _dependencies_for_energized_model(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.energized_model)

    def _dependencies_for_echo_crystal(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.echo_crystal)

    def _dependencies_for_power_beam_refresh_effect(self, asset_manager):
        yield from asset_manager.get_dependencies_for_asset(self.power_beam_refresh_effect)

    def dependencies_for(self, asset_manager):
        for method, field_name, field_type in [
            (self._dependencies_for_editor_properties, "editor_properties", "EditorProperties"),
            (self._dependencies_for_actor_parameters, "actor_parameters", "ActorParameters"),
            (self._dependencies_for_scannable_info_collapsed, "scannable_info_collapsed", "AssetId"),
            (self._dependencies_for_scannable_info_entangled, "scannable_info_entangled", "AssetId"),
            (self._dependencies_for_scannable_info_light, "scannable_info_light", "AssetId"),
            (self._dependencies_for_scannable_info_annihilator, "scannable_info_annihilator", "AssetId"),
            (self._dependencies_for_collapsed_effect, "collapsed_effect", "AssetId"),
            (self._dependencies_for_expanded_effect, "expanded_effect", "AssetId"),
            (self._dependencies_for_entangled_effect, "entangled_effect", "AssetId"),
            (self._dependencies_for_part, "part", "AssetId"),
            (self._dependencies_for_echo_effect, "echo_effect", "AssetId"),
            (self._dependencies_for_normal_crystal, "normal_crystal", "AssetId"),
            (self._dependencies_for_entangled_crystal, "entangled_crystal", "AssetId"),
            (self._dependencies_for_energized_model, "energized_model", "AssetId"),
            (self._dependencies_for_echo_crystal, "echo_crystal", "AssetId"),
            (self._dependencies_for_power_beam_refresh_effect, "power_beam_refresh_effect", "AssetId"),
        ]:
            try:
                yield from method(asset_manager)
            except Exception as e:
                raise Exception(
                    f"Error finding dependencies for SafeZoneCrystal.{field_name} ({field_type}): {e}"
                )


def _decode_editor_properties(data: typing.BinaryIO, property_size: int):
    return EditorProperties.from_stream(data, property_size)


def _decode_actor_parameters(data: typing.BinaryIO, property_size: int):
    return ActorParameters.from_stream(data, property_size)


def _decode_scannable_info_collapsed(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_scannable_info_entangled(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_scannable_info_light(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_scannable_info_annihilator(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_safezone_type(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_initially_entangled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_collapsed_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_expanded_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_entangled_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_part(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_echo_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_normal_crystal(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_entangled_crystal(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_energized_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_echo_crystal(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_max_time_expanded(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_time_entangled(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf0a45c32(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xd8116003(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x415046ed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xec9c01b2(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x545540e5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_power_beam_refresh_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


def _decode_hit_radius(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_hit_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_effect_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_unknown_0xbbbee60b(data: typing.BinaryIO, property_size: int):
    return Spline.from_stream(data, property_size)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', _decode_editor_properties),
    0xd29c031d: ('actor_parameters', _decode_actor_parameters),
    0x9b8b3323: ('scannable_info_collapsed', _decode_scannable_info_collapsed),
    0xe36e20a7: ('scannable_info_entangled', _decode_scannable_info_entangled),
    0xac794da8: ('scannable_info_light', _decode_scannable_info_light),
    0xc21f264f: ('scannable_info_annihilator', _decode_scannable_info_annihilator),
    0x1115fb68: ('safezone_type', _decode_safezone_type),
    0xa0d9e87f: ('initially_entangled', _decode_initially_entangled),
    0x42a046c2: ('collapsed_effect', _decode_collapsed_effect),
    0x5b91ff38: ('expanded_effect', _decode_expanded_effect),
    0x5b8275bc: ('entangled_effect', _decode_entangled_effect),
    0xadacec90: ('part', _decode_part),
    0xd2e4ad3: ('echo_effect', _decode_echo_effect),
    0x71efffc4: ('normal_crystal', _decode_normal_crystal),
    0xc3dd9b75: ('entangled_crystal', _decode_entangled_crystal),
    0xf1f3d90f: ('energized_model', _decode_energized_model),
    0x1e864b83: ('echo_crystal', _decode_echo_crystal),
    0xbd30f7a3: ('max_time_expanded', _decode_max_time_expanded),
    0xa7bdc4f8: ('max_time_entangled', _decode_max_time_entangled),
    0xf0a45c32: ('unknown_0xf0a45c32', _decode_unknown_0xf0a45c32),
    0xd8116003: ('unknown_0xd8116003', _decode_unknown_0xd8116003),
    0x415046ed: ('unknown_0x415046ed', _decode_unknown_0x415046ed),
    0xec9c01b2: ('unknown_0xec9c01b2', _decode_unknown_0xec9c01b2),
    0x545540e5: ('unknown_0x545540e5', _decode_unknown_0x545540e5),
    0x5490e214: ('power_beam_refresh_effect', _decode_power_beam_refresh_effect),
    0x887e8a8b: ('hit_radius', _decode_hit_radius),
    0xb7f5646d: ('hit_offset', _decode_hit_offset),
    0x41b72b2c: ('effect_offset', _decode_effect_offset),
    0xbbbee60b: ('unknown_0xbbbee60b', _decode_unknown_0xbbbee60b),
}
